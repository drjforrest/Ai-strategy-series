# CIS section — edited for internal consistency

**Date:** 7 Oct 2026 · **Edit principle:** the section previously defined CIS two ways at once — the opening paragraph used the **AIM-IS** direction (*integrating computational methods into implementation science*) while the later line used the **CIS** direction (*implementation science adapting to computational interventions*). This edit makes the whole section advance the differentiated CIS thesis, so it cannot be read as AIM-IS renamed.

---

## What is Computational Implementation Science?

**Computational Implementation Science (CIS)** is the implementation science of *computational* interventions: the study of how tools whose behaviour can change **after deployment** — model versions, decision thresholds, input data distributions, hardware, and external/vendor dependencies — are adopted, integrated, monitored, adapted, governed, sustained, and ultimately **retired** in real-world health systems.

The defining condition is not that software is present, but that **computational change can alter the identity, performance, or distributional effects of the intervention over time.** A stable rule-based reminder delivered through an electronic health record is adequately studied with conventional digital-health implementation approaches; a triage model that is retrained, shifts its thresholds across versions, or performs unevenly across subgroups and settings requires additional constructs and measures.

Established implementation frameworks — CFIR, RE-AIM, Proctor's implementation-outcomes taxonomy, NASSS, and the Dynamic Sustainability Framework — remain essential. CIS asks what must be **added** when the intervention is not a fixed innovation, protocol, or technology domain. Three gaps are especially important:

- **Computational fidelity** — not only whether the intervention was delivered as intended, but whether the deployed version, threshold, input pipeline, and model behaviour match the evaluated specification.
- **Computational maintenance** — not only continued delivery, but sustained *performance* under changing populations, data, and workflows (calibration, drift, subgroup effects).
- **Designed exit** — sustainment rarely treats withdrawal as an implementation outcome, yet computational interventions may require recalibration, restriction, replacement, or retirement.

**CIS complements and does not replace implementation science, and it is distinct from AIM-IS.** The distinction is directional: **AIM-IS asks how computational methods can strengthen implementation science; CIS asks how implementation science must adapt when the object being implemented is computational.** The two are siblings, not rivals.

**Core contribution.** CIS supports evaluation of not only whether an intervention works, but:

- whether the system is *structurally capable* of supporting it;
- whether policy intent is *realistically implementable*;
- whether ecosystem components (policy–workforce–capital) are *aligned*.

---

## Change notes

| # | Original | Edited | Why |
|---|---|---|---|
| 1 | "extends traditional implementation science by integrating computational, data-driven, and AI-enabled methods" | "the implementation science of *computational* interventions … behaviour can change after deployment" | Removes the AIM-IS contradiction; adopts the differentiated thesis. |
| 2 | "Unlike traditional implementation science, which often relies on qualitative evaluation / small-scale studies / retrospective analysis" | Dropped; replaced with the stable-reminder vs changing-model contrast | The old framing is a strawman (implementation science is heavily quantitative and mixed-methods) and would irritate an IS reviewer. |
| 3 | "CIS introduces: … integration of AI-derived insights into implementation evaluation" | Replaced with the three *gaps* (fidelity, maintenance, exit) | "AI-derived insights" again describes AIM-IS, not CIS. The three gaps are the actual novel constructs. |
| 4 | "CIS does NOT replace implementation science" (then AIM-IS distinction) | Kept, and **merged with** the AIM-IS line | The two sentences were saying the same thing; joining them makes the directional distinction land. |
| 5 | Core contribution bullets | Kept verbatim | Already correct and consistent with the CIS thesis. |

**Net:** one principled change — the section now defines CIS once, consistently, in the direction the commentary argues.
