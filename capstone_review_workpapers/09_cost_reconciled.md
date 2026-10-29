# 09: Reconciled Cost, Margin and Payback (cost_and_margin_analyst, round 2)

**Revenue input.** This round uses the reconciled revenue in `06_revenue_reconciled.md`, taken directly from `rev2.run()` (imported, not re-typed), and the rulings in `05_reconciliation_rulings.md`.

**Model files.**
- Model: `/tmp/claude-0/-home-user-Learning-env/597ac1d9-a808-55f6-8cf9-a6a3d19428fc/scratchpad/cm/cost3.py`
- Sensitivities: `/tmp/claude-0/-home-user-Learning-env/597ac1d9-a808-55f6-8cf9-a6a3d19428fc/scratchpad/cm/sens3.py`

**Conventions.**
- Units are $M unless noted.
- FY0 is the capstone year. FY1 month 1 is when the capstone delivers.
- Cost parameters carry over from `02_cost_margin.md` unless changed below. Everything not cited there is an ESTIMATE.

## 0. How the coordinator's rules were applied

| Rule | Implementation |
|---|---|
| GROSS revenue drives delivery cost and gross margin | Delivery cost is a % of each gross revenue line (table below). |
| INCREMENTAL revenue plus incremental pull-through drives payback and ROI | **Incremental contribution = gross contribution − counterfactual contribution** on the 40% (base; 50% downside, 30% upside) of assessments Guidehouse would have won anyway. The counterfactual assumes those assessments are delivered without the tool at **28% GM**, and that their pursuit cost would have been spent anyway (so it is added back). The tool's margin uplift on those deals therefore stays in incremental. Pull-through adds 30% CM × the incremental pull-through line. Base incremental pull-through is $6.25M, which adds $1.88M of CM. All payback and ROI figures are reported **with and without** pull-through. |
| County cost of acquisition (R11 ruling) | County revenue carries a **25% partner margin** plus **$10k of Guidehouse pre-sales per deal**. Package and update delivery cost is 20% (templated). County package margin is 55% per deal before the $10k pre-sales. This answers revenue_modeler's question: I used the per-deal $10k, not $50k per deal. |
| Services-style cost on consultant-delivered lines | Delivery cost by line: mapper and harness assessments **45%** (tool-assisted; GM 55%); mapper and harness implementations **65%** (GM 35%); data-generator custom packs **58%** (0.2 FTE-yr per $100k pack); data-generator royalty 5%. |
| Software run cost on subscription and assurance lines | Variable cost: config A mapper subscription 54% / harness assurance and portfolio 59% (from round 1). Config B is productized: 30% / 35%. Fixed run cost (content, PM, SRE, hosting, ConMon) is in §1. |

**Sales cost (bottom-up, ESTIMATE).**
- Pursuit cost is charged per mapper opportunity: FC $35k, FH $20k, DoD $50k, SL $25k, UK $25k. Opportunities are counted as wins ÷ segment win rate from rev2.
- Standalone harness pursuits cost 0.7× that in A and 0.35× in B (bundled into mapper pursuits).
- Each harness attach costs $15k. Each data-generator pack costs $5k.
- No CAC is charged on subscription conversions or renewals.
- Base result: **mapper sales cost is $3.50M = 22% of mapper revenue**. This is the largest single cost line. The usual 1–3% bid-and-proposal benchmark does not hold for $150–250k task orders.

## 1. Configurations

