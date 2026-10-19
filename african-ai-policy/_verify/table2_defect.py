"""Lay out the exact Table 2 defect and prepare the correction.

Source of truth: outputs/rhetoric_vs_readiness/per_dimension_correlation.csv
(the shipped, regenerable artefact -> 0/13 mismatch vs the 31-Aug manuscript).
"""
import pandas as pd, numpy as np

DOCX = ("/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/"
        "Documents/Private Northeastern/08_Research and Scholarship/Projects/"
        "National AI Strategies/Manuscript/"
        "African_AI_strategies_BMJGH_main_manuscript_v1.0-25-sept-2026.docx")

# Verbatim from the 25-Sep-2026 manuscript, Table 2
MS = {"Vision": 0.236, "Governance and Ethics": 0.180, "Maturity": 0.105,
      "Adaptability": 0.033, "Innovation Capacity": -0.086,
      "Data Availability": -0.088, "Digital Capacity": -0.118,
      "Human Capital": -0.141, "Infrastructure": -0.494}

repo = pd.read_csv('outputs/rhetoric_vs_readiness/per_dimension_correlation.csv')
repo = repo.set_index('dimension')['pearson_r'].to_dict()

print(f"{'Dimension':24s} {'Type':16s} {'ms':>8s} {'repo':>9s} {'delta':>8s}")
print("-" * 70)
for d in MS:
    kind = "Text-proximate" if d in ("Vision", "Governance and Ethics") else "Independent"
    print(f"{d:24s} {kind:16s} {MS[d]:+8.3f} {repo[d]:+9.4f} {repo[d]-MS[d]:+8.3f}")

tp_ms = np.mean([MS[d] for d in ("Vision", "Governance and Ethics")])
ind_dims = [d for d in MS if d not in ("Vision", "Governance and Ethics")]
ind_ms = np.mean([MS[d] for d in ind_dims])
tp_rp = np.mean([repo[d] for d in ("Vision", "Governance and Ethics")])
ind_rp = np.mean([repo[d] for d in ind_dims])

print(f"\nsubset means  text-proximate: ms {tp_ms:+.4f} vs repo {tp_rp:+.4f}")
print(f"subset means  independent   : ms {ind_ms:+.4f} vs repo {ind_rp:+.4f}")
print("\nNOTE: the manuscript's own prose (p156) and Table 2 note already state")
print("      +0.208 / -0.113 / -0.041 / p=0.028 -- i.e. the REPO values.")
print("      Only the nine table rows disagree with their own footnote.")
