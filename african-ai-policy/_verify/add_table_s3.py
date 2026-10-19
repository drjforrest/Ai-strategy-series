"""Add Table S3 (leave-one-country-out robustness of the circularity guard)
to the Supplementary Material, styled to match Table S2.

Result source: _verify/guard_fragility.py ->
               outputs/rhetoric_vs_readiness/guard_leave_one_out.csv
"""
import zipfile, shutil, re, csv, os

SRC = ("/Users/j.forrest/Library/CloudStorage/OneDrive-NortheasternUniversity/"
       "Documents/Private Northeastern/08_Research and Scholarship/Projects/"
       "National AI Strategies/Manuscript/"
       "African_AI_strategies_BMJGH_main_manuscript_v1.1-29sept2026.docx")
DST = SRC.replace("_v1.1-29sept2026.docx", "_v1.2-29sept2026.docx")
assert DST != SRC, "DST pattern did not match"

FILL_HDR, FILL_ROW = "1F3864", "FFFFFF"
BORDER = ('<w:tcBorders>'
          '<w:top w:val="outset" w:sz="6" w:space="0" w:color="auto"/>'
          '<w:left w:val="outset" w:sz="6" w:space="0" w:color="auto"/>'
          '<w:bottom w:val="outset" w:sz="6" w:space="0" w:color="auto"/>'
          '<w:right w:val="outset" w:sz="6" w:space="0" w:color="auto"/>'
          '</w:tcBorders>')
MARGIN = ('<w:tcMar><w:top w:w="40" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
          '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tcMar>')

def cell(text, width, header=False, centre=True):
    rpr = ('<w:b/><w:bCs/><w:color w:val="FFFFFF"/>' if header
           else '<w:color w:val="000000"/>')
    jc = '<w:jc w:val="center"/>' if centre else ''
    return (f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{BORDER}'
            f'<w:shd w:val="clear" w:color="auto" w:fill="{FILL_HDR if header else FILL_ROW}"/>'
            f'{MARGIN}<w:vAlign w:val="center"/><w:hideMark/></w:tcPr>'
            f'<w:p><w:pPr>{jc}</w:pPr><w:r><w:rPr>{rpr}'
            f'<w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
            f'<w:t xml:space="preserve">{text}</w:t></w:r></w:p></w:tc>')

def row(cells, header=False):
    trpr = '<w:trPr><w:tblHeader/></w:trPr>' if header else ''
    return f'<w:tr>{trpr}{"".join(cells)}</w:tr>'

WIDTHS = [1700, 2200, 2000, 1500, 1809]   # sums to 9209, matching Table S2
HDR = ["Country withheld", "Text-proximate mean r", "Independent mean r",
       "Permutation p", "p \u2264 0.05"]

rows_src = list(csv.DictReader(
    open("outputs/rhetoric_vs_readiness/guard_leave_one_out.csv")))
# full-set reference row first
data = [("None (full set)", "+0.208", "\u22120.113", "0.028", "Yes")]
for r in rows_src:
    data.append((r["dropped"],
                 f"{float(r['tp']):+.3f}".replace("-", "\u2212"),
                 f"{float(r['ind']):+.3f}".replace("-", "\u2212"),
                 f"{float(r['p']):.3f}",
                 "Yes" if r["sig"] == "True" else "No"))

tbl = ('<w:tbl><w:tblPr><w:tblW w:w="9209" w:type="dxa"/><w:tblBorders>'
       '<w:top w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
       '<w:left w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
       '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
       '<w:right w:val="single" w:sz="4" w:space="0" w:color="BFBFBF"/>'
       '</w:tblBorders><w:tblCellMar><w:left w:w="0" w:type="dxa"/>'
       '<w:right w:w="0" w:type="dxa"/></w:tblCellMar>'
       '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
       'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr><w:tblGrid>'
       + "".join(f'<w:gridCol w:w="{w}"/>' for w in WIDTHS)
       + '</w:tblGrid>')
tbl += row([cell(h, WIDTHS[i], header=True) for i, h in enumerate(HDR)], header=True)
for d in data:
    tbl += row([cell(d[0], WIDTHS[0], centre=False)]
               + [cell(x, WIDTHS[i + 1]) for i, x in enumerate(d[1:])])
tbl += '</w:tbl>'

caption = ('<w:p><w:pPr><w:pStyle w:val="Caption"/><w:keepNext/>'
           '<w:spacing w:before="240" w:after="0"/></w:pPr><w:r><w:rPr><w:b/><w:bCs/>'
           '</w:rPr><w:t>Table S3: Leave-one-country-out robustness of the '
           'circularity guard (text-derived emphasis versus 2024 Oxford '
           'readiness)</w:t></w:r></w:p>')

note_text = (
    "Each row repeats the circularity-guard analysis with a single country "
    "withheld; the first row reproduces the full 12-country result for "
    "reference. The directional pattern is stable throughout: the "
    "text-proximate subset remains positive and the independent subset "
    "remains negative in every variant. Statistical significance does not "
    "survive all removals, however, and withholding Nigeria, Morocco, "
    "C\u00f4te d\u2019Ivoire or South Africa individually raises p above 0.05. "
    "Because the permutations enumerate all 36 possible assignments of two of "
    "the nine dimensions, the smallest attainable p is 1/36 = 0.028, so the "
    "full-set result sits at the floor of the test and the separation should be "
    "read as a directional pattern rather than a precise effect. C\u00f4te "
    "d\u2019Ivoire is the country-name join harmonised in the main analysis, so "
    "its influence reflects both its own profile and the restored cell count.")
note = ('<w:p><w:pPr><w:spacing w:before="40" w:after="200"/></w:pPr>'
        '<w:r><w:rPr><w:i/><w:iCs/><w:color w:val="595959"/>'
        '<w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
        f'<w:t xml:space="preserve">{note_text}</w:t></w:r></w:p>')

xml = zipfile.ZipFile(SRC).read('word/document.xml').decode('utf-8')
anchor = ("Rwanda\u2019s 10% convergence estimate was r = +0.638 with bootstrap "
          "95% CI 0.248 to 0.975, reflecting uncertainty from the small number "
          "of contributing passages.</w:t></w:r></w:p>")
assert xml.count(anchor) == 1, f"anchor count = {xml.count(anchor)}"
xml = xml.replace(anchor, anchor + caption + tbl + note, 1)

plain = re.sub(r'<[^>]+>', '', xml)
assert plain.count("Table S3:") == 1
assert plain.count("Country withheld") == 1
print("Table S3 inserted; data rows:", len(data))

shutil.copy2(SRC, DST)
with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(DST, 'w', zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data_b = (xml.encode('utf-8') if item.filename == 'word/document.xml'
                  else zin.read(item.filename))
        zout.writestr(item, data_b)
print("wrote", os.path.basename(DST))
