"""Re-check the flagged extracts with FULL page extraction (no page cap),
and test Ethiopia against the concatenation of its two documents."""
import re
from pathlib import Path

D = Path("data/national_strategies")

def norm(s): return re.sub(r"\s+", " ", s.lower())
def pdf_text(p):
    import pdfplumber
    with pdfplumber.open(p) as pdf:
        return norm(" ".join((pg.extract_text() or "") for pg in pdf.pages))
def grams(s, n=8):
    w = s.split()
    return {" ".join(w[i:i+n]) for i in range(0, max(1, len(w)-n), 3)}
def cov(a, b):
    ga, gb = grams(a), grams(b)
    return 100*len(ga & gb)/max(1, len(ga))

cases = {
 "egypt":     (["Egypt_National_AI_Strategy_2025-2030.pdf"], None),
 "ghana":     (["Ghana_National_AI_Strategy_2023-2033.pdf"], None),
 "mauritius": (["Mauritius AI Strategy.pdf"], None),
 "senegal":   (["Senegal_AI_Strategy_2023.pdf"], None),
 "ethiopia":  (["Digital Ethiopia 2025 Strategy_EN.pdf",
                "Digital Ethiopia 2030 Vision_EN.pdf"], "concat"),
 "african_union": ([], None),
}
AXF = "african_union_ai.txt"

for stem, (pdfs, mode) in cases.items():
    txt = norm((D / f"{stem}_ai.txt").read_text(errors="ignore"))
    print(f"\n=== {stem}  (extract {len(txt.split())} words) ===")
    if not pdfs:
        print("  NO source PDF present in the corpus directory")
        continue
    joined = []
    for name in pdfs:
        p = D / name
        if not p.exists():
            print(f"  ! missing {name}"); continue
        t = pdf_text(p)
        joined.append(t)
        print(f"  {name[:46]:48s} {len(t.split()):6d} words  "
              f"coverage={cov(txt, t):5.1f}%")
    if mode == "concat" and len(joined) > 1:
        c = " ".join(joined)
        print(f"  {'CONCATENATED both docs':48s} {len(c.split()):6d} words  "
              f"coverage={cov(txt, c):5.1f}%")

# does an AU strategy PDF exist anywhere in the repo?
print("\n=== African Union source hunt ===")
for p in Path("data").rglob("*"):
    if p.is_file() and re.search(r"afric|union|continental", p.name, re.I):
        print("  ", p, f"({p.stat().st_size/1e6:.2f} MB)")
