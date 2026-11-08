#!/usr/bin/env python3
"""Apply approved targets without overwriting quote or payment information."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = json.loads((ROOT / "budget/approved_plan.json").read_text())
PATH = ROOT / "output/budget_quote_tracker.csv"

with PATH.open(newline="") as handle:
    reader = csv.DictReader(handle)
    fields = list(reader.fieldnames)
    rows = list(reader)

for field in ("Previous_fixed_target", "Allocation_status", "Approval_date"):
    if field not in fields:
        fields.append(field)

by_name = {row["Item"]: row for row in rows}
for allocation in PLAN["nonvenue_allocations"]:
    name = allocation["item"]
    if name not in by_name:
        row = {field: "" for field in fields}
        row.update(Category=allocation["category"], Item=name, Must_have="Y",
                   Workbook_status="Approved plan addition")
        rows.append(row)
        by_name[name] = row
    row = by_name[name]
    if not row.get("Approval_date"):
        row["Previous_fixed_target"] = row.get("Current_fixed_target", "")
    row["Current_fixed_target"] = str(allocation["amount"])
    row["Allocation_status"] = allocation["status"]
    row["Approval_date"] = PLAN["approved_date"]
    row["Scope_to_confirm"] = allocation["scope"]
    row["Budget_treatment"] = "Approved non-venue allocation; within existing category cap"

assert len(rows) == 85
assert sum(float(r["Current_fixed_target"] or 0) for r in rows) == PLAN["nonvenue_total"]
with PATH.open("w", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
print("Updated 85 tracker rows: 82 workbook items plus 3 approved tax/allowance lines.")
