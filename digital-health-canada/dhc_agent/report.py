"""Write the final report (Markdown + JSON) from the agent run."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from . import config
from .tools import Note


def write_report(
    *,
    mission: str,
    model: str,
    final_answer: str,
    notes: list[Note],
    transcript: list[str],
    finished: bool,
) -> Path:
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # --- transcript ------------------------------------------------------- #
    with open(config.TRANSCRIPT_MD, "w", encoding="utf-8") as fh:
        fh.write(f"# Agent transcript\n\nRun at {now}\n\n")
        fh.write("\n".join(f"- {line}" for line in transcript))
        fh.write("\n")

    # --- markdown report --------------------------------------------------- #
    md = [
        "# Digital Health Canada — Communications Digest",
        "",
        f"- Generated: {now}",
        f"- Model: {model}",
        f"- Mission: {mission}",
        f"- Items extracted: {len(notes)}",
        "",
        "---",
        "",
        final_answer,
        "",
        "---",
        "",
        "## Extracted findings (raw notes)",
        "",
    ]
    if not notes:
        md.append("_No notes were saved during this run._")
    for rec in notes:
        md.append(
            f"### {rec['n']}. {rec['title']}\n\n"
            f"- Date: {rec.get('date') or 'n/a'}\n"
            f"- Type: {rec.get('doc_type')}\n"
            f"- Theme: {rec.get('theme', 'other')}\n"
            f"- Source: {rec.get('source_url')}\n\n"
            f"{rec.get('summary')}\n"
        )
    with open(config.REPORT_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")

    # --- JSON report ------------------------------------------------------- #
    payload = {
        "generated_at": now,
        "model": model,
        "mission": mission,
        "finished": finished,
        "final_answer": final_answer,
        "findings": notes,
    }
    with open(config.REPORT_JSON, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)

    return config.REPORT_MD
