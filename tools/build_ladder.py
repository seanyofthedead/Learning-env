#!/usr/bin/env python3
"""Build the Demo 1 ladder sheet (maintainers only).

Writes the same page to copilot-kit/DEMO1_LADDER.html and chat-kit/DEMO1_LADDER.html:
one card per step with the prompt (newly added words highlighted), what was added, what
to look for in the answer, and copy buttons ("Copy prompt" and, for tools that can't take
attachments, "Copy report + prompt"). Works by double-click, prints cleanly, and can be
projected beside the chat tool so the room sees what changed.

Clean Demo 1 material: only the report text and the prompts. Preflight rebuilds it and
checks it is current. Usage:  python3 tools/build_ladder.py
"""
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_cache  # noqa: E402
import build_paste_blocks  # noqa: E402
import office_text  # noqa: E402

ROOT = build_cache.ROOT
FILES = ["copilot-kit/DEMO1_LADDER.html", "chat-kit/DEMO1_LADDER.html"]
REPORT = "fy26_q3_execution_report.xlsx"

CSS = """
:root{--c:#181818;--g:#96D200;--gt:#3D6200;--mut:#4D4D4D;--line:#C9CCC4;--soft:#F3F4F1}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--c);font-family:Arial,Helvetica,sans-serif;font-size:18px;line-height:1.4}
header{background:var(--c);color:#fff;border-bottom:6px solid var(--g);padding:14px 20px;display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center}
header h1{margin:0;font-size:26px}
.label{border:2px solid #fff;border-radius:6px;padding:2px 8px;font-weight:bold;font-size:18px}
main{max-width:1100px;margin:0 auto;padding:16px 20px 28px}
.how{background:var(--soft);border-left:8px solid var(--g);padding:10px 14px 10px 36px;margin:0 0 16px}
.how li{margin:4px 0}
.step{display:grid;grid-template-columns:56px minmax(0,1fr);gap:14px;border:1px solid var(--line);border-radius:10px;padding:14px;margin:0 0 14px;break-inside:avoid}
.num{width:48px;height:48px;border-radius:10px;background:var(--g);color:var(--c);font-weight:bold;font-size:26px;display:grid;place-items:center}
h2{margin:0 0 6px;font-size:22px}
.adds{display:block;font-size:18px;font-weight:normal;color:var(--mut);margin-top:2px}
.prompt{background:#fff;border:1px solid var(--line);border-left:6px solid var(--g);border-radius:6px;padding:10px 12px;margin:8px 0;font-size:20px}
.prompt .old{color:var(--mut)}
mark{background:var(--g);color:var(--c);font-weight:bold;padding:0 3px;border-radius:3px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.look{margin:8px 0}
.look b{color:var(--gt)}
.btns{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;margin-top:8px}
button{font:inherit;font-weight:bold;padding:6px 14px;border-radius:8px;border:2px solid var(--c);background:#fff;color:var(--c);cursor:pointer}
button.primary{background:var(--c);color:#fff}
.status{color:var(--gt);font-weight:bold}
.point{border:3px solid var(--g);border-radius:10px;padding:12px 14px;font-weight:bold}
@media (max-width:640px){.step{grid-template-columns:1fr}}
@media print{header{background:#fff;color:var(--c);border-bottom:4px solid var(--c)}.label{border-color:var(--c)}
 .btns,.how li.screen{display:none}mark{background:none;text-decoration:underline;text-decoration-thickness:3px}
 .num{border:3px solid var(--c);background:#fff}body{font-size:14px}.prompt{font-size:15px}}
"""

JS = """
(function(){
  var data = JSON.parse(document.getElementById('ladder-data').textContent);
  function fallbackCopy(t){
    var ta = document.createElement('textarea'); ta.value = t; ta.setAttribute('readonly', '');
    ta.style.position = 'fixed'; ta.style.top = '0'; ta.style.left = '0'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select(); var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta); return ok;
  }
  function say(el, ok){ el.textContent = ok ? 'Copied. Paste it into a new chat.' : 'Copy blocked here: select the prompt text and copy it by hand.'; }
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


def build_page():
    e = html.escape
    stages = build_cache.load_json("content", "demo1.json")["stages"]
    csv = office_text.csv_text(os.path.join(ROOT, "data", "fy26_q3_execution_report.csv"))
    data, cards = {}, []
    for i, st in enumerate(stages, 1):
        prompt = "".join(t for t, _, _ in st["segments"])
        data[f"p{i}"] = prompt
        data[f"b{i}"] = build_paste_blocks.paste_block(prompt, "fy26_q3_execution_report.csv", csv)
        segs = "".join(f"<mark>{e(t)}</mark>" if new else f"<span class=\"old\">{e(t)}</span>"
                       for t, _, new in st["segments"])
        cards.append(
            f"<section class=\"step\"><div class=\"num\">{i}</div><div>"
            f"<h2>{e(st['label'])}<span class=\"adds\">Adds: {e(st['adds_plain'])}</span></h2>"
            f"<p class=\"prompt\">{segs}</p>"
            f"<p class=\"look\"><b>Look for in the answer:</b> {e(st['look_for'])}</p>"
            f"<div class=\"btns\"><button class=\"primary\" data-copy=\"p{i}\">Copy prompt</button>"
            f"<button data-copy=\"b{i}\">Copy report + prompt</button>"
            f"<span class=\"status\" aria-live=\"polite\"></span></div></div></section>")
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return ("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
            f"<title>Demo 1 ladder</title><style>{CSS}</style></head><body>"
            "<header><h1>Demo 1: what changes at each step</h1>"
            "<span class=\"label\">Synthetic demonstration data</span></header><main>"
            "<ol class=\"how\">"
            "<li>Start a <b>new chat</b> for every step, so earlier answers don't carry over.</li>"
            f"<li class=\"screen\">Attach <b>{REPORT}</b> and click <b>Copy prompt</b>. If the tool can't take "
            "attachments, click <b>Copy report + prompt</b> instead and attach nothing.</li>"
            "<li>Paste, send, then check the answer against <b>Look for</b>. Green words are new at that step.</li>"
            "</ol>" + "".join(cards) +
            "<p class=\"point\">The point for the room: put the answers to step 1 and step 5 side by side. "
            "Same report, same AI. Only the prompt changed.</p>"
            f"</main><script id=\"ladder-data\" type=\"application/json\">{blob}</script>"
            f"<script>{JS}</script></body></html>\n")


def main(root=ROOT):
    page = build_page()
    for rel in FILES:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(page)
    if root == ROOT:
        print("Wrote " + ", ".join(FILES))


if __name__ == "__main__":
    main()
