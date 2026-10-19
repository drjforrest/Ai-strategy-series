# Health salience in AI strategies — a cross-cutting reading

**Date:** 6 Oct 2026 · **Method:** reproducible term-density scan (`outputs/sector_salience_african_ai.csv`, `outputs/canada/canada_sector_salience.csv`) · **Status:** descriptive finding, crude measure — see caveats.

Motivated by the observation that health integration in African AI strategies is low, and that AI crosses many sectors — some (fintech, edtech) with more political salience and an earlier start.

---

## 1. Health is a minor vertical in African AI strategies — confirmed

Sector-term density per 1,000 words, 12 national AI strategies (medians):

| Sector (term set) | Median /1k | Note |
|---|---|---|
| Government / public sector | **4.94** | dominant frame |
| Finance (broad: finance, banking, payments, investment…) | **4.54** | confounded — see caveats |
| Education (strict: education, learning, school, university) | **4.08** | |
| Training / skills | 2.96 | partly AI-workforce, not edtech |
| **Health (strict)** | **1.30** | |
| Agriculture | 1.42 | |

**Health sits at the bottom of the sector distribution** — roughly a third of the government, finance and education densities. The range is wide: **Mauritius 5.32/1k** (the clear outlier) down to **Côte d'Ivoire 0.00**; most strategies cluster between 0.4 and 2.8. The **AU Continental AI Strategy** fits the pattern (health 1.99, below education 4.79, finance 3.34, government 5.56).

**Canada reinforces it:** the *AI for All* strategy's health density is **3.71/1k — nearly three times the African median (1.30)**, but still **below** its own finance density (4.52). So health is a minor vertical in AI strategy **on both continents**; Canada simply weights it higher.

## 2. The mechanism: partly right, but fintech is not the standout

The claim "fintech has more political influence than health" is **directionally supported** but needs care:

- **"Fintech" as a literal term is rare everywhere** (median 0.24/1k — near-absent). The sector is discussed as *financial services / digital financial services / payments / financial inclusion*, not "fintech."
- The genuinely dominant "other" verticals are **government/digital-government** and **education/learning** — not fintech specifically. Education (strict) at 4.08/1k is ~3× health, and much of it is *learning and skills* language.
- Broad finance density (4.54) is inflated by **investment/funding** language ("investment in AI"), which is not the finance *sector*.

**Fairest statement:** in African AI strategies, **health is a second-tier vertical** behind government, education and the broad financial/investment frame — consistent with the hypothesis that health AI arrived later than the out-of-the-gate sectors, but the "fintech specifically" version overstates a term that barely appears.

## 3. Why it matters for the programme

- **It motivates Paper 3 directly.** If AI strategies barely address health, the workforce being trained for *health* AI is being trained for a policy afterthought — which is precisely the policy–capacity question Paper 3 asks.
- **It strengthens the CIS theory spine.** "Health AI is later to the game" implies less accumulated post-deployment monitoring capacity in health specifically — the computational-fidelity and algorithmovigilance capabilities CIS says matter. Sector lateness → governance immaturity.
- **It is a legitimate descriptive addition to Paper 2**, sitting alongside the AI-centrality and competency-overlap measures: health is not just thinly *linked* to AI policy; it is thinly *present* in it.

## 4. Caveats (do not present the ranking without these)

- **Keyword density, not semantic emphasis.** Crude but reproducible; it counts surface terms, not the weight a strategy gives a sector. Pair with the embedding instrument before publishing.
- **Confounds in two directions.** Broad finance overcounts (investment language); literal "fintech" undercounts (the sector is named differently). Education (strict) is the cleanest comparator to health.
- **"Training/skills" ≠ edtech.** Much education/training language concerns AI workforce capability, not the education sector as a vertical.
- **Health-adjacent terms excluded.** Public-health-only phrasing is captured, but "hospital," "pharmacy," "disease surveillance," etc. are not — a stricter health set would be *lower*, not higher.

## 5. Reproduce

```
./run.sh - <<'PY'
# sector-density scan; see outputs/sector_salience_african_ai.csv
PY
```

Full matrices: `outputs/sector_salience_african_ai.csv`, `outputs/canada/canada_sector_salience.csv`.
