You are helping Sean and Leila plan their wedding. Pick up a venue and vendor search that another AI assistant started and paused on Sun 8 Nov 2026. If any date below has already passed, shift the schedule forward and say so.

## Files in this repo (folder wedding/)
- budget/wedding_budget_model.py: the budget model. It needs venue_neutral_items.md and excluded_venues.txt in the same folder.
  - Run `python3 wedding/budget/wedding_budget_model.py` to run its tests and print the budget envelope.
  - Price one venue with `python3 wedding/budget/wedding_budget_model.py --venue <spec.json> --guests 185`. Field names are in class Venue and class Catering.
- budget/venue_neutral_items.md: the couple's 10 categories and 82 line items with estimates. This is the only source for workbook figures.
- budget/excluded_venues.txt: venues the couple ruled out. The model rejects any name on it.
- specs/: venue spec JSONs the earlier agents wrote, one folder per search. Reuse and correct them.
- data/round2_verified_research.json: round 2 venue and caterer checks with sources, the budget analysis, and platform research (marketplace terms and the Peerspace playbook).
- data/round3_partial_results.json: round 3 stages that finished before the pause. Stages marked "not yet verified" still need checking on official pages.
- plan/wedding_agent_plan.md: the overall plan, budget explanation, agent design and timeline.
- leila_page/wedding_plan.html: source of the page Leila uses on claude.ai. It shows for reference only; it runs only on claude.ai.

## Locked decisions
- Date: Sat 13 Nov 2027 first. Backups, in order: Sat 6 Nov, Sat 20 Nov, Fri 12 Nov 2027. Sun 14 Nov 2027 only as a last resort. Never lead with Sunday.
- Location: within about 60 minutes' drive of downtown DC (DC, Maryland, Northern Virginia).
- Guests: 185.
- Budget: $60,000 total, including a 10% reserve ($5,454.55) that is never spent. Spend limit $54,545.45.
- Category caps (total $54,545):
  - Venue + food & drink: $34,774 = venue envelope $32,139 + $2,635 fixed (insurance $700, specialty linens $935, vendor meals $400, wedding-night room $600)
  - Planning & legal: $5,250 (day-of coordinator $2,500, officiant $500, license $50, tips $2,000, kit $200)
  - Flowers & décor: $5,446
  - Attire & beauty: $4,375
  - Photo & video: $2,550 (photographer We Love Photography, $750, already booked; videographer $1,800)
  - Music & sound: $2,000 (DJ $1,500)
  - Stationery: $150
  - Guests & transport: $0
  - Pre/post events: $0
- Still open. Use these assumptions until the couple answers:
  - Dinner is buffet, BBQ or family style, with a beer-and-wine bar.
  - The ceremony is at the same venue, and a room flip is OK.
  - Their home county is unknown, so use non-resident rates.
  - Share no budget figure with vendors.
  - The coordinator is day-of only.

## The venue target
Everything the venue choice drives must total at most $32,139 all-in at 185 guests (about $174 per guest). That covers:
- rental or package, all hours including setup and breakdown
- food, staff, bar, service charge and tax
- cake and cake cutting
- rentals the venue lacks
- getting-ready room, parking, ceremony fee, security and required fees

Use wedding/budget/wedding_budget_model.py for every price. It already encodes these rules. Change it only to fix a confirmed error, and keep its tests passing:
- **Old prices:** if only 2026-or-older pricing is published, add 4% per year to reach 2027.
- **Tax:**
  - DC: 10% on catering and alcohol; rentals 6%, possibly 7% from Oct 2026 (confirm).
  - Maryland: 6% on food; 9% on alcohol, which may now be 12% (confirm).
  - Fairfax County, outside its towns: 10%.
  - Arlington and Alexandria: 11%.
  - Other Northern Virginia localities: 6%.
