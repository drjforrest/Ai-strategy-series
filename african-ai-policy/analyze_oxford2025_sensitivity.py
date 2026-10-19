"""Oxford 2025 temporal-alignment sensitivity for the rhetoric-readiness comparison.

The primary comparison uses Oxford 2024 (9 dimensions), which predates many strategies.
This script repeats the analysis against the Oxford Insights GAIRI 2025 framework
(6 pillars, 14 dimensions; latest source dated Dec 2025) for all corpus countries.

Rhetoric: run_reference_alignment.py --reference
          data/oxford_readiness_indices/oxford_dimensions_2025_dims14_embed.csv
          --label oxford_2025_dims14
Readiness: raw 2025 workbook, 'Dimensions-Pillars' sheet.

Circularity guard (pre-specified from the 2025 Methodology Report indicator list):
  strict: Policy vision + Policy commitment (Policy Capacity pillar; indicators
          scored from the existence/content of the national AI strategy)
  broad : strict + every dimension with >=1 indicator scored from a national AI
          strategy or policy document (Governance principles, Government digital
          policy, Human capital, Safety and security)

Country sets: all; excluding South Africa (withdrawn draft); predates_index (strategy
launched/published on or before 31 Dec 2025 - drops Ghana, Mauritius, South Africa,
Zimbabwe, launched Mar-Apr 2026).

Also: Spearman of operationalization breadth vs Oxford 2025 'Policy commitment'
(an external, expert-scored measure of the same construct: actions, agencies,
timeline, budget).

Outputs: outputs/sensitivity/oxford2025/
"""
from __future__ import annotations

import itertools

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import spearmanr

from src import config

OUT = config.OUTPUTS_DIR / "sensitivity" / "oxford2025"
RAW = config.DATA_DIR / "oxford_readiness_indices" / "2025-Government-AI-Readiness-Index-data-1.xlsx"
RHET = (config.OUTPUTS_DIR / "reference_alignment" / "oxford_2025_dims14" /
        "oxford_2025_dims14_alignment_scores.csv")
REF = config.DATA_DIR / "oxford_readiness_indices" / "oxford_dimensions_2025_dims14_embed.csv"
NAME = {"United Republic of Tanzania": "Tanzania", "Côte D'Ivoire": "Côte d'Ivoire"}
STRICT = {"Policy vision", "Policy commitment"}
BROAD = STRICT | {"Governance principles", "Government digital policy", "Human capital", "Safety and security"}
POST_INDEX = {"Ghana", "Mauritius", "South Africa", "Zimbabwe"}  # launched Mar-Apr 2026
ZA = "South Africa"
DRAFTS = {"South Africa", "Tanzania", "Lesotho"}


def load() -> pd.DataFrame:
    ref = pd.read_csv(REF)
    id2name = dict(zip(ref.competency_id, ref.name))
    rh = pd.read_csv(RHET)
    rh = rh[rh.country != "African Union"].assign(dimension=lambda d: d.competency_id.map(id2name))
    ox = pd.read_excel(RAW, sheet_name="Dimensions-Pillars", header=1)
    ox = ox.loc[:, ~ox.columns.astype(str).str.startswith("Unnamed")]
    ox["Country"] = ox["Country"].astype(str).str.strip().replace(NAME)
    dims = list(id2name.values())
    long = ox.melt(id_vars="Country", value_vars=dims, var_name="dimension", value_name="readiness_raw")
    long = long.rename(columns={"Country": "country"})
    cells = rh.merge(long, on=["country", "dimension"], how="inner").rename(columns={"similarity_score": "rhetoric_raw"})
    missing = sorted(set(rh.country) - set(cells.country))
    if missing:
        raise SystemExit(f"No Oxford 2025 scores for: {missing}")
    return cells[["country", "dimension", "rhetoric_raw", "readiness_raw"]]


def bh(p: np.ndarray) -> np.ndarray:
    """Benjamini-Hochberg q-values."""
    p = np.asarray(p, float); m = len(p); o = np.argsort(p); q = np.empty(m); prev = 1.0
    for i in range(m - 1, -1, -1):
        prev = min(prev, p[o[i]] * m / (i + 1)); q[o[i]] = prev
    return q