| | **(A) As scoped** | **(B) Revised** |
|---|---|---|
| Capstones | 3 (data generator, mapper, harness). Improper-payment analytics (IPA) shown separately as the optional 4th. | 3 (IPA not sponsored, per R5) |
| Upfront (sponsorship + hardening), timed FY0/FY1/FY2 | Data gen 0.61, mapper 1.77, harness 1.25 = **$3.63M** (+IPA 0.75 = $4.38M). Includes the full $768k FedRAMP 20x path for the mapper and $160k of incremental harness scope, spent FY1–FY2. | Data gen 0.30 (internal/open-source refactor only), mapper 1.12 (no FedRAMP; $116k for an agency-ATO kit and GovRAMP), harness 0.87 (shared boundary, no 3PAO) = **$2.29M** |
| Fixed run cost/yr (FY1 at 50%) | Data gen 0.24, mapper 0.67, harness 0.64. ConMon of $0.45M/yr (60/40 mapper/harness) starts at authorization (base month 18; upside 14; downside never, but the ATO spend is still sunk). | Data gen 0.08. Mapper 0.56 (shared SRE/PM, $60k hosting). Harness 0.35 (0.5 FTE curation + $60k licensed attack libraries). No ConMon unless FedRAMP is triggered. |
| FedRAMP gate | Pursued regardless | Triggered only when cumulative federal SaaS-only commitments reach ≥5 (40% of federal mapper subscriptions). Federal SaaS-candidate buyers are served in their own agency cloud tenant at **$150k one-time agency-ATO support each** until then. |
| Gate outcome | n/a | **Never triggered within FY1–FY3 in any case.** Cumulative commitments: base 2.4, down 0.7, up 4.9. |
| Subscription variable cost | 54% / 59% | 30% / 35% (productized) |
| Program marketing | $0.15M/yr | $0.15M/yr |

Revenue is held identical in A and B, per the coordinator.
- **B upside assumption:** the federal SaaS cohort (from month 26) accepts agency-cloud delivery. If it does not, about $1–2M of upside subscription revenue is at risk.
- **Data generator in B:** custom-pack revenue ($1.31M base) is kept as consultant services layered on the open-source generator.

## 2. Results: per product, 3-year totals (FY1–FY3)

Column definitions:
- **3-yr cash** = −(all upfront FY0–FY3) + Σ incremental CM FY1–FY3, shown without / with pull-through.
- **Payback** = the FY in which cumulative cash turns ≥0. An asterisk (*) means it is extrapolated at the FY3 run-rate.

### (A) As scoped

| Case | Product | Gross rev | GM | CM (gross) | CM % | Upfront | Fixed run | Sales | **3-yr cash** (no pull / pull) | **Payback** (no pull / pull) |
|---|---|---|---|---|---|---|---|---|---|---|
| Base | Mapper | 15.59 | 47% | 1.79 | 11% | 1.77 | 2.08 | 3.50 | **+0.75 / +2.26** | FY3 / FY3 |
| Base | Harness | 4.40 | 48% | −0.58 | −13% | 1.25 | 1.86 | 0.83 | **−2.12 / −1.75** | never / >FY10* |
| Base | Data gen | 1.31 | 42% | −0.12 | −9% | 0.61 | 0.60 | 0.07 | **−0.72 / −0.72** | >FY10* |
| Base | IPA (optional) | 0 | — | −0.81 | — | 0.75 | 0.81 | 0 | **−1.56** | never |
| Down | Mapper | 4.89 | 48% | −1.14 | −23% | 1.77 | 1.68 | 1.82 | −2.26 / −1.99 | >FY10* |
| Down | Harness | 1.06 | 48% | −1.45 | −136% | 1.25 | 1.59 | 0.37 | −2.79 / −2.74 | never |
| Down | Data gen | 0.23 | 42% | −0.52 | −229% | 0.61 | 0.60 | 0.01 | −1.12 | never |
| Up | Mapper | 30.50 | 47% | 7.11 | 23% | 1.77 | 2.17 | 5.00 | +5.88 / +10.19 | FY2 / FY1 |
| Up | Harness | 13.21 | 46% | 2.85 | 22% | 1.25 | 1.92 | 1.31 | +1.12 / +2.40 | FY3 / FY3 |
| Up | Data gen | 4.57 | 54% | 1.69 | 37% | 0.61 | 0.60 | 0.16 | +1.08 | FY2 |
| Up | IPA (optional) | 7.70 | 36% | 1.96 | 25% | 0.75 | 0.81 | 0 | +1.21 | FY2 |

### (B) Revised

