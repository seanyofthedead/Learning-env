# 08 — Growth Strategist: 19 changes to raise revenue / value returned

As of 2026-10-29. Inputs are 01–04 and the lead partner's rulings in 05. **ESTIMATE** marks anything without a URL. $ figures are USD and cover 3 years (FY1–FY3, with FY1 starting at the first cohort's delivery).

## 0. Baseline I am improving on (dependency: revenue_modeler rerun)

revenue_modeler is still rerunning under R1–R13, so I use a **working baseline (ESTIMATE): about $17M gross and $12–13M incremental core revenue over 3 years.**

How I got there:
- Start from the pre-ruling core of $23.8M.
- Mapper subscriptions drop from about $2.7M to about $1.0M (R1, R7, R8).
- Harness falls from about $5.6M to about $3.0M (R2 at 60% renewal, R3 removing 40% of conflicted opportunities).
- Data generator falls from $2.0M to about $1.3M (packs only, R4).
- State/local loses about $0.5M (R12).
- Netting out 40% of assessment revenue (R6) gives the incremental figure.

Every impact below is **incremental to that baseline**. Impacts are tagged **[REV]** (new revenue) or **[VAL]** (cost avoided or margin gained). Where an idea changes a modeled lever (win rate, cycle, attach), I scale from revenue_modeler's sensitivities: −5 pts win = −$3.8M, +3 mo cycle = −$3.5M on $23.8M. I multiply those by about 0.7 to reflect the smaller reconciled base.

**Weights:** revenue 40%, cost 20%, time 20%, risk 20%, as briefed. I kept them because the program's problem is that it may *never pay back* (cost analyst: −$9.4M cumulative at Y5 in scenario A), so cost and risk deserve real weight. As a check I re-ranked at 50/10/20/20. The top 5 did not change, and positions 6–8 only reordered (§3).

Scales: 1–5 on each axis. For Cost, 5 = cheap. For Time, 5 = fast. For Risk, 5 = low risk. Revenue impact is scored on revenue *or* value returned, so [VAL] ideas can score.

---

## 1. The ideas

### A. Pricing and packaging

**#2 Per-system and portfolio-tier pricing for the harness (and per-use-case impact assessments on the mapper)** [REV]
- **Change:** Replace the "$200K/yr recurring assurance" headline with three SKUs:
  - A **$75–150K pre-deployment assurance sprint per high-impact system**, re-bought on each major model or prompt change.
  - A **$0.6–1.2M/yr portfolio tier** for agencies with 8 or more high-impact systems.
  - A **$25–40K per-use-case M-25-21 impact-assessment** add-on on the mapper.
