"""The agent loop: an OpenRouter-hosted model (via the OpenAI SDK) plans,
calls tools, observes results, and iterates until it produces a final answer.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from typing import cast, final

from openai import OpenAI
from openai.types.chat import (
    ChatCompletion,
    ChatCompletionMessageParam,
    ChatCompletionToolUnionParam,
)

from . import config
from .tools import TOOL_SCHEMAS, NotesStore, ToolRunner

SYSTEM_PROMPT = """You are DHCAgent, an autonomous research assistant that finds, downloads, and extracts
information from the PUBLIC communications of Digital Health Canada (digitalhealthcanada.com),
Canada's professional association for digital health. Today's date is {today}.

## Scope
Relevant public material includes:
- News releases / communiqués at https://digitalhealthcanada.com/news/ (paginated: add /page/N/).
- Newsletter archives (sign-up page: https://digitalhealthcanada.com/sign-up-for-news/).
  Public archives are often hosted on third-party email platforms (e.g. Constant Contact) - use
  web_search to find them.
- Annual reports: https://digitalhealthcanada.com/about/annual-reports/ and
  https://digitalhealthcanada.com/annual-report-2025-26/
- Podcasts at https://digitalhealthcanada.com/podcasts/ (optional).

## Working style
1. Start from the seed URLs above; use fetch_page on listing pages to discover article links.
2. Fetch the actual article/report pages before summarizing anything. Never invent facts.
3. When a page links to a PDF/DOCX (newsletter, report), use download_file to save it and
   extract_text to read it.
4. After extracting an item's key information, immediately call save_notes with a concise,
   factual summary (include names, dates, figures, and the source URL).
5. Use web_search to locate material that is not obvious from the site (e.g. newsletter archives,
   press mentions hosted elsewhere).
6. Before your final answer, call read_notes so the report is grounded in what was extracted.

## Efficiency
You have a bounded step budget. Be strategic: sample the most relevant pages, don't re-fetch the
same URL twice, and don't exhaust the budget on one section while ignoring the others. If a
section is not publicly available (e.g. newsletter archives are members-only), say so explicitly
rather than guessing.

## Output
End with a structured final answer (no tool calls) in Markdown:
# Digital Health Canada - Communications Digest
- Run metadata (date, model, sources consulted count)
## 1. News / Communiqués (recent highlights, each with date, title, key facts, URL)
## 2. Newsletters (what was found and where; note if archive is not public)
## 3. Annual reports & other publications
## 4. Notable topics / themes
## 5. Sources (all URLs consulted)
"""

RADAR_SYSTEM_PROMPT = """You are DHCRadar, an autonomous intelligence agent sweeping the web for developments in
Canadian digital health and health informatics, powered by Tavily search. Today's date is {today}.

## Mandate (three themes)
1. **dhc_org** - Digital Health Canada the organization: announcements, news releases, leadership
   changes, reports, events (e-Health conference, CHIEF Executive Forum, Webinar Wednesdays), awards.
2. **digital_health_canada** - Digital health in Canada broadly: federal/provincial policy and
   programs (Canada Health Infoway, CIHI, Connected Care for Canadians Act / Bill C-72), funding,
   AI in healthcare, EHR/EMR initiatives, telehealth/virtual care, cybersecurity, provincial agencies.
3. **health_informatics** - Canadian health informatics: research and academic programs, conferences
   and associations (e-Health, HIMSS, AMIA-adjacent Canadian groups), standards (HL7/FHIR), workforce.

## Working style
1. Prefer the tavily_search tool: mix topic=news (recency) and topic=general (depth), use
   timelimit to bound recency (day/week/month), and run several targeted queries PER theme.
   Use web_search as a backup when Tavily returns nothing useful.
2. Fetch promising pages with fetch_page before summarizing; never invent facts.
3. Download PDF reports/announcements with download_file and read them with extract_text.
4. For every distinct item, call save_notes immediately - set the theme field
   (dhc_org | digital_health_canada | health_informatics | other) and a factual summary with
   names, dates, figures, and the source URL. Use the item's ACTUAL publication date from the
   page - never today's date.
5. Skip obvious duplicates; prefer primary sources (official sites, agencies, journals) over
   aggregators.
6. Before your final answer, call read_notes to ground the digest in what was extracted.

## Mandatory coverage
DO NOT stop early. Your final answer will be rejected until EVERY theme has at least
{min_per_theme} saved notes. If a search returns nothing useful, refine the query (add
organization names such as Infoway, CIHI, HIMSS, e-Health; add '2026'; try topic=general when
topic=news is thin, and vice versa). Keep going until all three themes are covered.

## Relevance
Every saved note must be genuinely about Canada or a Canadian organization, and relevant to its
theme. Do NOT pad coverage with global market-size reports, listicles, or non-Canadian news.
Quality beats quantity: if you cannot find enough relevant items after several refined
queries, say so explicitly in the digest instead of inventing or padding.

## Efficiency
You have a bounded step budget; do not spend it all on one theme. If a query returns nothing
notable, say so rather than padding with stale results. Aim for breadth: a handful of strong
items per theme beats one theme exhaustively covered.

## Output
End with a structured final answer (no tool calls) in Markdown:
# Canadian Digital Health & Health Informatics - Intelligence Radar
- Run metadata (date, model, number of items)
## 1. Digital Health Canada (the organization)
## 2. Digital health in Canada (policy, programs, industry)
## 3. Canadian health informatics (research, academia, practice)
Each item: **date — title**, 2-4 bullet key facts, source URL.
## 4. Cross-cutting themes & signals
## 5. Sources (all URLs consulted)
"""

SYSTEM_PROMPTS = {"site": SYSTEM_PROMPT, "radar": RADAR_SYSTEM_PROMPT}


class AgentBudgetExceeded(Exception):
    pass


@final
class Agent:
    """ReAct loop over an OpenRouter model with function-calling tools."""

    def __init__(
        self,
        model: str = config.DEFAULT_MODEL,
        max_steps: int = 25,
        mode: str = "site",
        notes: NotesStore | None = None,
        transcript: list[str] | None = None,
    ):
        if mode not in SYSTEM_PROMPTS:
            raise ValueError(f"Unknown mode '{mode}'; expected one of {sorted(SYSTEM_PROMPTS)}")
        self.model = model
        self.max_steps = max_steps
        self.mode = mode
        self.system_prompt = SYSTEM_PROMPTS[mode]
        self.notes = notes or NotesStore()
        self.runner = ToolRunner(self.notes)
        self.transcript = transcript if transcript is not None else []
        self._pushbacks = 0
        self.tokens_prompt = 0
        self.tokens_completion = 0
        self.client = OpenAI(
            base_url=config.OPENROUTER_BASE_URL,
            api_key=config.OPENROUTER_API_KEY,
            default_headers={
                **({"HTTP-Referer": config.HTTP_REFERER} if config.HTTP_REFERER else {}),
                **({"X-Title": config.APP_TITLE} if config.APP_TITLE else {}),
            },
        )

    # -- internals ---------------------------------------------------------- #
    def _log(self, line: str) -> None:
        self.transcript.append(line)

    def _chat(self, messages: list[ChatCompletionMessageParam]) -> ChatCompletion:
        last_exc: Exception | None = None
        for attempt in range(3):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=cast(list[ChatCompletionToolUnionParam], TOOL_SCHEMAS),
                    tool_choice="auto",
                )
            except Exception as exc:  # transient OpenRouter / network errors
                last_exc = exc
                self._log(f"  [retry] model call failed ({exc}); attempt {attempt + 1}/3")
                time.sleep(2 * (attempt + 1))
                continue
            if not resp.choices:  # some providers intermittently return empty choices
                last_exc = RuntimeError("model returned no choices (empty response)")
                self._log(f"  [retry] {last_exc}; attempt {attempt + 1}/3")
                time.sleep(2 * (attempt + 1))
                continue
            if resp.usage:
                self.tokens_prompt += resp.usage.prompt_tokens or 0
                self.tokens_completion += resp.usage.completion_tokens or 0
            return resp
        raise RuntimeError(f"Model call failed after 3 attempts: {last_exc}")

    # -- coverage helpers --------------------------------------------------- #
    def _incomplete_themes(self) -> list[str]:
        counts = {n["theme"]: sum(1 for r in self.notes.records if r["theme"] == n["theme"]) for n in self.notes.records}
        counts.setdefault("dhc_org", 0)
        counts.setdefault("digital_health_canada", 0)
        counts.setdefault("health_informatics", 0)
        return [
            t for t in config.RADAR_THEME_KEYS
            if counts.get(t, 0) < config.RADAR_MIN_ITEMS_PER_THEME
        ]

    def estimated_cost_usd(self) -> float:
        prompt_price, completion_price = config.MODEL_PRICES_USD.get(self.model, config.DEFAULT_MODEL_PRICES_USD)
        return (self.tokens_prompt / 1_000_000 * prompt_price) + (
            self.tokens_completion / 1_000_000 * completion_price
        )

    # -- main loop ---------------------------------------------------------- #
    def run(self, mission: str) -> str:
        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": self.system_prompt.format(
                    today=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    min_per_theme=config.RADAR_MIN_ITEMS_PER_THEME,
                ),
            },
            {"role": "user", "content": mission},
        ]
        seed_list = "\n".join(f"- {k}: {v}" for k, v in config.SEED_URLS.items())
        messages.append(
            {"role": "user", "content": f"Seed URLs you can trust as starting points:\n{seed_list}"}
        )
        self._log(f"Model: {self.model} | mode: {self.mode} | max steps: {self.max_steps}")
        self._log(f"Mission: {mission}")

        for step in range(1, self.max_steps + 1):
            response = self._chat(messages)
            message = response.choices[0].message

            tool_calls = message.tool_calls or []
            if not tool_calls:
                final = (message.content or "").strip()
                if not final:
                    raise RuntimeError(
                        "Model returned an empty response without tool calls; try a different --model or a narrower --mission."
                    )
                # Radar coverage guardrail: reject early final answers that leave
                # a theme under-covered, and nudge the model to keep researching.
                if self.mode == "radar" and self._incomplete_themes() and self._pushbacks < config.RADAR_MAX_PUSHBACKS:
                    incomplete = self._incomplete_themes()
                    detail = ", ".join(
                        f"{t} ({sum(1 for n in self.notes.records if n['theme'] == t)}"
                        f"/{config.RADAR_MIN_ITEMS_PER_THEME} notes)"
                        for t in incomplete
                    )
                    self._pushbacks += 1
                    self._log(
                        f"[step {step}] coverage incomplete ({detail}); "
                        f"pushback {self._pushbacks}/{config.RADAR_MAX_PUSHBACKS} - asking model to continue"
                    )
                    messages.append(
                        {
                            "role": "user",
                            "content": (
                                "Your final answer was NOT accepted: these theme(s) still have fewer than "
                                f"{config.RADAR_MIN_ITEMS_PER_THEME} saved notes: {detail}. Keep researching them "
                                "(refine tavily_search queries - e.g. add organization/institution names - fetch "
                                "pages, save notes) until every theme has at least "
                                f"{config.RADAR_MIN_ITEMS_PER_THEME} items, then produce the final digest again."
                            ),
                        }
                    )
                    continue
                self._log(f"[step {step}] FINAL ANSWER ({len(final)} chars)")
                return final

            # Assistant message carrying tool calls must be kept in history.
            messages.append(
                cast(ChatCompletionMessageParam, cast(object, message.model_dump(exclude_none=True)))
            )
            self._log(f"[step {step}] model requests {len(tool_calls)} tool call(s)")
            for tc in tool_calls:
                if tc.type != "function":
                    continue  # custom tool-call variants are not handled
                try:
                    args = json.loads(tc.function.arguments or "{}")
                    pretty_args = ", ".join(f"{k}={v}" for k, v in list(args.items())[:4])
                except json.JSONDecodeError:
                    pretty_args = tc.function.arguments
                self._log(f"  -> {tc.function.name}({pretty_args})")
                result = self.runner.call(tc.function.name, tc.function.arguments)
                self._log(f"  <- {result[:200]}{'...' if len(result) > 200 else ''}")
                messages.append(
                    {"role": "tool", "tool_call_id": tc.id, "content": result}
                )

        raise AgentBudgetExceeded(
            f"Step budget ({self.max_steps}) exhausted. Notes saved: {len(self.notes.records)}. "
            + "Re-run with --max-steps N (larger) or --mission to narrow the scope."
        )
