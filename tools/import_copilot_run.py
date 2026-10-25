#!/usr/bin/env python3
"""Make a recorded Microsoft 365 Copilot rehearsal the app's fallback.
Same as import_chat_run.py with the source set.

  python3 tools/import_copilot_run.py copilot-kit/rehearsals/2026-11-12 [--accept-resisted]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import import_chat_run  # noqa: E402

if __name__ == "__main__":
    import_chat_run.main(default_source="Microsoft 365 Copilot")
