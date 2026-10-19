# Paper 2b — Curriculum–policy alignment: analysis protocol

19 October 2026. Supersedes the policy-ecosystem framing (abstract v0.3) and the CDHS/education option in `Canada_rethink_CDHS_2026-10-18.md` as the e-Health27 submission design. Decision by J. Forrest: restrict Paper 2b to the methods used in Paper 1 so the move from Africa to Canada is methodologically continuous.

## Question

How closely does publicly documented Canadian health-informatics / HIM education align with the content of Canada's national digital-health and AI policy corpus?

## Data

**Policy corpus (unchanged from v0.2/v0.3):** AI for All (ISED, Jun 2026); pCHDS Expert Advisory Group reports (2021–22); Infoway Shared Pan-Canadian Interoperability Roadmap (Aug 2023); AI4H Guiding Principles (Jan 2025); Health Data Charter (2023); FPT communiqué (Oct 2023). The short-document rule still applies: the Charter is used for linkage only, not alignment scoring.

**Curriculum corpus:** `outputs/2026-10-18-canada-schema/Canadian_HI_HIM_Curriculum_Source_Package` — 114 programme entries (91 seed + 23 added), 269 unique source URLs over 72 hosts. Package source quality: A 47, B 38, C 25, D 4. Scope screen: 74 named HI/HIM/digital-health programmes, 37 adjacent/comparator programmes, 3 unresolved identities.

The package contains no page bodies. Text is re-retrieved by `paper2b_canada_ecosystem/curriculum/fetch_curriculum_sources.py` (run locally) into `paper2b_canada_ecosystem/raw/curriculum/` with a fetch log (status, bytes, text length, SHA-256, possible-JS-shell flag).

## Eligibility and text rules (fixed before scoring)

1. Unit = programme entry, after resolving the package's flagged duplicates and aliases (`candidate_reconciliation.json`). Bundled rows are not counted as independent programmes.
2. Primary group = named HI/HIM/digital-health programmes; comparison group = adjacent/comparator programmes; unresolved identities are excluded.
3. Only text from official institutional sources goes into the embedding corpus. Pages whose host fails the package `authority_check` are excluded from the primary analysis.
4. The package's generated `requirements_summary` and `source_notes` annotations are never embedded.
5. Pages whose text is a JavaScript shell or a retrieval failure are recorded as *insufficient documentation*, never as zero alignment (package code D rule).
6. Source genre is recorded per programme: course descriptions/requirements (A/B) vs programme overview/marketing (C). The primary analysis uses A/B; C enters a sensitivity analysis.
7. Minimum text: the series floor of TOP_FRAC_FLOOR = 3 chunks applies, and the same short-document rule as for the policy corpus (programmes below the floor are reported, not scored).
8. French sources are embedded in the original language. The multilingual model is the same one used in Paper 1, as for Côte d'Ivoire and Senegal.

## Measures (Paper 1 / Paper 2b instruments, unchanged)

