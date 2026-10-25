"""Read .docx/.xlsx files with the standard library only.

Two jobs:
  * docx_structure(): a faithful preview of the document (title lines, table, note
    paragraphs with run-level formatting) for the app's Demo 2 reveal.
  * docx_text() / xlsx_text() / csv_text(): the plain text an AI tool would ingest.
    It includes every run and every cell, whatever its color or size. That is the
    point of Demo 2.
"""
import zipfile
import xml.etree.ElementTree as ET

WNS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
SNS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def _runs(p):
    out = []
    for r in p.iter(WNS + "r"):
        text = "".join(t.text or "" for t in r.iter(WNS + "t"))
        if not text:
            continue
        rpr = r.find(WNS + "rPr")
        color, size = None, None
        if rpr is not None:
            c = rpr.find(WNS + "color")
            if c is not None:
                color = c.get(WNS + "val")
            s = rpr.find(WNS + "sz")
            if s is not None:
                size = int(s.get(WNS + "val")) / 2
            if rpr.find(WNS + "vanish") is not None:
                color = color or "vanish"
        hidden = (color or "").upper() in ("FFFFFF", "VANISH") or (size is not None and size < 4)
        out.append({"text": text, "hidden": hidden, "color": color, "size_pt": size})
    return out


def _ptext(p):
    return "".join(t.text or "" for t in p.iter(WNS + "t"))


def docx_structure(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(WNS + "body")
    title_lines, notes, table = [], [], None
    for el in body:
        if el.tag == WNS + "p":
            if table is None:
                t = _ptext(el)
                if t:
                    title_lines.append(t)
            else:
                runs = _runs(el)
                if runs:
                    notes.append({"runs": runs})
        elif el.tag == WNS + "tbl":
            rows = [[_ptext(tc) for tc in tr.findall(WNS + "tc")] for tr in el.findall(WNS + "tr")]
            table = {"columns": rows[0], "rows": rows[1:-1], "total": rows[-1]}
    return {"title_lines": title_lines, "table": table, "notes": notes}


def docx_text(path):
    """Everything a text extractor sees: paragraphs and table rows (tab-separated)."""
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    lines = []
    for el in root.find(WNS + "body"):
        if el.tag == WNS + "p":
            lines.append(_ptext(el))
        elif el.tag == WNS + "tbl":
            for tr in el.findall(WNS + "tr"):
                lines.append("\t".join(_ptext(tc) for tc in tr.findall(WNS + "tc")))
    return "\n".join(l for l in lines if l.strip())


def xlsx_cells(path):
    """{ref: value} for every cell, with shared strings resolved; plus fonts per cell."""
    with zipfile.ZipFile(path) as z:
        sst = ET.fromstring(z.read("xl/sharedStrings.xml"))
        strings = ["".join(t.text or "" for t in si.iter(SNS + "t")) for si in sst.findall(SNS + "si")]
        sheet = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))
    cells = {}
    for c in sheet.iter(SNS + "c"):
        v = c.find(SNS + "v")
        if v is None:
            continue
        val = strings[int(v.text)] if c.get("t") == "s" else v.text
        cells[c.get("r")] = {"value": val, "style": int(c.get("s", "0"))}
    return cells


def xlsx_text(path):
    rows = {}
    for ref, cell in xlsx_cells(path).items():
        col = "".join(ch for ch in ref if ch.isalpha())
        row = int("".join(ch for ch in ref if ch.isdigit()))
        rows.setdefault(row, {})[col] = cell["value"]
    out = []
    for r in sorted(rows):
        vals = [rows[r][c] for c in sorted(rows[r], key=lambda c: (len(c), c)) if rows[r][c] != ""]
        if vals:
            out.append("\t".join(vals))
    return "\n".join(out)


def csv_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()