- **Add-ons when the venue doesn't include them:**
  - tables & chairs $10/guest
  - setup and breakdown labor $3/guest
  - basic linens $30/table + $1.50/guest (19 tables)
  - china, glass & flatware $8/guest
  - dance floor $1,200
  - rental delivery and late pickup $600, plus rental tax
  - cake $8/guest + $150
  - cake cutting $2/guest
  - getting-ready room $600
  - parking $15/car at 2.5 guests per car if there's no free lot
- **Placeholder caterer for rental halls until quoted:** food $60 + staff $15 + beer & wine $20 + soft drinks $3 per guest, then a 20% service charge, then tax, plus a $200 bartender per 75 guests. That's about $124/guest all-in in MD and $129–133 in VA or DC. For each hall, also report the highest caterer price per guest that still fits.
- **Package ceilings at 185:** the maximum published 2027 per-person price before service charge and tax is:
  - $116 in DC or Fairfax County (assumes 25% service, 10% tax)
  - $115 in Arlington or Alexandria
  - $122 in Maryland or VA localities with no meals tax (assumes 22% service)

  Divide by 1.04 when the published price is from 2026.
- **Hourly spaces (Peerspace-type):** rate × all hours (about 10–11 including setup and breakdown) + platform fee (assume 5–9%) + cleaning + required staff fees. These rarely fit; about $200/hr is the practical ceiling.
- **Verdict:**
  - "fits": at or under $32,139 with at least $1,000 to spare
  - "edge": fits with less to spare, or only at the low end of a price range
  - "no": over the target, or fails a must-have
  - "unknown": price or capacity isn't published; ask in the inquiry

