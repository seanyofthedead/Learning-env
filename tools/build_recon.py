#!/usr/bin/env python3
"""Build Demo 3 (subledger to general ledger reconciliation) files. Standard library only,
byte-for-byte repeatable.

Writes:
  demo3/property_subledger_fy26_q3.{xlsx,csv}   the property system extract (40 asset records)
  demo3/general_ledger_fy26_q3.{xlsx,csv}       GL posting detail for the same accounts (38 postings)
  demo3/paste_block.txt                         both files as text + the prompt, for tools without uploads
  demo3/prompts.txt                             the demo prompts
  data/recon_answer_key.{json,md}               the five planted breaks (kept out of the report files)

Usage:  python3 tools/build_recon.py
"""
import csv
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_reports as br  # noqa: E402  (write_zip, x, col_letter)
import recon_data as rc  # noqa: E402

ROOT = br.ROOT
SL_BASE = "property_subledger_fy26_q3"
GL_BASE = "general_ledger_fy26_q3"

PROMPT = ("Act as a federal property accountant. Reconcile the attached property subledger to the general "
          "ledger for FY26 Q3, as of 30 June 2026. Match records by document number. Start with one table by "
          "account: subledger total, general ledger total and difference. Then, for each account that doesn't "
          "tie, list the documents that explain the difference, the amount and the likely reason, such as a "
          "duplicate, timing, a keying error, a misclassification or a missing record. Confirm that the items "
          "add up to each account's difference. End with a short research list for the property and accounting "
          "teams, brief enough to review in five minutes.")
VERIFY_PROMPT = ("Show your arithmetic for Equipment (1750): start from the subledger total, adjust for each "
                 "item you found, and land on the general ledger total.")
WEAK_PROMPT = "Compare these two files."


def sl_table():
    return [[r["asset"], r["doc"], r["account"], r["title"], r["desc"], r["acquired"], r["recorded"], r["cents"]]
            for r in rc.sl_rows()]


def gl_table():
    return [[r["doc"], r["posted"], r["account"], r["title"], r["desc"], r["cents"]] for r in rc.gl_rows()]


# ---------------------------------------------------------------- CSV

def csv_text(title, subtitle, columns, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow([title])
    w.writerow([subtitle])
    w.writerow([rc.LABEL_LINE])
    w.writerow([])
    w.writerow(columns)
    for row in rows:
        w.writerow([f"{v / 100:.2f}" if isinstance(v, int) else v for v in row])
    w.writerow([])
    w.writerow([rc.NOTE])
    return buf.getvalue()


# ---------------------------------------------------------------- XLSX

STYLES = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
          '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
          '<fonts count="4">'
          '<font><sz val="10"/><name val="Arial"/><family val="2"/></font>'
          '<font><b/><sz val="10"/><name val="Arial"/><family val="2"/></font>'
          '<font><b/><sz val="14"/><name val="Arial"/><family val="2"/></font>'
          '<font><i/><sz val="10"/><name val="Arial"/><family val="2"/></font></fonts>'
          '<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill>'
          '<fill><patternFill patternType="solid"><fgColor rgb="FFD9D9D9"/><bgColor indexed="64"/></patternFill></fill></fills>'
          '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
          '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
          '<cellXfs count="6">'
          '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'                       # 0 text
          '<xf numFmtId="0" fontId="2" fillId="0" borderId="0" xfId="0" applyFont="1"/>'         # 1 title
          '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>'         # 2 bold
          '<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1" applyAlignment="1">'
          '<alignment wrapText="1" vertical="center"/></xf>'                                      # 3 header
          '<xf numFmtId="4" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>'  # 4 #,##0.00
          '<xf numFmtId="0" fontId="3" fillId="0" borderId="0" xfId="0" applyFont="1"/>'         # 5 italic
          '</cellXfs><cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
          '</styleSheet>')


