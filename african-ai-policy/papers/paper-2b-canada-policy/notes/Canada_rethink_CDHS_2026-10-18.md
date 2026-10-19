# Rethinking the Canadian study: public expectations, policy and education

18 October 2026. Feasibility assessment and proposed abstract direction, not a completed national alignment study. Existing manuscripts and source workbooks remain unchanged.

## Recommendation

Rebuild the Canadian question around the capabilities required to make health AI accountable to patients. Use the Canadian Digital Health Survey (CDHS) to identify public expectations and reported experiences; policy documents to identify responsibilities and mechanisms; and the programme inventory as a sampling frame for examining publicly documented educational provision. Do not merge the three into a numerical readiness index.

Proposed question: **How are public expectations for responsible health AI reflected in Canadian policy commitments and publicly documented health-informatics education?**

The study must permit alignment as a finding. It should not start from the conclusion that policy or education has failed. A possible contribution is identifying where the same capability is described differently, where operational responsibilities are explicit, and where the evidence is insufficient to assess translation into practice.

For the imminent conference, use a bounded policy–survey analysis unless sufficient curriculum evidence can be verified. The three-source design is the stronger longer-term direction, but the supplied education workbook is not yet a curriculum dataset.

## What was actually inspected

### Survey

Source: `/Users/j.forrest/dev/projects/data-science/2025_cdhs_table.xlsx`.

