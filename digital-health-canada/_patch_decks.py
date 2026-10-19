from pptx import Presentation
OUT = "_deck_out/"

def set_cell(cell, text):
    p0 = cell.text_frame.paragraphs[0]
    if p0.runs:
        p0.runs[0].text = text
        for r in p0.runs[1:]:
            r.text = ""
    else:
        p0.text = text

# Deck A slide 16
prs = Presentation(OUT + "Paper-Series-Briefing-for-Co-Authors.pptx")
for sh in prs.slides[15].shapes:
    if getattr(sh, "has_table", False):
        set_cell(sh.table.cell(3, 4), "Canadian workforce & competency context; competency coding")
prs.save(OUT + "Paper-Series-Briefing-for-Co-Authors.pptx")
print("patched deck A slide16")

# Deck B: title slide subtitle check
prs2 = Presentation(OUT + "Year-1-Roadmap-for-Research-and-Scholarship.pptx")
print("deck B slide1 subtitle:", prs2.slides[0].shapes[2].text_frame.text)
print("deck B slide1 footer:", [p.text for p in prs2.slides[0].shapes[5].text_frame.paragraphs])