def build_xlsx(path, title, subtitle, columns, rows, widths, sheet_name, table_name):
    x, col = br.x, br.col_letter
    strings, index = [], {}

    def sst(s):
        if s not in index:
            index[s] = len(strings)
            strings.append(s)
        return index[s]

    out = []

    def srow(r, cells, ht=None):
        attrs = f' r="{r}"' + (f' ht="{ht}" customHeight="1"' if ht else "")
        out.append(f'<row{attrs}>{"".join(cells)}</row>')

    def s(ref, text, style=0):
        return f'<c r="{ref}" s="{style}" t="s"><v>{sst(text)}</v></c>'

    def n(ref, cents):
        return f'<c r="{ref}" s="4"><v>{cents / 100:.2f}</v></c>'

    srow(1, [s("A1", title, 1)], ht=20)
    srow(2, [s("A2", subtitle)])
    srow(3, [s("A3", rc.LABEL_LINE, 2)])
    srow(5, [s(f"{col(i)}5", c, 3) for i, c in enumerate(columns)], ht=28)
    r = 6
    for row in rows:
        srow(r, [n(f"{col(i)}{r}", v) if isinstance(v, int) else s(f"{col(i)}{r}", v) for i, v in enumerate(row)])
        r += 1
    last = r - 1
    srow(last + 2, [s(f"A{last + 2}", rc.NOTE, 5)])
    lc = col(len(columns) - 1)
    cols = "".join(f'<col min="{i + 1}" max="{i + 1}" width="{w}" customWidth="1"/>' for i, w in enumerate(widths))
    sheet = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
             '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
             'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
             '<sheetPr><pageSetUpPr fitToPage="1"/></sheetPr>'
             f'<dimension ref="A1:{lc}{last + 2}"/>'
             '<sheetViews><sheetView workbookViewId="0">'
             '<pane ySplit="5" topLeftCell="A6" activePane="bottomLeft" state="frozen"/>'
             '<selection pane="bottomLeft" activeCell="A6" sqref="A6"/></sheetView></sheetViews>'
             '<sheetFormatPr defaultRowHeight="13"/>'
             f'<cols>{cols}</cols><sheetData>{"".join(out)}</sheetData>'
             '<pageMargins left="0.4" right="0.4" top="0.5" bottom="0.5" header="0.3" footer="0.3"/>'
             '<pageSetup orientation="landscape" fitToWidth="1" fitToHeight="0"/>'
             '<tableParts count="1"><tablePart r:id="rId1"/></tableParts></worksheet>')
    tref = f"A5:{lc}{last}"
    table = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
             '<table xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" id="1" '
             f'name="{table_name}" displayName="{table_name}" ref="{tref}" totalsRowShown="0">'
             f'<autoFilter ref="{tref}"/><tableColumns count="{len(columns)}">'
             + "".join(f'<tableColumn id="{i + 1}" name="{x(c)}"/>' for i, c in enumerate(columns))
             + '</tableColumns><tableStyleInfo name="TableStyleLight1" showFirstColumn="0" '
             'showLastColumn="0" showRowStripes="1" showColumnStripes="0"/></table>')
    rel = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    parts = [
        ("[Content_Types].xml",
         '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
         '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
         '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
         '<Default Extension="xml" ContentType="application/xml"/>'
         '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
         '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
         '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
         '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
         '<Override PartName="/xl/tables/table1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.table+xml"/>'
         '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
         '</Types>'),
        ("_rels/.rels",
         '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
         '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
         f'<Relationship Id="rId1" Type="{rel}/officeDocument" Target="xl/workbook.xml"/>'
         '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
         '</Relationships>'),
        ("docProps/core.xml", br.core_props(f"{title} ({rc.LABEL})")),
        ("xl/workbook.xml",
         '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
         f'<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="{rel}">'
         f'<bookViews><workbookView/></bookViews><sheets><sheet name="{x(sheet_name)}" sheetId="1" r:id="rId1"/></sheets>'
         '</workbook>'),
        ("xl/_rels/workbook.xml.rels",
         '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
         '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
         f'<Relationship Id="rId1" Type="{rel}/worksheet" Target="worksheets/sheet1.xml"/>'
         f'<Relationship Id="rId2" Type="{rel}/styles" Target="styles.xml"/>'
         f'<Relationship Id="rId3" Type="{rel}/sharedStrings" Target="sharedStrings.xml"/>'
         '</Relationships>'),
        ("xl/styles.xml", STYLES),
        ("xl/sharedStrings.xml",
         '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
         '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
         f'count="{len(strings)}" uniqueCount="{len(strings)}">'
         + "".join(f'<si><t xml:space="preserve">{x(t)}</t></si>' for t in strings) + '</sst>'),
        ("xl/worksheets/sheet1.xml", sheet),
        ("xl/worksheets/_rels/sheet1.xml.rels",
         '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
         '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
         f'<Relationship Id="rId1" Type="{rel}/table" Target="../tables/table1.xml"/></Relationships>'),
        ("xl/tables/table1.xml", table),
    ]
    br.write_zip(path, parts)


