# Health-informatics training partnerships in Africa: an integrated research strategy

*A proof-of-concept and interconnected-aims proposal, built on live public data
(NIH RePORTER, July 2026). Extends the fragmentation/equity questions of the
published AI-diagnostic-trials network paper into the domain of **training
capacity** — where researchers are made, and by whom.*

---

## The connecting idea

Your published paper asked whether AI-diagnostic **trials** in Africa form a
connected, equitable network — and found they don't. The natural upstream
question is: **where do the people who run those trials get trained, and does the
training system reproduce the same North–South dependency?** Training is the
supply side of the research ecosystem. If the training network is itself a
US-centered hub with a single dominant funder, then fragmentation and dependency
in the trial network are not accidents — they are inherited from how capacity is
built.

That reframing makes your two priority aims one project with two movements:

- **Aim A (the network).** Reconstruct the training-partnership network — who
  hosts programs, who partners with whom — and characterize its structure with
  the same SNA toolkit as the trials paper.
- **Aim B (the coverage bias).** Treat the *incompleteness of every data source*
  as a first-class finding: quantify what each funder-database can and cannot
  see, and show that a naïve single-source map manufactures the very dependency
  it claims to observe.

They interlock because **Aim B is the validity condition for Aim A**: you cannot
claim the network is US-centered until you've shown the finding isn't just an
artifact of using a US funder's database.

---

## Proof of concept (already built, this session)

**Source:** NIH RePORTER v2 API (live). **Scope:** training-mechanism grants
(D43, D71, K43, G11, U2R, T37, R25) whose title/abstract/terms mention
informatics, bioinformatics, data science, digital health, e/m-health.

**Extracted dataset (`training_programs.csv`, `partnership_edges.csv`):**

- **270 unique African-hosted** training programs + **354 unique US-hosted,
  Africa-focused** programs (deduplicated across fiscal years; all with abstracts).
- **517 host↔partner institutional edges**, extracted from abstract text by LLM.
- African-hosted programs concentrated in **Uganda (68), South Africa (63),
  Nigeria (34), Kenya (33)**, Ghana, Zimbabwe, Mali.

**Aim A finding (structure).** At country level the partnership network is a
**hub-and-spoke centered on the United States**, not a distributed mesh. The
heaviest ties are South Africa–US (49), Uganda–US (42), Kenya–US (38),
Nigeria–US (29), Ghana–US (19). South–South ties exist but are thinner and mostly *within-country*
(Uganda–Uganda, South Africa–South Africa) rather than cross-border African
collaboration. This mirrors the trials-paper fragmentation: African training nodes
connect *up* to the North far more than *across* to each other.

**Aim B finding (coverage bias).** **87% (235/270) of African-hosted training
grants in this dataset come from a single funder** — the Fogarty International
Center (FIC). This is the blind spot in one number: a map built only from NIH data
sees almost exclusively the Fogarty-funded slice, and therefore *cannot* see
Wellcome/DELTAS, Gates, EU/EDCTP, DAAD, or locally-funded programs. The apparent
US-centrality of Aim A is **partly real and partly an instrument effect** — and
separating the two is the research contribution.

---

## Data-source map (tested reachability, this environment)

| Source | Reachable | Sees | Blind to |
|---|---|---|---|
| **NIH RePORTER** | ✅ | US-federal-funded training (esp. Fogarty D43/K43) | All non-US funders; locally-funded programs |
| **CrossRef Funder Registry** | ✅ | Funder identity on any DOI-linked output | Grants without publications |
| **Gates Foundation grants** | ✅ (granted) | Gates-funded global-health training | Non-Gates philanthropy |
| **OpenAlex** | ✅ | Author training/affiliation trajectories | Formal curricula |
| **IATI datastore** | ⚠️ needs API key/path | Multi-donor aid (EU, FCDO, foundations) | — |
| **Wellcome / DELTAS** | ⛔ (data portal blocked) | Wellcome-funded African capacity programs | — |
| **University program directories** | manual/scrape | African-led degree programs | — |

**The triangulation principle:** no single source is unbiased, so the fair map is
the *union* of sources with each source's coverage explicitly modeled. That is
exactly what makes Aim B publishable rather than a limitations paragraph.

---

## Proposed aims, sequenced

1. **Establish the multi-source denominator.** Assemble training programs from
   RePORTER + Gates + CrossRef-funder + (if granted) Wellcome/IATI, deduplicating
   across sources. Report per-source coverage and overlap — the "what each
   database sees" matrix. *(Aim B foundation.)*
2. **Reconstruct and characterize the partnership network.** Institution- and
   country-level SNA: centrality, brokerage, community detection, South–South vs.
   North–South edge ratios, over time. Reuse the trials-paper methods. *(Aim A.)*
3. **Quantify the instrument effect.** Show how network centrality metrics shift
   as sources are added — i.e. how much of "US-centrality" is Fogarty's shadow.
   *(Aim A × B — the interlock.)*
4. **Link training to output (optional bridge to the trials paper).** Do
   graduates/institutions of these programs appear as PIs/sites in the AI-trial
   and AI-publication networks? Connects supply side to the paper you published.
5. **Audit formal degree & diploma programs (Aim E, below).** The grant-invisible
   layer — degree programs and curriculum partnerships. Completes the coverage
   picture and surfaces candidate education partners. Detailed as Aim E below.

---

## Aim E — Audit of formal degree & diploma programs (the grant-invisible layer)

*Added at the researcher's suggestion. This aim targets exactly what the funder
databases in Aims A–D cannot see: locally-funded, university-hosted **degree and
diploma programs**, and the **curriculum/education partnerships** (twinning, joint
degrees, accreditation harmonization) that are a distinct tie-type from
research-grant partnerships.*