**Must-haves:**
- seats 185 at round tables WITH a dance floor in one room (standing or theater capacity doesn't count)
- indoor heated ceremony space: a separate room, or a priced room flip with a holding room
- separate cocktail-hour space
- alcohol allowed
- runs to at least 10pm, 11pm preferred
- outside DJ, florist and cake allowed
- enclosed candles allowed (ask)

## Rules
- Never propose, price or cite anything named Bellevue, Milan Ballroom, Grand Marquesa, Newton White or Hay-Adams. The couple already ruled those out.
- Take facts only from venues' and vendors' own websites and PDFs, government or park pages, and official tourism pages. Search results are leads only.
- Do not open or scrape any of these sites: Peerspace, The Knot, WeddingWire, Zola, Here Comes The Guide, Tagvenue, Giggster, Eventective, Thumbtack, Wedding Spot, Yelp, Splacer, Bridebook, and Cvent venue pages. Their terms ban automated access. The couple runs those searches and pastes results to you.
- If a venue was found on Peerspace, warn that booking it directly can trigger Peerspace's 30% off-platform fee.
- Never log in, use passwords, submit forms, book, pay or contact anyone. Draft messages only; the couple sends them.
- Give the source URL and price year for every fact. Write "unknown" instead of guessing, and label assumptions.

## Where things stand

**Verified earlier on official pages** (price sheets dated 2022–2026). The all-in figures assume a budget caterer.
- **Oak Room, Sandy Spring VFD (MD):** $27.2K–36.7K.
  - $3,000 Saturday (2026); seats 220 with a dance floor.
  - Outside caterer +$500; you set up the tables; no getting-ready room.
- **Vienna VFD Event Hall (VA):** $28.6K–38.1K.
  - $3,500 Saturday (2027), 8 hours including setup; ends 11pm.
  - Round tables +$400.
- **Stacy C. Sherwood Community Center (Fairfax City):** $29.0K–38.5K.
  - Alcohol needs a $300 fee and $1M insurance; tight cocktail rooms.
- **Silver Spring Civic Building, Great Hall (MD):** $29.4K–38.9K.
  - Seats 320; security required with alcohol.
  - Books 18 months ahead, so it's open now.
- **Holiday Inn Gaithersburg (MD):** $25.9K–34.3K.
  - $40/guest venue package (2023); alcohol must come from the hotel, price unknown.
- **Turf Valley Resort (Ellicott City):** $31.6K–35.9K, on the line.
  - $118/guest including a 4-hour bar (Nov 2026 menu); about 10% off non-Saturdays.

**Rejected:** Page House (DC, ballroom only 965 sq ft), Laurel Hill Golf Club, Glenview Mansion, West Belmont Place, Josephine Butler Parks Center, Elkridge Furnace Inn, North Hall at Eastern Market, The Hotel at UMD, Workhouse Arts Center, Town of Vienna Community Center (no food allowed in the gyms), Trinity Washington University.

**New this round, checked on official pages:** none confirmed yet; most need the rental price.
- **Montgomery County Ag Center, Heritage Building (Gaithersburg):** Harvest Room seats 360 banquet; tables and chairs set up for you; rates unpublished. Fits only if the hall fee is about $1,300 or less with the placeholder caterer.
- **White Oak Community Recreation Center Social Hall (Silver Spring):** 200 people, 4,000 sq ft; hourly rate unpublished; $31.4K before rental.
- **Woman's Club of Chevy Chase (MD):** seats 200 with a large dance floor; rates unpublished; $31.5K before rental.
- **Beth El Hebrew Congregation Ballroom (Alexandria):** seats 290 with a dance floor; setup and two police officers included; price unpublished; $31.6K before rental.
- **Gray's Event Center (Woodbridge, VA):** up to 200; price unpublished; $31.6K before rental.
- **Cheap rent but over with the placeholder caterer** (these fit with a cheaper caterer):
  - Odenton VFC Social Hall: $800 for 7 hours; $33.1K
  - Howard County Fairgrounds Dining Hall: $500/day; $34.4K
  - Bowie Community Center: $403 non-resident for 9 hours; $34.9K
  - Columbus Club of Arlington: $33.0K
  - Glenarden Gold Room: $2,850 Saturday; $35.3K

**Found but NOT yet checked.** Verify these on official pages first.
- **Great Room at Historic Savage Mill (Savage, MD):** about $29.9K.
  - $2,995 Saturday evening (2026), plus the required caterer, Putting on the Ritz.
  - Ceremony and cocktail space is a tented deck; confirm an indoor heated option.
- **Morningside Inn (Frederick, MD):** about $29.6K.
  - Site rental from $3,500 in November; 50–200 guests indoors.
- **The Gathering Place, Patuxent Grand Ballroom (Clarksville, MD):** up to 265 seated; rental unpublished; $30.1K before rental.
- **The Clubs at Quantico (VA):** about $31.4K with a cash bar.
  - Tradition Buffet $120/guest (2023 guide), service included, no sales tax.
  - Base-access rules apply.
- **Hidden Creek Country Club (Reston):** Premium package from $99.95/guest before service and tax; about $33.8K.
- **Waterford at Springfield, Hazel Ballroom (VA):** seats 190 with a dance floor.
  - Emerald Buffet $77/guest for 5 hours, including a 4-hour beer-and-wine bar.
  - That price sheet looks like 2018, so get 2027 pricing.
- **Packages with unpublished prices, worth an inquiry:** Old Hickory Golf Club (Woodbridge), The Villa (Beltsville), Celebrations at the Bay (Pasadena), Crowne Plaza College Park, Belmont Country Club (Ashburn), Spates Hall at Fort Myer, Chantilly National Golf & Country Club (Centreville).
- **Over budget:**

  | Venue | All-in at 185 |
  |---|---|
  | Event Center at Cascades Overlook | $36.2K |
  | Union Mills Public House | $36.0K |
  | Green Meadows Farm | $38.3K |
  | Hylton Performing Arts Center | $39.9K |
  | Laurel Park | $40.2K |
  | International Country Club | $38.1K |
  | Greater Springfield VFD hall | $35.7K |
  | McLean Community Center | $36.6K |
  | Lee Center | $39.8K |
  | Frederick Fairgrounds | $38.3K |

**Vendors found, not yet re-checked:**
- **Day-of coordinators (cap $2,500):**
  - White Dress Black Tie Events (Loudoun), from $1,900
  - Mayapple Weddings, $2,000
  - MICKNICS, $1,495 plus a required $330 assistant for 100+ guests
  - Lula Mae Special Events, month-of $1,950
  - Black Tie Entertainment, from $1,750
  - Best Wishes Weddings, $2,100 and up
  - Days and Eves, from $2,500
- **Videographers (cap $1,800):**
  - Precious Pics Pro, from $1,499
  - Complete Weddings + Events, $1,795
  - Once Like a Spark, $1,750–$2,040
  - The Studio Weddings, from $1,800

**Caterers priced earlier** (food + bar per guest):
- Famous Dave's ~$53
- Mission BBQ ~$63
- IndAroma ~$72–88
- Lebanese Taverna ~$80
- Catering At Your Door ~$81
- Taqueria Picoso ~$81

Bar services: Cartistry, Sunrise Rentals DMV, Boa Bar. In DC, only a licensed caterer can serve alcohol at an unlicensed venue.

## What to do
1. Run wedding/budget/wedding_budget_model.py and confirm its tests pass. Read the spec JSONs in wedding/specs/ and the data files before searching, so you don't redo finished work.
2. Verify the unchecked venues on official pages, then re-price every lead at 185 guests.
3. Re-check each vendor's own site: price, year, what's included, and how to contact them.
4. Rank the venues. Pick 10–12 to inquire about this week: confirmed fits plus promising venues with unpublished prices, since an inquiry is how you learn the price.
5. Write inquiry_pack.md, in this order:
   - **Send order:**
     - First: an email to We Love Photography asking their date-change policy and whether they're free Sat 6, Sat 20 and Fri 12 Nov 2027. Then 3 coordinator and 3 videographer inquiries.
     - Next: the venue inquiries and the caterer quote requests.
     - A follow-up message for 3 business days later.
     - A tracking table: Venue | Sent | Reply | Dates open | 2027 price | Next step.
   - **Each venue email** (150 words or less, with a subject line) asks:
     - availability on the dates
     - 2027 pricing in writing, including Friday pricing
     - seated capacity at round tables with a dance floor
     - ceremony and cocktail spaces
     - catering and bar rules
     - hours included and end time
     - holds and booking window
     - deposit, payment schedule and cancellation policy
     - 2–3 questions specific to that venue

     For phone-only venues, add a 60-second call script.
   - **One standard caterer quote request**, plus a line per caterer naming which halls it's for. The event: about 185 guests, a November 2027 evening, buffet, BBQ or family style, beer and wine with soft drinks. Ask for an itemized per-guest quote covering staff, service charge, tax, china and linens, bartenders and licenses, plus deposit terms and a tasting.
   - **Writing rules:**
     - Sign every message "Sean & Leila", with placeholders [wedding email] and [phone].
     - Use this date line, in this order: "Our first choice is Saturday, November 13, 2027. We'd also consider Saturday, November 6; Saturday, November 20; or Friday, November 12, 2027." Never mention Sunday.
     - Say "about 185 guests".
     - Never include a budget figure or per-guest target.
     - Don't claim anything about a venue that your sources don't support.
6. **Deliverables:** in wedding/output/, write venue_shortlist.md (table: Rank | Venue | Town | Type | All-in at 185 | Fit | Next step, with sources), inquiry_pack.md, and the spec JSON for every venue you price. Write in plain language; the couple reads on a phone.

**Timeline:**
- Tue 10 Nov 2026: first inquiries out
- 21–22 Nov: first tours
- Wed 25 Nov: checkpoint. If fewer than 3 venues fit, push on the backup dates.
- 5–6 and 12–13 Dec: more tours
- Fri 18 Dec 2026: sign the venue, after buying event insurance
