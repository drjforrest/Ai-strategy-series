"""Paper 2 — AI-strategy vs digital-health-strategy *connectivity* analysis.

Reframing this as a connectivity paper requires three reproducible measurements,
only the first of which currently exists in the repo:

  (i)   AI centrality        — explicit AI-term density per 1,000 words, by set
  (ii)  Competency overlap   — WHO-domain alignment, (re)scored here on the
                               digital-health set with the SAME instrument
  (iii) Document linkage     — citation / reference / shared-actor overlap
                               (NOT yet built — see report)

This script produces (i) and (ii) reproducibly. It reads the authoritative
primary AI-strategy scores (Ethiopia already excluded) and re-runs the WHO
instrument on the digital-health / digital-transformation text files.

HARD GUARD: cross-set comparison is only valid if every document is embedded
with the *same semantic* backend. If sentence-transformers is unavailable the
pipeline silently falls back to TF-IDF (lexical, non-comparable). We abort in
that case rather than emit corrupted numbers.

    python analyze_connectivity.py
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from src import alignment, competencies, config, preprocess
from src.models import load_embedding_model


# --------------------------------------------------------------------------- #
# Document sets, loaded from the corpus inventory (build_dh_corpus.py) so the
# set grows with the data rather than being hard-coded. Botswana is dropped: its
# PDF is scanned with no text layer (0 words).
# --------------------------------------------------------------------------- #
def _load_dh_sets() -> tuple[dict[str, str], dict[str, str]]:
    inv_path = config.OUTPUTS_DIR / "dh_corpus_inventory.csv"
    if not inv_path.exists():
        raise SystemExit(
            f"Missing {inv_path}. Run `./run.sh build_dh_corpus.py` first."
        )
    inv = pd.read_csv(inv_path)
    inv = inv[inv.words > 0]  # drop unextractable (scanned) documents
    dh = inv[inv.genre == "digital_health"]
    other = inv[inv.genre != "digital_health"]
    return (
        dict(zip(dh.country, dh.file)),
        dict(zip(other.country, other.file)),
    )


DH_SET, DT_SET = _load_dh_sets()

AI_TERM_RE = re.compile(
    r"\b(?:AI|artificial\s+intelligence|IA|intelligence\s+artificielle)\b",
    flags=re.IGNORECASE,
)


def ai_density_per_1k(text: str) -> float:
    words = len(text.split())
    if words == 0:
        return 0.0
    return 1000.0 * len(AI_TERM_RE.findall(text)) / words


def score_set(name_to_file: dict[str, str]) -> tuple[pd.DataFrame, "object"]:
    """Run the WHO instrument on a set of local .txt documents."""
    rows: list[dict] = []
    for country, fname in name_to_file.items():
        path = config.DH_DIR / fname
        if not path.exists():
            print(f"  ! missing {path.name} — skipping {country}")
            continue
        for i, chunk in enumerate(preprocess.load_and_chunk(path)):
            rows.append({"country": country, "chunk_id": i, "chunk_text": chunk})

    frame = pd.DataFrame(rows, columns=["country", "chunk_id", "chunk_text"])
    comp_df = competencies.load_competencies()
    model = load_embedding_model()

    if not model.name.startswith("sentence-transformers"):
        raise SystemExit(
            "ABORT: embedding backend is "
            f"'{model.name}', not a sentence-transformer. TF-IDF scores are "
            "lexical and NOT comparable with the primary matrix. Install "
            "sentence-transformers before running this analysis."
        )
    print(f"Embedding backend: {model.name}")

    corpus = competencies.embedding_texts(comp_df) + frame["chunk_text"].tolist()
    model.fit(corpus)
    comp_embeds = competencies.embed_competencies(comp_df, model, save_path=None)
    scores = alignment.build_alignment_scores(
        frame, comp_df, comp_embeds, model, cache_embeddings=False
    )
    return scores, model


def main() -> int:
    out = config.OUTPUTS_DIR / "connectivity"
    out.mkdir(parents=True, exist_ok=True)

    # --- (i) AI centrality across all three sets --------------------------- #
    dens_rows = []
    for set_name, mapping in {"AI strategy": None, "Digital health": DH_SET, "Digital transformation": DT_SET}.items():
        if set_name == "AI strategy":
            # Primary set: read the authoritative scores' countries and their txt files
            files = {c: config.COUNTRY_FILES[c] for c in config.COUNTRIES
                     if config.country_path(c).exists()}
            directory = config.NATIONAL_DIR
        else:
            files = mapping  # type: ignore[assignment]
            directory = config.DH_DIR
        for country, fname in files.items():
            path = directory / fname
            if not path.exists():
                continue
            text = preprocess.clean_text(preprocess.load_text(path))
            dens_rows.append({
                "set": set_name, "country": country,
                "words": len(text.split()),
                "ai_terms": len(AI_TERM_RE.findall(text)),
                "ai_density_per_1k": round(ai_density_per_1k(text), 2),
            })
    dens = pd.DataFrame(dens_rows)
    dens.to_csv(out / "ai_density_by_set.csv", index=False)

    print("\n=== (i) AI centrality (explicit AI terms per 1,000 words) ===")
    print(dens.groupby("set")["ai_density_per_1k"]
          .agg(["count", "min", "median", "max"]).round(2).to_string())

    # --- (ii) competency overlap ------------------------------------------ #
    primary = pd.read_csv(config.ALIGNMENT_SCORES_CSV)
    primary["set"] = "AI strategy"
    dh_scores, _ = score_set(DH_SET)
    dh_scores["set"] = "Digital health"
    dt_scores, _ = score_set(DT_SET)
    dt_scores["set"] = "Digital transformation"

    combined = pd.concat([primary, dh_scores, dt_scores], ignore_index=True)
    combined.to_csv(out / "alignment_all_sets.csv", index=False)

    per_country = (combined.groupby(["set", "country"])["similarity_score"]
                   .mean().round(4).reset_index())
    per_country.to_csv(out / "alignment_by_country.csv", index=False)

    dom = (combined.groupby(["set", "competency_id"])["similarity_score"]
           .mean().round(4).unstack("set"))
    dom.to_csv(out / "alignment_by_domain.csv")

    print("\n=== (ii) WHO-domain alignment by set (mean cosine) ===")
    print(dom.round(3).to_string())
    print("\n--- per-country mean alignment ---")
    print(per_country.to_string(index=False))

    print(f"\nWrote Paper-2 connectivity outputs -> {out}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
