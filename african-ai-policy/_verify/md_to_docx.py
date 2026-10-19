#!/usr/bin/env python3
"""Minimal Markdown -> .docx for the Paper 1 v2.0 manuscript (headings, bold, tables)."""
import re, sys
from docx import Document
from docx.shared import Pt

src, out = sys.argv[1], sys.argv[2]
lines = open(src, encoding="utf-8").read().splitlines()
doc = Document()
doc.styles["Normal"].font.size = Pt(11)

def add_runs(par, text):
    # split on **bold** and *italic*
    for tok in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            r = par.add_run(tok[2:-2]); r.bold = True
        elif tok.startswith("*") and tok.endswith("*"):
            r = par.add_run(tok[1:-1]); r.italic = True
        else:
            par.add_run(tok)

i = 0
while i < len(lines):
    ln = lines[i]
    if ln.startswith("|") and i + 1 < len(lines) and set(lines[i+1].replace("|","").strip()) <= set("-: "):
        # table block
        header = [c.strip() for c in ln.strip().strip("|").split("|")]
        i += 2
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
            i += 1
        t = doc.add_table(rows=1, cols=len(header)); t.style = "Light Grid Accent 1"
        for j, h in enumerate(header):
            t.rows[0].cells[j].text = h
        for row in rows:
            cells = t.add_row().cells
            for j, c in enumerate(row[:len(header)]):
                cells[j].text = c
        doc.add_paragraph()
        continue
    if ln.startswith("## "):
        doc.add_heading(ln[3:].strip(), level=1)
    elif ln.startswith("# "):
        doc.add_heading(ln[2:].strip(), level=0)
    elif ln.strip() == "---":
        pass
    elif ln.strip() == "":
        pass
    else:
        p = doc.add_paragraph()
        add_runs(p, ln)
    i += 1

doc.save(out)
print(f"wrote {out} ({len(lines)} source lines)")
