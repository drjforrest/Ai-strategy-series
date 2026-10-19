"""Which PDF backs benin_ai.txt and nigeria_ai.txt?"""
import re
from pathlib import Path

D = Path("data/national_strategies")

def norm(s):
    return re.sub(r"\s+", " ", s.lower())

def pdf_text(p: Path) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(p) as pdf:
            return norm(" ".join((pg.extract_text() or "") for pg in pdf.pages))
    except Exception as e:
        return f"__ERROR__ {e}"

def grams(s, n=8):
    w = s.split()
    return {" ".join(w[i:i+n]) for i in range(0, max(1, len(w)-n), 3)}

targets = {
    "benin_ai.txt":    D / "benin_ai.txt",
    "nigeria_ai.txt":  D / "nigeria_ai.txt",
}
cands = [
    "national-artificial-intelligence-and-big-data-strategy-1682673348.pdf",
    "National-Artificial-Intelligence-Strategy-19092025.pdf",
]

tg = {k: grams(norm(p.read_text(errors="ignore"))) for k, p in targets.items()}
for k, v in targets.items():
    t = norm(v.read_text(errors="ignore"))
    print(f"{k}: {len(t.split())} words")
    print(f"   probes -> benin:{t.count('benin')} nigeria:{t.count('nigeria')} "
          f"big data:{t.count('big data')}")

print()
for name in cands:
    p = D / name
    t = pdf_text(p)
    print(f"=== {name} ({p.stat().st_size/1e6:.2f} MB) ===")
    if t.startswith("__ERROR__"):
        print("  ", t[:110]); continue
    print(f"   {len(t.split())} words | benin:{t.count('benin')} "
          f"nigeria:{t.count('nigeria')} big data:{t.count('big data')}")
    g = grams(t)
    for k, src in tg.items():
        inter = len(src & g)
        print(f"   shared 8-grams with {k:16s}: {inter:5d} "
              f"({100*inter/max(1,len(src)):.1f}%)")
