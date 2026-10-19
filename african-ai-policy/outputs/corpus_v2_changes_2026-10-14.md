# Corpus v2 — reference date 30 Sep 2026 (branch `corpus-v2-cutoff-2026-09-30`)

Backup of the pre-change state: `_backup/20261014-115025-pre-corpus-v2/`.
Regeneration log: `_verify/corpus_v2_regeneration_2026-10-14.log`.
Environment check: before any corpus change, the chain was re-run on the v1 corpus in a
fresh pinned environment (sentence-transformers 5.6.0, torch 2.13.0); it reproduced every
v1 output (max abs diff 1e-5; chunk embeddings 2e-7).

## Corpus changes (12 national + AU -> 15 national + AU)
| Country | Change | Document now analysed | Source |
|---|---|---|---|
| Ghana | REPLACED | National AI Strategy 2025-2035 (MoCDTI, Dec 2025; launched Apr 2026), 19,536 words | AAGI mirror (official-domain copy still to locate). Old Oct-2022 draft -> `data/_superseded/` |
| Mauritius | REPLACED | AI for Mauritius (AIM) National AI Strategy 2025-2029 (launched 10 Apr 2026), 16,191 words | mitci.govmu.org (official). 2018 report -> `data/_superseded/` |
| Ethiopia | ADDED | National Artificial Intelligence Policy (FDRE, June 2024), English half only, 8,442 words | OECD.AI. Amharic stripped by `scripts/strip_ethiopic.py`. Digital Ethiopia docs stay in `data/_excluded/` |
| Zambia | ADDED | National AI Strategy 2024-2026 (Ministry of Technology and Science), 12,640 words | OECD.AI |
| Mauritania | ADDED | National AI Strategy 2025-2029 (English), 10,839 words | mtnima.gov.mr (official) |
| South Africa | KEPT, FLAGGED | Draft National AI Policy (withdrawn 26 Apr 2026, fictitious references) | sensitivity `no_ZA` in `outputs/sensitivity/` |
| Tanzania | KEPT | Draft v0.6 (the census "Final..." file is the same document) | now in the readiness comparison |

