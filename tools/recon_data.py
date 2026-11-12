"""Single source of truth for Demo 3: property subledger to general ledger reconciliation.

Synthetic demonstration data. No real agency, vendor, personnel or program identifiers.
Dollars (not thousands). FY26 Q3, as of 30 June 2026. Three capitalized property accounts
(USSGL-style numbers): 1730 Buildings, Improvements and Renovations; 1750 Equipment;
1820 Leasehold Improvements.

Two reports, joined by document number:
  - Property subledger: one row per asset record in the property system.
  - General ledger detail: one row per posting to the three accounts in Q3.

Five planted breaks (the answer key; never written into the report files):
  B1 Duplicate      Equipment     asset entered twice in the subledger (same document)
  B2 Cutoff         Equipment     two assets acquired 29-30 June, not posted in the Q3 GL
  B3 Missing record Equipment     GL posting with no asset record in the subledger
  B4 Transposition  Buildings     418,600.00 keyed as 481,600.00 in the GL (difference / 9)
  B5 Misclass       Buildings /   leasehold build-out posted to 1730 in the GL; subledger
                    Leasehold     has it in 1820 (equal and opposite differences)
"""

LABEL = "Synthetic demonstration data"
LABEL_LINE = ("SYNTHETIC DEMONSTRATION DATA — not real agency, vendor, personnel "
              "or program information")
AS_OF = "30 June 2026"

ACCOUNTS = {
    "1730": "Buildings, Improvements and Renovations",
    "1750": "Equipment",
    "1820": "Leasehold Improvements",
}

SL_TITLE = "Property Subledger — Capitalized Property, FY26 Q3"
SL_SUBTITLE = ("Demonstration Directorate · Property accountability system extract · "
               "Asset records as of 30 June 2026 · Dollars")
SL_COLUMNS = ["Asset ID", "Document number", "Account", "Account title", "Description",
              "Acquisition date", "Date recorded", "Acquisition cost"]

GL_TITLE = "General Ledger Detail — Property Accounts 1730, 1750, 1820, FY26 Q3"
GL_SUBTITLE = ("Demonstration Directorate · Postings 1 April to 30 June 2026 · Dollars")
GL_COLUMNS = ["Document number", "Posting date", "Account", "Account title", "Description", "Amount"]

NOTE = "Prepared for training use only."

