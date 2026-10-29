# 06 — Reconciled Revenue Model (revenue_modeler, round 2)

**What this applies.** This round applies the lead partner's rulings R1–R12 from `05_reconciliation_rulings.md`. Context for those rulings came from `03_market_competition.md` and `04_buyer.md`.

**Model.** The model is `/tmp/claude-0/-home-user-Learning-env/597ac1d9-a808-55f6-8cf9-a6a3d19428fc/scratchpad/model/rev2.py`. The waterfall in the changes table comes from `/tmp/claude-0/-home-user-Learning-env/597ac1d9-a808-55f6-8cf9-a6a3d19428fc/scratchpad/model/waterfall.py`.

- **Monthly resolution.** The model now runs month by month: months 1–36 are FY1–FY3, and FY1 month 1 is the month the capstone delivers. Round 1 was annual. The switch was needed so R7 (hardening) and R1 (subscriptions only after authorization) could be timed properly.
- **Units.** All figures are $M unless marked $K.
- **Sources.** Inputs not cited in round 1 (`01_revenue_modeler.md`) or in files 03/04 are ESTIMATE.

**Definitions.**

- **GROSS** = all revenue booked to the program.
- **INCREMENTAL** = GROSS − 40% × (mapper assessments + harness assessments). This follows R6. The 40% is the share Guidehouse would win anyway on the existing AI Readiness Maturity Model. I use 50% in the downside and 30% in the upside, which spans the 30–50% range behind the ruling.
- **Separate lines, not in core.** Pull-through services and improper-payment analytics (IP) are kept out of core totals. IP is upside only, per R5.

---

## 1. Headline

| Case | FY1 | FY2 | FY3 | **3-yr GROSS** | **3-yr INCREMENTAL** | End-FY3 recurring run-rate | Pull-through (gross / incr.), separate |
|---|---|---|---|---|---|---|---|
| **Base** | 2.31 | 6.67 | 12.32 | **21.3** | **17.1** | **3.2** | 8.4 / 6.3 |
| Downside | 0.64 | 1.90 | 3.65 | **6.2** | **4.4** | 0.55 | 1.6 / 1.1 |
| Upside (core) | 5.16 | 14.82 | 28.30 | **48.3** | **42.3** | 11.7 | 22.8 / 18.6 |
| Upside + IP (separate, contingent) | +0.83 | +2.75 | +4.13 | **+7.7 → 56.0** | **+7.7 → 50.0** | +4.4 IP run-rate | — |

**End-FY3 recurring run-rate** is defined as month-36 active subscriptions × annual price. It includes portfolio contracts, county update fees and royalties where they apply.

How the base compares with round 1:

- Base gross falls **$2.5M**, from $23.8M to $21.3M.
- Base incremental is **$6.7M** below round-1 gross.
- End-FY3 recurring run-rate falls from $5.0M to **$3.2M**.

The program in this window is **about 87% one-time assessment and implementation work** (base FY1–FY3 recurring revenue is $2.7M of $21.3M). The recurring line only becomes material after FY3.

---

## 2. Per-product × per-year — BASE (GROSS)

| Line | FY1 | FY2 | FY3 | 3-yr |
|---|---|---|---|---|
| Mapper assessment | 1.28 | 2.66 | 4.04 | 7.98 |
| Mapper implementation | 0.61 | 1.75 | 2.93 | 5.28 |
| Mapper subscription / managed service | 0.03 | 0.33 | 1.30 | 1.66 |
| Mapper county package via channel (R11): fixed fee + update service | 0.00 | 0.18 | 0.49 | 0.67 |
| **Mapper subtotal** | **1.92** | **4.92** | **8.76** | **15.59** |
| Harness assessment | 0.17 | 0.81 | 1.54 | 2.53 |
| Harness implementation | 0.03 | 0.29 | 0.61 | 0.93 |
| Harness recurring assurance | 0.01 | 0.21 | 0.73 | 0.95 |
| **Harness subtotal** | **0.21** | **1.31** | **2.88** | **4.41** |
| Data generator: custom calibrated packs only (R4) | 0.19 | 0.43 | 0.69 | 1.31 |
| **CORE GROSS** | **2.31** | **6.67** | **12.32** | **21.29** |
| less non-incremental (40% × assessments) | −0.58 | −1.39 | −2.23 | −4.20 |
| **CORE INCREMENTAL** | **1.73** | **5.28** | **10.09** | **17.09** |
| of which recurring (gross) | 0.03 | 0.56 | 2.12 | 2.72 |
| IP analytics (R5) | 0 | 0 | 0 | 0 |
| Pull-through services (separate), gross | 1.04 | 2.75 | 4.56 | 8.36 |
| Pull-through services (separate), incremental | 0.75 | 2.06 | 3.44 | 6.25 |