def pearson_p(r: float, n: int) -> float:
    t = r * np.sqrt((n - 2) / (1 - r * r))
    return float(2 * stats.t.sf(abs(t), n - 2))


def per_dim(cells):
    return {d: g[["rhetoric_raw", "readiness_raw"]].corr().iloc[0, 1] for d, g in cells.groupby("dimension")}


def guard(r: dict, tp_set: set) -> dict:
    dims = sorted(r)
    v = np.array([r[d] for d in dims])
    tp_mask = np.array([d in tp_set for d in dims])
    obs = v[tp_mask].mean() - v[~tp_mask].mean()
    k = tp_mask.sum()
    seps = [v[list(c)].mean() - np.delete(v, list(c)).mean() for c in itertools.combinations(range(len(v)), k)]
    hits = int(sum(s >= obs - 1e-12 for s in seps))
    return {"tp_mean_r": v[tp_mask].mean(), "ind_mean_r": v[~tp_mask].mean(), "separation": obs,
            "mean_r_all": v.mean(), "perm_hits": hits, "n_perm": len(seps), "perm_p": hits / len(seps)}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    cells = load()
    sets = {"all": cells, "no_ZA": cells[cells.country != ZA],
            "predates_index": cells[~cells.country.isin(POST_INDEX)],
            "no_drafts": cells[~cells.country.isin(DRAFTS)]}
    summ, pd_rows, loo = [], [], []
    for sname, df in sets.items():
        r = per_dim(df)
        pd_rows += [{"set": sname, "dimension": d, "pearson_r": v, "strict_tp": d in STRICT, "broad_tp": d in BROAD}
                    for d, v in r.items()]
        for gname, tp in (("strict", STRICT), ("broad", BROAD)):
            summ.append({"set": sname, "guard": gname, "n_countries": df.country.nunique(),
                         "n_cells": len(df), **guard(r, tp)})
        for c in sorted(df.country.unique()):
            g = guard(per_dim(df[df.country != c]), STRICT)
            loo.append({"set": sname, "country_withheld": c, **{k: g[k] for k in ("tp_mean_r", "ind_mean_r", "separation", "perm_p")}})
    S = pd.DataFrame(summ); S.to_csv(OUT / "readiness2025_summary.csv", index=False)
    P = pd.DataFrame(pd_rows)
    nmap = {k: v.country.nunique() for k, v in sets.items()}
    P["n"] = P["set"].map(nmap)
    P["p"] = [pearson_p(r, n) for r, n in zip(P.pearson_r, P.n)]
    P["q_BH"] = P.groupby("set")["p"].transform(lambda x: bh(x.to_numpy()))
    P.to_csv(OUT / "readiness2025_per_dimension.csv", index=False)
    L = pd.DataFrame(loo); L.to_csv(OUT / "readiness2025_loo_strict.csv", index=False)

    # Operationalization breadth vs Oxford 2025 Policy commitment (external benchmark)
    ops = pd.read_csv(config.OPERATIONALIZATION_CSV).set_index("country")
    pc = cells[cells.dimension == "Policy commitment"].set_index("country").readiness_raw
    j = pd.concat([ops[["operationalization_index", "focus_index"]], pc.rename("policy_commitment_2025")], axis=1, join="inner")
    val = []
    for nm, sub in (("all", j), ("predates_index", j[~j.index.isin(POST_INDEX)])):
        for m in ("operationalization_index", "focus_index"):
            rho, p = spearmanr(sub[m], sub.policy_commitment_2025)
            val.append({"set": nm, "measure": m, "n": len(sub), "spearman_rho": rho, "p": p})
    V = pd.DataFrame(val); V.to_csv(OUT / "operationalization_vs_policy_commitment.csv", index=False)
    j.to_csv(OUT / "operationalization_vs_policy_commitment_data.csv")

    pd.set_option("display.width", 200)
    print(S.round(3).to_string(index=False))
    print("\nper-dimension r (all / predates_index):")
    print(P.pivot(index="dimension", columns="set", values="pearson_r")[["all", "no_ZA", "predates_index", "no_drafts"]].round(3).to_string())
    print("\nLOO strict (all) p<=0.05:", L[(L.set == "all") & (L.perm_p <= 0.05)].country_withheld.tolist(),
          "| min p", round(L[L.set == "all"].perm_p.min(), 3))
    print("\n", V.round(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
