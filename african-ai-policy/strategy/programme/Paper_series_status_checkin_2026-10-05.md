# 3-paper series — status check-in

**Prepared:** 5 Oct 2026 · **Owner:** Dr. Jamie Forrest
**Method:** every claim below was read from the repository (`outputs/`, `data/`, `drafts/`) on this date. Where a number in a roadmap or draft disagrees with the pipeline output, the output wins and the disagreement is listed as drift.

**Clock:** HIMSS27 abstract due **11 Oct 2026** — 6 days out.

---

## Headline

| Paper | Analysis | Draft | Submission-ready? | Gating item |
|---|---|---|---|---|
| **1 — Rhetoric & readiness** | ✅ done + canonical (repo) | ✅ **full manuscript exists — v1.3, 29 Sep** — but built on the superseded 15-entry corpus | **No** | Port the v1.3 manuscript onto the 12+AU corpus and invert the framing (see below) |
| **2 — AI vs digital-health (HIMSS)** | ✅ done, reproducible | ✅ *poster_proposal* is the chosen file (numbers correct) | **Nearly** | Sweep the stale "14 / 50%" out of `ROADMAP.md`; verify HIMSS portal limits; finalise authors |
| **3 — Workforce & education** | ❌ not started here | ❌ none | **No** | Define protocol, then build the program/curriculum extraction sheet |

The good news: **Papers 1 and 2 are analytically complete and reproducible.** The remaining work is reconciliation, framing and packaging — not new analysis. Paper 3 is genuinely unstarted in this workspace.

---

## Paper 1 — Rhetoric and readiness (BMJ Global Health)

**Verified present**
- `outputs/alignment_scores.csv` — primary matrix, 13 entries × 9 domains = 117 rows.
- `outputs/operationalization/operationalization_index.csv` — 13 entries, six execution levers.
- `outputs/rhetoric_vs_readiness/per_dimension_correlation.csv` — 9 dimensions.
- `outputs/au_convergence/` — AU convergence + sensitivity.
- `outputs/figures_for_manuscript/` — `Figure1.png` (z heatmap), `Figure2.png` (alignment × operationalization scatter), `Figure3.png` (AU gap heatmap, Ethiopia/Morocco removed), `FigureS1_rhetoric_readiness.png` (demoted to supplement). All four exist.

**Canonical numbers (confirmed against outputs, 30 Sep run)**
- Corpus = **13 entries (12 national + AU)**, French included.
- Rhetoric–readiness: **11 countries / 99 cells**; pooled **r = −0.005**; text-proximate mean **r = +0.164** (Vision +0.130, Governance & Ethics +0.199); independent-dimension mean **r = −0.054**; separation **+0.218**; exact permutation **p = 0.083 (n.s.)**.
  - I re-derived these from `per_dimension_correlation.csv` — they reconcile exactly. One independent dimension (**Maturity, r = +0.301**) is the single strongest correlation, which is awkward for the "text tracks only text-proximate dimensions" story and must be addressed in the text, not hidden.
- Operationalization breadth: Rwanda & Zimbabwe 0.833, Tanzania 0.667; Mauritius & Senegal 0.167.
- External validity (not yet in the abstract): Olufadewa cross-check **Spearman ρ = −0.535 (p = 0.059)** — our alignment measure does *not* track expert-rated comprehensiveness. This is a strong, pre-emptive defence and belongs in Discussion/Limitations.