**Base logos:**

| | FY1 | FY2 | FY3 | 3-yr |
|---|---|---|---|---|
| Mapper assessment wins | 5.7 | 11.9 | 18.0 | ≈36 |
| Harness clients | 1.1 | 4.9 | 9.3 | ≈15 |
| New mapper subscriptions | 0.5 | 2.1 | 6.3 | ≈9 |
| New harness subscriptions | 0.3 | 2.4 | 4.9 | ≈8, with 40% annual churn |
| DG packs | 1.9 | 4.3 | 6.9 | ≈13 |
| County channel deals | 0 | 4 | 10 | 14 |

## 3. Per-product × per-year — DOWNSIDE and UPSIDE (GROSS)

| Line | Down FY1 | FY2 | FY3 | **3-yr** | Up FY1 | FY2 | FY3 | **3-yr** |
|---|---|---|---|---|---|---|---|---|
| Mapper assess / impl / sub | .41/.16/.00 | .91/.47/.07 | 1.52/.86/.21 | **4.62** | 2.43/1.37/.06 | 4.87/3.57/.82 | 7.01/5.59/3.36 | **29.08** |
| Mapper county channel | 0 | .07 | .20 | **0.26** | .10 | .42 | .90 | **1.42** |
| Harness assess / impl / sub | .03/.00/.00 | .20/.07/.03 | .43/.17/.13 | **1.06** | .44/.09/.02 | 1.88/.68/.66 | 3.32/1.33/2.22 | **10.65** |
| Harness portfolio tier (R9, upside only) | — | — | — | — | 0 | .41 | 2.15 | **2.56** |
| DG packs | .03 | .07 | .13 | **0.23** | .55 | 1.21 | 1.81 | **3.57** |
| DG royalty, Vant4ge/SI (R4, upside only) | — | — | — | — | .10 | .30 | .60 | **1.00** |
| **CORE GROSS** | .64 | 1.90 | 3.65 | **6.18** | 5.16 | 14.82 | 28.30 | **48.27** |
| **CORE INCREMENTAL** | .42 | 1.35 | 2.67 | **4.44** | 4.29 | 12.79 | 25.20 | **42.29** |
| IP analytics (upside only, separate) | 0 | 0 | 0 | 0 | .83 | 2.75 | 4.13 | **7.70** |
| Pull-through (separate), gross / incr. | | | | 1.57 / 1.05 | | | | 22.81 / 18.62 |

## 4. Segment split (3-yr core GROSS, excluding IP)

| Segment | Base | Down | Up |
|---|---|---|---|
| Federal (civilian + health) | 14.40 (68%) | 4.26 | 32.08 (+7.7 IP) |
| Defense | 1.53 (7%) | 0.37 | 3.53 |
| State/local (states direct + county channel) | 2.59 (12%) | 0.79 | 5.60 |
| UK (TS4) | 2.78 (13%) | 0.76 | 6.07 |
| Program-level (royalty) | 0 | 0 | 1.00 |
| **Total** | **21.29** | **6.18** | **48.27** |

**End-FY3 recurring run-rate:**

| Case | Run-rate | Main drivers |
|---|---|---|
| Base | $3.2M | Mapper subscriptions ≈ $2.0M, harness ≈ $1.0M, county updates $0.14M |
| Down | $0.55M | — |
| Up | $11.7M core | Includes 3 portfolio contracts ≈ $3.0M and royalty $0.6M. IP production adds ≈ $4.4M on top. |

---

## 5. Formulas (as implemented, monthly; `m` = month 1–36, `FY(m)` = ⌈m/12⌉)

**Pipeline and wins.**

- Opportunities open evenly through each year: FY0 covers months −11..0, then FY1–FY3.
- Each opportunity closes at `m_close = m_open + cycle_s`.
- An opportunity with `m_close ≤ 0` is ordinary pre-program consulting and is excluded.
- `m_close` is floored at month 3, because consultant-operated assessments start at month 3 (R7).
- `MAPwins[s,m] = Σ opps_MAP[s,y0]/12 × win_s` over opportunities closing in month m.
- `HARwins[s,m] = HARstandalone[s,m] × COI_s + attach_HAR × MAPwins[s,m−6] × COI_s`
- `COI_s = 1 − 0.40 × integrator_share_s` (R3). Integrator share by segment (ESTIMATE): FC 40%, FH 70%, DoD 20%, SL 50%, UK 30%. This gives harness haircuts of FC −16%, FH −28%, DoD −8%, SL −20%, UK −12%.

