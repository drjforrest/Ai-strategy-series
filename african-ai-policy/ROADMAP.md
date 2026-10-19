# Research programme roadmap — African AI strategies (3-paper series)

**Owner:** Dr. Jamie Forrest · **Status:** active · **Last updated:** 30 Sep 2026
**Authoritative data:** the repository (`outputs/`, `data/`), not the manuscript `.docx`.
This roadmap is the canonical plan; the manuscript and posters must be reconciled to it.

---

## The three papers

| | Question | Corpus | Framework / method | Comparator | Target | Status |
|---|---|---|---|---|---|---|
| **Paper 1** | Does national AI-strategy rhetoric correspond to independently measured AI readiness? | 12 national AI strategies + AU anchor | WHO nine digital-health core components (as the *rhetoric measurement grammar*) + multilingual sentence embeddings; circularity guard | Oxford Insights Government AI Readiness Index | BMJ Global Health | Draft abstract + repo analysis; **needs reconciliation** |
| **Paper 2** | Do AI strategies and digital-health strategies distribute implementation competencies and institutional linkage differently? | Group 1: 12 national AI strategies. Group 2: **15 digital-health strategies** (Rwanda, Namibia, Mauritius, Burundi, Botswana, Ethiopia, Ghana, Kenya, Niger, Senegal, DRC, Nigeria, Sierra Leone, South Africa, Zambia) | Genre/vocabulary contrast; operationalization levers; **document linkage** (regex/dictionary) | AI set vs digital-health set vs AU vision | HIMSS27 (poster; **no figure permitted**) → journal | Extended abstract drafted; connectivity + linkage built; **Group 2 = 14** |
| **Paper 3** | What competencies, educational pathways and accreditation capacity are needed for responsible AI in African health systems? | New primary data: program/curriculum extraction sheet (Digital Health & Health Informatics programs at African institutions) | Capacity/professionalisation analysis; mapping to competency frameworks | (none — new unit of analysis) | To be set | Scoping; depends on Paper 1 + 2 |

---

## Paper 1 — Rhetoric and readiness in national AI strategies

**Purpose.** Whether strategic emphasis in African national AI strategies corresponds to
independently measured national AI readiness.

**Design.** WHO digital-health competencies provide the backbone for "rhetoric"; the Oxford
Insights Government AI Readiness Index provides the external "readiness" comparator. A
circularity guard separates Oxford dimensions partly built from policy text from those built
on independent data.

**Contribution (as intended in the series plan).** The rhetoric–readiness matrix: text
aligns more clearly with readiness dimensions proximate to policy text than with independently
measured capability.

