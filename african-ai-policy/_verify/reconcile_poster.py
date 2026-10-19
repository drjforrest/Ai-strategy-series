"""Reconcile every number in the HIMSS27 poster abstract against the repo."""
import pandas as pd, numpy as np

pd.set_option('display.width', 200)

# ---- 1. WHO competency alignment (domain-level, 15 entries) ----
al = pd.read_csv("outputs/alignment_scores.csv")
dom = al.groupby('country')['similarity_score'].mean().sort_values(ascending=False)
print("=== mean WHO alignment, 15 entries ===")
for i,(c,v) in enumerate(dom.items(),1):
    print(f"  {i:2d}. {c:16s} {v:.3f}")
print(f"  range: {dom.min():.3f} - {dom.max():.3f}")

# ---- 2. operationalization breadth ----
op = pd.read_csv("outputs/operationalization/operationalization_index.csv")
op = op[op.country != "African Union"].copy()
L = ['timelines','budget','agencies','regulatory','monitoring','implementation']
op['breadth'] = op[[f'{k}_covered' for k in L]].mean(axis=1)
op = op.sort_values('breadth', ascending=False)
print("\n=== operationalization breadth (6 levers) ===")
for _,r in op.iterrows():
    cov = "".join('1' if r[f'{k}_covered'] else '0' for k in L)
    print(f"  {r.country:16s} {r.breadth:.3f}  [{cov}]")
print(f"  median breadth: {op.breadth.median():.3f}")

# ---- 3. rhetoric vs readiness guard ----
pc = pd.read_csv("outputs/rhetoric_vs_readiness/per_dimension_correlation.csv")
tp = pc[pc.text_proximate].pearson_r; ind = pc[~pc.text_proximate].pearson_r
print("\n=== circularity guard ===")
for _,r in pc.iterrows():
    print(f"  {r.dimension:22s} {r.pearson_r:+.4f}  text_proximate={r.text_proximate}")
print(f"  text-proximate mean r = {tp.mean():+.3f}   independent mean r = {ind.mean():+.3f}")
rr = pd.read_csv("outputs/rhetoric_vs_readiness/rhetoric_vs_readiness.csv")
r_pooled = np.corrcoef(rr.rhetoric_z, rr.readiness_z)[0,1]
print(f"  pooled r = {r_pooled:+.4f}   n cells = {len(rr)}")

# ---- 4. AU convergence ----
s1 = pd.read_csv("outputs/au_convergence/table_s1_convergence.csv")
s2 = pd.read_csv("outputs/au_convergence/table_s2_threshold_sensitivity.csv")
print("\n=== AU convergence (10% threshold) ===")
for _,r in s1.head(5).iterrows():
    print(f"  {r['rank']:2d}. {r.country:16s} r = {r.convergence_r:+.2f}")
print("  --- threshold sensitivity (rank 1) ---")
for _,r in s2.iterrows():
    print(f"  {r.threshold:>4s} -> {r.rank1:16s} r = {r.rank1_r:.2f}  top3: {r.top3}")

# ---- 5. guard leave-one-out ----
lo = pd.read_csv("outputs/rhetoric_vs_readiness/guard_leave_one_out.csv")
print(f"\n=== leave-one-out: significant in {lo.sig.sum()}/{len(lo)}; "
      f"Morocco p={lo[lo.dropped=='Morocco'].p.iloc[0]:.3f}")
