# 01 — Revenue Model (revenue_modeler)

**Scope.** This is a 3-year revenue model for the capstone program: the synthetic data generator (DG), the policy-to-AI-governance mapper (MAP), the agentic eval/red-team harness (HAR), and the optional improper-payment analytics (IP), which is shown as a separate line. FY1 starts in month 0, the month the first capstone cohort delivers. All $ figures are USD thousands ($K) unless shown as $M. UK figures are converted to USD at about 1.30 $/£ (ESTIMATE).

**Model source.** A deterministic Python model at `/tmp/claude-0/-home-user-Learning-env/597ac1d9-a808-55f6-8cf9-a6a3d19428fc/scratchpad/model/rev.py` produced every number in the tables. Change an input there and re-run it to reconcile with other workstreams.

**Labeling.** Every input is an **ESTIMATE** unless a URL is cited next to it.

---

## 0. Headline (base / downside / upside)

| $M | FY1 | FY2 | FY3 | 3-yr | FY3 exit ARR |
|---|---|---|---|---|---|
| **Core program (DG+MAP+HAR), base** | 2.50 | 7.40 | 13.95 | **23.8** | 5.0 |
| Core, downside | 0.63 | 1.88 | 3.75 | 6.3 | 0.8 |
| Core, upside | 5.58 | 16.20 | 29.93 | 51.7 | 12.3 |
| Improper-payment analytics (separate), base | 0.00 | 0.75 | 1.75 | 2.5 | — |
| Pull-through services (separate, NOT product), base | 1.08 | 2.90 | 4.92 | 8.9 | — |
| **Everything incl. IP + pull-through, base** | 3.58 | 11.05 | 20.62 | 35.3 | — |

What the base case says:

1. **The mapper is the business.** It produces about 68% of core revenue ($16.2M of $23.8M).
2. **Recurring revenue is a small share in this window.** Recurring is only 6% of core in FY2 and 25% in FY3.
3. **Most "product" revenue is really assessments and implementations.** About 75% of the 3-yr core is one-time, labor-delivered work. The cost analyst should apply services margins to it, not software margins.
4. **FedRAMP timing matters less than expected.** Moving FedRAMP from mid-FY2 to "never in window" costs only about $0.75M over 3 years. The client-hosted path absorbs most of the demand. The levers that dominate are **pipeline volume, win rate, and price**: −5 pts of win rate costs $3.8M over 3 years, and −20% price costs $4.7M.

---

## 1. Price points used (for reconciliation with market_and_competition_analyst)

All prices are ESTIMATE, anchored to the benchmarks below. Recurring lines escalate 3%/yr.

