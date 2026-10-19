"""Cross-check: our embedding measures vs Olufadewa et al. (2024) expert ratings.

Olufadewa et al., 'National eHealth strategy frameworks in Africa' (Oxford Open
Digital Health 2024, oqae047) independently reviewed 34 national eHealth
strategies, scoring each on five domains (vision/strategy, implementation plan,
M&E, FAIR mention, recency) and assigning an overall expert rating of
weak / moderate / strong.

This script asks a construct-validity question: does either of OUR measures
(WHO-competency alignment; operationalization breadth) track that independent
expert assessment?

  * WHO alignment        -- semantic engagement with the nine WHO digital-health
                            core components (embedding cosine).
  * Operationalization   -- share of six execution levers above median (lexicon).

Expected reading: expert 'comprehensiveness' is closest in construct to our
operationalization measure (implementation plan, M&E, budget), NOT to WHO
alignment. If alignment is uncorrelated with expert rating, that is evidence the
two are DISTINCT constructs -- which supports the paper's core claim but warns
against presenting alignment as a proxy for policy quality.

Reads : reference/olufadewa_2024_census.csv
        outputs/connectivity/alignment_by_country.csv
        outputs/operationalization/operationalization_index.csv
    ./run.sh crosscheck_olufadewa.py
"""
from __future__ import annotations

import pandas as pd
from scipy.stats import spearmanr

from src import config

REF = config.PROJECT_ROOT / "reference" / "olufadewa_2024_census.csv"
ORD = {"Weak": 0, "Moderate": 1, "Strong": 2}


def main() -> int:
    ref = pd.read_csv(REF)
    ref["rating_ord"] = ref["quality_rating"].map(ORD)

    align = pd.read_csv(config.OUTPUTS_DIR / "connectivity" / "alignment_by_country.csv")
    dh = (align[align.set == "Digital health"]
          .set_index("country")["similarity_score"].rename("who_alignment"))
    ops = (pd.read_csv(config.OPERATIONALIZATION_CSV)
           .set_index("country")["operationalization_index"].rename("op_breadth"))

    df = (ref.set_index("country")
          .join(dh, how="inner")
          .join(ops, how="left"))
    df = df.dropna(subset=["who_alignment"]).reset_index()

    print(f"=== Matched our DH corpus to Olufadewa ratings: n = {len(df)} ===\n")
    cols = ["country", "quality_rating", "who_alignment", "op_breadth"]
    print(df[cols].sort_values("who_alignment", ascending=False).to_string(index=False))

    print("\n=== Mean of our measures by expert rating ===")
    print(df.groupby("quality_rating")[["who_alignment", "op_breadth"]]
          .agg(["mean", "count"]).round(3).to_string())

    for measure in ("who_alignment", "op_breadth"):
        sub = df.dropna(subset=[measure])
        if sub["rating_ord"].nunique() > 1:
            rho, p = spearmanr(sub["rating_ord"], sub[measure])
            print(f"\nSpearman({measure} vs expert rating) = {rho:+.3f}  (p = {p:.3f}, n = {len(sub)})")

    # Which of our DH countries are NOT in the Olufadewa census (candidate gaps)
    ours = set(dh.index)
    theirs = set(ref.country)
    print(f"\nOur DH countries absent from Olufadewa census: {sorted(ours - theirs) or 'none'}")
    print(f"Olufadewa countries we could add to our DH corpus (n = {len(theirs - ours)}): "
          f"{', '.join(sorted(theirs - ours))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
