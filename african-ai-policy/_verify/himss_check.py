#!/usr/bin/env python3
"""HIMSS27 poster-proposal compliance check against the official call-for-posters spec."""
import re, sys

PATH = sys.argv[1] if len(sys.argv) > 1 else "drafts/Paper2_HIMSS_poster_proposal.md"
LIMITS = {"Background": 200, "Purpose": 150, "Methods": 200, "Results": 350, "Conclusions / Implications": 200}
TOTAL_MAX = 1100

text = open(PATH, encoding="utf-8").read()
# split on bold section headers like **Background**
parts = re.split(r"\n\*\*([^*]+)\*\*\n", text)
sections = {}
for i in range(1, len(parts), 2):
    name = parts[i].strip()
    body = parts[i + 1]
    # strip any following bold sub-headers that are actually new sections
    sections[name] = body

def wc(s):
    return len(re.findall(r"[\w'’\-]+", s))

print(f"{'SECTION':<28}{'WORDS':>6}{'LIMIT':>7}{'STATUS':>10}")
print("-" * 51)
body_total = 0
for k, v in sections.items():
    n = wc(v)
    lim = LIMITS.get(k)
    if lim:
        body_total += n
        status = "OK" if n <= lim else f"OVER +{n-lim}"
        print(f"{k:<28}{n:>6}{lim:>7}{status:>10}")
    else:
        print(f"{k:<28}{n:>6}{'--':>7}{'n/a':>10}")
print("-" * 51)
print(f"{'FIVE-SECTION TOTAL':<28}{body_total:>6}{TOTAL_MAX:>7}{'OK' if body_total<=TOTAL_MAX else 'OVER':>10}")
print()
extra = [k for k in sections if k not in LIMITS and k not in ("Keywords", "Funding / Acknowledgements", "Title of Poster", "Author List and Affiliations", "Corresponding & Presenting Author and Email", "Structured Poster Proposal")]
print("Non-spec sections present (HIMSS structure is fixed at 5):", extra)
print("AI disclosure present:", "AI disclosure" in text or "AI tool" in text or "AI/Platform" in text)
print("Table/graph present:", bool(re.search(r"\|.*\|", text)) or "![" in text)
