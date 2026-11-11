# Source documents

This repository tracks **code, generated outputs and documentation only**. The
primary source documents it analyses — national AI strategies, national digital
health and eHealth strategies, professional competency frameworks, readiness
index datasets and commercial market reports — are **not redistributed here**.
They are third-party publications whose licences differ and, in at least one
case, explicitly prohibit reproduction without written permission.

`corpus_manifest.csv` records every document the analysis reads, with the local
path the code expects, the document title, issuing body, language and planning
period where the project metadata records them, and the SHA-256 and byte size of
the exact file used. Checksums let anyone confirm that a copy they obtain
independently is the same file the published results were computed from.

## Obtaining the corpus

Place each document at the `local_path` given in the manifest, relative to
`african-ai-policy/`. The manifest carries a recorded `source_url` for 20 of the
129 documents; for the remaining 109 the project metadata does not record the
retrieval URL, so no URL is asserted here rather than guessed. Those documents
are obtained from the issuing body named in the manifest — for national
strategies, the relevant ministry or national AI office; for the Oxford
Government AI Readiness Index, the Oxford Insights public dataset releases; for
the Digital Health Canada frameworks and reports, Digital Health Canada.

After placing the files, verify with:

```bash
python - <<'PY'
import csv, hashlib, pathlib
root = pathlib.Path("african-ai-policy")
bad = miss = 0
for r in csv.DictReader(open("sources/corpus_manifest.csv")):
    p = root / r["local_path"] if not r["local_path"].startswith(("digital-health-canada","shared-resources")) \
        else pathlib.Path(r["local_path"])
    if not p.exists():
        print("missing:", r["local_path"]); miss += 1; continue
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    if h.hexdigest() != r["sha256"]:
        print("checksum differs:", r["local_path"]); bad += 1
print(f"{miss} missing, {bad} mismatched")
PY
```

## Derived text is also withheld

The pipeline's extracted plain-text corpora, passage tables and parsed
competency statements reproduce the substance of the source documents verbatim,
so they are withheld on the same grounds. The code regenerates all of them from
the source files. `dhc_hip_2026_provenance.json` records the SHA-256 of the two
Digital Health Canada 2026 PDFs, the statement and domain counts, and which
statement identifiers name AI, without reproducing any statement text.
