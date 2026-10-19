"""Paper 2 — Canadian benchmark: score the Canadian AI strategy and the
Pan-Canadian Health Data Strategy with the SAME WHO instrument used on the
African corpus.

Canada is a BENCHMARK case, not a sampling-frame observation. It is a
high-income, bilingual, federated country that produced an AI strategy and a
health-data strategy in the same period. The question: do the two Canadian
streams connect — and does that pattern differ from the African disconnection
(structural problem) or resemble a well-wired system (governance design choice)?

Reuses the validated instrument unchanged:
    clean -> chunk -> paraphrase-multilingual-MiniLM-L12-v2 -> cosine vs the
    nine WHO Global Strategy on Digital Health core components, aggregated by
    top_frac_mean (top 10%, floor 3) — identical to analyze_connectivity.py.

HARD GUARD: aborts on the TF-IDF fallback (lexical, non-comparable), exactly as
analyze_connectivity.py does.

    ./run.sh analyze_canada_benchmark.py
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from src import alignment, competencies, config, preprocess
from src.models import load_embedding_model

CANADA_DIR = config.DATA_DIR / "canada"
OUT_DIR = config.OUTPUTS_DIR / "canada"

# PDF (or PDFs) -> the two logical documents we score. The three EAG reports are
# components of one national health-data strategy and are concatenated, mirroring
# how scripts/extract_pdfs.py joins multi-PDF countries.
CANADA_DOCS: dict[str, list[str]] = {
    "Canada AI strategy": ["ai-strategy-en.pdf"],
    "Canada health-data strategy": [
        "pCHDS-first-EAG-report-en.pdf",
        "expert-advisory-group-report-02-building-canada-health-data-foundation.pdf",
        "expert-advisory-group-report-03-toward-world-class-health-data-system.pdf",
    ],
}
DOC_FILES: dict[str, str] = {
    "Canada AI strategy": "canada_ai.txt",
    "Canada health-data strategy": "canada_hd.txt",
}

# Same AI-terminology regex as analyze_connectivity.py (EN + FR).
AI_TERM_RE = re.compile(
    r"\b(?:AI|artificial\s+intelligence|IA|intelligence\s+artificielle)\b",
    flags=re.IGNORECASE,
)

# Coarse shared-actor proxy across the Canadian pair: named national health-data
# bodies. Mirrors the African linkage_shared_actors method at single-pair grain.
ACTOR_PATTERNS: dict[str, str] = {
    "CIHI": r"\b(?:CIHI|Canadian\s+Institute\s+for\s+Health\s+Information)\b",
    "Infoway": r"\b(?:Canada\s+Health\s+Infoway|Infoway)\b",
    "Statistics Canada": r"\b(?:Statistics\s+Canada|StatCan)\b",
    "PHAC": r"\bPublic\s+Health\s+Agency\s+of\s+Canada\b",
    "Health Canada": r"\bHealth\s+Canada\b",
    "CIHR": r"\b(?:CIHR|Canadian\s+Institutes?\s+of\s+Health\s+Research)\b",
    "CADTH": r"\b(?:CADTH|Canada'?s\s+Drug\s+Agency)\b",
}


def extract_pdf_text(pdf_paths: list[Path]) -> str:
    """PDF(s) -> cleaned text, concatenated with provenance markers."""
    import pdfplumber

    parts: list[str] = []
    for pdf_path in pdf_paths:
        with pdfplumber.open(pdf_path) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        body = preprocess.clean_text("\n\n".join(pages))
        marker = f"\n\n== source: {pdf_path.name} ==\n\n" if len(pdf_paths) > 1 else ""
        parts.append(f"{marker}{body}")
    return "\n".join(parts).strip()


def ensure_canada_texts(force: bool = False) -> dict[str, Path]:
    """Extract each Canadian document to .txt once (kept as an audit trail)."""
    paths: dict[str, Path] = {}
    for doc, pdf_names in CANADA_DOCS.items():
        target = CANADA_DIR / DOC_FILES[doc]
        pdfs = [CANADA_DIR / n for n in pdf_names]
        missing = [p.name for p in pdfs if not p.exists()]
        if missing:
            raise SystemExit(f"Missing Canadian PDF(s) under {CANADA_DIR}: {missing}")
        if force or not (target.exists() and target.stat().st_size > 0):
            target.write_text(extract_pdf_text(pdfs), encoding="utf-8")
        paths[doc] = target
    return paths


def ai_density(text: str) -> tuple[int, float]:
    words = len(text.split())
    n = len(AI_TERM_RE.findall(text))
    return n, (1000.0 * n / words if words else 0.0)


def score_docs(text_paths: dict[str, Path], model) -> pd.DataFrame:
    """Run the WHO instrument over the Canadian documents."""
    rows: list[dict] = []
    for doc, path in text_paths.items():
        for i, chunk in enumerate(preprocess.load_and_chunk(path)):
            rows.append({"country": doc, "chunk_id": i, "chunk_text": chunk})
    frame = pd.DataFrame(rows, columns=["country", "chunk_id", "chunk_text"])
    comp_df = competencies.load_competencies()
    comp_embeds = competencies.embed_competencies(comp_df, model, save_path=None)
    return alignment.build_alignment_scores(
        frame, comp_df, comp_embeds, model, cache_embeddings=False
    )


def actor_mentions(text: str) -> set[str]:
    return {
        actor
        for actor, pat in ACTOR_PATTERNS.items()
        if re.search(pat, text, flags=re.IGNORECASE)
    }


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    text_paths = ensure_canada_texts()
    raw = {doc: preprocess.clean_text(preprocess.load_text(p)) for doc, p in text_paths.items()}

    model = load_embedding_model()
    if not model.name.startswith("sentence-transformers"):
        raise SystemExit(
            "ABORT: embedding backend is "
            f"'{model.name}', not a sentence-transformer. TF-IDF scores are "
            "lexical and NOT comparable with the African matrix. Run via "
            "./run.sh (project venv) with sentence-transformers installed."
        )
    print(f"Embedding backend: {model.name}\n")

    # --- AI centrality ---------------------------------------------------- #
    dens_rows = []
    for doc, text in raw.items():
        n, d = ai_density(text)
        dens_rows.append(
            {"document": doc, "words": len(text.split()), "ai_terms": n,
             "ai_density_per_1k": round(d, 2)}
        )
    dens = pd.DataFrame(dens_rows)
    dens.to_csv(OUT_DIR / "canada_ai_density.csv", index=False)

    print("=== AI centrality — explicit AI terms per 1,000 words ===")
    print(dens.to_string(index=False))
    print("\nAfrican reference (from outputs/connectivity/):")
    print("  AI strategies   19.29–46.86/1k (median ~35.5)")
    print("  Digital health   0.00–1.11/1k  (median ~0.16)")

    # --- WHO-domain alignment -------------------------------------------- #
    scores = score_docs(text_paths, model)
    scores.to_csv(OUT_DIR / "canada_alignment_raw.csv", index=False)

    dom = (scores.groupby(["country", "competency_id"])["similarity_score"]
           .mean().round(4).unstack("country"))

    # Attach the African baselines for an at-a-glance comparison.
    africa_path = config.OUTPUTS_DIR / "connectivity" / "alignment_by_domain.csv"
    if africa_path.exists():
        africa = pd.read_csv(africa_path).set_index("competency_id")
        africa = africa.rename(columns={"AI strategy": "Africa AI",
                                        "Digital health": "Africa DH"})
        view = africa[["Africa AI", "Africa DH"]].join(dom)
    else:
        view = dom
    view.to_csv(OUT_DIR / "canada_alignment_by_domain.csv")

    print("\n=== WHO-domain alignment (mean cosine, by set) ===")
    print(view.round(3).to_string())

    summary_rows = []
    for col, label in [(c, c) for c in dom.columns]:
        summary_rows.append({"set": label, "mean_alignment": round(float(dom[col].mean()), 4)})
    if africa_path.exists():
        for a_col in ["Africa AI", "Africa DH"]:
            if a_col in view.columns:
                summary_rows.append({"set": a_col,
                                     "mean_alignment": round(float(view[a_col].mean()), 4)})

    # --- Linkage proxy across the Canadian pair --------------------------- #
    ai_text = raw["Canada AI strategy"]
    hd_text = raw["Canada health-data strategy"]
    ai_actors, hd_actors = actor_mentions(ai_text), actor_mentions(hd_text)
    shared = ai_actors & hd_actors
    union = ai_actors | hd_actors
    jaccard = round(len(shared) / len(union), 3) if union else 0.0

    link = {
        "ai_actors": "; ".join(sorted(ai_actors)) or "(none)",
        "hd_actors": "; ".join(sorted(hd_actors)) or "(none)",
        "shared_actors": "; ".join(sorted(shared)) or "(none)",
        "shared_jaccard": jaccard,
        "ai_names_health_data_strategy": bool(
            re.search(r"health\s+data\s+strategy|pan-?canadian\s+health\s+data", ai_text, re.I)
        ),
        "hd_names_ai_strategy": bool(
            re.search(r"artificial\s+intelligence\s+strategy|AI\s+for\s+All", hd_text, re.I)
        ),
    }
    pd.DataFrame([link]).to_csv(OUT_DIR / "canada_linkage_proxy.csv", index=False)

    print("\n=== Document linkage (Canadian pair, coarse proxy) ===")
    for k, v in link.items():
        print(f"  {k}: {v}")
    print("\nAfrican reference: shared-actor Jaccard 0.00–0.25; no AI strategy")
    print("names its health counterpart; only 2 of 12 health strategies name the AI strategy.")

    pd.DataFrame(summary_rows).to_csv(OUT_DIR / "canada_summary.csv", index=False)
    print(f"\nWrote Canadian benchmark outputs -> {OUT_DIR}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