Not added: Libya (Arabic; official site TLS certificate expired; Arabic extraction needs a
repair step — pdfplumber returns visual order, pypdfium2 reverses lam-alef); Algeria,
Namibia, Tunisia, Cameroon (no full text located); Guinea, Angola, Lesotho, Morocco
(not published / no document / draft / no full text). Burundi and Cape Verde inbox files are
misfiled/misattributed (a Senegal/Nigeria digest; Portugal's CNCTI recommendation).

## Pipeline fixes
* `scripts/build_oxford_panel.py` (new): rebuilds the Oxford tidy panel from raw workbooks;
  fixes the dropped "United Republic of Tanzania"; reproduces all 624 v1 rows exactly.
* `analyze_sensitivity_v2.py` (new): primary vs no-South-Africa; leave-one-out; AU convergence without SA.
* `outputs/rhetoric_vs_readiness/guard_leave_one_out.csv` regenerated (v1 file was a stale
  Morocco-inclusive run). Figure3 / FigureS1 copies refreshed.

## Headline numbers, v1 -> v2
| | v1 (12+AU) | v2 primary (15+AU) | v2 without South Africa |
|---|---|---|---|
| Readiness comparison | 11 countries, 99 cells | 15 countries, 135 cells | 14 countries, 126 cells |
| Mean of 9 per-dimension r | -0.005 | -0.098 | -0.143 |
| Text-proximate mean r | +0.164 | +0.067 | +0.002 |
| Independent mean r | -0.054 | -0.145 | -0.185 |
| Separation | +0.218 | +0.211 | +0.187 |
| Exact permutation p | 0.083 (3/36) | 0.056 (2/36) | 0.167 (6/36) |
| LOO removals reaching p<=0.05 | 0 (v3.0 Table S3 wrongly showed 8) | 3 (Nigeria, Tanzania, Zambia) | 0 |
| Alignment vs operationalization, Spearman rho | -0.218 (n=12) | -0.248 (n=15, p=0.374) | — |
| Most AU-convergent | Rwanda +0.590 | Ethiopia +0.629, Rwanda +0.517 | Ethiopia +0.658, Rwanda +0.519 |

Manuscript implications: readiness result remains a non-significant, exploratory pattern;
Vision and Governance & Ethics both weaken (Gov & Ethics +0.199 -> +0.022), and the
independent dimensions become more negative (Infrastructure -0.384). Rwanda is no longer the
most AU-convergent strategy. The AU anchor now sits below the national mean on all 9 domains (C9 essentially at the mean, -0.01)
(C5 -0.79; largest gaps C4 -1.38, C1 -1.13), so any "AU standards/interoperability gap"
wording must be re-derived. Tanzania's 2024 Oxford Vision score is 0.0.

## Figure 2 (alignment x operationalization)
* `plot_figure2.py` layout fixed: y-axis padded beyond 0-1 (Zambia 6/6 and Senegal/Mauritius 0/6 were clipped), ticks as k/6 levers, label collision avoidance, quadrant labels pinned to corners.
* Breadth is a within-sample index (levers above the corpus median), so adding countries moved existing scores: Senegal 1/6 -> 0/6, Mauritius 1/6 -> 0/6 (new text), Zimbabwe 4/6 -> 5/6, Nigeria 3/6 -> 4/6, Egypt 3/6 -> 2/6, Ghana 2/6 -> 5/6 (new text); Benin unchanged at 4/6. v3.0 values (Rwanda & Zimbabwe 0.833; Mauritius & Senegal 0.167; Tanzania 0.667) must be updated: Zambia 1.000 now leads.
* With n = 15 the medians fall on data points: Ghana sits on the alignment median, South Africa on the breadth median.

## Oxford 2025 temporal-alignment sensitivity (added 2026-10-14)
* AAGI was assessed and rejected as a comparator: its six pillar scores are computed client-side from the tracker's own policy metadata (e.g. +70 for status "published"; +80 if the note contains "implemented"), so they are strategy-derived, not independent readiness.
* New: `data/oxford_readiness_indices/oxford_dimensions_2025_dims14_embed.csv` (14 dimension definitions), `outputs/reference_alignment/oxford_2025_dims14/`, `analyze_oxford2025_sensitivity.py` -> `outputs/sensitivity/oxford2025/`.
* Guard (pre-specified from the 2025 Methodology Report): strict = Policy vision + Policy commitment; broad adds Governance principles, Government digital policy, Human capital, Safety and security.
* Result: the guard pattern does not replicate. All 15: strict separation -0.058 (p = 0.670, 61/91); broad +0.026 (p = 0.452). Excl. South Africa and strategy-predates-index (11) similar (p 0.42-0.68). No leave-one-out removal reaches p <= 0.05 (min 0.571).
* Largest single association: Data quality r = -0.671 (p = 0.006, BH q = 0.087; excl. SA r = -0.781, q = 0.014) — same direction as 2024 Infrastructure / Data Availability (compensatory emphasis); exploratory.
* Operationalization breadth does not track Oxford 2025 Policy commitment (Spearman rho = -0.197, p = 0.482, n = 15; -0.075 for the 11 pre-index strategies).
* Tables S6 and S7 added to `drafts/Paper1_tables_corpus_v2_2026-10-14.docx`.

## Corpus v2.1 — Lesotho added under draft rule A (2026-10-16)
* Rule: officially published draft/consultation versions are eligible and flagged. Lesotho's AI Policy and Implementation Plan (Second Draft, gov.ls, 2025) added; config + extraction; 16 national + AU.
* Full chain rerun (log: `_verify/corpus_v2_1_lesotho_regeneration_2026-10-16.log`, 15/15 steps exit 0). New no-drafts sensitivity (excl. South Africa, Tanzania, Lesotho) in `analyze_sensitivity_v2.py` and `analyze_oxford2025_sensitivity.py`; BH q now computed inside the Oxford 2025 script.
* Headline: readiness permutation p 0.056 -> 0.167; no LOO variant reaches 0.05; no-drafts p = 0.111. Full number list: `outputs/Paper1_number_changes_with_Lesotho_2026-10-16.md`.

Still to do: corpus_metadata.csv rows for the new entries; v3.0 text/tables; official-domain copy of Ghana 2025-2035.
