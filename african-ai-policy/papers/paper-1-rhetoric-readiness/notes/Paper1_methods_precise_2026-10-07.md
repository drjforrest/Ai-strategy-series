# Paper 1 — precise methods description

**Date:** 7 Oct 2026 · **Basis:** the actual code in `src/` and the run scripts, not the prose in the roadmaps. Every parameter below is read from `src/config.py`, `src/preprocess.py`, `src/alignment.py`, `src/operationalization.py`, and `analyze_rhetoric_vs_readiness.py`.

---

## 1. Manuscript Methods (submission-ready)

### 1.1 Corpus
A corpus of **13 policy documents** was assembled: **12 national AI strategies** (Benin, Côte d'Ivoire, Egypt, Ghana, Kenya, Mauritius, Nigeria, Rwanda, Senegal, South Africa, Tanzania, Zimbabwe) plus the **African Union Continental AI Strategy** as a regional anchor. The corpus is **multilingual** (English and French; e.g. Côte d'Ivoire and Senegal are French-language). Two genre exclusions were applied a priori: Ethiopia (its digital-transformation documents are not an AI strategy — AI is not integral throughout) and Morocco (no full-text national AI strategy is publicly available). Both are retained in the repository as genre-contrast cases.

### 1.2 Text preparation
Each document was normalised before analysis: PDF artefacts removed (run-on page headers/footers, hyphenated line-breaks rejoined), and the frequent PDF misreading of the "AI" ligature as "Al" repaired ("Al governance" → "AI governance") while preserving genuine proper names. Documents were then segmented into **overlapping ~150-word passages with 20 words of carry-over**, discarding fragments under 25 words. Segmentation is paragraph-aware: whole paragraphs are packed until the 150-word ceiling, and only paragraphs exceeding that ceiling are hard-split on the sliding window.

### 1.3 Rhetoric measure — the WHO nine-component instrument
Each passage was embedded with the multilingual sentence-transformer **`paraphrase-multilingual-MiniLM-L12-v2`**, placing English and French in one semantic space, and L2-normalised so that a dot product equals cosine similarity. The nine core components of the **WHO *Global Strategy on Digital Health 2020–2027*** (C1–C9: leadership and governance; investment and operations; services and applications; integration and sustainability; standards and interoperability; flexible infrastructure; adaptable workforce; legislation, ethics and compliance; people-centred approach) were operationalised as the **measurement grammar**: the nine component descriptions were embedded with the same model, and every passage was scored against all nine.

Passage scores were aggregated to a document-level score per component using **`top_frac_mean`** — the mean of each document's strongest **10% of passages (floored at 3)**. This length-scaled aggregation was chosen deliberately over a fixed *top-k*: a fixed *k* means "best 5 of 46" beats "best 5 of 365" and systematically penalises long strategies, whereas scaling the passage count with document length puts short and long strategies on comparable footing.

**Output.** A 13 × 9 document-by-component alignment matrix (`outputs/alignment_scores.csv`).

### 1.4 Operationalization measure — a separate, transparent axis
Because the WHO-alignment measure captures *semantic* similarity, and every strategy shares the digital-policy register, a second axis was built to capture *operational* commitment. Six execution levers were scored by hand-audited, **bilingual (English + French)** lexicon/regex detectors: **timelines; budget; agencies; regulatory; monitoring; implementation**. Detectors were designed to be auditable and language-fair (an English-only lexicon would fabricate an "anglophone = more operational" artefact in a corpus with French-language strategies).

Hits were normalised per 1,000 words to remove length bias. The **primary index is a *breadth* measure** — the fraction of the six levers a strategy addresses at above-median intensity for the sample — chosen because it avoids the two failure modes of a naïve composite (per-1k density over-rewards terse implementation matrices; raw counts over-reward long documents). A secondary **`focus_index`** (mean of min–max-scaled lever densities) captures how execution-dense the prose is. Both are *within-sample relative* measures.

### 1.5 Rhetoric–readiness analysis and the circularity guard
The **same instrument** (identical model, chunking, and aggregation) was re-applied to score each strategy against the nine **Oxford Insights Government AI Readiness Index** dimension definitions, giving a *text-derived emphasis* score per country per dimension (`run_reference_alignment.py`). This was joined to the independently measured Oxford dimension scores (2024, or the 2021–2024 mean) for the overlapping countries.

Both axes were **z-standardised within each dimension across countries**, so both read as "relative to peers." The association between them was then estimated by **Pearson correlation per dimension**, plus a pooled correlation across all country-by-dimension cells.

**The circularity guard.** Two of the nine Oxford dimensions are scored *partly by reading the strategy text itself* — **Vision** (its "National AI Strategy" indicator) and **Governance and Ethics** (its national-ethics-framework desk-research indicator). Correlating our text-derived emphasis against those dimensions is **method agreement (reliability)**, not evidence that strategies track real capability. The seven remaining dimensions are built from independent secondary data (infrastructure, data availability, digital capacity, adaptability, technological maturity, innovation capacity, human capital) and constitute the **genuine rhetoric–reality test**. The two subsets are reported separately, with the independent subset as the primary result.

