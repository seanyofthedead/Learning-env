#!/usr/bin/env python3
"""Build the printable presenter scripts from content/presenter.json (maintainers only).

Writes, for presenters who never touch Python:
  chat-kit/SCRIPT.md, chat-kit/SCRIPT.html        "Any chat live" + short app versions
  copilot-kit/SCRIPT.md, copilot-kit/SCRIPT.html  "Copilot live" + short app versions

Same cues, timing marks and room questions as the app's presenter window, so the two can
never drift. Preflight rebuilds these files and checks they are current.

Usage:  python3 tools/build_presenter_scripts.py
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_cache  # noqa: E402

ROOT = build_cache.ROOT
KITS = {
    "chat-kit": ("Any chat tool", "chat", "your chosen chat tool"),
    "copilot-kit": ("Microsoft 365 Copilot", "copilot", "Microsoft 365 Copilot"),
}
FILES = [f"{k}/SCRIPT.{ext}" for k in KITS for ext in ("md", "html")]
OUTPUTS = ("[Say where the app's answers came from, as its answer panels show: for example "
           "“recorded in <tool> at rehearsal” or “representative examples, pre-generated”.]")
OUTPUTS_SHORT = "[Say: the answers are pre-generated.]"
TITLES = {"demo1": "Demo 1: From weak to strong", "demo2": "Demo 2: Trust but verify"}


def fill(t):
    return (t or "").replace("{outputs_short}", OUTPUTS_SHORT).replace("{outputs}", OUTPUTS)


def sections(live_key):
    pres = build_cache.with_timing(json.load(open(os.path.join(ROOT, "content", "presenter.json"), encoding="utf-8")))
    out = []
    for demo in ("demo1", "demo2"):
        vs = pres[demo]["versions"]
        out.append((demo, vs[live_key], True))
        for k in ("90s", "45s"):
            if k in vs:
                out.append((demo, vs[k], False))
    return out


def cue_extras(c):
    rows = []
    if c.get("ask"):
        rows.append(("Ask the room", c["ask"]))
    if c.get("if_followed"):
        rows.append(("If it followed the hidden line", c["if_followed"]))
    if c.get("if_resisted"):
        rows.append(("If the tool caught it", c["if_resisted"]))
    if c.get("fallback"):
        rows.append(("Fallback", c["fallback"]))
    return rows


def end_time(c):
    m, s = map(int, c["at"].split(":"))
    t = m * 60 + s + c["seconds"]
    return f"{t // 60}:{t % 60:02d}"


INTRO_LIVE = ("Live in {where}. Steps and keys: RUNBOOK.md. Pass/fail at rehearsal: "
              "REHEARSAL_CHECKLIST.md. [Square brackets] are stage directions, not spoken.")
INTRO_SHORT = ("Short on time: run this version from the app (app/index.html, double-click). "
               "Keys: → next, End jumps to the last step, R resets. The app's answers are "
               "pre-generated; say so.")


def build_md(tool, secs, where):
    L = [f"# Presenter script: {tool}", "",
         "**Synthetic demonstration data.** Print this, or keep it open on the laptop screen.", ""]
    for demo, v, live in secs:
        L += [f"## {TITLES[demo]}: {v['label']} ({v['total']})", "",
              INTRO_LIVE.format(where=where) if live else INTRO_SHORT, ""]
        for c in v["cues"]:
            L += [f"### {c['at']}–{end_time(c)}  {c['label']}", "",
                  f"- **Do:** {c['do']}" if c.get("do") else "",
                  f"- **Say:** {fill(c['say'])}"]
            L += [f"- **{k}:** {t}" for k, t in cue_extras(c)]
            L.append("")
    return "\n".join(l for l in L if l is not None).replace("\n\n\n", "\n\n").rstrip() + "\n"


CSS = """
body{font-family:Arial,Helvetica,sans-serif;color:#181818;background:#fff;margin:24px;font-size:16px;line-height:1.4}
h1{font-size:26px;margin:0 0 4px}.label{font-weight:bold;border:2px solid #181818;display:inline-block;padding:2px 8px;margin:4px 0 12px}
h2{font-size:21px;border-bottom:5px solid #96D200;padding-bottom:4px;margin:28px 0 6px;break-before:page}
h2.first{break-before:auto}.intro{color:#333;margin:0 0 10px}
table{border-collapse:collapse;width:100%}th{color:#181818;border-bottom:3px solid #181818;text-align:left;padding:6px}
td{border-bottom:1px solid #bbb;padding:7px 6px;vertical-align:top}td.t{white-space:nowrap;font-weight:bold;width:6.5em}
td.do{width:28%;color:#333}.say{font-size:17px}.x{margin-top:6px;padding:3px 7px;border-left:5px solid #96D200;background:#F1F9DD}
.x b{display:block;font-size:13px;letter-spacing:.04em;text-transform:uppercase}.fb{border-left-color:#C8102E;background:#FBE9EC}
tr{break-inside:avoid}@media print{body{margin:10mm}}
"""


def build_html(tool, secs, where):
    e = html.escape
    parts = [f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>Presenter script</title>"
             f"<style>{CSS}</style></head><body><h1>Presenter script: {e(tool)}</h1>"
             "<div class=\"label\">Synthetic demonstration data</div>"
             "<p class=\"intro\">Print with your browser (Ctrl+P). [Square brackets] are stage directions.</p>"]
    for i, (demo, v, live) in enumerate(secs):
        parts.append(f"<h2{' class=\"first\"' if i == 0 else ''}>{e(TITLES[demo])}: {e(v['label'])} ({e(v['total'])})</h2>"
                     f"<p class=\"intro\">{e(INTRO_LIVE.format(where=where) if live else INTRO_SHORT)}</p>"
                     "<table><tr><th>Time</th><th>Do</th><th>Say</th></tr>")
        for c in v["cues"]:
            extras = "".join(f"<div class=\"x{' fb' if k == 'Fallback' else ''}\"><b>{e(k)}</b>{e(t)}</div>"
                             for k, t in cue_extras(c))
            parts.append(f"<tr><td class=\"t\">{e(c['at'])}–{e(end_time(c))}<br>{e(c['label'])}</td>"
                         f"<td class=\"do\">{e(c.get('do', ''))}</td>"
                         f"<td><div class=\"say\">{e(fill(c['say']))}</div>{extras}</td></tr>")
        parts.append("</table>")
    parts.append("</body></html>\n")
    return "".join(parts)


def main(root=ROOT):
    for kit, (tool, key, where) in KITS.items():
        secs = sections(key)
        os.makedirs(os.path.join(root, kit), exist_ok=True)
        for ext, text in (("md", build_md(tool, secs, where)), ("html", build_html(tool, secs, where))):
            with open(os.path.join(root, kit, f"SCRIPT.{ext}"), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
    if root == ROOT:
        print("Wrote " + ", ".join(FILES))


if __name__ == "__main__":
    main()