# ---------------------------------------------------------------- answer key

def answer_key_json():
    return {
        "label": rc.LABEL,
        "as_of": rc.AS_OF,
        "accounts": [{**a, "sl": a["sl"] / 100, "gl": a["gl"] / 100, "diff": a["diff"] / 100}
                     for a in rc.account_summary()],
        "total_difference": sum(a["diff"] for a in rc.account_summary()) / 100,
        "breaks": [{**b, "effect": {k: v / 100 for k, v in b["effect"].items()}} for b in rc.breaks()],
        "prompt": PROMPT,
        "verify_prompt": VERIFY_PROMPT,
    }


def answer_key_md():
    m = rc.money
    lines = [
        "# Demo 3 answer key: subledger to general ledger reconciliation",
        "",
        "Synthetic demonstration data. **Presenter only:** never put this file in front of the AI tool.",
        "",
        f"FY26 Q3, as of {rc.AS_OF}. Subledger minus general ledger (GL). Dollars.",
        "",
        "| Account | Subledger | General ledger | Difference |",
        "|---|---:|---:|---:|",
    ]
    for a in rc.account_summary():
        lines.append(f"| {a['account']} {a['title']} | {m(a['sl'])} | {m(a['gl'])} | {m(a['diff'])} |")
    tot = {k: sum(a[k] for a in rc.account_summary()) for k in ("sl", "gl", "diff")}
    lines += [f"| **Total** | {m(tot['sl'])} | {m(tot['gl'])} | {m(tot['diff'])} |", "",
              "## The five breaks", "",
              "| # | Type | Account | Document(s) | Effect (SL - GL) | What it is | Research step |",
              "|---|---|---|---|---:|---|---|"]
    for b in rc.breaks():
        eff = "; ".join(f"{k}: {m(v)}" for k, v in b["effect"].items())
        lines.append(f"| {b['id']} | {b['type']} | {b['account']} | {', '.join(b['docs'])} | {eff} | {b['why']} | {b['action']} |")
    lines += [
        "",
        "Equipment (1750): 186,400.00 duplicate + 114,250.00 cutoff - 58,700.00 missing record = 241,950.00.",
        "Buildings (1730): -63,000.00 transposition - 265,000.00 misclassification = -328,000.00.",
        "Leasehold (1820): +265,000.00 misclassification. 1730 and 1820 offset: the total hides it.",
        "",
        "## What a strong answer does",
        "",
        "1. Account table with all three differences right (241,950.00; -328,000.00; 265,000.00).",
        "2. Names all five breaks by document number, with the right reason.",
        "3. Equipment: shows three items netting to 241,950.00 (the one people find hard by hand).",
        "4. Spots that 1730 and 1820 offset (same document, wrong account), not two separate problems.",
        "5. Notes the 63,000.00 difference divides by 9 (transposed digits), or names it a keying error.",
        "6. Research list a reviewer can act on. It shouldn't claim to have fixed anything.",
        "",
        "## Verify on stage",
        "",
        "- Ctrl+F `D26-0117` in the subledger: two rows, same generator. That's the duplicate, checked by a person in five seconds.",
        "- If the AI gets a total wrong, say so: that's the point. Select the Acquisition cost column in Excel and read the sum in the status bar.",
    ]
    return "\n".join(lines) + "\n"


