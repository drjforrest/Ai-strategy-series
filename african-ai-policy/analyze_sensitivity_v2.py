"""Corpus-v2 sensitivity analyses (cut-off 30 Sep 2026).

Run AFTER analyze_rhetoric_vs_readiness.py and analyze_au_convergence.py.

Variants
  primary  : all national entries with Oxford 2024 scores
  no_drafts: primary minus all flagged drafts (South Africa, Tanzania, Lesotho)
  no_ZA    : primary minus South Africa (its Draft National AI Policy was withdrawn
             by the Minister on 26 Apr 2026 after fictitious references were found)

For each variant:
  * nine per-dimension Pearson r (primary unit of inference), text-proximate vs
    independent means, separation, exact permutation p over all C(9,2)=36
    assignments of two dimensions to the text-proximate subset
  * pooled r over country x dimension cells (descriptive only; cells are nested)
  * leave-one-country-out (replaces the stale hand-built Table S3)
And for no_ZA: AU convergence recomputed without South Africa (the z-scoring
reference set changes, so every country's profile r can move).

Outputs (outputs/sensitivity/):
  readiness_summary.csv, readiness_per_dimension.csv, readiness_loo.csv,
  au_convergence_noZA.csv, au_convergence_compare.csv
"""
from __future__ import annotations

import itertools
import subprocess
import sys

import numpy as np
import pandas as pd

from src import config

OUT = config.OUTPUTS_DIR / "sensitivity"
RVR = config.OUTPUTS_DIR / "rhetoric_vs_readiness" / "rhetoric_vs_readiness.csv"
ZA = "South Africa"
DRAFTS = {"South Africa", "Tanzania", "Lesotho"}  # draft rule A: flagged drafts


def guard(cells: pd.DataFrame) -> dict:
    dims = sorted(cells.dimension.unique())
    tp_dims = set(cells.loc[cells.text_proximate, "dimension"])
    r = {d: cells[cells.dimension == d][["rhetoric_raw", "readiness_raw"]].corr().iloc[0, 1] for d in dims}
    tp = float(np.mean([r[d] for d in dims if d in tp_dims]))
    ind = float(np.mean([r[d] for d in dims if d not in tp_dims]))
    v = [r[d] for d in dims]
    k = len(tp_dims)
    hits = sum(np.mean([v[i] for i in cb]) - np.mean([v[i] for i in range(len(v)) if i not in cb])
               >= (tp - ind) - 1e-12 for cb in itertools.combinations(range(len(v)), k))
    n_perm = len(list(itertools.combinations(range(len(v)), k)))
    z = cells.copy()
    for col in ("rhetoric_raw", "readiness_raw"):
        z[col] = z.groupby("dimension")[col].transform(lambda s: (s - s.mean()) / s.std(ddof=0))
    pooled = float(z[["rhetoric_raw", "readiness_raw"]].corr().iloc[0, 1])
    return {"n_countries": cells.country.nunique(), "n_cells": len(cells), "mean_r_all9": float(np.mean(v)),
            "pooled_r_cells": pooled, "tp_mean_r": tp, "ind_mean_r": ind, "separation": tp - ind,
            "perm_hits": int(hits), "n_perm": n_perm, "perm_p": hits / n_perm, "per_dim": r}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    cells = pd.read_csv(RVR)
    variants = {"primary": cells, "no_ZA": cells[cells.country != ZA],
                "no_drafts": cells[~cells.country.isin(DRAFTS)]}

    summ, perdim, loo = [], [], []
    for name, df in variants.items():
        g = guard(df)
        perdim += [{"variant": name, "dimension": d, "pearson_r": rv} for d, rv in g.pop("per_dim").items()]
        summ.append({"variant": name, **g})
        for c in sorted(df.country.unique()):
            h = guard(df[df.country != c]); h.pop("per_dim")
            loo.append({"variant": name, "country_withheld": c, "tp_mean_r": h["tp_mean_r"],
                        "ind_mean_r": h["ind_mean_r"], "separation": h["separation"],
                        "perm_p": h["perm_p"], "sig_0.05": h["perm_p"] <= 0.05})
    pd.DataFrame(summ).to_csv(OUT / "readiness_summary.csv", index=False)
    pd.DataFrame(perdim).to_csv(OUT / "readiness_per_dimension.csv", index=False)
    pd.DataFrame(loo).to_csv(OUT / "readiness_loo.csv", index=False)

    # AU convergence without South Africa: re-run the canonical script on filtered scores.
    scores = pd.read_csv(config.ALIGNMENT_SCORES_CSV)
    tmp = OUT / "_alignment_scores_noZA.csv"
    scores[scores.country != ZA].to_csv(tmp, index=False)
    nd = OUT / "au_convergence_noZA"
    subprocess.run([sys.executable, "analyze_au_convergence.py", "--scores", str(tmp), "--outdir", str(nd)],
                   check=True, cwd=config.PROJECT_ROOT, capture_output=True)
    prim = pd.read_csv(config.OUTPUTS_DIR / "au_convergence" / "au_convergence.csv")
    noza = pd.read_csv(nd / "au_convergence.csv")
    noza.to_csv(OUT / "au_convergence_noZA.csv", index=False)
    cmp_ = prim[["country", "profile_r_to_AU", "rank"]].merge(
        noza[["country", "profile_r_to_AU", "rank"]], on="country", how="left", suffixes=("_primary", "_noZA"))
    tmp2 = OUT / "_alignment_scores_noDrafts.csv"
    scores[~scores.country.isin(DRAFTS)].to_csv(tmp2, index=False)
    nd2 = OUT / "au_convergence_noDrafts"
    subprocess.run([sys.executable, "analyze_au_convergence.py", "--scores", str(tmp2), "--outdir", str(nd2)],
                   check=True, cwd=config.PROJECT_ROOT, capture_output=True)
    nodr = pd.read_csv(nd2 / "au_convergence.csv")
    cmp_ = cmp_.merge(nodr[["country", "profile_r_to_AU", "rank"]].rename(
        columns={"profile_r_to_AU": "profile_r_to_AU_noDrafts", "rank": "rank_noDrafts"}), on="country", how="left")
    cmp_.to_csv(OUT / "au_convergence_compare.csv", index=False)

    s = pd.DataFrame(summ).set_index("variant")
    print(s[["n_countries", "n_cells", "mean_r_all9", "pooled_r_cells", "tp_mean_r", "ind_mean_r",
             "separation", "perm_hits", "perm_p"]].round(3).to_string())
    print("\nLOO significant removals:", pd.DataFrame(loo).groupby("variant")["sig_0.05"].sum().to_dict())
    print("\nAU convergence primary vs no-ZA:\n", cmp_.round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
