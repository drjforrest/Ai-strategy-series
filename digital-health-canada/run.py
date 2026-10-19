"""Agentic seeker/extractor for Digital Health Canada's public communications.

Run:
  python run.py --mode site            # mine digitalhealthcanada.com (default)
  python run.py --mode radar           # Tavily-powered sweep of Canadian digital health / informatics
  python run.py --mode radar --mission "..." --max-steps 40
"""

from __future__ import annotations

import argparse
import os
import sys

from dhc_agent import config
from dhc_agent.agent import Agent, AgentBudgetExceeded
from dhc_agent.report import write_report
from dhc_agent.tools import NotesStore


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=["site", "radar"],
        default="site",
        help="site = mine Digital Health Canada's own site (default); radar = Tavily-powered sweep of "
        "Canadian digital health / health informatics across the web.",
    )
    parser.add_argument("--mission", default=None, help="Override the mission (default depends on --mode).")
    parser.add_argument("--model", default=config.DEFAULT_MODEL, help="OpenRouter model id (must support tool calling).")
    parser.add_argument("--max-steps", type=int, default=None, help="Maximum agent reasoning/tool-calling steps (radar defaults to 30).")
    args = parser.parse_args(argv)

    if not config.OPENROUTER_API_KEY:
        print(
            "ERROR: OPENROUTER_API_KEY is not set.\n"
            "  - Copy .env.example to .env and fill in your key (https://openrouter.ai/keys), or\n"
            "  - export OPENROUTER_API_KEY=sk-or-v1-..."
        )
        return 2

    mission = args.mission or (config.RADAR_MISSION if args.mode == "radar" else config.DEFAULT_MISSION)
    max_steps = args.max_steps or (30 if args.mode == "radar" else 25)

    if args.mode == "radar" and not os.getenv("TAVILY_API_KEY"):
        print(
            "ERROR: radar mode needs TAVILY_API_KEY (it leans on Tavily search).\n"
            "  - Get a key at https://app.tavily.com and add TAVILY_API_KEY=... to .env"
        )
        return 2

    notes = NotesStore()
    transcript: list[str] = []
    agent = Agent(
        model=args.model,
        max_steps=max_steps,
        mode=args.mode,
        notes=notes,
        transcript=transcript,
    )

    print(f"== DHCAgent | mode={args.mode} | model={args.model} | max_steps={max_steps}")
    print(f"== Output directory: {config.OUTPUT_DIR.resolve()}")
    print(f"== Mission: {mission[:120]}{'...' if len(mission) > 120 else ''}\n")

    finished = False
    try:
        final_answer = agent.run(mission)
        finished = True
    except AgentBudgetExceeded as exc:
        final_answer = (
            f"## Incomplete run\n\n{exc}\n\n"
            "The notes below were saved before the budget ran out."
        )
        print(f"WARNING: {exc}")
    except Exception as exc:
        import traceback

        final_answer = f"## Failed run\n\nAgent terminated with an error: {exc}"
        print(f"ERROR: {exc}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

    report_path = write_report(
        mission=mission,
        model=args.model,
        final_answer=final_answer,
        notes=notes.records,
        transcript=transcript,
        finished=finished,
    )

    print(f"\n== Findings: {config.FINDINGS_JSONL}")
    print(f"== Report:   {config.REPORT_MD}  (JSON: {config.REPORT_JSON})")
    print(f"== Downloads:{config.DOWNLOADS_DIR}")
    print(f"== Transcript: {config.TRANSCRIPT_MD}")
    print(f"== Tokens: {agent.tokens_prompt:,} in / {agent.tokens_completion:,} out "
          f"(est. cost ${agent.estimated_cost_usd():.4f})")
    return 0 if finished else 1


if __name__ == "__main__":
    sys.exit(main())