def paste_block():
    sl = csv_text(rc.SL_TITLE, rc.SL_SUBTITLE, rc.SL_COLUMNS, sl_table())
    gl = csv_text(rc.GL_TITLE, rc.GL_SUBTITLE, rc.GL_COLUMNS, gl_table())
    prompt = PROMPT.replace("the attached property subledger", "the property subledger pasted below")
    return (prompt + "\n\n"
            f"=== FILE 1: {SL_BASE}.csv ===\n{sl}\n"
            f"=== FILE 2: {GL_BASE}.csv ===\n{gl}")


def prompts_txt():
    return ("DEMO 3: SUBLEDGER TO GENERAL LEDGER RECONCILIATION (synthetic demonstration data)\n\n"
            "Attach both files in one new chat: property_subledger_fy26_q3.xlsx and general_ledger_fy26_q3.xlsx\n"
            "(or .csv). Then paste:\n\n"
            f"PROMPT\n{PROMPT}\n\n"
            f"FOLLOW-UP (verify the arithmetic)\n{VERIFY_PROMPT}\n\n"
            f"OPTIONAL CONTRAST (run first, in its own chat, only if time allows)\n{WEAK_PROMPT}\n\n"
            "No uploads in your tool? Paste the whole of paste_block.txt instead and attach nothing.\n")


OUTPUTS = [f"demo3/{SL_BASE}.xlsx", f"demo3/{SL_BASE}.csv", f"demo3/{GL_BASE}.xlsx", f"demo3/{GL_BASE}.csv",
           "demo3/paste_block.txt", "demo3/prompts.txt", "data/recon_answer_key.json", "data/recon_answer_key.md"]


def main(root=ROOT):
    rc.check()
    d3 = os.path.join(root, "demo3")
    os.makedirs(d3, exist_ok=True)
    os.makedirs(os.path.join(root, "data"), exist_ok=True)

    def wtext(rel, text):
        with open(os.path.join(root, rel), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)

    wtext(f"demo3/{SL_BASE}.csv", csv_text(rc.SL_TITLE, rc.SL_SUBTITLE, rc.SL_COLUMNS, sl_table()))
    wtext(f"demo3/{GL_BASE}.csv", csv_text(rc.GL_TITLE, rc.GL_SUBTITLE, rc.GL_COLUMNS, gl_table()))
    build_xlsx(os.path.join(d3, f"{SL_BASE}.xlsx"), rc.SL_TITLE, rc.SL_SUBTITLE, rc.SL_COLUMNS, sl_table(),
               [12, 14, 9, 38, 40, 14, 14, 16], "Property subledger", "PropertySubledger")
    build_xlsx(os.path.join(d3, f"{GL_BASE}.xlsx"), rc.GL_TITLE, rc.GL_SUBTITLE, rc.GL_COLUMNS, gl_table(),
               [14, 13, 9, 38, 32, 16], "GL detail", "GeneralLedger")
    wtext("demo3/paste_block.txt", paste_block())
    wtext("demo3/prompts.txt", prompts_txt())
    wtext("data/recon_answer_key.json", json.dumps(answer_key_json(), indent=1, ensure_ascii=False) + "\n")
    wtext("data/recon_answer_key.md", answer_key_md())
    if root == ROOT:
        print("Wrote " + ", ".join(OUTPUTS))


if __name__ == "__main__":
    main()
