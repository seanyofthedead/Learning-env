# Budget fee and scope review — 8 November 2026

**The arithmetic is reproducible, but “all-in” is still conditional on quotes.** The model does not automatically add tax to several non-venue purchases or cake lines; its uniform catering-tax treatment can also overstate some charges. These effects must be reconciled item by item, not offset against each other or funded from the reserve.

This is an audit only. No model, existing spec or locked category cap was changed. Sources are the [workbook figures](../../budget/venue_neutral_items.md), [current model](../../budget/wedding_budget_model.py), existing source-backed research, and official tax pages fetched below. Monetary sensitivities use 185 guests and the locked trimmed plan unless stated otherwise. Unknown tax inclusion in an estimate is **not** proof that the couple owes an additional amount.

## Highest-priority findings

| Finding | What is confirmed | Financial sensitivity; action |
|---|---|---|
| Non-venue sales tax | The model adds no separate tax to flowers/decor, attire/rings, specialty linens/chargers or thank-you cards. Their workbook rows do not state whether tax is included. | If selected goods totaling $9,335 are pretax, a 6% scenario adds **$560.10**; 7% adds **$653.45**. Obtain tax-inclusive quotes within each cap. These are alternative scenarios, not amounts to add together. |
| Cake and cutting tax | Cake purchase/delivery ($1,630) and cutting ($370 when needed) are added without a tax calculation. Whether their defaults already include tax is unstated. | At 6%, $1,480 cake merchandise alone adds **$88.80**; if the whole $2,000 cake/delivery/cutting stack is taxable and pretax, **$120**. Invoice classification and seller locality control the actual amount. |
| Tables of ten | `tables(185)` is always 19; this is a cost assumption, not a seating plan. | At nine per round, 21 tables; at eight, 24. Relative to 19, current centerpiece/specialty-linen/basic-linen formulas add **$327.60** or **$819** respectively using 6% tax on basic linens, before any omitted tax or extra table rental. |
| Insurance composition | The $700 fixed line is **$300 liability + $400 cancellation**. These are distinct estimates. | An actual $500 liability premium plus $400 cancellation totals $900, **$200 above the allowance**. A venue requiring a $1 million coverage limit does not itself establish a $1 million cost or a particular premium. |
| Staff, service and bartenders | Placeholder catering contains $2,775 staff, $600 bartenders and $3,626 service charge. None is a vendor quote. | They may be separate or overlap in a proposal. With MD model tax, removing an already-included staff line would reduce the scenario by **$3,529.80**; included bartenders by **$636**. These are reconciliation sensitivities, **not available savings**. |
| Service rate | A quoted service fee may differ from the placeholder 20%; “service charge” does not establish gratuity coverage. | Raising the placeholder charge from 20% to 25% increases its MD model total by **$966.44**. Ask separately about required gratuities and discretionary tips. |
| Unknown fee fields | A zero in `ceremony_fee`, extra hours, security, parking or other fees can mean missing evidence. | An estimate without all required fees is incomplete, even if the evaluator prints “FITS.” Get a complete fee schedule and contract before treating a scenario as a fit. |

The $9,335 tax scenario comprises $4,900 of flowers/decor excluding the $546 florist fee; $3,350 of clothing, accessories, shoes and rings excluding alterations/beauty; $935 specialty linens/chargers; and $150 cards. If the full florist fee is also taxable and pretax, 6% adds another **$32.76**. Vendor meals at a pretax $400 would add **$24** at 6%. Do not blanket-tax every service or use a meals-tax rate on clothing and flowers.

## Tax: actual omissions versus conservative assumptions