**The manuscript (located 5 Oct — supplied by the author)**
- `African_AI_strategies_BMJGH_main_manuscript_v1.3-29sept2026.docx` — a **complete** BMJ GH submission draft: structured abstract, Introduction, Methods, Results, Discussion, Strengths/Limitations, Declarations (Contributors/Funding/COI/Data availability), 33 numbered references, Table 1(a/b), Table 2, Figures 1–3, and Supplementary Tables S1–S3. Data-availability statement points to `github.com/drjforrest/african-ai-strategies` (a GitHub repo outside this working folder — a second place the canonical file may live).
- **It is already the sensible study** — but it is built on the **superseded 15-entry corpus** (14 national incl. Ethiopia *and* Morocco, + AU). Its headline numbers are the *pre-exclusion* ones: pooled **r = −0.041**, text-proximate mean **+0.208**, independent mean **−0.113**, permutation **p = 0.028 (108 cells / 12 countries)**.
- Useful: the script already concedes the fragility in its own words — *"the full-set result sits at the floor of the test… should be read as a directional pattern rather than a precise effect"* — and S3 already carries the leave-one-out table (4 of 12 removals push p > 0.05) plus the Morocco-exclusion sensitivity (p = 0.083).

**Drift / stale artefacts**
1. `_verify/himss_abstract.md` is a **stale leftover** of the same 15-entry run (pooled r = −0.041, p = 0.028, 108 cells). It also contains a CAHIIM/HIMSS-chapters sentence that belongs to **Paper 3**, not Paper 1. Retire or annotate it.
2. **The framing must be inverted, not just the numbers.** The repo's canonical decision (30 Sep) excludes **Morocco** on genre grounds (no public full text) → **12 national + AU = 13 entries** → p = **0.083 (n.s.)**. The v1.3 manuscript does the reverse: it treats 15 entries as primary (p = 0.028) and Morocco-exclusion as a *sensitivity*. Reconciliation therefore means promoting the genre-clean corpus to primary and demoting the readiness comparison from a headline result to an **explicitly exploratory** one — the position the reconceptualised abstract already takes.
3. **Reviewer risk to pre-empt:** a corpus edit that moves p across 0.05 looks post hoc unless narrated carefully. Report **both** corpora openly (primary = 12+AU; sensitivity = with Morocco), state the exclusion is genre-based *a priori*, and lead with the instrument. Do not let the null read as a failure — it is the correct, honest result.

**Remaining tasks to submission-ready**
1. **Port v1.3 onto the 12+AU run** (edit, do not re-derive): Table 1 drop Ethiopia + Morocco rows (15→13); Table 2 keep but re-state the primary; S1 convergence 14→12; S3 LOO 12→11; Figures 1/2/3 regenerate (Fig 2 108→99 cells); abstract & Results swap to pooled r = −0.005 / text-proximate +0.164 / independent −0.054 / p = 0.083, labelled exploratory.
2. Regenerate per the order in `ROADMAP.md`; remember `analyze_rhetoric_vs_readiness.py` reads the **Oxford** alignment from `run_reference_alignment.py`, not the WHO matrix — a token `run_pipeline.py` leaves it stale.
3. Re-frame: **lead with the instrument** (alignment vs operationalization construct separation) and the **AU standards/interoperability gap**; keep readiness explicitly **exploratory**. Do not headline a p = 0.083 null.
4. Add the external-validity paragraph (Olufadewa ρ = −0.535) and handle the Maturity r = +0.301 outlier.
5. Replace all `[cite:n]` placeholders with real references.
6. ICMJE author list, COI/funding statement, data/code-availability statement, reporting checklist, word-limit and format compliance for BMJ Global Health.

---

## Paper 2 — AI vs digital-health strategies (HIMSS27 poster → journal)

**Chosen artefact:** `drafts/Paper2_HIMSS_poster_proposal.md` (locked in on 4 Oct) — exact HIMSS fields, provided author block, Olufadewa cited in Background, overlap-disclosure in Funding.

**Verified present and reproducible**
- Corpus on disk: **15 digital-health `.txt` files** (Rwanda, Namibia, Mauritius, Burundi, Botswana, Ethiopia, Ghana, Kenya, Niger, Senegal, DRC, Nigeria, Sierra Leone, South Africa, Zambia) + Uganda's Digital Transformation Roadmap in a separate genre.
- `outputs/connectivity/` — all four measures present: `ai_density_by_set.csv`, `alignment_by_domain.csv`, `linkage_coverage.csv`, `linkage_shared_actors.csv`, plus `linkage_by_document.csv`.
- Pipeline: `build_dh_corpus.py` → `analyze_connectivity.py` → `analyze_linkage.py`.