### 1.6 Results as implemented
- **WHO alignment:** all 13 entries engage the nine components broadly; national mean alignment 0.432–0.546.
- **Operationalization breadth** varied independently of alignment: Rwanda and Zimbabwe 0.833, Tanzania 0.667, versus 0.167 for Mauritius and Senegal.
- **Rhetoric–readiness (the guarded test):** pooled **r = −0.005** across **99 country-by-dimension cells (11 countries)**. Mean r on the **seven independent dimensions = −0.054**; mean r on the **two text-proximate dimensions = +0.164** (Vision +0.130, Governance and Ethics +0.199). The direction is as the guard predicts, but the association is **not statistically significant (exact permutation p = 0.083)** and is therefore reported as **exploratory**.
- **Durable, sensitivity-robust result:** the **AU Continental AI Strategy is markedly thin on standards and interoperability (C5) relative to the AU Digital Transformation Strategy**.

### 1.7 Reproducibility statement
All analysis is deterministic given the corpus. Cross-set comparison is valid only under a single semantic backend: the pipeline **hard-aborts** if `sentence-transformers` is unavailable and the lexical TF-IDF fallback would be used, because TF-IDF scores are not comparable with the semantic matrix. Scripts are run through the project's pinned environment (`.venv`, Python 3.12).

---

## 2. Condensed version (abstract / slide level, ~120 words)

> Thirteen AI strategies (12 national + the AU) were segment-embedded with a multilingual sentence-transformer (`paraphrase-multilingual-MiniLM-L12-v2`) and scored against the nine WHO *Global Strategy on Digital Health* components (top-10% aggregation). A separate, hand-audited bilingual lexicon measured six execution levers (timelines, budget, agencies, regulation, monitoring, implementation). The same instrument re-scored each strategy against the nine Oxford AI-Readiness dimensions, joined to independently measured readiness and z-standardised within dimension. A **circularity guard** separated two dimensions partly scored from strategy text (Vision; Governance and Ethics) from seven built on independent data. Pooled association was r = −0.005 (independent dimensions: −0.054; text-proximate: +0.164); not significant (permutation p = 0.083) and reported as exploratory.

---

## 3. Key parameters (for a reproducibility appendix)

| Parameter | Value |
|---|---|
| Corpus | 12 national AI strategies + AU = 13 entries; multilingual (EN/FR) |
| Embedding model | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` |
| Passage length | ~150 words, 20-word overlap, min 25 words |
| Reference framework (primary) | WHO GSDH nine core components (C1–C9) |
| Aggregation | `top_frac_mean`, top 10%, floor 3 |
| Reference framework (cross-walk) | Oxford AI-Readiness 9 dimensions, 2021–2024 |
| Rhetoric–readiness cells | 99 (11 countries × 9 dimensions) |
| Operationalization levers | 6 (timelines, budget, agencies, regulatory, monitoring, implementation) |
| Operationalization index | breadth = fraction of 6 levers above sample median |

---

## 4. Operationalization levers — methods table (per-lever examples)

| Lever | Example signals (EN + FR) |
|---|---|
| Timelines | target years (2023–2035), FY23/24, "by 20XX", "à l'horizon", Q1–Q4, phases, short/medium/long-term |
| Budget | currency amounts (US$/€/RWF/KES/NGN/ZAR/XOF…), "million/billion/milliard", budget/financing/investissement |
| Agencies | "Ministry of…", "ministère de…", Authority/Agency/Commission, "responsible for", "chargé de" |
| Regulatory | Act/Bill/Law/Decree/Regulations, "loi/décret/arrêté", legal/regulatory framework, "shall enact" |
| Monitoring | "monitoring and evaluation", M&E, indicator/KPI/baseline/milestone, "suivi-évaluation", cible |
| Implementation | "implementation/action plan", roadmap, procurement/tender/pilot/deployment, "plan d'action", "mise en œuvre" |

---

## 5. Precision issues to fix in the current prose

These are places where the existing descriptions are vaguer than the code, or where the number must be stated exactly:

1. **"11 countries / 99 cells," not 12.** Tanzania and the AU drop out of the rhetoric–readiness join (no Oxford readiness score). State this explicitly — a reviewer will check why the corpus is 13 but the correlation is 11.
2. **Name the aggregation.** "Top-10%" must always be followed by "(mean of each document's strongest 10% of passages, floored at 3)."
3. **State the z-standardisation.** Because both axes are standardised *within dimension*, r is a within-dimension association across countries — not a raw-score correlation.
4. **Document the permutation test.** `analyze_rhetoric_vs_readiness.py` computes the correlations but not p = 0.083; the permutation permutation implementation should be cited/located so the p-value is reproducible.
5. **Handle the Maturity outlier openly.** **Maturity (Technology Sector) r = +0.301** is the single strongest correlation and is an *independent* dimension — awkward for the "text tracks only text-proximate dimensions" story. It cannot be omitted; address it in the text.
6. **Human Capital is the weakest (r = −0.215)** among independents — worth naming, as it echoes the workforce finding that motivates Paper 3.
7. **Drop "maturity model typology" until it exists.** The roadmap describes a "typology of AI strategy maturity models" as a Paper 1 output; the current pipeline produces none. Describe the real outputs instead.
8. **WHO component scoring is not "qualitative content analysis."** Call it what it is: segment-level multilingual embedding scored against a fixed competency framework.
