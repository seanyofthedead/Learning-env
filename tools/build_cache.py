#!/usr/bin/env python3
"""Assemble app/cache.json from content/ and the real Demo 2 files, and embed a
copy into app/index.html so the app works from file:// as well as over HTTP.

Usage:
  python3 tools/build_cache.py                 # representative outputs from content/outputs
  python3 tools/build_cache.py --keep-outputs  # keep outputs + generation info already in cache.json
                                                 # (use after regenerate_cache.py, when only
                                                 #  content or presenter text changed)
"""
import argparse
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import office_text  # noqa: E402
import report_data as rd  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "app", "cache.json")
INDEX = os.path.join(ROOT, "app", "index.html")

WEAK = "Summarize this report."
STRONG = ("Act as a federal budget analyst supporting an NSA directorate. Review the attached "
          "FY26 Q3 execution report for the O&M appropriation and identify the five largest "
          "variances against plan. Use DoD FMR Volume 3 terminology. Present findings in a "
          "leadership-ready table with the variance, likely cause, and a recommended follow-up "
          "for each.")
DEMO2_PROMPT = ("Act as a budget analyst. Identify the largest variance in this report and state "
                "whether execution is on plan.")

REPRESENTATIVE = {
    "mode": "representative-pregenerated",
    "model": None,
    "temperature": None,
    "generated_at": "2026-10-24",
    "note": ("Representative pre-generated outputs, authored for this demo because no model "
             "API key was available at build time. Regenerate with tools/regenerate_cache.py."),
}


def read(*p):
    with open(os.path.join(ROOT, *p), encoding="utf-8") as f:
        return f.read()


def load_json(*p):
    return json.loads(read(*p))


def build_demo1(outputs):
    src = load_json("content", "demo1.json")
    order = ["role", "task", "context", "output"]
    stages = []
    for i, st in enumerate(src["stages"]):
        segs = [{"text": t, "part": part, "new": new} for t, part, new in st["segments"]]
        prompt = "".join(s["text"] for s in segs)
        guesses = [src["guess_items"][p] for p in order[i:]]
        stages.append({
            "id": st["id"], "label": st["label"], "adds": st["adds"],
            "prompt_segments": segs, "prompt": prompt, "guesses": guesses,
            "change_note": st["change_note"],
            "output": {"markdown": outputs[f"demo1_{st['id']}"]},
        })
    assert [s["id"] for s in stages] == ["weak"] + order, "stage order"
    assert stages[0]["prompt"] == WEAK, "weak prompt text"
    assert stages[-1]["prompt"] == STRONG, "strong prompt text:\n" + stages[-1]["prompt"]
    return {"title": src["title"], "attachment": src["attachment"], "parts": src["parts"],
            "stages": stages, "comparison": src["comparison"]}


def build_demo2(outputs):
    src = load_json("content", "demo2.json")
    assert src["prompt"] == DEMO2_PROMPT
    docs = {}
    for key, meta in src["documents"].items():
        d = office_text.docx_structure(os.path.join(ROOT, meta["file"]))
        docs[key] = {"file": meta["file"], "display_name": meta["display_name"], **d}
    steps = []
    for st in src["steps"]:
        step = dict(st)
        if st["id"] in ("clean", "injected"):
            step["output"] = {"markdown": outputs[f"demo2_{st['id']}"]}
        steps.append(step)
    return {"title": src["title"], "prompt": src["prompt"], "payload": rd.PAYLOAD,
            "documents": docs, "steps": steps}


def fmt_mss(sec):
    return f"{sec // 60}:{sec % 60:02d}"


def with_timing(presenter):
    """Add each cue's 'at' mark from cumulative cue lengths; check totals add up."""
    for demo, d in presenter.items():
        if not isinstance(d, dict) or "versions" not in d:
            continue
        for name, v in d["versions"].items():
            t = 0
            for cue in v["cues"]:
                cue["at"] = fmt_mss(t)
                t += cue["seconds"]
            assert fmt_mss(t) == v["total"], f"{demo}/{name}: cues add to {fmt_mss(t)}, not {v['total']}"
            steps = [c["step"] for c in v["cues"]]
            assert steps == sorted(steps), f"{demo}/{name}: cues out of step order"
    return presenter


def representative_outputs():
    out = {}
    folder = os.path.join(ROOT, "content", "outputs")
    for name in sorted(os.listdir(folder)):
        if name.endswith(".md"):
            out[name[:-3]] = read("content", "outputs", name).strip()
    return out


def outputs_from_cache(cache):
    out = {f"demo1_{s['id']}": s["output"]["markdown"] for s in cache["demo1"]["stages"]}
    for s in cache["demo2"]["steps"]:
        if "output" in s:
            out[f"demo2_{s['id']}"] = s["output"]["markdown"]
    return out


def build(outputs=None, generation=None):
    if outputs is None:
        outputs = representative_outputs()
    presenter_path = os.path.join(ROOT, "content", "presenter.json")
    presenter = load_json("content", "presenter.json") if os.path.exists(presenter_path) else {}
    presenter = with_timing(presenter)
    cache = {
        "schema_version": 1,
        "label": rd.LABEL,
        "generation": generation or REPRESENTATIVE,
        "demo1": build_demo1(outputs),
        "demo2": build_demo2(outputs),
        "presenter": presenter,
    }
    text = json.dumps(cache, indent=1, ensure_ascii=False) + "\n"
    with open(CACHE, "w", encoding="utf-8") as f:
        f.write(text)
    embedded = embed(text) and embed_app()
    return cache, embedded


EMBED_RE = re.compile(r'(<script id="embedded-cache" type="application/json">)(.*?)(</script>)', re.S)


def embed(text):
    """Copy cache.json into index.html. Returns False if index.html has no slot yet."""
    if not os.path.exists(INDEX):
        return False
    html = read("app", "index.html")
    safe = text.replace("</", "<\\/")
    new, n = EMBED_RE.subn(lambda m: m.group(1) + "\n" + safe + m.group(3), html)
    if n != 1:
        return False
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(new)
    return True


APP_RE = re.compile(r'(<script id="app-fallback">)(.*?)(</script>)', re.S)


def embed_app():
    """Copy app.js into index.html as a backup, so the page still works when app.js is
    missing or cannot be loaded next to it. Returns False if there is no slot."""
    if not os.path.exists(INDEX):
        return False
    html = read("app", "index.html")
    js = read("app", "app.js").replace("</script", "<\\/script")
    new, n = APP_RE.subn(lambda m: m.group(1) + "\n" + js + m.group(3), html)
    if n != 1:
        return False
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(new)
    return True


def embedded_app():
    """The app.js copy embedded in index.html (used by preflight)."""
    m = APP_RE.search(read("app", "index.html"))
    return m.group(2).strip() if m else None


def embedded_cache():
    """The JSON embedded in index.html, parsed (used by preflight)."""
    m = EMBED_RE.search(read("app", "index.html"))
    return json.loads(m.group(2)) if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keep-outputs", action="store_true")
    a = ap.parse_args()
    if a.keep_outputs and os.path.exists(CACHE):
        old = json.loads(read("app", "cache.json"))
        _, emb = build(outputs_from_cache(old), old["generation"])
    else:
        _, emb = build()
    print("Wrote app/cache.json" + (" and embedded it (and a backup copy of app.js) in app/index.html" if emb else
                                     " (index.html slot not found; not embedded)"))


if __name__ == "__main__":
    main()
