"""Step 4: update corpus_metadata.csv to reflect the executed corpus state."""
import pathlib, re, pandas as pd

D = pathlib.Path("data")
m = pd.read_csv(D / "corpus_metadata.csv")

# recompute Kenya word count from the cleaned extract
ken = (D / "national_strategies" / "kenya_ai.txt").read_text()
AI_RE = re.compile(r"\bAI\b|\bIA\b|\bartificial intelligence\b|\bintelligence artificielle\b", re.I)
i = m.index[m.country == "Kenya"][0]
m.loc[i, "word_count"] = len(ken.split())
m.loc[i, "ai_mentions"] = len(AI_RE.findall(ken))
m.loc[i, "ai_density_per_1k"] = round(m.loc[i, "ai_mentions"] / m.loc[i, "word_count"] * 1000, 2)
m.loc[i, "provenance_flag"] = "RESOLVED 2026-09-30: 389-word NotebookLM derivative excised"

# Ethiopia: excluded from primary corpus
m["in_primary_corpus"] = True
j = m.index[m.country == "Ethiopia"][0]
m.loc[j, "in_primary_corpus"] = False
m.loc[j, "provenance_flag"] = "EXCLUDED 2026-09-30: genre mismatch; archived in data/_excluded/"

# Uganda: not a digital-health strategy -> not in secondary track
k = m.index[(m.country == "Uganda")][0]
m.loc[k, "in_primary_corpus"] = False

cols = list(m.columns)
m.to_csv(D / "corpus_metadata.csv", index=False)
print("updated corpus_metadata.csv")
print()
print(m[["collection","country","status","word_count","ai_density_per_1k",
         "genre_matches_collection","in_primary_corpus"]].to_string(index=False))
