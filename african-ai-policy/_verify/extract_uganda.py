"""Extract the Uganda Digital Transformation Roadmap to data/digital_health_strategies/uganda_dh.txt.

Uses the project's own extraction + cleaning path (pdfplumber + preprocess.clean_text)
so the secondary-track text is produced the same way as the primary extracts.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pdfplumber
from src import preprocess

SRC = pathlib.Path("data/digital_health_strategies/Uganda Digital Transformation Roadmap.pdf")
DST = pathlib.Path("data/digital_health_strategies/uganda_dh.txt")

with pdfplumber.open(SRC) as pdf:
    n_pages = len(pdf.pages)
    pages = [p.extract_text() or "" for p in pdf.pages]

body = preprocess.clean_text("\n\n".join(pages))
DST.write_text(body, encoding="utf-8")

raw_words = sum(len(p.split()) for p in pages)
clean_words = len(body.split())
print(f"  pages:            {n_pages}")
print(f"  raw words:        {raw_words:,}")
print(f"  cleaned words:    {clean_words:,}")
print(f"  chars:            {len(body):,}")
print(f"  wrote:            {DST}")
print()
print("  --- first 300 chars ---")
print("  " + body[:300].replace("\n", "\n  "))
