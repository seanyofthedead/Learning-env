#!/usr/bin/env python3
"""Venue-neutral wedding budget model (Sean & Leila, Nov 2027).

Source of historical workbook figures: venue_neutral_items.md (same folder) -- the
couple's 10 categories / 82 items with mid-range DC-area estimates, with ALL
venue-specific content removed. No venue the couple already looked at is used
or named here; the agent keeps its own exclusion list (see EXCLUSION_FILE).

What it does
  1. Rebuilds the non-venue total from the items file ($31,475 at 185 guests),
     scaling centerpieces (per table of 10), specialty linens
     (tables*20 + guests*3) and the florist fee (12% of florals); vendor meals
     and everything else stay flat.
  2. Approved allocations come from approved_plan.json. The $5,454.55 reserve
     is protected, spending is capped at $54,545.45 and venue costs at $32,139.
     Guest-count sensitivities do not change the approved 185-person plan.
  3. evaluate(Venue, guests) -> all-in venue cost (rental, F&B, service, tax,
     missing rentals, cake, getting-ready, parking, extra hours, fees, 2027
     escalation) + must-have check + fit verdict.
  4. Search-filter solvers (max package $/guest, max F&B minimum, max rental,
     max hourly rate) used to brief the venue scout.

Run:  python3 wedding_budget_model.py            # tests + report
      python3 wedding_budget_model.py --json     # machine-readable report
      python3 wedding_budget_model.py --venue candidate.json --guests 185

ASSUMPTIONS are labelled "ASSUMPTION" -- confirm or replace with real quotes.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEMS_MD = HERE / "venue_neutral_items.md"
EXCLUSION_FILE = HERE / "excluded_venues.txt"   # one name per line, kept by the couple
APPROVED_PLAN_FILE = HERE / "approved_plan.json"

BUDGET = 60_000.0
CONTINGENCY = 0.10
BASE_GUESTS = 185

# --------------------------------------------------------------------------
# 1. Items file -> non-venue total
# --------------------------------------------------------------------------

# Items whose cost is driven by the venue choice: they live INSIDE the envelope.
ENVELOPE_ITEMS = {
    # Venue & ceremony
    "Reception venue", "Ceremony space (indoor)", "Cocktail hour space",
    "Guest tables & chairs", "Setup & breakdown labor", "Getting-ready suite",
    "Guest parking", "Basic table linens & napkins", "China, glassware & flatware",
    "Dance floor", "Rental delivery & late-night pickup",
    "Extra hour for décor setup", "Liquor license",
    # Food & drink (all but vendor meals)
    "Hors d'oeuvres + dinner", "Catering service staff", "Bartenders",
    "Bar / alcohol", "Soft drinks, coffee & tea", "Caterer service charge (~20%)",
    "Sales tax (~6%)", "Cake cutting", "Wedding cake", "Cake tasting & delivery",
}

FLORAL_ITEMS = [  # base of the florist delivery & setup fee (12%)
    "Bridal bouquet", "Boutonnieres & corsages", "Ceremony florals",
    "Ceremony backdrop / arch", "Centerpieces", "Cocktail, bar & cake flowers",
    "Candles (hurricanes & votives)",
]
FLORIST_FEE_PCT = 0.12
CENTERPIECE_PER_TABLE = 150.0
CENTERPIECE_PER_TABLE_TRIMMED = 100.0

TRIMS = {  # historical reduction assumptions; superseded by approved_plan.json
    "Day-of coordinator": 2500, "Videographer": 1800, "DJ / MC": 1500,
    "Vendor tips": 2000, "Wedding bands": 1200, "Wedding dress": 1200,
    "Groom's suit / tux": 300, "Hair & makeup trials": 125,
    "Candles (hurricanes & votives)": 1000, "Ceremony backdrop / arch": 0,
}
LOCKED = {"Photographer": 750.0}  # Booked: We Love Photography


def parse_items(path: Path = ITEMS_MD) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| ") or line.startswith("| Category") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6:
            continue
        cat, item, must, est, firm, note = cells[:6]
        try:
            value = float(est)
        except ValueError:
            value = None  # "(venue provides/prices)" / "(depends on venue)"
        rows.append(dict(category=cat, item=item, must=(must == "Y"),
                         estimate=value, firm=firm, note=note))
    return rows


ITEMS = parse_items()
CATEGORIES = list(dict.fromkeys(r["category"] for r in ITEMS))


def tables(guests: int) -> int:
    return math.ceil(guests / 10)


def approved_plan() -> dict:
    """The approved allocations are targets, never evidence of supplier prices."""
    plan = json.loads(APPROVED_PLAN_FILE.read_text(encoding="utf-8"))
    allocations = plan["nonvenue_allocations"]
    names = [r["item"] for r in allocations]
    required = {r["item"] for r in ITEMS if r["must"] and r["item"] not in ENVELOPE_ITEMS}
    if len(names) != len(set(names)) or not required.issubset(names):
        raise ValueError("Approved plan must uniquely cover every required non-venue item")
    if any(r["category"] not in CATEGORIES or r["amount"] < 0 for r in allocations):
        raise ValueError("Invalid approved allocation category or negative amount")
    if round(sum(r["amount"] for r in allocations), 2) != 22406:
        raise ValueError("Approved non-venue allocations must total $22,406")
    if round(plan["spend_limit"] + plan["reserve"], 2) != BUDGET:
        raise ValueError("Spending limit plus protected reserve must equal $60,000")
    if plan["guests"] != BASE_GUESTS or plan["venue_hard_cap"] != 32139 or plan["venue_fit_cap"] != 31139:
        raise ValueError("Approved guest count and venue policy must retain locked requirements")
    amounts = {r["item"]: r["amount"] for r in allocations}
    if amounts["Photographer"] != LOCKED["Photographer"]:
        raise ValueError("Booked photographer allocation must remain $750")
    totals = {category: sum(r["amount"] for r in allocations if r["category"] == category)
              for category in CATEGORIES}
    expected = {"Venue & ceremony": 2235, "Food & drink": 400,
                "Planning & legal": 5250, "Flowers & décor": 5446,
                "Attire & beauty": 4375, "Photo & video": 2550,
                "Music & sound": 2000, "Stationery": 150,
                "Guests & transport": 0, "Pre/post events": 0}
    if totals != expected:
        raise ValueError("Approved allocations must preserve every locked category cap")
    return plan


def nonvenue_items(guests: int = BASE_GUESTS, trimmed: bool = False) -> dict[str, dict]:
    """Historical workbook, or approved allocations without assumed new savings.

    Approved fixed allocations remain unchanged in guest-count sensitivities;
    a different table/guest count requires a revised quote and allocation plan.
    """
    if trimmed:
        return {r["item"]: dict(category=r["category"], cost=float(r["amount"]),
                                 firm=r["status"], scope=r.get("scope", ""))
                for r in approved_plan()["nonvenue_allocations"]}
    t = tables(guests)
    out: dict[str, dict] = {}
    for r in ITEMS:
        if not r["must"] or r["item"] in ENVELOPE_ITEMS:
            continue
        name = r["item"]
        v = r["estimate"] or 0.0
        if name == "Centerpieces":
            v = t * CENTERPIECE_PER_TABLE
        elif name == "Specialty linens & chargers":
            v = t * 20 + guests * 3
        out[name] = dict(category=r["category"], cost=v, firm=r["firm"])
    floral_base = sum(out[n]["cost"] for n in FLORAL_ITEMS if n in out)
    out["Florist delivery & setup fee"]["cost"] = round(FLORIST_FEE_PCT * floral_base, 2)
    return out


def nonvenue_total(guests: int = BASE_GUESTS, trimmed: bool = False) -> float:
    return round(sum(v["cost"] for v in nonvenue_items(guests, trimmed).values()), 2)


def nonvenue_by_category(guests: int = BASE_GUESTS, trimmed: bool = False) -> dict[str, float]:
    by = {c: 0.0 for c in CATEGORIES}
    for v in nonvenue_items(guests, trimmed).values():
        by[v["category"]] += v["cost"]
    return {k: round(v, 2) for k, v in by.items()}


# --------------------------------------------------------------------------
# 2. Envelope
# --------------------------------------------------------------------------

def spend_limit(reading: int = 1) -> float:
    """Only spending that preserves the protected reserve is supported."""
    if reading != 1:
        raise ValueError("Spending the protected reserve is not an approved budget option")
    return float(approved_plan()["spend_limit"])


def envelope(guests: int = BASE_GUESTS, reading: int = 1, trimmed: bool = False) -> float:
    available = round(spend_limit(reading) - nonvenue_total(guests, trimmed), 2)
    return min(available, float(approved_plan()["venue_hard_cap"])) if trimmed else available


def envelope_table(guest_counts=(185,)) -> list[dict]:
    rows = []
    for g in guest_counts:
        for reading in (1,):
            a, t = envelope(g, reading, False), envelope(g, reading, True)
            rows.append(dict(guests=g, reading=reading,
                             nonvenue_as_is=nonvenue_total(g), nonvenue_trimmed=nonvenue_total(g, True),
                             envelope_as_is=a, envelope_trimmed=t,
                             per_guest_as_is=round(a / g, 2), per_guest_trimmed=round(t / g, 2)))
    return rows


# --------------------------------------------------------------------------
# 3. Taxes, catering, costing defaults
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Tax:
    food: float      # prepared food / catering (incl. staff, service charge)
    alcohol: float   # alcohol served on premises
    rental: float    # rented goods (linens, china, dance floor...)
    note: str = ""

# Checked Nov 2026 -- see report sources. Confirm with the venue/caterer's invoice.
TAX = {
    "WORKBOOK": Tax(0.06, 0.06, 0.06, "Workbook flat 6% (reproduces its own lines)"),
    "DC": Tax(0.10, 0.10, 0.07, "DC 10% restaurant/catered food & on-premises alcohol; general 6%, "
              "OTR 1 Oct 2025 notice: 7% from 1 Oct 2026 (some sources say delayed -- confirm)"),
    "MD": Tax(0.06, 0.09, 0.06, "MD 6%; alcohol 9% (lump-sum bills not itemized are taxed 9% in full)"),
    "VA": Tax(0.06, 0.06, 0.06, "NoVA 6% sales tax, locality with no meals tax -- confirm locality"),
    "VA-FAIRFAX": Tax(0.10, 0.10, 0.06, "6% + Fairfax County 4% meals tax from 1 Jan 2026 "
                      "(not in Herndon, Vienna, Clifton, Fairfax City, Falls Church -- own meals taxes)"),
    "VA-ARLINGTON": Tax(0.11, 0.11, 0.06, "6% + Arlington 5% meals tax (from 1 Jul 2025)"),
    "VA-ALEXANDRIA": Tax(0.11, 0.11, 0.06, "6% + Alexandria 5% meals tax"),
    "VA-PRINCE-WILLIAM": Tax(0.09, 0.09, 0.06, "6% + Prince William 3% meals tax from 1 Jan 2026; "
                            "outside catering depends on origin of sale -- confirm invoice"),
    "VA-VIENNA": Tax(0.10, 0.10, 0.06, "6% + Vienna 4% meals tax from 1 Jan 2026; "
                    "outside catering depends on origin of sale -- confirm invoice"),
    "VA-FAIRFAX-CITY": Tax(0.105, 0.105, 0.06, "6% + Fairfax City 4.5% meals tax; "
                          "outside catering depends on origin of sale -- confirm invoice"),
}


@dataclass
class Catering:
    """Per-guest catering structure. Defaults = workbook mid-range outside caterer."""
    food_pp: float = 95.0
    staff_pp: float = 25.0
    alcohol_pp: float = 35.0
    soft_pp: float = 4.0
    bartender_fee: float = 200.0
    guests_per_bartender: int = 75
    service_pct: float = 0.20
    service_on_bartenders: bool = False
    tax_on_service: bool = True
    includes_china: bool = False
    includes_basic_linens: bool = False
    includes_setup_breakdown: bool = False   # caterer sets/flips/strikes tables & chairs
    cake_cutting_pp: float = 2.0
    holds_liquor_license: bool = True        # licensed caterer -> no one-day license
    label: str = "workbook mid-range outside caterer"

    def cost(self, guests: int, tax: Tax) -> dict:
        food, staff = self.food_pp * guests, self.staff_pp * guests
        alc, soft = self.alcohol_pp * guests, self.soft_pp * guests
        bart = self.bartender_fee * math.ceil(guests / self.guests_per_bartender)
        base = food + staff + alc + soft + (bart if self.service_on_bartenders else 0)
        service = base * self.service_pct
        alc_share = alc / base if base else 0.0
        svc_alc = service * alc_share if self.tax_on_service else 0.0
        svc_non = service * (1 - alc_share) if self.tax_on_service else 0.0
        tax_amt = (food + staff + soft + bart + svc_non) * tax.food + (alc + svc_alc) * tax.alcohol
        total = food + staff + alc + soft + bart + service + tax_amt
        return dict(food=food, staff=staff, bartenders=bart, alcohol=alc, soft_drinks=soft,
                    service=round(service, 2), tax=round(tax_amt, 2), total=round(total, 2),
                    per_guest=round(total / guests, 2))


# ASSUMPTION scenario (not a quote): a budget buffet caterer with a beer-and-wine bar.
# DC buffet food runs ~$70-130/guest (monicabrowneweddings.com, 2026 page); $60 assumes
# a suburban/restaurant caterer at the low end -- the scout must find one that quotes this.
BUDGET_BUFFET_BEER_WINE = Catering(food_pp=60, staff_pp=15, alcohol_pp=20, soft_pp=3,
                                   service_pct=0.20, label="ASSUMPTION budget buffet + beer & wine")

# Costing defaults when the venue does not include something (workbook estimates unless marked)
DEFAULTS = dict(
    cake_pp=8.0, cake_tasting_delivery=150.0, cake_cutting_pp=2.0,
    china_pp=8.0,
    linen_per_table=30.0, linen_per_guest=1.5,  # derived fit: reproduces the workbook's $847.50 at 185 (~$4.58/guest)
    dance_floor=1200.0, rental_delivery=600.0, getting_ready=600.0, liquor_license=100.0,
    tables_chairs_pp=10.0,        # ASSUMPTION
    setup_labor_pp=3.0,           # ASSUMPTION: rental-company set/strike labor if nobody includes it
    parking_per_car=15.0, guests_per_car=2.5,  # ASSUMPTION: validation/valet if no free lot
    escalation_per_year=0.04,     # +4% per year the published price predates 2027
)


# --------------------------------------------------------------------------
# 4. Candidate venue -> all-in cost + verdict
# --------------------------------------------------------------------------

@dataclass
class Venue:
    name: str
    venue_type: str = "package"        # package | rental | fb_minimum | hourly
    jurisdiction: str = "VA"           # key into TAX
    # pricing
    rental_fee: float = 0.0            # flat site / room fee
    tax_on_rental_fee: bool = False    # ASK the venue
    service_on_rental_fee: bool = False
    hourly_rate: float = 0.0
    hours_booked: float = 11.0         # must include setup + breakdown hours
    min_hours: float = 0.0
    platform_fee_pct: float = 0.0      # marketplace guest fee (Peerspace: variable, ~5-9% anecdotal)
    cleaning_fee: float = 0.0
    package_pp: float = 0.0            # in-house per-person package (food + bar unless bar_pp>0)
    bar_pp: float = 0.0                # separate bar package per guest
    package_alcohol_share: float = 0.20  # ASSUMPTION: share of a bundled package that is alcohol (tax split)
    fb_minimum: float = 0.0            # F&B minimum, before service & tax
    service_pct: float = 0.0           # on venue F&B
    tax_on_service: bool = True
    ceremony_fee: float = 0.0
    venue_coordinator_fee: float = 0.0  # mandatory in-house coordinator
    security_fee: float = 0.0
    required_insurance_extra: float = 0.0  # beyond the $300 liability policy already budgeted
    extra_hour_fee: float = 0.0        # extra hour(s) for decor setup
    permit_fees: float = 0.0
    other_fees: float = 0.0
    price_year: int = 2027             # year of the published price
    includes: list = field(default_factory=list)
    # one of: tables_chairs setup_breakdown basic_linens china dance_floor getting_ready
    #         cake cake_cutting free_parking ceremony_space cocktail_space
    outside_catering: Catering | None = None  # for rental / hourly venues
    parking_cost: float | None = None  # if known; None + no free_parking -> ASSUMPTION default
    # must-haves / policies (None = unknown -> ask)
    seated_capacity_with_dance_floor: int | None = None  # rounds + dance floor in the SAME room
    indoor_ceremony: bool | None = None
    separate_cocktail_space: bool | None = None
    allows_enclosed_candles: bool | None = None
    allows_outside_vendors: bool | None = None   # DJ, florist, cake
    end_time: str | None = None
    date_available: bool | None = None
    within_60_min_of_dc: bool | None = None
    source_url: str = ""
    price_date: str = ""
    # Evidence gates. Missing fields in historical specs deliberately stay unknown.
    allows_alcohol: bool | None = None
    heated_indoor_ceremony: bool | None = None
    ceremony_seated_capacity: int | None = None
    ceremony_requires_flip: bool | None = None
    ceremony_flip_priced: bool | None = None
    holding_room_capacity: int | None = None
    reception_end_time: str | None = None  # confirmed event end, e.g. 22:00; not building access
    quote_complete: bool | None = None    # complete 2027 written quote, not a ceiling/placeholder
    tax_inclusion_confirmed: bool | None = None  # all separately priced costs reconciled


def load_exclusions(path: Path = EXCLUSION_FILE) -> set[str]:
    try:
        return {l.strip().lower() for l in path.read_text().splitlines() if l.strip()}
    except FileNotFoundError:
        return set()


def is_excluded(name: str, exclusions: set[str]) -> bool:
    n = name.lower()
    return any(x in n or n in x for x in exclusions)


def end_time_meets_requirement(value: str | None) -> bool | None:
    """Parse only a confirmed standalone clock time, never infer from prose.

    Midnight through 05:59 is treated as the following morning of this evening
    event. Rental windows, cleanup deadlines and conflicting text stay unknown.
    """
    if not value:
        return None
    value = value.strip().lower()
    if value == "midnight":
        return True
    match = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", value)
    if not match:
        return None
    hour, minute, suffix = int(match[1]), int(match[2] or 0), match[3]
    if minute > 59 or (suffix and not 1 <= hour <= 12) or (not suffix and hour > 23):
        return None
    if suffix:
        hour = hour % 12 + (12 if suffix == "pm" else 0)
    return hour >= 22 or hour < 6


def budget_verdict(all_in: float) -> str:
    plan = approved_plan()
    if all_in <= plan["venue_fit_cap"]:
        return "fits"
    return "edge" if all_in <= plan["venue_hard_cap"] else "no"


def evaluate(v: Venue, guests: int = BASE_GUESTS, exclusions: set[str] | None = None,
             tax_override: Tax | None = None) -> dict:
    exclusions = load_exclusions() if exclusions is None else exclusions
    if is_excluded(v.name, exclusions):
        return dict(venue=v.name, verdict="EXCLUDED (already considered by the couple)",
                    fit="no", budget_verdict=None, all_in=None)
    tax = tax_override if tax_override is not None else TAX[v.jurisdiction]
    inc = set(v.includes)
    d = DEFAULTS
    esc = (1 + d["escalation_per_year"]) ** max(0, 2027 - v.price_year)
    lines: dict[str, float] = {}
    flags: list[str] = []

    # --- venue fees (venue-quoted -> escalated) ---
    hourly = v.hourly_rate * max(v.hours_booked, v.min_hours)
    marketplace = (hourly + v.cleaning_fee) * v.platform_fee_pct
    fees = v.rental_fee + hourly + v.cleaning_fee + v.ceremony_fee + v.venue_coordinator_fee \
        + v.security_fee + v.extra_hour_fee + v.permit_fees + v.other_fees
    lines["venue fees (rental/hourly/ceremony/coordinator/security/permits/other)"] = fees * esc
    if marketplace:
        lines["marketplace guest fee"] = marketplace * esc
    if v.service_on_rental_fee:
        lines["service charge on rental"] = v.rental_fee * v.service_pct * esc
    if v.tax_on_rental_fee:
        lines["tax on rental fee"] = v.rental_fee * tax.rental * esc
    lines["required insurance beyond budgeted $300"] = v.required_insurance_extra

    # --- food & drink ---
    caterer = None
    if v.package_pp or v.fb_minimum or v.bar_pp:
        menu = (v.package_pp + v.bar_pp) * guests
        sub = max(v.fb_minimum, menu) * esc
        if v.fb_minimum and menu < v.fb_minimum:
            flags.append(f"menu at {guests} guests (${menu:,.0f}) is below the F&B minimum "
                         f"(${v.fb_minimum:,.0f}) -- shortfall is paid anyway")
        alc = v.bar_pp * guests * esc if v.bar_pp else sub * v.package_alcohol_share
        alc = min(alc, sub)
        service = sub * v.service_pct
        s_alc = service * (alc / sub) if (sub and v.tax_on_service) else 0.0
        s_non = service - s_alc if v.tax_on_service else 0.0
        t = (sub - alc + s_non) * tax.food + (alc + s_alc) * tax.alcohol
        lines["in-house F&B (package/minimum)"] = sub
        lines["F&B service charge"] = service
        lines["F&B tax"] = t
    else:
        caterer = v.outside_catering or Catering()
        c = caterer.cost(guests, tax)
        lines[f"outside catering all-in ({caterer.label})"] = c["total"]
        if not caterer.holds_liquor_license:
            lines["one-day liquor license"] = d["liquor_license"]
        if v.allows_outside_vendors is False:
            flags.append("venue does not allow outside vendors but has no in-house catering -- check")

    # --- rentals the venue (or caterer) lacks ---
    rentals = 0.0
    if "tables_chairs" not in inc:
        rentals += (x := d["tables_chairs_pp"] * guests); lines["tables & chairs (ASSUMPTION $10/guest)"] = x
    if "setup_breakdown" not in inc and not (caterer and caterer.includes_setup_breakdown):
        rentals += (x := d["setup_labor_pp"] * guests); lines["setup & breakdown labor (ASSUMPTION $3/guest)"] = x
    if "basic_linens" not in inc and not (caterer and caterer.includes_basic_linens):
        rentals += (x := d["linen_per_table"] * tables(guests) + d["linen_per_guest"] * guests)
        lines["basic linens & napkins"] = x
    if "china" not in inc and not (caterer and caterer.includes_china):
        rentals += (x := d["china_pp"] * guests); lines["china, glass & flatware"] = x
    if "dance_floor" not in inc:
        rentals += (x := d["dance_floor"]); lines["dance floor"] = x
    if rentals:
        lines["rental delivery & late-night pickup"] = d["rental_delivery"]
        lines["tax on rentals"] = (rentals + d["rental_delivery"]) * tax.rental

    # --- cake ---
    if "cake" not in inc:
        lines["wedding cake + tasting/delivery"] = d["cake_pp"] * guests + d["cake_tasting_delivery"]
    cut = caterer.cake_cutting_pp if caterer else d["cake_cutting_pp"]
    if "cake_cutting" not in inc:
        lines["cake cutting"] = cut * guests

    # --- getting ready, parking ---
    if "getting_ready" not in inc:
        lines["getting-ready suite"] = d["getting_ready"]
    if "free_parking" not in inc:
        if v.parking_cost is not None:
            lines["guest parking"] = v.parking_cost
        else:
            lines["guest parking (ASSUMPTION $15/car)"] = d["parking_per_car"] * math.ceil(guests / d["guests_per_car"])
            flags.append("parking cost unknown -- ask (free lot? validation? valet required?)")

    all_in = round(sum(lines.values()), 2)

    # --- must-haves ---
    if v.ceremony_requires_flip is False:
        flip_priced = holding_capacity = True
    elif v.ceremony_requires_flip is True:
        flip_priced = v.ceremony_flip_priced
        holding_capacity = None if v.holding_room_capacity is None else v.holding_room_capacity >= guests
    else:
        flip_priced = holding_capacity = None
    must = {
        "seats guests at rounds with dance floor in same room": None if v.seated_capacity_with_dance_floor is None
        else v.seated_capacity_with_dance_floor >= guests,
        "indoor ceremony space": v.indoor_ceremony,
        "heated indoor ceremony": v.heated_indoor_ceremony,
        "ceremony seats all guests": None if v.ceremony_seated_capacity is None else v.ceremony_seated_capacity >= guests,
        "ceremony room arrangement and any flip priced": flip_priced,
        "holding room for all guests if a flip is required": holding_capacity,
        "separate cocktail-hour space": v.separate_cocktail_space,
        "alcohol allowed": v.allows_alcohol,
        "allows enclosed candles": v.allows_enclosed_candles,
        "allows outside DJ/florist/cake": v.allows_outside_vendors,
        "reception runs to at least 22:00": end_time_meets_requirement(v.reception_end_time or v.end_time),
        "date available": v.date_available,
        "within ~60 min of downtown DC": v.within_60_min_of_dc,
        "approved guest count": guests == BASE_GUESTS,
    }
    nice = {"end time source note": v.end_time, "confirmed reception end": v.reception_end_time}
    failed = [k for k, ok in must.items() if ok is False]
    unknown = [k for k, ok in must.items() if ok is None]
    if v.allows_enclosed_candles is False:
        flags.append("Enclosed candles are required; a substitution requires an explicit plan change")
    if v.price_year < 2027:
        flags.append(f"price from {v.price_year}: escalated x{esc:.3f}; get 2027 pricing in writing")

    plan = approved_plan()
    env = {"R1 as-is": envelope(guests, 1, False), "R1 trimmed": plan["venue_hard_cap"]}
    cost_verdict = budget_verdict(all_in)
    evidence = {"complete written 2027 quote": v.quote_complete,
                "all applicable tax included or explicitly reconciled": v.tax_inclusion_confirmed}
    missing_evidence = [k for k, value in evidence.items() if value is not True]
    if v.price_year < 2027:
        missing_evidence.append("historical prices require an actual 2027 quote")
    if v.tax_inclusion_confirmed is not True:
        flags.append("Tax inclusion for cake and other separately priced costs is unconfirmed; defaults are unchanged")
    if v.quote_complete is not True:
        flags.append("Modeled scenario only: prices, required fees and inclusions need a complete written 2027 quote")
    if failed:
        fit = "no"
        reason = f"fails must-have: {', '.join(failed)}"
    elif cost_verdict == "no":
        fit = "no"
        reason = "modeled cost exceeds the $32,139 cap"
        if missing_evidence:
            reason += "; actual quote may differ"
    elif unknown or missing_evidence:
        fit = "unknown"
        reason = "unverified: " + ", ".join(unknown + missing_evidence)
    else:
        fit = cost_verdict
        reason = "complete quote and required policies confirmed"
    verdict = f"{fit.upper()}: {reason}; budget scenario: {cost_verdict}"
    return dict(venue=v.name, guests=guests, jurisdiction=v.jurisdiction, all_in=all_in,
                per_guest=round(all_in / guests, 2),
                lines={k: round(x, 2) for k, x in lines.items() if x},
                envelopes=env, headroom_r1_as_is=round(env["R1 as-is"] - all_in, 2),
                headroom_r1_trimmed=round(env["R1 trimmed"] - all_in, 2),
                must_haves=must, quote_evidence=evidence, nice_to_check=nice, flags=flags,
                fit=fit, budget_verdict=cost_verdict, verdict=verdict,
                source_url=v.source_url, price_date=v.price_date)


# --------------------------------------------------------------------------
# 5. Search-filter solvers (inverse of evaluate)
# --------------------------------------------------------------------------

def byo_stack(guests: int, tax: Tax, includes=(), caterer: Catering | None = None,
              parking: bool = True) -> float:
    """Everything outside rental and catering a bare venue needs (cake, rentals, ready room...)."""
    v = Venue(name="__probe__", venue_type="rental", includes=list(includes),
              outside_catering=caterer or Catering(food_pp=0, staff_pp=0, alcohol_pp=0, soft_pp=0,
                                                   bartender_fee=0, label="probe"),
              parking_cost=None if parking else 0.0)
    r = evaluate(v, guests, exclusions=set(), tax_override=tax)
    return r["all_in"] - r["lines"].get(next((k for k in r["lines"] if k.startswith("outside catering")), ""), 0)


def max_package_pp(guests, env, service_pct, tax: Tax, extras=0.0, alcohol_share=0.20, price_year=2027):
    """Max per-person package (food+bar, before service & tax) so all-in <= env."""
    mult = (1 + service_pct) * ((1 - alcohol_share) * (1 + tax.food) + alcohol_share * (1 + tax.alcohol))
    pp = (env - extras) / (guests * mult)
    return pp / (1 + DEFAULTS["escalation_per_year"]) ** max(0, 2027 - price_year)


def max_fb_minimum(env, service_pct, tax: Tax, extras=0.0, alcohol_share=0.20):
    mult = (1 + service_pct) * ((1 - alcohol_share) * (1 + tax.food) + alcohol_share * (1 + tax.alcohol))
    return (env - extras) / mult


def max_rental(guests, env, caterer: Catering, tax: Tax, includes=(), parking=True):
    return env - caterer.cost(guests, tax)["total"] - byo_stack(guests, tax, includes, caterer, parking)


def max_catering_allin_pp(guests, env, rental, tax: Tax, includes=(), parking=True):
    return (env - rental - byo_stack(guests, tax, includes, None, parking)) / guests


def max_hourly(guests, env, catering_allin_pp, tax: Tax, hours=11, platform_fee=0.09,
               cleaning=300.0, includes=(), parking=True):
    room = env - catering_allin_pp * guests - byo_stack(guests, tax, includes, None, parking)
    return (room / (1 + platform_fee) - cleaning) / hours


# --------------------------------------------------------------------------
# 6. Tests
# --------------------------------------------------------------------------

def run_tests() -> list[str]:
    ok = []
    assert len(ITEMS) == 82 and len(CATEGORIES) == 10, (len(ITEMS), len(CATEGORIES))
    ok.append("82 item rows / 10 categories parsed (83 table lines incl. header)")
    base = {r["item"]: r["estimate"] for r in ITEMS}
    it = nonvenue_items(185)
    for n in ("Centerpieces", "Specialty linens & chargers", "Florist delivery & setup fee"):
        assert abs(it[n]["cost"] - base[n]) < 0.01, (n, it[n]["cost"], base[n])
    ok.append("scaling rules reproduce workbook lines at 185 (centerpieces 2850, specialty linens 935, florist fee 840)")
    assert nonvenue_total(185) == 31475, nonvenue_total(185)
    assert nonvenue_total(150) == 30618 and nonvenue_total(130) == 30182
    ok.append("non-venue total 185=$31,475, 150=$30,618, 130=$30,182")
    assert round(envelope(185)) == 23070
    assert envelope(185, trimmed=True) == 32139
    assert nonvenue_total(185, True) == nonvenue_total(150, True) == 22406
    approved = nonvenue_items(185, True)
    assert approved["Florist delivery & setup fee"]["cost"] == 700
    assert approved["Ceremony backdrop / arch"]["cost"] == 200
    assert approved["Hair & makeup trials"]["cost"] == 400
    categories = nonvenue_by_category(185, True)
    assert categories["Flowers & décor"] == 5446 and categories["Attire & beauty"] == 4375
    assert sum(categories.values()) + approved_plan()["venue_hard_cap"] == 54545
    assert approved["Photographer"]["cost"] == 750
    try:
        spend_limit(2)
    except ValueError:
        pass
    else:
        raise AssertionError("Protected reserve must never become an available spending option")
    ok.append("Approved allocations total $22,406; category caps, fixed labor, funded arch/trial and protected reserve enforced")
    # workbook F&B lines at 185 with the workbook's flat 6% (tax base = catering + rentals + specialty linens)
    c = Catering().cost(185, TAX["WORKBOOK"])
    for k, n in (("food", "Hors d'oeuvres + dinner"), ("staff", "Catering service staff"),
                 ("bartenders", "Bartenders"), ("alcohol", "Bar / alcohol"),
                 ("soft_drinks", "Soft drinks, coffee & tea"), ("service", "Caterer service charge (~20%)")):
        assert abs(c[k] - base[n]) < 0.01, (k, c[k], base[n])
    rentals = base["Basic table linens & napkins"] + base["China, glassware & flatware"] + base["Dance floor"] \
        + base["Rental delivery & late-night pickup"] + base["Specialty linens & chargers"]
    assert abs(c["tax"] + rentals * 0.06 - base["Sales tax (~6%)"]) < 0.01
    lin = DEFAULTS["linen_per_table"] * tables(185) + DEFAULTS["linen_per_guest"] * 185
    assert abs(lin - base["Basic table linens & napkins"]) < 0.01
    ok.append(f"workbook caterer lines + 6% tax ($2,457.63) reproduced; mid-range caterer all-in "
              f"${c['per_guest']:.2f}/guest (6%), ${Catering().cost(185, TAX['DC'])['per_guest']:.2f} (DC 10%)")
    # evaluator: a package priced exactly at the solver's ceiling lands on the envelope
    env = envelope(185)
    extras = DEFAULTS["cake_pp"] * 185 + DEFAULTS["cake_tasting_delivery"] + 2 * 185 + DEFAULTS["getting_ready"]
    pp = max_package_pp(185, env, 0.22, TAX["MD"], extras)
    probe = Venue("probe pkg", jurisdiction="MD", package_pp=pp, service_pct=0.22,
                  includes=["tables_chairs", "setup_breakdown", "basic_linens", "china", "dance_floor",
                            "free_parking", "ceremony_space", "cocktail_space"],
                  seated_capacity_with_dance_floor=200, indoor_ceremony=True, separate_cocktail_space=True,
                  date_available=True, within_60_min_of_dc=True)
    r = evaluate(probe, 185, exclusions=set())
    assert abs(r["all_in"] - env) < 1, (r["all_in"], env)
    assert r["budget_verdict"] == "fits" and r["fit"] == "unknown"
    probe.package_pp += 1
    assert evaluate(probe, 185, exclusions=set())["fit"] == "unknown"
    ok.append(f"package solver/evaluator round-trip: ${pp:.2f}++ (22%, MD); affordable ceiling remains unknown without quote/evidence")
    # hourly solver round-trip
    rate = max_hourly(150, envelope(150, trimmed=True), 120, TAX["VA"], hours=11, platform_fee=0.09, cleaning=300)
    cat120 = Catering(food_pp=120 / 1.06, staff_pp=0, alcohol_pp=0, soft_pp=0, bartender_fee=0,
                      service_pct=0, label="flat $120 all-in")
    hv = Venue("probe hourly", venue_type="hourly", jurisdiction="VA", hourly_rate=rate, hours_booked=11,
               platform_fee_pct=0.09, cleaning_fee=300, outside_catering=cat120)
    hr = evaluate(hv, 150, exclusions=set())
    assert abs(hr["all_in"] - envelope(150, trimmed=True)) < 1, (hr["all_in"], envelope(150, trimmed=True))
    ok.append(f"hourly solver round-trip at 150 trimmed, $120/guest catering: max ${rate:.0f}/hr x 11 h")
    # must-have failure and exclusion
    bad = Venue("probe small", package_pp=50, service_pct=0.2, seated_capacity_with_dance_floor=120,
                indoor_ceremony=True, separate_cocktail_space=True, date_available=True, within_60_min_of_dc=True)
    assert evaluate(bad, 185, exclusions=set())["fit"] == "no"
    assert evaluate(Venue("Some Hall"), 185, exclusions={"some hall"})["verdict"].startswith("EXCLUDED")
    ok.append("capacity < guests -> no; exclusion list honoured")
    # F&B minimum shortfall
    fm = Venue("probe min", venue_type="fb_minimum", package_pp=80, fb_minimum=20000, service_pct=0.2)
    assert evaluate(fm, 150, exclusions=set())["lines"]["in-house F&B (package/minimum)"] == 20000
    ok.append("F&B minimum binds when menu x guests is below it")
    # Solvers must use the supplied rental tax, not the probe Venue's VA default.
    # A bare hall rents tables/chairs, setup labor, linens, china, dance floor,
    # and delivery: $5,625 at 150 guests. DC's extra 1% adds $56.25.
    assert abs(byo_stack(150, TAX["DC"]) - byo_stack(150, TAX["VA"]) - 56.25) < 0.011
    dc_rate = max_hourly(150, envelope(150, trimmed=True), 120, TAX["DC"],
                         hours=11, platform_fee=0.09, cleaning=300)
    dc_cat = Catering(food_pp=120 / 1.10, staff_pp=0, alcohol_pp=0, soft_pp=0,
                      bartender_fee=0, service_pct=0, label="flat $120 all-in")
    dc_hall = Venue("probe DC hourly", venue_type="hourly", jurisdiction="DC",
                    hourly_rate=dc_rate, hours_booked=11, platform_fee_pct=0.09,
                    cleaning_fee=300, outside_catering=dc_cat)
    assert abs(evaluate(dc_hall, 150, exclusions=set())["all_in"] - envelope(150, trimmed=True)) < 0.02
    ok.append("BYO stack propagates supplied rental tax; DC hourly solver/evaluator round-trip")
    # Decision gates are separate from numerical affordability.
    zero_tax = Tax(0, 0, 0, "synthetic test only")
    confirmed = dict(package_pp=31139 / 185,
                     includes=["tables_chairs", "setup_breakdown", "basic_linens", "china",
                               "dance_floor", "cake", "cake_cutting", "getting_ready", "free_parking",
                               "ceremony_space", "cocktail_space"],
                     seated_capacity_with_dance_floor=185, indoor_ceremony=True,
                     heated_indoor_ceremony=True, ceremony_seated_capacity=185,
                     ceremony_requires_flip=False, separate_cocktail_space=True,
                     allows_alcohol=True, allows_enclosed_candles=True, allows_outside_vendors=True,
                     reception_end_time="22:00", date_available=True, within_60_min_of_dc=True,
                     quote_complete=True, tax_inclusion_confirmed=True)
    def check(**overrides):
        return evaluate(Venue("synthetic confirmed policy test", **(confirmed | overrides)),
                        exclusions=set(), tax_override=zero_tax)
    for amount, expected in ((31139, "fits"), (31139.01, "edge"), (32139, "edge"), (32139.01, "no")):
        result = check(package_pp=amount / 185)
        assert result["all_in"] == amount
        assert result["budget_verdict"] == result["fit"] == expected, result
    for key in ("allows_enclosed_candles", "allows_outside_vendors", "allows_alcohol",
                "indoor_ceremony", "heated_indoor_ceremony", "separate_cocktail_space"):
        assert check(**{key: False})["fit"] == "no", key
        assert check(**{key: None})["fit"] == "unknown", key
    assert check(reception_end_time="21:59")["fit"] == "no"
    assert check(reception_end_time=None, end_time="rental window 8AM-12AM")["fit"] == "unknown"
    assert check(reception_end_time="midnight")["fit"] == "fits"
    assert end_time_meets_requirement("25:00") is None
    assert check(quote_complete=None)["fit"] == "unknown"
    assert check(tax_inclusion_confirmed=None)["fit"] == "unknown"
    assert check(quote_complete=False, package_pp=32140 / 185)["fit"] == "no"
    assert check(ceremony_requires_flip=True)["fit"] == "unknown"
    assert check(ceremony_requires_flip=True, ceremony_flip_priced=False, holding_room_capacity=185)["fit"] == "no"
    assert check(ceremony_requires_flip=True, ceremony_flip_priced=True, holding_room_capacity=184)["fit"] == "no"
    assert check(ceremony_requires_flip=True, ceremony_flip_priced=True, holding_room_capacity=185)["fit"] == "fits"
    assert check(ceremony_seated_capacity=184)["fit"] == "no"
    no_cutting = [x for x in confirmed["includes"] if x != "cake_cutting"]
    cake_result = check(includes=no_cutting)
    assert "wedding cake + tasting/delivery" not in cake_result["lines"]
    assert cake_result["lines"]["cake cutting"] == 370
    assert cake_result["all_in"] == 31509
    ok.append("Decision boundaries, failed/unknown policies, flip holding capacity, unknown quotes/tax and cake-included/cutting-extra regressions")
    return ok


# --------------------------------------------------------------------------
# 7. Report
# --------------------------------------------------------------------------

PKG_INCLUDES = ("tables_chairs", "setup_breakdown", "basic_linens", "china", "dance_floor",
                "free_parking", "ceremony_space", "cocktail_space")


def filters_report() -> dict:
    out = {}
    # (a) all-inclusive packages: extras = cake + cutting + getting-ready (if not included)
    pk = []
    for g in (185,):
        extras = DEFAULTS["cake_pp"] * g + DEFAULTS["cake_tasting_delivery"] + 2 * g + DEFAULTS["getting_ready"]
        for trimmed in (True,):
            env = envelope(g, 1, trimmed)
            row = dict(guests=g, plan="approved allocations" if trimmed else "historical workbook", envelope=env,
                       all_in_pp_incl_extras=round(env / g, 2),
                       package_allin_pp_ceiling=round((env - extras) / g, 2))
            for label, s, t in (("22% svc, 6% (MD/VA no meals tax)", 0.22, TAX["VA"]),
                                ("22% svc, MD alc 9%", 0.22, TAX["MD"]),
                                ("25% svc, 10% (DC / Fairfax Co.)", 0.25, TAX["DC"]),
                                ("25% svc, 11% (Arlington/Alexandria)", 0.25, TAX["VA-ARLINGTON"])):
                row[label] = round(max_package_pp(g, env, s, t, extras), 2)
            row["same, 2026 pricing (25%/10%)"] = round(max_package_pp(g, env, 0.25, TAX["DC"], extras, price_year=2026), 2)
            pk.append(row)
    out["package"] = pk
    # (b) rental-only + outside caterer
    rt = []
    for g in (185,):
        for trimmed in (True,):
            env = envelope(g, 1, trimmed)
            for label, inc, park in (("bare hall (BYO everything, paid parking)", (), True),
                                     ("hall incl. tables/chairs/setup + dance floor, free lot",
                                      ("tables_chairs", "setup_breakdown", "dance_floor", "free_parking"), False)):
                row = dict(guests=g, plan="approved allocations" if trimmed else "historical workbook", venue=label, envelope=env,
                           byo_stack=round(byo_stack(g, TAX["MD"], inc, None, park), 2))
                for R in (0, 2000, 4000, 6000):
                    row[f"max caterer all-in $/guest @ rental ${R:,}"] = round(
                        max_catering_allin_pp(g, env, R, TAX["MD"], inc, park), 2)
                row["max rental w/ budget buffet+beer&wine (MD)"] = round(
                    max_rental(g, env, BUDGET_BUFFET_BEER_WINE, TAX["MD"], inc, park), 2)
                row["max rental w/ workbook mid-range caterer (MD)"] = round(
                    max_rental(g, env, Catering(), TAX["MD"], inc, park), 2)
                rt.append(row)
    out["rental"] = rt
    # (c) restaurant buyout with F&B minimum (includes tables/chairs/china/linens/staff; no dance floor)
    rb = []
    for g in (185,):
        for trimmed in (True,):
            env = envelope(g, 1, trimmed)
            extras = (DEFAULTS["dance_floor"] + DEFAULTS["rental_delivery"]) * (1 + TAX["DC"].rental) \
                + DEFAULTS["cake_pp"] * g + DEFAULTS["cake_tasting_delivery"] + 2 * g + DEFAULTS["getting_ready"]
            for buyout in (0, 2500):
                rb.append(dict(guests=g, plan="approved allocations" if trimmed else "historical workbook", buyout_fee=buyout,
                               max_fb_min_dc_22pct=round(max_fb_minimum(env, 0.22, TAX["DC"], extras + buyout), 0),
                               max_fb_min_va_20pct_6=round(max_fb_minimum(env, 0.20, TAX["VA"], extras + buyout), 0),
                               max_menu_pp_dc=round(max_fb_minimum(env, 0.22, TAX["DC"], extras + buyout) / g, 2)))
    out["restaurant"] = rb
    # (d) hourly (Peerspace-type), 9% guest fee (conservative end of unverified 5-9%), $300 cleaning
    hr = []
    for g in (185,):
        for trimmed in (True,):
            env = envelope(g, 1, trimmed)
            for cpp in (100, 125, 150):
                row = dict(guests=g, plan="approved allocations" if trimmed else "historical workbook", catering_allin_pp=cpp)
                for h in (10, 11, 12):
                    row[f"max $/hr @{h}h"] = round(max_hourly(g, env, cpp, TAX["DC"], h, 0.09, 300), 0)
                hr.append(row)
    out["hourly"] = hr
    return out


def levers_report() -> dict:
    """Current plan sensitivities, not new savings or supplier offers."""
    plan = approved_plan()
    return {
        "already_assumed_nonvenue_reductions": nonvenue_total(185) - nonvenue_total(185, True),
        "ten_dollars_all_in_per_guest": 1850,
        "ten_dollars_before_22pct_service_and_9pct_tax": round(185 * 10 * 1.22 * 1.09, 2),
        "venue_shopping_target": plan["venue_shopping_target"],
        "headroom_at_shopping_target": round(spend_limit() - nonvenue_total(185, True) - plan["venue_shopping_target"], 2),
        "warning": "Targets and sensitivities are not quotes or secured savings; 185 guests and the protected reserve remain fixed.",
    }


def caps_report() -> dict:
    caps = nonvenue_by_category(185, trimmed=True)
    est = nonvenue_by_category(185, trimmed=False)
    fixed_in_venue_cats = caps["Venue & ceremony"] + caps["Food & drink"]
    wb_envelope_items = sum(r["estimate"] or 0 for r in ITEMS if r["item"] in ENVELOPE_ITEMS)
    return dict(caps_trimmed=caps, estimates_as_is=est,
                fixed_nonvenue_in_venue_food_cats=fixed_in_venue_cats,
                envelope_trimmed=envelope(185, trimmed=True), envelope_as_is=envelope(185),
                workbook_venue_driven_estimates_185=round(wb_envelope_items, 2),
                total_check=round(sum(caps.values()) + envelope(185, trimmed=True), 2))


def examples() -> list[dict]:
    """HYPOTHETICAL venues (not real places) to show the evaluator."""
    ex = [
        Venue("HYPOTHETICAL suburban banquet hall, all-inclusive", "package", "MD", package_pp=105,
              service_pct=0.22, ceremony_fee=750, price_year=2026,
              includes=list(PKG_INCLUDES) + ["cake", "cake_cutting", "getting_ready"],
              seated_capacity_with_dance_floor=250, indoor_ceremony=True, separate_cocktail_space=True,
              allows_enclosed_candles=True, allows_outside_vendors=True, date_available=None,
              within_60_min_of_dc=True),
        Venue("HYPOTHETICAL county-park hall rental + budget buffet", "rental", "VA-FAIRFAX", rental_fee=3500,
              outside_catering=BUDGET_BUFFET_BEER_WINE, includes=["tables_chairs", "free_parking",
                                                                  "ceremony_space", "cocktail_space"],
              seated_capacity_with_dance_floor=180, indoor_ceremony=True, separate_cocktail_space=True),
        Venue("HYPOTHETICAL DC restaurant buyout", "fb_minimum", "DC", rental_fee=0, fb_minimum=22000,
              package_pp=110, service_pct=0.22, includes=["tables_chairs", "setup_breakdown", "basic_linens", "china"],
              parking_cost=0, seated_capacity_with_dance_floor=150, indoor_ceremony=False,
              separate_cocktail_space=True),
        Venue("HYPOTHETICAL marketplace loft (hourly)", "hourly", "DC", hourly_rate=400, hours_booked=11,
              min_hours=4, platform_fee_pct=0.09, cleaning_fee=300, outside_catering=BUDGET_BUFFET_BEER_WINE,
              seated_capacity_with_dance_floor=150, indoor_ceremony=True, separate_cocktail_space=False),
    ]
    return [evaluate(v, g, exclusions=set()) for v, g in zip(ex, (185, 185, 185, 185))]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--venue", help="JSON file with Venue fields (outside_catering as a dict)")
    ap.add_argument("--guests", type=int, default=BASE_GUESTS)
    a = ap.parse_args(argv)
    tests = run_tests()
    if a.venue:
        spec = json.loads(Path(a.venue).read_text())
        if isinstance(spec.get("outside_catering"), dict):
            spec["outside_catering"] = Catering(**spec["outside_catering"])
        print(json.dumps(evaluate(Venue(**spec), a.guests), indent=2))
        return
    rep = dict(tests=tests, envelope_table=envelope_table(), filters=filters_report(),
               levers=levers_report(), caps=caps_report(), examples=examples(),
               mid_range_caterer_pp={k: Catering().cost(185, TAX[k])["per_guest"] for k in TAX},
               budget_caterer_pp={k: BUDGET_BUFFET_BEER_WINE.cost(185, TAX[k])["per_guest"] for k in TAX})
    if a.json:
        print(json.dumps(rep, indent=1, default=str))
        return
    print("TESTS PASSED:"); [print("  -", t) for t in tests]
    print("\nAPPROVED PLAN: 185 guests; $54,545.45 spending limit; $5,454.55 reserve protected")
    print(f"{'guests':>6} {'rdg':>3} {'non-venue':>10} {'env as-is':>10} {'$/g':>6} {'env trim':>10} {'$/g':>6}")
    for r in rep["envelope_table"]:
        print(f"{r['guests']:>6} {r['reading']:>3} {r['nonvenue_as_is']:>10,.0f} {r['envelope_as_is']:>10,.0f} "
              f"{r['per_guest_as_is']:>6.0f} {r['envelope_trimmed']:>10,.0f} {r['per_guest_trimmed']:>6.0f}")
    print("\nMid-range caterer all-in $/guest by jurisdiction:", rep["mid_range_caterer_pp"])
    print("Budget buffet+beer&wine all-in $/guest:", rep["budget_caterer_pp"])
    for k, rows in rep["filters"].items():
        print(f"\nFILTER {k}:")
        for r in rows:
            print("  ", r)
    print("\nLEVERS:", json.dumps(rep["levers"], indent=1))
    print("\nCAPS:", json.dumps(rep["caps"], indent=1))
    print("\nEXAMPLES (hypothetical):")
    for e in rep["examples"]:
        print(f"  {e['venue']} @ {e['guests']}: ${e['all_in']:,.0f} (${e['per_guest']:.0f}/g) -> {e['verdict']}")
        for k, x in e["lines"].items():
            print(f"      {k}: {x:,.0f}")
        for f in e["flags"]:
            print("      !", f)


if __name__ == "__main__":
    main()
