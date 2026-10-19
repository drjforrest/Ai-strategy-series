# Digital Health Canada — Agentic News/Newsletter Extractor

An agentic Python program that uses a model served by **OpenRouter** to **seek, download, and
extract** information from the public communications of
[Digital Health Canada](https://digitalhealthcanada.com/) — news releases / communiqués,
newsletter archives, annual reports, and podcasts.

The agent runs a ReAct-style loop: it reasons, calls tools (web search, page fetch, file
download, PDF/DOCX extraction), observes the results, saves structured findings, and finally
writes a sourced digest to `output/report.md`.

## How it works

```
┌────────────┐   tools   ┌──────────────────────────────┐
│  OpenRouter│ ◄───────► │ web_search / tavily_search /  │
│  model     │           │ fetch_page / download_file /  │
│ (agent)    │           │ extract_text / save_notes /   │
└────────────┘           │ read_notes                    │
                        └──────────────┬───────────────┘
                                        │ saves findings
                              ┌─────────▼─────────┐
                              │ output/           │
                              │  downloads/       │  ← PDFs, DOCX, …
                              │  findings.jsonl   │  ← structured notes
                              │  findings.md      │
                              │  report.md        │  ← final digest + sources
                              │  transcript.md    │
                              └───────────────────┘
```

- **Model**: any tool-calling model on OpenRouter (default `openai/gpt-4o-mini`; change via
  `OPENROUTER_MODEL`). For radar mode, **`openai/gpt-4.1-mini` is recommended** — `gpt-4o-mini`
  meets coverage quotas but pads with irrelevant items; the slightly pricier 4.1-mini stays on-
  topic (~$0.10 per full radar sweep). Runs report their token usage and estimated cost.
- **Search**: `tavily_search` (deep, dated results, news-topic filtering) is the radar mode's
  primary tool; `web_search` uses Tavily when `TAVILY_API_KEY` is set, else DuckDuckGo via
  the `ddgs` package.
- **Extraction**: `pypdf` for PDFs, `python-docx` for DOCX, BeautifulSoup for HTML.
- **Modes**: `--mode site` focuses on digitalhealthcanada.com itself; `--mode radar` sweeps
  the wider Canadian digital-health / informatics landscape.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then edit .env and paste your OpenRouter API key
```

Get a key at <https://openrouter.ai/keys> (you must add a small credit balance; keys start
with `sk-or-v1-`).

## Usage

### Site mode (default) — mine Digital Health Canada's own site

```bash
python run.py
```

### Radar mode — Tavily-powered sweep of Canadian digital health / informatics

Sweeps the web for recent, notable developments across three themes: Digital Health Canada
the organization, digital health in Canada broadly (policy, programs, funding, AI), and
Canadian health informatics (research, academia, practice). **Requires a Tavily API key**
(<https://app.tavily.com>):

```bash
python run.py --mode radar
python run.py --mode radar --max-steps 40     # bigger sweep
```

Custom mission / model / budget (either mode):

```bash
python run.py \
  --mission "Find Digital Health Canada news releases from the last 3 months and any public newsletter archive; summarize each with dates and URLs." \
  --model "anthropic/claude-3.5-sonnet" \
  --max-steps 30
```

Results land in `output/`:

| File | Contents |
|---|---|
| `output/report.md` | Final digest with sections + every source URL |
| `output/report.json` | Same, machine-readable |
| `output/findings.jsonl` / `.md` | One structured note per extracted item |
| `output/downloads/` | Downloaded PDF/DOCX newsletters & reports |
| `output/transcript.md` | Full agent/tool trace |

## Seed sources (verified Aug 2026)

- News / communiqués: <https://digitalhealthcanada.com/news/> (paginated as `/news/page/N/`)
- Newsletter sign-up: <https://digitalhealthcanada.com/sign-up-for-news/> (archives, when
  public, are typically hosted on third-party platforms — the agent searches for them)
- Annual reports: <https://digitalhealthcanada.com/about/annual-reports/>,
  <https://digitalhealthcanada.com/annual-report-2025-26/>
- Podcasts: <https://digitalhealthcanada.com/podcasts/>

## Notes & etiquette

- The fetcher sends a descriptive `User-Agent`, retries with backoff, and stays on
  public, non-authenticated pages. Don't hammer the site: keep `--max-steps` reasonable.
- Only facts actually found in fetched content are reported — the agent is instructed not to
  invent dates, figures, or quotes, and to say explicitly when something (e.g. a members-only
  newsletter archive) is not publicly available.
- Some pages are JS-rendered and may return little text; `fetch_page` returns the links it
  does find so the agent can still navigate.

## Extending

- Add seed URLs / tweak the default mission: `dhc_agent/config.py`.
- Change tool behaviour (truncation limits, noise tags, search backend): `dhc_agent/tools.py`.
- Adjust the agent's working instructions: `SYSTEM_PROMPT` in `dhc_agent/agent.py`.
