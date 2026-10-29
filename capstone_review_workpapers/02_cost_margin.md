# 02 — Cost & Margin Analysis (cost_and_margin_analyst)

Scope: the synthetic data generator (SDG), the policy-to-AI-governance mapper (GOV), the agentic red-team harness (RTH), the optional improper-payment analytics (IPA), and the program as a whole.
Horizon: 5 years starting at capstone kickoff (Y1 = academic year 2027).
Model: Python, deterministic. Reproducible at `/tmp/claude-0/-home-user-Learning-env/597ac1d9-a808-55f6-8cf9-a6a3d19428fc/scratchpad/cm/model2.py`.
Labels: **[SRC]** means verified against a cited source. **ESTIMATE** means my assumption.

---

## 0. Global assumptions

| Parameter | Value | Basis |
|---|---|---|
| Loaded internal cost, engineer/data scientist | **$150/hr**. That is $24,000 per FTE-month (160 hrs) and $288,000 per FTE-year (1,920 hrs). | ESTIMATE: ~$155k salary × 1.35 fringe, plus overhead. This is a *cost*, not a bill rate. For reference, GSA price lists show a Data Scientist at $163.89/hr and a Senior Data Scientist at $235.77/hr as ceiling *bill* rates (2021 vendor schedule) [SRC](https://www.gsaadvantage.gov/ref_text/GS10F0354T/0WD65Y.3S3J4P_GS-10F-0354T_GS10F0354TJUNE222021GS10F0354TSAPERETEXTFILE.DOC) |
| Loaded cost, product owner / compliance SME | $175/hr | ESTIMATE |
| Loaded cost, legal/contracts and BD director | $200–250/hr | ESTIMATE |
| Customer life (for amortizing CAC) | 3 years | ESTIMATE |
| Churn | 10%/yr, with replacements costing full CAC | ESTIMATE |
| Program marketing and partner enablement (Vant4ge, TS4) | $150k/yr | ESTIMATE |

---

## 1. Sponsorship cost (per capstone)

**Fee benchmarks [SRC]:**
- MSU CSE charges $5,000 per project ([link](https://capstone.cse.msu.edu/2023-01/projects/sponsorship/)).
- UCSB CS asks for a $5,000 gift ([link](https://www.corporaterelations.ucsb.edu/department-computer-science-capstone-program)).
- BYU CS charges $5,000 and the sponsor keeps the IP ([link](https://cs.byu.edu/community/companies/sponsor-capstone)).
- CU Boulder CS offers a $7,000 donation option, or **$15,000 if the sponsor retains the IP** ([link](https://www.colorado.edu/cs/engage/sponsor-computer-science-capstone)).
- UT Dallas UTDesign charges $10,000 for one semester and **$15,000 for two semesters** ([link](https://utdesign.utdallas.edu/?p=23934)).
- UGA charges $5,000–$25,000 depending on tier ([link](https://engineering.uga.edu/?p=3497)).

Our program rules require IP assignment and a two-semester build, so I use **$15k per project**.

| Line item | Hours × rate | $ per capstone |
|---|---|---|
| University fee (IP assigned, 2 semesters) | — | 15,000 [SRC range] |
| Cloud credits / synthetic sandbox | — | 5,000 ESTIMATE |
| AI CoE product owner: 0.25 FTE × ~9 months | 360 h × $175 | 63,000 ESTIMATE |
| Technical mentors: 2 × 4 h/week × 30 weeks | 240 h × $150 | 36,000 ESTIMATE |
| Compliance, 508 and security SME reviews (graded deliverables) | 60 h × $175 | 10,500 ESTIMATE |
| Legal: IP and no-real-data agreement | 40 h × $250 | 10,000 ESTIMATE |
| **Total per capstone** | | **$139,500** |

- **Program total:** $418.5k for 3 capstones, or $558k with IPA.
- The **university fee is only about 11% of sponsorship cost**. Internal mentor time is about 78%. If the CoE does not budget the product-owner time, this budget is wrong.

**What the capstone actually delivers (ESTIMATE):**
- A team of 4–5 students working ~8 h/week for 30 weeks puts in about 1,100 hours.
- At roughly 35% of professional productivity, that equals about 2.5 professional FTE-months of prototype work.
- **I assume 30% of capstone code survives into the product.** The rest is rewritten for security, multi-tenancy and testability.
- The capstone's real value is validated requirements, UX, the eval set and the data schemas, not production code.

---

## 2. Post-capstone hardening (one-time)

FTE-months are priced at $24k each. External costs are third-party spend.

| Workstream | SDG | GOV | RTH | IPA | Notes |
|---|---|---|---|---|---|
| Rewrite/refactor (assumes 30% of code survives) | 6 | 10 | 10 | 6 | ESTIMATE |
| Security engineering (threat model, SAST/DAST, SBOM, pen test fixes) | 2 | 6 | 5 | 3 | RTH runs adversarial payloads, so it needs a sandbox. IPA is PHI-adjacent once real claims arrive. |
| Section 508 remediation | 1 | 3 | 2 | 2 | SDG is mostly API/CLI. GOV is UI-heavy (gap-analysis editor, reports). |
| Productization (multi-tenancy, logging/audit, RBAC, SSO via PIV/CAC and Entra/Okta) | 4 | 8 | 6 | 4 | ESTIMATE |
| LLM evaluation and content curation (golden sets, corpora, crosswalks) | 4 | 8 | 10 | 6 | GOV builds the NIST 800-53 r5, CJIS, HIPAA, StateRAMP and OMB AI memo corpora plus crosswalks. RTH builds attack, bias and privacy test libraries. IPA does model validation. |
| ATO internal effort (SSP, policies, evidence automation) | 2 | 12 | 6 | 4 | SDG and IPA deploy inside the client's or Guidehouse's existing boundary. GOV takes the FedRAMP 20x Moderate + GovRAMP path. RTH shares the GOV boundary as an incremental scope. |
| **FTE-months** | **19** | **47** | **39** | **25** | **Program: 130 FTE-months (~10.8 FTE-years)** |
| Internal labor $ | 456k | 1,128k | 936k | 600k | |
| 508 audit + VPAT/ACR (external) | 10k | 25k | 15k | 15k | Audits run $1.25k–$25k+ depending on complexity ([accessible.org](https://accessible.org/pricing/), [ADA Compliance Pros](https://www.adacompliancepros.com/blog/accessibility-audit-cost)). The 508-edition ACR is ~$550 ([accessible.org](https://accessible.org/cost-vpat/)). Multi-role apps are budgeted at the high end, plus re-test. |
| FedRAMP readiness/advisory | — | 150k | — | — | Gap assessment ~$50–150k ([cipherssecurity](https://cipherssecurity.com/?p=14585)). Quzara lists $50–75k readiness and $160–190k documentation ([Quzara PDF](https://cdn.govexec.com/media/quzara_fedramp_pricing.pdf)). |
| 3PAO initial assessment (Moderate) | — | 250k | 100k (incremental scope) | — | Knox puts it at $125–300k ([link](https://knoxsystems.com/resources/fedramp-cost)). Pivot Point puts it at $200–250k ([link](https://www.pivotpointsecurity.com/time-and-cost-factors-to-attain-a-fedramp-ato/)). |
| GovRAMP fees, compliance tooling | — | 80k | 60k | — | The GovRAMP Progressing Snapshot costs $9.5k/yr ([GovRAMP](https://govramp.org/pricing-overview)). The rest is ESTIMATE. |
| **Total hardening $** | **$466k** | **$1,633k** | **$1,111k** | **$615k** | **Program: $3.83M** |
| **Upfront investment I (sponsorship + hardening)** | **$606k** | **$1,773k** | **$1,251k** | **$755k** | **Program: $4.38M** |

**Cross-check against benchmarks [SRC]:**
- Total initial Moderate authorization is quoted at $250–750k ([Secureframe](https://secureframe.com/hub/fedramp/costs.md)) and $400–900k, with ~$650k typical ([Precision Federal](https://precision-federal.pages.dev/insights/fedramp-li-saas-path-for-startups)).
- 20x Moderate Year 1 is quoted at $350–800k ([Secureframe](https://secureframe.com/hub/fedramp/costs.md)).
- My GOV ATO line is $288k internal + $480k external = **$768k**, which sits at the top of the 20x range. That is conservative and deliberate.

**ATO timing:**
- 20x Phase 3 (wide adoption of Low and Moderate) is targeted for FY26 Q3–Q4 but has slipped ([fedramp.gov/20x/phases](https://fedramp.gov/20x/phases/)).
- With hardening running 6–9 months after the capstone ends in May 2027, the earliest realistic **federal SaaS authorization is mid/late 2028 (ESTIMATE)**.
- Until then, GOV and RTH must be sold either as Guidehouse-operated services or deployed inside an agency's own Azure Government or GovCloud tenant under that agency's ATO. Agency-ATO support is ~$100–200k of effort per client (ESTIMATE). This dependency is for revenue_modeler.

---

## 3. Annual run cost: hosting, inference, support, corpus

**Hosting:**
- The GovCloud premium over commercial is 10–30%. EC2 is ~13%, RDS ~21%, and egress is higher ([atonementlicensing](https://atonementlicensing.com/blog/aws-govcloud-pricing/), [alphabravo](https://blog.alphabravo.io/aws-govcloud-vs-commercial-aws-understanding-the-capabilities-and-differences/)).
- Claude Sonnet 4.5 is available on Bedrock in GovCloud with reserved tier ([AWS](https://aws.amazon.com/about-aws/whats-new/2026/01/amazon-bedrock-reserved-tier-for-claude-sonnet-in-govcloud)).
- I price inference at commercial list +20% (ESTIMATE): about $3.6 per million input tokens and $18 per million output tokens for a Sonnet-class model ([Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)).

**Per-tenant inference (ESTIMATE):**
- **GOV:** 2,000 queries/month × (30k input + 2k output tokens) = 60M input + 4M output tokens per month. At the rates above that is ≈ $290/month, or **~$3.5k/yr**. Corpus re-embedding adds ~$1k/yr.
- **RTH:** quarterly campaigns of ~5k multi-turn attack episodes plus LLM-judge scoring come to ~1.5B tokens/yr, or **~$8–10k/yr per client**.
- **Inference is not the cost problem.** Labor is.

| Annual fixed run cost (F) | SDG | GOV | RTH | IPA |
|---|---|---|---|---|
| Corpus / content currency (FTE) | 0.25 (schemas) | 0.75 (control frameworks, OMB/NIST updates, crosswalk QA) | **1.0** (new jailbreaks, agent-attack taxonomies, bias suites) | 0.5 (model refresh, CMS rule changes) |
| Product management (FTE) | 0.25 | 0.5 | 0.5 | 0.25 |
| SRE / platform support (FTE) | 0.25 | 0.75 | 0.5 | 0.25 |
| ConMon: 1 FTE + annual 3PAO $100k + tooling $60k = $448k, split 60% GOV / 40% RTH | — | 269k | 179k | — |
| Base hosting (prod + stage + DR, GovCloud/Azure Gov) | 24k | 96k | 60k | 36k |
| **F ($/yr)** | **$240k** | **$941k** | **$815k** | **$324k** |

- Annual 3PAO assessments run $75–125k ([Knox](https://knoxsystems.com/resources/fedramp-cost)). ConMon runs 15–25% of initial authorization cost per year ([Precision Federal](https://precision-federal.pages.dev/insights/fedramp-li-saas-path-for-startups)). My $448k shared ConMon figure is ≈ 58% of the $768k ATO cost, which is above that benchmark because it includes the ISSO FTE.

**Variable delivery cost per client (v, ESTIMATE):**

| | Reference ACV (A) | Variable cost (v) | What v contains | Unit gross margin |
|---|---|---|---|---|
| SDG license | $75k | $20k | 0.05 FTE support + hosting | **73%** |
| GOV managed subscription | $250k | $135k | 0.4 FTE analyst ($115k) + tenant hosting/inference $10k + tier-2 support $10k | **46%** |
| RTH assurance service | $200k | $118k | 0.35 FTE red-teamer ($100k) + inference $10k + hosting $8k | **41%** |
| IPA engagement | $500k | $318k | 1.0 FTE data scientist ($288k) + hosting $30k | **36%** |

GOV assessment (one-time, $150k):
- With the tool, the assessment takes ~450 h × $150 = $68k, a **55% margin**.
- Without the tool it takes ~720 h, a 28% margin.
- **The tool's clearest economic value is ~27 points of assessment margin.**

---

## 4. Sales cost / CAC by segment (ESTIMATE, benchmarked)

**Benchmark [SRC]:** B&P typically costs 1–3% of contract value, with small contracts costing proportionally more ([Frazier & Deeter](https://frazierdeeter.com/insights/article/understanding-bid-and-proposal-costs-in-government-contracting/), [Wikipedia](https://en.wikipedia.org/wiki/Government_contract_proposal)). Our deals are $150–500k, so the percentage is far higher. I therefore build CAC bottom-up.

| Segment | Pursuit labor | Cost per pursuit | Win rate | **CAC per won client** |
|---|---|---|---|---|
| Federal civilian, new logo (competitive task order) | BD 120h@$200 + solution architect 160h@$175 + proposal 200h@$125 + orals 40h@$200 | $85k | 30% | **$283k** |
| Federal, expansion on existing vehicle (health practice, managed services) | BD 60h + SA 80h + light proposal | $30k | 60% | **$50k** |
| State/local, new RFP or cooperative contract | | $45k | 25% | **$180k** |
| State/local via Vant4ge channel | co-sell | $20k | 40% | **$50k** |
| UK TS4 call-off | | $40k | 30% | **$133k** |
| **Blended (50% expansion, 30% federal new, 20% SLG new)** | | | | **≈ $146k → modeled at $150k** |

- Modeled CAC is SDG $60k (mostly attach), GOV and RTH $150k, IPA $100k (internal practice).
- At $150k CAC against $115k/yr unit contribution, **GOV's CAC payback is 15.7 months**. RTH's is 22 months ($150k / $82k).

---

## 5. Margin & payback

### 5.1 Formulas
- Unit contribution: u = A − v. Unit gross margin: g = u/A.
- Annual contribution in year t: CMₜ = Nₜ·u − F − newₜ·CAC, where newₜ = (Nₜ − Nₜ₋₁) + 0.10·Nₜ₋₁.
- **Clients needed to cover run cost:** N_run = F / u = F / (A·g).
- **Clients needed to repay upfront I over T years at steady state:** N_T = (F + I/T) / (u − CAC/L).
- Payback year: the first t where −I + Σ CMₜ ≥ 0.

### 5.2 Reference client counts (MINE, for revenue_modeler to replace)

| Product | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| SDG (external licenses) | 2 | 5 | 8 | 10 | 12 |
| GOV subscriptions | 3 | 8 | 15 | 22 | 28 |
| RTH assurance clients | 2 | 6 | 12 | 16 | 20 |
| IPA engagements | 0 | 1 | 2 | 3 | 3 |

### 5.3 Results: scenario A, standalone (as currently scoped)

| | I | F/yr | GM | N_run | N_3yr payback | Y3 revenue | Y3 CM | Cum. CM at Y5 | Payback |
|---|---|---|---|---|---|---|---|---|---|
| SDG | $0.61M | $0.24M | 73% | 4.4 | 12.6 | $0.60M | +$0.02M | −$0.61M | >5 yr |
| GOV | $1.77M | $0.94M | 46% | 8.2 | 23.6 | $3.75M | −$0.42M | −$2.69M | ~yr 7 |
| RTH | $1.25M | $0.82M | 41% | 9.9 | 38.5 | $2.40M | −$0.88M | **−$4.33M** | never at these assumptions |
| IPA | $0.75M | $0.32M | 36% | 1.8 | 3.9 | $1.00M | −$0.06M | −$1.04M | ~yr 9 |
| **Program** | **$4.38M** | | 45% | | | **$7.75M** | **−$1.49M (−19%)** | **−$9.42M** | **>5 yr** |

### 5.4 Scenario B, lean/shared platform
Changes from scenario A:
- SDG stays an internal enabler only (no external sales, $296k upfront).
- GOV and RTH share one authorization boundary, SRE and PM.
- RTH is sold as an attach (CAC $90k). GOV CAC is $120k via existing vehicles and Vant4ge.

Results:
- Program upfront I falls to **$3.78M**.
- Year 5 cumulative is **−$6.08M**. Y5 CM is +$1.74M (14%).
- There is **still no payback in 5 years.**

### 5.5 Scenario C, lean plus productized delivery
Delivery labor is automated down: GOV v = 30% of ACV, RTH v = 35%. That means roughly 0.2 FTE per GOV client, not 0.4.
- GOV GM is 70%. **Payback in year 5**, with cumulative +$2.86M at Y5.
- RTH GM is 65%. **Payback in year 5** (+$0.81M).
- **Program: GM 64%, Y3 CM +$0.69M (10%), Y5 CM +$4.38M (35%), payback in year 5 (cumulative +$1.17M).**

### 5.6 Break-even lookup for re-plugging revenue (GOV; F = $941k, I = $1.77M, CAC = $150k)

| GOV ACV | N_run at g = 46% | N_3yr payback | N_run at g = 70% |
|---|---|---|---|
| $150k | 13.6 | 80.6 | 9.0 |
| $200k | 10.2 | 36.5 | 6.7 |
| $250k | 8.2 | 23.6 | 5.4 |
| $350k | 5.8 | 13.8 | 3.8 |
| $500k | 4.1 | 8.5 | 2.7 |

RTH, with F = $815k:
- At g = 41%: N_run is 13.3 at $150k, 9.9 at $200k, 6.6 at $300k and 5.0 at $400k.
- At g = 65% and F = $671k (shared platform): N_run is 5.2 at $200k.

**Rule of thumb for the lead partner:** the program needs about **$9–10M of recurring revenue at 45% GM** (or about $6.5M at 64% GM) just to cover the ~$2.5M of fixed run cost plus about $1.5M/yr of CAC.

### 5.7 Upside not modeled
- **Consulting pull-through.** Gap analyses lead to remediation work. Each GOV client generating $300k/yr of follow-on work at 30% CM would add $90k of contribution per client per year. That alone would cut GOV's N_run from 8.2 to 4.6. This is the strongest economic argument for the program, and revenue_modeler should quantify it.
- **Internal value of SDG.** It avoids demo-data creation on pursuits. At ~80 h per pursuit × 40 pursuits/yr × $150, that is about $480k/yr (ESTIMATE). That would justify SDG as an internal tool without any external sales.

---

## 6. Cost-sink flag

**Most likely cost sink: the red-team harness (RTH).**
1. It has the **highest fixed run cost relative to unit economics**: N_run = 9.9 clients at $200k ACV, against 8.2 for GOV and 1.8 for IPA.
2. It needs **1.0 FTE ($288k/yr) of content currency that never amortizes.** Agent attack techniques, jailbreaks and bias benchmarks go stale in months, unlike control frameworks, which revise on a cycle of years. Without that FTE the harness loses credibility fast.
3. Its unit gross margin is **41%, the lowest of the subscription products.** Assurance needs expert red-teamers in the loop, and that labor is hard to automate without lowering assurance quality.
4. It is the only product with a **negative cumulative contribution that is still worsening at Y5** in scenario A (−$4.33M). It reaches 22 clients and ~$4M of revenue in Y5 and still does not cover F + CAC.
5. Its capstone deliverable is likely the least reusable (the 30% survival assumption is probably optimistic here). Agentic tooling is still unsettled, and adversarial code needs a security rebuild.

**Mitigation:**
- Run RTH as an attach module on the GOV platform and authorization boundary (scenario B). That saves about $296k of upfront cost and $144k/yr of fixed cost.
- Price it at ≥$300k ACV, or as per-system assessments of $75–100k each.
- License third-party attack libraries rather than curating them all in-house.

**Watch item: GOV's ATO is the largest single cash outlay ($768k) and adds ~$270k/yr of ConMon.**
- Starting FedRAMP before 5 or more committed federal SaaS buyers exist would turn GOV into a sink.
- Gate the 3PAO spend on signed demand. Until then, sell through agency-tenant deployments and GovRAMP.

---

## 7. Dependencies and likely contests
- **revenue_modeler:** my client counts and ACVs are placeholders. Re-plug them into §5.6. Two things I expect to be contested: my federal SaaS timing (no FedRAMP-authorized sales before mid/late 2028), and my $150k blended CAC (higher than a "warm accounts" assumption would give).
- **market_and_competition_analyst:** whether GOV can command $250k/yr against GRC incumbents (e.g., ServiceNow IRM, Archer, Drata/Vanta federal offerings). If market ACV is ≤$150k, GOV needs ≥13.6 clients just to cover run cost.
- **public_sector_buyer:** whether agencies will accept agency-tenant deployment pre-FedRAMP, and whether a red-team service from a firm that also builds their AI raises an independence objection (it would cut RTH's win rate).
- **Contestable assumptions:** the 30% code-survival rate, the $150/hr loaded cost, 0.4 FTE of delivery per GOV client, and the 10% churn rate.