**Mapper.**

- `Rev_MAP_assess = Σ MAPwins × MAP_assess_$`
- `Rev_MAP_impl[m+3] = 0.50 × MAPwins[m] × MAP_impl_$`. Implementation runs 3 months after the assessment.
- `NewSubs_MAP = 0.50 × 0.70 × MAPwins`, i.e. **35% of assessments become subscriptions (R1)**. DoD is ×0.5 (in-enclave only).
- Subscription start timing:
  - **Non-federal, and the consultant-operated or in-agency-boundary share of federal (60%):** start at `max(impl_end, month 9)` (R7).
  - **Federal SaaS-only share (40%):** start at `max(impl_end, auth_month + 12)`. In base, authorization at FY2 month 6 (month 18) means federal SaaS subscriptions start at **month 30, i.e. FY3 month 6** (R1 + R7).
- `Active[m] = Active[m−1] × (1 − churn)^(1/12) + NewSubs[m]`
- `Rev_sub[m] = Active[m] × price/12 × 1.03^(FY−1)`
- Churn is 10% for the mapper.

**Harness.**

- `Rev_HAR_assess = HARwins × HAR_assess_$`
- `Rev_HAR_impl[m+3] = 0.40 × HARwins[m] × HAR_impl_$`
- `NewSubs_HAR = 0.60 × HARwins`, starting at `max(m+3, month 9)`.
- No SaaS gate, because the harness runs inside the agency's environment.
- Churn is **40%, i.e. 60% renewal (R2)**.

**Portfolio tier (upside only, R9).**

- `Rev_portfolio = active_portfolio × $900K/yr` (midpoint of $0.6–1.2M).
- Starts: month 20, month 28 and month 32, one contract each.

**Data generator (R4).**

- `Rev_DG = 0.30 × (MAPwins + HARstandalone) × $100K per calibrated pack` (within the $50–150K range).
- No license line and no implementation line.
- Royalty $0.1M / $0.3M / $0.6M in upside only.

**Counties (R11, via the Vant4ge or cooperative-contract channel only).**

- `Rev_county_pkg = deals_FY × $40K`. Deals are 0 / 4 / 10 in base. The package is "AI policy + CJIS 6.0 crosswalk"; the buyer range is $25–50K.
- `Rev_county_upd = (prior deals + 0.5 × new deals) × 50% × $20K/yr`
- State/local direct opportunities are now **states only**: 2 / 6 / 10 / 12, down from 2 / 8 / 16 / 24.

**Incrementality and pull-through.**

- `INCR = GROSS − nonincr × (Rev_MAP_assess + Rev_HAR_assess)`, with nonincr = 0.40 base, 0.50 down, 0.30 up (R6).
- `Pull_gross = ratio × (MAP assess + impl + HAR assess + impl)`, with ratio 0.5 base, 0.3 down, 0.7 up.
- `Pull_incr` applies the same ratio but uses incremental assessments.

**Worked example (base, mapper subscriptions, federal civilian + health, FY3).**

- Federal civ+health mapper wins are 4.0 / 7.8 / 11.4 (≈23 in total).
- New federal subscriptions are 0.3 / 1.2 / 4.5. FY3 includes the deferred SaaS-only cohort that starts at month 30.
- Each is billed at $250K/yr × 1.03², prorated monthly, with 10% churn.
- Result: **$0.94M** of the $1.30M FY3 mapper subscription line. The remainder comes from DoD, states and the UK.

### Prices used ($K)

The only price changes from round 1 are the federal mapper subscription and the data-generator pack. Other unchanged prices (mapper and harness implementation, state/UK harness) are in `01_revenue_modeler.md`.

| | FC / FH | DoD | SL | UK |
|---|---|---|---|---|
| Mapper assessment | 250 | 250 | 150 | 180 |
| **Mapper subscription (R8)** | **250** | **250** | 150 | 200 |
| Harness assessment | 175 | 225 | 100 | 140 |
| Harness assurance /yr (R9) | 200 | 250 | 100 | 150 |
| **DG custom pack (R4)** | 100 | 100 | 100 | 100 |
| **County package / update (R11)** | — | — | 40 / 20 per yr | — |

### Scenario levers

