# Paper 3 — Protocol v0.1

**Working title:** *Training the workforce that AI strategy assumes: a continental mapping of health-informatics and digital-health programmes in Africa, and their coverage of responsible-AI competencies*

**Owner:** Dr. Jamie Forrest · **Date:** 5 Oct 2026 · **Status:** protocol for review (no data collected yet)
**Position in series:** Paper 3 is the human-capacity leg. Papers 1–2 map *policy* (AI strategies; digital-health strategies) and find that standards, interoperability and workforce are the under-specified competencies. Paper 3 tests whether the *training system* supplies the competencies those policies assume — and, specifically, the competencies responsible AI in health requires.

---

## 1. The gap this paper fills (and what it must NOT repeat)

**Closest prior art — must be differentiated, not duplicated.** Were et al. (2021, *JAMIA* 28(9):1843–1848) compared competency coverage across **7 accredited MSc health-informatics programmes in the East African Community**, coding curricula against a **73-competency template (40 IMIA-recommended + 8 optional + 25 unique)**; two reviewers reached Cohen's κ = 0.738; coverage ranged from 32 to 49 of 73 competencies and only 4 of 21 institution-pairs exceeded 70% similarity. Were et al. (2022, Stud Health Technol Inform) proposed harmonized benchmarks from the same work. **This is the template for the method — and the bar Paper 3 must clear.**

Paper 3 is *not* a re-run of Were et al. Its three differentiators:
1. **Continental scope, not East Africa.** Extend to all African regions and to the full credential range (BSc, MSc, MPH, PGDip, certificate), not just accredited MSc programmes.
2. **The responsible-AI overlay (the novel contribution).** The IMIA/AMIA templates predate the generative-AI era. Paper 3 adds a purpose-built competency set for **responsible AI in health** (see §4) and measures its coverage — directly answering the gap Papers 1–2 surfaced.
3. **The policy–capacity linkage.** Join programme coverage to the Paper 1–2 policy corpus: for each country, does the existence of a national AI strategy and a digital-health strategy correspond to actual training capacity? A country can legislate AI and train nobody. This is the paper's headline claim candidate.

**Premise correction (carried from the architecture review).** Do **not** pre-commit to "workforce is the weak one." In the document analysis, workforce (C7) is the weakest *AI-strategy* domain (0.428) but sits mid-pack in the *digital-health* set (0.578). Paper 3 must let the curriculum data decide.

---

## 2. Research questions

- **RQ1 (landscape).** What health-informatics / digital-health / health-data-science programmes exist across African higher-education institutions — how many, where, at which credential levels, hosted in which academic units, in which languages?
- **RQ2 (coverage).** How comprehensively do these programmes cover (a) the foundational health-informatics competency domains and (b) the responsible-AI-in-health competency set?
- **RQ3 (variability).** How much do competency coverage and programme structure vary across institutions, regions and host-unit type?
- **RQ4 (linkage — headline).** Is national training capacity associated with the presence of national AI and digital-health strategies? Which countries have policy ambition without corresponding training capacity (or the reverse)?
- **RQ5 (professionalisation).** How do the programmes connect to professionalisation and accreditation mechanisms (HELINA, IFHIMA member associations, national statutory boards, CAHIIM/HIMSS presence)?

---

## 3. Sampling frame and unit of analysis

**Unit of analysis:** the **programme** (a credentialed course of study), nested within institution → country → AU region.

**Design:** cross-sectional desktop curriculum review (document analysis of publicly available programme structures and course catalogues), with an optional confirmatory survey of programme directors in a second phase.

**Inclusion criteria (all must hold):**
- Offered by a higher-education institution based in an African Union member state (or an African-serving institution with a substantial in-region campus), *and*
- Leads to a credential: BSc, MSc, MPH, PGDip, or a structured certificate (≥ ~60 hours), *and*
- The programme title **or** its core curriculum centres health informatics, digital health, eHealth, biomedical informatics, health information management, or health data science.

**Exclusion criteria:**
- General computer-science, IT or public-health programmes without an informatics core;
- Standalone short workshops / single modules with no credential;
- Programmes that have ceased intake before the census date.

