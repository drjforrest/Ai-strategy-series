"""Build data/oxford_readiness_indices/processed/oxford_panel_2021_2024_tidy.csv
from the raw Oxford Insights Government AI Readiness Index workbooks.

Replaces the previous hand-built panel (which silently omitted Tanzania because
Oxford lists it as "United Republic of Tanzania"). Name harmonisation:
  * "United Republic of Tanzania" -> "Tanzania"
  * "Côte D'Ivoire" (2021-2023) / "Côte d'Ivoire" -> "Cote d'Ivoire" (panel convention)
  * 2021 dimension "Size" -> "Maturity" (renamed by Oxford from 2022)
  * "Data Representativeness" dropped (not one of the nine dimensions analysed)

Countries kept: every national entry in config.COUNTRY_FILES plus Morocco (kept for
the with-Morocco sensitivity analysis). Validated: reproduces all 624 rows of the
previous 12-country panel exactly (max abs diff 0.0).

    python -m scripts.build_oxford_panel
"""
from __future__ import annotations

import pandas as pd

from src import config

RAW = config.DATA_DIR / "oxford_readiness_indices"
OUT = RAW / "processed" / "oxford_panel_2021_2024_tidy.csv"
FILES = {
    2021: "2021-Government-AI-Readiness-Index-public-dataset.xlsx",
    2022: "2022-Government-AI-Readiness-Index-public-data.xlsx",
    2023: "2023-Government-AI-Readiness-Index-Public-Indicator-Data.xlsx",
    2024: "2024-GAIRI-data.xlsx",
}
NAME = {"United Republic of Tanzania": "Tanzania", "Côte D'Ivoire": "Cote d'Ivoire",
        "Côte d'Ivoire": "Cote d'Ivoire"}
PILLARS = ["Government", "Technology Sector", "Data and Infrastructure"]


def tidy_year(year: int, fname: str) -> pd.DataFrame:
    xl = pd.ExcelFile(RAW / fname)
    df = xl.parse(xl.sheet_names[1], header=1)
    df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
    df = df.rename(columns={df.columns[0]: "country"})
    total = next(c for c in df.columns if str(c).lower().startswith(("total", "overall")))
    df = df.drop(columns=[c for c in df.columns if str(c).lower().startswith("ranking")])
    dims = [c for c in df.columns if c not in ["country", total, *PILLARS]]
    df["country"] = df["country"].astype(str).str.strip().replace(NAME)
    rows = []
    for _, r in df.iterrows():
        rows.append((r.country, year, "overall", "Overall", r[total]))
        rows += [(r.country, year, "pillar", p, r[p]) for p in PILLARS]
        rows += [(r.country, year, "dimension", d, r[d]) for d in dims]
    out = pd.DataFrame(rows, columns=["country", "year", "level", "metric", "score"])
    out.loc[(out.year == 2021) & (out.metric == "Size"), "metric"] = "Maturity"
    return out[out.metric != "Data Representativeness"]


def main() -> int:
    panel = pd.concat([tidy_year(y, f) for y, f in FILES.items()], ignore_index=True)
    keep = {NAME.get(c, c) for c in config.COUNTRIES if c != "African Union"} | {"Morocco"}
    keep = {"Cote d'Ivoire" if c == "Côte d'Ivoire" else c for c in keep}
    panel = panel[panel.country.isin(keep)].dropna(subset=["score"])
    panel = panel.sort_values(["year", "country", "level", "metric"], kind="stable")
    panel.to_csv(OUT, index=False)
    counts = panel[panel.level == "dimension"].groupby("year").country.nunique().to_dict()
    missing = sorted(keep - set(panel.country))
    print(f"wrote {OUT.name}: {len(panel)} rows; countries with dimension scores per year {counts}")
    print(f"no Oxford scores for: {missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