- **Why:** Buyers call testing episodic (04 §5.2). Per-event pricing captures the episodes instead of fighting them. It also sets a price floor of at least $100K per system, which the cost analyst says is needed to escape the harness cost sink (02 §6).
- **Market size:** 445 federal high-impact use cases; VA alone has 215 ([Nextgov](https://www.nextgov.com/artificial-intelligence/2026/04/agencies-report-over-3000-ai-use-cases-2025/412898/)).
- **3-yr impact, about +$2.0M.** Assumption: 8/15/20 systems in FY1–FY3 at $100K, plus one portfolio tier at $0.8M in FY3, comes to about $5.1M gross. That cannibalizes roughly $3.1M of the existing harness assessment and assurance lines.
- **Cost:** about $50K for pricing, contract templates and the evidence-pack format.
- **Owner:** AI CoE product owner, with a pricing desk.
- **Scores:** R4 C5 T5 Risk3. The risk is that per-system pricing invites unit-price comparison with $30–50K commercial red-teams.

**#3 Price assessments as ≤$350K firm-fixed-price SKUs and re-plan vehicles after CIO-SP4** [REV]
- **Change:**
  - Cap every federal assessment SKU at ≤$350K so it qualifies for simplified acquisition. The SAT rose to $350K on 1 Oct 2025 ([Federal Register](https://www.govinfo.gov/content/pkg/FR-2025-08-27/html/2025-16412.htm)).
  - Load the SKUs on GSA MAS: 541611 for governance, 54151S for IT services, and 54151HACS for the red-team framing.
  - Load them on OASIS+ as well. Guidehouse holds 47QRCA25DU150 ([Guidehouse](https://guidehouse.com/government-contract-vehicles/oasis-plus)).
  - On-ramp to the CDAO AI T&E BPA through Tradewinds if Guidehouse is not already a holder (79 holders, [Sweetspot](https://www.sweetspot.so/markets/federal/vehicles/ai-test-and-evaluation/)).
  - Drop CIO-SP4. It was cancelled 30 Jan 2026 ([ExecutiveGov](https://www.executivegov.com/articles/nitaac-cio-sp4-cancellation)).
- **3-yr impact, about +$1.5M.** Assumption: SAT-sized FFP orders on vehicles Guidehouse already holds cut 2–3 months from the 9-month federal civilian cycle. Inverting the modeler's sensitivity (+3 mo = −$3.5M) and scaling by 0.7 gives about +$1.5–2.0M; I use the low end. ESTIMATE.
- **Cost:** about $100K for SIN modifications, a Tradewinds video pitch, and a T&E BPA proposal.
- **Owner:** federal contracts and capture lead.
- **Scores:** R4 C5 T5 Risk4.

**#19 Fee-at-risk / outcome-based SLA on the managed service** [REV]
- **Change:** Put 10–15% of the mapper managed-service fee at risk against measurable outcomes:
  - updated crosswalk within 30 days of a new rule (COSAIS, M-26-xx, GovRAMP);
  - AO or OIG acceptance of the evidence package;
  - for state HHS, Medicaid Enterprise System outcomes-based certification evidence accepted.
- Pure share-in-savings is impractical in federal contracting, so I recommend this hybrid, not contingency pricing.
- **3-yr impact, about +$0.5M.** Assumption: +3 pts subscription conversion and +5 pts renewal, applied to the about $1.0M reconciled subscription line plus FY3 entrants. ESTIMATE.
- **Cost:** about $50K for contracts, metric instrumentation and legal.
- **Owner:** AI CoE product owner and contracts.
- **Scores:** R2 C4 T4 Risk2. It only works once delivery is productized (#17). Otherwise Guidehouse puts fees at risk on labor it can't control.

### B. Bundling and scope

**#4 Make the AI Readiness Maturity Model the paid front door: "Readiness → Inventory → Controls → Evidence" in one SKU** [REV]
- **Change:**
  - Fold a mapper-generated OMB-format inventory and gap analysis into the Maturity Model, sold as a $150–300K FFP under the SAT.
  - Make the annual Maturity *re-score* a contractual component of the mapper managed service, which gives the subscription a visible annual deliverable.
- **Why:** No single competitor offers the whole evidence chain (03 §7.3). Booz Allen and Credo cover only the inventory piece.
- **3-yr impact, about +$2.5M.** Assumption: +5 pts mapper win rate (about +$2.0M after scaling the modeler's −5 pt sensitivity), plus assessment→subscription conversion rising from 35% to 42% (about +$0.5M).
- **Caveat:** Part of this is Maturity Model revenue Guidehouse would book anyway. Report it net of R6.
- **Cost:** about $200K for integration, re-branding and sales enablement for about 40 account leads.
- **Owner:** AI CoE product owner, with the Maturity Model offering lead.
- **Scores:** R4 C4 T4 Risk4.

**#16 New scope: an OMB M-25-22 pre-award vendor-AI evaluation service** [REV]
- **Change:** Sell the harness to *contracting officers and CAIOs* to test vendors' AI in source selection and before award. M-25-22 requires agencies to check AI they buy ([PilieroMazza](https://www.pilieromazza.com/omb-issues-memoranda-on-use-and-acquisition-of-ai-by-federal-agencies-part-1-what-it-means-for-government-contractors/)).
- **Why:** Guidehouse is the evaluator here, not the builder, so the R3 conflict of interest does not arise as long as Guidehouse does not bid on the same procurement. That is the FAR 9.505-3 evaluation-services rule, which is a real trade-off.
- **3-yr impact, about +$1.3M.** Assumption: 3/4/6 evaluations at about $100K each. Nearly all of it is incremental because the buyer is new. ESTIMATE.
- **Cost:** about $75K for the evaluation protocol and source-selection-sensitive handling procedures.
- **Owner:** federal AI CoE / acquisition advisory lead.
- **Scores:** R3 C5 T4 Risk3.

**#18 Scope cut: drop improper-payment analytics as a product and keep it as a proposal and demo sandbox only** [VAL]
- **Change:** Do not spend the about $615K of improper-payment hardening (02 §2). Point the synthetic-claims sandbox at program-integrity pursuits instead: FPS 2.0, CERT, and state Medicaid PI recompetes. Guidehouse already holds CMS FEIPM/SEIPM, $63.9M ([OrangeSlices](https://orangeslices.ai/guidehouse-secures-64m-cms-federal-and-state-exchange-improper-payment-measurement-rc-support-contract/)).
- **3-yr value, about +$1.1M.** Assumption: about $0.6M of avoided hardening, plus +3 pts win probability on about $40M of program-integrity pursuit TCV, with about 40% of that revenue landing in the window (about $0.5M). ESTIMATE.
- **Cost:** about $25K.
- **Owner:** federal health practice lead.
- **Scores:** R2 C5 T4 Risk4. It is consistent with R5.

**#17 Internal-first: run the mapper as the delivery engine on existing *firm-fixed-price* ATO/GRC/governance work** [VAL]
- **Change:** Before selling the mapper, deploy it inside Guidehouse's own FFP assessment and ATO-support delivery.
- **Why:** The cost analyst found the tool cuts a governance assessment from about 720 hours to about 450 and lifts margin from 28% to 55% (02 §3). That is the most certain value in the program.
- **Caveat:** Apply it to FFP only. On T&M contracts, efficiency *reduces* revenue.
- **3-yr value, about +$1.8M margin.** Assumption: about $8M/yr of addressable FFP governance and ATO labor (ESTIMATE; the managed services lead should verify), with realized hours savings of 2.5% / 7.5% / 12.5% of that base as adoption ramps.
- **Cost:** about $100K for internal rollout and training.
- **Owner:** managed services lead.
- **Scores:** R3 C5 T5 Risk4.

### C. Conflict of interest and the harness cost sink

**#1 Independence firewall plus a dual harness SKU** [REV]
- **Two SKUs:**
  - **(a) "Build-time AI QA."** Developer-side testing on systems Guidehouse or Vant4ge build. It is labelled as developer testing, not independent assurance. This lets Guidehouse attach the harness to its own builds without a conflict-of-interest problem.
  - **(b) "Independent AI Assurance."** A firewalled unit with separate staff and a separate reporting line. It never tests a system that Guidehouse builds or integrates, and it files a FAR 9.5 OCI mitigation plan.
- **Variant:** a third-party co-signer, such as a university AI assurance lab or a 3PAO, signs the attestation while Guidehouse runs the harness. That is more credible to an OIG but splits the margin by about 20–30% (ESTIMATE).
- **3-yr impact, about +$1.4M.** Assumption: about $2.0M of harness revenue is removed under R3. The firewall or co-signer recovers half (about $1.0M). The build-time QA line attached to Guidehouse and Vant4ge builds adds about $0.4M (20 builds × $20K).
- **Cost:** about $150K setup for legal, OCI plans and org design, plus about $50K/yr.
- **Owner:** AI CoE product owner, with General Counsel/contracts.
- **Scores:** R3 C4 T4 Risk3.

**#12 Open-source the harness core as Inspect plugins; keep mission suites and evidence mapping proprietary** [VAL]
- **Change:**
  - Build the harness on UK AISI's Inspect (MIT licence; [GitHub](https://github.com/UKGovernmentBEIS/inspect_ai)).
  - Publish the core.
  - Keep proprietary the benefits, Medicaid and corrections agent suites and the mapping of each finding to an M-25-21 practice and an ATO control.
  - License third-party attack libraries instead of curating everything in-house.
- **Why:** It attacks the 1.0 FTE/yr of content currency that never amortizes (02 §6). It also lets agencies specify the harness in RFPs and aligns it with GSA USAi and CAISI rather than competing with them.
- **3-yr value, about +$0.9M.** Assumption:
  - about 0.4 FTE/yr of content work avoided ≈ $0.29M;
  - about 4 FTE-months less hardening ≈ $0.1M;
  - about +$0.5M from spec-in and credibility win-rate lift.
  - All ESTIMATE.
- **Cost:** about $120K for an OSPO review, licence check against the university IP assignment, and community maintenance.
- **Owner:** AI CoE harness lead.
- **Scores:** R2 C4 T4 Risk3.

**Harness kill-gate (attached to #1, #2 and #12):** At FY2 month 6, if the harness has fewer than 6 paying clients at ≥$100K per system, or gross margin below 50%, fold it into the mapper as an evidence feature. That stops the −$4.3M Y5 drift in 02 §5.3.

**#5 Demand-gate FedRAMP; deploy in agency tenants until 5 signed federal SaaS LOIs exist** [VAL]
- **Change:** Do not start the 3PAO assessment (about $768K) or ConMon (about $448K/yr shared) until five agencies have signed letters of intent. Until then, deploy in the agency's own Azure Government or GovCloud tenant under its ATO, and pursue GovRAMP Ready for states. A Progressing Snapshot costs $9.5K/yr ([GovRAMP](https://govramp.org/pricing-overview)).
- **3-yr value, about +$1.0M net.** Assumption: about $0.77M of ATO spend avoided plus about 1.5 years of ConMon (about $0.67M), less about $0.4–0.75M of revenue lost to buyers who only accept hosted SaaS (modeler sensitivity: FedRAMP never = −$0.74M; R7 already defers subscriptions).
- **Cost:** $0. It saves money.
- **Owner:** AI CoE product owner, with the CISO.
- **Scores:** R3 C5 T5 Risk4.

### D. Channels and partners

**#8 Vant4ge embedded attach: every Vant4gePoint deployment ships with Guidehouse governance and data** [REV]
- **Attach bundle:**
  - a CJIS 6.0 / HIPAA / IRS 1075 rule-pack assessment (about $100K);
  - a CJIS-safe synthetic sandbox for training and upgrade testing (about $50K, the county director's must-have from 04 §2.1);
  - build-time AI QA (#1a).
- Do **not** sell independent assurance on deployments where Guidehouse integrates. The partnership was announced 7 Apr 2026 ([release](https://lifestyle.q923radio.com/story/157747/vant4ge-partners-with-guidehouse-to-advance-ai-enabled-solutions-for-public-safety-and-human-services-2/)).
- **3-yr impact, about +$1.65M.** Assumption: 4/6/8 Vant4ge public-sector deployments per year with a Guidehouse role, a 50% attach rate at $150K, and 40% taking a $75K/yr update service. The deployment counts are ESTIMATE and unverified.
- **Cost:** about $150K for joint solution packaging and a revenue-share agreement.
- **Owner:** partnerships lead.
- **Scores:** R3 C4 T3 Risk3.

**#7 County channel: a fixed-fee "AI policy + CJIS 6.0 crosswalk" kit sold through state-association master agreements, co-ops and Vant4ge** [REV]
- **Change:** Sell a $25–50K kit, under typical bid thresholds, through one master agreement per state with the county association or a state contract counties can piggyback on, plus Sourcewell or OMNIA through a reseller.
- Delivery must be ≤100 hours, about 80% templated by the mapper.
- **Rule (R11):** per-county CAC has to stay below about $10K. The $50K channel CAC in R11 cannot carry a $35K deal. Kill the county line if CAC exceeds $15K.
- **3-yr impact, about +$0.9M.** Assumption: 3 state master agreements yield 25 counties at $35K (about $0.88M), with about 40% taking a $15K/yr update service from FY2.
- **Cost:** about $120K.
- **Owner:** state and local practice lead.
- **Scores:** R2 C4 T3 Risk3.

**#9 Hyperscaler marketplaces: list on AWS (including GovCloud) and Azure, sell through Consulting Partner Private Offers via Carahsoft, and co-sell with AWS and Microsoft public-sector teams** [REV]
- **Change:** List the mapper as a professional-services or managed listing, deployed into the buyer's tenant. Buyers draw down committed cloud spend through private offers ([AWS CPPO](https://aws.amazon.com/blogs/awsmarketplace/how-to-create-consulting-partner-private-offers); [AWS SLG myth-busting](https://aws.amazon.com/blogs/publicsector/aws-marketplace-myth-busting-for-state-and-local-government-agencies)).
- **Why:** It pairs with #5 because the agency-tenant deployment avoids Guidehouse-hosted FedRAMP. Credo AI already sells this way ([AWS listing](https://aws.amazon.com/marketplace/pp/prodview-x67krdatcdday)).
- **3-yr impact, about +$1.0M.** Assumption: 5 incremental deals at about $200K, net of marketplace fees of about 3% (ESTIMATE).
- **Cost:** about $80K for the listing, co-sell enablement and partner-tier requirements.
- **Owner:** alliances/partnerships lead.
- **Scores:** R3 C4 T4 Risk4.

**#10 License content to other firms: OEM the crosswalk rule packs to GRC platforms and the harness mission suites to mid-tier SIs** [REV]
- **Change:**
  - License the crosswalk rule packs (OSCAL format, covering CJIS, HIPAA, IRS 1075, GovRAMP, COSAIS and M-25-21) to RegScale, Paramify or ServiceNow. Those platforms have no services arm (03 §3.4).
  - License the harness mission suites to mid-tier SIs.
  - Release OEM content on a 6-month lag so the managed service keeps an edge.
- **3-yr impact, about +$0.75M.** Assumption: 2 OEM deals at $200K/yr starting mid-FY2 (about $0.6M), plus 3 SI suite licences at $50K in FY3. It also yields partner-sourced services leads that are not counted.
- **Cost:** about $150K for packaging, legal and IP clearance under the university assignment.
- **Owner:** partnerships lead, with the AI CoE.
- **Scores:** R3 C4 T3 Risk2. The risk is cannibalization and channel conflict.

### E. Open source, funding routes and UK

**#11 Open-source the data generator as a "Public Sector Synthetic Data Commons" (Apache-2.0); monetize calibrated packs and RFP bake-off datasets** [VAL+REV]
- **Change:**
  - Open-source the generator.
  - Sell state-schema "bake-off" caseloads that a state hands to every bidder (04 §2.1), at about $75K each.
  - Keep custom calibrated packs at $50–150K under a client DUA.
- **Why:** Free substitutes already exist (Synthea, NeMo, MOSTLY AI; 03 §2.1), and nobody publishes realistic benefits, court or permit data.
- **3-yr value, about +$1.5M:**
  - 4 bake-off sets ≈ $0.3M [REV];
  - DG run cost cut from $240K to about $120K/yr through community maintenance and scope trimming ≈ $0.3M [VAL];
  - about $0.48M/yr of demo-data creation avoided on pursuits (02 §5.7), ramping over about 2 years ≈ $0.9M [VAL].
- **Cost:** about $100K for an OSPO review, documentation and a re-identification test report.
- **Owner:** AI CoE product owner.
- **Scores:** R2 C5 T5 Risk4. **Dependency:** confirm the IP assignment allows relicensing.

**#6 Medicaid 90/10: package the mapper, harness and data generator as an MES "AI governance and testing" module** [REV]
- **Change:** Sell to state Medicaid agencies, not the CTO, as an allowable DDI cost in the state's APD. That carries a 90% federal match, and certified operations carry 75% ([CMS SMD #22-001](https://www.medicaid.gov/federal-policy-guidance/downloads/smd22001.pdf)).
- **Module contents:**
  - a MARS-E/ARC-AMPE plus IRS 1075 crosswalk;
  - eligibility-agent testing ahead of the 31 Dec 2026 work-requirement start (04 §0);
  - synthetic test data for outcomes-based certification.
- **Why:** It is the only live state funding route under R12. The state pays 10 cents on the dollar, so deals can be about 2–3× the $150K state/local ticket.
- **3-yr impact, about +$2.1M.** Assumption: 1.5 states in FY2 and 2.5 in FY3 at about $450K DDI (about $1.8M), plus about $0.3M of 75%-match operations. First revenue lands only in FY2, because APD approval adds about 2–4 months (ESTIMATE).
- **Cost:** about $250K for the APD template, certification-aligned packaging and the state HHS rule pack.
- **Owner:** state HHS / Medicaid practice lead.
- **Scores:** R4 C3 T2 Risk3.

**#13 UK/TS4 adaptation pack: ATRS record generator, AI Playbook crosswalk, Inspect-based assurance** [REV]
- **Change:**
  - Add a UK rule pack mapping the 10 principles of the AI Playbook for the UK Government ([GOV.UK](https://gov.uk/government/publications/ai-playbook-for-the-uk-government/artificial-intelligence-playbook-for-the-uk-government-html)) together with UK GDPR DPIA and Equality Act public-sector equality duty requirements.
  - Add an **ATRS record generator**. ATRS is mandatory for central departments and public-facing ALBs ([GOV.UK](https://gov.uk/government/publications/algorithmic-transparency-recording-standard-mandatory-scope-and-exemptions-policy/algorithmic-transparency-recording-standard-atrs-mandatory-scope-and-exemptions-policy)), and compliance has historically been weak.
  - Run harness evidence on Inspect (#12), the AISI standard.
  - Sell through TS4 Lot 1 for the ATRS and inventory sprint and Lot 5/5a for the managed service. Lots 1–5a allow direct award ([Find a Tender](https://www.find-tender.service.gov.uk/Notice/001978-2026)).
- **3-yr impact, about +$1.3M.** Assumption: +4 UK sprints beyond base at about $180K (about $0.72M), plus 2 managed services at about $200K/yr for about 1.5 years (about $0.6M).
- **Cost:** about $150K of localization (about 6 FTE-months), plus about $50K of UK pre-sales.
- **Owner:** UK lead.
- **Scores:** R3 C4 T3 Risk3. The risk is the weak UK brand, which keeps the win rate at 25%.

### F. The capstone program itself

**#14 Turn the capstone into a recurring recruiting pipeline** [VAL]
- **Change:**
  - Run an annual cohort with 3–4 teams of about 5 students, so about 18 students a year.
  - Make the hire path explicit: a summer internship bridge, clearance-eligibility screening at team selection, and offers before graduation.
  - Run each year's problems from the product backlog, so the pipeline also keeps generating product features.
- **Quantification (ESTIMATE except benchmarks):**
  - Hire rate is 25% of students, so about 4.5 hires a year. That is deliberately below NACE's 63.1% intern conversion ([NACE](https://naceweb.org/talent-acquisition/internships/intern-offer-and-conversion-rates-fall-acceptances-rise)), because a capstone is a weaker funnel than an internship.
  - Three graduating cohorts inside the window give about 13 hires.
  - Avoided cost per hire is about $22K on an agency fee (20% × an assumed $110K entry AI salary) and about $5.5K internal (the SHRM 2025 non-executive average, $5,475, [SHRM](https://www.shrm.org/topics-tools/research/2025-recruiting-benchmarking)). Blended 50/50 that is about $14K.
  - Faster ramp is worth about $15K per hire: about 1 month of productivity, because hires arrive already knowing the stack.
  - **13 × about $29K ≈ $0.38M**, with a range of $0.25–0.55M. First-year attrition reduction is not counted.
- **Cost:** about $50K/yr of university-relations time, about $150K over 3 years.
- **Owner:** university relations, with talent acquisition.
- **Scores:** R2 C4 T3 Risk4.
- **Note:** This value alone does not cover the $418K sponsorship cost. Recruiting is a co-benefit, not the justification.

**#15 Capstone-as-a-service: run state-sponsored AI studios with in-state universities** [REV]
- **Change:** Offer states a managed program office ($150K/yr) that runs agency AI problems through in-state university teams. The data generator satisfies the no-real-data rule, and Guidehouse hardens what survives.
- **Why:** The state CTO persona called the capstone "a plus with my legislature" (04 §4), and it also feeds #14.
- **3-yr impact, about +$0.75M.** Assumption: 2 studios in FY2 and 3 in FY3 at $150K, before pull-through.
- **Cost:** about $150K for the playbook, university agreements and legal.
- **Owner:** state and local practice lead, with university relations.
- **Scores:** R2 C4 T3 Risk3.

---

## 2. Scored and ranked (weights 40/20/20/20)

| Rank | Idea | Rev | Cost | Time | Risk | **Weighted** | 3-yr $M (mid) | Cost $K | Owner |
|---|---|---|---|---|---|---|---|---|---|
| 1 | #3 SAT-priced SKUs + vehicle re-plan (post CIO-SP4) | 4 | 5 | 5 | 4 | **4.40** | 1.5 REV | 100 | Federal contracts/capture lead |
| 2 | #2 Per-system + portfolio-tier pricing | 4 | 5 | 5 | 3 | **4.20** | 2.0 REV | 50 | AI CoE product owner |
| 3 | #4 Maturity Model front-door bundle | 4 | 4 | 4 | 4 | **4.00** | 2.5 REV | 200 | AI CoE PO + Maturity Model lead |
| 4 | #17 Internal-first mapper on FFP delivery | 3 | 5 | 5 | 4 | **4.00** | 1.8 VAL | 100 | Managed services lead |
| 5 | #5 Demand-gated FedRAMP; agency-tenant deploy | 3 | 5 | 5 | 4 | **4.00** | 1.0 VAL | 0 | AI CoE PO + CISO |
| 6 | #16 M-25-22 pre-award vendor-AI evaluation | 3 | 5 | 4 | 3 | **3.60** | 1.3 REV | 75 | Federal AI CoE / acquisition advisory |
| 7 | #11 Open-source DG + bake-off/calibrated packs | 2 | 5 | 5 | 4 | **3.60** | 1.5 VAL+REV | 100 | AI CoE PO |
| 8 | #9 Hyperscaler marketplaces + co-sell | 3 | 4 | 4 | 4 | **3.60** | 1.0 REV | 80 | Alliances lead |
| 9 | #18 Drop IP analytics product; demo sandbox | 2 | 5 | 4 | 4 | **3.40** | 1.1 VAL | 25 | Federal health practice lead |
| 10 | #1 Independence firewall + dual harness SKU | 3 | 4 | 4 | 3 | **3.40** | 1.4 REV | 200 | AI CoE PO + General Counsel |
| 11 | #6 Medicaid 90/10 MES module | 4 | 3 | 2 | 3 | **3.20** | 2.1 REV | 250 | State HHS/Medicaid practice lead |
| 12 | #8 Vant4ge embedded attach | 3 | 4 | 3 | 3 | **3.20** | 1.65 REV | 150 | Partnerships lead |
| 13 | #13 UK/TS4 ATRS + AI Playbook + Inspect | 3 | 4 | 3 | 3 | **3.20** | 1.3 REV | 200 | UK lead |
| 14 | #12 Open-source harness core on Inspect | 2 | 4 | 4 | 3 | **3.00** | 0.9 VAL | 120 | AI CoE harness lead |
| 15 | #10 Content-OEM licensing to GRC/SIs | 3 | 4 | 3 | 2 | **3.00** | 0.75 REV | 150 | Partnerships lead |
| 16 | #14 Capstone recruiting pipeline | 2 | 4 | 3 | 4 | **3.00** | 0.4 VAL | 150 | University relations |
| 17 | #7 County kit via state association/co-op/Vant4ge | 2 | 4 | 3 | 3 | **2.80** | 0.9 REV | 120 | State and local practice lead |
| 18 | #15 Capstone-as-a-service state studios | 2 | 4 | 3 | 3 | **2.80** | 0.75 REV | 150 | State and local lead + university relations |
| 19 | #19 Fee-at-risk outcome SLA | 2 | 4 | 4 | 2 | **2.80** | 0.5 REV | 50 | AI CoE PO + contracts |

**Totals (ESTIMATE):**
- The mid estimates sum to about **$24.4M**: about $17.9M REV and about $6.5M VAL. Total one-time cost is about $2.3M.
- The ideas overlap. #3, #4 and #19 all lift win rate or cycle, and #8, #7 and #6 share state HHS accounts. I therefore apply a **~30% overlap haircut**, which gives **about $12–13M of incremental revenue plus about $4.5M of value over 3 years**.
- That roughly doubles the reconciled incremental baseline. It does **not** by itself fix 5-year payback. It does close most of the cost analyst's scenario A→C gap when combined with #5, #12, #17 and the harness kill-gate.

---

## 3. Robustness

- Re-ranked at revenue 50 / cost 10 / time 20 / risk 20, the top 5 are unchanged (#3, #2, #4, #17, #5). Positions 6–8 reorder to #9, #16, #1.
- #6 (Medicaid 90/10) is the idea most sensitive to the time weight. On revenue alone it ties for the top score, but first revenue lands only in FY2. I recommend starting the APD work now even though it ranks 11th.

## 4. Dependencies and mutual exclusions

| Relation | Ideas | Note |
|---|---|---|
| **Mutually exclusive** | #12 (open-source harness core) ↔ licensing the harness *core* under #10 | Under #12, only mission suites are licensed in #10 |
| **Mutually exclusive (choose primary)** | #1 internal firewall ↔ #1 third-party co-signer | They can coexist by account, but one must be the default. Use the co-signer where the OIG is the audience |
| **Trade-off** | #16 ↔ integrator revenue on the same procurement | FAR 9.505-3: an evaluator can't bid. Pick #16 only where Guidehouse wouldn't bid |
| **Tension** | #10 crosswalk OEM ↔ mapper managed-service moat | Mitigate with a 6-month content lag and no state-HHS packs in OEM |
| Depends on | #9 → #5 | Marketplace deals deploy in agency tenants instead of Guidehouse-hosted FedRAMP |
| Depends on | #8 → #1 | Vant4ge deployments get build-time QA only, never independent assurance |
| Depends on | #8, #6 → #11 | CJIS sandbox and MES test data come from the open data generator |
| Depends on | #7 → #8 and #17 | County economics need the Vant4ge channel and templated delivery |
| Depends on | #13 → #12 | UK assurance runs on Inspect |
| Depends on | #19 → #17 | Fees go at risk only after delivery is productized |
| Depends on | #15 → #14, #11 | |
| Overlap (not additive) | #3, #4, #19; #6, #7, #8 | Included in the 30% haircut |
| External dependency | #10, #11, #12 | The university IP assignment must allow Guidehouse to relicense and open-source |

## 5. Round-1 findings addressed

- **Conflict of interest (R3):** #1 (firewall, co-signer, build-time QA), #16 (a new buyer with no conflict), and #8 (keeps assurance off Guidehouse-integrated Vant4ge deployments).
- **CIO-SP4 cancelled:** #3 (MAS SINs, OASIS+, CDAO T&E BPA via Tradewinds, NASPO, TS4).
- **County channel (R11):** #7, with a per-county CAC cap below $10K and a kill rule at $15K.
- **Medicaid 90/10 (R12):** #6.
- **FedRAMP gating:** #5 and #9.
- **Harness cost sink:** #2 (price floor ≥$100K per system), #12 (open-source core, licensed attack libraries), #1 (recover conflicted accounts), and the FY2 M6 kill-gate.

## 6. Suggested 90-day sequence

1. **Month 0–1:** #3, #2, #5 and #18. These are pricing and governance decisions that cost almost nothing.
2. **Month 1–3:** #17 internal rollout, #4 bundle, and #11 open-source review. Start the #6 APD template and the #1 OCI plan.
3. **Month 3–6:** #9 listings, #8 Vant4ge joint SKU, #13 UK pack, and #16 protocol.
4. **FY2:** #10, #7, #15 and #19, and only if the FY2 M6 gates are met.

## 7. Flags for teammates

- **revenue_modeler:** please replace my working baseline. My lever-based impacts (#3, #4, #19) scale off your pre-ruling sensitivities × 0.7.
- **cost_and_margin_analyst:** #17's $8M/yr FFP addressable base is the key unverified number. #5 and #12 change F and I in your scenario B/C.
- **devil_advocate:** the strongest attack on this list is that about 27% of the value is [VAL] (cost avoided), not revenue, and that #4 and #17 partly repackage revenue Guidehouse already earns.

## Sources
- https://www.nextgov.com/artificial-intelligence/2026/04/agencies-report-over-3000-ai-use-cases-2025/412898/
- https://www.govinfo.gov/content/pkg/FR-2025-08-27/html/2025-16412.htm
- https://guidehouse.com/government-contract-vehicles/oasis-plus
- https://www.sweetspot.so/markets/federal/vehicles/ai-test-and-evaluation/
- https://www.executivegov.com/articles/nitaac-cio-sp4-cancellation
- https://www.pilieromazza.com/omb-issues-memoranda-on-use-and-acquisition-of-ai-by-federal-agencies-part-1-what-it-means-for-government-contractors/
- https://orangeslices.ai/guidehouse-secures-64m-cms-federal-and-state-exchange-improper-payment-measurement-rc-support-contract/
- https://github.com/UKGovernmentBEIS/inspect_ai
- https://govramp.org/pricing-overview
- https://lifestyle.q923radio.com/story/157747/vant4ge-partners-with-guidehouse-to-advance-ai-enabled-solutions-for-public-safety-and-human-services-2/
- https://aws.amazon.com/blogs/awsmarketplace/how-to-create-consulting-partner-private-offers
- https://aws.amazon.com/blogs/publicsector/aws-marketplace-myth-busting-for-state-and-local-government-agencies
- https://aws.amazon.com/marketplace/pp/prodview-x67krdatcdday
- https://www.medicaid.gov/federal-policy-guidance/downloads/smd22001.pdf
- https://gov.uk/government/publications/ai-playbook-for-the-uk-government/artificial-intelligence-playbook-for-the-uk-government-html
- https://gov.uk/government/publications/algorithmic-transparency-recording-standard-mandatory-scope-and-exemptions-policy/algorithmic-transparency-recording-standard-atrs-mandatory-scope-and-exemptions-policy
- https://www.find-tender.service.gov.uk/Notice/001978-2026
- https://naceweb.org/talent-acquisition/internships/intern-offer-and-conversion-rates-fall-acceptances-rise
- https://www.shrm.org/topics-tools/research/2025-recruiting-benchmarking
