#!/usr/bin/env python3
"""Build research coverage, without selecting suppliers or changing quotes."""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent
DOMAINS = ("venues", "food", "design", "style", "services", "admin")
with (OUTPUT / "budget_quote_tracker.csv").open(newline="") as handle:
    budget_rows = list(csv.DictReader(handle))
known_items = {row["Item"] for row in budget_rows}
sections = []
routes = defaultdict(list)
catalog = []
for domain in DOMAINS:
    report = f"research/fulfillment_{domain}.md"
    data = json.loads((OUTPUT / "research" / f"fulfillment_{domain}.json").read_text())
    assert (OUTPUT / report).exists(), report
    for section in data["sections"]:
        key = f"{domain}/{section['id']}"
        names = [v["name"] for v in section["vendors"]]
        for item in section["budget_items"]:
            assert item in known_items, (key, "unknown budget item", item)
            routes[item].append((key, section["title"], names, report, section["vendors"]))
        sections.append({"id": key, "title": section["title"], "report": report,
                         "budget_scope": section["budget_scope"],
                         "budget_items": section["budget_items"], "vendors": section["vendors"]})
        for vendor in section["vendors"]:
            catalog.append({"Section": section["title"], "Provider": vendor["name"],
                            "Official_or_booking_record_link": vendor["url"],
                            "Published_price": vendor["published_price"],
                            "Price_year": vendor["price_year"],
                            "Budget_scope": section["budget_scope"],
                            "Scope": vendor["scope"], "Unresolved": vendor["gaps"],
                            "Availability": vendor["availability"], "Research_detail": report})

allowance_names = {
    "Flowers & decor sales tax allowance", "Flowers & decor uncommitted allowance",
    "Attire & beauty sales tax allowance",
}
coverage = []
for row in budget_rows:
    item = row["Item"]
    matched = routes[item]
    supplier_names = list(dict.fromkeys(name for entry in matched for name in entry[2]))
    links = list(dict.fromkeys(v["url"] for entry in matched for v in entry[4]))
    details = list(dict.fromkeys(entry[3] for entry in matched))
    if row["Must_have"] != "Y":
        status, owner = "Not funded", "No supplier selection; optional item excluded"
        supplier_names, links, details = [], [], []
    elif row["Workbook_status"] == "Booked":
        status, owner = "Existing booking; confirm contract scope", "We Love Photography"
    elif row["Workbook_status"] == "Gift":
        status, owner = "Gift; confirm scope and delivery", "Couple's brother / couple"
        supplier_names, links, details = [], [], ["approved_budget.md"]
    elif item in allowance_names:
        status, owner = "Budget control; no separate supplier", "Couple; reconcile selected supplier invoices"
        supplier_names, links, details = [], [], ["approved_budget.md"]
    else:
        assert matched, ("Unmapped funded item", item)
        status = "Options researched; selection and complete quote pending"
        owner = " / ".join(dict.fromkeys(entry[1] for entry in matched))
        if item == "Vendor tips":
            status, owner = "Payment ledger; no additional supplier", "Couple and selected coordinator"
    coverage.append({"Category": row["Category"], "Item": item,
                     "Approved_fixed_allocation": row["Current_fixed_target"],
                     "Budget_treatment": row["Budget_treatment"],
                     "Status": status, "Fulfillment_route_or_owner": owner,
                     "Provider_options": " | ".join(supplier_names),
                     "Viewable_links": " | ".join(links), "Research_detail": " | ".join(details),
                     "Scope_to_confirm": row["Scope_to_confirm"]})

assert len(coverage) == 85
assert sum(float(r["Approved_fixed_allocation"] or 0) for r in coverage) == 22406
assert sum(r["Status"] == "Not funded" for r in coverage) == 21
for name, rows in (("fulfillment_coverage.csv", coverage), ("vendor_catalog.csv", catalog)):
    with (OUTPUT / name).open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
index = {"checked_date": "2026-11-08", "approved_plan": "../budget/approved_plan.json",
         "warning": "Supplier routes and published prices are research, not selections, full quotes or confirmed 2027 availability.",
         "budget_rows": len(coverage), "sections": sections,
         "coverage_status_counts": dict(Counter(r["Status"] for r in coverage)),
         "provider_entries": len(catalog),
         "distinct_provider_names": len({r["Provider"] for r in catalog})}
(OUTPUT / "research/fulfillment_index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"rows": len(coverage), "sections": len(sections),
                  "provider_entries": len(catalog), "coverage": index["coverage_status_counts"]}, indent=2))
