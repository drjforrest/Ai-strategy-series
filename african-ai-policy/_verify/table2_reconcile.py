"""Does the 25-Sep manuscript's Table 2 match anything the repo can produce?"""
import pandas as pd, numpy as np, sys, itertools
sys.path.insert(0, '.')
pd.set_option('display.width', 200)

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

# Verbatim from the 25-Sep-2026 manuscript, Table 2
MS = {
    "Vision": 0.236, "Governance and Ethics": 0.180, "Maturity": 0.105,
    "Adaptability": 0.033, "Innovation Capacity": -0.086,
    "Data Availability": -0.088, "Digital Capacity": -0.118,
    "Human Capital": -0.141, "Infrastructure": -0.494,
}

rhet = pd.read_csv('outputs/reference_alignment/oxford_dimensions_2021_2024_embed/'
                   'oxford_dimensions_2021_2024_embed_alignment_scores.csv')
rhet = rhet[rhet.competency_id.isin(DIM_MAP)].copy()
rhet['dimension'] = rhet.competency_id.map(lambda c: DIM_MAP[c][0])
rhet = rhet.rename(columns={'similarity_score': 'rhetoric_raw'})[['country','dimension','rhetoric_raw']]
rhet['country'] = rhet['country'].replace({"Côte d'Ivoire": "Cote d'Ivoire"})   # accent fold

panel = pd.read_csv('data/oxford_readiness_indices/processed/oxford_panel_2021_2024_tidy.csv')
dims = panel[panel.level == 'dimension'].copy()
dims['country'] = dims['country'].astype(str).replace({"Côte d'Ivoire": "Cote d'Ivoire"})

def pearson(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < 3 or a.std() == 0 or b.std() == 0: return np.nan
    return float(np.corrcoef(a, b)[0, 1])

def per_dim(rhet_df, meas_df, how='pearson'):
    df = rhet_df.merge(meas_df, on=['country','dimension'], how='inner')
    out = {}
    for d, g in df.groupby('dimension'):
        if how == 'pearson':
            out[d] = pearson(g.rhetoric_raw, g.readiness_raw)
        else:
            out[d] = g[['rhetoric_raw','readiness_raw']].corr(method='spearman').iloc[0,1]
    return out, df

def meas_for(year):
    if year == 'mean':
        m = dims.groupby(['country','metric'], as_index=False)['score'].mean()
    else:
        m = dims[dims.year.astype(str) == str(year)][['country','metric','score']].copy()
    return m.rename(columns={'metric':'dimension','score':'readiness_raw'})

def show(tag, got):
    diffs = {d: got.get(d, np.nan) - MS[d] for d in MS}
    maxabs = max(abs(v) for v in diffs.values())
    match = sum(1 for v in diffs.values() if abs(v) < 0.0005)
    print(f"\n--- {tag}: {match}/9 exact matches, max|diff| = {maxabs:.3f}")
    for d in sorted(MS, key=lambda x: MS[x]):
        g = got.get(d, np.nan)
        flag = 'OK ' if abs(g - MS[d]) < 0.0005 else '>> '
        print(f"   {flag}{d:22s} ms={MS[d]:+.3f}  got={g:+.4f}")

print("="*74)
print("MANUSCRIPT Table 2 vs REPO, under several defensible variants")
print("="*74)

for year in ['2024', 'mean', '2021', '2022', '2023']:
    g, df = per_dim(rhet, meas_for(year))
    show(f"Pearson, year={year}, n={df.country.nunique()} countries", g)

g, df = per_dim(rhet, meas_for('2024'), how='spearman')
show("Spearman, year=2024", g)

