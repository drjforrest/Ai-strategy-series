"""How fragile is the circularity guard? Leave-one-country-out on the
permutation p. If dropping a single country crosses p=0.05, the guard's
significance is not a stable property of the data.

Uses the same construction as analyze_rhetoric_vs_readiness.py.
"""
import itertools, sys
import numpy as np
import pandas as pd

sys.path.insert(0, ".")

DIM_MAP = {
    "GOV_VISION":          ("Vision", "Government", True),
    "GOV_GOVERNANCE":      ("Governance and Ethics", "Government", True),
    "GOV_DIGITAL_CAPACITY":("Digital Capacity", "Government", False),
    "GOV_ADAPTABILITY":    ("Adaptability", "Government", False),
    "TECH_MATURITY":       ("Maturity", "Technology Sector", False),
    "TECH_INNOVATION":     ("Innovation Capacity", "Technology Sector", False),
    "TECH_HUMAN_CAPITAL":  ("Human Capital", "Technology Sector", False),
    "DATA_INFRASTRUCTURE": ("Infrastructure", "Data and Infrastructure", False),
    "DATA_AVAILABILITY":   ("Data Availability", "Data and Infrastructure", False),
}

rhet = pd.read_csv("outputs/reference_alignment/oxford_dimensions_2021_2024_embed/"
                   "oxford_dimensions_2021_2024_embed_alignment_scores.csv")
rhet = rhet[rhet.competency_id.isin(DIM_MAP)].copy()
rhet["dimension"] = rhet.competency_id.map(lambda c: DIM_MAP[c][0])
rhet = rhet.rename(columns={"similarity_score": "rhetoric_raw"})[
    ["country", "dimension", "rhetoric_raw"]]
rhet["country"] = rhet["country"].replace({"Côte d'Ivoire": "Cote d'Ivoire"})

panel = pd.read_csv("data/oxford_readiness_indices/processed/oxford_panel_2021_2024_tidy.csv")
p = panel[(panel.level == "dimension") & (panel.year.astype(str) == "2024")].copy()
p["country"] = p["country"].astype(str).replace({"Côte d'Ivoire": "Cote d'Ivoire"})
meas = p[["country", "metric", "score"]].rename(
    columns={"metric": "dimension", "score": "readiness_raw"})

base = rhet.merge(meas, on=["country", "dimension"], how="inner")
base["tp"] = base.dimension.map(lambda d: next(v[2] for v in DIM_MAP.values() if v[0] == d))


def pearson(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3 or a.std() == 0 or b.std() == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def guard(df):
    per = (df.groupby(["dimension", "tp"])
             .apply(lambda g: pearson(g.rhetoric_raw, g.readiness_raw),
                    include_groups=False)
             .reset_index(name="r"))
    tp = per[per.tp]["r"].mean()
    ind = per[~per.tp]["r"].mean()
    rb = per.set_index("dimension")["r"].to_dict()
    c = t = 0
    for combo in itertools.combinations(sorted(per.dimension.unique()), 2):
        t += 1
        if np.mean([rb[x] for x in combo]) >= tp - 1e-12:
            c += 1
    return tp, ind, c / t, c, t


tp0, ind0, p0, c0, t0 = guard(base)
print(f"FULL SET (n={base.country.nunique()} countries, "
      f"{len(base)} cells): tp={tp0:+.4f} ind={ind0:+.4f}  p={p0:.4f} ({c0}/{t0})\n")

print("=== leave-one-country-out ===")
print(f"{'dropped':16s} {'tp':>8s} {'ind':>8s} {'p':>7s}  {'verdict':>10s}")
rows = []
for c in sorted(base.country.unique()):
    d = base[base.country != c]
    tp, ind, pv, cc, tt = guard(d)
    verdict = "sig" if pv <= 0.05 else "NOT sig"
    rows.append({"dropped": c, "tp": tp, "ind": ind, "p": pv, "sig": pv <= 0.05})
    print(f"{c:16s} {tp:+8.4f} {ind:+8.4f} {pv:7.4f}  {verdict:>10s}")

r = pd.DataFrame(rows)
print(f"\ndrops crossing p>0.05 : {int((~r.sig).sum())} / {len(r)}")
print(f"p range across drops  : {r.p.min():.4f} to {r.p.max():.4f}")
print(f"full-set p            : {p0:.4f}")
if (~r.sig).any():
    print("countries whose removal removes significance:",
          ", ".join(r[~r.sig].dropped))
r.to_csv("outputs/rhetoric_vs_readiness/guard_leave_one_out.csv", index=False)
print("\nwrote outputs/rhetoric_vs_readiness/guard_leave_one_out.csv")
