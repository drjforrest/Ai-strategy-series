"""Does Ethiopia's digital-infrastructure peak survive a length-matched aggregation?

Recomputes the country x competency alignment from the CACHED chunk embeddings
(no re-embedding) under the manuscript's top-10% rule and under variants that
hold the number of averaged passages FIXED, then compares.
"""
import numpy as np, pandas as pd, glob, os, re

EMB = "outputs/embeddings"
comp = pd.read_csv("data/who_strategy/competencies.csv").set_index("competency_id")["name"]
C = np.load("outputs/competency_embeddings.npy")
Cn = C / np.linalg.norm(C, axis=1, keepdims=True)

def load():
    canon = {"ethiopia": "Ethiopia", "rwanda": "Rwanda", "ghana": "Ghana", "kenya": "Kenya",
             "mauritius": "Mauritius", "egypt": "Egypt", "nigeria": "Nigeria",
             "zimbabwe": "Zimbabwe", "tanzania": "Tanzania", "benin": "Benin",
             "morocco": "Morocco", "senegal": "Senegal", "cote_divoire": "Côte d'Ivoire",
             "south_africa": "South Africa", "african_union": "African Union"}
    out = {}
    for f in sorted(glob.glob(f"{EMB}/*_chunk_embeddings.npy")):
        stem = os.path.basename(f).replace("_ai_chunk_embeddings.npy", "")
        out[canon[stem]] = np.load(f)
    return out

def top_frac_mean(S, frac, floor):
    n = S.shape[0]
    k = max(min(floor, n), int(round(frac * n)))
    k = max(1, min(k, n))
    return np.partition(S, -k, axis=0)[-k:, :].mean(axis=0)

def top_k_mean(S, k):
    k = max(1, min(k, S.shape[0]))
    return np.partition(S, -k, axis=0)[-k:, :].mean(axis=0)

def agg(E, rule):
    Sn = E / np.linalg.norm(E, axis=1, keepdims=True)
    S = Sn @ Cn.T
    if rule[0] == "frac":  return top_frac_mean(S, rule[1], rule[2])
    if rule[0] == "k":     return top_k_mean(S, rule[1])
    if rule[0] == "mean":  return S.mean(axis=0)

E = load()
ids = list(comp.index)
rules = {
  "top10% (manuscript)": ("frac", 0.10, 3),
  "top 20%":             ("frac", 0.20, 3),
  "top 30%":             ("frac", 0.30, 3),
  "fixed top-5":         ("k", 5),
  "fixed top-10":        ("k", 10),
  "fixed top-20":        ("k", 20),
  "all-chunk mean":      ("mean",),
}
rows = {name: {} for name in rules}
for ctry, arr in E.items():
    for name, rule in rules.items():
        rows[name][ctry] = agg(arr, rule)

for name in rules:
    df = pd.DataFrame(rows[name], index=ids)
    c6 = df.loc["C6"]
    rank = int((c6 > c6["Ethiopia"]).sum()) + 1
    top = c6.sort_values(ascending=False)
    print(f"=== {name} ===")
    print("  C6 top5:", " | ".join(f"{c} {v:.3f}" for c, v in top.head(5).items()))
    print(f"  Ethiopia C6 = {c6['Ethiopia']:.3f}  rank {rank}/{len(c6)}")
    print()

# how much does each country's n_chunks drive its C6 score under top10%?
n10 = pd.Series({c: max(3, int(round(0.10 * a.shape[0]))) for c, a in E.items()})
c6_10 = pd.Series({c: agg(a, ("frac", 0.10, 3))[5] for c, a in E.items()})
print("=== top-10%: passages averaged vs C6 score ===")
j = pd.DataFrame({"n_chunks": {c: E[c].shape[0] for c in E},
                  "k_avg": n10, "C6": c6_10}).sort_values("C6", ascending=False)
print(j.round(3).to_string())
print("  corr(n_chunks, C6) =", round(np.corrcoef(j.n_chunks, j.C6)[0, 1], 3))
print("  corr(k_avg,    C6) =", round(np.corrcoef(j.k_avg, j.C6)[0, 1], 3))
