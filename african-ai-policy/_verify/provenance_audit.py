"""Provenance audit: is every corpus .txt backed by a genuine source PDF?

For each of the 15 corpus extracts, score every candidate PDF in the directory
by shared 8-gram coverage and report the best match. Flags:
  * extracts with no plausible source  (coverage below threshold)
  * PDFs that match no extract          (possible AI derivatives / duplicates)
"""
import re, sys
from pathlib import Path

D = Path("data/national_strategies")
MAX_PAGES = 40          # cap for speed; matching does not need every page
THRESH = 15.0           # % of corpus-extract 8-grams that must be shared

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower())

def pdf_text(p: Path) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(p) as pdf:
            pages = pdf.pages[:MAX_PAGES]
            return norm(" ".join((pg.extract_text() or "") for pg in pages))
    except Exception as e:
        return f"__ERROR__{e}"

def grams(s: str, n: int = 8):
    w = s.split()
    return {" ".join(w[i:i+n]) for i in range(0, max(1, len(w)-n), 3)}

txts = {p.stem.replace("_ai", ""): norm(p.read_text(errors="ignore"))
        for p in sorted(D.glob("*_ai.txt"))}
pdfs = sorted(D.glob("*.pdf"))
print(f"{len(txts)} corpus extracts x {len(pdfs)} candidate PDFs\n")

tg = {k: grams(v) for k, v in txts.items()}
pt = {}
for p in pdfs:
    t = pdf_text(p)
    pt[p.name] = t
    if t.startswith("__ERROR__"):
        print(f"  ! extraction failed: {p.name} -> {t[:80]}")

print("\n=== best source match per extract ===")
used = set()
for stem in sorted(tg):
    best, best_cov = None, 0.0
    for name, t in pt.items():
        if t.startswith("__ERROR__"):
            continue
        g = grams(t)
        if not g:
            continue
        inter = len(tg[stem] & g)
        cov = 100 * inter / max(1, len(tg[stem]))
        if cov > best_cov:
            best, best_cov = name, cov
    used.add(best)
    flag = "OK " if best_cov >= THRESH else "!! "
    print(f"  {flag}{stem:16s} <- {str(best)[:52]:54s} {best_cov:5.1f}%")

print("\n=== PDFs matching no corpus extract ===")
unmatched = [n for n in pt if n not in used]
if unmatched:
    for n in unmatched:
        print(f"  !! {n}  ({len(pt[n].split())} words extracted)")
else:
    print("  none")

print("\n=== word counts (extract vs best PDF) ===")
for stem in sorted(tg):
    print(f"  {stem:16s} txt={len(txts[stem].split()):6d} words")
