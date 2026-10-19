"""Step 1: excise the 389-word NotebookLM derivative from kenya_ai.txt.

Keeps only the real strategy content (doc1). Single-source extracts in this repo
carry no '== source:' marker, so the marker is stripped for consistency.
"""
import pathlib, re

P = pathlib.Path("data/national_strategies/kenya_ai.txt")
orig = P.read_text(encoding="utf-8")
before = len(orig.split())

marks = [m.start() for m in re.finditer(r"== source:", orig)]
print(f"source markers found: {len(marks)}")
assert len(marks) == 2, "expected exactly 2 source markers"

doc1 = orig[marks[0]:marks[1]]      # real strategy
doc2 = orig[marks[1]:]              # derivative

# strip the marker line from doc1 (single-source files have none)
body = re.sub(r"^== source:.*?==\s*", "", doc1.strip(), count=1, flags=re.S).strip()
P.write_text(body + "\n", encoding="utf-8")

after = len(body.split())
print(f"  before: {before:,} words")
print(f"  derivative removed: {len(doc2.split()):,} words")
print(f"  after:  {after:,} words")
print(f"  first line now: {body.splitlines()[0][:70]}")
print(f"  NotebookLM artefacts remaining: {len(re.findall(r'NotebookLM|ToKnow\.ai|Audio Overview', body))}")
