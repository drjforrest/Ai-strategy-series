# Health Informatics Training & Capacity in Africa — Project Notes

*A consolidation of exploratory data work extending the published paper
"Mapping AI diagnostic innovation networks in sub-Saharan Africa." These notes
are a working document to stew on and share with colleagues — not a manuscript.
Every empirical claim links to a saved artifact; every unverified claim is
flagged as such.*

---

## 0. Where this came from and what it is

The published paper was a census social-network analysis of 11 registered
AI-diagnostic trials in sub-Saharan Africa, whose headline finding was near-total
network fragmentation. Rather than add literature to a closed project, this work
pivots to an **adjacent question with richer public data**: how is the *human and
institutional capacity* for health informatics and health data science in Africa
structured — who trains whom, who funds it, who partners with whom, and what does
the formal record systematically fail to see?

The work divides into three connected strands, each with saved data and figures:

1. **A landscape** of AI-in-health research output across Africa (OpenAlex).
2. **A training-partnership network** reconstructed from NIH RePORTER, with
   coverage-bias treated as a first-class finding.
3. **A program register** — a two-layer audit of degree/diploma programs and
   their curriculum partnerships, with accreditation decomposed into independent
   covariates.

A recurring methodological theme runs through all three: **the gap between what
an administrative database records and what actually exists on the ground.** That
gap is not noise to be minimized — it is the object of study.

---

## 1. The research landscape (OpenAlex)

A baseline of scale and geography, from OpenAlex (concept AI = C154945302,
filtered to African institutions, 2015 onward).

- **~32,500** AI + health works with at least one African-affiliated author.
- Steady growth: roughly 3× more such works per year in 2025 than in 2015.
- Output concentrates in a few hubs. Highest-volume African countries: **Egypt,
  South Africa, Nigeria, Morocco, Tunisia, Ethiopia**; highest-volume
  co-authoring countries outside Africa: the **US (4,821), UK (2,644), Saudi
  Arabia (2,157), France (1,817), India (1,683), China (1,204)**.
- **Authorship-leadership signal** (sample of 1,600 recent works): African
  first-author 51%, last-author 58%, corresponding-author 65% — an African-led
  *majority* — but **75% are internationally co-authored**. "Parachute science"
  is real on the co-authorship axis, more nuanced on the leadership axis.

![AI-health research landscape in Africa]({{artifact:art_86126dbe-6d52-4ef0-8b81-b539dbc43400}})

*Caveat: OpenAlex grant/funder coverage for these works is near-empty (0 of 50
sampled carried grant records), so funder mapping needs a different source — see
strand 2.*

---

## 2. The training-partnership network (NIH RePORTER)

**Aim A** — reconstruct and characterize the health-informatics *training*
partnership network. **Aim B** — treat the coverage bias of the source as a
finding, not a limitation. Aim B is the validity condition for Aim A.

### What was built
From NIH RePORTER (Fogarty and related training grants; activity codes D43, D71,
G11, K43, U2R, T37, R25; informatics/data-science/digital-health text filter):

- **624 unique training programs** (270 African-hosted + 354 US-hosted,
  Africa-focused), all with abstracts.
- **517 host↔partner ties**, extracted from abstracts and direction-classified
  (North-South, South-South, North-North).

### Key findings
- **Funder concentration.** Of the 270 African-hosted programs, **235 (87%) are
  funded by Fogarty (FIC)** alone. The next largest is NICHD at 15. This is a
  near-monopoly of one US institute over the visible training record.
- **The network is hub-and-spoke through the US.** Heaviest country-pair ties:
  **South Africa–US (49), Uganda–US (42), Kenya–US (38), Nigeria–US (29),
  Ghana–US (19)**. South-South ties exist but are thinner and mostly
  within-country.

![Training-partnership network and funder concentration]({{artifact:art_210bebbc-b3fa-49ad-8516-4d22d32421bf}})

### The coverage-bias problem (Aim B), stated honestly
RePORTER sees **only US-federally-funded programs.** It systematically misses
Wellcome, Gates, EU/EDCTP, DAAD, IDRC, and DELTAS/H3Africa funding, and it misses
African-led, university-internal, and tuition-funded programs entirely. The irony
is structural: **a map built only from NIH data will manufacture exactly the
North-dominance the original paper interrogated.** So the 87%-Fogarty and
everything-routes-through-the-US findings are simultaneously *true of the visible
record* and *artifacts of which record is visible.* Quantifying that shadow — by
folding in non-US funders — is a defined next step, not a solved problem.

---

## 3. The program register — a two-layer audit

**Aim E** — audit formal degree and diploma programs and their curriculum
partnerships. This is the grant-invisible layer: programs that run on tuition and
subvention leave no trace in any funder database. It is therefore the direct
empirical test of the Aim-B claim.

