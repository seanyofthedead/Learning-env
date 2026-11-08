#!/usr/bin/env python3
"""Venue-neutral wedding budget model (Sean & Leila, Nov 2027).

Source of every workbook figure: venue_neutral_items.md (same folder) -- the
couple's 10 categories / 83 items with mid-range DC-area estimates, with ALL
venue-specific content removed. No venue the couple already looked at is used
or named here; the agent keeps its own exclusion list (see EXCLUSION_FILE).

What it does
  1. Rebuilds the non-venue total from the items file ($31,475 at 185 guests),
     scaling centerpieces (per table of 10), specialty linens
     (tables*20 + guests*3) and the florist fee (12% of florals); vendor meals
     and everything else stay flat.
  2. Venue envelope = spend limit - non-venue total, for any guest count,
     Reading 1 ($60K / 1.10 = $54,545.45, reserve inside) or Reading 2 ($60K,
     reserve on top), as-is or with the trims.
  3. evaluate(Venue, guests) -> all-in venue cost (rental, F&B, service, tax,
     missing rentals, cake, getting-ready, parking, extra hours, fees, 2027
     escalation) + must-have check + fit verdict.
  4. Search-filter solvers (max package $/guest, max F&B minimum, max rental,
     max hourly rate) used to brief the venue scout.

Run:  python3 venue_neutral_budget.py            # tests + report
      python3 venue_neutral_budget.py --json     # machine-readable report
      python3 venue_neutral_budget.py --venue candidate.json --guests 165

ASSUMPTIONS are labelled "ASSUMPTION" -- confirm or replace with real quotes.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
ITEMS_MD = HERE / "venue_neutral_items.md"
EXCLUSION_FILE = HERE / "excluded_venues.txt"   # one name per line, kept by the couple

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

TRIMS = {  # ceilings ("trimmed" plan)
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


def nonvenue_items(guests: int = BASE_GUESTS, trimmed: bool = False) -> dict[str, dict]:
    """Must-have, non-envelope items costed at `guests`."""
    t = tables(guests)
    out: dict[str, dict] = {}
    for r in ITEMS:
        if not r["must"] or r["item"] in ENVELOPE_ITEMS:
            continue
        name = r["item"]
        v = r["estimate"] or 0.0
        if trimmed and name in TRIMS:
            v = float(TRIMS[name])
        if name == "Centerpieces":
            v = t * (CENTERPIECE_PER_TABLE_TRIMMED if trimmed else CENTERPIECE_PER_TABLE)
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
    """Reading 1: reserve inside the $60K (workbook logic). Reading 2: reserve on top."""
    return BUDGET / (1 + CONTINGENCY) if reading == 1 else BUDGET


def envelope(guests: int = BASE_GUESTS, reading: int = 1, trimmed: bool = False) -> float:
    return round(spend_limit(reading) - nonvenue_total(guests, trimmed), 2)


def envelope_table(guest_counts=(185, 165, 150, 130)) -> list[dict]:
    rows = []
    for g in guest_counts:
        for reading in (1, 2):
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
    seated_capacity_with_dance_floor: int | None = None
    indoor_ceremony: bool | None = None
    separate_cocktail_space: bool | None = None
    allows_enclosed_candles: bool | None = None
    allows_outside_vendors: bool | None = None   # DJ, florist, cake
    end_time: str | None = None
    date_available: bool | None = None
    within_60_min_of_dc: bool | None = None
    source_url: str = ""
    price_date: str = ""


def load_exclusions(path: Path = EXCLUSION_FILE) -> set[str]:
    try:
        return {l.strip().lower() for l in path.read_text().splitlines() if l.strip()}
    except FileNotFoundError:
        return set()


def is_excluded(name: str, exclusions: set[str]) -> bool:
    n = name.lower()
    return any(x in n or n in x for x in exclusions)


def evaluate(v: Venue, guests: int = BASE_GUESTS, exclusions: set[str] | None = None) -> dict:
    exclusions = load_exclusions() if exclusions is None else exclusions
    if is_excluded(v.name, exclusions):
        return dict(venue=v.name, verdict="EXCLUDED (already considered by the couple)", all_in=None)
    tax = TAX[v.jurisdiction]
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
    must = {
        "seats guests with dance floor": None if v.seated_capacity_with_dance_floor is None
        else v.seated_capacity_with_dance_floor >= guests,
        "indoor ceremony space": v.indoor_ceremony if "ceremony_space" not in inc else True,
        "separate cocktail-hour space": v.separate_cocktail_space if "cocktail_space" not in inc else True,
        "date available": v.date_available,
        "within ~60 min of downtown DC (assumption)": v.within_60_min_of_dc,
    }
    nice = {"allows enclosed candles": v.allows_enclosed_candles,
            "allows outside DJ/florist/cake": v.allows_outside_vendors, "end time": v.end_time}
    failed = [k for k, ok in must.items() if ok is False]
    unknown = [k for k, ok in must.items() if ok is None]
    if v.allows_enclosed_candles is False:
        flags.append("no enclosed flame: switch candles to LED (budget the same $1,000-2,000 line)")
    if v.price_year < 2027:
        flags.append(f"price from {v.price_year}: escalated x{esc:.3f}; get 2027 pricing in writing")

    env = {
        "R1 as-is": envelope(guests, 1, False), "R1 trimmed": envelope(guests, 1, True),
        "R2 as-is": envelope(guests, 2, False), "R2 trimmed": envelope(guests, 2, True),
    }
    if all_in <= env["R1 as-is"]:
        cost_verdict = "FITS as-is"
    elif all_in <= env["R1 trimmed"]:
        cost_verdict = "FITS only with the trims"
    elif all_in <= env["R2 trimmed"]:
        cost_verdict = "FITS only by spending the 10% reserve (Reading 2) -- couple must approve"
    else:
        cost_verdict = f"OVER by ${all_in - env['R2 trimmed']:,.0f} even trimmed + reserve"
    if failed:
        verdict = f"REJECT (fails must-have: {', '.join(failed)}); cost: {cost_verdict}"
    elif unknown:
        verdict = f"{cost_verdict} -- PENDING answers: {', '.join(unknown)}"
    else:
        verdict = cost_verdict
    return dict(venue=v.name, guests=guests, jurisdiction=v.jurisdiction, all_in=all_in,
                per_guest=round(all_in / guests, 2),
                lines={k: round(x, 2) for k, x in lines.items() if x},
                envelopes=env, headroom_r1_as_is=round(env["R1 as-is"] - all_in, 2),
                headroom_r1_trimmed=round(env["R1 trimmed"] - all_in, 2),
                must_haves=must, nice_to_check=nice, flags=flags, verdict=verdict,
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
    r = evaluate(v, guests, exclusions=set())
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
    exp = {185: (23070, 32139), 165: (23506, 32463), 150: (23927, 32772), 130: (24363, 33096)}
    for g, (a, t) in exp.items():
        assert round(envelope(g)) == a and round(envelope(g, trimmed=True)) == t, (g, envelope(g), envelope(g, trimmed=True))
        assert round(envelope(g, 2) - envelope(g), 2) == 5454.55
    ok.append("envelope table reproduced (185/165/150/130, as-is & trimmed); Reading 2 adds $5,454.55")
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
    assert r["verdict"] == "FITS as-is"
    probe.package_pp += 1
    assert evaluate(probe, 185, exclusions=set())["verdict"].startswith("FITS only with the trims")
    ok.append(f"package solver/evaluator round-trip: ${pp:.2f}++ (22%, MD) -> all-in == envelope -> FITS as-is; +$1 -> trims")
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
    assert evaluate(bad, 185, exclusions=set())["verdict"].startswith("REJECT")
    assert evaluate(Venue("Some Hall"), 185, exclusions={"some hall"})["verdict"].startswith("EXCLUDED")
    ok.append("capacity < guests -> REJECT; exclusion list honoured")
    # F&B minimum shortfall
    fm = Venue("probe min", venue_type="fb_minimum", package_pp=80, fb_minimum=20000, service_pct=0.2)
    assert evaluate(fm, 150, exclusions=set())["lines"]["in-house F&B (package/minimum)"] == 20000
    ok.append("F&B minimum binds when menu x guests is below it")
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
    for g in (185, 165, 150):
        extras = DEFAULTS["cake_pp"] * g + DEFAULTS["cake_tasting_delivery"] + 2 * g + DEFAULTS["getting_ready"]
        for trimmed in (False, True):
            env = envelope(g, 1, trimmed)
            row = dict(guests=g, plan="trimmed" if trimmed else "as-is", envelope=env,
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
    for g in (185, 150, 130):
        for trimmed in (False, True):
            env = envelope(g, 1, trimmed)
            for label, inc, park in (("bare hall (BYO everything, paid parking)", (), True),
                                     ("hall incl. tables/chairs/setup + dance floor, free lot",
                                      ("tables_chairs", "setup_breakdown", "dance_floor", "free_parking"), False)):
                row = dict(guests=g, plan="trimmed" if trimmed else "as-is", venue=label, envelope=env,
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
    for g in (185, 150, 130):
        for trimmed in (False, True):
            env = envelope(g, 1, trimmed)
            extras = (DEFAULTS["dance_floor"] + DEFAULTS["rental_delivery"]) * (1 + TAX["DC"].rental) \
                + DEFAULTS["cake_pp"] * g + DEFAULTS["cake_tasting_delivery"] + 2 * g + DEFAULTS["getting_ready"]
            for buyout in (0, 2500):
                rb.append(dict(guests=g, plan="trimmed" if trimmed else "as-is", buyout_fee=buyout,
                               max_fb_min_dc_22pct=round(max_fb_minimum(env, 0.22, TAX["DC"], extras + buyout), 0),
                               max_fb_min_va_20pct_6=round(max_fb_minimum(env, 0.20, TAX["VA"], extras + buyout), 0),
                               max_menu_pp_dc=round(max_fb_minimum(env, 0.22, TAX["DC"], extras + buyout) / g, 2)))
    out["restaurant"] = rb
    # (d) hourly (Peerspace-type), 9% guest fee (conservative end of unverified 5-9%), $300 cleaning
    hr = []
    for g in (185, 150, 130):
        for trimmed in (False, True):
            env = envelope(g, 1, trimmed)
            for cpp in (100, 125, 150):
                row = dict(guests=g, plan="trimmed" if trimmed else "as-is", catering_allin_pp=cpp)
                for h in (10, 11, 12):
                    row[f"max $/hr @{h}h"] = round(max_hourly(g, env, cpp, TAX["DC"], h, 0.09, 300), 0)
                hr.append(row)
    out["hourly"] = hr
    return out


def levers_report() -> dict:
    L = {}
    L["trims_value_185"] = round(envelope(185, trimmed=True) - envelope(185), 2)
    L["reading2_value"] = round(spend_limit(2) - spend_limit(1), 2)
    L["nonvenue_saving_per_guest_cut"] = round((nonvenue_total(185) - nonvenue_total(150)) / 35, 2)
    # beer & wine bar: alcohol 35 -> 22 (ASSUMPTION), 20% svc, DC 10%
    L["beer_wine_saving_185_dc"] = round(Catering().cost(185, TAX["DC"])["total"]
                                         - Catering(alcohol_pp=22).cost(185, TAX["DC"])["total"], 0)
    # buffet/family style: food 95->72, staff 25->18 (ASSUMPTION)
    L["buffet_saving_185_dc"] = round(Catering().cost(185, TAX["DC"])["total"]
                                      - Catering(food_pp=72, staff_pp=18).cost(185, TAX["DC"])["total"], 0)
    # jurisdiction: same mid-range caterer DC 10% vs MD (6%/9% alcohol)
    L["dc_vs_md_tax_185"] = round(Catering().cost(185, TAX["DC"])["total"] - Catering().cost(185, TAX["MD"])["total"], 0)
    # brunch/lunch: ASSUMPTION ~25% off food & ~40% off alcohol
    L["brunch_saving_185_dc"] = round(Catering().cost(185, TAX["DC"])["total"]
                                      - Catering(food_pp=95 * 0.75, alcohol_pp=35 * 0.6).cost(185, TAX["DC"])["total"], 0)
    # package all-in $150/guest: cost at each count vs envelope
    L["pkg150_by_count"] = {g: dict(cost=150 * g, env_as_is=envelope(g), env_trim=envelope(g, trimmed=True))
                            for g in (185, 165, 150, 130)}
    # breakeven guest count for a package all-in P/guest (as-is and trimmed)
    def breakeven(P, trimmed):
        g = 200
        while g > 50 and P * g > envelope(g, 1, trimmed):
            g -= 1
        return g
    L["breakeven_guests"] = {P: dict(as_is=breakeven(P, False), trimmed=breakeven(P, True))
                             for P in (125, 150, 175, 200, 225)}
    return L


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
    return [evaluate(v, g, exclusions=set()) for v, g in zip(ex, (185, 150, 150, 150))]


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
    print("\nENVELOPE (Reading 1 = $54,545.45 limit; Reading 2 = $60,000)")
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
