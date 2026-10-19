"""Per-entry corpus verification for Paper 1 (small corpus -> check every document).

For each candidate document it reports, from the local text alone:
  - word count
  - AI-term density overall and in the first / middle / last third
    (tests the "AI must be integral throughout, not concentrated late" rule that
    excluded Ethiopia)
  - a French-language signal (this corpus is multilingual)
  - the first ~90 characters (a sanity check that the file is the strategy)

Also scans data/_excluded, data/_rejected and data/inbox for any candidate file
NOT in the corpus, so nothing qualifying is missed.

Outputs: outputs/corpus_verification.csv

    ./run.sh verify_corpus.py
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

import pandas as pd

from src import config, preprocess

OUT = config.OUTPUTS_DIR / "corpus_verification.csv"

# Same bilingual AI term set as analyze_linkage.py — including the French "IA".
AI_RE = re.compile(
    r"\b(?:AI|IA|artificial\s+intelligence|intelligence\s+artificielle|"
    r"machine\s+learning|apprentissage\s+automatique)\b",
    re.IGNORECASE,
)
FR_RE = re.compile(r"\b(?:des|les|une|dans|pour|avec|selon|ainsi)\b", re.IGNORECASE)


def density(text: str) -> float:
    words = len(text.split())
    return round(1000.0 * len(AI_RE.findall(text)) / words, 2) if words else 0.0


def thirds(text: str) -> tuple[float, float, float]:
    words = text.split()
    n = len(words)
    if n < 3:
        return (0.0, 0.0, 0.0)
    a, b = n // 3, 2 * n // 3
    return (
        density(" ".join(words[:a])),
        density(" ".join(words[a:b])),
        density(" ".join(words[b:])),
    )


def read(path: Path) -> str:
    return preprocess.clean_text(preprocess.load_text(path))


def row_for(country: str, path: Path, in_corpus: bool) -> dict:
    text = read(path)
    words = len(text.split())
    first, mid, last = thirds(text)
    fr_hits = len(FR_RE.findall(text))
    return {
        "country": country,
        "file": path.name,
        "in_corpus": in_corpus,
        "words": words,
        "ai_density": density(text),
        "ai_first_third": first,
        "ai_mid_third": mid,
        "ai_last_third": last,
        "ai_min_third": round(min(first, mid, last), 2),
        "french_signal_per_1k": round(1000.0 * fr_hits / words, 1) if words else 0.0,
        "preview": text[:90].replace("\n", " "),
    }


def main() -> int:
    rows = []
    for c in config.COUNTRIES:
        p = config.country_path(c)
        if p.exists():
            rows.append(row_for(c, p, True))

    # Off-corpus candidates: make sure nothing qualifying was missed.
    for label, d in [
        ("excluded", config.DATA_DIR / "_excluded"),
        ("rejected", config.DATA_DIR / "_rejected"),
        ("inbox", config.DATA_DIR / "inbox"),
        ("other", config.DATA_DIR / "digital_health_strategies"),
    ]:
        if d.exists():
            for f in sorted(d.glob("*.txt")):
                rows.append(row_for(f"{label}:{f.stem}", f, False))

    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False)

    print("=== Papers 1 corpus — per-entry verification ===\n")
    cols = ["country", "words", "ai_density", "ai_first_third", "ai_mid_third",
            "ai_last_third", "ai_min_third", "french_signal_per_1k"]
    with pd.option_context("display.width", 200, "display.max_columns", 20):
        print(df[df.in_corpus][cols].to_string(index=False))

    print("\n=== Off-corpus candidates (verify nothing qualifying is missed) ===\n")
    off = df[~df.in_corpus][cols + ["file"]]
    print(off.to_string(index=False) if not off.empty else "  (none)")

    print(f"\nWrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