**Discovery sources (recorded per programme for reproducibility):**
1. Inter-University Council for East Africa (IUCEA) register of accredited programmes;
2. National higher-education regulator registers (e.g. Kenya's CUE, South Africa's CHE, Nigeria's NUC, Rwanda's HEC);
3. HELINA (Pan African Health Informatics Association) membership and education listings;
4. The Digital Health Skills for Africa (dhsafrica.org) programme list — a useful seed, not an authority;
5. Targeted web/scholar search (multilingual: English, French, Portuguese, Arabic);
6. Snowballing from programme and faculty pages;
7. AMIA / IMIA education-network and Africa CDC workforce-development documents.

---

## 4. Coding scheme

**Two-layer competency template.**

**Layer A — foundational health-informatics domains (baseline).** Use the **IMIA recommendations on education in biomedical and health informatics** (second revision, 2023) as the primary template, because it is (i) international rather than US-centric, (ii) explicitly education-oriented, and (iii) the same family Were et al. used — enabling direct comparison with the East African precedent. Use the **AMIA 2017 ten foundational domains** (Valenta et al., *JAMIA* 2018;25(12):1657–1668) as a cross-walk / sensitivity check, since AMIA's domains are the accreditation gold standard and map cleanly onto IMIA.

**Layer B — responsible-AI-in-health overlay (the novel contribution).** A purpose-built set derived from Papers 1–2 and the AI-governance literature. Provisional domains:
- B1. Data ethics, privacy and data-protection law (incl. African frameworks)
- B2. Algorithmic bias, fairness and equity in clinical/population AI
- B3. AI governance, accountability and human-rights-based regulation
- B4. Clinical validation, evaluation and post-deployment monitoring of AI tools
- B5. Human factors, clinician–AI interaction and safety
- B6. Interoperability and data standards as AI prerequisites (links to Paper 1's AU standards gap)
- B7. Health-data science/ML methods (foundational technical literacy)
- B8. AI procurement, economics and sustainability in low-resource systems

Every Layer-B domain is traceable to an empirical finding in Papers 1–2 — so the overlay is not invented but *derived*, which is itself a contribution.

**Extraction variables (per programme):** institution; country; AU region; programme name as stated; credential and level; host college/department; duration and credits; delivery mode (face-to-face/online/blended); language(s); core course list; stated competencies; accreditation body and status; whether AI/ML topics appear and where; tuition (if public).

**Coding procedure.** Two coders independently map each course/competency statement to the template. Report **Cohen's κ** for inter-rater agreement; adjudicate disagreements by consensus with a third reviewer. Target κ ≥ 0.70 (Were et al. achieved 0.738).

---

## 5. Analysis plan

**RQ1 (landscape):** descriptive — counts by country, region, credential, host-unit type; a continental map figure (Figure 1); a programme-inventory table (Table 1).

**RQ2 (coverage):** per-programme **coverage proportion** = (# competency statements matched to template domain) / (template size), for Layer A and Layer B separately. Report distribution (median, IQR, range) and a coverage heatmap (programmes × domains).

**RQ3 (variability):** **Jaccard similarity** between programme competency sets, as in Were et al., to quantify pairwise overlap; test whether coverage differs by region, credential level and host-unit type (Kruskal–Wallis; report effect sizes, not just p, given small n).

**RQ4 (linkage — headline):** build a country-level table joining (a) Paper 1 presence of a national AI strategy, (b) Paper 2 presence of a matched digital-health strategy, and (c) number of programmes per capita / per national health workforce. Test the association (Spearman; descriptive if n is small). Produce a **policy–capacity quadrant figure** (Figure 2): countries high on policy ambition × low on training capacity are the actionable finding.

**RQ5 (professionalisation):** qualitative mapping of programmes to accreditation/professional bodies; narrative synthesis with the HELINA/IFHIMA/Kenya-board landscape from Paper 1.

**Reporting standard:** use **GRADE-CERQual** language only if a qualitative synthesis is included; otherwise report as a structured descriptive census with explicit coverage uncertainty. State clearly that curriculum *documents* show *intended* coverage, not delivered competence — the same tool-versus-truth caveat that governs Papers 1–2.

---

## 6. Risks, limitations and mitigations

| Risk | Mitigation |
|---|---|
| **Duplication of Were et al.** | Explicit differentiation (§1): continental scope + Layer-B overlay + policy linkage. Cite Were et al. as the precedent and position Paper 3 as its continental, AI-era extension. |
| **Non-public curricula** | Multi-source discovery (§3); where only syllabus summaries are public, code at the course-title level and flag granularity; optional Phase-2 director survey. |
| **Language coverage** | Multilingual search (EN/FR/PT/AR); francophone and lusophone programmes must not be under-counted (a bias Papers 1–2 were careful to avoid). |
| **Definitional creep** ("informatics" means different things) | Pre-specified inclusion criteria; report included *and* excluded candidates with reasons. |
| **Small n / weak linkage power** | Present RQ4 as descriptive quadrants, not inferential; report cell sizes explicitly. |
| **Curriculum ≠ competence** | State as a first-order limitation; frame all coverage as *intended*. |
| **Currency** | Fixed census date; all programme data timestamped. |

---

## 7. Deliverables and decision gates

1. **Census sheet** (`data/paper3_programme_census.xlsx`) — one row per programme, all extraction variables, with source URLs and access dates.
2. **Coding matrix** — programme × Layer-A/Layer-B domain, with κ.
3. **Analysis outputs** (`outputs/paper3/`) — coverage distributions, Jaccard matrix, policy–capacity join.
4. **Manuscript** — target journal to be decided *after* results (candidates: *JAMIA Open*, *BMJ Global Health*, *Health Policy and Planning*, or *Applied Clinical Informatics*), since the framing depends on whether the headline is the policy–capacity gap or the responsible-AI coverage gap.

**Decision gates for Dr. Forrest:**
- **G1.** Confirm the two-layer template (IMIA + derived responsible-AI overlay) vs a single framework. *Recommendation: two-layer — the overlay is the novelty.*
- **G2.** Confirm continental scope vs a defensible region (e.g. EAC + SADC) if time is constrained.
- **G3.** Decide whether Phase-2 programme-director survey is in scope (adds rigour, adds cost/time/ethics).
- **G4.** Confirm the sampling frame is a *census of public information* (no ethics approval needed) rather than human-subjects research.

---

## 8. Immediate next actions

1. [ ] Ratify G1–G4.
2. [ ] Draft the Layer-B competency statements as *reviewable artefacts* (mirroring the Table 1b approach in Paper 1) — the item the paper stands or falls on.
3. [ ] Build the empty census sheet and seed it with the ~12 programmes already surfacing in the literature (Makerere, Dar es Salaam, Moi, Kenyatta, Muhimbili, Gondar, Mekelle, Bahir Dar, Rwanda, KwaZulu-Natal, Western Cape, Nairobi, Strathmore, Njala, ESMT).
4. [ ] Pilot coding on 3 programmes to calibrate the template and κ before full extraction.
5. [ ] Only then: full census → analysis → framing decision.

---

## References (to verify at drafting)

- Were MC, Gong W, Balirwa P, et al. Comparative analysis of competency coverage within accredited master's in health informatics programs in the East African region. *J Am Med Inform Assoc.* 2021;28(9):1843–1848. doi:10.1093/jamia/ocab075
- Valenta AL, Berner ES, Boren SA, et al. AMIA Board White Paper: AMIA 2017 core competencies for applied health informatics education at the master's degree level. *J Am Med Inform Assoc.* 2018;25(12):1657–1668. doi:10.1093/jamia/ocy132
- IMIA. Recommendations of the International Medical Informatics Association on Education in Biomedical and Health Informatics (Second Revision). 2023.
- Were MC et al. Developing Harmonized Benchmarks for the Master of Science in Health Informatics for the East African Region. *Stud Health Technol Inform.* 2022. doi:10.3233/SHTI220211
- Olufadewa II, et al. National eHealth strategy frameworks in Africa. *Oxford Open Digital Health.* 2024;oqae047.
- Papers 1–2 (this series) — for the policy corpus and the C7/C5 findings feeding the Layer-B derivation.

*Note: [cite:n] placeholders from earlier tool output must be replaced with the above before drafting.*
