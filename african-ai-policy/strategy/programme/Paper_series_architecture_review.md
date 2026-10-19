# Paper-series architecture — review and connectivity results

**Date:** 30 Sep 2026 · **Basis:** repo as authoritative (Ethiopia excluded; 13 national + AU).

## 1. Verdict on the architecture

The three-way split — *explicitly-AI strategies* (rhetoric+readiness) → *digital-health strategies* (WHO framework, connectivity) → *workforce/accreditation* (primary data) — is sound, and it is the split the data independently supports. Genre, not geography, is the correct discriminator, and you found it by hitting the same wall three ways (Ethiopia's density, the second paper's overlap, the third paper's object). That is convergent validity, not coincidence.

One shared assumption to make explicit: **Paper 1 and Paper 2 use the same framework** (the nine WHO *Global Strategy on Digital Health* core components). That is fine — it is "same instrument, new corpus and new question" — but it means Paper 2 is not introducing a new framework, only a new contrast. Be transparent about that; don't let it read as a fresh instrument.

## 2. A premise to correct before Paper 3 is built on it

You wrote that in the digital-health strategies *"the workforce mapping is particularly weak in the region."* The document-level data do not support that:

| WHO domain | AI strategies (n=13) | Digital-health strategies (n=3) | Direction |
|---|---|---|---|
| C3 Services & applications | 0.446 | 0.639 | DH leads |
| C4 Integration & sustainability | 0.492 | 0.645 | DH leads |
| C9 People-centred | 0.459 | 0.613 | DH leads |
| C1 Leadership & governance | 0.488 | 0.638 | DH leads |
| C6 Flexible infrastructure | 0.502 | 0.591 | DH leads |
| **C7 Adaptable workforce** | **0.428** | **0.572** | DH leads |
| C5 Standards & interoperability | 0.462 | 0.548 | DH leads |
| C2 Investment & operations | 0.492 | 0.504 | ~equal |
| **C8 Legislation, ethics & compliance** | **0.493** | **0.475** | **AI leads** |

Workforce (C7) is **not** the weakest digital-health domain — it sits mid-pack at 0.572. The genuinely weak domains in the *digital-health* set are **C8 (legislation/ethics, 0.475)** and **C2 (investment, 0.504)**. What workforce *is* is much weaker in the **AI strategies** (0.428, the lowest of all nine AI domains).

**Implication for Paper 3:** the "workforce is under-mapped" claim is strongest as an *AI-strategy* finding and cannot be established from strategy *text* at all for the digital-health set (n = 3, and the scores are moderate, not low). It will have to come from your **program/curriculum extraction sheet** — which is exactly the primary data you have started. Good news: that makes Paper 3's contribution load-bearing rather than a spin-off, and it means you should *not* pre-commit to "workforce is the weak one" until the sheet says so.

Also note the mirror-image finding, which is more interesting than a simple gap: the AI and digital-health streams emphasise **different parts of the health system** — health documents lead on services/integration/people-centredness, AI documents lead on *legislation and ethics*. That asymmetry is a Paper-2 result in its own right.

## 3. Paper 2 connectivity — what is now reproducible

New script `analyze_connectivity.py` → `outputs/connectivity/`. It reads the authoritative primary scores and re-scores the digital-health set with the same `paraphrase-multilingual-MiniLM-L12-v2` backend. It **hard-aborts** if the environment falls back to TF-IDF, because lexical scores are not comparable with the primary matrix — this is the trap the old secondary run may have fallen into.

Reproducible now:
- **(i) AI centrality:** AI strategies 19.3–46.9/1k (median 35.5); digital-health 0.14–1.11 (median 0.27); Uganda 1.44. No overlap → hard genre boundary.
- **(ii) Competency overlap:** digital-health strategies 0.565–0.601 per country, above every AI strategy (0.432–0.546); domain asymmetry above.
- **(iii) Document linkage:** **not built.** Citation/reference/shared-actor overlap is the genuinely new Paper-2 method and the gating task.

Environment note: the *active* `python3` is 3.9 with **no** sentence-transformers; the project's `.venv/bin/python` (3.12) has it. Run pipeline scripts with `.venv/bin/python`, or the fallback silently changes the method.

## 4. Small corroboration

The AU Digital-Transformation-Strategy comparison in the manuscript (mean 0.5613 vs AU AI 0.4573) **is** reproducible from `_verify/dts_scores.csv` (mean = 0.5613 exactly), so that first-class finding stands. `dts_scores.csv` merely ends at C9 without a trailing newline, so `tail` looked like EOF — cosmetic, not a data problem.

## 5. Recommended next actions

1. Run `.venv/bin/python analyze_connectivity.py` after any corpus change; treat `outputs/connectivity/` as the Paper-2 numbers.
2. Build measurement (iii) — document linkage — or Paper 2 stays an embedding study on n = 3.
3. Decide explicitly whether Paper 2 keeps the WHO nine-component framework or adopts a distinct *individual-competency* framework. If it keeps WHO, its novelty must rest on the connectivity question and linkage method, not the framework.
4. Let the Paper-3 extraction sheet decide which competency is weakest; don't inherit the assumption.
