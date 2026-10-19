"""Enrich corpus_metadata.csv — multilingual AI terms + genre flags (v2)."""
import pathlib, re, pandas as pd

D = pathlib.Path("data")
NS, DH = D / "national_strategies", D / "digital_health_strategies"

SUB = {"Benin":"West Africa","Côte d'Ivoire":"West Africa","Egypt":"North Africa",
 "Ethiopia":"East Africa","Ghana":"West Africa","Kenya":"East Africa",
 "Mauritius":"East Africa","Morocco":"North Africa","Nigeria":"West Africa",
 "Rwanda":"East Africa","Senegal":"West Africa","South Africa":"Southern Africa",
 "Tanzania":"East Africa","Zimbabwe":"Southern Africa","African Union":"Continental",
 "Namibia":"Southern Africa","Uganda":"East Africa"}

# Multilingual: corpus contains French strategies. Count EN "AI" / FR "IA"
# and the full phrases in both languages.
AI_RE = re.compile(r"\bAI\b|\bIA\b|\bartificial intelligence\b|\bintelligence artificielle\b", re.I)

GENRE_PRIMARY = {"Benin":True,"Côte d'Ivoire":True,"Egypt":True,"Ethiopia":False,
 "Ghana":True,"Kenya":True,"Mauritius":True,"Morocco":False,"Nigeria":True,
 "Rwanda":True,"Senegal":True,"South Africa":True,"Tanzania":True,"Zimbabwe":True,
 "African Union":True}
GENRE_DH = {"Rwanda":True,"Namibia":True,"Mauritius":True,"Uganda":False}

NOTE = {
 "Ethiopia":"Digital-transformation strategy; AI incidental",
 "Morocco":"Conference-synthesis report, not a national strategy",
 "Mauritius":"Working-group report accompanying the strategy",
 "South Africa":"Draft (Gazette, 2026)","Tanzania":"Draft framework v0.6",
 "Uganda":"General digital transformation, not a digital-health strategy"}
PROV = {"Kenya":"CONTAINS 389-word NotebookLM derivative (Kenya_National_AI_Strategy_2025-2030.pdf)"}

def metrics(p):
    t = p.read_text(encoding="utf-8", errors="ignore")
    w = len(t.split()); n = len(AI_RE.findall(t))
    return w, n, round(n / w * 1000, 2) if w else 0.0

meta = pd.read_csv(D / "corpus_metadata.csv")
meta["subregion"] = meta.country.map(SUB)
meta["genre_matches_collection"] = meta.apply(
    lambda r: (GENRE_PRIMARY if r.collection == "AI strategies" else GENRE_DH).get(r.country), axis=1)
meta["genre_note"] = meta.country.map(NOTE).fillna("")
meta["provenance_flag"] = meta.country.map(PROV).fillna("")

m = meta.apply(lambda r: metrics((NS if r.collection == "AI strategies" else DH) / r.local_filename), axis=1)
meta["ai_mentions"] = [x[1] for x in m]
meta["ai_density_per_1k"] = [x[2] for x in m]

cols = ["collection","country","subregion","document_title","policy_domain",
 "issuing_body","status","planning_period","language","local_filename",
 "word_count","ai_mentions","ai_density_per_1k","genre_matches_collection",
 "genre_note","provenance_flag","source_url"]
meta = meta[cols]
meta.to_csv(D / "corpus_metadata.csv", index=False)
print("rewrote data/corpus_metadata.csv |", len(meta), "rows x", len(cols), "cols\n")
prim = meta[meta.collection == "AI strategies"].sort_values("ai_density_per_1k", ascending=False)
print("=== PRIMARY: AI density per 1,000 words (multilingual count) ===")
print(prim[["country","language","status","word_count","ai_mentions",
            "ai_density_per_1k","genre_matches_collection"]].to_string(index=False))
print()
print("=== SECONDARY ===")
print(meta[meta.collection != "AI strategies"][["country","policy_domain","word_count",
      "ai_mentions","ai_density_per_1k","genre_matches_collection"]].to_string(index=False))
