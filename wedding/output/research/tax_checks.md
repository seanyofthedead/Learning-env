# Tax and model checks — 8 November 2026

Use the model's computed figures, not the rounded figures in the handoff. The reserve remains untouched. Tax estimates are planning assumptions until the venue and caterer identify the taxable items and the applicable selling jurisdiction on a written quote.

## Rates checked on official pages

| Jurisdiction | Evidence and effective year | Planning treatment |
|---|---|---|
| DC rented goods | [DC OTR notice dated 1 October 2025](https://otr.cfo.dc.gov/release/notice-oct-1-2025-tax-changes): “The general sales tax rate will increase to 7.0% for periods beginning on and after Oct. 1, 2026.” Freshly retrieved on 8 November 2026. | Keep the model's 7% rental tax for 2027. This verifies the published scheduled change, not the absence of a later amendment. The general rates page could not be retrieved; get the invoice rate confirmed. The model retains 10% for catered food/on-premises alcohol; that rate was not independently reverified in this pass. |
| Maryland | [Current Maryland statute, Tax–General §11-104](https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gtg&section=11-104&enactments=false), retrieved 8 November 2026: subsection (g)(1) specifies “9% of the charge for the alcoholic beverage”; subsection (g)(2) specifies 6% for separately stated related labor, services and materials. Subsection (i) specifies 6% for a mandatory gratuity/service charge in the nature of a tip for a group of more than ten. Subsection (k)'s 12% from FY2026 applies to **cannabis**, not alcohol. | Retain food/rentals 6%, alcohol 9%. There is no support here for changing alcohol to 12%. Price/tax year: current statute as retrieved; obtain 2027 invoice confirmation. |
| Northern Virginia state/regional sales tax | [Virginia Tax retail sales and use tax](https://www.tax.virginia.gov/retail-sales-and-use-tax), retrieved 8 November 2026, lists 6% for Northern Virginia, including Fairfax City/County, Loudoun, and Prince William. Publication year unknown. | Add the applicable local meals tax to the 6% general rate for the planning scenario; rental goods remain 6%. |
| Fairfax County | [County FAQ](https://www.fairfaxcounty.gov/taxes/business/food-and-beverage-tax-frequently-asked-questions), retrieved 8 November 2026: food/beverage tax 4%, collection begins 1 January 2026. | County F&B scenario totals 10%. County tax is not a substitute for a town or city tax. |
| Vienna town | [Town Finance Meals Tax](https://www.viennava.gov/Town-Departments/Finance/Meals-Tax), retrieved 8 November 2026: “Effective Jan. 1, 2026, the Meals Tax Rate will increase from 3% to 4%.” | Add model key `VA-VIENNA`: 10% F&B, 6% rentals. Earlier 9% combined assumptions are outdated. |
| Fairfax City | [City Meals Tax](https://www.fairfaxva.gov/Property-Business/Taxes/Excise-Taxes/Meals-Tax), retrieved 8 November 2026: “The City of Fairfax imposes a 4.5% tax upon each and every meal sold in the city in or from a food establishment.” Publication/effective year not stated. | Add model key `VA-FAIRFAX-CITY`: 10.5% F&B, 6% rentals. Sherwood's city address does not establish the origin of an outside caterer's sale. |
| Prince William County | [County Food and Beverage Tax](https://www.pwcva.gov/department/tax-administration/food-and-beverage-tax), retrieved 8 November 2026: “Effective January 1, 2026: Tax rate change to 3%.” | Add model key `VA-PRINCE-WILLIAM`: 9% F&B, 6% rentals. Appropriate locality scenario for Woodbridge/Old Hickory/Gray's; verify caterer origin. |
| Alexandria | [City FY2026 tax rates](https://www.alexandriava.gov/taxes/tax-rates), updated 17 October 2025 and retrieved 8 November 2026, lists Restaurant Meals Tax 5%. | Retain 11% combined F&B scenario and 6% rentals; 2027 invoice still required. |
| Arlington | Existing repository assumption: 11% combined F&B, 6% rentals. | Not independently reverified during this pass. Do not describe this as a newly verified 2027 rate. |

Maryland state rates apply to both Montgomery and Howard County leads in the model. Clarksville is the Gathering Place lead's town; do not assign a Montgomery County resident discount to it or to any other venue without eligibility evidence. Use non-resident venue rates as instructed.

## Catering tax follows the seller

The [Fairfax County FAQ](https://www.fairfaxcounty.gov/taxes/business/food-and-beverage-tax-frequently-asked-questions) states: “For catering transactions, the Food and Beverage Tax is imposed based on the origin of the sale, not the destination of the event.” Thus a hall's address alone cannot determine an outside caterer's final local meals tax. New locality keys correct the scenario labels and known in-house selling jurisdictions; they do not make an unknown caterer's tax definitive.

The same FAQ distinguishes discretionary/mandatory gratuities from other charges. A mandatory gratuity of up to 20% is not treated like an unrestricted taxable service fee for county meals tax. Ask the caterer to distinguish service charges, gratuities and labor, and itemize tax. No speculative exemption is deducted from the estimate.

Maryland's model allocates part of service tax to alcohol at 9%. For an itemized quote meeting §11-104(g)(2) or (i), that portion is instead 6%. On the placeholder $20 alcohol × 185 guests × 20% service, the current model is conservatively $22.20 higher. The code keeps this conservative service-tax assumption until the quote identifies the charge; the $22.20 is not available spending headroom.

## Confirmed code correction

`byo_stack(guests, tax, ...)` accepted a tax argument but built a probe venue using the default VA rate and never passed the supplied tax into the evaluator. DC rental ceilings were therefore overstated. The evaluator now accepts an optional `tax_override`, and the helper passes its supplied tax through. Existing callers remain compatible.

Two focused checks now verify that the bare-hall stack at 150 guests rises exactly $56.25 when rental tax rises from 6% to 7%, and that the DC hourly solver round-trips through the evaluator to the envelope. All existing model tests and both checks pass. The three locality keys above were added using official evidence; no budget workbook lines or reserve rules were changed.

For a particular hall, the most reliable caterer ceiling is `(32139 − all modeled costs except the outside-catering line) / 185`, using that venue's actual fees/inclusions. This also avoids the generic solver omitting security, extra hours, permits or other venue-specific fees. The ceiling includes catering staff, hosted beer/wine, soft drinks, bartenders, service and tax; cake/rentals already counted separately must not be counted twice.

## Handoff arithmetic corrections

The placeholder caterer is $60 food + $15 staff + $20 beer/wine + $3 soft drinks per guest. For 185 guests, a 20% service charge is $3,626, and three $200 bartenders add $600 before tax. The model therefore returns:

| Tax scenario | Catering all-in per guest at 185 |
|---|---:|
| Maryland | $128.81 |
| VA with no local meals tax | $128.09 |
| Prince William | $131.72 |
| DC / Fairfax County / Vienna | $132.93 |
| Fairfax City | $133.53 |
| Arlington / Alexandria | $134.14 |

The handoff's “about $124/guest in MD” is too low for its stated placeholder. Use $128.81. These figures exclude venue fees and the separately modeled cake/rentals/getting-ready/parking stack.

The model's exact trimmed envelope is $32,139.45; deliverables use the user's more conservative $32,139 limit. The exact spend limit is $54,545.45 and reserve is $5,454.55. Do not use the model's alternative “Reading 2” reserve-spending verdict as permission to exceed the locked limit.

The model's insurance line is labeled “beyond budgeted $300,” while the locked plan now has $700 fixed insurance. No automatic $400 insurance addition should be introduced; only a verified incremental requirement beyond the locked $700 belongs in the venue scenario.

Unknown rates, missing published fees and unknown vendor origin remain quote questions. No forms were submitted and no vendor was contacted.
