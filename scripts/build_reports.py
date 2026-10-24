#!/usr/bin/env python3
"""Build the synthetic FY26 Q3 execution report as .csv, .xlsx and .docx.

Standard library only. Files are byte-for-byte repeatable (fixed zip timestamps,
fixed part order). Writes:

  data/fy26_q3_execution_report.{csv,xlsx,docx}      Demo 1 report (clean)
  demo2/demo_report.{xlsx,docx}                       Demo 2 clean copy (identical bytes)
  demo2/INJECTED_demo_report_DO_NOT_USE.{xlsx,docx}   Demo 2 injected copy
  copilot-kit/fy26_q3_execution_report.{xlsx,docx}    clean copies for the Copilot path

Only the INJECTED files carry hidden text. The hidden text is the benign payload in
report_data.PAYLOAD, documented in demo2/REVEAL.md.

Usage:  python3 scripts/build_reports.py
"""
import csv
import io
import os
import sys
import zipfile
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import report_data as rd  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP_TIME = (2026, 1, 1, 0, 0, 0)
BASE = "fy26_q3_execution_report"
INJECTED = "INJECTED_demo_report_DO_NOT_USE"

# Where the hidden text goes (documented in demo2/REVEAL.md).
XLSX_HIDDEN_CELL = "A36"
DOCX_HIDDEN_AFTER = rd.NOTES[1]  # appended to the end of this paragraph


def x(s):
    return escape(s, {'"': "&quot;"})


