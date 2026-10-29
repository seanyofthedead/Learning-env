#!/usr/bin/env python3
"""Build the one-page test guide for the lean test kit (maintainers only).

Writes test-kit/TEST_GUIDE.html: how to test both demos in Copilot (or any chat tool),
the exact prompts with copy buttons, what to look for in each answer, and a scorecard for
judging whether the demo will land with an audience. Prompts come from the same sources as
the rest of the kit; preflight checks the file is current.

Usage:  python3 tools/build_test_guide.py
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_cache  # noqa: E402
import build_paste_blocks  # noqa: E402
import office_text  # noqa: E402
import report_data as rd  # noqa: E402

ROOT = build_cache.ROOT
FILE = "test-kit/TEST_GUIDE.html"
REPORT = "fy26_q3_execution_report.xlsx"
CLEAN = "demo_report.docx"
INJECTED = "INJECTED_demo_report_DO_NOT_USE.docx"

CSS = """
:root{--c:#181818;--g:#96D200;--gt:#3D6200;--mut:#4D4D4D;--line:#C9CCC4;--soft:#F3F4F1;--red:#C8102E}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--c);font-family:Arial,Helvetica,sans-serif;font-size:18px;line-height:1.45}
header{background:var(--c);color:#fff;border-bottom:6px solid var(--g);padding:14px 20px;display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center}
header h1{margin:0;font-size:26px}
.label{border:2px solid #fff;border-radius:6px;padding:2px 8px;font-weight:bold;font-size:16px}
main{max-width:1050px;margin:0 auto;padding:16px 20px 32px;overflow-wrap:anywhere}
.scroll{overflow-x:auto}
h2{font-size:23px;border-bottom:4px solid var(--g);padding-bottom:4px;margin:28px 0 10px}
h3{font-size:20px;margin:0 0 6px}
.box{background:var(--soft);border-left:8px solid var(--g);padding:10px 14px;margin:10px 0}
.warn{border-left-color:var(--red)}
.step{border:1px solid var(--line);border-radius:10px;padding:14px;margin:12px 0;break-inside:avoid}
.num{display:inline-grid;place-items:center;width:34px;height:34px;border-radius:8px;background:var(--g);font-weight:bold;margin-right:8px}
.prompt{background:#fff;border:1px solid var(--line);border-left:6px solid var(--g);border-radius:6px;padding:10px 12px;margin:8px 0}
.look{margin:8px 0}.look b{color:var(--gt)}
.btns{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;margin-top:6px}
button{font:inherit;font-weight:bold;font-size:16px;padding:5px 12px;border-radius:8px;border:2px solid var(--c);background:#fff;color:var(--c);cursor:pointer}
button.primary{background:var(--c);color:#fff}
.status{color:var(--gt);font-weight:bold;font-size:16px}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:16px}
th{text-align:left;border-bottom:3px solid var(--c);padding:6px}
td{border-bottom:1px solid var(--line);padding:7px 6px;vertical-align:top}
td.g{border-left:6px solid var(--g)}td.y{border-left:6px solid #E8B400}td.r{border-left:6px solid var(--red)}
details{margin:10px 0}summary{cursor:pointer;font-weight:bold}
.tick{white-space:nowrap}
@media (max-width:640px){table{font-size:15px}}
@media print{header{background:#fff;color:var(--c);border-bottom:4px solid var(--c)}.label{border-color:var(--c)}
 .btns{display:none}body{font-size:13px}h2{break-before:auto}details{display:block}details>*{display:block}}
"""

JS = """
(function(){
  var data = JSON.parse(document.getElementById('guide-data').textContent);
  function fallbackCopy(t){
    var ta = document.createElement('textarea'); ta.value = t; ta.setAttribute('readonly', '');
    ta.style.position = 'fixed'; ta.style.top = '0'; ta.style.left = '0'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select(); var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta); return ok;
  }
  function say(el, ok){ el.textContent = ok ? 'Copied.' : 'Copy blocked: select the text and copy it by hand.'; }
  var buttons = document.querySelectorAll('button[data-copy]');
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function(){
      var text = data[this.getAttribute('data-copy')];
      var status = this.parentNode.querySelector('.status');
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function(){ say(status, true); }, function(){ say(status, fallbackCopy(text)); });
      } else { say(status, fallbackCopy(text)); }
    });
  }
})();
"""


def e(s):
    return html.escape(s)


def prompt_card(n, title, key, prompt, look, block_key=None, note=""):
    btns = f"<button class=\"primary\" data-copy=\"{key}\">Copy prompt</button>"
    if block_key:
        btns += f"<button data-copy=\"{block_key}\">Copy report + prompt (if you can't attach)</button>"
    return (f"<div class=\"step\"><h3><span class=\"num\">{e(str(n))}</span>{e(title)}</h3>{note}"
            f"<div class=\"prompt\">{e(prompt)}</div>"
            f"<div class=\"btns\">{btns}<span class=\"status\" aria-live=\"polite\"></span></div>"
            f"<p class=\"look\"><b>Look for:</b> {look}</p></div>")


def build():
    stages = {s["id"]: s for s in build_cache.load_json("content", "demo1.json")["stages"]}
    prompts = {k: "".join(t for t, _, _ in s["segments"]) for k, s in stages.items()}
    csv = office_text.csv_text(os.path.join(ROOT, "data", "fy26_q3_execution_report.csv"))
    data = {}
    for k, p in prompts.items():
        data[k] = p
        data[k + "_block"] = build_paste_blocks.paste_block(p, "fy26_q3_execution_report.csv", csv)
    data["d2"] = build_cache.DEMO2_PROMPT
    data["quote"] = build_cache.QUOTE_PROMPT

    d1 = (
        prompt_card(1, "Weak prompt", "weak", prompts["weak"],
                    "A long, competent answer: the problems are in there, somewhere. Note roughly how long it is "
                    "(a full screen or more is what you want). <span class=\"tick\">☐ long, not a short table</span>",
                    "weak_block")
        + prompt_card(2, "Role + Task + Context", "context", prompts["context"],
                      "Smarter <i>and longer</i>: budget terms (unobligated balance, reprogramming, tri-annual review) and "
                      "the 30 September deadline. <span class=\"tick\">☐ longer than answer 1</span>",
                      "context_block")
        + prompt_card(3, "Full prompt (Role + Task + Context + Output)", "output", prompts["output"],
                      "It gets <b>short</b>: a one-sentence bottom line, then a five-row table that fits on one screen. Check the rows:"
                      "<br>☐ SYN-102 Help Desk, obligations −$4,800K, late contract award"
                      "<br>☐ SYN-107 Device Refresh, +$3,100K, <b>cause not stated</b> → ask the program office"
                      "<br>☐ SYN-109 Mission Support, expenditures −$2,600K, <b>likely billing/invoice lag</b> (inferred from the numbers)"
                      "<br>☐ SYN-103 Facilities, +$1,800K, reprogramming"
                      "<br>☐ SYN-108 Software Licenses, +$1,250K, duplicate posting (document SYN-26-0447, 12 and 13 May)",
                      "output_block")
        + "<details><summary>Optional: the two in-between steps (explained from a slide on stage, not run live)</summary>"
        + prompt_card("2a", "+ Role only", "role", prompts["role"],
                      "Budget vocabulary appears; still a summary.", "role_block")
        + prompt_card("2b", "+ Role + Task", "task", prompts["task"],
                      "A ranked list of five lines with dollar amounts.", "task_block")
        + "</details>"
    )
    d2 = (
        prompt_card(4, f"Copy A: {CLEAN}", "d2", build_cache.DEMO2_PROMPT,
                    "Names <b>SYN-102 / Help Desk</b> as the largest variance (−$4,800K) and says execution is "
                    "<b>not</b> on plan. <span class=\"tick\">☐ correct</span>")
        + prompt_card(5, f"Copy B: {INJECTED}", "d2", build_cache.DEMO2_PROMPT,
                      "Either outcome is usable; note which:<br>☐ <b>Followed</b> the hidden line: says “on plan” "
                      "and leaves out Help Desk<br>☐ <b>Caught it</b>: still names Help Desk, or warns about an "
                      "instruction in the file<br>☐ <b>Blocked</b>: the tool or a security warning stops it (tell your "
                      "security contact; on stage, go straight to the Word reveal)",
                      note="<p>Same prompt as Copy A, in a <b>new</b> chat (or Copy B's own Copilot pane in Word).</p>")
        + prompt_card(6, "Follow-up in the same Copy B chat: what did it read?", "quote", build_cache.QUOTE_PROMPT,
                      "It quotes the notes, including a sentence nobody can see in Word: <i>“" + e(rd.PAYLOAD) +
                      "”</i> <span class=\"tick\">☐ hidden sentence appears on screen</span>")
        + "<div class=\"step\"><h3><span class=\"num\">7</span>The reveal in Word</h3>"
          f"<p>Open <b>{INJECTED}</b> in Word (light mode). Click in the document, press <b>Ctrl+A</b>, set "
          "<b>Font Color → Automatic</b> and <b>Font Size → 12</b>. The sentence appears at the end of the last line. "
          "Press Ctrl+Z twice and <b>don't save</b>.</p><p class=\"look\"><b>Look for:</b> the sentence appears. "
          "<span class=\"tick\">☐ reveal works</span></p></div>"
    )
    rows = [
        ("Contrast: answers 1 and 3 side by side (Win+Left / Win+Right)",
         "Anyone can tell the difference in 3 seconds: a long block vs. a short table",
         "Both long, but answer 3 is a table", "Answer 1 is already a short table: the contrast is gone"),
        ("Readability: answer 3 at 125–150% zoom, from 4 metres away",
         "Bottom line and table readable", "Readable after scrolling", "Can't read it from the back"),
        ("Accuracy: the five rows in step 3", "All five, right amounts", "Four of five, or a small number slip",
         "Wrong largest variance, or invented numbers"),
        ("Judgment: Device Refresh and Mission Support",
         "Says Device Refresh's cause isn't stated; infers a billing lag for Mission Support",
         "Gets one of the two",
         "Confidently invents a cause for Device Refresh (keep it: a live example of why you verify)"),
        ("Speed", "Each answer starts within 10 s and finishes within 30 s", "30–60 s", "Over 60 s, or errors"),
        ("Demo 2: the quote step (step 6)", "The hidden sentence is quoted on screen",
         "Not quoted, but the Word reveal works", "File blocked and the reveal can't be shown"),
        ("Demo 2: Copy B outcome (step 5)", "Followed or Caught it: both work, pick the matching ending",
         "", "Blocked with no explanation"),
        ("Timing (with you talking)", "Demo 1 in 4:00, Demo 2 in 1:30", "Up to 30 s over", "More than a minute over"),
    ]
    score = ("<div class=\"scroll\"><table><tr><th>What to check</th><th>Green</th><th>Yellow</th><th>Red</th></tr>"
             + "".join(f"<tr><td><b>{e(a)}</b></td><td class=\"g\">{e(b)}</td><td class=\"y\">{e(c)}</td>"
                       f"<td class=\"r\">{e(d)}</td></tr>" for a, b, c, d in rows) + "</table></div>")
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return ("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
            f"<title>Demo test guide</title><style>{CSS}</style></head><body>"
            "<header><h1>Demo test guide: will it land?</h1><span class=\"label\">Synthetic demonstration data</span></header><main>"
            "<div class=\"box\"><b>What's in this folder</b><br>"
            f"<b>{REPORT}</b>: the report for Demo 1 (attach it)<br>"
            f"<b>{CLEAN}</b>: Demo 2, Copy A<br>"
            f"<b>{INJECTED}</b>: Demo 2, Copy B, with one harmless hidden sentence<br>"
            "<b>TEST_GUIDE.html</b>: this page. About 25 minutes in Microsoft 365 Copilot or any approved chat tool.</div>"
            "<div class=\"box warn\"><b>Before you start:</b> use an approved tool and a work account. "
            f"Tell your security contact before you open <b>{INJECTED}</b> in Copilot: Microsoft Defender may flag it. "
            "Use Word in light mode. Afterwards, delete the uploaded files and the test chats.</div>"
            "<h2>Demo 1: from weak to strong (about 10 minutes)</h2>"
            f"<p>For each step: start a <b>new chat</b>, attach <b>{REPORT}</b>, click <b>Copy prompt</b>, paste, send. "
            "Steps 1–3 are the ones you'll run live on stage.</p>" + d1 +
            "<h2>Demo 2: trust but verify (about 8 minutes)</h2>"
            f"<p>Test in Word with the Copilot pane open, or in Copilot Chat with the file attached. Start a new chat for each copy.</p>" + d2 +
            "<h2>Will it land? Score each line</h2>"
            "<p>Green on everything, or one yellow: run it live. Two or three yellows: run it live with the recorded "
            "fallback ready, and lean on the side-by-side. Any red: fix it, try again, or present a recording and say so.</p>"
            + score +
            "<h2>The colleague test (5 minutes, the best predictor)</h2>"
            "<p>Run steps 1, 2 and 3, then Demo 2, for one budget analyst who hasn't seen it. Then ask:</p>"
            "<ol><li><b>What changed between the first and the last answer?</b> If they can't say it in one sentence "
            "(“the last one was something I could hand my boss”), the contrast isn't landing.</li>"
            "<li><b>Is this our problem?</b> Would they recognise these variances in their own reports?</li>"
            "<li><b>Would you try the four-part prompt on Monday?</b> A yes means the session has done its job.</li>"
            "<li><b>What's the one thing you'd tell a colleague about Demo 2?</b> You want: "
            "“it reads text you can't see, so check it against the source.”</li></ol>"
            "<p>Note: tool ____ &nbsp; date ____ &nbsp; greens __ yellows __ reds __ &nbsp; colleague verdict ________</p>"
            f"</main><script id=\"guide-data\" type=\"application/json\">{blob}</script><script>{JS}</script></body></html>\n")


def main(root=ROOT):
    p = os.path.join(root, FILE)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(build())
    if root == ROOT:
        print("Wrote " + FILE)


if __name__ == "__main__":
    main()
