from pptx import Presentation
DOCS = "/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/Knowledge Base/Documents MD Notebook/"
prs = Presentation(DOCS + "Year-1-Roadmap-for-Research-and-Scholarship.pptx")

print("### ROADMAP slides 14-15 (full) ###")
for idx in (13, 14):
    slide = prs.slides[idx]
    print(f"\n--- SLIDE {idx+1} ---")
    for j, sh in enumerate(slide.shapes):
        if sh.has_text_frame and sh.text_frame.text.strip():
            print(f"  [{j}] {sh.name!r} type={sh.shape_type}")
            for k, p in enumerate(sh.text_frame.paragraphs):
                t = "".join(r.text for r in p.runs)
                if t.strip():
                    print(f"      p{k} lvl{p.level}: {t}")

print("\n### ROADMAP slides 2,4,7 FULL ###")
for idx in (1, 3, 6):
    slide = prs.slides[idx]
    print(f"\n--- SLIDE {idx+1} ---")
    for j, sh in enumerate(slide.shapes):
        if getattr(sh, "has_table", False):
            tbl = sh.table
            print(f"  [{j}] TABLE {len(tbl.rows)}x{len(tbl.columns)}")
            for r_i, row in enumerate(tbl.rows):
                cells = [c.text for c in row.cells]
                print(f"      r{r_i}: {cells}")
        elif sh.has_text_frame and sh.text_frame.text.strip():
            for k, p in enumerate(sh.text_frame.paragraphs):
                t = "".join(r.text for r in p.runs)
                if t.strip():
                    print(f"  [{j}] {sh.name!r} p{k}: {t}")