# (asset_id, document, account, description, acquisition_date, date_recorded, cost_cents)
# Costs in cents to keep arithmetic exact.
_SL = [
    ("PA-26-0101", "D26-0101", "1750", "Forklift, electric, 5,000 lb", "2026-04-03", "2026-04-06", 3895000),
    ("PA-26-0102", "D26-0102", "1750", "Server rack and UPS, data room A", "2026-04-07", "2026-04-09", 6420000),
    ("PA-26-0103", "D26-0103", "1750", "Network switch stack, Building 1", "2026-04-09", "2026-04-13", 5278000),
    ("PA-26-0104", "D26-0104", "1750", "Lab freezer, -80 C", "2026-04-14", "2026-04-15", 2764000),
    ("PA-26-0105", "D26-0105", "1750", "Electric utility cart", "2026-04-16", "2026-04-20", 3150000),
    ("PA-26-0106", "D26-0106", "1750", "Video conferencing system, Conference Center", "2026-04-21", "2026-04-23", 4530000),
    ("PA-26-0107", "D26-0107", "1750", "Large-format printer and plotter", "2026-04-24", "2026-04-27", 2687500),
    ("PA-26-0108", "D26-0108", "1750", "Floor scrubber, ride-on", "2026-04-28", "2026-04-30", 2940000),
    ("PA-26-0109", "D26-0109", "1750", "Storage array, 500 TB", "2026-05-01", "2026-05-05", 14260000),
    ("PA-26-0110", "D26-0110", "1750", "Mobile shelving system, records room", "2026-05-05", "2026-05-07", 3325000),
    ("PA-26-0111", "D26-0111", "1750", "Access control panels and badge readers", "2026-05-08", "2026-05-12", 5812500),
    ("PA-26-0112", "D26-0112", "1750", "Telehandler, 10,000 lb", "2026-05-12", "2026-05-14", 9680000),
    ("PA-26-0113", "D26-0113", "1750", "X-ray mail screening unit", "2026-05-15", "2026-05-19", 7450000),
    ("PA-26-0114", "D26-0114", "1750", "CNC lathe, maintenance shop", "2026-05-19", "2026-05-21", 8830000),
    ("PA-26-0115", "D26-0115", "1750", "Pallet racking system, warehouse bay 4", "2026-05-22", "2026-05-27", 4196000),
    ("PA-26-0116", "D26-0116", "1750", "Uninterruptible power system, 200 kVA", "2026-05-27", "2026-05-29", 11845000),
    ("PA-26-0117", "D26-0117", "1750", "Generator, 500 kW diesel", "2026-06-01", "2026-06-02", 18640000),
    ("PA-26-0118", "D26-0118", "1750", "Snow removal attachment set", "2026-06-04", "2026-06-08", 2390000),
    ("PA-26-0119", "D26-0119", "1750", "Audio-visual control system, auditorium", "2026-06-09", "2026-06-11", 3978000),
    ("PA-26-0120", "D26-0120", "1750", "Air compressor, 100 hp", "2026-06-12", "2026-06-15", 4725000),
    ("PA-26-0121", "D26-0121", "1750", "Commercial dishwasher, dining facility", "2026-06-16", "2026-06-17", 2560000),
    ("PA-26-0122", "D26-0122", "1750", "Spectrum analyzer", "2026-06-22", "2026-06-23", 6345000),
    ("PA-26-0123", "D26-0123", "1750", "Firewall appliance pair", "2026-06-24", "2026-06-25", 5490000),
    ("PA-26-0124", "D26-0117", "1750", "Generator, 500 kW diesel", "2026-06-01", "2026-06-26", 18640000),   # B1 duplicate
    ("PA-26-0125", "D26-0125", "1750", "Boom lift, 60 ft", "2026-06-29", "2026-06-30", 7290000),           # B2 cutoff
    ("PA-26-0126", "D26-0126", "1750", "Loading dock leveler set", "2026-06-30", "2026-06-30", 4135000),   # B2 cutoff
    ("PA-26-0201", "D26-0131", "1730", "HVAC chiller replacement, Building 1", "2026-04-10", "2026-04-14", 31240000),
    ("PA-26-0202", "D26-0132", "1730", "Elevator modernization, Building 3", "2026-04-30", "2026-05-04", 22875000),
    ("PA-26-0203", "D26-0133", "1730", "Roof replacement, Building 2", "2026-05-14", "2026-05-18", 41860000),   # B4 (GL keyed 481,600)
    ("PA-26-0204", "D26-0134", "1730", "Fire suppression upgrade, data room A", "2026-05-20", "2026-05-22", 16730000),
    ("PA-26-0205", "D26-0135", "1730", "Restroom renovation, Building 1", "2026-06-05", "2026-06-09", 9645000),
    ("PA-26-0206", "D26-0136", "1730", "Security vestibule, main entrance", "2026-06-11", "2026-06-12", 18490000),
    ("PA-26-0207", "D26-0137", "1730", "Boiler replacement, Building 3", "2026-06-19", "2026-06-22", 25530000),
    ("PA-26-0208", "D26-0138", "1730", "Window replacement, Building 2", "2026-06-23", "2026-06-25", 13980000),
    ("PA-26-0301", "D26-0141", "1820", "Interior build-out, leased suite 120", "2026-04-17", "2026-04-21", 19850000),
    ("PA-26-0302", "D26-0142", "1820", "Interior build-out, leased suite 210", "2026-05-06", "2026-05-08", 26500000),  # B5 (GL in 1730)
    ("PA-26-0303", "D26-0143", "1820", "Cabling and data drops, leased suite 120", "2026-05-13", "2026-05-15", 4680000),
    ("PA-26-0304", "D26-0144", "1820", "Lighting retrofit, leased warehouse", "2026-05-29", "2026-06-02", 5830000),
    ("PA-26-0305", "D26-0145", "1820", "Conference room fit-out, leased suite 210", "2026-06-08", "2026-06-10", 7265000),
    ("PA-26-0306", "D26-0146", "1820", "Security upgrades, leased suite 300", "2026-06-15", "2026-06-17", 6120000),
]