**Canonical Paper-2 numbers (confirmed against `outputs/connectivity/`)**
- **AI centrality:** AI strategies 19.29–46.86/1k (median ≈35.5); digital-health 0.00 (Burundi) –1.11/1k; Uganda 1.44. **No overlap** → hard genre boundary.
- **Competency overlap (identical WHO instrument, n = 15 DH):** DH leads on all nine domains; DH mean **0.602** vs AI **0.472**. Widest: governance C1 0.668/0.487, services C3 0.658/0.447. Near-parity: **C5 standards/interoperability 0.581/0.461** and C8 legislation/ethics 0.514/0.493, C2 investment 0.512/0.492.
- **Document linkage:** coverage **7 of 12 (58%)** — Ghana, Kenya, Mauritius, Nigeria, Rwanda, Senegal, South Africa. Shared-actor Jaccard 0.00 (Senegal) → 0.25 (Mauritius). Cross-referencing near-zero (DRC 3 refs, Senegal 1 ref, from the DH side; no AI strategy names its health counterpart).

**Drift — where the stale numbers live (corrected)**
The chosen file `poster_proposal.md` is **already consistent and correct**: Set B = **15** countries and linkage **7 of 12 (58%)**, matching `outputs/connectivity/`. The stale numbers sit in *other* artefacts and must be swept so nobody quotes them:
- **`ROADMAP.md` §Paper 2** still says Group 2 = **14** and linkage **6 of 12 (50%)** — fix to 15 / 7-of-12 / 58%.
- **`drafts/Paper2_HIMSS_poster_extended_abstract.md`** is an earlier draft that says Set B = 14 and **"6 of 12 (50%)"** — superseded; retire or annotate.
- **`drafts/Paper2_HIMSS_extended_abstract.md`** is correct (15 / 7-of-12 / 58%) but is the non-chosen variant — keep only as reference.
- **`_verify/himss_abstract.md`** is a Paper-1 artefact (15-entry old run), not Paper 2 — don't confuse the two "15"s.
Net: the file you'll submit is sound; the risk is a co-author or reviewer citing the roadmap. Fix the roadmap first.

**Open decisions on Paper 2**
1. **Kenya provenance — freeze it in print.** The Olufadewa census lists Kenya's artifact as the **2016 National eHealth Policy (2016–2030)**; but a `DHA_Strategic_Plan_2025_2028` PDF also sits in the DH folder. Roadmap and the draft's open items call Kenya's entry the *Digital Health Agency Strategic Plan 2025–2028*. Decide which document is scored, and cite it in Methods — a reviewer who cross-checks against Olufadewa will notice the mismatch.
2. **Nigeria type flag** — the NDHA is an *architecture*, not a strategy. Flag it or say so.
3. **Ethiopia extraction artefact** — `DDIIGGIITTAALL` doubled characters in headers; body usable.
4. **South Africa filename** is misnamed `national-digital-strategy-...` but is the *National Digital Health Strategy 2019–2024*.
5. **Stray/duplicate files:** Namibia appears twice; two Egypt PDFs in `national_strategies/`.
6. **HIMSS portal:** verify the character/word limit and whether the structured-proposal format (vs. free-text abstract) is accepted for this track — the 4 Oct decision to use the structured poster file should be confirmed against the current call.

**Remaining tasks to submission-ready (6 days)**
- [ ] Freeze the 15/58% numbers everywhere in the chosen file.
- [ ] Settle Kenya provenance + the four data flags in Limitations.
- [ ] Confirm HIMSS field/limit compliance and the poster-vs-paper disclosure line.
- [ ] Finalise the ICMJE author list (poster block currently: Forrest, Remera, Maloney, Nardone, Schoene, Nachega).
- [ ] How the two source genres redistribute across the nine domains (health: services/integration/people-centredness; AI: legislation/ethics) is *in the data* — state it as a finding, don't let it read as incidental.

