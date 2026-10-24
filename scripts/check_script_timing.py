#!/usr/bin/env python3
"""Check every presenter cue can be spoken in its time slot.

Rate: 2.6 words/second (about 155 words a minute, a calm conference pace). Room
questions with a pause reserve 6 s in full versions (the presenter waits for answers)
and 2 s in compressed ones (asked, not waited on). Expands {outputs} to its longest form.
Prints one line per cue and exits non-zero if any cue is over.
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATE = 2.6
OUTPUTS = "The answers were pre-generated, as representative examples, so the demo runs the same every time."

def words(t):
    t = t.replace("{outputs_short}", "Answers are pre-generated.").replace("{outputs}", OUTPUTS)
    t = re.sub(r"\[[^\]]*\]", "", t)  # stage directions in [brackets] are not spoken
    return len(re.findall(r"[A-Za-z0-9’'-]+", t))

def main():
    d = json.load(open(os.path.join(ROOT, "content", "presenter.json"), encoding="utf-8"))
    bad = 0
    for demo in ("demo1", "demo2"):
        for name, v in d[demo]["versions"].items():
            for c in v["cues"]:
                branch = max(words(c.get("if_followed", "")), words(c.get("if_resisted", "")))
                n = words(c["say"]) + (words(c["ask"]) if c.get("ask") else 0) + branch
                pause = (6 if name in ("full", "copilot") else 2) if c.get("ask") else 0
                need = n / RATE + pause
                ok = need <= c["seconds"]
                bad += not ok
                print(f"{'ok  ' if ok else 'OVER'} {demo}/{name:4} step {c['step']} {c['label']:<13} {n:3d} words  needs {need:5.1f}s of {c['seconds']}s")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
