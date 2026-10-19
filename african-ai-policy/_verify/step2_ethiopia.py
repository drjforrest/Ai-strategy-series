"""Step 2: archive Ethiopia out of the primary corpus (genre exclusion).

Moves the extract to data/_excluded/ and comments out the config registration.
Keeps the evidence (PDF, extract) for the genre-contrast set.
"""
import pathlib, re, shutil

D = pathlib.Path("data")
EXC = D / "_excluded"
EXC.mkdir(exist_ok=True)

# 1. move the extract
src = D / "national_strategies" / "ethiopia_ai.txt"
dst = EXC / "ethiopia_ai.txt"
if src.exists():
    shutil.move(str(src), str(dst))
    print(f"moved {src.name} -> _excluded/ ({len(dst.read_text().split()):,} words)")

# 2. move the source PDFs
for f in ["Digital Ethiopia 2025 Strategy_EN.pdf", "Digital Ethiopia 2030 Vision_EN.pdf"]:
    p = D / "national_strategies" / f
    if p.exists():
        shutil.move(str(p), str(EXC / f))
        print(f"moved {f} -> _excluded/")

# 3. deregister from config
cfg = pathlib.Path("src/config.py")
t = cfg.read_text()
old = '    "Ethiopia": "ethiopia_ai.txt",\n'
assert old in t, "Ethiopia registration not found"
new = ('    # EXCLUDED 2026-09-30: genre mismatch. Digital Ethiopia 2025 + 2030 Vision are\n'
       '    # general digital-transformation strategies, not a national AI strategy\n'
       '    # (AI-term density 1.87/1k words vs 19-46 for retained entries). Extract and\n'
       '    # PDFs archived in data/_excluded/; retained as a genre-contrast case.\n'
       '    # "Ethiopia": "ethiopia_ai.txt",\n')
t = t.replace(old, new, 1)
cfg.write_text(t)
print("deregistered Ethiopia in src/config.py")

# 4. verify
import importlib, sys
sys.path.insert(0, ".")
import src.config as C
importlib.reload(C)
print(f"\nconfig.COUNTRIES now has {len(C.COUNTRIES)} entries")
print("Ethiopia in COUNTRIES:", "Ethiopia" in C.COUNTRIES)
print("Remaining:", ", ".join(C.COUNTRIES))