This strand is **evidence synthesis, not an API pull** — assembled from published
reviews, national accreditation registries, the HELINA/IMIA directory, and
institutional websites, with an explicit `verification_status` on every row.

### 3.1 Two layers, because the label is contested
A central lesson of this work: **"health informatics" is a moving label.** Its
competencies increasingly live under adjacent disciplinary names. The register is
therefore built in two layers:

- **Layer 1 — named HI programs** (23 programs, 10 countries): degrees explicitly
  called "Health Informatics" / "Medical Informatics" / "Health Information
  Management." The enumerable object; a clean denominator.
- **Layer 2 — the adjacent layer** (13 programs and counting): programs delivering
  HI competencies under epidemiology-biostatistics, data science, bioinformatics,
  or ML/AI labels. Larger, harder to bound, and where much of the strongest
  research capacity actually sits.

![Continent-wide named-HI program register]({{artifact:art_42b62a39-ebf0-4e0b-84ae-9908ab9f306d}})

![The adjacent layer: HI competencies under other disciplinary labels]({{artifact:art_9377b837-14a6-4129-bba7-31d63c536271}})

**The clearest illustration** is the University of the Witwatersrand, which runs
**"Public Health Informatics" as a named field of study *inside* its MSc
Epidemiology** — an HI track embedded in the older, more established discipline. A
name-based audit would never find it. Stellenbosch is the same story: a top-ranked
African AI-health research institution with no HI-*branded* degree, delivering the
competencies through epidemiology, biostatistics, and ML/AI degrees.

**Finding:** formal HI-branded training and actual HI research capacity are *not
the same map.* The research leaders sit disproportionately in Layer 2.

### 3.2 Accreditation is a separate covariate, not a synonym for the layer
An important clarification worked out with the data: "adjacent" is a
*disciplinary-label* axis, and accreditation is a *different, independent* axis.
The registers now decompose accreditation into three explicit covariates:

| Covariate | What it captures | What the data shows |
|---|---|---|
| **Academic accreditor** | national/regional degree regulator (CHE, NUC, GTEC, CUE, IUCEA…) | The named/adjacent split does **not** track academic accreditation. *Note: for the adjacent layer the regulator was inferred from each institution's country (national degree accreditation is the default), not verified per-program — so this shows the two axes are not collinear, not that every adjacent program's accreditation was independently confirmed.* One adjacent entry (ITI Egypt) is a **fellowship, not a degree**. |
| **HI-professional recognition** | accredited *by an HI standards body* (CAHIIM-style) or IMIA/HELINA alignment | **0 of 36 programs** carry HI-body accreditation — including the named MSc HI programs. There is no pan-African HI-specific accreditor to be excluded by. |
| **Licensure pathway** | route to professional/clinical registration (HPCSA, college fellowship) | Near-zero everywhere (2 of 36): UKZN (South Africa, HPCSA route) and ITI (Egypt, Egyptian Fellowship Board). |

**This is itself a finding:** health informatics in Africa is *academically*
institutionalized (it is taught almost entirely as nationally accredited
degrees — the one exception in the register being ITI Egypt, a fellowship) but
**not yet *professionally* accredited as its own discipline** — no HI-specific
accreditation body, essentially no licensure pathway. The IMIA/HELINA competency standards are
*voluntary alignment*, not accreditation. Accreditation should enter any eventual
analysis as three independent variables, not as a proxy for the label.

### 3.3 The grant-invisibility payoff (Aim B, demonstrated)
Cross-referencing the East Africa register against the RePORTER training-grant
set: **8 of 11 host institutions appear in the grant data; 3 do not** (Mekelle,
University of Dar es Salaam, Kabarak). Two of the three run *accredited MSc HI
programs.*

![Register vs. grant-data cross-reference]({{artifact:art_d9dcd9e0-aaa8-448b-b1f1-d41de775b1dd}})

The precise, defensible claim is at the **program level, not the institution
level**: grant databases have no field that records a teaching program at all, so
100% of the degree programs are invisible *as programs* — even where the host
institution is grant-visible. An institution appearing in RePORTER means it
*receives* research grants, not that its degree was grant-funded; the two are
different objects at the same address. The 3/11 institution-level gap is only the
visible tip.

### 3.4 Curriculum partnerships are a distinct tie-type
The education-partnership network (twinning, joint degrees, accreditation
harmonization) is structurally different from the research-grant network:

- **The strongest example is a genuine joint degree**: the University of the
  Western Cape's Master in Health Information Management is **tri-national — UWC +
  Muhimbili (Tanzania) + Neu-Ulm (Germany), DAAD-funded**, with teaching blocks
  rotating across all three countries.
