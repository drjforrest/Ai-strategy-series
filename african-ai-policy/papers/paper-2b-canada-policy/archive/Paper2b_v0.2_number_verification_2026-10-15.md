# Paper 2b abstract v0.2 — corpus, methods and number verification
15 Oct 2026. Design: Canada-internal policy ecosystem; no external reference set. Supersedes the v0.1 memo (Africa-as-benchmark design, retired).

## Corpus
| Document | Year | Words | Source | Use |
|---|---|---|---|---|
| AI for All — Canada's National AI Strategy (ISED) | Jun 2026 | 13,483 | `african-ai-policy/data/canada/canada_ai.txt` | linkage + alignment |
| Pan-Canadian Health Data Strategy — 3 Expert Advisory Group reports (PHAC) | 2021–22 | 28,670 | `data/canada/canada_hd.txt` | linkage + alignment |
| Shared Pan-Canadian Interoperability Roadmap (Infoway) | Aug 2023 | 26,408 | `digital-health-canada/docs/SharedPan-CanadianInteroperabilityRoadmap_Aug2023_EN.pdf` → `raw/roadmap.txt` (pdfplumber, pipeline extractor) | linkage + alignment |
| Pan-Canadian AI for Health (AI4H) Guiding Principles (FPT) | Jan 2025 | 1,052 | canada.ca page, main content → `raw/ai4h.txt` | linkage + alignment (10 passages; score rests on top 3) |
| Pan-Canadian Health Data Charter (FPT) | Oct 2023 | 562 | canada.ca page → `raw/charter.txt` | linkage only (4 passages) |
| FPT Health Ministers' communiqué announcing the Joint FPT Action Plan | Oct 2023 | 1,494* | `digital-health-canada/docs/FPT Communique….pdf` → `raw/fpt_communique.txt` | linkage only; stands in for the Action Plan (no published full text located) |

*Includes repeated browser page headers and one duplicated paragraph; counts are used as presence/absence only.

## Instrument
Alignment: unchanged series instrument via `analyze_canada_benchmark.score_docs` (paraphrase-multilingual-MiniLM-L12-v2; ~150-word passages, 20-word overlap; top-10% mean, floor 3). Run in env `aipolicy-embed`; reproduced the stored 6 Oct Canadian scores to max |diff| 1.2e-7. Script: `score_canada_ecosystem.py`.
Linkage: deterministic regex on cleaned text, `linkage_canada_ecosystem.py`; self-references marked "self". AI density uses the series regex (`AI_TERM_RE`).

## Every number in the abstract
| Abstract claim | Value | File |
|---|---|---|
| Health-side cross-citations | Roadmap→PCHDS 3 (2 explicit "Pan-Canadian Health Data Strategy", 1 "Expert Advisory Group" as stakeholder); communiqué→Roadmap 1, →Charter 1; AI4H→Action Plan 1, →Charter 2 | `out/canada_ecosystem_crossrefs.csv` |
| No health-side document names a national AI strategy (2017 or 2026) | 0 in Roadmap, communiqué, Charter, EAG, AI4H | same |
| AI for All names none of the five health-side documents; 0 Infoway, 0 Health Canada (names CIHI 2, Statistics Canada 3) | — | same; `out/canada_ecosystem_actors.csv` |
| Health-data reference in AI for All = VITAL clinical-data platform ("Unlocking Canada's Health Data to Power AI Innovation") | — | text check |
| AI terms/1k: AI for All 37.68; Roadmap 0.04 (1 term in 26,408 words; "emerging technologies (e.g., artificial intelligence…) at the discretion of each jurisdiction"); EAG 0.42; AI4H 33.27 | — | crossrefs CSV + context check |
| Interoperability terms: Roadmap 347, EAG 73, AI for All 2 (AI models/standards) | — | crossrefs CSV |
| Mean alignment: AI for All 0.4524; Roadmap 0.5912; EAG 0.5952; AI4H 0.5029 (Charter 0.4850, not reported) | — | `out/canada_ecosystem_alignment_raw.csv` |
| AI for All below Roadmap and EAG on 9/9 components | True for both | same |
| C5 standards & interoperability: AI for All 0.4416, Roadmap 0.6415, EAG 0.6680, AI4H 0.5424 | widest **average** gap (0.213); vs Roadmap alone C3 (0.203) edges C5 (0.200) — hence "widest average gap" | same |

## Notes for co-authors
* ISED appears in the Roadmap only as a federal stakeholder with interoperability needs (3 mentions; regex double-counts name + acronym). Not used in the abstract, because AI for All names its own department.
* The Roadmap's "FPT Action Plan" reference (Aug 2023) is to an earlier FPT plan; it predates the Oct 2023 Joint Action Plan, so it is not counted as a citation of it.
* Dating: AI for All (2026) post-dates every health-side document, so its zero citations are the cleanest directional test. Health-side documents could have named the 2017 Pan-Canadian AI Strategy; none does.
* Not assessed: provincial/territorial strategies; Bill C-72 (Connected Care for Canadians Act); the Action Plan's full text.