# GL descriptions are the ledger's own short text (upper case, abbreviated), as a real
# extract would show. Posting dates trail acquisition by a few days.
_GL_DESC = {
    "D26-0101": "FORKLIFT ELEC 5000LB", "D26-0102": "SERVER RACK/UPS DATA RM A",
    "D26-0103": "NETWORK SWITCH STACK BLDG 1", "D26-0104": "LAB FREEZER -80C",
    "D26-0105": "ELEC UTILITY CART", "D26-0106": "VTC SYSTEM CONF CTR",
    "D26-0107": "LG FORMAT PRINTER/PLOTTER", "D26-0108": "FLOOR SCRUBBER RIDE-ON",
    "D26-0109": "STORAGE ARRAY 500TB", "D26-0110": "MOBILE SHELVING RECORDS RM",
    "D26-0111": "ACCESS CTRL PANELS/READERS", "D26-0112": "TELEHANDLER 10000LB",
    "D26-0113": "XRAY MAIL SCREENING UNIT", "D26-0114": "CNC LATHE MAINT SHOP",
    "D26-0115": "PALLET RACKING WHSE BAY 4", "D26-0116": "UPS 200KVA",
    "D26-0117": "GENERATOR 500KW DIESEL", "D26-0118": "SNOW REMOVAL ATTACHMENTS",
    "D26-0119": "AV CONTROL SYS AUDITORIUM", "D26-0120": "AIR COMPRESSOR 100HP",
    "D26-0121": "COMMERCIAL DISHWASHER DFAC", "D26-0122": "SPECTRUM ANALYZER",
    "D26-0123": "FIREWALL APPLIANCE PAIR", "D26-0158": "UTILITY TRUCK 4X4",
    "D26-0131": "HVAC CHILLER REPL BLDG 1", "D26-0132": "ELEVATOR MODERNIZATION BLDG 3",
    "D26-0133": "ROOF REPLACEMENT BLDG 2", "D26-0134": "FIRE SUPPRESSION UPG DATA RM A",
    "D26-0135": "RESTROOM RENOVATION BLDG 1", "D26-0136": "SECURITY VESTIBULE MAIN ENT",
    "D26-0137": "BOILER REPLACEMENT BLDG 3", "D26-0138": "WINDOW REPLACEMENT BLDG 2",
    "D26-0141": "INTERIOR BUILDOUT SUITE 120", "D26-0142": "INTERIOR BUILDOUT SUITE 210",
    "D26-0143": "CABLING/DATA DROPS SUITE 120", "D26-0144": "LIGHTING RETROFIT LEASED WHSE",
    "D26-0145": "CONF RM FIT-OUT SUITE 210", "D26-0146": "SECURITY UPG SUITE 300",
}

DUPLICATE_ASSET = "PA-26-0124"            # B1
CUTOFF_DOCS = ["D26-0125", "D26-0126"]    # B2
MISSING_SL = ("D26-0158", "2026-06-18", "1750", 5870000)   # B3: in the GL only
TRANSPOSED = ("D26-0133", 48160000)       # B4: GL amount
MISCLASS = ("D26-0142", "1730")           # B5: GL account


def _plus_days(date, n):
    y, m, d = (int(p) for p in date.split("-"))
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    d += n
    while d > days[m - 1]:
        d -= days[m - 1]
        m += 1
    return f"{y:04d}-{m:02d}-{d:02d}"


def money(cents):
    return f"{cents // 100:,}.{cents % 100:02d}" if cents >= 0 else "-" + money(-cents)


def sl_rows():
    return [{"asset": a, "doc": doc, "account": acct, "title": ACCOUNTS[acct], "desc": desc,
             "acquired": acq, "recorded": rec, "cents": c}
            for a, doc, acct, desc, acq, rec, c in _SL]


def gl_rows():
    rows = []
    seen = set()
    for a, doc, acct, desc, acq, rec, c in _SL:
        if a == DUPLICATE_ASSET or doc in CUTOFF_DOCS or doc in seen:
            continue
        seen.add(doc)
        if doc == TRANSPOSED[0]:
            c = TRANSPOSED[1]
        if doc == MISCLASS[0]:
            acct = MISCLASS[1]
        rows.append({"doc": doc, "posted": _plus_days(acq, 3), "account": acct, "title": ACCOUNTS[acct],
                     "desc": _GL_DESC[doc], "cents": c})
    doc, posted, acct, c = MISSING_SL
    rows.append({"doc": doc, "posted": posted, "account": acct, "title": ACCOUNTS[acct],
                 "desc": _GL_DESC[doc], "cents": c})
    rows.sort(key=lambda r: (r["posted"], r["doc"]))
    return rows


