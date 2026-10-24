#!/usr/bin/env python3
"""Build paste-ready text for running Demo 1 in ANY chat tool (no upload needed).

Writes chat-kit/paste/:
  demo1_1_weak.txt ... demo1_5_output.txt   report text (the CSV) followed by that stage's prompt
  demo2_prompt.txt                          the Demo 2 prompt alone (the report is copied from Word live)

Clean Demo 1 material: only the report's own text and the prompts. Preflight rebuilds
these files and checks they are byte-identical and contain no hidden instruction.

Usage:  python3 scripts/build_paste_blocks.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_cache  # noqa: E402
import office_text  # noqa: E402

ROOT = build_cache.ROOT
STAGES = ["weak", "role", "task", "context", "output"]
FILES = [f"chat-kit/paste/demo1_{i}_{s}.txt" for i, s in enumerate(STAGES, 1)] + ["chat-kit/paste/demo2_prompt.txt"]


def paste_block(prompt, file_name, file_text):
    return (f"Attached file: {file_name}\n----- start of file -----\n{file_text.rstrip()}\n"
            f"----- end of file -----\n\n{prompt}\n")


def main(root=ROOT):
    csv = office_text.csv_text(os.path.join(ROOT, "data", "fy26_q3_execution_report.csv"))
    stages = build_cache.build_demo1({f"demo1_{s}": "" for s in STAGES})["stages"]
    out = os.path.join(root, "chat-kit", "paste")
    os.makedirs(out, exist_ok=True)
    for i, st in enumerate(stages, 1):
        with open(os.path.join(out, f"demo1_{i}_{st['id']}.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write(paste_block(st["prompt"], "fy26_q3_execution_report.csv", csv))
    with open(os.path.join(out, "demo2_prompt.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(build_cache.DEMO2_PROMPT + "\n")
    if root == ROOT:
        print("Wrote chat-kit/paste/ (5 Demo 1 paste blocks + Demo 2 prompt)")


if __name__ == "__main__":
    main()