**Corpus (repo-authoritative).** **12 national AI strategies** (Benin, Côte d'Ivoire, Egypt,
Ghana, Kenya, Mauritius, Nigeria, Rwanda, Senegal, South Africa, Tanzania, Zimbabwe) +
the African Union Continental AI Strategy = **13 entries**. French-language entries included
(Senegal, Côte d'Ivoire).

**Exclusions (documented):** Ethiopia — digital-transformation genre, AI incidental
(1.87/1k). Morocco — no publicly available full-text national AI strategy (referenced in
official documents only; only a conference-synthesis report exists). Algeria, Namibia, Tunisia —
no qualifying strategy text published as of the cut-off. Uganda — broad digital-transformation
roadmap, not an AI strategy.

---

## Paper 2 — AI strategies versus digital-health strategies

**Purpose.** How national AI strategies and national digital-health strategies differ in
attention to the policy and implementation foundations for responsible AI in health —
foregrounding health-system execution, interoperability, governance, monitoring, workforce,
financing and implementation responsibility. This framing is the better HIMSS fit.

**Design.** Do not reuse the Oxford rhetoric–readiness matrix as the central outcome. Compare
policy genres: whether AI-specific and health-sector strategies distribute critical
implementation competencies differently, with emphasis on institutional linkage,
interoperability, regulation, workforce, financing, timelines, monitoring and implementation
responsibility.

**Corpus.** Group 1 = 12 national AI strategies. Group 2 = **15 digital-health strategies** (Rwanda, Namibia, Mauritius, Burundi, Botswana, Ethiopia, Ghana, Kenya, Niger, Senegal, DRC, Nigeria, Sierra Leone, South Africa, Zambia). Off-set contrast: Uganda's *Digital Transformation Roadmap* (`digital_transformation`). Note: South Africa's PDF is misnamed `national-digital-strategy...` but is the *National Digital Health Strategy for South Africa 2019-2024* — it is in the DH set.

**Canonical Paper-2 numbers (expanded set, 1 Oct 2026):**
- AI centrality: AI strategies 19.3–46.9/1k (median 35.5); digital-health 0.00–1.11/1k (median 0.16) — **no overlap**.
- WHO-domain alignment: digital-health leads on all nine domains; the **C5 standards/interoperability gap has narrowed** (DH 0.584 vs AI 0.461); C2 investment and C8 legislation/ethics leads are marginal.
- Document linkage: **7 of 12** AI-strategy countries (58% — Ghana, Kenya, Mauritius, Nigeria, Rwanda, Senegal, South Africa) have a matched health strategy; cross-referencing remains **near-zero**; shared-actor Jaccard weak (0.00–0.25).

**Data flags:** Ethiopia DH has a doubled-character PDF extraction artefact in headers; Nigeria DH is an *architecture* not a strategy; Uganda is digital-transformation not digital-health.

**Built so far (repo).** `build_dh_corpus.py` (extract + inventory) → `analyze_connectivity.py` — (i) AI centrality, (ii) WHO-domain overlap; `analyze_linkage.py` — (iii) document linkage. Figures: none permitted at HIMSS.

---

## Paper 3 — Workforce, competencies, and professional capacity

**Purpose.** Shift from document comparison to human and institutional capacity: the
competencies, educational pathways, professionalisation mechanisms and accreditation-relevant
capacities needed for responsible AI implementation in African health systems.

**Rationale.** Aligns with the broader programme on AI-ready health-informatics education,
professional recognition and regional quality assurance. Papers 1–2 are the upstream
policy-analysis foundation.

**Contribution.** How competencies required for responsible AI in health appear across
health-informatics, digital-health, public-health informatics and related training pathways,
and where regional bodies (e.g. HELINA) may build capacity and standards.

---

## Recommended sequence

1. **Paper 1 first** — the flagship, closest to journal-ready.
2. **Paper 2** — the HIMSS submission, distinct comparative question, health-informatics framing.
3. **Paper 3** — once Papers 1–2 have established the policy landscape.

---

## Critical review — challenges to resolve (added by the research assistant)

These are points where the plan as written is vulnerable; none blocks the plan, but each
should be decided before the relevant paper is finalised.

1. **Paper 1 corpus is 12, not 14.** The draft roadmap says "14 country-level AI policy or
   strategy entries + AU". The repo now excludes both Ethiopia (genre) and Morocco (no
   public full text), giving **12 national + AU = 13 entries**. Fix everywhere.

1b. **CANONICAL PAPER-1 NUMBERS (regenerated from the 12+AU corpus, 30 Sep 2026).** These
   supersede every earlier figure:
   - Primary alignment: 13 entries × 9 domains = 117 rows (`outputs/alignment_scores.csv`).
   - Rhetoric–readiness: **11 countries / 99 cells; pooled r = −0.005; independent-dimension
     mean r = −0.054; text-proximate mean r = +0.164; separation +0.218; exact permutation
     p = 0.083 (3 of 36) — NOT significant at 0.05.**
   - Note: one *independent* dimension (Maturity, Technology Sector) shows r = +0.301, the
     strongest single correlation in the set.
   - **Consequence:** removing Morocco (a correct genre-compliance decision) moved the
     permutation p from 0.028 → 0.083, i.e. across the significance threshold. The
     rhetoric–readiness result is a **null with a non-significant directional hint**, and must
     be presented as exploratory. This materially strengthens challenge #2 below.
   - **Regeneration gotcha:** `analyze_rhetoric_vs_readiness.py` reads the **Oxford-dimension**
     alignment, produced by `run_reference_alignment.py` — NOT the WHO alignment. Re-running
     `run_pipeline.py` alone leaves it stale. Full regeneration order:
     `run_pipeline.py` → `run_operationalization.py` → `run_reference_alignment.py` →
     `analyze_rhetoric_vs_readiness.py` → `analyze_convergence_tables.py` →
     `analyze_connectivity.py` → `analyze_linkage.py` → `verify_corpus.py`.

2. **Paper 1's "signature result" is its weakest evidence.** The rhetoric–readiness contrast
   rests on an exact permutation p at the *floor* of the test (1/36 = 0.028), and
   leave-one-country-out drops significance for Nigeria, Morocco, Côte d'Ivoire and South
   Africa. Elevating this as the headline invites a reviewer to knock down the paper's
   flagship claim. **Recommendation:** make the signature contribution the *instrument +
   alignment/operationalization construct separation + the AU standards/interoperability gap*,
   and present readiness as explicitly exploratory.