- **Model and aggregation:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`; same chunking; `top_frac_mean` with TOP_FRACTION = 0.10 and floor 3.
- **M1 — Component profile.** Score each programme and each policy document against the same nine WHO Global Strategy on Digital Health core components (C1–C9; C7 = health workforce) used for the Paper 2b policy scoring. M2 follows `analyze_au_convergence.py`: z-score each component across the scorable programmes, place each policy document (and the pooled policy profile) on that scale, and take the Pearson r of the emphasis profiles. Compare the curriculum profile with the policy profile per component, by rank and by within-profile differences. Raw cross-genre cosine levels are not compared directly.
- **M2 — Policy convergence.** Similarity of each programme to the policy corpus, computed the way Paper 1 computed national convergence on the AU continental strategy, for the corpus overall and per document (e.g. AI for All vs the health-side documents).
- **M3 — AI emphasis.** Same AI-term dictionary density (per 10k words) as Paper 1, curriculum vs policy.
- **Comparison:** named HI/HIM programmes vs adjacent programmes on M1–M3 (rank-based tests, effect sizes; descriptive given the sample).
- **Sensitivity:** include C-quality programmes; exclude French programmes; restrict to course-description text only.

## Reference framework decision (19 Oct, J. Forrest)

The primary reference is now the **Digital Health Canada Health Informatics Professional Competencies (2022)**: 55 statements in 7 domains (`data/dhc_competencies/`, PDF SHA-256 9cc35…). WHO C1–C9 is retained as a secondary reference, kept for continuity with Paper 1. The instrument is unchanged. Each DHC statement is one reference item ("domain. statement"); domain score = mean of its statement scores. B4.1 exceeds the model's 128-token limit, so it is split into a–e and averaged back. Sensitivity analyses use the 55-statement profile and the 32 statements tested on the CA exam (Candidate Handbook v250410).

Script: `curriculum/score_curriculum_dhc.py` → `out/curriculum/dhc/`.

### DHC results (primary set: 30 named, 18 adjacent)

- **M2 is null under DHC.** Named and adjacent programmes do not differ in profile convergence with any policy document: all 8 analyses give p ≥ 0.05 (`sensitivity_summary_dhc.csv`). The WHO-based EAG convergence difference therefore depends on the reference and is not a headline result. Programme-level r under WHO and DHC agrees only moderately: Spearman 0.52 for EAG, 0.44 for AI for All.
- **Policy side.** AI for All is the lowest-scoring policy document on 6 of 7 DHC domains; AI4H is lowest on C6 (10 passages, less stable). Of the three long documents, AI for All is lowest on 55 of 55 statements. Mean across domains: AI for All 0.399, AI4H 0.422, EAG 0.540, Roadmap 0.544. Caveat: AI for All is a whole-of-economy strategy, so some of this gap is by design.
- **Curricula vs policy order.** The domain-emphasis order of named-programme medians agrees with the pooled policy order: Spearman ρ = 0.75 (p = 0.052, 7 domains). The adjacent-programme order agrees too (ρ = 0.89), so this is not specific to HI. Both rank B4 Canadian health system 1st and C6 Project management 7th. A2 Technology ecosystem is 2nd in policy and 5th in curricula.
- **M1, named vs adjacent raw domain scores** (same genre on both sides). Named programmes are higher on B4 (p = 0.051) and B3 (p = 0.062); no domain reaches p < 0.05.
- **AI.** 0 of 55 DHC statements mention AI or machine learning; the nearest is A2.9, emerging technologies. 17 of 30 named curricula contain no AI term, against 37.68 per 1,000 words in AI for All and 33.27 in AI4H.

## Interpretation limits

- The results describe *publicly documented* curricula. Absence from a page is not absence from teaching, and alignment is a permissible finding.
- Programme counts are not graduate output or workforce supply; province-level patterns may reflect how intensively each province was searched (the inventory had a BC-specific completeness pass).
- Embedding similarity measures textual correspondence, not competence or implementation.

## Conference scope (e-Health27, deadline 20 Oct 2026, 17:00 PT)

The abstract reports only what is actually scored by the deadline, with denominators: programmes eligible, retrieved, scorable. If scoring is partial, it is labelled as a pilot. No projected findings.

## Status

- [x] Curriculum source package (18 Oct)
- [x] Downloader written and parser-tested offline (19 Oct)
- [x] Local fetch run (19 Oct): 235/269 sources retrieved (207 HTML, 28 PDF); 34 failed (16 × HTTP 202 empty bot-challenge responses — Queen's, McGill, Ontario Tech; 9 × 403 — e.g. George Brown, Brock; 5 × 404; 2 × 502; 1 SSL; 1 timeout); 26 retrieved pages are possible JS shells (< 400 chars). Log: `paper2b_canada_ecosystem/raw/curriculum/fetch_log.csv`.
- [x] Corpus built (`curriculum/build_curriculum_corpus.py` → `raw/curriculum/corpus/`, register `programme_corpus_register.csv`). Implemented rules: primary text = requirements/course-description pages + package verbatim descriptions; extended = + status/supporting pages; non-institutional hosts excluded (NIHI, CCHIM, Health Info Canada, StudyInCanada, CanAm, Azent, Naver, OPPQ, Bordeaux); CA-P103/P104 merged into CA-P037 (112 units). Whole calendars (e.g. Dalhousie 2017–18 graduate calendar, 2.85M chars) are status/supporting sources, so they enter the extended set only; sources > 40k chars are flagged per programme.
- Scorable (primary text, ≥ 10 passages): 30/74 named, 18/36 adjacent. At the 3-passage floor: 40 named, 25 adjacent. Extended text, ≥ 10 passages: 54 named, 28 adjacent.
- [x] Scored M1–M3 (19 Oct; `curriculum/score_curriculum_alignment.py` → `out/curriculum/`). Policy-document scores reproduce the stored Paper 2b values exactly (max |Δ| = 0.0, 36 values). Primary results (30 named, 18 adjacent):
  - M2 median profile r, named vs adjacent: EAG 0.300 vs −0.249 (Mann–Whitney p = 0.005, rank-biserial 0.49); Roadmap 0.171 vs −0.214 (p = 0.036); AI4H 0.098 vs 0.112 (p = 0.62); AI for All −0.118 vs 0.195 (p = 0.046); pooled policy 0.175 vs −0.062 (p = 0.075). Only EAG survives Bonferroni correction across 5 anchors.
  - M3: AI for All 37.68 and AI4H 33.27 AI terms/1k words; EAG 0.42; Roadmap 0.04. Named programmes: median 0.00/1k; 17/30 contain no AI term; hits are mostly a single dedicated AI course (e.g. Northeastern Vancouver HINF 5500, Douglas HIMP 4510).
  - M1 component ranks (1 = strongest), named-programme median vs pooled policy: C5 standards/interoperability 1 vs 2; C7 workforce 3 vs 8; C9 people-centred 4 vs 1; C2 investment 9 vs 9.
  - Sensitivity (`out/curriculum/sensitivity_summary.csv`): the EAG difference holds at the ≥3-passage floor, without large sources, without French programmes, and with package-quality A only (p 0.003–0.044). It weakens with extended (overview/marketing) text (p = 0.090). The AI for All difference is not robust (p 0.11–0.44 outside the primary analysis), though the named median r is negative in every analysis.
  - Disclosure: the author's own programme (CA-P006, Northeastern Vancouver) is in the sample.
- [ ] Number verification; abstract v0.4
