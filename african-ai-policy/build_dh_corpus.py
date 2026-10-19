"""Extract the expanded digital-health corpus to text and inventory it.

The digital-health folder grew from 3 to many countries. Filenames are irregular
(country-code prefixes, opaque hashes, French titles), so rather than fuzzy-match
we use an explicit, reviewable filename -> country map. Extraction is skipped
where the target .txt already exists (use --force to redo).

Genre calls are recorded explicitly, not inferred:
  * South Africa's file is misnamed "national-digital-strategy..." but its actual
    title (verified from the PDF) is the *National Digital Health Strategy for
    South Africa 2019-2024* (National Department of Health) -> digital-health set.
  * Uganda's document is a digital-transformation roadmap -> 'digital-transformation'.
  * Nigeria's NDHA is a digital-health *architecture* (infrastructure), still
    health-sector -> kept in the DH set but flagged type=architecture.

    ./run.sh build_dh_corpus.py
    ./run.sh build_dh_corpus.py --force
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

from src import config, preprocess
from scripts.extract_pdfs import extract_text

# country -> (pdf filename, genre) ; genre in {digital_health, national_digital, digital_transformation}
DH_MAP: dict[str, tuple[str, str]] = {
    "Rwanda":       ("RWA_Rwanda_Digital-Health-Strategy_2018-2023.pdf", "digital_health"),
    "Namibia":      ("NAM_Namibia_National-eHealth-strategy_2021-2025.pdf", "digital_health"),
    "Mauritius":    ("Roadmap_for_Digital_Health_Transformation_in_Mauritius.pdf", "digital_health"),
    "Burundi":      ("BDI_Burundi_National-plan-development-digital-health_2020-2024.pdf", "digital_health"),
    "Botswana":     ("BOT_Botswana_eHealth-Strategy_2020-2024.pdf", "digital_health"),
    # Kenya: the Digital Health Agency's national Strategic Plan 2025-2028 (the
    # statutory agency established by the Digital Health Act 2023). A national
    # health-sector digital strategy document; the 2016-2030 National eHealth
    # Policy is the alternative/earlier entry.
    "Kenya":        ("DHA_Strategic_Plan_2025_2028_Stakeholder_Version_July_25_4a65588a18.pdf", "digital_health"),
    "Ethiopia":     ("ETH_Ethiopia_Digital-Health-Blueprint_2021.pdf", "digital_health"),
    "Ghana":        ("gha_ghana_policy-and-strategy-on-digital-health_2023-2027.pdf", "digital_health"),
    "Niger":        ("NER_Niger_National-eHealth-Strategy_2019-2023.pdf", "digital_health"),
    "Senegal":      ("Plan Stratégique Santé Digitale 2018 - 2023.pdf", "digital_health"),
    "DRC":          ("pndisii_2020_2024.pdf", "digital_health"),
    "Nigeria":      ("83cfc4_4e435ffb27084421b62605872634624b.pdf", "digital_health"),
    "Sierra Leone": ("SLE_Sierra_Leone_National-Digital-Health-Strategy_2018-2023.pdf", "digital_health"),
    "Zambia":       ("ZMB_Zambia_Digital-Health-Strategy_2022-2026.pdf", "digital_health"),
    "South Africa": ("national-digital-strategy-for-south-africa-2019-2024-b.pdf", "digital_health"),
    "Uganda":       ("Uganda Digital Transformation Roadmap.pdf", "digital_transformation"),
}

AI_RE = re.compile(r"\b(?:AI|IA|artificial\s+intelligence|intelligence\s+artificielle)\b", re.IGNORECASE)


def slug(country: str) -> str:
    return country.lower().replace(" ", "_").replace("'", "")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="re-extract even if the .txt exists")
    args = ap.parse_args()

    rows = []
    for country, (pdf_name, genre) in DH_MAP.items():
        pdf = config.DH_DIR / pdf_name
        txt = config.DH_DIR / f"{slug(country)}_dh.txt"
        if not pdf.exists():
            print(f"  ! missing PDF for {country}: {pdf_name}")
            continue
        # Treat a missing OR empty .txt as needing (re)extraction. A prior failed
        # run can leave a 0-byte file, which would otherwise be skipped forever.
        needs_extract = args.force or (not txt.exists()) or txt.stat().st_size == 0
        if needs_extract:
            txt.write_text(extract_text([pdf]), encoding="utf-8")
            if txt.stat().st_size == 0:
                print(f"  ! {country}: extraction produced NO text "
                      f"(scanned PDF with no text layer — needs OCR)")
        text = preprocess.clean_text(preprocess.load_text(txt))
        words = len(text.split())
        rows.append({
            "country": country,
            "genre": genre,
            "file": txt.name,
            "words": words,
            "ai_terms": len(AI_RE.findall(text)),
            "ai_density_per_1k": round(1000.0 * len(AI_RE.findall(text)) / words, 2) if words else 0.0,
        })

    df = pd.DataFrame(rows).sort_values(["genre", "country"])
    out = config.OUTPUTS_DIR / "dh_corpus_inventory.csv"
    df.to_csv(out, index=False)

    print(f"\n=== digital-health / digital-transformation corpus (n = {len(df)}) ===")
    with pd.option_context("display.width", 160, "display.max_columns", 20):
        print(df.to_string(index=False))
    print(f"\nby genre:\n{df.groupby('genre').size().to_string()}")
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
