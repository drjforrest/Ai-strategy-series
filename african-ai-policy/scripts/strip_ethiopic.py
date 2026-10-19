"""Strip Amharic (Ethiopic script) from a bilingual Amharic/English strategy text.

The Ethiopian National AI Policy (June 2024) is published as a bilingual
Amharic/English document. The embedding model (paraphrase-multilingual-MiniLM-L12-v2)
does not cover Amharic, and the operationalization / AI-density lexicons are EN+FR,
so the Amharic half is removed and only the English text is analysed.

Rule: drop any line in which Ethiopic characters (U+1200-U+139F, U+2D80-U+2DDF,
U+AB00-U+AB2F) make up >= 20% of non-space characters; then remove any residual
Ethiopic tokens from the remaining lines. Run after scripts.extract_pdfs:

    python -m scripts.strip_ethiopic data/national_strategies/ethiopia_ai.txt
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ETHIOPIC = re.compile(r"[\u1200-\u139F\u2D80-\u2DDF\uAB00-\uAB2F]")
LINE_THRESHOLD = 0.20


def strip(text: str) -> tuple[str, dict]:
    kept, dropped = [], 0
    for line in text.splitlines():
        chars = [c for c in line if not c.isspace()]
        share = (len(ETHIOPIC.findall(line)) / len(chars)) if chars else 0.0
        if share >= LINE_THRESHOLD:
            dropped += 1
            continue
        cleaned = " ".join(tok for tok in line.split(" ") if not ETHIOPIC.search(tok))
        kept.append(cleaned)
    out = re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).strip() + "\n"
    stats = {"lines_dropped": dropped, "words_before": len(text.split()),
             "words_after": len(out.split()), "ethiopic_left": len(ETHIOPIC.findall(out))}
    return out, stats


def main() -> int:
    path = Path(sys.argv[1])
    out, stats = strip(path.read_text(encoding="utf-8"))
    path.write_text(out, encoding="utf-8")
    print(f"{path.name}: {stats}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
