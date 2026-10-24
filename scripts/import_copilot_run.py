#!/usr/bin/env python3
"""Make a recorded Copilot rehearsal the app's fallback.

  python3 scripts/import_copilot_run.py copilot-kit/rehearsals/2026-11-12
  python3 scripts/import_copilot_run.py <folder> --accept-resisted   # Copilot ignored the hidden line
  python3 scripts/build_cache.py                                     # back to the representative outputs

Rewrites app/cache.json (and the copy inside index.html) with the answers Copilot actually
gave, labelled "Recorded live in Microsoft 365 Copilot on <date>" on every answer panel,
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
import copilot_run  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--date", help="recording date (default: folder name if YYYY-MM-DD, else today)")
    ap.add_argument("--accept-resisted", action="store_true",
                    help="allow a run where Copilot did not follow the hidden line")
    a = ap.parse_args()
    ans, missing = copilot_run.load(a.folder)
    if missing:
        sys.exit("Missing answers: " + ", ".join(missing) + ". Nothing imported.")
    name = os.path.basename(os.path.normpath(a.folder))
    date = a.date or (name if re.fullmatch(r"\d{4}-\d{2}-\d{2}", name) else datetime.date.today().isoformat())
    build_cache.build(ans, {
        "mode": "copilot-recorded", "model": "Microsoft 365 Copilot", "temperature": None,
        "generated_at": date,
        "note": f"Answers recorded live in Microsoft 365 Copilot on {date} (rehearsal run), imported "
                f"from {a.folder}.",
    })
    print(f"Imported {len(ans)} Copilot answers recorded {date} into app/cache.json.")
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
