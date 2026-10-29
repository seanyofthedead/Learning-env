# Capstone-to-Product Program: Pricing and Go-to-Market Review

**To:** Guidehouse AI CoE leadership, Federal Health, Managed Services, Partnerships, UK
**From:** Lead partner, pricing and GTM review
**Date:** 29 October 2026
**Basis:** Six analyst workstreams (revenue, cost and margin, market and competition, buyer role-play, devil's advocate, growth) plus one reconciliation round. All figures are 3-year totals for FY1–FY3 unless noted. FY1 starts when the first capstone cohort delivers. **"ESTIMATE" means not verified against a source.** Sourced figures are cited in Appendix E.

---

## 1. Executive summary

In the reconciled base case the program books **$21.3M of gross revenue over 3 years ($2.3M / $6.7M / $12.3M), or $17.1M incremental**. Incremental nets out the 40% of assessments Guidehouse would likely win anyway (ESTIMATE). Gross margin is **47%**. As scoped, the program is **−$2.5M cash-negative after 3 years** (payback ~FY4.7, ESTIMATE).

The revised configuration recommended here holds revenue flat but cuts upfront spend from $3.6M to $2.3M. Under it, gross margin is **50%**, 3-year cash is **+$1.3M** (+$3.1M with pulled-through services), and payback lands in **FY3**.

Even the upside ($48M over 3 years) is under 1% of firm revenue (ESTIMATE). Treat this as a margin, positioning and pipeline program, not a revenue line.

| Product | Call | Why |
|---|---|---|
| **Policy-to-AI-governance mapper** | **KEEP, modified** | 73% of revenue and the only product that pays back on its own. Sell it as a consultant-delivered assessment plus managed service, not standalone SaaS. Defer FedRAMP. |
| **Agentic AI red-team harness** | **MODIFY** | The cost sink: −$2.1M as scoped. Sell it as a mapper add-on on a shared boundary, priced per system, behind an independence firewall. Kill gate in FY2. |
| **Synthetic data generator** | **MODIFY** | No standalone market. Open-source it as an enabler and sell only calibrated data packs. |
| **Improper-payment analytics (optional 4th)** | **KILL as a product** | $0 base revenue and −$1.6M cash. Keep it as a demo inside the existing CMS work. |

---

## 2. Revenue model

### 2.1 Key assumptions (reconciled base)

| Assumption | Base value | Basis |
|---|---|---|
| Mapper assessment price | $250K federal / $150K state / $180K UK | Market range $150–350K. Federal price kept under the $350K simplified acquisition threshold (SAT). ESTIMATE |
| Mapper implementation | $400K / $200K / $250K; 50% of assessments convert | ESTIMATE |
| Mapper subscription | $250K federal / $150K state / $200K UK per year; **35% of assessments convert**; 10% churn | Buyer analyst: 30–40%. Ruling R1/R8 |
| Harness | $175K assessment ($225K defense); $200K/yr assurance; **35% attach to mapper; 60% renewal** | Buyer analyst: episodic, 50–60% renewal (R2) |
| Harness conflict-of-interest haircut | −40% of harness opportunities where Guidehouse is the AI integrator | FAR 9.5. Integrator share 20–70% by segment, ESTIMATE (R3) |
| Data generator | Custom packs only: $100K, sold to 30% of mapper and harness wins | Market: $50–150K packs. Free alternatives exist (R4) |
| Counties | Channel only: $40K package plus $20K/yr update; 0/4/10 deals | R11 |
| Win rates and cycles | 30–40% win rate (defense 20%, state −5 pts); 6–15-month cycles | Expansion sales on existing vehicles. ESTIMATE |
| Timing | Consultant-run assessments from month 3; managed service from month 9; FedRAMP 20x Moderate at FY2 month 6, so federal SaaS starts FY3 month 6 | R7. ESTIMATE |
| Wins over 3 years | ≈36 mapper assessments, ≈15 harness clients, ≈9 mapper subscriptions | Model output |

### 2.2 Three cases ($M; formulas in Appendix A)

| Case | FY1 | FY2 | FY3 | **3-yr gross** | **3-yr incremental** | Recurring run-rate, end FY3 |
|---|---|---|---|---|---|---|
| Downside | 0.64 | 1.90 | 3.65 | **6.2** | 4.4 | 0.55 |
| **Base** | 2.31 | 6.67 | 12.32 | **21.3** | **17.1** | **3.2** |
| Upside | 5.16 | 14.82 | 28.30 | **48.3** | 42.3 | 11.7 |

- **Base mix:** mapper $15.6M, harness $4.4M, data generator $1.3M. Federal civilian plus health $14.4M (68%), UK $2.8M, state/local $2.6M, defense $1.5M. 87% is one-time, people-delivered work.
- **Outside core:** pulled-through services $8.4M gross / $6.3M incremental (0.5× assessment and implementation revenue, ESTIMATE). Improper-payment analytics adds +$7.7M in the upside only, contingent on a real-data task order.
- **Levers (pre-reconciliation run):** win rate −5 pts = −$3.8M; price −20% = −$4.7M; sales cycle +3 months = −$3.5M. FedRAMP never landing costs only ~$0.7M inside the window.

---

## 3. Cost, margin, and payback

**Upfront cost.** Sponsorship is **$139.5K per capstone**: a ~$15K university fee plus ~78% AI CoE time. Hardening is **130 FTE-months / $3.83M**, assuming **30% of capstone code survives** at $24K per FTE-month (ESTIMATE). The mapper's full FedRAMP 20x path, including a 3PAO, is $768K. Pursuit cost is about **$97K per mapper win**, or 22% of mapper revenue, the largest single cost line.

**Configurations compared**

| | A: as scoped | **B: revised** |
|---|---|---|
| Design | Three standalone products; FedRAMP regardless | Shared platform and authorization boundary; generator open-sourced; harness sold as a mapper add-on; FedRAMP only after 5 committed federal SaaS buyers (deliver in the agency's own cloud until then); productized delivery |
| Upfront (sponsorship + hardening) | $3.63M ($4.38M with improper-payment) | **$2.29M** |
| Gross margin, base | 47% | **50%** |
| 3-yr cash, base: no pull-through / with | −2.54 / −0.66 | **+1.26 / +3.14** |
| Payback, base | ~FY4.7 / ~FY3.3 (extrapolated) | **FY3 / FY3** |
| 3-yr cash, downside | −6.62 | −3.90 |
| 3-yr cash, upside | +7.63 | +13.07 |

**By product (base, 3-yr cash, $M; no pull-through / with)**

| Product | Revenue | GM (A→B) | A | B |
|---|---|---|---|---|
| Mapper | 15.59 | 47% → 50% | +0.75 / +2.26 | **+1.97 / +3.48** |
| Harness | 4.40 | 48% → 53% | **−2.12 / −1.75 (never pays back)** | −0.24 / +0.13 |
| Data generator | 1.31 | 42% | −0.72 | −0.02 |
| Improper-payment | 0 | — | −1.56 | not sponsored |

**Cost sink: the red-team harness.** It carries 1.0 FTE ($288K/yr) of attack-library upkeep that never pays down, an authorization boundary it doesn't need, and a 40% conflict-of-interest haircut. It is the weakest product in every case (−$1.56M in B downside).

**Biggest sensitivities.** Tool-assisted assessment margin is assumed at 55%, from cutting 720 hours to 450 (ESTIMATE); at 45%, B's base drops to +$0.21M. Halving pursuit cost lifts B to +$2.37M. Measure both on the first three assessments.

---

## 4. Market and competition

| Product | Alternatives (verified) | What agencies pay | Best motion |
|---|---|---|---|
| Synthetic data | Synthea (free), NVIDIA NeMo Data Designer (Gretel), MOSTLY AI SDK, SDV, Tonic | DOJ/Gretel $148K/yr; Air Force/Tonic $74K; custom builds $0.58–1.25M | **Give away / open-source.** Sell calibrated packs at $50–150K |
| Governance mapper | RegScale (Navy $4.35M, DOE $3.0M), Telos Xacta (FBI $2.87M), ServiceNow (DISA $2.0M), Paramify ($95–105K), Booz Allen + Credo AI "AI Inventory Jumpstart" | AI-governance advisory task orders $0.27–1.74M (FAA/EY $1.17M; CMS $1.07M) | **Bundle** as assessment plus managed service. Feed the GRC tool the agency already runs (OSCAL output); don't replace it |
| Red-team harness | Inspect, garak, PyRIT, NIST Dioptra (free); GSA USAi / NIST CAISI baselines | Engagements $110–800K; assurance labs $0.8–1.8M | **Open-source the core; sell recurring assurance** per system |
| Improper payments | Guidehouse already holds the CMS exchange improper-payment measurement contract ($63.9M, June 2026) | Buyers pay for accuracy on real claims | **Bundle only** as a demo sandbox |

- **Demand drivers:** OMB M-25-21 and M-25-22 are in force; the AI use-case inventory is statutory (Advancing American AI Act), so it survives memo churn; the 2025 inventory lists 3,611 use cases, 445 high-impact; NIST is drafting AI overlays for 800-53; Texas TRAIGA has covered state and local government since 1 January 2026. **Weak spots:** M-26-04 sunsets around December 2027, and state AI laws face a federal preemption push.
- **Vehicles:** **CIO-SP4 was cancelled on 30 January 2026, so drop it.** Use GSA MAS (SINs 541611, 54151S, 54151HACS, 518210C), OASIS+ (held), the DoD CDAO AI T&E BPA (holder status unverified), NASPO and state contracts, and TS4 Lots 1 and 5/5a.
- **Gaps Guidehouse can own:** one evidence chain from Maturity Model to inventory to mapped controls to red-team evidence (no competitor offers it); AI governance sold with each Vant4ge deployment; HHS, VA and DHA, the heaviest AI users; UK ATRS on Inspect.

---

## 5. Buyer feedback summary

All figures below are role-play ESTIMATES.

| Product | Federal CIO / Chief AI Officer (CAIO) | State CTO | County IT director |
|---|---|---|---|
| Synthetic data | 25%; $0 standalone | 35%; $40–120K | 10%; <$15K |
| Governance mapper | **45%** (CAIO 55%); $150–340K assessment under the SAT | **50%**; $100–250K + $75–200K/yr | 30%; $15–60K fixed fee |
| Red-team harness | 50%, **≤15% if Guidehouse built the system** | 40%; $75–200K per system | 20% |
| Improper-payment | ≤10% on synthetic data | 30% on real data, through the Medicaid agency | 5% |

- **First buy:** federal CAIO, a red-team "minimum-practices evidence package" for 3–5 high-impact use cases (the M-25-21 deadline has passed, so the market is remediation); federal CIO, a mapper assessment; state CTO, a statewide inventory, crosswalk and review-board kit; county, a fixed-fee AI policy plus CJIS 6.0 crosswalk.
- **Must-haves:** federal, OSCAL output into the existing ATO tool plus a contractual independence firewall; state, one maintained crosswalk (IRS 1075, MARS-E, CJIS, state AI rules) with a 30-day update SLA; county, turnkey delivery in 30 days.
- **Blockers:** who supports it and under whose authorization; conflict of interest; free templates (GSA, CAIO Council, NACo); lapsed TMF and state and local cybersecurity grant funding (the live route for state HHS is the Medicaid 90/10 match).
- **"Built from a capstone":** a liability in federal sales, a plus with states as a workforce story. Don't lead with it federally.

---

## 6. Risks and the devil's advocate case

**Devil's case:** 3-yr gross **$7.6M**, incremental $5.0M, net **$0.8M** after lost billable hours.
- **Inputs:** 21 mapper wins, 20% subscription conversion, 15% harness attach, 50% renewal, 10–15% code survival, $5.2M hardening and $2.45M/yr run cost.
- **Cash:** −$11.4M at FY3 and −$15.5M at FY5. The material threshold is ≥$30M/yr incremental, about 1% of firm revenue (ESTIMATE). The program never reaches it.

**Arguments and resolution**

| Argument | Assessment | What would have to be true for it to be wrong (kill criteria) |
|---|---|---|
| Attach and conversion are inflated | Partly accepted: conversion cut to 35% and renewal to 60% | ≥30% of assessment clients sign a ≥$150K/yr subscription by Nov 2028; ≥25% harness attach |
| Capstone code won't harden cheaply | Credible, and unmeasured | Hardening ≤$2.3M (Config B) with ≥25% code survival, confirmed by an AI CoE code audit at capstone handoff |
| Cannibalization: the tool cuts assessment hours 37.5%. On an assumed $30M advisory book, 50% billed by the hour, FY3 revenue falls $2.25M | **Accepted as the main structural risk** | Use the mapper on fixed-price work first. Freed hours are resold at ≥50%. Net advisory revenue in AI governance doesn't fall YoY |
| Channel conflict: Vant4ge has its own agentic AI (AIDA); hyperscalers bundle governance tooling | Accepted: don't red-team partner products | Vant4ge co-sell agreement signed by FY1 Q2 that names governance as a Guidehouse attach |
| Conflict of interest in red-teaming what we build | Accepted (R3) | Zero conflict-of-interest findings; independence firewall approved by Legal |
| Policy churn; free baselines (GSA USAi) | Partly mitigated by the statutory inventory requirement | ≥15 qualified opportunities by 31 May 2027 (stop hardening below 8); ≥5 signed mapper assessments, ≥3 federal, by Feb 2028 |
| The capstone calendar misses the September federal and July state buying windows | Accepted | Run assessments with the tool internally from month 3, ahead of hardening |

**Reconciling the devil's case with the base.** The devil's revenue sits between the downside ($6.2M) and the base ($21.3M), so I treat it as a stress case, not the plan. The difference is mainly win volume (21 vs 36) and conversion (20% vs 35%). The kill criteria above are built to tell within 12–18 months which number is real.

---

## 7. Top 5 recommended changes, ranked

Impacts come from the growth strategist's 3-year mid-case estimates, made against a ~$17M placeholder base (ESTIMATE). They overlap, so haircut the sum by ~30%.

| # | Change | Expected 3-yr impact | Cost | Owner |
|---|---|---|---|---|
| 1 | **Adopt Config B.** Shared boundary; harness as a mapper add-on; generator open-sourced; FedRAMP only after 5 letters of intent; agency-cloud delivery in the meantime | 3-yr cash −$2.5M → **+$1.3M** (+$3.8M swing); downside loss cut by $2.7M | Saves $1.34M upfront | AI CoE product owner + CFO |
| 2 | **Make the AI Readiness Maturity Model the paid front door.** Maturity score → inventory → controls → evidence, with an annual re-score built into the subscription | **+$2.5M** (+5 pts win rate; conversion 35%→42%, ESTIMATE) | ~$200K | AI CoE lead + federal civilian account leads |
| 3 | **Price harness work per system.** $75–150K sprint, $120–300K/yr assurance, a $0.6–1.2M/yr portfolio tier; **plus M-25-22 pre-award vendor AI evaluation** (no conflict of interest when Guidehouse doesn't bid) | **+$2.0M + $1.3M** (13 evaluations × ~$100K) | ~$150K + Legal conflict-of-interest review | AI CoE product owner + Contracts/Legal |
| 4 | **Price assessments under the SAT ($350K) and run a new vehicle plan.** GSA MAS, OASIS+, CDAO T&E BPA, NASPO, TS4; drop CIO-SP4 | **+$1.5M** (2–3-month shorter cycle) | ~$100K | Federal capture lead |
| 5 | **Use the mapper first on Guidehouse's own fixed-price governance and ATO work** | **+$1.8M margin** (assumes ~$8M/yr such labor, unverified) | Low; internal rollout | Managed services lead |

**Next in line.**
- Medicaid 90/10 module for state HHS: +$2.1M, first revenue FY2.
- Vant4ge governance attach: +$1.65M.
- UK ATRS/AI Playbook on Inspect: +$1.3M.
- Capstone as a recruiting pipeline: ~13 hires × ~$29K avoided cost ≈ $0.4M (ESTIMATE).

---

## 8. Revised program recommendation

**Run two product capstones plus one enabling capstone on a single shared platform, in Config B.**

- **Capstone 1, governance mapper (lead):** OSCAL output, an M-25-21 artifact pack, and one maintained crosswalk (NIST 800-53 / AI overlay, CJIS 6.0, HIPAA, IRS 1075, StateRAMP/GovRAMP). Delivered as a Maturity-Model-led assessment plus managed service, consultant-operated from month 3.
- **Capstone 2, red-team harness (add-on):** built on Inspect / PyRIT / garak with licensed attack libraries; priced per system; sold only behind an independence firewall or where Guidehouse is not the integrator.
- **Capstone 3, synthetic data generator (enabler):** Apache-2.0 release, paid calibrated packs only, feeds the demos for 1 and 2.
- **Drop the improper-payment capstone;** reuse synthetic claims as a demo inside the CMS work.
- **New program rules:** product owner at ≥0.5 FTE (from 0.25); code audit at handoff targeting ≥25% survival; university agreement permits open-source release and relicensing.
- **Stage gates:** (1) 31 May 2027: ≥15 qualified opportunities, or stop hardening. (2) FY2 month 6: ≥10 mapper wins and ≥4 harness clients; if the harness misses, fold it into the mapper; if the mapper misses, internal tooling only. (3) FedRAMP: 5 signed federal SaaS letters of intent before any 3PAO contract.

---

## 9. Open questions that need a human decision

1. **Ambition:** do we accept that this is a margin and positioning program worth ~$1–3M of 3-year cash, not material revenue? Or do we fund the upside levers (portfolio tier, Medicaid module, UK)?
2. **Conflict-of-interest policy:** may Guidehouse red-team AI it built if there's a firewall, or only third-party systems? Legal and Contracts must rule before harness pursuits begin.
3. **Cannibalization stance:** will practice leaders accept fewer billable hours on hourly-billed governance work in exchange for margin on fixed-price work?
4. **Vehicles:** confirm whether Guidehouse holds the CDAO AI T&E BPA (≈$1.0M of defense harness revenue at risk) and which OASIS+ domains it holds.
5. **University IP:** will the partner universities agree to open-source release and relicensing to third parties?
6. **Vant4ge:** is governance attach on Vant4ge deployments in scope of the partnership? How do we avoid red-teaming Vant4ge's own AI (AIDA)?
7. **FedRAMP:** do we agree to defer the ~$0.77M FedRAMP spend until 5 letters of intent, even though base volumes suggest that is FY4?
8. **Resourcing:** who funds the product owner at 0.5 FTE or more, and who owns pursuit cost (22% of mapper revenue)?

---
---

## Appendix A: Revenue formulas (as implemented, monthly; m = 1–36)

- **Pipeline:** opportunities open evenly each year; `m_close = m_open + cycle_s`, floored at month 3.
- **Mapper wins:** `MAPwins[s,m] = Σ opps[s,y]/12 × win_s`
- **Assessment revenue:** `Rev_MAP_assess = Σ MAPwins × price_s`
- **Implementation revenue:** `Rev_MAP_impl[m+3] = 0.50 × MAPwins[m] × impl_$`
- **New subscriptions:** `NewSubs = 0.50 × 0.70 × MAPwins` (defense ×0.5). Non-federal and 60% of federal start at max(impl_end, month 9). The federal SaaS-only 40% start at auth_month + 12 (month 30).
- **Subscription revenue:** `Active[m] = Active[m−1] × (1−churn)^(1/12) + NewSubs[m]`; `Rev_sub = Active × price/12 × 1.03^(FY−1)`
- **Harness wins:** `HARwins = (standalone + 0.35 × MAPwins[m−6]) × (1 − 0.40 × integrator_share_s)`. Integrator share, ESTIMATE: federal civilian 40%, federal health 70%, defense 20%, state/local 50%, UK 30%.
- **Harness revenue:** implementation = 0.40 × wins × impl_$; new subscriptions = 0.60 × wins; churn 40%.
- **Data generator:** `Rev_DG = 0.30 × (MAPwins + HARstandalone) × $100K`
- **Counties:** `Rev_county = deals × $40K + (prior + 0.5 × new) × 50% × $20K`
- **Incremental:** `INCR = GROSS − k × (assessment revenue)`; k = 0.40 base / 0.50 down / 0.30 up.
- **Pull-through:** `Pull = r × (assessment + implementation revenue)`; r = 0.5 / 0.3 / 0.7 (ESTIMATE).

**Downside / upside levers:**

| Lever | Downside | Upside |
|---|---|---|
| Opportunities | ×0.6 | ×1.3 |
| Win rate | −5 pts | +5 pts |
| Sales cycle | +3 months | −2 months |
| Price | ×0.8 | ×1.1 |
| Assessment → subscription | 24% | 44% |
| Harness attach | 20% | 50% |
| Harness renewal | 50% | 75% |
| FedRAMP | Never | FY2 month 2 |

### Base by line ($M, gross)

| Line | FY1 | FY2 | FY3 | 3-yr |
|---|---|---|---|---|
| Mapper assessment | 1.28 | 2.66 | 4.04 | 7.98 |
| Mapper implementation | 0.61 | 1.75 | 2.93 | 5.28 |
| Mapper subscription | 0.03 | 0.33 | 1.30 | 1.66 |
| Mapper county channel | 0 | 0.18 | 0.49 | 0.67 |
| Harness (assessment / implementation / assurance) | 0.21 | 1.31 | 2.88 | 4.41 |
| Data-generator packs | 0.19 | 0.43 | 0.69 | 1.31 |
| **Core gross** | **2.31** | **6.67** | **12.32** | **21.29** |
| **Core incremental** | 1.73 | 5.28 | 10.09 | 17.09 |
| Pull-through (separate) | 1.04 | 2.75 | 4.56 | 8.36 |

## Appendix B: Cost formulas and inputs

- **Payback formulas.**
  - Clients needed to cover run cost: `N_run = F / (A − v)`.
  - Clients needed to repay upfront within T years: `N_T = (F + I/T) / (A − v − CAC/L)`.
  - Mapper at $250K ACV: 8.2 clients to cover run cost; 23.6 to repay upfront within 3 years (round-1 cost parameters).
- **Delivery cost by line (ESTIMATE).**
  - Assessments 45% (GM 55%).
  - Implementations 65%.
  - Data-generator packs 58%.
  - Subscriptions 54% (A) / 30% (B); assurance 59% / 35%.
- **Fixed run cost per year.**
  - A: data generator $0.24M, mapper $0.67M, harness $0.64M, plus $0.45M/yr continuous monitoring after authorization.
  - B: data generator $0.08M, mapper $0.56M, harness $0.35M.
- **Hardening by product (FTE-months / $).** Data generator 19 / $466K; mapper 47 / $1.63M (incl. $768K ATO path); harness 39 / $1.11M; improper-payment 25 / $615K.
- **LLM inference** is minor: about $3.5K per mapper client per year and $10K per harness client per year. Labor drives cost.
- **County economics.** 25% partner margin plus $10K of Guidehouse pre-sales per deal.

## Appendix C: Reconciliation log

| # | Conflict | Resolution |
|---|---|---|
| R1 | Subscription conversion 40% (revenue) vs 30–40% (buyer) | 35%; federal SaaS ≥12 months after authorization |
| R2 | Harness renewal 85% vs 50–60% | 60% (downside 50%, upside 75%) |
| R3 | Conflict of interest not modeled | −40% of harness opportunities in integrator accounts (−$1.08M, the largest single ruling) |
| R4 | Data-generator revenue $2.0M vs ~$0 | Packs only ($1.31M); royalties in upside only |
| R5 | Improper-payment $2.5M vs $0 | $0 base; upside only |
| R6 | Incrementality ignored | Report gross and incremental; net out 40% of assessments |
| R7 | Selling from month 0 vs hardening first | Consultant-run assessments from month 3; managed service from month 9 |
| R8 | Mapper subscription $300K vs $100–600K | $250K federal |
| R9 | Harness price | $200K per year; portfolio tier in upside only |
| R10 | CIO-SP4 | Dropped (cancelled) |
| R11 | County sales cost | Channel only; 25% partner margin + $10K per deal |
| R12 | Lapsed TMF/SLCGP funding | State win rate −5 pts |
| R13 | Cost model used placeholder revenue | Re-plugged with reconciled revenue |
| R14 | Devil's case ($7.6M) vs base ($21.3M) | Kept as a stress case; kill criteria decide by FY2 |
| R15 | Devil's hardening $5.2M vs $3.83M | $3.83M (A) / $2.29M (B) used; code audit at handoff to verify |
| R16 | Growth impacts sized on a ~$17M placeholder base | Used as directional ESTIMATES, with a 30% overlap haircut |

## Appendix D: Full growth list (top 12 of 19, weighted score)

Weights: revenue 40%, cost 20%, time 20%, risk 20%.

| # | Idea | Score |
|---|---|---|
| 1 | Price under the SAT + vehicle plan | 4.40 |
| 2 | Per-system harness pricing + portfolio tier | 4.20 |
| 3 | Maturity Model as the front door | 4.00 |
| 4 | Internal-first on fixed-price work | 4.00 |
| 5 | FedRAMP after 5 letters of intent | 4.00 |
| 6 | M-25-22 pre-award vendor evaluation | 3.60 |
| 7 | Open-source the data generator + paid packs | 3.60 |
| 8 | Hyperscaler marketplaces + co-sell (+$1.0M) | 3.60 |
| 9 | Drop improper-payment product; demo sandbox (+$1.1M value) | 3.40 |
| 10 | Independence firewall + dual harness SKU (+$1.4M) | 3.40 |
| 11 | Medicaid 90/10 module (+$2.1M) | 3.20 |
| 12 | Vant4ge embedded attach (+$1.65M) | 3.20 |
| 13 | UK ATRS / AI Playbook / Inspect (+$1.3M) | 3.20 |

**Also on the list:** licensing rule packs to other firms (+$0.75M), recruiting pipeline (~$0.4M), and a county kit (viable only if sales cost is under $10K per county).

**Mutually exclusive:**
- Open-sourcing the harness core rules out licensing that core.
- The M-25-22 service bars Guidehouse from bidding on the same procurement.

## Appendix E: Sources and working files

Contract awards come from USAspending; labor rates come from the GSA CALC+ API (queried 29 October 2026). Policy citations (OMB M-25-21/22, M-26-04, the Advancing American AI Act, TRAIGA, the CIO-SP4 cancellation, TMF/SLCGP lapse, NASCIO 2026 priorities) and benchmark sources (FedRAMP 20x cost, 3PAO, capstone fees) are cited with URLs in the analyst workpapers in `./capstone_review_workpapers/`:

- `01_revenue_modeler.md`, `06_revenue_reconciled.md`, model `rev2.py`
- `02_cost_margin.md`, `09_cost_reconciled.md`, models `cost3.py`, `sens3.py`
- `03_market_competition.md`, `04_buyer.md`
- `07_devil_advocate.md` (15 kill criteria), `08_growth_strategist.md` (19 ideas)
- `05_reconciliation_rulings.md`

**Not verified (ESTIMATE):**
- Firm revenue (~$3B) and the 1% materiality threshold.
- The $30M advisory book and its hourly-billed share.
- Integrator shares.
- Code survival.
- Pull-through ratio.
- County bid thresholds.
- CDAO BPA and OASIS+ domain holdings.
- The $8M/yr internal governance labor.
