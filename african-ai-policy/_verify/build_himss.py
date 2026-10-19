"""Build the corrected HIMSS27 poster proposal DOCX (preserves the original)."""
import pathlib, zipfile, shutil, re

BASE = pathlib.Path("/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/"
    "Documents/Private Northeastern/08_Research and Scholarship/Projects/National AI Strategies")
SRC  = BASE / "HIMSS27_Poster_Proposal_Forrest_African_AI_Strategies.docx"
NEW  = BASE / "HIMSS27_Poster_Proposal_Forrest_African_AI_Strategies_REVISED_29sept2026.docx"
md   = pathlib.Path("/Users/j.forrest/dev/projects/data-science/african-ai-policy/_verify/"
                    "himss_abstract.md").read_text()