232 worksheets of aggregate cross-tabulations, with weighted proportions, weighted bases and unweighted counts. They are not respondent-level records. The national base for Q33, Q35, Q37 and Q38 is 11,311. The [official methodology](https://insights.infoway-inforoute.ca/2025-digital-health-survey-methodology) dates fieldwork to February 27–March 27, 2026 despite the 2025 survey label; it describes an online nonprobability panel weighted by region, age and gender. Conventional probability-sample margins of error are not appropriate.

Verified illustrative estimates, calculated as 100 × the indicated workbook values:

- Q33!B7: 56.9% trust AI scribes to document information accurately but believe human oversight is still needed. Q33!B6: 7.1% trust fully. Q33!B8: 25.0% do not trust; Q33!B9: 11.0% are unsure.
- Q35!B6: 50.9% would choose AI scribes in future encounters. This is preference, not actual use.
- Q37!B6: 24.3% report ever seeking chatbot medical advice instead of contacting a health professional. This does not establish harm, unmet need or the reason for that choice.
- Q38!B7+B9: 22.5% mostly/completely trust chatbot health information. This is a separate marginal distribution; it cannot identify whether the people reporting substitution are those who distrust chatbots.
- Q30!B7: 37.7% report not being informed but wanting to be informed about provider scribe use. Its unweighted base is 4,105, not 11,311. The exact questionnaire routing was not obtained, so this is excluded from any proposed national headline. Q30 measures notification, not consent. Q31 has a smaller base again (1,734); do not conflate the items.

Item stems were checked against the [official question index](https://insights.infoway-inforoute.ca/data_table_2025). Do not interpret worksheet IDs from answer labels alone. Retain uncertainty categories; do not renormalize them away. Do not add response percentages across separate multiple-response items to estimate people.

### Education

Source: `/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/Documents/Private Northeastern/99_Archive/23-Aug-26/Program Administration/MSHI/Background/Market Comparison/Canada-Health-Informatics-Digital-Health-Programs-Workbook.xlsx`.

The workbook describes itself as a July 20, 2026 market-comparison inventory. Recounting populated institution rows reproduces 91 entries: 46 graduate, 10 undergraduate, 35 professional-diploma entries. Status labels total 66 Active, 9 Paused/Suspended, 3 Discontinued and 13 Adjacent/Borderline. These are verified workbook counts, not verified current national programme totals.

Its strengths are programme URLs, credential and location fields, focus summaries and explicit uncertainty notes. Its limitations matter to the proposed inference:

- Rows mix full degrees, streams, research fields, paired MSc/PhD offerings, certificates and feeder pathways. Define the unit before counting programmes.
- The graduate category includes certificates and diplomas. The diploma category includes short courses and feeder certificates. Analyse actual credential types separately.
- The inventory spans HI, HIM, digital health, precision health, bioinformatics and general adjacent programmes. A denominator of 91 would not describe a coherent HI curriculum sample.
- Focus-area prose is not an exhaustive syllabus or evidence of assessment. Absence from a summary cannot mean absence from teaching.
- Programme counts do not measure graduate production, workforce supply or competence. Cohort/throughput information is not sufficiently established for those claims.
- Some entries explicitly flag old calendars, uncertain status or aggregator sources. The stated special BC completeness pass means geographic differences may partly reflect search intensity.
- The reported scope and comprehensiveness are claims of the source workbook, not independently established facts. Its market-comparison instructions do not govern this research.

A current [BCIT programme page](https://www.bcit.ca/courses/digital-health-programs/) advertises an AI course, and the [UVic MSc page](https://www.uvic.ca/health/hinf/graduate/masters/health-informatics/index.php) remains available. These are limited spot checks, not validation of the whole inventory. They also caution against assuming Canadian programmes lack AI content.

### Policy and previous framing

Inspected the existing reframe memo, competency–demand design memo, Canadian policy source text and `paper2b_canada_ecosystem/out/commitments_raw.csv`. The latter contains 609 extracted rows: 594 labelled DH_foundation and 15 AI_in_health; 11 rows have anchor_ok other than True. Those extraction flags do not establish conceptual validity or independent commitments.

The earlier analysis risks confusing documentary visibility with implementation. Strategies, principles and funding agreements have different functions; differences in dates, actor names and citations can reflect genre and publication year. A time-limited agreement is not evidence that the underlying capability expires. An omitted citation is not evidence of organisational disconnection. Treat previous figures as descriptive outputs requiring source and construct review, not findings to preserve at all costs.

The [AI4H principles](https://www.canada.ca/en/health-canada/corporate/transparency/health-agreements/pan-canadian-ai-guiding-principles.html) already address consent, safety/oversight, transparency and AI literacy. That is evidence of thematic correspondence with survey concerns, not proof of successful implementation. Conversely, the survey does not establish that national policy has failed.

## A defensible integration design

Use a small, explicit crosswalk. Begin with human oversight, notification/consent, and AI literacy. Keep patient-operated chatbots distinct from clinician-operated scribes; their responsibilities differ. Broader equity and cultural-safety questions warrant appropriate conceptual and community expertise rather than opportunistic subgroup comparisons.

For each domain retain three different evidence types:

1. **Public evidence:** item wording, population/routing, weighted response distribution, unweighted base and uncertainty.
2. **Policy evidence:** exact passage, document type/date, responsible role or organisation, specified action, operational mechanism and monitoring provision. Generic principles and operational guidance must be distinguishable. Mark out-of-scope documents separately from absence.
3. **Educational evidence:** current programme/course source, required versus elective status, explicit learning outcome, assessment evidence and source accessibility. Use “explicitly documented”, “related but nonspecific”, “not located in reviewed materials”, and “insufficient documentation”. These are not a numerical competence scale.

The common unit is the capability domain; the underlying units remain survey respondents, policy passages and programme/course documents. Present a joint evidence display, not a statistical row join. Do not correlate province-level programme counts with survey attitudes: programme location is not training exposure, online provision crosses borders, and many confounders remain.

Before coding, fix eligibility, corpus cutoff and search procedure. Pilot the definitions on a deliberately varied subset; have two researchers independently code a subset and resolve differences. Record negative cases and inaccessible materials. Treat topic selection after inspecting the survey as exploratory. Assess curriculum content only from direct documentation; verify apparent absence with programme information where feasible.

## Novelty and scope

The survey percentages are already publicly available. [Chandrasekaran and colleagues, JMIR 2025](https://www.jmir.org/2025/1/e77501) analysed CDHS2023 AI attitudes, consent and associated characteristics. A newer trust percentage alone is a weak contribution. The proposed added value is an auditable comparison between public expectations, assigned policy responsibilities and explicit educational outcomes. A broader literature search is still needed before claiming novelty or a first national study.

This offers a Canada-internal contribution to the series: examining translation from public expectations and formal commitments into documented preparation for practice. It does not require an international comparator and does not claim that Canadian HI programmes are responsible for all public AI literacy or every clinician's practice.

## Abstract direction and completion gates

Working title: **From public expectations to professional preparation: responsible health AI in Canada**.

Purpose: examine whether oversight, transparency and AI-literacy expectations have identifiable counterparts in policy and education.

Methods: descriptive secondary analysis of weighted CDHS tables, combined with a reproducible document analysis. Specify exactly which policy instruments and education records were actually coded; label a pilot as a pilot.

Results available now: survey estimates above; educational inventory composition; thematic correspondence in AI4H. These support feasibility, not a national education deficit or operational policy gap. The completed abstract needs the actual crosswalk results and denominators from the selected document sample. Do not insert projected findings.

Implications to test: where requirements are explicit, they can inform training and implementation; where public documentation is insufficient, the finding is an evidence gap requiring verification. Recommendations should follow observed patterns, including alignment.

The [e-Health27 call](https://www.e-healthconference.com/e-health-27/abstracts/) closes October 20, 2026 at 5 p.m. Pacific. The [official template](https://www.e-healthconference.com/wp-content/uploads/2026/09/e-Health27_Abstract-Submission_Template.pdf) allows a 20-word title, 75-word summary and 500-word structured body. e-Health26 has already occurred. Given the short interval, a bounded policy–survey paper is more defensible than promising a completed national curriculum assessment. Do not let the deadline convert this feasibility assessment into asserted findings.

## Filing recommendation

Keep both supplied originals unchanged until the study scope is settled. The CDHS workbook belongs in shared Canadian source data because both policy and education work may use it. The education workbook should remain an attributed seed inventory, with a separate research derivative that excludes internal market-comparison commentary and adds source dates, eligibility and evidence fields. Record hashes and provenance when making those copies. Do not move the private administrative original into a research repository by default.

## Confidence

High: inspected cell values, inventory counts and aggregate-data limitations. Moderate: feasibility of the proposed integration and critique of the existing framing. Unresolved: national inventory completeness, current programme status, detailed survey routing, curricular coverage, full policy operationalisation and originality against the wider literature.
