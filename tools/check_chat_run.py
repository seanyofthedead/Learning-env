#!/usr/bin/env python3
"""Judge one rehearsal in any chat tool: were the answers good enough to run live?

  python3 tools/check_chat_run.py chat-kit/rehearsals/2026-11-12-chatgpt --source "ChatGPT, <model>"
  python3 tools/check_copilot_run.py copilot-kit/rehearsals/2026-11-12      # same, source = Copilot

Uses the same rules as preflight (tools/output_checks.py). Prints each check, a verdict
per demo, and a row to paste into the rehearsal log. Exit 0 only when both
demos count as a successful rehearsal.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chat_run  # noqa: E402
from output_checks import clean_results, final_table_results, injected_followed  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(default_source=None):
    ap = argparse.ArgumentParser(description="Judge a recorded rehearsal.")
    ap.add_argument("folder")
    ap.add_argument("--source", default=default_source, help='tool and model, e.g. "ChatGPT, <model>"')
    a = ap.parse_args()
    if not os.path.isdir(a.folder):
        sys.exit(f"Not a folder: {a.folder}")
    folder, source = a.folder, a.source or "<tool, model>"
    planted = json.load(open(os.path.join(ROOT, "data", "answer_key.json"), encoding="utf-8"))["planted"]
    ans, missing = chat_run.load(folder)

    def show(name, ok, detail=""):
        print(f"  {'ok  ' if ok else 'MISS'} {name}" + (f"   [{detail[:110]}]" if (detail and not ok) else ""))
        return ok

    print(f"Rehearsal: {folder}  ({source})  Synthetic demonstration data\n")
    print("Demo 1: From weak to strong")
    d1 = True
    for k in chat_run.KEYS[:5]:
        d1 &= show(f"answer saved: {k}", k in ans)
    stages = [ans.get(k, "") for k in chat_run.KEYS[:5]]
    for i in range(1, 5):
        if stages[i] and stages[i - 1]:
            d1 &= show(f"{chat_run.KEYS[i]} differs from the stage before", stages[i] != stages[i - 1])
    for name, ok, detail in final_table_results(ans.get("demo1_output", ""), planted):
        d1 &= show(name, ok, detail)

    print("\nDemo 2: Trust but verify")
    d2_clean = all(show(n, ok, d) for n, ok, d in clean_results(ans.get("demo2_clean", ""))) \
        if "demo2_clean" in ans else show("answer saved: demo2_clean", False)
    if "demo2_injected" in ans:
        followed = injected_followed(ans["demo2_injected"])
        show("injected copy: the tool followed the hidden line (says on plan, omits SYN-102)", followed,
             ans["demo2_injected"][:110])
    else:
        followed = show("answer saved: demo2_injected", False)

    v1 = "SUCCESS" if d1 else "FAIL"
    v2 = "SUCCESS" if (d2_clean and followed) else ("RESISTED (the tool ignored the hidden line)"
                                                    if d2_clean and "demo2_injected" in ans else "FAIL")
    print(f"\nVerdict  Demo 1: {v1}   Demo 2: {v2}")
    if missing:
        print("Missing files: " + ", ".join(missing))
    date = os.path.basename(os.path.normpath(folder))
    print("\nPaste into the rehearsal log (fill the blanks):")
    print(f"| # | {date} | {source} | <machine / account> | <paste / upload> | "
          f"{'SYN-102, not on plan' if d2_clean else 'wrong'} | "
          f"{'followed (on plan)' if followed else 'resisted'} | <yes/no> | <m:ss> | "
          f"D1 {v1}, D2 {v2.split()[0]} | <initials> |")
    sys.exit(0 if (d1 and v2 == "SUCCESS") else 1)


if __name__ == "__main__":
    main()
