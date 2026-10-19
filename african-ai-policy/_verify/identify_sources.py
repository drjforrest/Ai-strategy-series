"""Identify which source PDF backs each corpus .txt extract.

Compares distinctive phrases from the .txt against text extracted from each
candidate PDF, so file moves are evidence-based rather than guessed.
"""
import re, sys
from pathlib import Path

D = Path("data/national_strategies")

def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"\s+", " ", s)
    return s

def pdf_text(p: Path) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(p) as pdf:
            return norm(" ".join((pg.extract_text() or "") for pg in pdf.pages))
    except Exception as e:
        return f"__ERROR__ {e}"

txt = norm((D / "kenya_ai.txt").read_text(errors="ignore"))
print(f"kenya_ai.txt: {len(txt)} chars, {len(txt.split())} words")

# distinctive phrases from the corpus extract
probes = [
    "artificial intelligence", "national ai strategy", "kenya",
    "ministry of information", "data protection", "digital economy",
    "2025", "2030",
]
print("\nprobe counts in kenya_ai.txt:")
for p in probes:
    print(f"  {p:24s} {txt.count(p)}")

for name in ["Kenya AI Strategy 2025 - 2030.pdf",
             "Kenya_National_AI_Strategy_2025-2030.pdf"]:
    p = D / name
    t = pdf_text(p)
    ok = not t.startswith("__ERROR__")
    print(f"\n=== {name} ({p.stat().st_size/1e6:.2f} MB) ===")
    if not ok:
        print("  extraction failed:", t[:120]); continue
    print(f"  extracted: {len(t)} chars, {len(t.split())} words")
    for pr in probes:
        print(f"    {pr:24s} {t.count(pr)}")
    # similarity via shared 8-gram coverage
    def grams(s, n=8):
        w = s.split()
        return {" ".join(w[i:i+n]) for i in range(0, max(1, len(w)-n), 3)}
    g1, g2 = grams(txt), grams(t)
    if g2:
        inter = len(g1 & g2)
        print(f"  shared 8-grams: {inter} / {len(g1)} "
              f"({100*inter/max(1,len(g1)):.1f}% of corpus extract)")
