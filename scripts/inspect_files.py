#!/usr/bin/env python3
"""Integrity inspection of every report file, down to the raw XML.

For each Demo 1 file (and its identical copies) it lists every part inside the
package and flags anything that could hide or steer content:
  * hidden formatting: font colors, white text, tiny fonts, hidden/vanish runs,
    highlight, hidden rows/columns/sheets, number formats that hide values (;;;)
  * places text can hide: comments, notes, headers/footers, footnotes, custom XML,
    document variables, fields, hyperlinks, embedded objects, defined names,
    data validation messages, conditional formats, extra sheets
  * metadata: every core-properties field
  * text: zero-width or control characters; any string that is not part of the
    report's own content (report_data.py)
Then it diffs each INJECTED file against its clean twin and shows that the only
difference is the disclosed sentence and its white formatting.

  python3 scripts/inspect_files.py        # prints the report; exit 0 if all clean
"""
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_reports  # noqa: E402
import report_data as rd  # noqa: E402

ROOT = build_reports.ROOT
ZERO_WIDTH = re.compile("[​-‏‪-‮⁠-⁤﻿­\x00-\x08\x0b\x0c\x0e-\x1f]")

# Every string the report is supposed to contain.
body, tot = rd.table_strings()
EXPECTED = set([rd.TITLE, rd.SUBTITLE, rd.LABEL_LINE, "Total", ""] + rd.COLUMNS + rd.NOTES
               + [c for r in body for c in r] + tot
               + [f"{rd.TITLE} ({rd.LABEL})", rd.LABEL])

EXPECTED_PARTS = {
    "xlsx": {"[Content_Types].xml", "_rels/.rels", "docProps/core.xml", "xl/workbook.xml",
             "xl/_rels/workbook.xml.rels", "xl/styles.xml", "xl/sharedStrings.xml",
             "xl/worksheets/sheet1.xml", "xl/worksheets/_rels/sheet1.xml.rels", "xl/tables/table1.xml"},
    "docx": {"[Content_Types].xml", "_rels/.rels", "docProps/core.xml", "word/document.xml",
             "word/_rels/document.xml.rels", "word/styles.xml"},
}

# Patterns that would indicate hidden or steering content. (pattern, what it means)
DOCX_FLAGS = [
    (r"<w:color\b", "font color set on text"), (r"<w:vanish\b", "hidden (vanish) text"),
    (r"<w:specVanish\b", "special hidden text"), (r"<w:webHidden\b", "web-hidden text"),
    (r"<w:highlight\b", "highlight"), (r"<w:sz w:val=\"([0-9]|1[0-1])\"", "font under 6 pt"),
    (r"<w:instrText\b|<w:fldSimple\b", "field code"), (r"<w:hyperlink\b", "hyperlink"),
    (r"<w:altChunk\b|<w:object\b|<w:pict\b|<w:drawing\b", "embedded object/image"),
    (r"<w:docVar\b", "document variable"), (r"<w:comment", "comment"),
    (r"<w:footnote|<w:endnote|<w:headerReference|<w:footerReference", "footnote/header/footer"),
    (r"<w:position w:val=\"-", "text lowered out of view"),
]
XLSX_FLAGS = [
    (r"<color rgb=\"FFFFFFFF\"|<color rgb=\"FFFFFF\"|<color theme=\"0\"", "white font"),
    (r"<font>(?:(?!</font>).)*<color\b", "font color set"),
    (r"<sz val=\"[0-5](\.\d+)?\"", "font under 6 pt"),
    (r"hidden=\"1\"|state=\"hidden\"|state=\"veryHidden\"", "hidden row/column/sheet"),
    (r"formatCode=\"[^\"]*;;;?[^\"]*\"", "number format that can hide values"),
    (r"<definedName\b", "defined name"), (r"<dataValidation\b", "data validation message"),
    (r"<conditionalFormatting\b", "conditional formatting"), (r"<hyperlink\b", "hyperlink"),
    (r"<legacyDrawing\b|<drawing\b|<oleObject\b", "drawing/comment/object"),
]