def account_summary():
    out = []
    for acct, title in ACCOUNTS.items():
        sl = sum(r["cents"] for r in sl_rows() if r["account"] == acct)
        gl = sum(r["cents"] for r in gl_rows() if r["account"] == acct)
        out.append({"account": acct, "title": title, "sl": sl, "gl": gl, "diff": sl - gl})
    return out


def breaks():
    """The answer key: each break with its account effect (subledger minus GL, cents)."""
    sl = {r["asset"]: r for r in sl_rows()}
    dup = sl[DUPLICATE_ASSET]
    cut = [r for r in sl_rows() if r["doc"] in CUTOFF_DOCS]
    tr_sl = next(r for r in sl_rows() if r["doc"] == TRANSPOSED[0])
    mc = next(r for r in sl_rows() if r["doc"] == MISCLASS[0])
    return [
        {"id": "B1", "type": "Duplicate record", "account": "1750", "docs": [dup["doc"]],
         "assets": ["PA-26-0117", DUPLICATE_ASSET], "effect": {"1750": dup["cents"]},
         "why": "Same document and cost recorded twice in the property system (asset IDs PA-26-0117 and PA-26-0124, "
                "recorded 2 June and 26 June). The GL has it once.",
         "action": "Property team: confirm one physical generator and retire the duplicate record PA-26-0124.",
         "keywords": ["duplicate", "twice", "double"]},
        {"id": "B2", "type": "Cutoff / timing", "account": "1750", "docs": CUTOFF_DOCS,
         "assets": [r["asset"] for r in cut], "effect": {"1750": sum(r["cents"] for r in cut)},
         "why": "Acquired 29 and 30 June and recorded in the property system, but not posted in the Q3 GL.",
         "action": "Accounting: confirm the July postings; report as a timing difference, or accrue if material.",
         "keywords": ["timing", "cutoff", "cut-off", "period end", "quarter end", "july", "not yet posted", "late"]},
        {"id": "B3", "type": "Missing property record", "account": "1750", "docs": [MISSING_SL[0]],
         "assets": [], "effect": {"1750": -MISSING_SL[3]},
         "why": "Utility truck posted to Equipment in the GL with no asset record in the property system.",
         "action": "Property team: locate and tag the truck and add the asset record, or reverse the posting if it isn't ours.",
         "keywords": ["missing", "no asset record", "not in the subledger", "not recorded", "untagged", "no record"]},
        {"id": "B4", "type": "Transposition (keying error)", "account": "1730", "docs": [TRANSPOSED[0]],
         "assets": [tr_sl["asset"]], "effect": {"1730": tr_sl["cents"] - TRANSPOSED[1]},
         "why": "Roof replacement is 418,600.00 in the subledger and 481,600.00 in the GL. The 63,000.00 difference "
                "divides evenly by 9, the classic sign of transposed digits.",
         "action": "Accounting: check the invoice and correct the GL posting.",
         "keywords": ["transpos", "keying", "typo", "data entry", "digits", "divisible by 9", "418,600", "481,600"]},
        {"id": "B5", "type": "Misclassification", "account": "1730 / 1820", "docs": [MISCLASS[0]],
         "assets": [mc["asset"]], "effect": {"1820": mc["cents"], "1730": -mc["cents"]},
         "why": "Leased suite 210 build-out is in 1820 Leasehold Improvements in the subledger but posted to 1730 "
                "Buildings in the GL. Equal and opposite differences; no net effect.",
         "action": "Accounting: reclassify 265,000.00 from 1730 to 1820 in the GL.",
         "keywords": ["misclass", "reclass", "wrong account", "miscoded", "posted to 1730", "offset"]},
    ]


def check():
    """The breaks explain every account difference exactly."""
    summ = {s["account"]: s["diff"] for s in account_summary()}
    explained = {a: 0 for a in ACCOUNTS}
    for b in breaks():
        for a, v in b["effect"].items():
            explained[a] += v
    assert explained == summ, (explained, summ)
    assert (summ["1750"], summ["1730"], summ["1820"]) == (24195000, -32800000, 26500000), summ
    assert len(sl_rows()) == 40 and len(gl_rows()) == 38
    assert len({r["doc"] for r in gl_rows()}) == len(gl_rows()), "GL documents unique"
    return summ


if __name__ == "__main__":
    s = check()
    for row in account_summary():
        print(row["account"], row["title"], money(row["sl"]), money(row["gl"]), money(row["diff"]))
    print("total diff", money(sum(s.values())))
