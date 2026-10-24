#!/usr/bin/env python3
"""Make a recorded rehearsal (any chat tool) the app's fallback.

  python3 scripts/import_chat_run.py chat-kit/rehearsals/2026-11-12-chatgpt --source "ChatGPT, <model>"
  python3 scripts/import_copilot_run.py copilot-kit/rehearsals/2026-11-12    # same, source = Copilot
  ... --accept-resisted        # the tool ignored the hidden line; present the "caught it" ending
  python3 scripts/build_cache.py                                     # back to the representative outputs

Rewrites app/cache.json (and the copy inside index.html) with the answers the tool actually
gave, labelled "Recorded in <source> · <date>" on every answer panel,
then runs preflight. Prompts, documents and the presenter script are unchanged.
"""
import argparse
import datetime
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_cache  # noqa: E402
import chat_run  # noqa: E402


def main(default_source=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--source", default=default_source, required=default_source is None,
                    help='tool and model as it should appear on screen, e.g. "ChatGPT, <model>"')
    ap.add_argument("--date", help="recording date (default: date at the start of the folder name, else today)")
    ap.add_argument("--accept-resisted", action="store_true",
                    help="allow a run where the tool did not follow the hidden line")
    a = ap.parse_args()
    ans, missing = chat_run.load(a.folder)
    if missing:
        sys.exit("Missing answers: " + ", ".join(missing) + ". Nothing imported.")
    name = os.path.basename(os.path.normpath(a.folder))
    m = re.match(r"\d{4}-\d{2}-\d{2}", name)
    date = a.date or (m.group(0) if m else datetime.date.today().isoformat())
    build_cache.build(ans, {
        "mode": "chat-recorded", "model": a.source, "temperature": None,
        "generated_at": date,
        "note": f"Answers recorded live in {a.source} on {date} (rehearsal run), imported from {a.folder}.",
    })
    print(f"Imported {len(ans)} answers recorded in {a.source} on {date} into app/cache.json.")
    cmd = [sys.executable, os.path.join(build_cache.ROOT, "scripts", "preflight.py")]
    if a.accept_resisted:
        cmd.append("--accept-resisted")
    r = subprocess.run(cmd, capture_output=True, text=True)
    print("Preflight: " + r.stdout.strip())
    if r.returncode:
        print("The cache now holds this run but does not pass. Re-record, re-import, or restore the\n"
              "representative cache with: python3 scripts/build_cache.py")
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
