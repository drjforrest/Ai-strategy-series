# Adjacent project ideas: AI, technology, and development in Africa

*Brainstorm brief building outward from "Mapping AI diagnostic innovation networks
in sub-Saharan Africa." Every idea below is anchored to a public data source I
tested live from this environment (July 2026). Reachability and feasibility notes
are real, not assumed.*

---

## What the published paper established (the launch point)

The paper is a **census social-network analysis of 11 registered AI-diagnostic
trials** in sub-Saharan Africa, drawn from ClinicalTrials.gov, PACTR, and the WHO
ICTRP. Its headline finding was **complete network fragmentation** — no shared
institutions or funders linking the trials into a connected collaboration
structure — and it raised, without being able to resolve, questions about
**Northern institutional dominance, equity of authorship/leadership, and
sustainability**. It deliberately scoped *out*: treatment/therapeutic AI, disease
surveillance, health-system/operational AI, and anything not captured as a
*registered trial*.

That scoping is exactly where the adjacent territory lies. The trial registry is
the tip of an iceberg; the research literature, the deployment/regulatory record,
and the open-source software layer beneath it are all publicly measurable and
were never in frame.

---

## Data-source reachability (tested live, this environment)

| Source | Status | What it unlocks |
|---|---|---|
| **OpenAlex** | ✅ reachable (key wired) | Full research-collaboration network: authors, institutions, countries, author *position* & corresponding-author flags, concepts, citations |
| **ClinicalTrials.gov v2** | ✅ reachable | Registered trials, sponsors, locations, status/phase |
| **CrossRef** | ✅ reachable | DOIs, funder metadata (Funder Registry), references |
| **GitHub API** | ✅ reachable | Open-source health/AI software, contributors, geography |
| **openFDA** | ✅ reachable, but weak AI indexing | Device clearances — poor for AI/ML text search |
| **World Bank** | ⛔ blocked (grantable) | ICT/development indicators (internet %, health spend) |
| **Our World in Data** | ⛔ blocked (grantable) | Curated development/technology time series |
| **WHO GHO** | ⛔ blocked (grantable) | Health-system & workforce indicators |

Blocked sources are one approval click away if an idea depends on them.

---

## Measured signal already in hand (not hypothetical)

From a live pull of the AI-in-health research base with an African affiliation:

- **~32,500 AI + health works** with an African institutional affiliation since 2015.
- Output concentrated in **Egypt, South Africa, Nigeria, Morocco, Tunisia, Ethiopia**;
  the highest-volume non-African co-authoring countries are **the US (4,821), UK (2,644),
  Saudi Arabia (2,157), France (1,817), India (1,683), and China (1,204)** — the same
  North–South pattern the paper flagged, now visible at ecosystem scale.
- In a 1,600-work sample of recent (2022–) AI-health works with an African affiliation:
  **51% African first-author, 58% African last-author, 65% African corresponding-author**,
  yet **75% internationally co-authored**.

That last line is the interesting one: the "parachute science" story is real on
co-authorship (3 in 4 papers involve a Northern partner) but **more nuanced on
leadership** than a simple dominance narrative — African researchers hold the
senior-author roles in the majority of papers. Adjudicating *that* tension is a
publishable question, and it's the same network-analysis toolkit the paper already
used.

---

## Six project ideas, ranked by fit + feasibility

### ⭐ 1. From 11 trials to the whole field: the AI-health research collaboration network of Africa
**The direct scale-up of the paper.** Replace the 11-trial census with the full
OpenAlex co-authorship/co-institution network of AI-health research with African
affiliations (~32k works). Same SNA methods (centrality, community detection,
North–South bridging), but now with the statistical power to test what the
11-trial paper could only gesture at: *Is the research network as fragmented as
the trial network, or does the literature reveal collaboration structure the
registry misses?*
- **Data:** OpenAlex (reachable). **Health-informatics fit:** ★★★★★
- **Novelty vs. paper:** same method, ~3000× the sample, tests the paper's own open questions.
- **Feasible now:** yes, fully.

### ⭐ 2. Who leads vs. who hosts: an authorship-equity analysis of African health AI
Turn the measured signal above into a paper. Using author *position* and
corresponding-author flags (confirmed available in OpenAlex), quantify — by
country, institution, funder, and over time — the gap between **where the data /
patients are** and **where the intellectual leadership sits**. Track whether
African-led share is rising. This is a decolonizing-global-health / research-equity
contribution with a clean, reproducible metric.
- **Data:** OpenAlex (reachable). **Health-informatics fit:** ★★★★★
- **Novelty:** operationalizes "parachute science" as a longitudinal, measurable index.
- **Feasible now:** yes — preview metric already computed.

### 3. The trial → publication → regulation pipeline (leakage analysis)
Link the paper's registered trials forward: do African health-AI trials produce
publications (CrossRef/OpenAlex), and do any reach a regulatory/deployment
signal? Measure the **attrition** at each stage and where the pipeline leaks. A
health-informatics translational-gap study.
- **Data:** ClinicalTrials.gov + OpenAlex + CrossRef (all reachable); openFDA weak.
- **Fit:** ★★★★☆ **Feasible now:** mostly — deployment endpoint is the hard part.

### 4. The open-source layer: who actually builds African health-AI tools?
The software beneath the papers. Mine GitHub for health-AI repositories tied to
African health problems (malaria, TB, maternal health, HIV) and map
**contributor geography, funding acknowledgements, and sustainability** (commit
longevity, bus factor). Complements the formal-literature view with the
build-layer view.
- **Data:** GitHub API (reachable). **Fit:** ★★★★☆
- **Novelty:** software-supply-chain lens rarely applied to global-health AI.

### 5. Concept drift: what *kind* of health AI is Africa researching, and does it match disease burden?
Using OpenAlex concept tags, map the **thematic** distribution of African
health-AI research (diagnostics vs. imaging vs. NLP vs. genomics vs. health-systems)
and test alignment against actual disease burden. Reveals mismatches between
research attention and health need.
- **Data:** OpenAlex (reachable); burden data (WHO GHO / IHME) needs an allowlist grant.
- **Fit:** ★★★★☆ **Feasible now:** research side yes; burden side needs one approval.

### 6. Funder structure of African health AI (the missing half of the paper)
The paper found funders didn't connect the trials. Rebuild the **funder network**
at literature scale using CrossRef Funder Registry + OpenAlex grant metadata.
*Caveat I verified:* OpenAlex grant coverage for these works is thin (0 of 50
sampled had grant records), so this idea depends on CrossRef funder metadata and
acknowledgement-text mining — flagged as higher-risk.
- **Data:** CrossRef (reachable), OpenAlex (sparse grants). **Fit:** ★★★☆☆
- **Feasible now:** partially — data-quality risk is real; validate coverage first.

---

## Recommended next step

Ideas **1 and 2 are the strongest**: maximal continuity with the published work,
full health-informatics relevance, and **buildable end-to-end from OpenAlex today**
with no blocked dependencies. #2 already has a live preview metric. Either can be
turned into a full reproducible pipeline + figures in a single follow-up session.