---

## Paper 3 — Workforce, competencies and educational capacity

**Status: not started in this workspace.** No draft, no extraction sheet, no protocol file. `data/census_search_sheet_filled.xlsx` is the **document-census tracker** (55 AU members × 3 genres), *not* the program/curriculum sheet — a different instrument for a different paper.

**What exists to build on**
- The **premise is already corrected in-repo** (`Paper_series_architecture_review.md` §2): workforce is the weakest **AI-strategy** domain (C7 = 0.428), but in the digital-health set C7 sits mid-pack (0.578) and the weak domains are **C8 legislation/ethics (0.514)** and **C2 investment (0.512)**. So Paper 3 must *let the extraction sheet decide* which competency is weakest — do not pre-commit to "workforce is the weak one."
- A scattered Paper-3 germ sentence sits in the stale `_verify/himss_abstract.md`: CAHIIM accredits no African program; HIMSS chapters are US/Canada/India only; regional professionalisation is emerging via HELINA, IFHIMA member associations, and Kenya's Health Records & Information Managers Board. Useful — relocate it.

**Remaining tasks (must precede analysis)**
1. **Write the protocol (1 page):** sampling frame (countries, institution types, program levels), unit of analysis, coding scheme, and the **competency framework to map to** (WHO? AMIA? national?) — the roadmap's critical-review point #7. Without this it reads as a position piece.
2. **Choose the recruiting/eligibility rule:** desktop program scan vs survey vs both.
3. **Build the program/curriculum extraction sheet** (institutions, program name, level, curriculum fields, accreditation body, AI content flag).
4. **Then** the capacity/professionalisation analysis and the HELINA/regional-body framing.

---

## Cross-cutting (all three papers)

1. **Salami-slicing guard.** Papers 1 and 2 share the 12-country AI-strategy corpus. State the distinctness explicitly wherever both are cited: the *question*, the *second corpus (DH)*, and the *linkage method* differ — not the documents. Paper 2's chosen file already carries an overlap-disclosure line; keep it.
2. **Instrument reuse disclosure.** Both papers use the same nine WHO core components. Paper 2 introduces *no new framework* — say so plainly (architecture review §1).
3. **Figure grammar discipline.** Paper 1: heatmaps + alignment×operationalization scatter. Paper 2: dot/strip plot, slope/dumbbell, binary grid — deliberately different. The only legitimate Sankey is the study-architecture alluvial. (No figures permitted at HIMSS.)
4. **Environment trap (repeat of a past failure).** Run pipeline scripts with the project venv (`.venv/bin/python` / `./run.sh`), which has `sentence-transformers` (py 3.12). The active `python3` is 3.9 without it and **silently falls back to TF-IDF**, which is not comparable. `analyze_connectivity.py` hard-aborts on this; others may not.
5. **Roadmap hygiene.** Update `ROADMAP.md` to (a) fix Paper 2 Group 2 = **15** (not 14) and linkage **7/12 (58%)** (not 6/12 50%), (b) switch canonical regeneration order to the mnemonics 30 Sep, so the roadmap and outputs agree.

---

## Suggested next actions (ordered)

1. **Paper 2, today→tomorrow:** freeze 15/58% in `Paper2_HIMSS_poster_proposal.md`; settle Kenya provenance + limitations flags; verify HIMSS portal limits. This is the only 11 Oct hard deadline.
2. **Paper 1, this week in parallel:** locate the canonical manuscript outside this repo; then start reconciliation item 2 (numbers/tables/figures) and item 3 (reframe to lead with the instrument).
3. **Paper 3, after HIMSS:** write the protocol before touching data.
