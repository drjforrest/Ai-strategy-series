# Research programme strategy — AI, interoperability and health-informatics capacity

**Owner:** Dr. Jamie Forrest · **Date:** 6 Oct 2026 · **Purpose:** programme-level strategy across the three-paper series, now with a Canadian comparator threaded in; written to double as the source for a 5-minute programme talk (2–3 slides).

---

## 0. The programme in one sentence

**The world is writing AI policy faster than it is building the data, interoperability and workforce scaffolding that AI needs to reach patients — and this programme measures that gap with one reproducible instrument, at continental scale and now against a high-income benchmark.**

That sentence is the whole talk. Everything below is the evidence for it.

**The structure is three papers, three objects, one instrument:**

| | Object of study | Question in one line |
|---|---|---|
| **Paper 1** | AI strategies (rhetoric) | Do AI strategies engage the competencies safe digital health requires — and does their emphasis track measured capability? |
| **Paper 2** | AI strategies **vs** health-data strategies (connectivity) | Are AI policy and health policy one connected system or two parallel, unlinked streams? |
| **Paper 3** | The training system (capacity) | Does the workforce being trained actually supply the competencies the policies assume? |

Genre — not geography — is the discriminator. The series moves **policy → connectivity → capacity**, from text, to the relationship between texts, to the humans the texts assume.

---

## 1. Paper 1 — Rhetoric and readiness
**Status:** analysis complete and reproducible; full manuscript exists (v1.3, 29 Sep) on a superseded corpus, awaiting port to the 12+AU run. **Venue:** BMJ Global Health.