3. **"Near journal-ready" understates the reconciliation debt.** Three versions currently
   disagree: the manuscript `.docx` (15 entries; pooled r = −0.041; convergence Rwanda 0.638),
   the repo outputs (13+AU; different convergence values), and the figures (11 countries; 99
   cells; pooled r = +0.02; Figure 3 still contains an Ethiopia row). **One spec must be
   fixed and every table, figure and number regenerated from `outputs/` before submission.**

4. **Paper 2 should run the operationalization index on Group 2.** The plan asks Paper 2 to
   compare "timelines, monitoring, implementation responsibility" — i.e. the six
   operationalization levers — but those are currently computed **only** for the AI-strategy
   set (`outputs/operationalization/`). Extend to the digital-health set or the comparison
   cannot be made.

5. **Paper 2's Group 2 is thin (n = 3).** Either expand the digital-health corpus (the
   census-search tooling exists), or frame the comparison explicitly as descriptive/pilot and
   say so. Keep the n small-sample caveat visible.

6. **Papers 1 and 2 share the AI-strategy corpus.** State this explicitly to pre-empt
   salami-slicing concerns. The distinctness is the *question*, the *second corpus*, and the
   *linkage method* — not the documents.

7. **Paper 3 needs a defined method and sampling frame, not just a topic.** Specify: the
   program/curriculum scan (the extraction sheet), the sampling frame (which countries,
   institutions, program types), the coding scheme (mapped to which competency framework:
   WHO? AMIA? national?), and the unit of analysis. Without these it risks reading as a
   position piece.

8. **Paper 3 premise correction.** Document-text analysis does **not** show workforce is the
   weakest digital-health domain (C7 sits mid-pack at 0.572); the weak digital-health domains
   are legislation/ethics (C8, 0.475) and investment (C2, 0.504). Workforce *is* the weakest
   **AI-strategy** domain (0.428). Let the extraction sheet produce the workforce/accreditation
   finding rather than inheriting it.

9. **Sequence risk.** Submitting Paper 1 first is sound *only if* it leads on the instrument.
   If it leads on the fragile rhetoric–readiness result, the series front-loads its weakest leg.

10. **Citation placeholders.** `[cite:1]`/`[cite:40]` markers are tool artefacts; replace with
    real references.

11. **Figure grammar discipline (series-wide).** Paper 1 figures follow the reframing (the
    readiness scatter moves to supplementary; the alignment × operationalization scatter takes
    a main slot). Paper 2 uses *different* grammars (dot plot, slope/dumbbell, binary grid) so
    the two papers do not look like one study sliced. A study-architecture alluvial is the one
    legitimate Sankey.

12. **Figures regenerated from the canonical corpus (30 Sep 2026).** Producer scripts and
    outputs in `outputs/figures_for_manuscript/`:
    - `Figure1.png` — within-competency z heatmap, 12 national + AU anchor (`plot_figure1.py`).
    - `Figure2.png` — **alignment × operationalization scatter** (the robust construct-separation
      finding), taking the main slot previously held by the readiness scatter (`plot_figure2.py`).
    - `Figure3.png` — AU emphasis-gap heatmap, Ethiopia/Morocco removed (`analyze_au_convergence.py`).
    - `FigureS1_rhetoric_readiness.png` — the exploratory rhetoric–readiness quadrant, demoted
      to supplementary (`analyze_rhetoric_vs_readiness.py` → `quadrant.png`).
    All confirmed free of the excluded Ethiopia and Morocco rows. Regenerate with the analysis scripts.

---

## Artefact map (repo)

| Artefact | Path |
|---|---|
| Primary alignment (AI strategies × WHO) | `outputs/alignment_scores.csv` |
| Digital-health corpus inventory | `outputs/dh_corpus_inventory.csv` (`build_dh_corpus.py`) |
| Operationalization levers | `outputs/operationalization/operationalization_index.csv` |
| Rhetoric vs readiness | `outputs/rhetoric_vs_readiness/` |
| AU convergence + sensitivity | `outputs/au_convergence/` |
| Paper 2 connectivity (density, overlap) | `outputs/connectivity/` (`analyze_connectivity.py`) |
| Paper 2 document linkage | `outputs/connectivity/` (`analyze_linkage.py`) |
| DTS vs AU comparator | `_verify/dts_scores.csv` |
| Corpus metadata / collection audit | `data/corpus_metadata.csv` |
| Drafts | `drafts/` |

**Run everything with the shim:** `./run.sh <script>` (venv = uv spawn of pyenv 3.12.0;
never the bare `python3`, which lacks sentence-transformers and silently degrades to TF-IDF).