[Virginia Tax's retail sales page](https://www.tax.virginia.gov/retail-sales-and-use-tax), undated, fetched 8 November 2026, says the tax applies to sales, leases and rentals of tangible personal property and lists 6% for Northern Virginia. This supports checking flowers, apparel, rings and rented goods for tax; it does not determine where these particular purchases will be sourced or whether existing estimates include it.

[Virginia services regulation, 23VAC10-210-4040](https://law.lis.virginia.gov/admincode/title23/agency10/chapter210/section4040/), current page fetched 8 November 2026, says services generally are exempt, while services supplied with taxable goods can be taxable under the transaction's “true object.” [Virginia Code §58.1-609.5](https://law.lis.virginia.gov/vacode/title58.1/chapter6/section58.1-609.5/), current text fetched the same date, exempts qualifying personal/professional services, separately stated alterations, and separately stated transportation. Therefore:

- Do not automatically add 6% to the entire DJ, coordinator, officiant or beauty bill. Ask whether a quote includes a separately taxable equipment rental or goods component. Delivery of photographs/video can also affect classification; the booked photographer amount is not reopened without its contract.
- A florist's fee can contain design, fabrication, delivery, setup or rental labor with different treatment. The model's 12% fee is a workbook assumption, not a verified taxable-service classification.
- Cake merchandise, delivery and cutting should be separately identified. A general 6% example is a sensitivity, not a final cake-tax ruling. Virginia's [meals regulation, 23VAC10-210-930](https://law.lis.virginia.gov/admincode/title23/agency10/chapter210/section930/), fetched 8 November 2026, treats catered meals and associated charges as taxable, but a bakery sale may have a different applicable base or local treatment.

The [Fairfax County FAQ](https://www.fairfaxcounty.gov/taxes/business/food-and-beverage-tax-frequently-asked-questions), undated page fetched 8 November 2026, states that catering meals tax follows **origin of sale**, not event destination. It also says separately stated service and delivery charges are not subject to the county's food/beverage tax; mandatory gratuities are taxed locally only on the portion above 20%. These are local meals-tax rules, not a blanket exemption from Virginia sales tax. For the placeholder's $3,626 separately stated service fee, applying the full combined 10% instead of excluding the county's 4% component would overstate tax by **$145.04**, if the quoted charge qualifies. Do not assume the same local rule in another city or town.

[Maryland Tax–General §11-104(g) and (i)](https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gtg&section=11-104&enactments=false), current statute fetched 8 November 2026, specifies 9% on alcohol, 6% on separately stated associated labor/services, and 6% on qualifying mandatory gratuity/service charges for groups over ten. The model's alcohol-share service-tax split is conservatively **$22.20 higher** for the placeholder than a qualifying separately itemized 6% service charge. The 12% rate in subsection (k) concerns cannabis, not alcohol. Neither this $22.20 nor the Fairfax sensitivity is a discount to apply without a quote.

DC's 7% goods/rental scenario is based on the [OTR October 2025 notice](https://otr.cfo.dc.gov/release/notice-oct-1-2025-tax-changes) scheduling the increase from October 2026, as documented in [tax checks](tax_checks.md). A later amendment was not ruled out in that check. The 7% column above is a planning sensitivity, not a claim that all purchases occur in DC.

## Catering, gratuities and duplicated inclusions

The current MD placeholder is **$23,830.56**, or **$128.81 per guest**, for food, staff, hosted beer/wine, soft drinks, three bartenders, 20% service and modeled tax. It excludes the separately priced cake/rentals/venue stack. It is internally coherent if a caterer really charges each component separately.

Ask the quote to distinguish:

1. Food/bar package inclusions, serving hours, setup/cleanup, staff roles and shift lengths.
2. Number of bartenders, hours, minimum call-out and whether their wages are already in bar or staffing prices.
3. Administrative/service fee base, taxable amount, and whether any portion is distributed as gratuity.
4. Required gratuity versus optional tips; retain the overall $2,000 tips line until recipient-specific overlap is established.

The model excludes bartender fees from the service-fee base by default. Charging its 20% service on those fees adds **$127.20** after MD modeled tax. This can move in either direction depending on the contract. A staff wage line plus a service charge is not automatically double counting.

The IRS's [February 2015 archived fact sheet on tips versus service charges](https://www.irs.gov/newsroom/tips-versus-service-charges-how-to-report), fetched 8 November 2026, distinguishes discretionary tips from automatic service charges and notes that employers can retain a portion. This is explanatory historical federal payroll guidance, not a current local wedding-tax determination. Its practical implication is to ask who receives the charge rather than assume all service fees replace tips.

Avoid double counting china/basic linens when a caterer includes them. The evaluator supports this through `Catering.includes_china`, `includes_basic_linens` and `includes_setup_breakdown`; use those only when the quote establishes inclusion. Wedding package staff are generally represented inside `package_pp`, not by an extra outside-catering line.

## Inflation, layout and add-on scope

**The 4% annual uplift is the couple's modeling rule, not a vendor promise or a cap.** A 2023 figure grows 16.99% by 2027; a 2018 figure grows 42.33%. Such old prices remain weak evidence even after escalation. Dates and fees may change discontinuously, and a proposal may permit further increases after deposit.

The evaluator escalates venue fees and in-house package prices using one `price_year`; it does **not** automatically escalate outside-caterer fields, defaults or non-venue estimates. That is appropriate for explicitly nominal-2027 placeholders, but dated caterer quotes must be uplifted once separately. The reviewed Savage Mill spec labels its manual 2026 ×1.04 uplift; the $90/$100/$110 value scenarios explicitly label nominal-2027 aggregate bills. Do not apply a second uplift to those. As a sensitivity, raising all placeholder food/staff/bar/soft-drink/bartender inputs 4% increases its MD total by **$953.22**. Do not apply 4% blindly to genuinely booked, fixed-price contracts.

**Table count:** the 21/24-table sensitivities above include extra $100 centerpieces plus 12% florist fee, $20 specialty linen allowance per table, and $30 basic linen per table with 6% tax. They assume basic linens are not already included. If included, the corresponding increases are **$264 / $660** before any unmodeled tax or rental changes. The default tables/chairs allowance is per guest, so it does not model additional table-rental charges. Neither calculation checks actual round diameter, dance-floor area, wheelchair access, vendor tables, sweetheart table or buffet footprint. A capacity plan controls the counts; vendor meals do not automatically establish where vendors sit.

**Cake:** the $150 is one combined tasting/delivery allowance. Do not append another delivery allowance if a quote already includes it. Check delivery distance, setup, cake stand rental, cutting and actual portion count before replacement. A confirmed code limitation exists: when `includes` contains `cake`, the model never adds cake-cutting cost even if `cake_cutting` is absent. No current output spec was found with that combination, so this is a latent issue, not a demonstrated current total error.

**Setup:** absent setup inclusion, the model adds $555 labor, and if any rentals/labor are missing it adds $600 delivery plus rental tax. When setup labor alone is missing, this produces **$1,224.30** at 6%. A labor-only contractor might not need a rental truck; conversely a venue flip may cost more. This is a conservative package of defaults to replace with a quote, not proof of a $600 delivery charge. Candles already say setup/strike is included in the workbook, while the 12% florist fee also uses candles in its base: ask whether the florist adds a general production fee on that work or whether this overlaps.

**Getting-ready versus wedding-night room:** these are separate $600 purposes. The former is within venue-driven costs when a suitable changing space is absent; the latter is a fixed non-venue item. An included wedding-night room does not prove access before the ceremony, and a dressing room does not supply an overnight stay. Combining them may save up to $600 only if timing, capacity and terms support both uses. Hotel taxes/resort/parking charges need to fit the final all-in room allowance.

## Insurance and cash commitments

**Correction to the earlier tax-checks note:** comparing extra liability premiums against the entire $700 insurance budget can undercount cost. The model's “beyond budgeted $300” label refers correctly to the **liability** allocation. The other $400 is cancellation insurance. Review actual policy prices, venue-required coverage, host-liquor terms and exclusions separately; do not assume one policy substitutes for the other. This paragraph supersedes the broader combined-$700 interpretation in `tax_checks.md`.

Deposits normally change **payment timing**, not total cost, when credited against the contracted total. Track each deposit, whether refundable, the remaining balance, due dates, and what the cancellation schedule makes nonrefundable. A refundable damage/security hold is a cash requirement even when excluded from expected expense. A retained damage amount becomes an expense. Do not add credited deposits twice or use the protected reserve as temporary funding for holds. Existing photographer payments and date-change penalties must be reconciled against the booked contract, not assumed transferable.

Until contracts arrive, nonrefundable exposure and required peak cash are **unknown**. Venue insurance must be purchased before signing under the locked timeline, but policy eligibility, effective date and what commitments it actually covers remain questions for the insurer's own terms. This review does not infer coverage from the word “cancellation.”

## Model verdict limits and next decision

The evaluator's budget tests pass, but its verdict is not the couple's full acceptance test. Outside-vendor permission and end time sit in `nice_to_check`; alcohol has no explicit acceptance field; enclosed-candle denial adds a flag. Consequently a numerical “FITS” result does not prove these must-haves. Unknown zero fees, heated ceremony details, round-table layout and cocktail space also require manual review. The model's “Reading 2” reserve-spending alternatives are not authorized.

Before a commitment, reconcile each selected quote into four distinct numbers: its all-in contracted cost, its remaining unquoted allowances, refundable cash holds, and cumulative nonrefundable exposure. Keep the fixed categories and venue costs within **$54,545.45**, preserve **$5,454.55** untouched, and retain the conservative **$32,139** venue envelope unless the couple explicitly reallocates documented savings. A verified rise in fixed non-venue costs reduces money available for venues; it does not create permission to use the reserve.
