"""Verify two remaining abstract claims: (a) Ethiopia's top single-competency score,
(b) the quadrant tallies behind the 'rhetoric exceeding readiness' sentence."""
import pandas as pd

al = pd.read_csv("outputs/alignment_scores.csv")
comp = pd.read_csv("data/who_strategy/competencies.csv")
print("competency codes:")
print(comp.to_string(index=False))
print()

# C6 = flexible digital infrastructure?
al2 = al.merge(comp, on='competency_id', how='left', suffixes=('','_c'))
name_col = [c for c in al2.columns if 'name' in c.lower() or 'label' in c.lower()
            or 'competency' in c.lower() and c != 'competency_id']
print("cols:", list(al2.columns))
print()

# highest single competency score corpus-wide, excluding AU
rows = al2[al2.country != 'African Union']
top = rows.sort_values('similarity_score', ascending=False).head(8)
print("=== top single competency scores (excl. AU) ===")
print(top.to_string(index=False))
print()

# Ethiopia's per-competency profile
eth = rows[rows.country == 'Ethiopia'].sort_values('similarity_score', ascending=False)
print("=== Ethiopia per-competency ===")
print(eth.to_string(index=False))

# ---- quadrant tallies ----
rr = pd.read_csv("outputs/rhetoric_vs_readiness/rhetoric_vs_readiness.csv")
print("\n=== quadrant tallies by country ===")
t = rr.pivot_table(index='country', columns='quadrant', values='dimension',
                   aggfunc='count').fillna(0).astype(int)
t['n'] = t.sum(axis=1)
print(t.to_string())
