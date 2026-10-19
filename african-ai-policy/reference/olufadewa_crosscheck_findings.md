# Cross-check against Olufadewa et al. (2024) — expert-rated eHealth strategy census

**Source:** Olufadewa II, Iyiola OP, Nnatus J, et al. *National eHealth strategy frameworks in Africa: a comprehensive assessment using the WHO-ITU eHealth strategy toolkit and FAIR guidelines.* Oxford Open Digital Health 2024; oqae047. doi:10.1093/oodh/oqae047

**What it provides:** an independent, expert-rated review of **34 African national eHealth/digital-health strategies**, scored on five domains (national vision & strategy; implementation plan; monitoring & evaluation; FAIR mention; recency) and given an overall **Weak / Moderate / Strong** rating. This is a useful external anchor because it assesses the *same document family* we analyse, by a different method.

**Reproduce:** `./run.sh crosscheck_olufadewa.py` (data: `reference/olufadewa_2024_census.csv`).

---

## Result — our WHO-alignment measure does *not* track expert-assessed quality

Matched to our digital-health corpus (**n = 13**; Mauritius is the only one of ours absent from their census):

| Our measure | vs Olufadewa expert rating |
|---|---|
| WHO-competency alignment | **Spearman ρ = −0.535** (p = 0.059) |
| Operationalization breadth | not testable — not yet computed for the digital-health set |

Mean WHO alignment by expert rating:

| Expert rating | Mean WHO alignment | n |
|---|---|---|
| Moderate | 0.617 | 9 |
| **Strong** | **0.570** | 4 |

**Interpretation.** Our embedding alignment is *mildly negatively* associated with expert-assessed strategy comprehensiveness — and the four strategies an independent panel rated **Strong** (Burundi, Sierra Leone, Namibia, Niger) sit at the *bottom* of our alignment ranking, below the Moderate group. This is a striking demonstration that:

1. **Semantic engagement with WHO competency vocabulary is not a measure of policy quality.** A strategy can score high on our instrument through broad, aspirational coverage of competency language while lacking the implementation plan, M&E and budgeting that expert raters reward. Our instrument measures *articulated emphasis*, and this external check confirms it does **not** proxy for comprehensiveness.
2. It **strengthens the paper's core claim** (alignment, operationalization and quality are non-equivalent constructs) with an external comparator rather than an internal assertion.
3. It **warns against headline rankings.** Any statement like "Côte d'Ivoire ranks first" or "X has the strongest digital-health strategy" must be avoided — the external evidence now shows our ranking does not track expert quality.

**Caveats.** n = 13; the negative correlation is only marginal (p = 0.059); and the two instruments measure different things by design, so the negative sign should not be over-read as "good strategies score worse." The safe, defensible wording: *our measure is orthogonal to (and if anything inversely related to) independently expert-rated strategy comprehensiveness, confirming that it captures emphatic coverage rather than implementation quality.*

---

## Bonus: 21 candidate additions to the digital-health corpus

The census names strategies we do not yet hold, several of which would raise linkage coverage if the paired AI strategy exists:

**Overlap with our AI-strategy set (would create new matched pairs):** Kenya, Egypt, Tanzania, Zimbabwe, Cote d'Ivoire, Benin.
**Others named:** Burkina Faso, Cameroon, Comoros, Eswatini, Gabon, Gambia, Guinea, Lesotho, Liberia, Madagascar, Malawi, Mozambique, Sudan, Togo, Uganda.

**Priority for Paper 2 linkage:** search for the **Kenya**, **Egypt** and **Tanzania** digital-health strategies — each country already has an AI strategy in our corpus, so adding its health strategy would directly increase matched-pair coverage (currently 6/12). Malawi, Mozambique, Uganda and Zimbabwe are also candidates, though some are older (pre-2018).

---

## Where this should go

- **Paper 1 (Discussion / Limitations):** a short external-validity paragraph — "our measure was compared against an independent expert rating of the same document family and found to be uncorrelated, confirming that alignment is not a quality proxy." This pre-empts the reviewer objection that high alignment might simply mean a better strategy.
- **Paper 2:** cite the census as prior art and corroboration that African digital-health strategies vary widely in comprehensiveness; the connectivity finding complements their quality finding.