| Lever | Downside | Upside |
|---|---|---|
| Opportunities | ×0.6 | ×1.3 |
| Win rate | −5 pts (state/local therefore 20%) | +5 pts |
| Sales cycle | +3 mo | −2 mo |
| Price | ×0.8 | ×1.1 |
| Assessment → subscription | 24% | 44% |
| Harness attach | 20% | 50% |
| Harness renewal (R2) | 50% | 75% |
| Mapper churn | 20% | 5% |
| FedRAMP | Never in window, so no federal SaaS subscriptions | FY2 month 2, so federal SaaS from FY3 month 2 |
| Managed-service start | Month 12 | Month 9 |
| County deals | 0 / 2 / 5 | 2 / 8 / 16 |
| Non-incremental share | 50% | 30% |
| Upside-only lines | — | Portfolio tier, royalty, IP |

---

## 6. Changes vs. round 1

The waterfall applies rulings one at a time, cumulatively, to 3-yr core GROSS revenue in base.

| Step / ruling | 3-yr core after step | Δ $M | Why |
|---|---|---|---|
| Round-1 base (annual model) | 23.84 | — | Round-1 output |
| Model rebuilt monthly, round-1 inputs | 24.56 | +0.72 | Monthly timing replaces the annual half-year approximation for implementations. This is structure, not a ruling. |
| **R4** DG: packs only at $100K; license and implementation dropped; royalty moved to upside | 24.17 | −0.39 | Data-generator revenue goes from $2.0M to $1.3M |
| **R7** Hardening: assessments from month 3, managed service from month 9 | 24.16 | −0.01 | Wins shift by weeks within FY1. Subscriptions slip a few months, a small 3-yr effect. Deals that would have closed before month 1 were already excluded. |
| **R1** 35% assessment→subscription; federal SaaS ≥12 months after authorization (FY3 month 6) | 23.55 | −0.61 | Subscription revenue −$0.6M |
| **R8** Federal mapper subscription $300K → $250K | 23.31 | −0.24 | Price on a small recurring base |
| **R2** Harness renewal 85% → 60% | 23.08 | −0.23 | Small 3-yr impact. Much larger on FY4+ value. |
| **R3** Conflict of interest: −40% of harness opportunities in integrator accounts | 22.00 | **−1.08** | Largest single ruling. It hits federal health hardest. |
| **R12** State win rate −5 pts | 21.45 | −0.55 | TMF and SLCGP funding has lapsed |
| **R11** Counties removed from direct state/local sales; channel line added | 21.29 | −0.15 | −$0.8M from direct state/local, +$0.67M from the county channel |
| **R5** IP analytics to upside only | (core unchanged) | −2.50 vs. round-1 core+IP | Removed from base entirely |
| **R6** Report incremental | **17.09 incremental** | −4.20 | 40% of assessment revenue netted out |
| **R9** Portfolio tier | upside only | +2.56 (upside) | Three contracts at $0.9M/yr |
| **R10** Vehicles: CIO-SP4 dropped; GSA MAS / OASIS+ / CDAO T&E BPA / NASPO / TS4 Lots 1 and 5 | no Δ | 0 | Sales cycles assumed to run on these vehicles. **Risk flag:** if Guidehouse is not a CDAO T&E BPA holder (unverified per 03), DoD harness revenue ($1.0M of the $1.53M DoD total) is at risk. |
| **R13** | n/a | — | cost_and_margin_analyst re-plugs this revenue |

---

## 7. Notes for downstream teammates

1. **For cost_and_margin_analyst (R13).**
   - Use base GROSS $2.31M / $6.67M / $12.32M for delivery cost.
   - Use INCREMENTAL $1.73M / $5.28M / $10.09M for program payback.
   - About 87% of base revenue is labor-delivered (assessments, implementations, packs).
   - **County channel CAC (R11):** if the ~$50K is per deal, the county line is margin-negative ($40K package). It only works if $50K is per channel cohort or per year. Please confirm which interpretation you used.
   - Federal SaaS hosting cost begins in FY3 month 6 in base. Downside needs **no FedRAMP spend in the window**.
2. **Churn is a FY4+ problem.** Harness renewal at 60% means about 40% of assurance logos must be replaced each year. Beyond FY3, the harness behaves like an episodic service, which matches the buyer's view.
3. **The biggest remaining unverified inputs** are pipeline volume (about 36 mapper wins in base), the integrator-share percentages behind R3, and the 0.5× pull-through ratio. All three are ESTIMATE.
4. **IP upside is contingent.** It assumes a real-data task order under existing CMS contracts in FY1 (one pilot), with production starting in FY2. The buyer gave ≤10% likelihood for a synthetic-only product and 25% as an accelerator inside a real-data pursuit, so upside IP should be read as a low-probability tail.
