"""Paper 2, measurement (iii) — document linkage.

Measures whether national AI strategies and digital-health strategies are
*connected within a national policy system* — via three deterministic signals
(regex/dictionary, NOT embeddings, so this is a distinct method from the
alignment work):

  A. Cross-reference  — does the AI strategy name the country's digital-health
                        strategy (and vice versa)?
  B. Institutional    — how strongly does each document engage the *other*
                        sector's vocabulary (health anchors in AI docs; AI
                        anchors in digital-health docs)?
  C. Shared actors    — Jaccard overlap of named government bodies across a
                        country's matched document pair.
  + Coverage          — how many AI-strategy countries even HAVE a matched
                        digital-health document in the corpus (the structural
                        finding).

Reads only local .txt files. No model, no network, fully reproducible.

    ./run.sh analyze_linkage.py
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

from src import config, preprocess

OUT = config.OUTPUTS_DIR / "connectivity"
AI_DIR = config.NATIONAL_DIR
DH_DIR = config.DH_DIR


# Digital-health set from the corpus inventory (build_dh_corpus.py): health-sector
# documents only, excluding unextractable (scanned) PDFs.
def _load_dh_set() -> dict[str, str]:
    inv = pd.read_csv(config.OUTPUTS_DIR / "dh_corpus_inventory.csv")
    dh = inv[(inv.genre == "digital_health") & (inv.words > 0)]
    return dict(zip(dh.country, dh.file))


DH_SET = _load_dh_set()  # country -> dh .txt filename


# Countries with BOTH a national AI strategy and a digital-health strategy, i.e.
# the pairs in which cross-document linkage can actually be measured.
def _matched() -> dict[str, tuple[str, str]]:
    out = {}
    for c, dh_file in DH_SET.items():
        if c in config.COUNTRY_FILES and config.country_path(c).exists():
            out[c] = (config.COUNTRY_FILES[c], dh_file)
    return out


MATCHED = _matched()

# --------------------------------------------------------------------------- #
# Term sets (EN + FR so the multilingual corpus is covered)
# --------------------------------------------------------------------------- #
HEALTH_ANCHORS = [
    r"digital\s+health", r"e-?health", r"health\s+information\s+system",
    r"health\s+data", r"ministry\s+of\s+health", r"health\s+work(?:er|force)",
    r"patient", r"clinical", r"diagnostic", r"disease\s+surveillance",
    r"telemedicine", r"primary\s+care",
    r"sant[ée]\s+num[ée]rique", r"minist[èe]re\s+de\s+la\s+sant[ée]",
    r"donn[ée]es\s+de\s+sant[ée]",
]
AI_ANCHORS = [
    r"artificial\s+intelligence", r"machine\s+learning", r"deep\s+learning",
    r"\balgorithm", r"\bAI\b",
    # French: the abbreviation "IA" is essential — omitting it under-counts the
    # French-language strategies (Senegal, Côte d'Ivoire) by ~7x and would inject
    # exactly the language bias this study warns against.
    r"\bIA\b",
    r"intelligence\s+artificielle", r"apprentissage\s+automatique", r"algorithme",
]

# Named cross-document references
AI_TO_DH_REF = [
    r"digital\s+health\s+strateg(?:y|ic\s+plan)", r"e-?health\s+strateg",
    r"national\s+digital\s+health", r"health\s+sector\s+strateg",
    r"strat[ée]gie\s+de\s+sant[ée]\s+num[ée]rique",
]
DH_TO_AI_REF = [
    r"artificial\s+intelligence\s+strateg", r"national\s+AI\s+strateg",
    r"\bAI\s+polic", r"intelligence\s+artificielle",
]

AGENCY_RE = re.compile(
    r"\b(?:Ministry|Department|Authority|Agency|Commission|Board|Council|"
    r"Institute|Bureau|Bank)\s+of\s+[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*",
)

_compiled = {}


def _count(patterns: list[str], text: str) -> int:
    total = 0
    for p in patterns:
        rx = _compiled.setdefault(p, re.compile(p, re.IGNORECASE))
        total += len(rx.findall(text))
    return total


def _density(count: int, words: int) -> float:
    return round(1000.0 * count / words, 3) if words else 0.0


def _read(path: Path) -> str | None:
    if not path.exists():
        return None
    return preprocess.clean_text(preprocess.load_text(path))


def _agencies(text: str) -> set[str]:
    return {re.sub(r"\s+", " ", m).strip().lower() for m in AGENCY_RE.findall(text)}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------ #
    # Coverage: how many AI-strategy countries have a matched DH doc?
    # ------------------------------------------------------------------ #
    ai_countries = [c for c in config.COUNTRIES
                    if config.country_path(c).exists() and c != "African Union"]
    dh_countries = list(DH_SET)
    both = sorted(set(ai_countries) & set(dh_countries))
    coverage = {
        "ai_strategy_countries": len(ai_countries),
        "digital_health_countries": len(dh_countries),
        "countries_with_both": len(both),
        "both_list": ", ".join(both),
        "share_with_both": round(len(both) / len(ai_countries), 3),
    }
    pd.DataFrame([coverage]).to_csv(OUT / "linkage_coverage.csv", index=False)

    print("=== Coverage: matched AI+health document pairs ===")
    print(f"  AI-strategy countries: {coverage['ai_strategy_countries']} | "
          f"digital-health countries: {coverage['digital_health_countries']} | "
          f"with BOTH: {coverage['countries_with_both']} "
          f"({coverage['share_with_both']:.0%}) -> {coverage['both_list']}")

    # ------------------------------------------------------------------ #
    # A + B: cross-reference and institutional engagement, over ALL docs
    # ------------------------------------------------------------------ #
    rows = []
    for c in ai_countries:
        text = _read(config.country_path(c))
        if text is None:
            continue
        w = len(text.split())
        rows.append({
            "country": c, "doc": "AI strategy",
            "words": w,
            "other_sector_refs": _count(AI_TO_DH_REF, text),
            "other_sector_density": _density(_count(AI_TO_DH_REF, text), w),
            "health_anchor_density": _density(_count(HEALTH_ANCHORS, text), w),
            "ai_anchor_density": _density(_count(AI_ANCHORS, text), w),
        })
    for c in dh_countries:
        text = _read(DH_DIR / DH_SET[c])
        if text is None:
            continue
        w = len(text.split())
        rows.append({
            "country": c, "doc": "Digital-health strategy",
            "words": w,
            "other_sector_refs": _count(DH_TO_AI_REF, text),
            "other_sector_density": _density(_count(DH_TO_AI_REF, text), w),
            "health_anchor_density": _density(_count(HEALTH_ANCHORS, text), w),
            "ai_anchor_density": _density(_count(AI_ANCHORS, text), w),
        })
    docs = pd.DataFrame(rows)
    docs.to_csv(OUT / "linkage_by_document.csv", index=False)

    print("\n=== A/B: cross-sector reference and engagement by document ===")
    print(docs[["country", "doc", "other_sector_refs", "other_sector_density",
                "health_anchor_density", "ai_anchor_density"]].to_string(index=False))

    # ------------------------------------------------------------------ #
    # C: shared actors within matched pairs
    # ------------------------------------------------------------------ #
    pair_rows = []
    for c, (ai_f, dh_f) in MATCHED.items():
        ai_t, dh_t = _read(AI_DIR / ai_f), _read(DH_DIR / dh_f)
        if ai_t is None or dh_t is None:
            continue
        a, d = _agencies(ai_t), _agencies(dh_t)
        shared = a & d
        union = a | d
        pair_rows.append({
            "country": c,
            "agencies_ai": len(a), "agencies_dh": len(d),
            "shared_agencies": len(shared),
            "jaccard": round(len(shared) / len(union), 3) if union else 0.0,
            "shared_examples": "; ".join(sorted(shared)[:5]),
        })
    pairs = pd.DataFrame(pair_rows)
    pairs.to_csv(OUT / "linkage_shared_actors.csv", index=False)

    print("\n=== C: shared government actors within matched pairs ===")
    if pairs.empty:
        print("  (no matched pairs found)")
    else:
        print(pairs.to_string(index=False))

    print(f"\nWrote document-linkage outputs -> {OUT}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
