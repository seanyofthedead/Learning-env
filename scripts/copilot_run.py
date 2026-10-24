"""Read a folder of answers copied out of Microsoft 365 Copilot during a rehearsal.

Expected files (.md or .txt), one per answer, pasted with Copilot's Copy button:
  demo1_weak  demo1_role  demo1_task  demo1_context  demo1_output  demo2_clean  demo2_injected
"""
import os
import re

KEYS = ["demo1_weak", "demo1_role", "demo1_task", "demo1_context", "demo1_output",
        "demo2_clean", "demo2_injected"]

CITATIONS = [
    re.compile(r"\[\d+\]\([^)]*\)"),      # [1](https://...)
    re.compile(r"\[\^\d+\^\]"),           # [^1^]
    re.compile(r"【[^】]*】"),  # 【1†source】
    re.compile(r"(?<=\S)\[\d+\]"),        # word[1]
]


def clean_text(text):
    """Remove citation markers and turn tab-separated tables into markdown pipe tables."""
    text = text.replace("\r\n", "\n").replace(" ", " ")
    for c in CITATIONS:
        text = c.sub("", text)
    out, block = [], []

    def flush():
        if block:
            width = max(len(r) for r in block)
            rows = [r + [""] * (width - len(r)) for r in block]
            out.append("| " + " | ".join(rows[0]) + " |")
            out.append("|" + "---|" * width)
            out.extend("| " + " | ".join(c.replace("|", "/") for c in r) + " |" for r in rows[1:])
            block.clear()

    for line in text.split("\n"):
        if line.count("\t") >= 2 and not line.strip().startswith("|"):
            block.append([c.strip() for c in line.split("\t")])
        else:
            flush()
            out.append(line.rstrip())
    flush()
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()


def load(folder):
    """{key: cleaned text} and a list of missing keys."""
    found, missing = {}, []
    for k in KEYS:
        for ext in (".md", ".txt"):
            p = os.path.join(folder, k + ext)
            if os.path.exists(p):
                with open(p, encoding="utf-8-sig") as f:
                    t = clean_text(f.read())
                if t:
                    found[k] = t
                break
        if k not in found:
            missing.append(k)
    return found, missing
