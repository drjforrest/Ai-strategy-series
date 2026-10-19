# Policy attention vs capital allocation — a divergence

**Date:** 6 Oct 2026 · **Status:** exploratory synthesis — motivates a Paper 2 extension; not yet a measured finding · **Sources verified** (see §4).

Triggered by the observation that, although "fintech" barely appears in the African AI strategies, commercial capital on the continent is concentrated in fintech. Both are true — and they measure different things.

---

## 1. Two maps of the same territory

| Map | Fintech | Health | What it measures |
|---|---|---|---|
| **Policy text** (this repo; `outputs/sector_salience_african_ai.csv`) | literal "fintech" 0.24/1k; broad finance 4.54/1k | 1.30/1k | what strategies *say* |
| **Capital allocation** (Partech/AVCA 2024) | **~47–60% of equity funding** | **~3%**, and **falling** | where *money* goes |

**The two maps disagree.** In strategy text, health receives *more* stated attention than fintech. In capital, fintech receives roughly a twentyfold greater share. Policy salience and market salience are **decoupled** — and in different directions.

## 2. The verified capital picture (2024)

- **Fintech dominates and grew.** Partech: **60% of total equity funding**, the only sector to grow in both deal count (+16%) and funding (+59%). AVCA: **59% of capital**, 30% by volume. NTU/Disrupt Africa: 47%, up from 42% in 2023. Range ≈ **47–60%**, depending on denominator (equity vs equity+debt; tech-enabled vs startups).
- **HealthTech is small and contracting.** Partech: **US$65M in 2024, −70% YoY** (from $212M), 31 deals (−40%). Weetracker: healthcare/wellness/beauty **2.99%** of funding.
- **AI is rising — but riding fintech infrastructure.** AVCA: AI broke into the **top four** most-funded verticals. Partech: AI is "an enabling layer inside established business models (primarily fintech and logistics)," not a standalone sector. So on the continent, **AI capital ≈ fintech capital** — AI adoption follows payment rails (M-Pesa, MTN), exactly as the venture reports describe.
- **Development capital is being diverted elsewhere.** Weetracker: DFIs — the largest source of African VC — shifted toward **climate**, at the expense of logistics, healthcare, education and agriculture, whose **combined share dropped from 25%**.

## 3. Why this matters for the programme

1. **It supplies the missing third map.** The programme currently measures *policy → policy* connectivity (Paper 2). Adding *policy → capital* turns the thesis from "policy streams are unlinked" into the stronger **"policy, capital and capability are three uncoordinated maps."**
2. **It reframes the health-tech problem as structural.** HealthTech is not merely under-represented in strategy text; it is **commercially the hardest** (long regulatory cycles, low B2C willingness-to-pay, slow B2G procurement — the bottlenecks the venture reports name). Capital follows the shortest path to return; health is not it.
3. **It sharpens the CIS argument.** If AI capital concentrates in fintech, then health-specific **post-deployment monitoring and evaluation capacity** is proportionally starved — the computational-fidelity capability CIS says health systems need but rarely build. Capital concentration *predicts* governance immaturity in health AI.
4. **It gives Paper 3 a policy–capital–capacity triad.** A country can legislate AI, attract AI capital, and *still* train no health-informatics workforce. The quadrant figure gains a second axis.

## 4. Sources and corrections

**Do not cite the attached summary; its figures are off.** Corrected against primary reports:

| Claim in pasted summary | Primary report says |
|---|---|
| Fintech "~35–40% of capital" | **60%** of equity funding (Partech 2024) — summary **understates** |
| HealthTech "~5–10%" | **~3%**, and **−70% YoY** (Partech; Weetracker) — summary **overstates** and misses contraction |

Verified sources:
- Partech, *Africa Tech Venture Capital 2024* (23 Jan 2025) — fintech 60% equity; healthtech $65M, −70%.
- AVCA, *2024 Venture Capital in Africa Report* — financials 59% of capital / 30% volume; AI in top four.
- Weetracker, *Annual VC Report 2024* — healthcare/wellness/beauty 2.99%; DFI shift to climate.
- Briter, *Africa Investment Report 2024* — sector diversification framing.
- NTU-SBF / Disrupt Africa — fintech ~47%.

## 5. Caveats before this becomes a paper claim

- **Definitional mismatch.** "Fintech share" is computed differently across reports (equity vs equity+debt; sector tags vary). Report a range and name each source's denominator.
- **Scope.** These are **commercial venture** figures. They exclude government AI spending, donor/DFI grants to health, and public-sector digital-health investment — precisely where African health tech is often funded. The comparison is capital *structure*, not total health AI investment.
- **Different units.** Policy density is per 1,000 words; capital is dollars. The divergence is qualitative (direction), not a ratio to be reported.
- **One year.** 2024 is a contraction year for healthtech; single-year snapshots are volatile. Trend across 2021–2025 before claiming a durable gap.
- **Not yet in the pipeline.** This synthesis is drawn from external reports, not the repo's own instrument. To become a Paper 2 result it needs a small, curated capital table (year × sector × source) committed to the repo like the corpus.

## 6. Suggested next step

Build `data/capital/african_ai_capital_by_sector.csv` (2021–2025, per source, with denominators) and add a **policy-attention vs capital-allocation** panel to Paper 2 — the strongest form of the programme thesis.
