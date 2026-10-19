# Paper 2b — Canadian policy ecosystem

## Current design (19 Oct 2026)

**Curriculum–policy alignment.** The study compares publicly documented Canadian health-informatics/HIM programme curricula with the Canadian national digital-health and AI policy corpus. It uses the instruments from Paper 1 (same multilingual embedding model, top-10% aggregation, AI-term dictionary). The primary reference framework is the Digital Health Canada HIP Competencies (2022; 7 domains, 55 statements; `data/dhc_competencies/`). WHO C1–C9 is a secondary reference, kept for continuity with Paper 1. Target is the e-Health27 abstract (deadline 20 Oct 2026, 17:00 PT).

- Protocol: [notes/Paper2b_curriculum_policy_protocol_2026-10-19.md](notes/Paper2b_curriculum_policy_protocol_2026-10-19.md)
- Curriculum sources: `outputs/2026-10-18-canada-schema/Canadian_HI_HIM_Curriculum_Source_Package` (114 programme entries; URLs and metadata only)
- Page retrieval: `paper2b_canada_ecosystem/curriculum/fetch_curriculum_sources.py` → `paper2b_canada_ecosystem/raw/curriculum/`

These earlier framings are superseded for the conference submission and retained for reference: the policy-ecosystem/SNA framing (abstract v0.3) and the CDHS + education option (`notes/Canada_rethink_CDHS_2026-10-18.md`).

## Folder layout

manuscript/ is the 19 October working draft, “Are Canadian health informatics programmes teaching what digital health policy needs?”, with the edited and tracked Word files. Page renders from that editing session are in manuscript/_renders/. conference/ links to the earlier v0.3 abstract. archive/ retains v0.1 and v0.2 with their associated versioned checks. notes/ contains verification notes, framing assessments and the current protocol. analysis/ links to the ecosystem scripts, raw sources and outputs at the series root (`paper2b_canada_ecosystem/`). earlier-canada-benchmark/ retains the earlier comparator work.

## Contents

- [analysis](analysis/)
- [archive](archive/)
- [conference](conference/)
- [earlier-canada-benchmark](earlier-canada-benchmark/)
- [manuscript](manuscript/)
- [notes](notes/)