- **Regional harmonization** (IUCEA + IMIA + national regulators setting common
  MSc-HI benchmarks) is a *governance* partnership structure the grant data cannot
  see at all.
- A **South-South training-hub pattern** appears in the adjacent layer:
  bioinformatics centers of excellence (ACE-Uganda at Makerere, CEBIB at Nairobi,
  the Pwani–Makerere–MUHAS network) are regional training hubs — a different
  partnership geometry than North-South research grants.

---

## 4. Data-quality notes (read before citing)

This is exploratory synthesis and several entries rest on secondary sources or
directory listings. What is and isn't confirmed:

- **Verification tiers are explicit in every register.** "Verified" means checked
  against an institution's own domain or a peer-reviewed source *this session*;
  "Needs verification" means seen only in an aggregator/directory and awaiting a
  confirming email.
- **The JAMIA East Africa review** (Were et al., 2021, doi:10.1093/jamia/ocab075)
  — only the open-access *abstract* was retrieved. It reports aggregate findings
  (7 of 8 accredited programs, 73-competency template, coverage 43.8–67.1%) but
  **does not name the individual institutions.** The named-program list was
  reconstructed from institutional sources, and East Africa rows that relied on
  the review alone are marked "Needs verification — review abstract only." Do not
  quote institution-level curriculum detail to this paper.
- **The Helwan (Egypt) entry** cites PMC10474413 by accession and title; the
  author line was not confirmed in-window, so no author-year is asserted.
- **The register is deliberately non-exhaustive** for large systems (Nigeria,
  Egypt), and says so in the data. Egypt and Nigeria need dedicated enumeration.
- **The "study-abroad" pathway** (e.g. University of Toronto's MHI for African
  scholars) is tagged `North-hosted` and kept separate — it is a real capacity
  channel but not an African-hosted program.

---

## 5. The project as one set of interconnected aims

These strands are meant to be **one project with connected aims**, not disparate
analyses:

1. **Aim A — Training-partnership SNA.** Reconstruct and characterize the network
   (done, RePORTER; extend with non-US funders).
2. **Aim B — Coverage bias as a finding.** Quantify what each source misses; the
   validity condition for A (demonstrated at program level; extend continent-wide).
3. **Aim C — Instrument effect.** Show how the choice of data source shapes the
   apparent North-South structure (the "manufactured dominance" argument).
4. **Aim D — Link training to output.** Do these programs/institutions appear as
   PIs/sites in the AI-trials and AI-publications networks? Bridges to the
   published paper.
5. **Aim E — Degree/diploma program audit.** The two-layer register and its
   curriculum-partnership and accreditation structure (this strand).

The spine connecting all five is the single question the published paper opened:
**what does the record show, what does it hide, and how does the choice of record
shape the story we tell about African health-technology capacity?**

---

## 6. Open threads / next moves (for discussion)

- **Multi-source funder denominator.** Fold Gates, CrossRef, Wellcome, DELTAS
  into the RePORTER set to quantify Fogarty's shadow (Aim B, continent-wide).
- **Enumerate Nigeria and Egypt properly** — the two largest known gaps in the
  register.
- **Map the South-South bioinformatics-hub network** (ACE-Uganda, CEBIB, Pwani
  network) as a distinct partnership geometry.
- **Backfill the adjacent layer** systematically across all top-ranked research
  institutions, not just by chance discovery.
- **Institutional outreach** (researcher to do manually): confirm the "Needs
  verification" rows, especially University of Rwanda (accredited but curriculum
  under revision — no published record exists).

---

## Appendix — artifact index

**Registers & networks (data)**
- Continent-wide named-HI register (23 programs, 3 accreditation covariates) — `africa_hi_program_register.csv`
- East Africa register — `ea_hi_program_register.csv`
- Adjacent-layer register (13 programs) — `africa_hi_adjacent_register.csv`
- Curriculum partnerships (continent) — `africa_hi_curriculum_partnerships.csv`
- Curriculum partnerships (East Africa) — `ea_hi_curriculum_partnerships.csv`
- Register↔grant cross-reference — `ea_hi_grant_crossref.csv`
- Training programs (RePORTER, 624) — `training_programs.csv`
- Training partnership edges (517) — `partnership_edges.csv`

**Figures**
- AI-health research landscape — `ai_health_africa_landscape.png`
- Training-partnership network + funder concentration — `training_partnerships.png`
- Continent-wide register — `africa_hi_register.png`
- East Africa register — `ea_hi_register.png`
- Adjacent layer — `africa_hi_adjacent_layer.png`
- Register↔grant cross-reference — `ea_hi_grant_crossref.png`

**Strategy / ideation (prose)**
- Training-partnership strategy (Aims A–E, detailed) — `training_partnerships_strategy.md`
- Adjacent-project idea set (6 ranked ideas) — `adjacent_project_ideas.md`
