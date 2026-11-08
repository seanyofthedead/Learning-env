#!/usr/bin/env python3
"""Read-only reconciliation of the workbook and the current wedding plan.

Run from any directory. Prints audit JSON; never changes the workbook or tracker.
The independent pre-approval reconstruction is in research/budget_math_audit.json.
Current approved allocations come from budget/approved_plan.json.
"""
import importlib.util
import json
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("wedding_budget", ROOT / "budget/wedding_budget_model.py")
model = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = model
spec.loader.exec_module(model)

rows = model.parse_items()
priced_must = sum((Decimal(str(r["estimate"])) for r in rows
                   if r["must"] and r["estimate"] is not None), Decimal(0))
nonvenue = Decimal(str(model.nonvenue_total(185, trimmed=True)))
limit = Decimal("54545.45")
reserve = Decimal("5454.55")
assert limit + reserve == Decimal("60000")
assert len(rows) == 82
assert priced_must == Decimal("76658.13")
assert nonvenue == Decimal("22406")

scenarios = []
for label, venue in [("Current hard ceiling", Decimal("32139")),
                     ("Minimum $1,000 venue headroom", Decimal("31139")),
                     ("Approved venue shopping target", Decimal("30000"))]:
    total = venue + nonvenue
    scenarios.append(dict(label=label, venue_driven=float(venue),
                          other_spending=float(nonvenue), planned_spending=float(total),
                          unallocated_spending_headroom=float(limit-total),
                          protected_reserve=float(reserve),
                          quote_status="planning scenario, not an offer"))

findings = dict(
    workbook_rows=len(rows),
    priced_must_haves=float(priced_must),
    unpriced_must_haves=[r["item"] for r in rows if r["must"] and r["estimate"] is None],
    original_nonvenue=model.nonvenue_total(185),
    current_nonvenue=float(nonvenue),
    already_assumed_nonvenue_reductions=model.nonvenue_total(185)-float(nonvenue),
    strict_venue_envelope=32139,
    scenarios=scenarios,
    marginal_costs=dict(
        ten_dollars_all_in_per_guest=1850,
        ten_dollars_before_22pct_service_and_9pct_tax=round(185*10*1.22*1.09, 2),
        historical_five_more_tables_before_additional_tax=5*(100+12+30+20),
    ),
    limitations=["Targets are not supplier quotes.",
                 "Unknown required costs remain unknown, not zero.",
                 "No scenario authorizes spending the protected reserve.",
                 "Approved category caps remain fixed; actual table quantities and complete supplier quotes are still required."]
)
print(json.dumps(findings, indent=2))