| Product / component | Fed civ (FC) | Fed health (FH) | Defense (DoD) | State/local (SL) | UK (TS4) |
|---|---|---|---|---|---|
| MAP assessment (fixed-price gap analysis + AI use-case inventory + impact assessments, ~10–12 wks) | 250 | 250 | 250 | 150 | 180 |
| MAP implementation (load the agency control catalog/SSP, integrate with GRC/eMASS/ServiceNow, train) | 400 | 400 | 400 | 200 | 250 |
| MAP managed service subscription, /yr | 300 | 300 | 300 | 150 | 200 |
| HAR assessment (red-team/eval of ~4–6 AI systems/agents + audit-ready report) | 175 | 175 | 225 | 100 | 140 |
| HAR implementation (install harness in the agency's CI/CD or ATO pipeline) | 200 | 200 | 250 | 100 | 150 |
| HAR recurring assurance, /yr (quarterly re-tests + continuous monitoring) | 200 | 200 | 250 | 100 | 150 |
| DG custom dataset pack (one-time) | 60 | 60 | 60 | 60 | 60 |
| DG implementation into test/training environment | 80 | 80 | 80 | 80 | 80 |
| DG license, /yr per environment | 50 | 50 | 50 | 50 | 50 |
| DG OEM/embed royalty (Vant4ge + SI partners), program-level | FY1 0, FY2 150, FY3 300 | | | | |
| IP pilot (FH only) | — | 750 | — | — | — |
| IP production managed analytics, /yr (FH only) | — | 2,000 | — | — | — |

Scenario multipliers: downside ×0.8 on all prices, upside ×1.1.

**Benchmarks behind the prices:**

- **Governance subscription.** Commercial AI-governance platforms are estimated at about $100–175K/yr (professional) and $200–350K+/yr (enterprise) for Credo AI. Broader estimates run $30–150K/yr, and some sources put enterprise contracts at $120–500K/yr. Sources: https://aitoolsatlas.ai/tools/credo-ai/pricing, https://saaswithalex.pages.dev/posts/enterprise-ai-governance-platforms-compared/. Credo prices per AI use case, sold through private offer (https://aws.amazon.com/marketplace/pp/prodview-x67krdatcdday). At $300K/yr, MAP is priced at the top of the commercial range. That is defensible only because it bundles managed analyst labor. *This is the number most likely to be contested.*
- **Red-team engagements.** Commercial LLM red-team engagements run about $6–45K+ (https://securitywall.co/blog/llm-security-audit-cost) and average about $30–50K (https://aona.ai/blog/ai-red-teaming-cost-roi-enterprise-budget-2026/). Per-test pricing ranges from $8K to $150K by system shape (https://repello.ai/blog/ai-red-teaming-vendor-pricing). The HAR assessment at $175K is therefore about 4–6 systems at around $35K each, plus federal reporting overhead.
- **Federal assessment task orders.** I found no public award value for M-25-21 governance task orders. A VA solicitation for AI governance framework development exists with no value disclosed (https://www.cleat.ai/government/contracts/ai-governance-framework-development-vj30). The $250K MAP assessment is ESTIMATE, sized at roughly 4 FTE × 12 weeks at blended federal rates.
- **Improper-payment market size.** CMS FY2025 improper payments were Medicare FFS $28.83B, MA $23.67B, Medicaid $37.39B, and CHIP $1.37B (https://cms.gov/newsroom/fact-sheets/fiscal-year-2025-improper-payments-fact-sheet). The prize is large, but IP pricing is ESTIMATE.

---

## 2. Segment assumptions

| Segment | MAP qualified opps opened FY0 / FY1 / FY2 / FY3 | Win rate | Sales cycle (mo) | HAR standalone opps FY0–FY3 | Notes |
|---|---|---|---|---|---|
| Fed civilian | 4 / 10 / 18 / 24 | 30% | 9 | 0/2/4/6 | Sold as task orders or mods on existing BPAs/IDIQs. A new vehicle would add 6–12 months. |
| Fed health | 4 / 8 / 13 / 15 | 40% | 6 | 0/1/3/4 | Incumbency in the large FH practice (HHS opdivs). This is the shortest path. |
| Defense | 0 / 3 / 6 / 8 | 20% | 15 | 0/4/8/10 | M-25-21 exempts National Security Systems (https://www.mondaq.com:443/unitedstates/new-technology/1621604/omb-directs-agencies-to-accelerate-ai-adoption-and-devise-governance-strategy), so MAP fits DoD poorly. HAR (T&E of agents) is the DoD wedge. |
| State/local | 2 / 8 / 16 / 24 | 30% | 9 | 0/1/3/5 | Smaller tickets. Vant4ge HHS/justice channel. Procurement through cooperative contracts. |
| UK (TS4) | 2 / 5 / 10 / 13 | 25% | 6 | 0/2/3/4 | TS4 Lots 1–5a allow award without competition (https://www.find-tender.service.gov.uk/Notice/001978-2026). Framework est. £16B (same source). Guidehouse UK brand is weak, which keeps the win rate modest. |

- **FY0 opportunities.** These are pipeline opened during the capstone year. They are sold on Guidehouse's existing AI Readiness Maturity Model and a demo, before the product exists.
- **Sales-cycle benchmarks.** Government tech buys take about 22 months on average, per Gartner 2022 as cited secondhand (https://starbridge.ai/blog/how-to-shorten-government-sales-cycle). Other benchmarks are 6–18 months to a first sale (https://www.fedmarket.com/article/free_content/481) and 180–365 days (https://www.devcommx.com/abm-agency/washington-dc/government-tech).
- **Why my cycles are shorter.** I assume 6–15 months, which is shorter than the benchmarks. These are **existing-client expansions on existing vehicles**, not new-vendor sales. The downside case adds +3 months to every cycle.

**Resulting base new logos (MAP assessment wins):**

| Segment | FY1 | FY2 | FY3 | 3-yr |
|---|---|---|---|---|
| FC | 1.65 | 3.60 | 5.85 | 11.1 |
| FH | 2.40 | 4.20 | 5.60 | 12.2 |
| DoD | 0.00 | 0.45 | 1.05 | 1.5 |
| SL | 1.05 | 3.00 | 5.40 | 9.5 |
| UK | 0.88 | 1.88 | 2.88 | 5.6 |
| **Total** | **6.0** | **13.1** | **20.8** | **~40** |

**HAR clients (attach + standalone):**

| | FY1 | FY2 | FY3 | 3-yr |
|---|---|---|---|---|
| Attach (via MAP) | 1.0 | 3.4 | 5.9 | 10.3 |
| Standalone | 0.7 | 3.2 | 6.1 | 10.0 |
| **Total** | **1.7** | **6.6** | **12.0** | **~20** |

Downside totals: MAP 2.3 / 5.5 / 9.6. Upside totals: MAP 10.5 / 22.0 / 33.1.

---

## 3. Formulas (exactly as implemented)

Notation: `s` = segment, `Y` = FY1..FY3, `pm` = scenario price multiplier, `esc` = 3%.

**Sales-cycle landing.** Opportunities open evenly through a year and close `d` months later. The share that lands `k` years later is:

`land_k(d) = overlap([d, 12+d], [12k, 12k+12]) / 12`

| Cycle | Lands same year | Lands next year | Lands in 2 years |
|---|---|---|---|
| 6 mo | 0.50 | 0.50 | — |
| 9 mo | 0.25 | 0.75 | — |
| 15 mo | 0 | 0.75 | 0.25 |

**Wins:**

`MAPwins[s,Y] = Σ_{y0=FY0..Y} opps_MAP[s,y0] × land_{Y−y0}(cycle_s) × win_s`

**Mapper:**

- `Rev_MAP_assess[Y] = Σ_s MAPwins[s,Y] × MAP_assess_$[s] × pm`
- `MAPimpl[s,Y] = conv_impl × (0.5·MAPwins[s,Y] + 0.5·MAPwins[s,Y−1])`, with conv_impl = 50% base, 35% down, 60% up. Half of implementations land in the same FY as the assessment, half in the next.
- `Rev_MAP_impl[Y] = Σ_s MAPimpl[s,Y] × MAP_impl_$[s] × pm`
- `NewSubs_MAP[s,Y] = MAPimpl[s,Y] × conv_sub × gate[s,Y] × dodmult_s + recovered_deferred[s,Y]`, with conv_sub = 80% base, 65% down, 85% up, and dodmult = 0.5 for DoD (in-enclave only).
- `Active_MAP[s,Y] = Active_MAP[s,Y−1] × (1 − churn_MAP) + NewSubs_MAP[s,Y]`
- `Rev_MAP_sub[Y] = Σ_s (Active_MAP[s,Y−1] × (1 − churn) + 0.5 × NewSubs_MAP[s,Y]) × MAP_sub_$[s] × pm × (1+esc)^(Y−1)`. New subscriptions count for half a year in their start year.

**Harness:**

- `HARattach[s,Y] = attach_HAR × (0.5·MAPwins[s,Y] + 0.5·MAPwins[s,Y−1])`, with attach = **35% of mapper clients buy the harness** base, 20% down, 50% up.
- `HARwins[s,Y] = Σ opps_HAR[s,y0] × land × win_s + HARattach[s,Y]`
- `Rev_HAR_assess[Y] = Σ_s HARwins[s,Y] × HAR_assess_$[s] × pm`
- `Rev_HAR_impl[Y] = Σ_s 40% × (0.5·HARwins[Y] + 0.5·HARwins[Y−1]) × HAR_impl_$[s] × pm`
- `NewSubs_HAR[s,Y] = conv_HAR × (0.5·HARwins[Y] + 0.5·HARwins[Y−1]) × gate_HAR[s,Y]`, with conv_HAR = 60% base, 45% down, 70% up. Revenue follows the same retained + half-year formula with churn_HAR.

**Data generator (attach and OEM; no standalone direct sales):**

- `DGpacks[s,Y] = attach_DG × (MAPwins[s,Y] + HARstandalone[s,Y])`, with attach_DG = 30% base, 15% down, 45% up.
- `Rev_DG_pack[Y] = Σ DGpacks × 60 × pm`
- `Rev_DG_impl[Y] = Σ 30% × DGpacks × 80 × pm`
- `NewLic_DG = 40% × DGpacks`; license revenue follows the subscription formula with churn_DG.
- `Rev_DG_OEM[Y]` = fixed schedule: 0 / 150 / 300 base, 0 / 0 / 100 down, 100 / 300 / 600 up.

**Improper payments (separate line):**

`Rev_IP[Y] = pilots[Y] × 750 × pm + (Σ_{y<Y} prod[y] + 0.5 × prod[Y]) × 2,000 × pm`

| Scenario | Pilots FY1 / FY2 / FY3 | Production starts FY1 / FY2 / FY3 |
|---|---|---|
| Base | 0 / 1 / 1 | 0 / 0 / 1 |
| Down | 0 / 0 / 1 | 0 / 0 / 0 |
| Up | 1 / 2 / 1 | 0 / 1 / 1 |

**Pull-through (separate, NOT added to product lines):**

`PullThrough[Y] = pull_ratio × (Rev_MAP_assess + Rev_MAP_impl + Rev_HAR_assess + Rev_HAR_impl)[Y]`, with pull_ratio = 0.5 base, 0.3 down, 0.7 up.

This represents downstream ATO support, AI-system remediation, data modernization, and use-case build work that the assessments surface. It is ESTIMATE and the most contestable number in this file. It is reported separately to avoid double-counting.

**Worked example (base, FC mapper assessments, FY2).**

- Opportunities: FY1 = 10 and FY2 = 18. FC cycle = 9 months, so 25% of an opp cohort lands in the same year and 75% in the next.
- `MAPwins_FC_FY2 = (10 × 0.75 + 18 × 0.25) × 0.30 = (7.5 + 4.5) × 0.30 = 3.6`
- `Rev_MAP_assess_FC_FY2 = 3.6 × $250K = $900K`

---

## 4. Authorization (ATO / FedRAMP / StateRAMP→GovRAMP) gating

**Ungated from day 1:**

- All assessments and implementations. Guidehouse delivers them with consultant-operated tooling.
- MAP when it runs on public regulations plus client documents inside a Guidehouse CUI enclave, or **inside the agency's own cloud tenant**, where it inherits the agency's ATO through an agency-specific authorization (about 3–6 months, absorbed in the half-year subscription convention).
- HAR, which by nature runs inside the agency environment against the agency's agents.
- All UK work. UK assurance is Cyber Essentials Plus/ISO 27001, not FedRAMP.
- DoD work, which is in-enclave only.

**Gated: the Guidehouse-hosted multi-tenant SaaS option.** I assume some buyers *only* buy hosted SaaS and defer until it is authorized:

- MAP subscriptions: FC 40%, FH 40%, SL 50%.
- HAR subscriptions: half of those shares (20% / 20% / 25%).
- Formula: `gate[s,Y] = 1 − saas_share_s × (1 − auth_frac[Y])`.
- Deferred buyers convert at 70% in the year authorization arrives. The other 30% are lost to the delay.

**Federal: FedRAMP 20x Moderate.**

- Status: the Phase 2 Moderate pilot finished in March 2026 with 8 initial authorizations, and Phase 3 began April 2026 (https://fedramp.gov/20x/timeline/). Public Class B/C pipelines (Moderate ≈ Class C) are reported to open 31 Aug 2026, per a secondary source (https://knoxsystems.com/resources/fedramp-news-2026). Other sources say traditional timelines have not shortened: 9–14 months minimum for new vendors in 2026 (https://starbridge.ai/blog/how-to-shorten-government-sales-cycle).
- Base: submit early in FY1 after hardening, and get authorized at **FY2 month 6** (auth_frac = 0 / 0.5 / 1.0).
- Upside: FY2 month 2 (0 / 0.85 / 1).
- Downside: **not authorized within FY1–FY3** (0 / 0 / 0). That is plausible if no agency sponsor or 20x Class C slot materializes.
- DoD IL4/IL5 is not modeled in the window.

**State/local: GovRAMP (formerly StateRAMP).**

- Ready status takes about 3–6 months and full authorization about 12–18 months (https://www.a-lign.com/articles/guide-to-the-stateramp-authorization-process, https://govramp.org/ready). Many states accept Ready or a Progressing Snapshot.
- Base: effective acceptance at FY1 month 6 (0.5 / 1 / 1). Down: 0 / 0.5 / 1. Up: 0.75 / 1 / 1.

**Improper payments: real-data gated.** A synthetic-claims proof of concept sells without authorization. Production on real CMS or state Medicaid claims requires a system ATO plus a data use agreement, so production starts no earlier than FY3 in base.

**Sensitivity (base core 3-yr = $23.84M):**

| Change | 3-yr core | Δ |
|---|---|---|
| FedRAMP never in window | $23.10M | −0.74 |
| FedRAMP at FY1 end | $24.01M | +0.17 |
| Sales cycles +3 mo | $20.32M | −3.52 |
| Win rates −5 pts | $20.05M | −3.79 |
| Prices −20% | $19.17M | −4.67 |
| HAR attach 20% / 50% | $22.65M / $25.03M | −1.19 / +1.19 |
| Churn MAP 20% / HAR 25% | $23.63M | −0.21 |

Churn barely moves the total because the recurring base is still small within 3 years. It matters a lot to FY4+ value.

---

## 5. Churn / renewal

| Line | Base | Down | Up | Rationale |
|---|---|---|---|---|
| MAP subscription | 10% | 20% | 5% | Government renewals are option-year exercises. Non-exercise happens on budget cuts or recompetes. |
| HAR assurance | 15% | 25% | 10% | More discretionary. Tied to how many AI systems are in production. |
| DG license | 20% | 30% | 15% | Easily substituted by open-source synthetic tools (e.g., Synthea for health). |

All churn rates are ESTIMATE. Churn applies to the prior-year active base from FY2 onward. Escalator is 3%/yr.

---

## 6. Per-product × per-year tables ($M)

### Base

| Line | FY1 | FY2 | FY3 | 3-yr |
|---|---|---|---|---|
| MAP assessment | 1.33 | 2.85 | 4.45 | 8.63 |
| MAP implementation | 0.51 | 1.60 | 2.79 | 4.91 |
| MAP subscription | 0.10 | 0.66 | 1.95 | 2.71 |
| **Mapper subtotal** | **1.94** | **5.11** | **9.19** | **16.24** |
| HAR assessment | 0.27 | 1.06 | 1.94 | 3.26 |
| HAR implementation | 0.06 | 0.29 | 0.66 | 1.02 |
| HAR recurring assurance | 0.04 | 0.29 | 0.98 | 1.31 |
| **Harness subtotal** | **0.37** | **1.64** | **3.58** | **5.59** |
| DG dataset packs | 0.12 | 0.29 | 0.48 | 0.90 |
| DG implementation | 0.05 | 0.12 | 0.19 | 0.36 |
| DG license | 0.02 | 0.08 | 0.20 | 0.30 |
| DG OEM (Vant4ge/SI) | 0.00 | 0.15 | 0.30 | 0.45 |
| **Data-gen subtotal** | **0.19** | **0.64** | **1.17** | **2.01** |
| **CORE PROGRAM TOTAL** | **2.50** | **7.40** | **13.95** | **23.84** |
| of which recurring | 0.16 | 1.18 | 3.43 | 4.77 |
| Improper-payment analytics (separate) | 0.00 | 0.75 | 1.75 | 2.50 |
| **Core + IP** | 2.50 | 8.15 | 15.70 | 26.34 |
| Pull-through services (separate) | 1.08 | 2.90 | 4.92 | 8.91 |
| **Grand total incl. pull-through** | 3.58 | 11.05 | 20.62 | 35.25 |

Base core by segment, 3-yr: FC 7.26, FH 8.23, DoD 1.56, SL 3.44, UK 2.90, plus OEM 0.45.

### Downside

| Line | FY1 | FY2 | FY3 | 3-yr |
|---|---|---|---|---|
| MAP (assess / impl / sub) | 0.41 / 0.11 / 0.02 | 0.97 / 0.37 / 0.09 | 1.66 / 0.71 / 0.26 | 4.60 |
| HAR (assess / impl / sub) | 0.04 / 0.01 / 0.00 | 0.26 / 0.07 / 0.04 | 0.54 / 0.18 / 0.15 | 1.31 |
| DG (pack / impl / lic / OEM) | 0.02 / 0.01 / 0.00 / 0 | 0.05 / 0.02 / 0.01 / 0 | 0.09 / 0.04 / 0.03 / 0.10 | 0.36 |
| **CORE** | **0.63** | **1.88** | **3.75** | **6.26** |
| IP (separate) | 0 | 0 | 0.60 | 0.60 |
| Pull-through (separate) | 0.17 | 0.50 | 0.93 | 1.60 |
| Grand total | 0.80 | 2.38 | 5.28 | 8.46 |

### Upside

| Line | FY1 | FY2 | FY3 | 3-yr |
|---|---|---|---|---|
| MAP (assess / impl / sub) | 2.53 / 1.17 / 0.26 | 5.23 / 3.57 / 1.72 | 7.76 / 5.95 / 4.85 | 33.05 |
| HAR (assess / impl / sub) | 0.70 / 0.15 / 0.12 | 2.44 / 0.70 / 0.85 | 4.19 / 1.47 / 2.74 | 13.35 |
| DG (pack / impl / lic / OEM) | 0.35 / 0.14 / 0.06 / 0.10 | 0.82 / 0.33 / 0.24 / 0.30 | 1.28 / 0.51 / 0.56 / 0.60 | 5.31 |
| **CORE** | **5.58** | **16.20** | **29.93** | **51.71** |
| IP (separate) | 0.83 | 2.75 | 4.13 | 7.70 |
| Pull-through (separate) | 3.19 | 8.36 | 13.56 | 25.10 |
| Grand total | 9.59 | 27.31 | 47.61 | 84.51 |

Scenario levers (down / up vs. base):

| Lever | Downside | Upside |
|---|---|---|
| Opportunities | ×0.6 | ×1.3 |
| Win rate | −5 pts | +5 pts |
| Sales cycle | +3 mo | −2 mo |
| Price | ×0.8 | ×1.1 |
| MAP conversion (impl / sub) | 35% / 65% | 60% / 85% |
| HAR attach | 20% | 50% |
| HAR subscription conversion | 45% | 70% |
| DG attach | 15% | 45% |
| Churn | Higher (see §5) | Lower (see §5) |
| FedRAMP | Never in window | FY2 month 2 |
| GovRAMP | Later | Earlier |
| IP pilots / production | Fewer | More |
| Pull-through ratio | 0.3 | 0.7 |

---

## 7. How the data generator monetizes (explicit choice)

I modeled DG as an **attach and enabler, not a standalone direct-sale product**. It reaches about $2.0M over 3 years in base, roughly 8% of core.

- 30% of new MAP and standalone-HAR logos buy a custom dataset pack ($60K).
- 30% of those buy an implementation ($80K).
- 40% take a $50K/yr license.
- OEM/embed royalties come through Vant4ge and SI partners.

**Its main value is internal and not counted as revenue.** It cuts demo and test costs, enables the HAR (synthetic PII test fixtures), and enables the IP proof of concept without real data.

**Recommendation for the orchestrator:** treat DG as a cost/enabler line for go/no-go purposes. A free or open release could be argued for, since the revenue at stake is only about $0.3–1.2M/yr. I am flagging this for market_and_competition_analyst, who is assessing the giveaway vs. bundle question.

---

## 8. Caveats and dependencies

1. **Incrementality is not netted out.** An estimated 30–50% of FH/FC MAP assessment revenue is AI-governance consulting that Guidehouse's AI CoE would likely win anyway on the existing Maturity Model. The cost_and_margin_analyst and orchestrator should haircut by that much when attributing to the capstone program. Only recurring lines and DG/HAR licenses are clearly incremental.
2. **For cost_and_margin_analyst.**
   - Assessment and implementation lines are labor-delivered. Use consulting margins (about 25–35%), not SaaS margins.
   - Recurring lines are about $4.8M over 3 years in base.
   - Hosting cost depends on the FedRAMP decision. Downside assumes no SaaS and therefore no FedRAMP spend, which is a cost saving, not just a revenue loss.
   - Moderate authorization costs are estimated at $500K–$2M+ (https://guardsarm.com/compare/fedramp-vs-stateramp/).
3. **For market_and_competition_analyst.** MAP subscription at $300K/yr fed is above most commercial AI-governance SaaS pricing. If agencies benchmark against Credo AI or OneTrust, or get it via GOTS or free NIST tooling, MAP subscriptions fall toward $100–150K. That is roughly a −$1.4M 3-yr impact in base, from the subscription line alone.
4. **Missing FY1 hardening gap.** The capstone delivers a prototype, not a product. The model sells assessments from month 0, using the tool consultant-side. If the CoE needs 6–9 months to harden before any client use, shift FY1 down by about 40%.
5. **Fractional clients.** The model produces expected values, such as 0.45 DoD wins. Actual outcomes are lumpy, and a single FH production IP deal (about $2M/yr) swings the total materially.
6. **Pipeline volume is the biggest unverified input.** About 104 base MAP opportunities over FY0–FY3. public_sector_buyer should sanity-check whether 18–24 federal civilian AI-governance opportunities a year is realistic for Guidehouse accounts.

### Sources

- https://fedramp.gov/20x/timeline/
- https://knoxsystems.com/resources/fedramp-news-2026
- https://starbridge.ai/blog/how-to-shorten-government-sales-cycle
- https://www.fedmarket.com/article/free_content/481
- https://www.devcommx.com/abm-agency/washington-dc/government-tech
- https://www.a-lign.com/articles/guide-to-the-stateramp-authorization-process
- https://govramp.org/ready
- https://guardsarm.com/compare/fedramp-vs-stateramp/
- https://aitoolsatlas.ai/tools/credo-ai/pricing
- https://saaswithalex.pages.dev/posts/enterprise-ai-governance-platforms-compared/
- https://aws.amazon.com/marketplace/pp/prodview-x67krdatcdday
- https://securitywall.co/blog/llm-security-audit-cost
- https://aona.ai/blog/ai-red-teaming-cost-roi-enterprise-budget-2026/
- https://repello.ai/blog/ai-red-teaming-vendor-pricing
- https://www.cleat.ai/government/contracts/ai-governance-framework-development-vj30
- https://www.mondaq.com:443/unitedstates/new-technology/1621604/omb-directs-agencies-to-accelerate-ai-adoption-and-devise-governance-strategy
- https://cms.gov/newsroom/fact-sheets/fiscal-year-2025-improper-payments-fact-sheet
- https://www.find-tender.service.gov.uk/Notice/001978-2026
