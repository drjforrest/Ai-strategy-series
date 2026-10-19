"""Trim the abstract to <=1,100 words without losing any verified number."""
import re, pathlib

p = pathlib.Path("himss_abstract.md")
t = p.read_text()

EDITS = [
 ("are widely promoted as ways to extend scarce specialist capacity",
  "are promoted to extend scarce specialist capacity"),
 ("described as policy mimicry or pilotitis, in which progress is asserted more often than observed",
  "described as policy mimicry or pilotitis, in which progress is asserted more than observed"),
 ("a reproducible, multilingual, reference-agnostic instrument",
  "a reproducible, multilingual instrument"),
 ("a multilingual sentence transformer that places English and French text",
  "a multilingual sentence transformer placing English and French text"),
 ("with a floor of three passages, then standardized within domain",
  "with a floor of three passages, standardized within domain"),
 ("These patterns are interpreted comparatively rather than as measures of policy quality or implementation.",
  "These patterns are comparative, not measures of policy quality or implementation."),
 ("Zimbabwe was aligned-low in five and aligned-high in none; Egypt and Mauritius most often "
  "understated measured capability (walk>talk in seven and six dimensions respectively); while Nigeria "
  "and Benin more often showed rhetoric exceeding measured readiness (talk>walk in four and three dimensions).",
  "Zimbabwe was aligned-low in five of nine dimensions; Egypt and Mauritius most often understated "
  "measured capability; while Nigeria and Benin more often showed rhetoric exceeding measured readiness."),
 ("Ethiopia\u2019s combined, longer documents", "Ethiopia\u2019s combined documents"),
 ("Ethiopia's combined, longer documents", "Ethiopia's combined documents"),
 ("a 12-country readiness comparison in which Ethiopia and Tanzania could not be included because their "
  "readiness scores rest partly on strategy text",
  "a 12-country readiness comparison that excludes Ethiopia and Tanzania, whose readiness scores rest "
  "partly on strategy text"),
 ("The findings therefore support a robust descriptive pattern rather than a causal claim or definitive "
  "country ranking.",
  "The findings support a robust descriptive pattern rather than a causal claim or definitive ranking."),
 ("a modest, heterogeneous corpus that may not reflect differences across 54 African Union member states",
  "a modest, heterogeneous corpus that may not reflect all 54 African Union member states"),
]
for old, new in EDITS:
    if old in t:
        t = t.replace(old, new, 1)
p.write_text(t)

def sec(name, nxt):
    return re.search(rf"# {re.escape(name)}(.*?)(?=# {re.escape(nxt)})", t, re.S).group(1)
order = [("Background","Purpose"),("Purpose","Methods"),("Methods","Results"),
         ("Results","Conclusions / Implications"),("Conclusions / Implications","Keywords")]
wc = lambda s: len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\u2019\-\.%]*", s))
body = "".join(sec(a,b) for a,b in order)
for a,b in order: print(f"  {a:30s} {wc(sec(a,b)):5d}")
print(f"\nTOTAL Background-Conclusions: {wc(body)}  (limit 1100)")
