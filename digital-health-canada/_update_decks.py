# -*- coding: utf-8 -*-
"""Update both decks to reflect the reframed programme. Preserves run formatting."""
import os
from pptx import Presentation

DOCS = "/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/Knowledge Base/Documents MD Notebook/"
A = DOCS + "Paper-Series-Briefing-for-Co-Authors.pptx"
B = DOCS + "Year-1-Roadmap-for-Research-and-Scholarship.pptx"
OUT = "_deck_out/"
os.makedirs(OUT, exist_ok=True)

def set_para(p, text):
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r.text = ""
    else:
        p.text = text

def set_cell(cell, text):
    tf = cell.text_frame
    p0 = tf.paragraphs[0]
    set_para(p0, text)
    for p in tf.paragraphs[1:]:
        for r in p.runs:
            r.text = ""

def shape(slide, name):
    for sh in slide.shapes:
        if sh.name == name:
            return sh
    raise KeyError(f"shape {name!r} not found")

def P(slide, name, idx, text):
    set_para(shape(slide, name).text_frame.paragraphs[idx], text)

def C(slide, r, c, text):
    for sh in slide.shapes:
        if getattr(sh, "has_table", False):
            set_cell(sh.table.cell(r, c), text)
            return
    raise KeyError("no table on slide")

edits = 0

# ============ DECK A ============
prs = Presentation(A)
S = prs.slides

# Slide 2 - remove comparator implication
P(S[1], "Text 1", 1,
  "In many contexts — low- and middle-income countries and high-income settings alike — AI strategies are written as if "
  "enabling conditions already exist or will emerge in parallel. In practice, technical infrastructure, trained workforce "
  "capacity, regulatory maturity, interoperability standards, and sustainable investment pathways remain uneven, fragmented, "
  "or underdeveloped. The programme tests this first in African policy, then in Canadian professional competencies and workforce demand.")
edits += 1

# Slide 4 - Series at a glance table
C(S[3], 2, 4, "Submitted Oct 11, 2026")
C(S[3], 3, 1, "Canadian competencies & workforce demand")
C(S[3], 3, 2, "Do profession-defined competencies match employer demand for AI-era HI roles?")
C(S[3], 3, 3, "SHTI / JAMIA Open / Canadian venue")
C(S[3], 3, 4, "Design set; e-Health27 deferred")
C(S[3], 4, 2, "Do training programmes supply policy-assumed competencies — and do the domains travel?")
C(S[3], 4, 4, "Protocol v0.2; register inherited (~36 programmes)")
edits += 6

# Slide 5 - panel 3 (Paper 2b)
P(S[4], "Text 9", 0, "Paper 2b: Canadian Competencies and Demand")
P(S[4], "Text 10", 0,
  "Do profession-defined competencies match employer demand? A Canadian competency–demand study that establishes premises for the African work.")
edits += 2

# Slide 11 - Paper 2b slide rewrite
P(S[10], "Text 0", 0, "Paper 2b: Do Canadian Competencies Match Workforce Demand?")
P(S[10], "Text 1", 0, "Data")
P(S[10], "Text 2", 0,
  "Canadian professional and workforce data: Digital Health Canada's Health Informatics Professional Core Competencies "
  "(seven domains) and Career Matrix; the ~34 Canadian health informatics and health information management programmes "
  "(Borycki et al., 2024); and employer demand coded from health-sector job postings, which the OECD (2025) has already "
  "analysed at scale for Canada.")
P(S[10], "Text 3", 0, "Gap and Positioning")
P(S[10], "Text 4", 0,
  "Borycki and Kushniruk (2026) established qualitatively that Canadian health informatics specialist curricula lag on AI, "
  "and that the pathway for developing those competencies is unclear — but they measured nothing. This study measures the lag: "
  "coding programmes against the DHC framework and employer demand, and testing whether a professionally adopted competency "
  "framework matches the market.")
