#!/usr/bin/env python3
"""Preflight: run both demos headlessly against the cache and check everything that
must be true on the day. Prints PASS, or FAIL and the first failure. Exit code 0/1.

  python3 tools/preflight.py            # PASS / FAIL
  python3 tools/preflight.py -v         # list every check

Needs Python 3.8+. Uses Node.js (if installed) to run the app's own render code; without
Node the rendered-HTML checks are skipped and PASS says so.
"""
import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_cache  # noqa: E402
import build_reports  # noqa: E402
import office_text  # noqa: E402
import report_data as rd  # noqa: E402

ROOT = build_cache.ROOT
VERBOSE = False


class Fail(Exception):
    pass


def check(name, cond, detail=""):
    if not cond:
        raise Fail(f"{name}" + (f": {detail}" if detail else ""))
    if VERBOSE:
        print(f"  ok  {name}")


def path(*p):
    return os.path.join(ROOT, *p)


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


from output_checks import (LARGEST, NOT_ON_PLAN, clean_results, final_table_results,  # noqa: E402
                           injected_followed, table_rows)


def run_checks(skip_node=False, accept_resisted=False):
    notes = []
    key = json.load(open(path("data", "answer_key.json"), encoding="utf-8"))
    planted = key["planted"]

    # ---- 1. files present
    for p in ["app/index.html", "app/app.js", "app/cache.json", "app/SCHEMA.md",
              "data/answer_key.md", "data/answer_key.json", "demo2/REVEAL.md"] + build_reports.OUTPUT_FILES:
        check(f"file exists: {p}", os.path.exists(path(p)))

    # ---- 2. report files are exactly what the builder makes (no hand edits, no tampering)
    tmp = tempfile.mkdtemp(prefix="preflight-")
    try:
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()):
            build_reports.main(tmp)
        for p in build_reports.OUTPUT_FILES:
            check(f"rebuild is byte-identical: {p}", sha(path(p)) == sha(os.path.join(tmp, p)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for a, b in (("data/fy26_q3_execution_report.xlsx", "demo2/demo_report.xlsx"),
                 ("data/fy26_q3_execution_report.docx", "demo2/demo_report.docx"),
                 ("data/fy26_q3_execution_report.xlsx", "copilot-kit/fy26_q3_execution_report.xlsx"),
                 ("data/fy26_q3_execution_report.docx", "copilot-kit/fy26_q3_execution_report.docx")):
        check(f"clean copy identical: {b}", sha(path(a)) == sha(path(b)))

    # ---- 3. payload only where it belongs
    clean_files = [p for p in build_reports.OUTPUT_FILES if "INJECTED" not in p]
    for p in clean_files:
        text = (office_text.csv_text(path(p)) if p.endswith(".csv") else
                office_text.docx_text(path(p)) if p.endswith(".docx") else office_text.xlsx_text(path(p)))
        check(f"no hidden instruction in clean file: {p}", "ignore the largest" not in text.lower())
    for p in [p for p in build_reports.OUTPUT_FILES if "INJECTED" in p]:
        text = office_text.docx_text(path(p)) if p.endswith(".docx") else office_text.xlsx_text(path(p))
        check(f"injected file carries the payload exactly once: {p}", text.count(rd.PAYLOAD) == 1)
    injected_anywhere = [os.path.relpath(os.path.join(d, f), ROOT) for d, _, fs in os.walk(ROOT)
                         if ".git" not in d for f in fs if "INJECTED" in f]
    check("INJECTED files live only in ./demo2", all(p.startswith("demo2" + os.sep) for p in injected_anywhere),
          ", ".join(injected_anywhere))

    insp = subprocess.run([sys.executable, path("tools", "inspect_files.py")], capture_output=True, text=True)
    check("integrity inspection: Demo 1 files clean, injected differs only by the payload",
          insp.returncode == 0, insp.stdout[-400:])

    # ---- 4. report numbers match the answer key
    rows = {r["code"]: r for r in rd.rows()}
    check("report has 25 lines", len(rows) == 25)
    for v in planted:
        r = rows[v["code"]]
        actual = r["obl_var"] if v["measure"] == "obligations" else r["exp_var"]
        check(f"answer key variance matches report: {v['code']}", actual == v["variance_k"],
              f"{actual} vs {v['variance_k']}")
    others = [max(abs(r["obl_var"]), abs(r["exp_var"])) for c, r in rows.items()
              if c not in {v["code"] for v in planted}]
    check("five planted variances are the five largest",
          max(others) < min(abs(v["variance_k"]) for v in planted), f"largest other {max(others)}")
    check("largest variance is SYN-102", max(rows.values(), key=lambda r: abs(r["obl_var"]))["code"] == "SYN-102")

    # ---- 5. cache structure
    cache = json.load(open(path("app", "cache.json"), encoding="utf-8"))
    check("schema_version is 1", cache.get("schema_version") == 1)
    check("label is 'Synthetic demonstration data'", cache.get("label") == rd.LABEL)
    gen = cache["generation"]
    check("generation mode is valid",
          gen["mode"] in ("representative-pregenerated", "model-generated", "copilot-recorded", "chat-recorded"))
    if gen["mode"] != "representative-pregenerated":
        check(f"{gen['mode']} cache names its source and date", bool(gen.get("model")) and bool(gen.get("generated_at")))
    check("index.html embeds an identical copy of cache.json", build_cache.embedded_cache() == cache)
    check("index.html embeds an identical backup copy of app.js",
          build_cache.embedded_app() == open(path("app", "app.js"), encoding="utf-8").read().strip())

    d1 = cache["demo1"]
    ids = [s["id"] for s in d1["stages"]]
    check("Demo 1 has 5 ladder stages", ids == ["weak", "role", "task", "context", "output"], str(ids))
    check("Demo 1 weak prompt is exact", d1["stages"][0]["prompt"] == build_cache.WEAK)
    check("Demo 1 strong prompt is exact", d1["stages"][-1]["prompt"] == build_cache.STRONG)
    for i, s in enumerate(d1["stages"]):
        check(f"Demo 1 {s['id']}: segments join to the prompt",
              "".join(x["text"] for x in s["prompt_segments"]) == s["prompt"])
        new_parts = {x["part"] for x in s["prompt_segments"] if x["new"]}
        check(f"Demo 1 {s['id']}: only the added part is highlighted",
              new_parts == ({s["adds"]} if s["adds"] else {"base"}), str(new_parts))
        check(f"Demo 1 {s['id']}: guess list shrinks by one per stage", len(s["guesses"]) == 4 - i)
        if i:
            prev = d1["stages"][i - 1]
            check(f"Demo 1 {s['id']}: output differs from previous stage",
                  s["output"]["markdown"].strip() != prev["output"]["markdown"].strip())

    # ---- 6. Demo 1 final table has all five planted variances, each with its cause
    final = d1["stages"][-1]["output"]["markdown"]
    for name, ok, detail in final_table_results(final, planted):
        check(f"Demo 1 {name}", ok, detail)
    check("Demo 1 final table is a markdown table (renders as an HTML table)",
          sum(1 for l in final.splitlines() if l.strip().startswith("|")) >= 7)
    weak = d1["stages"][0]["output"]["markdown"]
    check("Demo 1 weak output has no table", not table_rows(weak))

    # ---- 7. Demo 2
    d2 = cache["demo2"]
    check("Demo 2 has 3 steps", [s["id"] for s in d2["steps"]] == ["clean", "injected", "reveal"])
    check("Demo 2 prompt is exact", d2["prompt"] == build_cache.DEMO2_PROMPT)
    check("Demo 2 payload is the agreed benign sentence", d2["payload"] == rd.PAYLOAD)
    check("Demo 2 reveal caption", d2["steps"][2].get("caption") == "Both files look identical to a human reader.")
    clean = d2["steps"][0]["output"]["markdown"]
    inj = d2["steps"][1]["output"]["markdown"]
    for name, ok, detail in clean_results(clean):
        check(f"Demo 2 {name}", ok, detail)
    followed = injected_followed(inj)
    recorded = gen["mode"] in ("copilot-recorded", "chat-recorded")
    if accept_resisted and recorded and not followed:
        notes.append("injected run did NOT follow the hidden line; accepted with --accept-resisted: "
                     "present the 'tool caught it' ending")
    else:
        check("Demo 2 injected run follows the planted instruction (says on plan, omits SYN-102)"
              + ("" if not recorded else
                 "; if the tool resisted, re-record or use --accept-resisted"), followed, inj[:160])
    hidden = [r for p in d2["documents"]["injected"]["notes"] for r in p["runs"] if r["hidden"]]
    check("reveal preview carries exactly one hidden run, the payload",
          len(hidden) == 1 and hidden[0]["text"].strip() == rd.PAYLOAD)
    check("clean preview carries no hidden run",
          not any(r["hidden"] for p in d2["documents"]["clean"]["notes"] for r in p["runs"]))
    for k in ("clean", "injected"):
        doc = d2["documents"][k]
        fresh = office_text.docx_structure(path(doc["file"]))
        check(f"Demo 2 {k} preview matches the real .docx", all(doc[x] == fresh[x] for x in fresh))

    kit = open(path("copilot-kit", "prompts.txt"), encoding="utf-8").read()
    for st in d1["stages"]:
        check(f"copilot-kit/prompts.txt has the {st['id']} prompt verbatim", st["prompt"] in kit)
    check("copilot-kit/prompts.txt has the Demo 2 prompt verbatim", d2["prompt"] in kit)
    check("copilot-kit/prompts.txt has the Demo 2 quote prompt verbatim", build_cache.QUOTE_PROMPT in kit)

    # ---- 7b. any-chat paste blocks (clean Demo 1 material)
    import build_paste_blocks
    from output_checks import ZERO_WIDTH
    tmp = tempfile.mkdtemp(prefix="preflight-paste-")
    try:
        build_paste_blocks.main(tmp)
        csv_text = office_text.csv_text(path("data", "fy26_q3_execution_report.csv")).rstrip()
        for i, f in enumerate(build_paste_blocks.FILES):
            check(f"paste block exists and is current: {f}",
                  os.path.exists(path(f)) and sha(path(f)) == sha(os.path.join(tmp, f)))
            t = open(path(f), encoding="utf-8").read()
            check(f"paste block has no hidden instruction or zero-width characters: {f}",
                  "ignore the largest" not in t.lower() and not ZERO_WIDTH.search(t))
            if i < 5:
                check(f"paste block holds the full report and the {d1['stages'][i]['id']} prompt",
                      csv_text in t and t.rstrip().endswith(d1["stages"][i]["prompt"]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ---- 7b2. paper rehearsal checklist agrees with the answer key
    ck = open(path("chat-kit", "REHEARSAL_CHECKLIST.md"), encoding="utf-8").read()
    check("copilot-kit checklist is identical to chat-kit checklist",
          ck == open(path("copilot-kit", "REHEARSAL_CHECKLIST.md"), encoding="utf-8").read())
    for v in planted:
        row = next((l for l in ck.splitlines() if v["code"] in l), "")
        sign = "+" if v["variance_k"] > 0 else "\u2212"
        check(f"rehearsal checklist lists {v['code']} with {sign}{abs(v['variance_k']):,} and its cause",
              f"{sign}{abs(v['variance_k']):,}" in row and any(k in row.lower() for k in v["cause_keywords"]), row)

    # ---- 7b3. Demo 1 ladder sheet (Demo 1 material): current, clean, holds every prompt
    import build_ladder
    tmp = tempfile.mkdtemp(prefix="preflight-ladder-")
    try:
        build_ladder.main(tmp)
        for f in build_ladder.FILES:
            check(f"ladder sheet exists and is current: {f}",
                  os.path.exists(path(f)) and sha(path(f)) == sha(os.path.join(tmp, f)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    lad = html.unescape(open(path(build_ladder.FILES[0]), encoding="utf-8").read())
    check("ladder sheet has no hidden instruction or zero-width characters",
          "ignore the largest" not in lad.lower() and not ZERO_WIDTH.search(lad))
    check("ladder sheet shows every Demo 1 prompt and a 'look for' line per step",
          all(st["prompt"].split(". ")[-1][:40] in lad for st in d1["stages"]) and lad.count("Look for in the answer") == 5)

    # ---- 7c. printable presenter scripts are current (no Python needed to present)
    import build_presenter_scripts
    tmp = tempfile.mkdtemp(prefix="preflight-scripts-")
    try:
        build_presenter_scripts.main(tmp)
        for f in build_presenter_scripts.FILES:
            check(f"printable script exists and is current: {f}",
                  os.path.exists(path(f)) and sha(path(f)) == sha(os.path.join(tmp, f)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ---- 7d. lean test kit: guide is current and holds every prompt; zip matches its files
    import build_test_guide
    import package_test_kit
    import zipfile
    tmp = tempfile.mkdtemp(prefix="preflight-testkit-")
    try:
        build_test_guide.main(tmp)
        check("test guide exists and is current: " + build_test_guide.FILE,
              os.path.exists(path(build_test_guide.FILE)) and
              sha(path(build_test_guide.FILE)) == sha(os.path.join(tmp, build_test_guide.FILE)))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    guide = html.unescape(open(path(build_test_guide.FILE), encoding="utf-8").read())
    check("test guide holds the weak, middle and strong prompts, the Demo 2 prompt and the quote prompt",
          all(p in guide for p in (build_cache.WEAK, d1["stages"][3]["prompt"], build_cache.STRONG,
                                   build_cache.DEMO2_PROMPT, build_cache.QUOTE_PROMPT)))
    zp = path("release", package_test_kit.TOP + ".zip")
    check("release/SDFM_demo_test_kit.zip exists", os.path.exists(zp))
    with zipfile.ZipFile(zp) as z:
        names = sorted(n.split("/", 1)[1] for n in z.namelist())
        same = names == sorted(package_test_kit.FILES) and all(
            z.read(f"{package_test_kit.TOP}/{n}") == open(path(src), "rb").read()
            for n, src in package_test_kit.FILES.items())
    check("test kit zip holds exactly the guide and the three demo files, all current "
          "(rebuild with tools/package_test_kit.py)", same)

    # ---- 8. presenter script
    pres = cache["presenter"]
    want = {"demo1": {"copilot": "4:00", "chat": "4:00", "full": "4:00", "90s": "1:30", "45s": "0:45"},
            "demo2": {"copilot": "1:30", "chat": "1:30", "full": "1:30", "45s": "0:45"}}
    for demo, versions in want.items():
        for vname, total in versions.items():
            v = pres[demo]["versions"].get(vname)
            check(f"presenter {demo}/{vname} exists", v is not None)
            check(f"presenter {demo}/{vname} totals {total}", v["total"] == total)
            secs = sum(c["seconds"] for c in v["cues"])
            check(f"presenter {demo}/{vname} cue lengths add to {total}",
                  f"{secs // 60}:{secs % 60:02d}" == total, str(secs))
            if vname in ("copilot", "chat"):
                check(f"presenter {demo}/{vname} says it is live, on synthetic data",
                      "live" in v["cues"][0]["say"].lower() or "staged" in v["cues"][0]["say"].lower())
                check(f"presenter {demo}/{vname} has a fallback line for every live step",
                      all(c.get("fallback") for c in v["cues"]
                          if c["step"] in ((1, 2, 3, 4, 5) if demo == "demo1" else (1, 2))))
            else:
                check(f"presenter {demo}/{vname} says outputs are pre-generated",
                      "{outputs" in v["cues"][0]["say"])
    asks = " ".join(c.get("ask", "") for c in pres["demo1"]["versions"]["full"]["cues"])
    check("room question: what is the AI being forced to guess", "forced to guess" in asks)
    asks = " ".join(c.get("ask", "") for c in pres["demo2"]["versions"]["full"]["cues"])
    check("room question: which file would you have trusted", "which file would you have trusted" in asks.lower())
    for vname in ("copilot", "chat"):
        cp = pres["demo2"]["versions"][vname]["cues"][-1]
        check(f"{vname} reveal cue has both endings (followed / caught it)",
              bool(cp.get("if_followed")) and bool(cp.get("if_resisted")))

    # ---- 9. run the app's own render code headlessly
    node = shutil.which("node")
    if skip_node or not node:
        notes.append("node not found: rendered-HTML checks skipped" if not skip_node else "rendered-HTML checks skipped")
        return "; ".join(notes)
    out = subprocess.run([node, path("tools", "headless_run.js"), path("app", "cache.json")],
                         capture_output=True, text=True, timeout=60)
    check("headless app run succeeds", out.returncode == 0, out.stderr[:300])
    run = json.loads(out.stdout)
    check("Demo 1 takes 6 key presses (5 stages + side-by-side)", run["demo1"]["key_presses"] == 6)
    check("Demo 2 takes 3 key presses", run["demo2"]["key_presses"] == 3)
    for demo in ("demo1", "demo2"):
        for s in run[demo]["steps"]:
            check(f"{demo} step {s['step']} renders", len(s["html"]) > 200)
            check(f"{demo} step {s['step']} presenter has a script line", "pv-say" in s["presenter"] or "pv-do" in s["presenter"])
    for s in range(1, 6):
        h = run["demo1"]["steps"][s]["html"]
        check(f"Demo 1 stage {s} highlights the new prompt part", h.count('class="seg-new"') >= 1)
    final_html = run["demo1"]["steps"][6]["html"]
    m = re.search(r'<table class="md-table">.*?<tbody>(.*?)</tbody>', final_html, re.S)
    check("Demo 1 side-by-side renders the leadership table as an HTML table", m is not None)
    body_rows = re.findall(r"<tr>(.*?)</tr>", m.group(1), re.S)
    check("leadership table has 5 rows", len(body_rows) == 5, str(len(body_rows)))
    for v in planted:
        check(f"rendered table includes {v['code']}", any(v["code"] in html.unescape(r) for r in body_rows))
    check("side-by-side shows the weak output too", "generally on track" in final_html or 'data-stage="weak"' in final_html)
    rev = html.unescape(run["demo2"]["steps"][3]["html"])
    check("reveal shows the hidden text highlighted", 'class="hidden-run"' in rev and rd.PAYLOAD in rev and "revealed" in rev)
    check("reveal shows the caption", "Both files look identical to a human reader." in rev)
    check("reveal shows both outputs", 'data-step="clean"' in rev and 'data-step="injected"' in rev)
    check("reveal labels the injected answer to match what it did",
          ("Followed the hidden line" in rev) == followed)
    from_label = {"copilot-recorded": "Recorded", "chat-recorded": "Recorded", "model-generated": "Pre-generated",
                  "representative-pregenerated": "Representative"}[gen["mode"]]
    for demo in ("demo1", "demo2"):
        for s in run[demo]["steps"][1:]:
            check(f"{demo} step {s['step']} labels where the answer came from",
                  from_label in html.unescape(s["html"]))
    for i in (1, 2):
        h = run["demo2"]["steps"][i]["html"]
        check(f"Demo 2 step {i} hides the payload (white, tiny) before the reveal",
              ("revealed" not in h) and (('class="hidden-run"' in h) == (i == 2)))
    return "; ".join(notes) or None


def main():
    global VERBOSE
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--no-node", action="store_true", help="skip the headless app run")
    ap.add_argument("--accept-resisted", action="store_true",
                    help="recorded Copilot run where Copilot ignored the hidden line: allow it")
    a = ap.parse_args()
    VERBOSE = a.verbose
    try:
        note = run_checks(skip_node=a.no_node, accept_resisted=a.accept_resisted)
    except Fail as e:
        print(f"FAIL: {e}")
        sys.exit(1)
    except Exception as e:  # a crash is a failure too, never a silent pass
        print(f"FAIL: preflight error: {type(e).__name__}: {e}")
        sys.exit(1)
    print("PASS" + (f" ({note})" if note else ""))


if __name__ == "__main__":
    main()