| Case | Product | Gross rev | GM | CM (gross) | CM % | Upfront | Fixed run | Sales | **3-yr cash** (no pull / pull) | **Payback** (no pull / pull) |
|---|---|---|---|---|---|---|---|---|---|---|
| Base | Mapper | 15.59 | 50% | 2.50 | 16% | 1.12 | 1.77 | 3.50 | **+1.97 / +3.48** | FY3 / FY2 |
| Base | Harness | 4.40 | 53% | 0.92 | 21% | 0.87 | 0.94 | 0.47 | **−0.24 / +0.13** | ~FY3.3* / FY3 |
| Base | Data gen | 1.31 | 42% | 0.27 | 21% | 0.30 | 0.21 | 0.07 | **−0.02** | ~FY3.1* |
| Down | Mapper | 4.89 | 50% | −0.91 | −19% | 1.12 | 1.52 | 1.82 | −1.46 / −1.20 | >FY10* / ~FY8.6* |
| Down | Harness | 1.06 | 52% | −0.59 | −56% | 0.87 | 0.94 | 0.20 | −1.56 / −1.51 | never |
| Down | Data gen | 0.23 | 42% | −0.13 | −57% | 0.30 | 0.21 | 0.01 | −0.42 | never |
| Up | Mapper | 30.50 | 50% | 8.16 | 27% | 1.12 | 2.14 | 5.00 | +7.42 / +11.74 | FY2 / FY1 |
| Up | Harness | 13.21 | 56% | 5.66 | 43% | 0.87 | 0.94 | 0.78 | +4.31 / +5.58 | FY2 |
| Up | Data gen | 4.57 | 54% | 2.08 | 45% | 0.30 | 0.21 | 0.16 | +1.78 | FY2 |

**Why gross margin is only about 47–53%.** About 87% of revenue is people-delivered. The blended GM is a services GM, not a software GM. Productization (B) lifts GM by only about 3 points in base, because subscriptions are just $2.7M of $21.3M. The cash gain in B comes mainly from avoided fixed cost (about $1.3M upfront and $0.45M/yr ConMon).

## 3. Results: program

| | (A) Base | (A) Base + IPA | (A) Down | (A) Up | **(B) Base** | (B) Down | (B) Up |
|---|---|---|---|---|---|---|---|
| Gross revenue 3-yr | 21.29 | 21.29 | 6.18 | 48.27 | **21.29** | 6.18 | 48.27 |
| Gross margin | 47% | 47% | 48% | 47% | **50%** | 50% | 52% |
| Contribution (gross basis) | 0.64 (3%) | −0.17 (−1%) | −3.56 (−57%) | 11.20 (23%) | **3.24 (15%)** | −2.08 (−34%) | 15.45 (32%) |
| Upfront investment | 3.63 | 4.38 | 3.63 | 3.63 | **2.29** | 2.29 | 2.29 |
| Upfront timing FY0 / FY1 / FY2 | 0.42 / 2.58 / 0.63 | 0.56 / 3.19 / 0.63 | same as base | same as base | **0.42 / 1.87 / 0** | same as base | same as base |
| Incremental CM FY1 / FY2 / FY3, no pull | −0.30 / −0.06 / 1.45 | −0.46 / −0.39 / 1.13 | −0.79 / −1.29 / −0.91 | 0.73 / 2.82 / 7.72 | **−0.05 / 0.76 / 2.84** | −0.53 / −0.76 / −0.31 | 0.96 / 4.04 / 10.36 |
| Incremental CM, with pull-through | −0.07 / 0.55 / 2.48 | −0.23 / 0.23 / 2.16 | −0.75 / −1.20 / −0.73 | 1.45 / 4.70 / 10.69 | **0.18 / 1.38 / 3.87** | −0.50 / −0.66 / −0.13 | 1.69 / 5.92 / 13.33 |
| **3-yr cumulative cash, no pull** | **−2.54** | −4.10 | −6.62 | +7.63 | **+1.26** | −3.90 | +13.07 |
| **3-yr cumulative cash, with pull** | **−0.66** | −2.22 | −6.31 | +13.22 | **+3.14** | −3.58 | +18.65 |
| **Payback, no pull / pull** | ~FY4.7* / ~FY3.3* | ~FY6.6* / ~FY4.0* | never / never | FY3 / FY2 | **FY3 / FY3** | never / never | FY2 / FY2 |
| 3-yr ROI, no pull / pull | −70% / −18% | −94% / −51% | −183% / −174% | 210% / 364% | **55% / 137%** | −170% / −156% | 570% / 814% |

