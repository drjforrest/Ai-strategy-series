# AI strategy research programme

Analysis code for a programme of studies measuring how national artificial
intelligence strategies and digital health policy engage digital-health and
health-informatics competency frameworks.

The method is common to every study: policy, strategy or curriculum text is
cleaned, split into passages, embedded with a multilingual sentence-transformer,
and compared by cosine similarity against the statements of a normative reference
framework — the WHO Global Strategy on Digital Health components, or the Digital
Health Canada Health Informatics Professional (HIP) Core Competencies. Each
document's score for a reference statement is the mean of its strongest-matching
passages. Full method, parameters and caveats are in
[african-ai-policy/README.md](african-ai-policy/README.md).

## What is in this repository

Code, generated outputs and written documentation.

| Folder | Contents |
|---|---|
| [african-ai-policy](african-ai-policy/) | The analysis pipeline: `src/` package, the `run_*.py` and `analyze_*.py` entry points, plotting scripts, and `outputs/` with the generated score matrices, convergence tables, sensitivity results and figures |
| [african-ai-policy/_verify](african-ai-policy/_verify/) | Verification scripts and their outputs — the checks run against each result before it was reported |
| [african-ai-policy/papers](african-ai-policy/papers/) | Per-study protocols, methods notes and verification memos |
| [digital-health-canada](digital-health-canada/) | A source-monitoring agent for Canadian digital health publications, and deck-generation scripts |
| [hi-africa-partnerships](hi-africa-partnerships/) | Dormant scoping work on health informatics training partnerships in Africa: registers and notes |
| [sources](sources/) | Manifest and checksums for the source documents the analysis reads |
| [organization](organization/) | Records of two repository reorganisations, with path and checksum manifests |

`papers/` and `strategy/` at the repository root are relative links into
`african-ai-policy/`.

## What is not in this repository

**Source documents.** National AI strategies, digital health and eHealth
strategies, competency frameworks, readiness-index datasets and commercial market
reports are third-party publications under differing licences, at least one of
which prohibits reproduction without written permission. They are not
redistributed here. [sources/SOURCES.md](sources/SOURCES.md) explains how to
obtain them, and `sources/corpus_manifest.csv` gives the local path, title,
issuing body and SHA-256 of each file used, so an independently obtained copy can
be confirmed identical to the one behind the published results.

**Derived full text.** Extracted plain-text corpora, passage tables and parsed
competency statements reproduce the substance of those documents verbatim, so
they are withheld on the same grounds. The code regenerates them from the source
files.

**Unpublished manuscripts.** Draft manuscripts, tracked-change reviews and
co-author presentation decks are not published here.

## Running the analysis

See the quickstart in [african-ai-policy/README.md](african-ai-policy/README.md).
Source documents must be in place first; the pipeline aborts rather than scoring
an incomplete corpus.

## Licence and citation

Code is MIT-licensed; written documentation and generated outputs are CC BY 4.0.
See [LICENSE](LICENSE). Neither licence covers the third-party source documents.
Citation metadata is in [CITATION.cff](CITATION.cff).

## Provenance

This repository was reorganised on 18 October 2026 and tidied for publication on
11 November 2026. [organization/moves-2026-10-18.json](organization/moves-2026-10-18.json)
records original and organized paths with SHA-256 hashes, and
[organization/verification.md](organization/verification.md) records the checks
run at the time. Folder names such as `archive` mark a superseded version rather
than a discarded file.
