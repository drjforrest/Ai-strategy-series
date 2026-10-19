"""Find ANY repo-computable variant matching the 25-Sep manuscript Table 2."""
import pandas as pd, numpy as np, sys, itertools
sys.path.insert(0, '.')
pd.set_option('display.width', 220)

DIM_MAP = {
    "GOV_VISION": ("Vision","Government",True),
    "GOV_GOVERNANCE": ("Governance and Ethics","Government",True),
    "GOV_DIGITAL_CAPACITY": ("Digital Capacity","Government",False),
    "GOV_ADAPTABILITY": ("Adaptability","Government",False),
    "TECH_MATURITY": ("Maturity","Technology Sector",False),
    "TECH_INNOVATION": ("Innovation Capacity","Technology Sector",False),
    "TECH_HUMAN_CAPITAL": ("Human Capital","Technology Sector",False),
    "DATA_INFRASTRUCTURE": ("Infrastructure","Data and Infrastructure",False),
    "DATA_AVAILABILITY": ("Data Availability","Data and Infrastructure",False),
}
MS = {"Vision":0.236,"Governance and Ethics":0.180,"Maturity":0.105,"Adaptability":0.033,
      "Innovation Capacity":-0.086,"Data Availability":-0.088,"Digital Capacity":-0.118,
      "Human Capital":-0.141,"Infrastructure":-0.494}

rhet = pd.read_csv('outputs/reference_alignment/oxford_dimensions_2021_2024_embed/'
                   'oxford_dimensions_2021_2024_embed_alignment_scores.csv')
rhet = rhet[rhet.competency_id.isin(DIM_MAP)].copy()
rhet['dimension'] = rhet.competency_id.map(lambda c: DIM_MAP[c][0])
rhet = rhet.rename(columns={'similarity_score':'rhetoric_raw'})[['country','dimension','rhetoric_raw']]
rhet['country'] = rhet['country'].replace({"Côte d'Ivoire":"Cote d'Ivoire"})

panel = pd.read_csv('data/oxford_readiness_indices/processed/oxford_panel_2021_2024_tidy.csv')
p = panel[panel.level=='dimension'].copy()
p['country'] = p['country'].astype(str).replace({"Côte d'Ivoire":"Cote d'Ivoire"})

def dims_for(year, agg='first'):
    if year=='mean':
        m = p.groupby(['country','metric'], as_index=False)['score'].mean()
    else:
        m = p[p.year.astype(str)==str(year)][['country','metric','score']].copy()
    return m.rename(columns={'metric':'dimension','score':'readiness_raw'})

def perdim(df, how='pearson'):
    out={}
    for d,g in df.groupby('dimension'):
        if len(g)<3 or g.rhetoric_raw.std()==0 or g.readiness_raw.std()==0:
            out[d]=np.nan; continue
        out[d]=g[['rhetoric_raw','readiness_raw']].corr(method=how).iloc[0,1]
    return out

def score(got):
    if any(pd.isna(v) for v in got.values()): return 99,0
    errs=[abs(got[d]-MS[d]) for d in MS]
    return max(errs), sum(1 for e in errs if e<0.005)

best=[]
for year in ['2024','mean','2021','2022','2023']:
    m = dims_for(year)
    base = rhet.merge(m, on=['country','dimension'], how='inner')
    cs = sorted(base.country.unique())
    # sweep: keep-all, and every single-country exclusion, and every 2-country exclusion
    combos = [()] + [(c,) for c in cs] + list(itertools.combinations(cs,2))
    for how in ['pearson','spearman','kendall']:
        for drop in combos:
            d = base[~base.country.isin(drop)]
            if d.country.nunique() < 9: continue
            got = perdim(d, how)
            mx, n = score(got)
            best.append((mx, n, year, how, drop, got))

best.sort(key=lambda t:(t[0], -t[1]))
print("Top 8 closest variants found anywhere in the sweep:\n")
for mx, n, year, how, drop, got in best[:8]:
    print(f"  year={year:5s} corr={how:8s} drop={drop if drop else 'none'} "
          f"-> exact={n}/9 max|diff|={mx:.3f}")
print("\n--- if a 9/9 match exists, show it in full ---")
if best[0][1]==9:
    mx,n,year,how,drop,got = best[0]
    for d in sorted(MS, key=lambda x: MS[x]):
        print(f"   {d:22s} ms={MS[d]:+.3f} got={got[d]:+.4f}")
else:
    print("   NO variant reproduced the manuscript Table 2 (best exact = "
          f"{best[0][1]}/9).")
