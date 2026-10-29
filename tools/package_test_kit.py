#!/usr/bin/env python3
"""Package the lean test kit (maintainers only).

  python3 tools/package_test_kit.py [output_dir]      # default: ./release

Writes SDFM_demo_test_kit.zip with only four files: TEST_GUIDE.html (steps, prompts, what to
look for, scorecard) and the three demo files. The full presenter kit (runbooks, scripts,
fallback app) is still available with tools/package_kit.py.
"""
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_test_guide  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOP = "SDFM_demo_test_kit"
ZIP_TIME = (2026, 1, 1, 0, 0, 0)
FILES = {  # name in the zip: source in the repo
    "TEST_GUIDE.html": build_test_guide.FILE,
    "fy26_q3_execution_report.xlsx": "data/fy26_q3_execution_report.xlsx",
    "demo_report.docx": "demo2/demo_report.docx",
    "INJECTED_demo_report_DO_NOT_USE.docx": "demo2/INJECTED_demo_report_DO_NOT_USE.docx",
}


def main(out_dir=None):
    out_dir = out_dir or os.path.join(ROOT, "release")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{TOP}.zip")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, src in FILES.items():
            info = zipfile.ZipInfo(f"{TOP}/{name}", date_time=ZIP_TIME)
            info.external_attr = 0o644 << 16
            with open(os.path.join(ROOT, src), "rb") as f:
                z.writestr(info, f.read(), compress_type=zipfile.ZIP_DEFLATED)
    print(f"Wrote {path} ({len(FILES)} files)")
    return path


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