ROI = (Σ incremental CM − upfront) / upfront.

**Downside detail.**
- B's downside loss is $3.9M, against $6.6M for A. B caps the downside about $2.7M better.
- Neither configuration pays back in the downside, because FY3 incremental CM is still negative.
- The kill/continue gate should be set at FY2 mid-year (see §5).

## 4. Sensitivities (base)

| Lever | (A) 3-yr cash, no pull / pull | (B) 3-yr cash, no pull / pull |
|---|---|---|
| As modeled | −2.54 / −0.66 | +1.26 / +3.14 |
| Pursuit cost halved (vehicle reuse, existing CMS/health accounts, templated proposals) | −1.31 / +0.56 | +2.37 / +4.25 |
| Tool-assisted assessment GM 45% instead of 55% | −3.59 / −1.71 | +0.21 / +2.09 |
| B, if 5 federal SaaS buyers arrive early and FedRAMP is spent in FY3 ($0.70M; ConMon from FY4) | — | ≈ +0.56 / +2.44 |

Assessment margin and pursuit cost move the answer more than any hosting, LLM or ATO line. The economics hinge on whether the tool actually cuts assessment hours by about 35–40% (from 720 to 450 hrs), so this should be the first thing measured on the first 3 consultant-operated assessments.

## 5. Cost-sink verdict (unchanged: the harness)

**In (A), the harness is the clear sink.**
- Base 3-yr cash is **−$2.12M**, and FY3 incremental CM is still negative, so it never pays back.
- On only $4.4M of revenue it carries $1.25M upfront, $1.86M fixed run cost (1.0 FTE of attack-library upkeep, plus a 40% ConMon share for a boundary it does not need, since rev2 runs it inside agency environments) and $0.83M of sales cost.
- The reconciled revenue makes it worse than round 1: COI removes 40% of integrator accounts (R3) and renewal is 60% (R2).
- Data generator (−$0.72M) and IPA (−$1.56M, $0 base revenue under R5) are smaller sinks that are simply avoidable.

**In (B), the harness moves to roughly break-even.**
- Base −$0.24M without pull-through, +$0.13M with; payback ~FY3.3.
- It remains **the weakest product in every case and the largest downside loss** (−$1.56M).
- Keep it as a mapper add-on, priced ≥$200k, with licensed rather than in-house attack libraries.
- Kill trigger: <4 harness clients by FY2 mid-year.

**The mapper is the profit engine but also the largest cost exposure.**
- Its $3.5M pursuit spend is 22% of its revenue.
- In A it adds a $0.77M FedRAMP outlay that base revenue does not justify: only 2.4 federal SaaS-only commitments by FY3, far below the 5-buyer gate.
- **Recommendation: adopt B.** Do not start FedRAMP until 5 federal SaaS buyers are signed. On rev2 base volumes that will not happen before FY4.

**Program gate (ESTIMATE).** At FY2 month 6, if cumulative mapper assessment wins are below about 10 (base is about 12 by then), the program is tracking toward the downside (−$3.9M in B). Stop new hardening spend and run the tools as internal delivery accelerators only.

## 6. Dependencies and likely contests
- **revenue_modeler:**
  - Pursuit-cost-per-opportunity values are mine (ESTIMATE). They imply blended CAC of about $97k per mapper win.
  - The B upside assumes the federal SaaS cohort accepts agency-cloud delivery.
  - The county answer: $10k per deal, with a 25% partner margin.
- **market_and_competition / buyer:**
  - Whether agencies accept consultant-operated or in-tenant delivery as a substitute for FedRAMP SaaS. B depends on it.
  - Whether tool-assisted assessments can hold $250k pricing while costing about 45% to deliver.
- **devil_advocate:** the base program only clears in (B), and only by $1.3M without pull-through over 3 years. Most of the value is pull-through and assessment-margin uplift, not product revenue.