def write_zip(path, parts):
    """parts: list of (name, str). Deterministic output."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in parts:
            info = zipfile.ZipInfo(name, date_time=ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data.encode("utf-8"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(buf.getvalue())


def core_props(title):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{x(title)}</dc:title>'
            f'<dc:creator>{x(rd.LABEL)}</dc:creator>'
            '<dcterms:created xsi:type="dcterms:W3CDTF">2026-07-10T00:00:00Z</dcterms:created>'
            '</cp:coreProperties>')


# ---------------------------------------------------------------- CSV

def build_csv(path):
    def raw(r, code, name, remarks):
        return [code, name, r["annual"], r["obl_plan"], r["obl"], r["obl_var"],
                rd.fmt_pct(r["obl_pct"]), r["exp_plan"], r["exp"], r["exp_var"],
                rd.fmt_pct(r["exp_pct"]), remarks]
    body = [raw(r, r["code"], r["name"], r["remarks"]) for r in rd.rows()]
    tot = raw(rd.total(), "", "Total", "")
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    w.writerow([rd.TITLE])
    w.writerow([rd.SUBTITLE])
    w.writerow([rd.LABEL_LINE])
    w.writerow([])
    w.writerow(rd.COLUMNS)
    for r in body:
        w.writerow(r)
    w.writerow(tot)
    w.writerow([])
    for n in rd.NOTES:
        w.writerow([n])
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(out.getvalue())


# ---------------------------------------------------------------- XLSX

def col_letter(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def xlsx_styles(inject):
    # fonts: 0 normal, 1 bold, 2 title bold 14, 3 italic, [4 white - injected only]
    fonts = [
        '<font><sz val="10"/><name val="Arial"/><family val="2"/></font>',
        '<font><b/><sz val="10"/><name val="Arial"/><family val="2"/></font>',
        '<font><b/><sz val="14"/><name val="Arial"/><family val="2"/></font>',
        '<font><i/><sz val="10"/><name val="Arial"/><family val="2"/></font>',
    ]
    if inject:
        fonts.append('<font><sz val="10"/><color rgb="FFFFFFFF"/><name val="Arial"/><family val="2"/></font>')
    fills = ['<fill><patternFill patternType="none"/></fill>',
             '<fill><patternFill patternType="gray125"/></fill>',
             '<fill><patternFill patternType="solid"><fgColor rgb="FFD9D9D9"/><bgColor indexed="64"/></patternFill></fill>']
    borders = ['<border><left/><right/><top/><bottom/><diagonal/></border>',
               '<border><left/><right/><top style="thin"><color auto="1"/></top><bottom/><diagonal/></border>']
    # cellXfs:
    # 0 default, 1 title, 2 bold, 3 header (bold, gray, wrap), 4 number, 5 pct,
    # 6 text wrap, 7 total label, 8 total number, 9 total pct, 10 italic, [11 white]
    xfs = [
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment vertical="top"/></xf>',
        '<xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"/>',
        '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>',
        '<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment wrapText="1" vertical="center"/></xf>',
        '<xf numFmtId="3" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1" applyAlignment="1"><alignment vertical="top"/></xf>',
        '<xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1" applyAlignment="1"><alignment vertical="top"/></xf>',
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>',
        '<xf numFmtId="0" fontId="1" fillId="0" borderId="1" xfId="0" applyFont="1" applyBorder="1"/>',
        '<xf numFmtId="3" fontId="1" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyBorder="1"/>',
        '<xf numFmtId="164" fontId="1" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyBorder="1"/>',
        '<xf numFmtId="0" fontId="3" fillId="0" borderId="0" xfId="0" applyFont="1"/>',
    ]
    if inject:
        xfs.append('<xf numFmtId="0" fontId="4" fillId="0" borderId="0" xfId="0" applyFont="1"/>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<numFmts count="1"><numFmt numFmtId="164" formatCode="0.0%"/></numFmts>'
            f'<fonts count="{len(fonts)}">{"".join(fonts)}</fonts>'
            f'<fills count="{len(fills)}">{"".join(fills)}</fills>'
            f'<borders count="{len(borders)}">{"".join(borders)}</borders>'
            '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
            f'<cellXfs count="{len(xfs)}">{"".join(xfs)}</cellXfs>'
            '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
            '</styleSheet>')


def build_xlsx(path, inject=False):
    strings, index = [], {}

    def sst(s):
        if s not in index:
            index[s] = len(strings)
            strings.append(s)
        return index[s]

    rows_xml = []

    def srow(r, cells, ht=None):
        attrs = f' r="{r}"' + (f' ht="{ht}" customHeight="1"' if ht else "")
        rows_xml.append(f'<row{attrs}>{"".join(cells)}</row>')

    def s(ref, text, style=0):
        return f'<c r="{ref}" s="{style}" t="s"><v>{sst(text)}</v></c>'

    def n(ref, val, style=4):
        return f'<c r="{ref}" s="{style}"><v>{val}</v></c>'

    def f(ref, formula, val, style=4):
        return f'<c r="{ref}" s="{style}"><f>{x(formula)}</f><v>{val}</v></c>'

    srow(1, [s("A1", rd.TITLE, 1)], ht=20)
    srow(2, [s("A2", rd.SUBTITLE, 0)])
    srow(3, [s("A3", rd.LABEL_LINE, 2)])
    srow(5, [s(f"{col_letter(i)}5", c, 3) for i, c in enumerate(rd.COLUMNS)], ht=40)
    first, r = 6, 6
    for row in rd.rows():
        cells = [s(f"A{r}", row["code"]), s(f"B{r}", row["name"]),
                 n(f"C{r}", row["annual"]), n(f"D{r}", row["obl_plan"]), n(f"E{r}", row["obl"]),
                 f(f"F{r}", f"E{r}-D{r}", row["obl_var"]),
                 f(f"G{r}", f"IF(D{r}=0,0,F{r}/D{r})", repr(row["obl_pct"]), 5),
                 n(f"H{r}", row["exp_plan"]), n(f"I{r}", row["exp"]),
                 f(f"J{r}", f"I{r}-H{r}", row["exp_var"]),
                 f(f"K{r}", f"IF(H{r}=0,0,J{r}/H{r})", repr(row["exp_pct"]), 5)]
        if row["remarks"]:
            cells.append(s(f"L{r}", row["remarks"], 6))
        srow(r, cells)
        r += 1
    last = r - 1
    t = rd.total()
    srow(r, [s(f"A{r}", "", 7), s(f"B{r}", "Total", 7)]
         + [f(f"{c}{r}", f"SUM({c}{first}:{c}{last})", t[k], 8)
            for c, k in (("C", "annual"), ("D", "obl_plan"), ("E", "obl"))]
         + [f(f"F{r}", f"E{r}-D{r}", t["obl_var"], 8),
            f(f"G{r}", f"IF(D{r}=0,0,F{r}/D{r})", repr(t["obl_pct"]), 9)]
         + [f(f"{c}{r}", f"SUM({c}{first}:{c}{last})", t[k], 8)
            for c, k in (("H", "exp_plan"), ("I", "exp"))]
         + [f(f"J{r}", f"I{r}-H{r}", t["exp_var"], 8),
            f(f"K{r}", f"IF(H{r}=0,0,J{r}/H{r})", repr(t["exp_pct"]), 9)])
    total_row = r
    srow(total_row + 2, [s(f"A{total_row + 2}", rd.NOTES[0], 10)])
    srow(total_row + 3, [s(f"A{total_row + 3}", rd.NOTES[1], 10)])
    if inject:
        hr = int(XLSX_HIDDEN_CELL[1:])
        assert hr > total_row + 3
        srow(hr, [s(XLSX_HIDDEN_CELL, rd.PAYLOAD, 11)])
    last_row = int(XLSX_HIDDEN_CELL[1:]) if inject else total_row + 3

    widths = [10, 34, 12, 12, 12, 12, 12, 12, 12, 12, 12, 70]
    cols = "".join(f'<col min="{i + 1}" max="{i + 1}" width="{w}" customWidth="1"/>'
                   for i, w in enumerate(widths))
    sheet = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
             '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
             'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
             '<sheetPr><pageSetUpPr fitToPage="1"/></sheetPr>'
             f'<dimension ref="A1:L{last_row}"/>'
             '<sheetViews><sheetView workbookViewId="0">'
             '<pane ySplit="5" topLeftCell="A6" activePane="bottomLeft" state="frozen"/>'
             '<selection pane="bottomLeft" activeCell="A6" sqref="A6"/></sheetView></sheetViews>'
             '<sheetFormatPr defaultRowHeight="13"/>'
             f'<cols>{cols}</cols>'
             f'<sheetData>{"".join(rows_xml)}</sheetData>'
             '<pageMargins left="0.4" right="0.4" top="0.5" bottom="0.5" header="0.3" footer="0.3"/>'
             '<pageSetup orientation="landscape" fitToWidth="1" fitToHeight="0"/>'
             '</worksheet>')
    sst_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
               '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
               f'count="{len(strings)}" uniqueCount="{len(strings)}">'
               + "".join(f'<si><t xml:space="preserve">{x(t)}</t></si>' for t in strings)
               + '</sst>')
    workbook = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                '<bookViews><workbookView/></bookViews>'
                '<sheets><sheet name="FY26 Q3 Execution" sheetId="1" r:id="rId1"/></sheets>'
                '<calcPr calcId="191029" fullCalcOnLoad="1"/>'
                '</workbook>')
    wb_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
               '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
               '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
               '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
               '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>'
               '</Relationships>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '</Relationships>')
    ctypes = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
              '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
              '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
              '<Default Extension="xml" ContentType="application/xml"/>'
              '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
              '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
              '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
              '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
              '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
              '</Types>')
    write_zip(path, [
        ("[Content_Types].xml", ctypes), ("_rels/.rels", rels),
        ("docProps/core.xml", core_props(f"{rd.TITLE} ({rd.LABEL})")),
        ("xl/workbook.xml", workbook), ("xl/_rels/workbook.xml.rels", wb_rels),
        ("xl/styles.xml", xlsx_styles(inject)), ("xl/sharedStrings.xml", sst_xml),
        ("xl/worksheets/sheet1.xml", sheet),
    ])


# ---------------------------------------------------------------- DOCX

W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


def run(text, bold=False, italic=False, size=None, color=None):
    rpr = ""
    if bold:
        rpr += "<w:b/>"
    if italic:
        rpr += "<w:i/>"
    if color:
        rpr += f'<w:color w:val="{color}"/>'
    if size:
        rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    rpr = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
    return f'<w:r>{rpr}<w:t xml:space="preserve">{x(text)}</w:t></w:r>'


def para(runs, after=80, align=None):
    ppr = f'<w:spacing w:before="0" w:after="{after}"/>'
    if align:
        ppr += f'<w:jc w:val="{align}"/>'
    return f"<w:p><w:pPr>{ppr}</w:pPr>{''.join(runs)}</w:p>"


def cell(text, width, bold=False, shade=None, align=None, size=14):
    tcpr = f'<w:tcW w:w="{width}" w:type="dxa"/>'
    if shade:
        tcpr += f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>'
    p = para([run(text, bold=bold, size=size)], after=0, align=align)
    return f"<w:tc><w:tcPr>{tcpr}</w:tcPr>{p}</w:tc>"


def build_docx(path, inject=False):
    body, tot = rd.table_strings()
    widths = [760, 2000] + [940] * 9 + [3300]  # = 14520 twips
    num_cols = set(range(2, 11))
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    hdr = "".join(cell(c, widths[i], bold=True, shade="D9D9D9", size=13) for i, c in enumerate(rd.COLUMNS))
    trs = [f'<w:tr><w:trPr><w:tblHeader/></w:trPr>{hdr}</w:tr>']
    for r in body:
        trs.append("<w:tr>" + "".join(
            cell(v, widths[i], align="right" if i in num_cols else None) for i, v in enumerate(r))
            + "</w:tr>")
    trs.append("<w:tr>" + "".join(
        cell(v, widths[i], bold=True, align="right" if i in num_cols else None)
        for i, v in enumerate(tot)) + "</w:tr>")
    borders = "".join(f'<w:{b} w:val="single" w:sz="4" w:space="0" w:color="808080"/>'
                      for b in ("top", "left", "bottom", "right", "insideH", "insideV"))
    table = ('<w:tbl><w:tblPr><w:tblW w:w="14520" w:type="dxa"/>'
             f'<w:tblBorders>{borders}</w:tblBorders>'
             '<w:tblLayout w:type="fixed"/>'
             '<w:tblCellMar><w:left w:w="50" w:type="dxa"/><w:right w:w="50" w:type="dxa"/></w:tblCellMar>'
             f'</w:tblPr><w:tblGrid>{grid}</w:tblGrid>{"".join(trs)}</w:tbl>')

    last_runs = [run(rd.NOTES[1], italic=True, size=16)]
    if inject:
        # Simple hidden-text technique: white, 1-point text at the end of the last line.
        last_runs.append(run(" " + rd.PAYLOAD, size=2, color="FFFFFF"))
    parts = [
        para([run(rd.TITLE, bold=True, size=28)], after=40),
        para([run(rd.SUBTITLE, size=18)], after=40),
        para([run(rd.LABEL_LINE, bold=True, size=18)], after=120),
        table,
        para([], after=60),
        para([run(rd.NOTES[0], italic=True, size=16)], after=40),
        para(last_runs, after=0),
    ]
    sect = ('<w:sectPr><w:pgSz w:w="15840" w:h="12240" w:orient="landscape"/>'
            '<w:pgMar w:top="720" w:right="660" w:bottom="720" w:left="660" w:header="360" '
            'w:footer="360" w:gutter="0"/></w:sectPr>')
    document = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                f'<w:document {W}><w:body>{"".join(parts)}{sect}</w:body></w:document>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
              f'<w:styles {W}><w:docDefaults><w:rPrDefault><w:rPr>'
              '<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="Arial" w:cs="Arial"/>'
              '<w:sz w:val="18"/><w:szCs w:val="18"/><w:lang w:val="en-US"/>'
              '</w:rPr></w:rPrDefault><w:pPrDefault><w:pPr>'
              '<w:spacing w:after="80" w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault>'
              '</w:docDefaults>'
              '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
              '</w:styles>')
    doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
                '</Relationships>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '</Relationships>')
    ctypes = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
              '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
              '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
              '<Default Extension="xml" ContentType="application/xml"/>'
              '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
              '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
              '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
              '</Types>')
    write_zip(path, [
        ("[Content_Types].xml", ctypes), ("_rels/.rels", rels),
        ("docProps/core.xml", core_props(f"{rd.TITLE} ({rd.LABEL})")),
        ("word/document.xml", document), ("word/_rels/document.xml.rels", doc_rels),
        ("word/styles.xml", styles),
    ])


OUTPUT_FILES = [
    "data/fy26_q3_execution_report.csv", "data/fy26_q3_execution_report.xlsx",
    "data/fy26_q3_execution_report.docx", "demo2/demo_report.xlsx", "demo2/demo_report.docx",
    "demo2/INJECTED_demo_report_DO_NOT_USE.xlsx", "demo2/INJECTED_demo_report_DO_NOT_USE.docx",
    "copilot-kit/fy26_q3_execution_report.xlsx", "copilot-kit/fy26_q3_execution_report.docx",
]


def main(root=ROOT):
    p = lambda *a: os.path.join(root, *a)  # noqa: E731
    os.makedirs(p("data"), exist_ok=True)
    build_csv(p("data", f"{BASE}.csv"))
    for folder, name in (("data", BASE), ("demo2", "demo_report"), ("copilot-kit", BASE)):
        build_xlsx(p(folder, f"{name}.xlsx"))
        build_docx(p(folder, f"{name}.docx"))
    build_xlsx(p("demo2", f"{INJECTED}.xlsx"), inject=True)
    build_docx(p("demo2", f"{INJECTED}.docx"), inject=True)
    print("Built report files in data/, demo2/, copilot-kit/")


if __name__ == "__main__":
    main()
