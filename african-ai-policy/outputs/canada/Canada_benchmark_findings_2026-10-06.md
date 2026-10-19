# Canadian benchmark — first results

**Date:** 6 Oct 2026 · **Run:** `./run.sh analyze_canada_benchmark.py` (semantic backend confirmed) · **Outputs:** `outputs/canada/`

Canada scored with the **identical WHO instrument** used on the African corpus — same model (`paraphrase-multilingual-MiniLM-L12-v2`), same nine WHO core components, same `top_frac_mean` (top 10%) aggregation, same TF-IDF hard-abort. Canada is a **benchmark case**, deliberately outside the sampling frame; all comparisons are descriptive, n = 1.

**Documents scored.** *AI for All* (Canada's national AI strategy, June 2026; 13,483 words) vs the **Pan-Canadian Health Data Strategy**, constructed from the three Expert Advisory Group reports (28,670 words).

---

## 1. AI centrality — the genre boundary replicates

| Document | Words | AI terms | AI/1k | African band |
|---|---|---|---|---|
| Canada AI strategy | 13,483 | 508 | **37.68** | AI strategies 19.3–46.9 (median 35.5) |
| Canada health-data strategy | 28,670 | 12 | **0.42** | Digital health 0.00–1.11 (median 0.16) |

**Canada lands squarely inside both African bands** — its AI strategy at essentially the African AI-strategy median, its health-data strategy at the African digital-health level. The same **hard vocabulary boundary** that separates the two African policy streams separates the two Canadian streams. **The divide is not a low-resource artefact; it reproduces in a G7 country.**

## 2. WHO-domain alignment — the health sector leads again

| Domain | Africa AI | Africa DH | Canada AI | Canada HD |
|---|---|---|---|---|
| C1 Leadership & governance | 0.487 | 0.668 | 0.433 | 0.625 |
| C2 Investment & operations | 0.492 | 0.512 | 0.430 | 0.443 |
| C3 Services & applications | 0.447 | 0.658 | 0.443 | 0.632 |
| C4 Integration & sustainability | 0.489 | 0.654 | 0.480 | 0.604 |
| **C5 Standards & interoperability** | 0.461 | 0.581 | **0.442** | **0.668** |
| C6 Flexible infrastructure | 0.498 | 0.619 | 0.492 | 0.570 |
| C7 Adaptable workforce | 0.427 | 0.578 | 0.439 | 0.577 |
| C8 Legislation, ethics & compliance | 0.493 | 0.514 | 0.440 | 0.577 |
| C9 People-centred | 0.458 | 0.635 | 0.473 | 0.660 |
| **Mean** | **0.472** | **0.602** | **0.452** | **0.595** |

- **The health-data strategy leads the AI strategy on all nine domains in Canada**, exactly as in Africa. The set means are almost uncannily close: Africa 0.472 / 0.602 vs Canada 0.452 / 0.595. **The "health sector leads on every domain" pattern is structural, not continental.**
- **The interoperability signal is the sharpest and most usable.** Canada's health-data strategy scores **C5 = 0.668 — its single highest domain**. Both AI strategies are thin on C5 (Africa 0.461, Canada 0.442). So in **both** systems: the health side carries interoperability, the AI side does not absorb it. This directly reinforces Paper 1's AU standards-gap finding and gives the e-Health abstract a Canada-relevant hook — a country that built interoperability infrastructure first (Infoway, pan-Canadian standards) has a health-data strategy that reflects it.

## 3. Document linkage — Canada is measurably more connected, but only partly

| Signal | Canada | African benchmark |
|---|---|---|
| Shared-actor Jaccard (coarse proxy) | **0.333** | 0.00–0.25 |
| Shared actors | CIHI (once in each), Statistics Canada (in each) | usually one ministry |
| AI strategy names the health-data strategy | **Yes** — references a *"pan-Canadian health data platform designed to connect…"* | **No** (0 of 12) |
| Health-data strategy names the AI strategy | **No** | 2 of 12 (DRC, Senegal) |

**Canada is more wired than any African pair** — highest institutional overlap, and its AI strategy explicitly reaches toward the pan-Canadian health-data platform. But the linkage is **asymmetric in the same direction as Africa**: the AI strategy glances at health data; the health-data strategy does **not** name the AI strategy. Canada is *partially* connected, not cleanly connected.

---

## 4. What this means for the paper (both claims survive — and strengthen)

The benchmark resolves the "structural vs design choice" question **as both**:

1. **Structural.** The genre boundary (AI/1k) and the domain asymmetry (health leads every domain) **replicate in a G7 country**. Both are properties of how AI policy and health-data policy are *authored*, not of national wealth. This is a much larger claim than an African finding.
2. **Design choice.** Canada is still **more connected** (Jaccard 0.333; explicit platform reference; CIHI shared). Connectivity is therefore **improvable by design** — the actionable, Canada-facing result. The gap can be closed; it just isn't closed by default.

**The headline for Paper 2:** *the AI/health-data disconnect is structural — it reproduces in Canada — but it is not inevitable; a country that builds shared institutional ownership (CIHI) and cross-references its platform connects measurably more.*

---

## 5. Caveats to carry into the write-up (do not omit)

- **Benchmark of one.** Descriptive; no inference. Frame as a reference case, never as "n = 16."
- **Genre caveat on the Canadian health document.** Canada's "health-data strategy" is a **three-report EAG advisory series**, not a single ratified strategy document. That is itself a governance observation — Canada deliberated through an expert group; most African states have a single ratified strategy. Score is a fair use of the instrument, but the asymmetry of document type must be stated.
- **Thin health integration in the AI strategy.** Only **22** occurrences of "health" in a 13.5k-word AI strategy; health appears as one priority sector among many. Consistent with the low C5 score.
- **Coarse actor proxy.** The Canadian actor list is a hand-built 7-pattern list (CIHI, Infoway, StatCan, PHAC, Health Canada, CIHR, CADTH), matching the African shared-actor method's spirit but not its exact dictionary. Treat Jaccard 0.333 as directional, not precise.
- **AI-strategy PDF is the ISED *AI for All* full text.** Confirmed 13,483 words on disk.

## 6. Next steps

- Fold these numbers into §2 of the programme strategy (Canadian comparator).
- Draft the e-Health27 abstract off this (AU standards gap + Canadian interoperability replication), track **"In Support of Connected Health"**, Oral first choice. Deadline **20 Oct 2026, 17:00 PT**.
- Optional robustness: run the Canadian pair through the **operationalization** lever (Paper 1's six-lever measure) to test whether Canada's AI strategy is thin not just on interoperability language but on execution specificity — a same-instrument extension.
