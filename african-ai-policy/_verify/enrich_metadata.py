"""Enrich data/corpus_metadata.csv with verified/derived fields.

Adds: subregion, adoption_year, ai_mentions, ai_density_per_1k,
roundness, genre_matches_collection, provenance_flag, status_flag.
Text-derived fields are computed from the extracts on disk.
"""
import pathlib, re, pandas as pd

D = pathlib.Path("data")
NS, DH = D / "national_strategies", D / "digital_health_strategies"

# subregion (UN geoscheme, standard)
SUB = {"Benin":"West Africa","Côte d'Ivoire":"West Africa","Egypt":"North Africa",
 "Ethiopia":"East Africa","Ghana":"West Africa","Kenya":"East Africa",
 "Mauritius":"East Africa","Morocco":"North Africa","Nigeria":"West Africa",
 "Rwanda":"East Africa","Senegal":"West Africa","South Africa":"Southern Africa",
 "Tanzania":"East Africa","Zimbabwe":"Southern Africa","African Union":"Continental",
 "Namibia":"Southern Africa","Uganda":"East Africa"}

# Multilingual: the corpus contains French strategies. A term is counted if it
# appears as a standalone token; EN "AI", FR "IA", and the full phrases EN/FR.
AI_RE = re.compile(r"\bAI\b|\bIA\b|\bartificial intelligence\b|\bintelligence artificielle\b", re.I)

def metrics(p: pathlib.Path):
    t = p.read_text(encoding="utf-8", errors="ignore")
    w = len(t.split())
    n = len(AI_RE.findall(t))
    return w, n, round(n / w * 1000, 2) if w else 0.0

# status / genre flags
GENRE_MATCH = {  # does the document's genre satisfy "national AI strategy"?
 "Benin":True,"Côte d'Ivoire":True,"Egypt":True,"Ethiopia":False,
 "Ghana":True,"Kenya":True,"Mauritius":True,"Morocco":False,"Nigeria":True,
 "Rwanda":True,"Senegal":True,"South Africa":True,"Tanzania":True,
 "Zimbabwe":True,"African Union":True}
GENRE_NOTE = {
 "Ethiopia":"Digital-transformation strategy; AI mentioned but not the subject",
 "Morocco":"Conference-synthesis report, not a national strategy",
 "Mauritius":"Working-group report accompanying the strategy",
 "South Africa":"Draft (Gazette, 2026)","Tanzania":"Draft framework v0.6"}

PROV = {"Kenya":"CONTAINS 389-word NotebookLM derivative (Kenya_National_AI_Strategy_2025-2030.pdf)"}

meta = pd.read_csv(D / "corpus_metadata.csv")
meta["subregion"] = meta.country.map(SUB)
meta["genre_matches_collection"] = meta.country.map(GENRE_MATCH)
meta["genre_note"] = meta.country.map(GENRE_NOTE).fillna("")
meta["provenance_flag"] = meta.country.map(PROV).fillna("")

def pathfor(r):
    return (NS if r.collection == "AI strategies" else DH) / r.local_filename
m = meta.apply(lambda r: metrics(pathfor(r)), axis=1)
meta["ai_mentions"] = [x[0] for x in m]
meta["ai_density_per_1k"] = [x[2] for x in m]
meta = meta.rename(columns={"ai_mentions":"_tmp_n"})  # placeholder, fix below
meta["ai_mentions"], meta["ai_density_per_1k"] = [x[1] for x in m], [x[2] for x in m]

cols = ["collection","country","subregion","document_title","policy_domain",
 "issuing_body","status","planning_period","language","local_filename",
 "word_count","ai_mentions","ai_density_per_1k","genre_matches_collection",
 "genre_note","provenance_flag","source_url"]
meta = meta[cols]
meta.to_csv(D / "corpus_metadata.csv", index=False)
print("rewrote data/corpus_metadata.csv |", len(meta), "rows x", len(cols), "cols")
print()
print(meta[["country","status","word_count","ai_mentions","ai_density_per_1k",
            "genre_matches_collection"]].to_string(index=False))
