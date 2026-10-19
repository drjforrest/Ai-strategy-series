"""Genre audit of the primary corpus + Kenya duplication check."""
import re, pathlib, pandas as pd

D = pathlib.Path("data/national_strategies")

# --- Kenya duplication check ---
k = (D / "kenya_ai.txt").read_text()
heads = [m.start() for m in re.finditer(r"KENYA\s+ARTIFICIAL\s+INTELLIGENCE\s+STRATEGY", k, re.I)]
marks = [m.start() for m in re.finditer(r"== source:", k)]
print("=== KENYA ===")
print(f"  title occurrences: {len(heads)} | source marks: {len(marks)}")
print(f"  total words: {len(k.split())}")
if len(marks) == 2:
    d1, d2 = k[marks[0]:marks[1]], k[marks[1]:]
    w1, w2 = len(d1.split()), len(d2.split())
    print(f"  doc1 {w1} words | doc2 {w2} words")
    a, b = set(d1.split()), set(d2.split())
    jac = len(a & b) / len(a | b)
    print(f"  token-set Jaccard overlap: {jac:.3f}  (>0.8 = same document)")

# --- genre map ---
GENRE = {
 "Benin":        ("National AI & Big Data Strategy (SNIAM)", "AI strategy"),
 "Côte d'Ivoire":("Stratégie IA à l'horizon 2030", "AI strategy"),
 "Egypt":        ("Egypt National AI Strategy, 2nd ed 2025-2030", "AI strategy"),
 "Ethiopia":     ("Digital Ethiopia 2025 + Digital Ethiopia 2030 Vision", "Digital transformation"),
 "Ghana":        ("Ghana National AI Strategy 2023-2033", "AI strategy"),
 "Kenya":        ("Kenya AI Strategy 2025-2030", "AI strategy"),
 "Mauritius":    ("The Mauritius Artificial Intelligence Strategy (WG report)", "AI strategy (report)"),
 "Morocco":      ("AI roadmap / conference-synthesis report", "AI roadmap"),
 "Nigeria":      ("National AI Strategy, Sept 2025", "AI strategy"),
 "Rwanda":       ("The National AI Policy", "AI policy"),
 "Senegal":      ("Stratégie de Développement de l'IA", "AI strategy"),
 "South Africa": ("Draft National AI Strategy (Gazette 2026)", "AI strategy (draft)"),
 "Tanzania":     ("National AI Strategy Framework (Draft v0.6)", "AI strategy (draft)"),
 "Zimbabwe":     ("Zimbabwe National AI Strategy 2026-2030", "AI strategy"),
 "African Union":("Continental AI Strategy", "AI strategy (continental)"),
}
print("\n=== GENRE MAP ===")
for c,(doc,g) in GENRE.items():
    print(f"  {c:15s} {g:24s} {doc[:52]}")

df = pd.DataFrame([{"country":c,"genre":g} for c,(d,g) in GENRE.items()])
print("\n=== counts ===")
print(df.genre.str.replace(r" \(.*\)","",regex=True).value_counts().to_string())
print(f"  AI-specific (incl. policy/roadmap/report/draft/continental): "
      f"{(df.genre.str.contains('AI')).sum()}/15")
print(f"  Pure digital-transformation: {(df.genre=='Digital transformation').sum()}/15")
