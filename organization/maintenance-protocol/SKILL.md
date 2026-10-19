---
name: ai-strategy-series-maintenance
description: Maintain Jamie Forrest's AI strategy research programme folder organization, file new paper and strategy materials, and preserve shared analysis dependencies at /Users/j.forrest/dev/projects/data-science/ai-strategy-series. Use during substantive work in this project or when asked to organize its papers; do not apply to unrelated research folders.
---

# AI strategy series maintenance

Jamie asked Codex on 18 October 2026 to take responsibility for maintaining this project's organization. Keep relevant new and revised materials organized as part of authorized project work; routine filing does not need another confirmation. This is an ongoing working convention, not a scheduled monitoring task or permission to change scientific decisions, delete materials, publish, or contact collaborators.

Project root: `/Users/j.forrest/dev/projects/data-science/ai-strategy-series`.

## Establish current context

Read the root `README.md`, `strategy/README.md`, and the affected paper's `README.md`. Inspect current paths and Git status in each affected nested repository before changing files. The root was not a Git repository at initial organization; `african-ai-policy` and `digital-health-canada` were separate repositories with existing uncommitted changes. Verify this rather than assuming it remains true.

The map below records the accepted 18 October structure. Later explicit user decisions supersede it. Read document contents and corrections, not just names or modification times, when routing ambiguous work.

| Folder under `papers/` | Scope |
|---|---|
| `paper-1-rhetoric-readiness` | BMJ Global Health manuscript; AI policy rhetoric, readiness, methods, tables and figures |
| `paper-2-policy-connectivity` | African AI versus digital-health policies, connectivity/linkage analyses and HIMSS materials |
| `paper-2b-canada-policy` | Canadian policy ecosystem, e-Health abstracts and number-verification/framing notes |
| `paper-3-workforce-capacity` | Programme/curriculum census, competency framework, responsible-AI overlay and two-system design |
| `paper-4-policy-capital` | Exploratory investment and policy–capital work; do not assume a completed manuscript |
| `canada-competency-demand` | Emerging Canadian standards–employer-demand–education study; no series number assigned |

`strategy/` holds programme plans, concepts, roadmap and presentation links. `shared-resources/` provides links to shared sources.

## Context that prevents misfiling

- `hi-africa-partnerships` is dormant July partner-scoping work with reusable registers, networks, figures and JAMIA drafts. The 15 October `Paper3_vs_hi-africa-partnerships_relationship` note explicitly supersedes the earlier overlap audit. Do not promote that JAMIA draft to an active paper or declare a competing-submission problem without evidence of revival. Preserve register verification caveats when reused; do not merge data merely to tidy folders.
- Paper 3's Canadian arm tests framework portability; it is distinct from Paper 2b's Canadian policy analysis and the separate Canadian competency–demand proposal.
- September/early-October roadmap corpus counts and comparator assumptions predate later changes. The 16 October Paper 1 Lesotho change note postdates the 14 October co-author manuscript. Treat these dates as a guide to the recorded correction, not proof that a draft has since been reconciled.
- Paper 2b retains alternative/revised framing assessments. Filing is not authority to select a scientific design. The Canadian demand memo records a resolved prior-art concern alongside older text: read the correction before repeating a blocker.
- File names containing FINAL, venue names and proposed deadlines do not prove submission or acceptance. Research results and current publication status require their own evidence.

## Preserve the working layout

Actual organized documents live in `african-ai-policy/papers/` and `african-ai-policy/strategy/`. The top-level `papers/<workstream>` entries and `strategy` are relative symbolic links to those folders. Paper asset links point to existing datasets, outputs or repositories. `african-ai-policy/drafts/` holds compatibility links for the moved documents.

Keep one canonical working copy. File new writing directly in the appropriate physical paper folder (for example `manuscript`, `protocol`, `design`, `notes`, `tables`, `conference` or `scoping`), using existing conventions where they fit. Add a new category only when it makes navigation clearer. Put earlier versions or explicitly superseded assessments in `archive`, retaining recognizable version/date names. Never overwrite a distinct version silently.

Leave source corpora, analysis code, outputs, environments, credentials, `.git`, verification history and backup trees in their existing repository locations unless the actual task requires changing them. Link to shared assets rather than copying them into each paper. Run analyses from the repository directory expected by their scripts.

When adding symbolic links, compute relative targets from the **resolved physical parent directory**, not a top-level alias path. Test both the direct and top-level entry paths. A wrong relative target through the `strategy` alias was caught and fixed during initial organization.

For an existing-file move, inspect references first. Preserve a compatibility link where scripts or historical references depend on the old path; new files do not automatically need legacy links. Watch for software that saves by replacing a symlink rather than following it: detect divergent regular files at legacy paths before consolidating anything.

## Record and verify maintenance

- Before moves, record original paths and SHA-256 hashes; refuse collisions. For substantial batches, add a dated manifest under root `organization/`, following `moves-2026-10-18.json`. Do not rewrite the historical manifest to imply it describes later file contents.
- Verify each moved file's content is unchanged, compatibility links reach the intended destination, and newly created navigation/Markdown links resolve. Do not follow directory symlinks recursively when walking the tree.
- Refresh the affected paper index and root/strategy index only where scope or navigation changed. Preserve uncertainty and distinguish historical notes from current decisions.
- Report the organization result and actual checks briefly. Do not claim scientific validation from filesystem checks; do not rerun expensive pipelines solely for a document move.
- The initial manifest covered 32 moved items containing 31 files; hashes matched and 53 symbolic links resolved. This is historical evidence, not a permanent expected file count.

Keep this skill aligned with explicit later user decisions. Update Codex memory only when the user explicitly requests a memory update; ordinary maintenance does not authorize memory writes.
