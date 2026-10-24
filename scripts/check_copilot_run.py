#!/usr/bin/env python3
"""Judge one Microsoft 365 Copilot rehearsal. Same as check_chat_run.py with the source set.

  python3 scripts/check_copilot_run.py copilot-kit/rehearsals/2026-11-12
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_chat_run  # noqa: E402

if __name__ == "__main__":
    check_chat_run.main(default_source="Microsoft 365 Copilot")
