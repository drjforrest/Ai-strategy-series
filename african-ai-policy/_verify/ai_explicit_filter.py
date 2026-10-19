"""Comparative country results with vs without AI-explicit-only filter.

Filter = AI-term density (per 1,000 words). Ethiopia (1.87) is the only primary
entry that is not AI-explicit; Morocco (26.1) is AI-explicit despite being a
report, so it is RETAINED.
"""
import pandas as pd, numpy as np

meta = pd.read_csv("data/corpus_metadata.csv")
prim = meta[meta.collection == "AI strategies"]
AI_EXPLICIT = set(prim[prim.ai_density_per_1k >= 5].country)     # threshold well above DT band
print("AI-explicit set:", sorted(AI_EXPLICIT))
print("excluded from primary:", sorted(set(prim.country) - AI_EXPLICIT), "\n")

# ---- 1. WHO alignment ----
al = pd.read_csv("outputs/alignment_scores.csv")
dom = al.groupby("country").similarity_score.mean().sort_values(ascending=False)
print("=== 1. WHO competency alignment (mean over 9 domains) ===")
print(f"  full  : max {dom.max():.3f} ({dom.idxmax()})  min {dom.min():.3f}  n={len(dom)}")
w = dom[dom.index.isin(AI_EXPLICIT)]
print(f"  filtered: max {w.max():.3f} ({w.idxmax()})  min {w.min():.3f}  n={len(w)}")
print("\n  rank  country           full   filtered")
for i, c in enumerate(dom.index, 1):
    if c in AI_EXPLICIT:
        print(f"  {i:4d}  {c:17s} {dom[c]:.3f}  {list(w.index).index(c)+1}")
    else:
        print(f"  {i:4d}  {c:17s} {dom[c]:.3f}  EXCLUDED")

# ---- 2. operationalization ----
op = pd.read_csv("outputs/operationalization/operationalization_index.csv")
op = op[op.country != "African Union"]
L = ["timelines","budget","agencies","regulatory","monitoring","implementation"]
op["breadth"] = op[[f"{k}_covered" for k in L]].mean(axis=1)
op = op.sort_values("breadth", ascending=False)
print("\n=== 2. operationalization breadth (of 6 levers) ===")
for _, r in op.iterrows():
    tag = "" if r.country in AI_EXPLICIT else "   <- excluded"
    print(f"  {r.country:17s} {r.breadth:.3f}{tag}")
print(f"  median full: {op.breadth.median():.3f} | median filtered: {op[op.country.isin(AI_EXPLICIT)].breadth.median():.3f}")

# ---- 3. AU convergence ----
s1 = pd.read_csv("outputs/au_convergence/table_s1_convergence.csv").sort_values("convergence_r", ascending=False)
s1["new_rank"] = s1.country.apply(lambda c: sorted(s1[s1.country.isin(AI_EXPLICIT)].convergence_r, reverse=True).index(s1[s1.country==c].convergence_r.iloc[0]) + 1 if c in AI_EXPLICIT else None)
print("\n=== 3. AU convergence (10% rule) ===")
print("  rank  country            r       filtered-rank")
for i, (_, r) in enumerate(s1.iterrows(), 1):
    fr = f"{int(r.new_rank):2d}" if pd.notna(r.new_rank) else "EXCLUDED"
    print(f"  {i:4d}  {r.country:17s} {r.convergence_r:+.3f}   {fr}")

# ---- 4. guard ----
rr = pd.read_csv("outputs/rhetoric_vs_readiness/rhetoric_vs_readiness.csv")
print("\n=== 4. circularity guard ===")
print("  guard countries:", sorted(rr.country.unique()))
print("  Ethiopia in guard:", "Ethiopia" in set(rr.country), "-> guard UNAFFECTED by this filter")
