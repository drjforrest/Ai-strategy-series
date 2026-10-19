"""Convergence to the AU vision: Table S1 + S2, rebuilt for the CURRENT corpus.

Replaces _verify/v15*.py and v18_sens_final.py, whose hardcoded `name_map`
omitted Ethiopia and Tanzania and so crashed / silently dropped them. The country
list is derived from src.config.COUNTRY_FILES, so it cannot drift again.

Outputs (outputs/au_convergence/):
  table_s1_convergence.csv        rank, country, r at the prespecified 10%
  table_s2_threshold_sensitivity.csv   rank 1 and top-3 at 5/10/20% + Spearman
"""
from __future__ import annotations

import glob
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, ".")
from src import config

CID = [f"C{i}" for i in range(1, 10)]
ANCHOR = "African Union"

# stem (e.g. 'ethiopia') -> display name, derived from config so it always matches
NAME_BY_STEM = {
    fn.replace(".txt", "").replace("_ai", ""): name
    for name, fn in config.COUNTRY_FILES.items()
}
print(f"country map derived from config: {len(NAME_BY_STEM)} stems")
print("  includes Ethiopia/Tanzania:",
      "ethiopia" in NAME_BY_STEM, "tanzania" in NAME_BY_STEM)

# competency embeddings, L2-normalised
comp = np.load(config.COMPETENCY_EMBEDDINGS_NPY)
comp = comp / np.linalg.norm(comp, axis=1, keepdims=True)


def align(top_frac: float, floor: int = 3) -> pd.DataFrame:
    """top-fraction mean cosine per (country, competency) from passage embeddings."""
    rows = []
    for f in sorted(glob.glob(str(config.EMBEDDINGS_CACHE_DIR / "*_chunk_embeddings.npy"))):
        stem = (os.path.basename(f)
                .replace("_chunk_embeddings.npy", "")
                .replace("_ai", ""))
        if stem not in NAME_BY_STEM:
            print(f"  ! no display name for stem '{stem}' -- skipped")
            continue
        E = np.load(f)
        E = E / np.linalg.norm(E, axis=1, keepdims=True)
        S = E @ comp.T
        n = S.shape[0]
        k = min(n, max(floor, int(round(n * top_frac))))
        for j in range(9):
            rows.append({"country": NAME_BY_STEM[stem], "competency_id": CID[j],
                         "score": np.sort(S[:, j])[::-1][:k].mean(), "k": k})
    return pd.DataFrame(rows)


def convergence(long: pd.DataFrame) -> pd.Series:
    """Pearson r of within-competency-standardised profile vs the AU profile."""
    mat = long.pivot_table(index="country", columns="competency_id",
                           values="score", aggfunc="first")[CID]
    pool = [c for c in mat.index if c != ANCHOR]
    mu = mat.loc[pool].mean(axis=0)
    sd = mat.loc[pool].std(axis=0, ddof=0).replace(0, 1.0)
    z = (mat - mu) / sd
    a = z.loc[ANCHOR, CID].to_numpy(float)
    a = a - a.mean()
    out = {}
    for c in pool:
        v = z.loc[c, CID].to_numpy(float)
        v = v - v.mean()
        out[c] = float(v @ a / (np.linalg.norm(v) * np.linalg.norm(a)))
    return pd.Series(out)


def bootstrap_ci(long: pd.DataFrame, rng, n_boot: int = 20000):
    """Resample the nine domains -> percentile CI on each country's convergence r."""
    mat = long.pivot_table(index="country", columns="competency_id",
                           values="score", aggfunc="first")[CID]
    pool = [c for c in mat.index if c != ANCHOR]
    mu = mat.loc[pool].mean(axis=0)
    sd = mat.loc[pool].std(axis=0, ddof=0).replace(0, 1.0)
    z = (mat - mu) / sd
    a = z.loc[ANCHOR, CID].to_numpy(float)

    def r_of(v, aa):
        vc, ac = v - v.mean(), aa - aa.mean()
        d = np.linalg.norm(vc) * np.linalg.norm(ac)
        return float(vc @ ac / d) if d else np.nan

    rows = []
    for c in pool:
        v = z.loc[c, CID].to_numpy(float)
        obs = r_of(v, a)
        bs = []
        for _ in range(n_boot):
            i = rng.integers(0, 9, 9)
            vv, aa = v[i], a[i]
            if vv.std() == 0 or aa.std() == 0:
                continue
            bs.append(r_of(vv, aa))
        lo, hi = np.percentile(bs, [2.5, 97.5])
        rows.append({"country": c, "r": obs, "lo95": lo, "hi95": hi})
    return pd.DataFrame(rows)


def main() -> int:
    outdir = config.OUTPUTS_DIR / "au_convergence"
    outdir.mkdir(parents=True, exist_ok=True)

    # ---- Table S1: prespecified 10% ----
    r10 = convergence(align(0.10)).sort_values(ascending=False)
    s1 = r10.rename("convergence_r").rename_axis("country").reset_index()
    s1.insert(0, "rank", range(1, len(s1) + 1))
    s1.to_csv(outdir / "table_s1_convergence.csv", index=False)
    print(f"\n=== Table S1 ({len(s1)} countries, 10% prespecified) ===")
    print(s1.round(3).to_string(index=False))

    # ---- Table S2: threshold sensitivity ----
    thr = {f"{int(t*100)}%": convergence(align(t)) for t in (0.05, 0.10, 0.20)}
    tdf = pd.DataFrame(thr)
    rows = []
    for label, col in tdf.items():
        top = col.sort_values(ascending=False)
        rows.append({"threshold": label, "rank1": top.index[0],
                     "rank1_r": top.iloc[0], "top3": "; ".join(top.index[:3])})
    s2 = pd.DataFrame(rows)
    s2.to_csv(outdir / "table_s2_threshold_sensitivity.csv", index=False)
    print(f"\n=== Table S2 (threshold sensitivity, {len(tdf)} countries) ===")
    print(s2.round(3).to_string(index=False))

    sp = {f"{a} vs {b}": tdf[a].corr(tdf[b], method="spearman")
          for a, b in [("5%", "10%"), ("10%", "20%"), ("5%", "20%")]}
    print("\nSpearman between rankings:")
    for k, v in sp.items():
        print(f"  {k:12s} {v:+.3f}")

    # ---- Rwanda bootstrap CI on the 10% profile ----
    rng = np.random.default_rng(7)
    bs = bootstrap_ci(align(0.10), rng)
    bs = bs.sort_values("r", ascending=False)
    bs.to_csv(outdir / "convergence_bootstrap_ci.csv", index=False)
    rw = bs[bs.country == "Rwanda"].iloc[0]
    print(f"\nRwanda 10% convergence r = {rw.r:+.3f} "
          f"(95% CI {rw.lo95:+.3f} to {rw.hi95:+.3f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