**Why it completes the project.** Aims A–D map the *research-funding* network and
its coverage bias. But a Master's in Health Informatics at a Kenyan or Ghanaian
university that runs on tuition and government subvention leaves **no trace in
RePORTER, Gates, or CrossRef**. A degree-program audit is therefore not a
side-quest — it is the direct empirical test of the Aim-B claim that grant data
systematically undercounts African-led capacity. If the audit finds many programs
invisible to the grant sources, that *quantifies* the blind spot.

**This is evidence synthesis, not an API pull — and that shapes the method.**
There is no clean programmatic source for degree programs. But the ground is
partly prepared:

- **Existing audits to seed from.** A 2021 *JAMIA* study (Were et al., first/
  corresponding author Martin C. Were; doi:10.1093/jamia/ocab075) already reviewed
  curricula from **7 of 8 accredited MSc Health Informatics programs in the East
  African common labor/education zone**, coding them against a **73-competency
  IMIA-derived template** and using Jaccard similarity to compare coverage. This
  gives both a validated method and a citable seed set (East Africa). *(Note: only
  the open-access ABSTRACT of this paper was retrieved this session; the abstract
  reports the aggregate findings but does not name the individual institutions or
  print their curricula — the named-program list must be reconstructed from
  institutional sources, not quoted from this paper.)* A *JHIA* scoping review on a
  digital-health curriculum for the African health workforce is a second potential
  seed source, but was seen only as a search-result title this session and not
  retrieved — its scope and figures are unverified and must be confirmed before
  citing.
- **Institutional anchor.** HELINA — the Pan-African Health Informatics
  Association and IMIA's African regional body (founded 1993) — runs an Education
  Working Group that sets minimum MSc-HI competency standards and works with the
  Inter-University Council of East Africa on accreditation. HELINA's membership
  (12+ national associations) and directory are the backbone of a continent-wide
  program registry.
- **Competency framework.** The IMIA Recommendations on Biomedical & Health
  Informatics Education provide the standard against which curricula can be scored
  — so "curriculum coverage" is measurable, not subjective.

**Proposed method (systematic, reproducible):**
1. **Assemble the program register.** Union of: published scoping-review program
   lists (JAMIA/JHIA seeds) + national accreditation-body registries + HELINA
   member-association directories + university-catalog search. Record for each:
   institution, country, degree level (certificate/diploma/BSc/MSc/PhD), year
   established, mode (in-person/online/hybrid), and stated international
   affiliations.
2. **Extract curriculum-partnership ties.** From program pages/handbooks, code
   named partner institutions and partnership *type* (joint/dual degree, twinning,
   faculty exchange, accreditation harmonization, curriculum donor). This yields an
   **education-partnership network** — distinct from, and comparable to, the
   research-grant network of Aims A–B.
3. **Score curricula** against the IMIA competency template (reuse the JAMIA
   coding scheme) to map *what* is taught and where the gaps are.
4. **Cross-reference against grant data.** For each degree program, check whether
   its host institution appears in the RePORTER/Gates training-grant set — the
   direct measure of Aim-B invisibility.

**Publishable outputs:** a continent-wide degree/diploma program register (a
resource in itself), an education-partnership network, a competency-coverage map,
and a quantified estimate of how much formal training capacity the grant
databases miss. It also directly serves your applied goal — the register surfaces
**candidate curriculum/education partners**, not just describes the landscape.

**First cross-reference result (Aim B payoff, computed this session).** Matching
the 11-program East Africa register against the RePORTER training-grant set:
**8 of 11 host institutions appear in the grant data; 3 do not** (Mekelle
University, University of Dar es Salaam, Kabarak University). Two of those three
are *accredited MSc HI programs* — so even a host institution's total absence
from the informatics-training grant record does not mean it lacks a degree
program. And the converse caveat matters just as much: a host institution
appearing in RePORTER (e.g. Makerere, Moi, Nairobi) means it *receives* informatics
grants, **not** that its MSc HI degree was grant-funded — degree programs and
research-training grants are different objects at the same institution. The clean
Aim-B statement is therefore at the *program* level, not the institution level:
the grant databases have no field that records a degree program at all, so 100%
of the teaching programs are invisible as programs even where their host is
grant-visible. (`ea_hi_grant_crossref.csv`.)

**Feasibility flags (honest):** No API; requires curated scraping + manual
verification, so it is more labor-intensive than Aims A–B. Program directories go
stale and some curricula aren't public. Recommended to **scope the first pass to
East Africa** (where the JAMIA seed set and IUCEA accreditation give a verifiable
denominator), then expand. I did **not** pre-populate the institution list here
because the full JAMIA curricula table wasn't in the open-access text — building
the register from verified sources is step 1 of the work, not something to
fabricate up front.

---

## Caveats (verified, not assumed)

- **LLM partner-extraction has error.** 517 edges are a first pass from abstract
  text; ~54% of African-hosted and ~25% of US-hosted grants yielded ≥1 partner —
  the rest either name no partner or describe it too vaguely. A validation round
  (manual audit of a sample; cross-check against grant "foreign components") is
  required before publication-grade claims.
- **RePORTER dedup** is by core project number; multi-project programs may still
  double-count. 
- **Country normalization** merged case/spelling variants (USA/United States) but
  a residual "Unknown/Regional" bucket (~5 edges) was dropped from the network.
- **This is US-funded data only** — every structural claim in Aim A is currently
  conditional on that, which is the whole point of Aim B.

---

## Deliverables from this session

- `training_partnerships.png` — the two-panel proof of concept (network + funder concentration).
- `training_programs.csv` — 624 unique programs with host, funder, extracted partners.
- `partnership_edges.csv` — 517 host↔partner edges classified by direction.