P(S[10], "Text 4", 1, "Status: Design set. The e-Health27 abstract has been deferred (tier discipline); the prior-art gap is confirmed.")
P(S[10], "Text 5", 0, "Method")
P(S[10], "Text 6", 0, "Standard and Supply")
P(S[10], "Text 7", 0,
  "Programmes coded against the DHC HIP Core Competencies (seven domains), cross-walked to IMIA 2023 so that the Canadian "
  "and African registers share one template.")
P(S[10], "Text 8", 0, "Demand")
P(S[10], "Text 9", 0,
  "Employer requirements coded from job postings. The finding is the alignment — or divergence — between professional standard, "
  "programme content, and market demand.")
edits += 11

# Slide 12 - Paper 3
P(S[11], "Text 2", 0,
  "Continental census of credentialed health informatics and digital health programmes (BSc through certificate), coded from "
  "public curricula. The register is inherited from the July 2026 scoping work: 36 programmes (23 named, 13 adjacent-label) "
  "across ten countries. Extends Were et al. (2021) beyond the East African Community.")
P(S[11], "Text 4", 1,
  "Cross-system test: a Canadian programme arm tests whether the competency domains behave comparably in both systems — "
  "comparability is the hypothesis, not the premise.")
edits += 2

# Slide 17 - Paper 3 gates
P(S[16], "Text 6", 0,
  "Ratify the two-layer template, the two-system (Africa + Canada) design, the optional director survey, and the ethics position. "
  "Volunteer as a second coder for the pilot.")
edits += 1

prs.save(OUT + "Paper-Series-Briefing-for-Co-Authors.pptx")
print(f"DECK A saved. edits={edits}")

# ============ DECK B ============
edits_b = 0
prs = Presentation(B)
S = prs.slides

# Slide 1 - date
P(S[0], "TextBox 8", 3, "Draft, October 16, 2026")
edits_b += 1

# Slide 2 - remove comparator implication
P(S[1], "Text 1", 1,
  "In many contexts — LMICs and high-income settings like Canada — AI strategies are formulated as if financing is the "
  "only enabling condition. In practice, technical infrastructure, trained workforce capacity, regulatory maturity, "
  "interoperability standards, and sustainable investment pathways remain uneven, fragmented, or underdeveloped.")
edits_b += 1

# Slide 4 - objective 03
P(S[3], "Text 14", 0, "Establish the Canadian premise")
P(S[3], "Text 15", 0, "Do profession-defined competencies match employer demand? (Paper 2b)")
edits_b += 2

# Slide 7 - activities table
C(S[6], 2, 4, "Submitted Oct 11, 2026")
C(S[6], 3, 1, "Canadian competencies & workforce demand")
C(S[6], 3, 2, "Do profession-defined competencies match employer demand for AI-era HI roles?")
C(S[6], 3, 3, "SHTI / JAMIA Open / Canadian venue")
C(S[6], 3, 4, "Design set; e-Health27 deferred")
C(S[6], 4, 2, "Do training programmes supply policy-assumed competencies — and do the domains travel?")
C(S[6], 4, 4, "Protocol v0.2; register inherited (~36 programmes)")
edits_b += 7

# Slide 14 - Next Steps
P(S[13], "Text 3", 0,
  "Evolve proxies for sector salience and policy/capital alignment into a formal semantic instrument. Formalize the "
  "six-lever operationalization score (Figure 2) as a coded, inter-rater-checked instrument and apply it to the Canadian "
  "competency dataset.")
P(S[13], "Text 9", 0,
  "Embed the responsible-AI overlay and Canadian competency findings in MSHI curriculum development. The Canadian programme "
  "arm of Paper 3 tests whether the competency domains travel across systems, and feeds directly into MSHI programme design.")
edits_b += 2

prs.save(OUT + "Year-1-Roadmap-for-Research-and-Scholarship.pptx")
print(f"DECK B saved. edits={edits_b}")