- **Data.** 13 entries — 12 national AI strategies (Benin, Côte d'Ivoire, Egypt, Ghana, Kenya, Mauritius, Nigeria, Rwanda, Senegal, South Africa, Tanzania, Zimbabwe) + the AU Continental AI Strategy, French included.
- **Method.** Multilingual sentence-transformer embeddings; the nine WHO *Global Strategy on Digital Health* core components act as the **measurement grammar**; a separate six-lever **operationalization** score separates semantic alignment from execution specificity; a **circularity guard** splits the nine Oxford Government AI Readiness dimensions into text-proximate vs independently-built, tested with an exact permutation.
- **Contribution.** A reference-agnostic, circularity-guarded **instrument**, plus the demonstration that **alignment, operationalization and measured capability are non-equivalent constructs**.
- **Durable result.** The **AU Continental AI Strategy is markedly thin on standards and interoperability relative to the AU Digital Transformation Strategy** — the most robust finding in the project; it survives every sensitivity test.
- **Honest position.** The rhetoric–readiness association is **exploratory**: pooled r = −0.005; text-proximate mean +0.164 vs independent mean −0.054; exact permutation **p = 0.083 (n.s.)**. Excluding Morocco on genre grounds moved p across 0.05; the manuscript must report both corpora openly, keep the genre exclusion a priori, and lead with the instrument, not the null.

## 2. Paper 2 — Connectivity (the Canadian comparator lands here)
**Status:** analysis complete and reproducible; HIMSS27 poster is submission-ready (abstract due **11 Oct 2026**). **Venue:** HIMSS27 poster → journal.

- **Data.** Set A: 12 national AI strategies + AU (same corpus as Paper 1). Set B: 15 national digital-health strategies, four French-language; Uganda retained as an off-genre contrast.
- **Method.** One instrument, three independent operationalisations of "connectivity": **(i) AI centrality** (explicit AI terms per 1,000 words, EN+FR); **(ii) competency overlap** against the WHO nine components; **(iii) document linkage** — a deterministic, embeddings-independent regex/dictionary measure of coverage, cross-reference and shared-actor Jaccard overlap.
- **Results.** A **hard genre boundary** — AI centrality 19.3–46.9/1k in AI strategies vs 0.00–1.11/1k in health strategies, no overlap. Competency overlap: health leads on all nine domains (0.602 vs 0.472). Linkage: 7 of 12 AI-strategy countries (58%) have a matched health strategy, yet **no AI strategy names its health counterpart** and shared-actor Jaccard runs 0.00–0.25. Connected in coverage, unlinked in substance.
- **Canadian comparator (new).** Canada is a country with **both** an AI strategy *and* a health-data strategy produced by the same government in the same period — the identical two-document structure, in a high-income, bilingual, federated setting. Scoring *AI for All* (June 2026) and the Pan-Canadian Health Data Charter/Strategy with the **same instrument** turns Canada into a **benchmark case**, not a fifth African one.
  - If Canada's two streams **also** fail to connect → the disconnection is **structural, not a resource problem**. A much bigger claim.
  - If Canada **does** connect (CIHI as a shared actor across both is already a hint) → the African disconnection is **a governance-design choice, not inevitable**. That is the actionable, Canada-facing result.
  - Either way the reviewer's real question — *what does this do for Canadian healthcare?* — is answered with evidence.
- **Design caveat to state explicitly.** Canada is a **benchmark of one**, deliberately outside the sampling frame. Frame it as a reference case, not as an additional sample; do not let it read as "n = 16."

## 3. Paper 3 — Capacity and the responsible-AI overlay
**Status:** protocol written (v0.1, 5 Oct); **no data collected.** **Venue:** HELINA / AMIA / MedInfo / health-professions education — decided after results.

- **Data.** A continental census of health-informatics / digital-health programmes (one row per programme), by public document review.
- **Method (two-layer template).** **Layer A** — foundational informatics domains, IMIA (2nd rev. 2023) with AMIA 2017 as cross-walk. **Layer B** — a purpose-built **responsible-AI-in-health overlay**, each domain traceable to an empirical finding in Papers 1–2 (data ethics; bias/fairness; governance/accountability; clinical validation; human factors; interoperability as AI prerequisite; ML literacy; AI procurement/economics).
- **Headline candidate (RQ4).** The **policy–capacity linkage** — for each country, does policy ambition correspond to actual training capacity? *A country can legislate AI and train nobody.* Presented as descriptive quadrants, not inference (small n).
- **Discipline (carried from the architecture review).** Do **not** pre-commit to "workforce is the weakest." Workforce is the weakest **AI-strategy** domain (C7 = 0.428) but mid-pack in the digital-health set — let the census decide.
- **Differentiation from prior art.** Were et al. (2021, JAMIA) is the template and the bar: continental scope + the responsible-AI overlay + the policy linkage are Paper 3's three distinct claims.
- **Canadian pilot (new).** Run the Layer-B overlay on **5–8 Canadian programmes** (Toronto MHI, Waterloo MHIA, UVic MSc, Ontario Tech, U of T MScAC AI-in-healthcare, and the CAHIIM-accredited set) as a **pilot and comparator**. This does three things at once: calibrates coding and κ before the full African census; gives a high-income benchmark for the same overlay; and speaks directly to MSHI teaching and curriculum design. It also generalises the instrument across two systems — the difference between "a study of Africa" and "a validated method."

---

## 4. What makes this one programme, not three papers

- **One instrument, carried.** The WHO nine components + embedding pipeline run through Papers 1 and 2; the responsible-AI overlay in Paper 3 is *derived from* their findings. Disclose the reuse plainly — Paper 2 introduces no new framework.
- **One argument, escalating.** Policy language (1) → whether policy systems talk to each other (2) → whether people are being trained for what policy assumes (3). Each step narrows from text to the humans the text depends on.
- **One reproducibility standard.** Same clean → segment → embed → score pipeline; `.venv/bin/python` (3.12 + sentence-transformers) enforced, and `analyze_connectivity.py` **hard-aborts** on TF-IDF fallback so lexical and semantic scores can never be silently mixed.
- **Salami-slicing guard.** Papers 1 and 2 share the 12-country AI corpus; the *question*, the *second corpus* and the *linkage method* differ — not the documents. State that in every submission.

---

## 5. Canada's role — one home, not three

Put the Canadian comparator in **Paper 2** as the benchmark case; let it reappear in **Paper 3** as the programme pilot; keep **Paper 1** continental and genre-clean. Spreading it across all three makes it read as padding in each. Canada's job is to answer *"is this about resources or about architecture?"* once, convincingly.

---

## 6. Timeline and decision gates

| Date | Item | Action |
|---|---|---|
| **11 Oct 2026** | HIMSS27 abstract | Finalise author list; freeze 15/58%; verify portal limits. *Highest priority.* |
| **20 Oct 2026, 17:00 PT** | **e-Health27 abstract** (blind, ≤500-word body, Vancouver May 2027) | Submit Abstract 1 — the AU standards/interoperability gap, "In Support of Connected Health" track, **Oral** first choice / e-Poster second. Confirm BMJ GH prior-presentation policy. |
| Oct–Nov 2026 | Canadian texts | Pull *AI for All* + Pan-Canadian Health Data Charter; format as `data/canada/canada_ai.txt`, `canada_hd.txt`; score with the existing pipeline. |
| Q4 2026 | Paper 2 journal version | Add Canada as benchmark; write up connectivity for a journal. |
| Q1 2027 | Paper 1 | Port v1.3 to the 12+AU corpus; reframe; submit to BMJ GH. |
| Q1–Q2 2027 | Paper 3 | Ratify G1–G4; build census sheet; pilot κ on 3 African + 3 Canadian programmes; then full census. |

**Gates still open (Paper 3):** G1 two-layer template; G2 continental vs regional scope; G3 Phase-2 director survey in/out; G4 census-of-public-information (no ethics approval).

---

## 7. Talk-ready slides (5 minutes, 3 slides)

### Slide 1 — The thesis (60 sec)
- Title: **"AI policy is outrunning the scaffolding it needs."**
- One line: *Africa is writing national AI strategies faster than it is building the data, interoperability and workforce infrastructure AI needs to reach patients.*
- One instrument, three papers: **policy → connectivity → capacity.**
- Visual: the three-object alluvial (AI strategies → digital-health strategies → trained workforce), with the instrument as the spine.

### Slide 2 — The evidence (2 min)
- **Paper 1 (BMJ GH).** 12 African AI strategies + AU; WHO nine-component instrument; alignment, operationalization and measured capability are non-equivalent; **AU AI strategy is thin on standards/interoperability** — the durable result.
- **Paper 2 (HIMSS27).** AI vs health-data strategies: a hard genre boundary (AI terms 19–47/1k vs ~0/1k); health leads on all nine domains; **7 of 12 countries matched, but no AI strategy names its health counterpart** — connected in coverage, unlinked in substance.
- **Paper 3 (in development).** Continental census of health-informatics programmes against a **responsible-AI competency overlay** — does anyone train the workforce the policies assume? Plus a **Canadian pilot** of the same overlay.
- Visual: the AI-centrality ranges (non-overlapping) and the linkage grid.

### Slide 3 — Why it matters, and where it goes (2 min)
- **The Canadian turn.** Canada — *AI for All* (June 2026) + the Pan-Canadian Health Data Charter + CIHI's Health Sector Data Space — is the **benchmark**: does a well-resourced system wire AI policy to its health-data custodian, or repeat the same disconnect? The answer tells us whether the gap is **structural** or a **design choice**.
- **So what.** Interoperability standards, data governance and workforce pathways should be built as **shared AI–health infrastructure**, not as separate agendas. Canada is building the scaffolding first and layering AI on top; the sequencing is the lesson.
- **Where it goes.** Paper 1 → BMJ GH; Paper 2 → HIMSS27, then journal; Paper 3 → HELINA/AMIA, with a Canadian programme pilot that feeds directly into MSHI curriculum.
- Visual: the policy–capacity quadrant (ambition × training capacity), Canada plotted.

**Speaker note:** 5 minutes is ~2 slides of content, not 3. Use Slide 1 as the opener (30–45 s), Slide 2 as the body (~2.5 min), and keep Slide 3 as your close — if time is short, drop to the "Canada + so what" bullets and end on the one-sentence thesis.

---

## 8. What I need to finish the e-Health abstract

Once the Canadian documents are in `data/canada/`, I have everything: the AU standards-gap result, the linkage numbers, the framing. Send the word and I will (a) confirm the Canadian texts score cleanly on the WHO instrument, (b) draft the ≤20-word title, ≤75-word summary and ≤500-word four-section body, fully de-identified for blind review, and (c) sanity-check it against the "In Support of Connected Health" track language.

---

## 9. Computational Implementation Science (CIS) — the theory spine, folded in

**Status:** commentary drafted ("Computational Implementation Science: Naming and Formalizing…"); submission venue undecided (Implementation Science Communications *Debate* vs npj Digital Medicine *Perspective*). **Role in the programme:** CIS is not a fourth silo — it is the **theoretical frame the three empirical papers sit inside.**

### 9.1 What CIS is (the one-line version)
**CIS is the implementation science of computational interventions** — the study of how tools whose outputs and effects change *after deployment* (model versions, thresholds, data distributions, hardware, vendor dependencies) are adopted, monitored, adapted, governed, sustained and **retired**. Its defining claim: for computational interventions, **adoption, workflow integration and sustained use do not guarantee sustained performance, equity or benefit.** Conventional implementation success can coexist with computational failure.

### 9.2 Why it belongs in *this* programme (not next to it)
The three papers are an empirical instrument for the problem CIS names in theory. The join is almost exact:

| CIS construct | What the programme already measures |
|---|---|
| **Computational fidelity** — does the deployed version/threshold/input match the evaluated spec? | Paper 1's **operationalization** levers + Paper 3's curriculum-coverage "intended vs delivered" caveat |
| **The intervention doesn't stay still** | Paper 2's **hard genre boundary** — AI terms 19–47/1k in AI strategies vs ~0/1k in health strategies |
| **Governance principles ≠ operational capability** | Paper 1's **AU standards/interoperability gap** — policy *says* interoperability; the scaffolding isn't built |
| **Retirement / decommissioning as a designed outcome** | Paper 2's **linkage finding** — no AI strategy names its health counterpart; no exit criteria connecting the streams |
| **Minimum-viable, risk-proportionate capability** | Paper 3's **responsible-AI overlay** — whether anyone is trained to inspect data, verify thresholds, monitor subgroup drift, or discontinue safely |

The programme's robust empirical result **is** a CIS finding: *policies commit to post-deployment monitoring and lifecycle governance they have no existing capability to enact.* The three papers show it at continental scale; CIS gives it a name and a theory.

### 9.3 How CIS strengthens each empirical paper
- **Paper 1** — CIS explains *why* the standards/interoperability gap matters: interoperability is a computational-fidelity dependency, not a bookmark. The rhetoric–readiness null becomes a CIS hypothesis — policy language lives in a different register from operational capability.
- **Paper 2** — CIS supplies the "so what": two unlinked streams mean no shared owner for post-deployment monitoring. The linkage measure (coverage / cross-reference / shared-actor Jaccard) is a proxy for **whether a governance capability has a home**. Canada's CIHI benchmark is, in CIS terms, a test of whether capability is *institutionally located*.
- **Paper 3** — CIS tells you what the overlay must measure: not "does the curriculum mention AI," but "does it train the computational-fidelity and algorithmovigilance capabilities the policies assume." The Layer-B domains map onto the CIS agenda almost one-to-one.

### 9.4 Where CIS sits as a deliverable
Two viable shapes — pick after the empirical papers land:
1. **Theory-spine, embedded.** CIS becomes the **framing/devices** of Papers 1–3 (each cites it; it is the programme's theoretical contribution). Lowest risk; no fourth submission to manage.
2. **A fourth output — the commentary itself,** positioned as the *theory* paper the programme **empirically closes**. Sequencing: submit the commentary once at least one empirical paper is public, so it can cite real results rather than promise them. A *Debate* piece in Implementation Science Communications, citing Papers 1–2, is the natural home; npj Digital Medicine *Perspective* only if you want the digital-health audience and the case studies kept front.

**My recommendation:** build it as the **theory spine now** (cheap, strengthens every submission) and release the standalone commentary as the **programme's capping paper** when the census is done — it then reads as an agenda *vindicated*, not proposed.

**Decision (Dr. Forrest, 6 Oct 2026):** the commentary is an **early draft and is parked** — *not* a near-term submission. It will be published **in relation to the outcomes of Papers 1–3**, once the empirical results are in hand. Treat §9 as the theory spine that shapes the framing of the three papers *now*; defer the standalone piece until the results exist. Open task: preserve the verifiability of the four African case citations (CAD4TB; cervical AVE; Penda Health; Babyl) and re-check for any emerging use of the term before drafting resumes.

### 9.5 Verification and honesty notes before submission
- **AIM-IS is verified:** Fontaine G, Michie S, Beidas RS, et al. *AI Methods for Implementation Science (AIM-IS)*. *Implementation Science* 2026. doi:10.1186/s13012-026-01503-5 (14 Apr 2026). Keep the directional framing — AIM-IS = AI *for* implementation science; CIS = implementation science *for* computational interventions. The commentary's own distinction is correct and timely.
- **The novelty claim needs tightening.** Exact-phrase search finds no established usage of "computational implementation science" in the health/biomedical literature — *supports* the claim, but is not proof. Before submission: run an exact-phrase search in Google Scholar + Scopus/Web of Science; hedge the sentence to *"no established usage in the health or biomedical implementation literature, to our knowledge"*; and watch the separate CS-education "computer implementation" usage so a reviewer can't use it to unseat the term.
- **Citation hygiene (the commentary's own note 2).** The African cases — CAD4TB (Fehr 2023; Nzimande 2025), cervical AVE (Phiri 2026), Penda Health, Babyl Rwanda — must be individually verified to first source before submission. These are the commentary's load-bearing empirics.
- **Positionality paragraph (the commentary's own note 4).** Essential and on-brand: your Rwanda/MoH and TOGETHER experience is *why* the African cases develop theory rather than frame settings by deficit. Write it early — it also pre-empts a reviewer reading the cases as extraction.

### 9.6 Add CIS to the talk (extends §7)
If you have a **fourth slide** (or if you drop one §7 slide, keep this):
- **"The theory underneath."** CIS: when the intervention changes after deployment, implementation success ≠ sustained performance. The programme's finding — *policy commits to monitoring it can't yet perform* — is a CIS result. One instrument, three empirical papers, one theoretical frame.
- This is the line that turns "three African policy papers" into "**a research programme with a theoretical contribution**" — exactly what a programme talk needs to land.

---

## 10. Preliminary Research & Future Directions

### 10.1 Preliminary research — pilot evidence already in hand

The programme rests on completed pilot work, not proposals. Each pilot has already produced a reproducible result.

| Pilot | Status | Headline output |
|---|---|---|
| **P1. AI-strategy instrument** (Paper 1) | Complete, reproducible | 12 national AI strategies + AU scored against the WHO nine components; alignment, operationalization and measured readiness shown to be non-equivalent; **AU AI strategy markedly thin on standards/interoperability** vs the AU Digital Transformation Strategy. |
| **P2. Connectivity & linkage** (Paper 2) | Complete, reproducible | A hard genre boundary (AI terms 19.3–46.9/1k vs 0.00–1.11/1k); health leads on all nine domains (0.602 vs 0.472); 7 of 12 AI-strategy countries have a matched health strategy, yet **no AI strategy names its health counterpart**. |
| **P3. Canadian benchmark** | Complete, reproducible | *AI for All* vs the Pan-Canadian Health Data Strategy scored with the **same instrument**: the genre boundary and the "health leads every domain" pattern **replicate in a G7 country**, and Canada is measurably **more connected** (shared-actor Jaccard 0.333 vs 0.00–0.25) but **asymmetrically** so. |
| **P4. Sector salience scan** | Complete, exploratory | Health is a **second-tier vertical** in African AI strategies (median 1.30/1k vs government 4.94, finance 4.54, education 4.08) — and the same is true in Canada (3.71/1k). |
| **P5. Policy vs capital** | Exploratory, sources verified | Policy text and capital allocation **diverge**: fintech ~60% of African equity funding vs healthtech ~3% (and falling), even though policy text gives health *more* attention than fintech. |
| **P6. Computational Implementation Science** (theory) | Draft, parked | CIS named and drafted as the implementation science of computational interventions; to be published **in relation to** Papers 1–3 outcomes, not before. |

**What the pilots already establish.** (1) A reproducible, multilingual instrument exists and generalises across two continents. (2) The AI/health-data disconnect is **structural but improvable**. (3) Health AI is a **second-tier priority** in policy and a **third-tier recipient** of capital. Together these are enough to draft, submit and defend — the programme is past proof-of-concept.

### 10.2 Future directions

**Near term (publish what exists).**
1. **Paper 1 → BMJ Global Health.** Port the manuscript onto the 12+AU corpus; lead with the instrument; keep the readiness comparison explicitly exploratory.
2. **Paper 2 → HIMSS27 + journal.** Add Canada as the benchmark case; add the **policy-attention vs capital-allocation** panel (the strongest form of the thesis).
3. **e-Health27 abstract** (20 Oct 2026) — the AU standards gap + Canadian replication, "In Support of Connected Health" track.

**Medium term (build the missing leg).**
4. **Paper 3 census + responsible-AI overlay.** Programme census across African higher education; Layer-A (IMIA/AMIA) + Layer-B (derived responsible-AI domains); a **Canadian programme pilot** of the same overlay that doubles as MSHI curriculum work.
5. **The policy–capital–capacity triad.** Extend Paper 3's quadrant to three axes — a country can legislate AI, attract AI capital, and still train no one.
6. **Curate a capital dataset** (`data/capital/african_ai_capital_by_sector.csv`, 2021–25, per source with denominators) so the capital panel is reproducible, not assembled from memory.

**Longer term (extend the programme).**
7. **CIS as the capping theory paper** — released once ≥1 empirical paper is public, so it cites results rather than promises them; target Implementation Science Communications (*Debate*) or npj Digital Medicine (*Perspective*).
8. **Measurement upgrades:** move sector salience and policy–capital from keyword proxies to the semantic instrument; add **operationalization-lever** scoring for Canada.
9. **Currency and scope:** a fixed census date with scheduled refresh; Phase-2 programme-director survey (adds rigour, cost, ethics); possible extension of the instrument beyond Africa to other low- and middle-income regions.
10. **Teaching integration:** feed the responsible-AI overlay and the Canadian benchmark directly into MSHI curriculum design and the AI-related teaching standards in the annual goal portfolio.

### 10.3 The through-line

> **Preliminary research shows the instrument works, the disconnect is structural, and health is under-weighted in both policy and capital. The future direction is to close the loop — from what policies *say*, to what systems *build*, to who is *trained* to run them — with the Canadian benchmark showing the gap can be closed by design.**

*Note added 6 Oct 2026. Written for the research-programme strategy document; §10 may also serve as the scaffold for a formal Research & Scholarship statement.*

---

## 11. Programme tiers — core spine vs conference branches

**Clarification (Dr. Forrest, 7 Oct 2026).** The expansion of the programme from three papers to six items reflects a **deliberate diversion toward conference themes** — notably e-Health's Canadian focus — layered on the original intent. The branch items are **conference abstracts first**. They may become full manuscripts if they gain traction; if not, the **original core ideas stand as fallback**. Do not over-weight the branches in slides, statements, or reporting.

### Two tiers

| Tier | Items | Intent | Venue |
|---|---|---|---|
| **Tier 1 — Core spine** | Paper 1 (rhetoric & readiness) · Paper 2 (connectivity) · Paper 3 (workforce capacity) · Commentary (CIS) | Full manuscripts intended; carry the programme | BMJ GH · journal · journal · npj Digital Medicine |
| **Tier 2 — Conference branches (probes)** | **Paper 2b** (Canada comparator) · abstract variants | **Abstract-first**; manuscript optional; preserve core ideas as fallback | e-Health27 (Canada) · HIMSS27 (2a) |

### Implications for how this is represented

1. **Naming.** Call 2b a **comparator branch of Paper 2**, not a sibling "paper," until it earns its own manuscript. Two abstracts drawn from the same African AI corpus (2a connectivity, 2b Canada) otherwise invite a **salami-slicing** read. The distinction is real and defensible — 2a adds the *African digital-health* corpus and the *linkage method*; 2b adds the *Canadian comparator* — but it must be stated wherever both appear.
2. **Fallback is a feature.** The core three (plus commentary) survive regardless of whether any conference branch is accepted. Branch abstracts are **options**, not obligations, and cost little.
3. **Abstract discipline.** Conference abstracts may never become manuscripts — so they must not (a) claim beyond the data, (b) promise analyses not yet done (e.g. a "maturity typology"), or (c) create duplicate-presentation conflicts across venues. Keep claims to what the instrument has produced.
4. **CIS floor and ceiling.** The commentary remains **parked** (Tier 1, released after Papers 1–3 outcomes). Its *concept* may frame the branches, but the standalone piece is not a branch submission.

### Still open before slides
- **Reconcile the CIS definition.** The Year-1 Loop document defines CIS as *integrating computational methods into implementation science* — the **AIM-IS** direction — whereas the commentary defines it as *implementation science for computational interventions*. These are opposite theses; adopt the commentary's (differentiated) version on any slide, and soften the Loop line that lumps "AIM and IS frameworks" together (AIM-IS is a sibling, not a target).
- **Confirm targets:** Canada document = Pan-Canadian Health Data Strategy (EAG reports) vs "Digital Health Strategy"; Paper 3 journal = "after results" vs "JMIR"; Paper 2a = HIMSS27 poster (and whether a separate GH informatics call is also in play).
