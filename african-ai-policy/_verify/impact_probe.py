import pandas as pd, numpy as np, sys
sys.path.insert(0, '.')
pd.set_option('display.width', 200)

al = pd.read_csv('outputs/alignment_scores.csv')
OLD = ["Benin","Côte d'Ivoire","Egypt","Ghana","Kenya","Mauritius","Morocco",
       "Nigeria","Rwanda","Senegal","South Africa","Zimbabwe"]
NEW = ["Ethiopia","Tanzania"]

print("=== A. Figure 1: z depends on who is pooled ===")
mat = al.pivot(index='country', columns='competency_id', values='similarity_score')
CID = [f'C{i}' for i in range(1,10)]
print("  today   :", len([c for c in mat.index if c!='African Union']), "national")
print("  ms says : 12 national")

print("\n=== B. Table 2: needs Oxford 2024 dimension rows ===")
panel = pd.read_csv('data/oxford_readiness_indices/processed/oxford_panel_2021_2024_tidy.csv')
dims = panel[(panel.level=='dimension') & (panel.year.astype(str)=='2024')]
ox = sorted(dims.country.unique())
print("  2024 Oxford countries (n=%d): %s" % (len(ox), ox))
for c in NEW:
    print(f"    {c:10s} in Oxford 2024 panel? {'YES' if c in ox else 'NO'}")
print(f"  -> Table 2 join: {len(sorted(set(ox) & set(mat.index)))} countries")

print("\n=== C. Convergence ranking: 12- vs 14-country pool ===")
def conv(pool):
    m = mat.loc[pool + ['African Union'], CID]
    mu = m.loc[pool].mean(axis=0)
    sd = m.loc[pool].std(axis=0, ddof=0).replace(0,1.0)
    z = (m - mu)/sd
    a = z.loc['African Union', CID].to_numpy(float); a = a - a.mean()
    out = {}
    for c in pool:
        v = z.loc[c, CID].to_numpy(float); v = v - v.mean()
        out[c] = float(v @ a / (np.linalg.norm(v)*np.linalg.norm(a)))
    return pd.Series(out).sort_values(ascending=False)

c12, c14 = conv(OLD), conv(NEW + OLD)
cmp = pd.DataFrame({'r_12country': c12, 'r_14country': c14})
cmp['rank_12'] = c12.rank(ascending=False).astype(int)
cmp['rank_14'] = c14.rank(ascending=False).astype(int)
cmp['shift'] = cmp['rank_14'] - cmp['rank_12']
print(cmp.sort_values('r_12country', ascending=False).round(3).to_string())
print(f"\n  Spearman(12 vs 14 rankings) = {c12.corr(c14, method='spearman'):.3f}")
print(f"  Rwanda r: {c12['Rwanda']:+.3f} -> {c14['Rwanda']:+.3f} "
      f"(rank {int(cmp.loc['Rwanda','rank_12'])} -> {int(cmp.loc['Rwanda','rank_14'])})")
