"""Inspect both decks: every slide, every shape, every text frame.
Read-only. Prints structure so the edit plan can be exact.
"""
from pptx import Presentation
from pptx.util import Emu

DOCS = "/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/Knowledge Base/Documents MD Notebook/"
DECKS = {
    "PAPER-SERIES-BRIEFING": DOCS + "Paper-Series-Briefing-for-Co-Authors.pptx",
    "YEAR-1-ROADMAP": DOCS + "Year-1-Roadmap-for-Research-and-Scholarship.pptx",
}

for label, path in DECKS.items():
    prs = Presentation(path)
    print("=" * 100)
    print(f"{label}  ::  {path.split('/')[-1]}")
    print(f"  slides={len(prs.slides)}  size={Emu(prs.slide_width).inches:.2f}x{Emu(prs.slide_height).inches:.2f} in")
    print("=" * 100)
    for i, slide in enumerate(prs.slides):
        print(f"\n--- SLIDE {i+1} (layout='{slide.slide_layout.name}') ---")
        for j, sh in enumerate(slide.shapes):
            kind = sh.shape_type
            has_tf = sh.has_text_frame
            has_tbl = getattr(sh, "has_table", False)
            tag = f"[{j}] {sh.shape_type}"
            print(f"  {tag}  name={sh.name!r}  tf={has_tf} table={has_tbl}")
            if has_tf:
                for k, para in enumerate(sh.text_frame.paragraphs):
                    txt = "".join(r.text for r in para.runs)
                    if txt.strip():
                        print(f"        p{k} lvl{para.level}: {txt[:200]}")
            if has_tbl:
                tbl = sh.table
                print(f"        TABLE {len(tbl.rows)}x{len(tbl.columns)}")
                for r_i, row in enumerate(tbl.rows):
                    cells = [c.text.replace("\n", " / ")[:40] for c in row.cells]
                    print(f"          r{r_i}: {cells}")
        if slide.has_notes_slide:
            try:
                nt = slide.notes_slide.notes_text_frame.text
            except Exception:
                nt = ""
            if nt and nt.strip():
                print(f"  NOTES: {nt[:300]}")
    print("\n")