def inspect(path, kind):
    """Returns (findings, strings, parts, core) for one package."""
    findings = []
    with zipfile.ZipFile(path) as z:
        parts = {i.filename: z.read(i.filename).decode("utf-8") for i in z.infolist()}
    extra = set(parts) - EXPECTED_PARTS[kind]
    missing = EXPECTED_PARTS[kind] - set(parts)
    if extra:
        findings.append(f"unexpected parts: {sorted(extra)}")
    if missing:
        findings.append(f"missing parts: {sorted(missing)}")
    flags = DOCX_FLAGS if kind == "docx" else XLSX_FLAGS
    for name, xml in parts.items():
        for pat, meaning in flags:
            hits = re.findall(pat, xml, re.S)
            if hits:
                findings.append(f"{name}: {meaning} ({len(hits)}x)")
        if ZERO_WIDTH.search(xml):
            findings.append(f"{name}: zero-width or control character")
    core = dict(re.findall(r"<(?:dc|cp|dcterms):(\w+)[^>]*>([^<]*)</", parts["docProps/core.xml"]))
    core = {k: unescape(v) for k, v in core.items()}
    tag = r"<w:t[^>]*>([^<]*)</w:t>" if kind == "docx" else r"<t[^>]*>([^<]*)</t>"
    src = parts["word/document.xml"] if kind == "docx" else parts["xl/sharedStrings.xml"]
    strings = [unescape(s) for s in re.findall(tag, src)]
    if kind == "docx":  # paragraphs may split text across runs; join per cell/paragraph
        strings = [unescape("".join(re.findall(tag, p)))
                   for p in re.findall(r"<w:p>.*?</w:p>", src, re.S)]
    unknown = [s for s in strings if s not in EXPECTED]
    for k, v in core.items():
        if k in ("title", "creator") and v not in EXPECTED:
            unknown.append(f"core.{k}={v}")
    if unknown:
        findings.append(f"text not in the report source: {unknown}")
    return findings, strings, parts, core


def unescape(s):
    return s.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&amp;", "&")


def inspect_csv(path):
    findings = []
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if ZERO_WIDTH.search(text):
        findings.append("zero-width or control character")
    non_ascii = sorted({c for c in text if ord(c) > 127})
    allowed = set("—–·")
    if set(non_ascii) - allowed:
        findings.append(f"unexpected non-ASCII characters: {non_ascii}")
    import csv
    import io
    cells = [c for row in csv.reader(io.StringIO(text)) for c in row]
    nums = re.compile(r"^-?\d+(\.\d+)?%?$")
    unknown = [c for c in cells if c not in EXPECTED and not nums.match(c)]
    if unknown:
        findings.append(f"text not in the report source: {unknown}")
    return findings, non_ascii


def main():
    ok = True
    print("INTEGRITY INSPECTION (Synthetic demonstration data)\n")
    clean = [p for p in build_reports.OUTPUT_FILES if "INJECTED" not in p]
    for rel in clean:
        path = os.path.join(ROOT, rel)
        if rel.endswith(".csv"):
            findings, non_ascii = inspect_csv(path)
            print(f"[{'CLEAN' if not findings else 'FLAG '}] {rel}  (non-ASCII: {''.join(non_ascii)})")
        else:
            kind = rel.rsplit(".", 1)[1]
            findings, strings, parts, core = inspect(path, kind)
            print(f"[{'CLEAN' if not findings else 'FLAG '}] {rel}")
            print(f"        parts: {', '.join(sorted(parts))}")
            print(f"        metadata: {core}")
            print(f"        {len(strings)} text items, all from the report source" if not any(
                "text not in" in f for f in findings) else "")
        for f in findings:
            print(f"        ! {f}")
        ok &= not findings

    print("\nINJECTED vs CLEAN (demo2)")
    for kind in ("xlsx", "docx"):
        c = os.path.join(ROOT, "demo2", f"demo_report.{kind}")
        i = os.path.join(ROOT, "demo2", f"INJECTED_demo_report_DO_NOT_USE.{kind}")
        fc, sc, pc, _ = inspect(c, kind)
        fi, si, pi, _ = inspect(i, kind)
        new_findings = [f for f in fi if f not in fc]
        changed = [n for n in pi if pi[n] != pc.get(n)]
        print(f"  {kind}: parts that differ: {changed}")
        for f in new_findings:
            print(f"        + {f}")
        expect_text = [f for f in new_findings if "text not in" in f]
        only_payload = len(expect_text) == 1 and rd.PAYLOAD in expect_text[0]
        print(f"        only extra text is the disclosed payload: {only_payload}")
        ok &= only_payload and not fc
    print("\nAPP: Demo 1 screens and cache")
    import json
    import shutil
    import subprocess
    cache = json.load(open(os.path.join(ROOT, "app", "cache.json"), encoding="utf-8"))
    d1 = json.dumps(cache["demo1"], ensure_ascii=False)
    d1_ok = rd.PAYLOAD.lower() not in d1.lower() and not ZERO_WIDTH.search(d1)
    print(f"  cache.json demo1 section free of hidden instruction and zero-width characters: {d1_ok}")
    ok &= d1_ok
    node = shutil.which("node")
    if node:
        run = json.loads(subprocess.run([node, os.path.join(ROOT, "scripts", "headless_run.js")],
                                        capture_output=True, text=True, check=True).stdout)
        bad = [s["step"] for s in run["demo1"]["steps"]
               if "hidden-run" in s["html"] or "data-hidden" in s["html"] or "display:none" in s["html"]]
        print(f"  Demo 1 screens with hidden elements: {bad or 'none'}")
        ok &= not bad
    else:
        print("  (node not found: rendered Demo 1 screens not inspected)")
    print("\nRESULT:", "Demo 1 files clean; injected files differ only by the disclosed sentence."
          if ok else "FINDINGS ABOVE")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
