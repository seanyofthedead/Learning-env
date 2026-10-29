# 07 — Devil's Advocate: why this program will not move Guidehouse revenue

**Role:** devil_advocate, round 2. **As of:** 2026-10-29.
**Inputs:** 00_context, 01_revenue_modeler, 02_cost_margin, 03_market_competition, 04_buyer, 05_reconciliation_rulings.
**Model:** a deterministic script at `/tmp/claude-0/-home-user-Learning-env/597ac1d9-a808-55f6-8cf9-a6a3d19428fc/scratchpad/devil/devil.py`. It produced every devil's-case number below.
**Labels:** every input is **ESTIMATE** unless a URL is cited. Amounts are USD.
**Calendar:** FY1 starts at capstone delivery. Per 02_cost_margin, the capstone ends in May 2027, so FY1 runs Jun 2027–May 2028, FY2 Jun 2028–May 2029 and FY3 Jun 2029–May 2030. Quarters are program quarters: FY1 Q1 is Jun–Aug 2027.

---

## 0. Verdict in five lines

1. **Materiality bar.** Guidehouse has about $3B in revenue ([Washington Technology](https://washingtontechnology.com/companies/2023/11/guidehouse-get-more-global-private-equity-owner/391799/); [Wikipedia](https://en.wikipedia.org/wiki/Guidehouse)). "Material" means **≥1% of revenue, about $30M/yr of *incremental* revenue, by FY3** (see §1).
2. **Even the optimistic models fall short.** The revenue modeler's pre-ruling base produces **$13.95M gross in FY3 (0.47%)**. Only its *upside* case ($29.9M gross FY3) reaches the bar, and only on a gross basis.
3. **The devil's case is far smaller.** It produces **$4.2M gross in FY3 and $7.6M gross over 3 years**. After netting out work Guidehouse would win anyway, that becomes **$2.9M incremental in FY3**. After cannibalization of existing time-and-materials (T&M) hours, net new revenue is **$0.6–1.7M in FY3, or 0.02–0.06% of the firm.**
4. **Cash is negative and keeps getting worse.** Cumulative program cash is **−$11.4M by FY3 and −$15.5M by FY5**, with no payback. Covering fixed run cost alone would take about **$40M/yr of gross program revenue** at devil's-case margins.
5. **What it really is.** The program is at best a **margin-and-win-rate tool for the existing advisory book**. It is not a revenue line. Fund it that way: about $1M, internal-only, with the kill gates in §8. Do not fund a $4–6M product bet.

---

## 1. What "material" means for Guidehouse

| Anchor | Value | Basis |
|---|---|---|
| Firm revenue | ~$3.0B/yr | Cited at the Bain deal (Nov 2023, $5.3B EV) ([Washington Technology](https://washingtontechnology.com/companies/2023/11/guidehouse-get-more-global-private-equity-owner/391799/); [consulting.us](https://www.consulting.us/news/9917/bain-capital-to-acquire-guidehouse-for-53-billion)). Guidehouse is private and 2025 revenue is unverified. **ESTIMATE: $3.0–3.5B** |
| Organic growth a PE owner expects | ~6–8%/yr ≈ $180–240M of new revenue each year | ESTIMATE |
| EBITDA | ~12–15% ≈ $360–525M | ESTIMATE, typical for government services |
| **Revenue materiality threshold** | **≥1% of revenue ≈ $30M/yr incremental by FY3**, or ≥10% of one year's organic growth (≈$20M) | 1% is the conventional threshold for a line a CEO tracks or a PE board discusses. A sub-1% line does not change guidance, valuation or headcount plans |
| "Noticeable" (not material) | 0.5% ≈ $15M/yr | ESTIMATE |
| **Profit materiality** | ≥1% of EBITDA ≈ $4–5M/yr contribution | A program can be material to *profit* without being material to *revenue*. That distinction is the core of §5 |

**Test:** does the program produce at least $30M/yr of *incremental* revenue in FY3, or at least $4–5M/yr of *net contribution*? In the devil's case it fails both by about 20×.

---

## 2. Devil's-case 3-year model (formulas + outputs)

### 2.1 Inputs, and why each differs from 01_revenue_modeler

| Input | Rev-modeler base (pre-ruling) | Ruling (05) | **Devil** | Evidence for the devil's number |
|---|---|---|---|---|
| Mapper assessment wins FY1/FY2/FY3 | 6.0 / 13.1 / 20.8 (≈40) | — | **3 / 7 / 11 (21)** | (a) CAIO offices have 3–8 FTE and **no contract budget** (04 §1a). (b) Credo AI + Booz Allen already sell an "AI Inventory Jumpstart" ([Credo AI](https://www.credo.ai/blog/credo-ai-and-booz-allen-transforming-ai-governance-for-federal-agencies)). (c) The M-25-21 deadline passed in Apr 2026, so the "get ready" wave has largely been bought, and the market is now remediation (04 §0). (d) There are 445 high-impact systems in **56 agencies** ([Nextgov](https://www.nextgov.com/artificial-intelligence/2026/04/agencies-report-over-3000-ai-use-cases-2025/412898/)). Winning 21 governance task orders in 3 years means about 1 in 3 agencies, against Booz, Deloitte, EY, MITRE, Accenture Federal and Tech2i |
| Blended assessment price | $250K federal / $150K state | — | **$190K** | Buyer: kept under the $350K SAT, $150–340K federal, $100–250K state, $15–60K county (04 §2.2) |
| Implementation conversion / price | 50% / $400K | — | **35% / $280K** | Buyers want output pushed into the GRC tool they already own, not a new implementation (03 §3.4) |
| Assessment→subscription | 40% (50%×80%) | **35%** | **20%** | Federal subscriptions need authorization. Buyer prior is 30–40% (04 §5.1). Every verified platform buyer already owns a GRC system of record (03 §3.4). Free templates cover the inventory (§6.3). Commercial SaaS benchmark: a 15–25% services-to-subscription conversion is typical for "assessment-led" land motions (ESTIMATE, no public source) |
| Federal subscription start | FY2 M6 | **FY3 M6** | FY3 M6, **0.25 yr of revenue in FY3** | Ruling R7 |
| Subscription renewal | 90% | — | **75%** mapper | Option-year non-exercise. CAIO budgets are borrowed (04) |
| Harness attach to mapper | 35% | 40% COI haircut on warm accounts | **15%** | 35% × (1 − 0.40 COI) = 21% *before* the episodic-demand problem. Buyer: at most 15% where Guidehouse is the SI (04 §2.3) |
| Harness standalone wins | ≈10 | — | **0.5 / 2 / 3** | Free substitutes (Inspect, garak, PyRIT, Dioptra, GSA USAi + CAISI). Big-security bundling (03 §4) |
| Harness price / recurring conversion / renewal | $175K / 60% / 85% | renewal **60%** | **$150K / 30% / 50%** | Testing is event-driven, at deployment or major change (04 §5.2). Market sprint price is $75–150K per agent (03 §4.2) |
| Data generator | $2.0M incl. license + OEM | custom packs only | **0 / 2 / 3 packs × $75K** | R4 |
| Incrementality net-out | 0 | **40%** of assessments | **50%** of assessments | The AI CoE and the Maturity Model already sell this work. The capstone tool does not create the client relationship |
| Hardening + sponsorship (I) | $4.38M (130 FTE-mo) | — | **$5.62M** ($0.42M sponsorship + $5.2M hardening) | §4 |
| Fixed run cost (F) | $2.0M/yr (GOV $0.94M + RTH $0.82M + SDG $0.24M) | — | **$2.45M/yr**, half-year in FY1 | §4.3 |
| Contribution margin | — | — | **35%** services, **45%** subscription | 02 §3. The 55% tool-assisted assessment margin is competed away (§5) |
| CAC | $150K blended | — | **$100K × incremental wins** | Mostly expansion. Charged only on the 50% of wins that are incremental |

### 2.2 Formulas (as implemented)

- `MAP_assess[Y] = wins[Y] × 0.19`
- `MAP_impl[Y] = 0.35 × (0.5·wins[Y] + 0.5·wins[Y−1]) × 0.28`
- Non-federal subscriptions:
  - `new_nf[Y] = 0.20 × wins[Y−1] × 0.40`
  - `rev_nf[Y] = (active_nf[Y−1]·0.75 + 0.5·new_nf[Y]) × 0.15`
- Federal subscriptions:
  - `fed_pool = 0.20 × 0.60 × (wins[1] + wins[2])`
  - `rev_fed[3] = fed_pool × 0.25 × 0.25` (all federal subscriptions start FY3 M6)
- `HARwins[Y] = 0.15 × (0.5·wins[Y] + 0.5·wins[Y−1]) + standalone[Y]`
- `HAR_assess = HARwins × 0.15`
- `HAR_impl = 0.25 × HARwins × 0.15`
- `HAR_sub[Y] = (active[Y−1]·0.50 + 0.5·0.30·HARwins[Y−1]) × 0.15`
- `GROSS = Σ lines`
- `INCREMENTAL = GROSS − 0.50 × (MAP_assess + HAR_assess)`
- `Cannibalized[Y] = Book × T&M_share × hour_cut × adoption[Y]`, with Book = $30M, T&M share = 0.5, hour cut = 0.375, adoption = 10% / 25% / 40%
- `NET = INCREMENTAL − Cannibalized × (1 − redeploy)`
- `CM = 0.35 × (INCREMENTAL − subs) + 0.45 × subs`
- `Contribution = CM − F − CAC`
- `Cum cash = −I + Σ Contribution`

### 2.3 Output ($M)

| Line | FY1 | FY2 | FY3 | 3-yr |
|---|---|---|---|---|
| Mapper assessment | 0.57 | 1.33 | 2.09 | 3.99 |
| Mapper implementation | 0.15 | 0.49 | 0.88 | 1.52 |
| Mapper subscription | 0.00 | 0.02 | 0.14 | 0.16 |
| Harness assessment | 0.11 | 0.41 | 0.65 | 1.17 |
| Harness implementation | 0.03 | 0.10 | 0.16 | 0.29 |
| Harness recurring | 0.00 | 0.02 | 0.08 | 0.09 |
| Data-gen custom packs | 0.00 | 0.15 | 0.22 | 0.38 |
| **GROSS core** | **0.85** | **2.52** | **4.23** | **7.61** |
| **INCREMENTAL** (−50% of assessments) | 0.51 | 1.65 | 2.86 | 5.03 |
| Cannibalized T&M revenue on the existing book | −0.56 | −1.41 | −2.25 | −4.22 |
| **NET new revenue, 0% redeployment of freed hours** | **−0.05** | **0.24** | **0.61** | **0.81** |
| **NET new revenue, 50% redeployment** | 0.23 | 0.95 | 1.74 | 2.92 |
| Program contribution (CM − F − CAC) | −1.23 | −2.36 | −2.19 | −5.78 |
| **Cumulative cash incl. I = $5.62M** | **−6.85** | **−9.21** | **−11.40** | |
| FY3 exit ARR | | | **0.55** (mapper 0.41, harness 0.14) | |

- **Payback.** None. Extrapolating gross at +35%/yr, cumulative cash is **−$13.5M at FY4 and −$15.5M at FY5**.
- **Break-even.** `F / (CM% − CAC%)` = 2.45 / (0.24 − 0.18) ≈ **$40M/yr of gross program revenue** just to cover run cost. That is 10× the devil's FY3 figure and about 3× the rev-modeler base.
- **Materiality.** Net FY3 revenue of $0.6–1.7M is **0.02–0.06%** of $3B. Incremental FY3 revenue of $2.9M is **0.1%**.

### 2.4 Cross-check against the other models

| | FY3 revenue | 3-yr | % of $3B (FY3) |
|---|---|---|---|
| Rev-modeler upside (gross) | 29.9 | 51.7 | 1.0% |
| Rev-modeler base, pre-ruling (gross) | 13.95 | 23.8 | 0.47% |
| Reconciled base (my projection of rulings R1–R7; the rev-modeler rerun governs) | ~8–10 gross / ~5–7 incremental | ~14–17 gross | ~0.2–0.3% |
| Rev-modeler downside | 3.75 | 6.3 | 0.13% |
| **Devil (incremental / net)** | **2.9 / 0.6–1.7** | **5.0 / 0.8–2.9** | **0.02–0.1%** |

The devil's case sits just under the rev-modeler's own downside. **No case except the gross upside crosses 1%.** That conclusion holds whatever one thinks of my individual inputs.

---

## 3. Attack 1 — attach and conversion rates

| Rate | Claim | Devil | Argument |
|---|---|---|---|
| Mapper → harness attach | 35% | **15%** | (1) **FAR 9.5 COI.** The buyer says ≤15% where Guidehouse is the SI (04 §2.3). The ruling removes 40% of warm-account opportunities. (2) **Different buyer.** The mapper is bought by the CIO/CAIO. The harness is bought by the *program office that owns the AI system* (04 §2.3), so attach requires a second sale. (3) **Episodic need.** Testing happens at deployment or major change. Only about 10–15 civilian agencies have the ≥8–10 high-impact cases that justify a portfolio (04 §5.2). The 445 high-impact systems are concentrated: VA has 215 ([ExecutiveGov](https://executivegov.com/articles/omb-federal-ai-use-cases-2025)). (4) **Free and government substitutes** are standardizing: GSA USAi has 25+ agencies on it at no cost today ([MeriTalk](https://www.meritalk.com/?p=207921)), and the GSA–CAISI MOU (Mar 2026) standardizes evaluation ([NIST](https://www.nist.gov/news-events/news/2026/03/caisi-signs-mou-gsa-boost-ai-evaluation-science-federal-procurement-through)) |
| Assessment → subscription | 40% → 35% (R1) | **20%** | Federal subscriptions are gated until FY3 M6. An 18–30-month gap between the assessment and the first subscription dollar means the CAIO, budget and priorities can all change. Agencies own RegScale, Xacta, ServiceNow or watsonx and want OSCAL *output*, not another tool (03 §3.4). Microsoft ships NIST AI RMF, ISO 42001 and EU AI Act templates inside Purview Compliance Manager ([Microsoft Learn](https://learn.microsoft.com/purview/compliance-manager-regulations-list)), and an AI feature that turns regulatory PDFs into templates (MC1192260, [handsontek](https://m365admin.handsontek.net/microsoft-purview-compliance-manager-ai-powered-regulatory-templates/)). That is the mapper's core function, bundled into an E5 licence agencies already pay for |
| Harness renewal | 85% → 60% (R2) | **50%** | Recurring testing has no regulatory mandate. M-25-21 requires *ongoing monitoring*, which the agency's own vendor tooling (Azure Foundry red-teaming agent, Bedrock Guardrails) can claim to satisfy |
| Mapper renewal | 90% | **75%** | Borrowed CAIO money. Option years go unexercised on recompete or when a CAIO leaves |
| Pull-through (0.5×) | 01 §3 | **0.2× and not incremental** | Remediation, ATO and modernization follow-on is exactly the work Guidehouse already sells. Counting it double-counts the existing book |

---

## 4. Attack 2 — "capstone code can be hardened cheaply"

### 4.1 Code survival: 30% is not supported

- **No published study measures production survival of sponsored-capstone code.** The closest is a 7-year study (300+ projects, 200+ organizations). It found that **some sponsors value proof of concept over deployed systems** and that only the best-performing projects were fully deployed ([SMU/AMCIS 2020](https://ink.library.smu.edu.sg/sis_research/5278)). Programs that sell IP ownership typically bar students from presenting the work (Kennesaw, $15K IP tier; [KSU PDF](https://campus.kennesaw.edu/colleges-departments/ccse/partnerships/docs/capstone-sponsorship-overview.pdf)). That cuts the student incentive to polish.
- **Mechanism (ESTIMATE).** A two-semester team of 4–5 students working 8 h/week spends most of its effort on UI and integration glue. Those are the layers that get rewritten for PIV/CAC SSO, multi-tenancy, RBAC, audit logging, 508 and SBOM.
- **What survives is non-code:** schemas, eval sets, requirements and UX. The LLM framework the students pick, such as a 2026-vintage LangChain or LlamaIndex version, will be one or two major versions stale by hardening.
- **Devil: 10–15% code survival.** Rewrite effort scales roughly with (1 − survival). Going from 70% to 87% rewrite raises the rewrite line in 02 §2 from 32 to about 40 FTE-months.

### 4.2 Hardening budget re-estimated

| Item | 02 (FTE-mo) | Devil (FTE-mo) | Why |
|---|---|---|---|
| Rewrite (SDG/GOV/RTH) | 26 | 34 | Survival of 10–15% instead of 30% |
| LLM eval + corpora | 22 | 36 | GOV needs a **clause-level citation gold set** across about 8 frameworks before anyone will sign a gap analysis ("who signs?", 04 §2.2). RTH needs agent-specific attack suites |
| Security / 508 / productization | 32 | 40 | RTH runs adversarial payloads, so it needs an isolated sandbox. Overrun factor 1.25 |
| ATO internal | 20 | 25 | Overrun |
| **Total (3 core products)** | **105 (+25 IPA = 130)** | **~135 FTE-mo + external $0.69M + 15% schedule contingency ≈ $5.2M** | Overrun benchmark: implementations "often run 2–3× initial estimates" ([CostBench, unverified aggregator](https://www.costbench.com/software/ai-evaluation/ragas/hidden-costs/)). I apply only about 1.35× |

### 4.3 The real cost is keeping content current, and 02 understates it

Frameworks the mapper must track, and their churn:

| Framework | Recent churn | Source |
|---|---|---|
| NIST SP 800-53 | Release 5.2.0 added SA-15(13), SA-24 and SI-02(07) in Aug 2025, shipped five days after preview | [NIST CSRC](https://csrc.nist.gov/News/2025/nist-releases-revision-to-sp-800-53-controls) |
| COSAIS AI overlays | Drafts through 2026 | 03 §1 |
| CJIS | v6.0 (Dec 2024), transition to ~2027 | 04 §0 |
| HIPAA Security Rule | Rewrite pending (ESTIMATE) | — |
| GovRAMP | Rebrand | 03 §1 |
| FedRAMP 20x | Moves from controls to KSIs, which changes the mapping target itself | — |
| OMB AI memos | M-24-10 → M-25-21 (Apr 2025) → M-26-04 (Dec 2025, **sunsets ~Dec 2027**) | 03 §1 |
| State AI laws | TRAIGA; Colorado delayed and litigated; DOJ preemption task force | 03 §1 |
| Others | IRS 1075, MARS-E → ARC-AMPE, UK ATRS | 04 §2.2 |

- **The buyer's must-have is a 30-day SLA on rule changes** (state CTO, 04 §2.2). Meeting that across about 12 sources with lawyer-grade citations takes about **1.5 FTE, not 0.75**.
- **LLM eval maintenance:**
  - Hosted models are deprecated on roughly 12–18-month cycles (ESTIMATE). Each migration means re-running the gold set, re-tuning prompts and, if the embedding model changes, **re-indexing the whole corpus** ([apxml](https://apxml.com/courses/optimizing-rag-for-production/chapter-1-production-rag-foundations/rag-long-term-maintenance)).
  - Gold sets go stale as rules change.
  - Practitioner budgets are about €150K/yr of engineering for one RAG system, before content experts ([curiosity.ai](https://blog.curiosity.ai/blog/2026-07-cost-of-a-diy-rag-stack)).
- **Harness:** attack taxonomies age in months (02 §6). The bias module must support **two opposing policy regimes**, demographic bias and M-26-04 "ideological neutrality" (03 §1).
- **Devil's F = $2.45M/yr**, versus 02's $2.0M across GOV, RTH and SDG. This is the cost that makes payback impossible.

---

## 5. Attack 3 — cannibalization: margin up, revenue down

The cost analyst's own numbers: a mapper assessment takes **720 hours without the tool and 450 with it**, a 37.5% cut (02 §3). That is a productivity tool, and on hourly work productivity tools lower revenue.

**Setup (ESTIMATE).**
- Guidehouse's existing AI-governance, ATO-documentation and compliance-mapping advisory book that the tool would touch: **B = $30M/yr**. This is a small share of a $3B firm with large cyber, health and ATO practices.
- **50% is T&M/labor-hour**, where revenue = hours × rate. 50% is fixed-price.
- Internal adoption reaches 10% / 25% / 40% in FY1–FY3.

| Effect | Formula | FY3 | 3-yr |
|---|---|---|---|
| Lost T&M revenue | B × 0.5 × 0.375 × adopt | **−$2.25M** | −$4.22M |
| Lost contribution on that revenue (30% CM) | × 0.30 | −$0.67M | −$1.27M |
| Fixed-price cost saving (cost = 70% of revenue) | B × 0.5 × adopt × 0.70 × 0.375 | +$1.57M | +$2.95M |
| **Net on the existing book** | | **Revenue −$2.25M, profit +$0.90M** | **Revenue −$4.2M, profit +$1.7M** |

**Implications.**
- Cannibalization alone (−$2.25M) **wipes out 79% of the devil's FY3 incremental product revenue** ($2.86M).
- Freed hours have to be resold to be revenue-neutral. At 50% redeployment, net FY3 is $1.74M. At 0%, it is $0.61M.
- **The fixed-price gain erodes too.** Price-reasonableness reviews and GSA's software-should-be-cheap anchor ([FedScoop OneGov](https://fedscoop.com/gsa-onegov-ai-deals-some-extensions-new-offers/)), push fixed prices down once competitors (Booz + Credo, Deloitte) use the same AI. Clients are already demanding AI-driven savings from Accenture and the Big Four ([Irish Times/FT](https://www.irishtimes.com/business/2026/08/31/consultants-head-for-a-showdown-with-their-own-clients/)). Assume the 27-point margin gain halves by FY3.
- **Firm-level 3-yr P&L of the program** = program contribution −$5.78M − I $5.62M + existing-book profit +$1.68M ≈ **−$9.7M**.

**Bottom line.** Revenue moves *down* on the existing book while profit moves up a little. The program can be **profit-accretive only if the product lines are tiny and the tool is used purely internally on fixed-price work**. That is an internal-tooling case, not a product case.

**Sensitivity.** At B = $10M, cannibalization is −$0.75M in FY3 and the conclusion is unchanged. At B = $60M, net FY3 revenue is negative.

---

## 6. Attack 4 — channel conflict and platform encroachment

### 6.1 Vant4ge
- **Vant4ge sells its own AI.** Vant4gePoint, plus **AIDA, a patent-pending agentic AI interview system** ([HJ News / PRNewswire, 7 Apr 2026](https://www.hjnews.com/news/state/vant4ge-partners-with-guidehouse-to-advance-ai-enabled-solutions-for-public-safety-and-human-services/article_b3a5adc8-787c-505e-95e4-9279a6879242.html)). The press release gives Guidehouse "advisory, implementation, and change management" ([Guidehouse](https://guidehouse.com/news/communities-energy-infrastructure/2026/vant4ge-partnership)). It does not give Guidehouse an assurance role over Vant4ge's AI.
- **Red-teaming AIDA is a conflict.** If Guidehouse red-teams AIDA, it is assuring its partner's product, which is impaired objectivity. If it publishes adverse findings, it damages the partner. Either way the "every Vant4ge deployment ships with a harness line" attach rule (03 §4.4) is contestable by Vant4ge itself.
- **Vant4ge can build the governance layer itself.** The likely move for a 28-year platform vendor is to add native governance and audit features to keep the account (ESTIMATE). A third-party add-on raises the TCO of the bid, which works against a county buyer who is price-sensitive (04 §2.2).
- **The partnership is untested.** It is less than 7 months old and has no disclosed joint award (no USAspending evidence found, ESTIMATE).

### 6.2 Integrators that might resell
- Booz Allen has Credo AI. Deloitte, Accenture Federal, Leidos and CACI hold the CDAO AI T&E BPA (79 holders, 03 §4.3). Maximus, Conduent and Gainwell own state HHS.
- **No integrator resells a competitor's delivery engine.** The OEM/royalty line was correctly cut by R4.

### 6.3 Hyperscalers and platforms (near-zero marginal price, already inside the boundary)

| Vendor | Feature | Overlap |
|---|---|---|
| Microsoft | Purview Compliance Manager NIST AI RMF / ISO 42001 / EU AI Act templates ([MS Learn](https://learn.microsoft.com/purview/compliance-manager-regulations-list)); AI regulatory-template generation ([MC1192260](https://m365admin.handsontek.net/microsoft-purview-compliance-manager-ai-powered-regulatory-templates/)); Foundry **AI Red Teaming Agent** with agentic-risk tests (public preview, Nov 2025) ([MS DevBlogs](https://devblogs.microsoft.com/foundry/assess-agentic-risks-with-the-ai-red-teaming-agent-in-microsoft-foundry/)) | Mapper + harness |
| AWS | Bedrock Guardrails **Automated Reasoning checks** that compile policy documents into verifiable rules, with source references (Feb 2026) and refinement workflows (Jun 2026); Guardrails in GovCloud ([AWS](https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-guardrails/), [AWS KMS note](https://aws.amazon.com/about-aws/whats-new/2025/10/customer-managed-kms-keys-automated-reasoning-checks)) | Harness / runtime assurance |
| ServiceNow | **AI Control Tower**: AI asset inventory, lifecycle, risk and compliance, agent auto-discovery; government go-to-market via Carahsoft ([ServiceNow docs](https://www.servicenow.com/docs/r/store-release-notes/store-integrationhub-rn-ai-control-tower.html); [GovEvents](https://govevents.com/event/27987)) | Mapper inventory + impact assessments |
| Google | Vertex AI evaluation / model armor (ESTIMATE, not verified here) | Harness |

**Consequence.** The mapper competes for the *same GRC seat* that ServiceNow and Microsoft already hold. The only defensible piece is the **human-signed, cited, maintained crosswalk**, which is labor. Labor scales linearly and is exactly what §5 shows the tool cannibalizes.

---

## 7. Attack 5 — other structural risks

| Risk | Mechanism | Revenue effect (ESTIMATE) |
|---|---|---|
| **COI of red-teaming what you build** | FAR 9.5 impaired objectivity and biased ground rules. Guidehouse's warm accounts (federal health, the CMS improper-payment incumbency at $63.9M, Vant4ge clients) are exactly where it builds or integrates. An independent-assurance firewall needs a separate team, which raises F | Removes 40–60% of the harness's addressable warm market. It also risks *existing* SI recompetes if an OIG flags the conflict |
| **Policy volatility** | Three OMB AI memo regimes in 20 months. M-26-04 sunsets ~Dec 2027, *inside FY1*. The DOJ AI Litigation Task Force targets state laws. The 1–2-year product rebuild cycle collides with an 18–30-month sales-to-subscription lag | Each regime change resets gold sets and bias suites, costing about 2–4 FTE-months each (ESTIMATE). It also lets buyers defer: "wait for the next memo" |
| **Free government baselines** | GSA USAi is free to 25+ agencies today and moves to cost recovery in FY27 ([MeriTalk](https://www.meritalk.com/?p=207921)). The GSA–CAISI evaluation framework is due for pilots ([GSA](https://www.gsa.gov/about-us/newsroom/news-releases/gsa-and-nist-partner-to-boost-ai-evaluation-science-in-federal-procurement-03182026)). CIO Council inventory guidance and templates are free ([cio.gov](https://CIO.gov/assets/resources/2023-Guidance-for-AI-Use-Case-Inventories.pdf)). NIST AI RMF Playbook, NACo and GovAI Coalition toolkits are free | Caps subscription price at about $100–150K (01 §8.3). This is the source of the 20% conversion figure |
| **University IP and no-real-data** | Students and faculty may retain publication rights, and student-introduced copyleft dependencies contaminate the code. The no-real-data clause means the mapper is **never tested on a real SSP** and the generator is calibrated only on published statistics (03 §2.4). Accuracy is therefore unknown until the first paying client becomes the test bed | Adds 1–2 quarters to the first referenceable win. It also creates a reputational tail risk if the first client finds hallucinated control mappings |
| **Key-person risk** | One CoE product owner at 0.25 FTE across three products (02 §1). Buyers ask "who answers the phone in year 3?" (04 §4). AI product talent turnover is high (ESTIMATE ~20%/yr) | P(PO departs within 24 months) ≈ 35% (ESTIMATE). Loss of the PO plausibly stalls the program by 2–3 quarters |
| **Capstone calendar vs sales windows** | Capstones deliver in **May 2027**. Hardening takes 6–9 months, to **Dec 2027–Feb 2028**. That **misses the federal Q4 buying surge (Jul–Sep 2027)**, so the first usable federal year-end is **Sep 2028**. State FY27–28 budgets (starting 1 Jul 2027) were built in fall 2026, so the first state budget that can carry it starts 1 Jul 2028. UK fiscal year starts in April | About 12 months of dead calendar. This is why devil FY1 wins are 3, not 6 |
| **Funding** | TMF lapsed; SLCGP lapsed 30 Sep 2026 (04 §0) | R12 already applied |
| **ATO spend before demand** | $768K ATO + $270K/yr ConMon (02 §6) | Sunk if fewer than 5 federal SaaS buyers commit |

---

## 8. What would have to be true for the devil to be wrong: leading indicators and kill criteria

**Rule:** if a **KILL** threshold is missed on its date, stop new spend on that line. The lead partner should require a signed scorecard at each gate.

| # | Devil's argument | Must be true for the program to be material | Leading indicator (observable) | **Kill criterion (threshold, date)** |
|---|---|---|---|---|
| K0 | Pipeline is too small | Federal and state mapper demand is at the rev-modeler base or higher | Qualified mapper opportunities (named buyer, funding line, vehicle) | **≥15 qualified opps by capstone delivery (31 May 2027)**. **KILL hardening funding if <8** |
| K1 | Wins lag | Conversion of pipeline to signed work | Signed mapper assessments (federal + state + UK) | **≥5 signed by FY1 Q3 (end Feb 2028), ≥3 of them federal**. **KILL subscription/ATO spend if <3 signed by FY1 Q4 (May 2028)** |
| K2 | Incrementality ≈ 50% | Most wins are new buyers or new budget, not relabeled CoE work | Share of mapper wins at agencies with **no Guidehouse AI advisory task order in the prior 24 months** | **≥50% of FY1 wins are net-new accounts or new funding lines.** If <30%, reclassify as an internal tool |
| K3 | Assessment→subscription ≈ 20% | Buyers pay for maintenance | Signed subscription or managed-service options **priced ≥$150K/yr** | **≥30% of FY1 assessment clients sign a priced subscription option by FY2 Q2 (Nov 2028)**. KILL the SaaS/FedRAMP path if <20% |
| K4 | FedRAMP is spent ahead of demand | Committed federal SaaS buyers | Letters of intent or agency ATO sponsors | **≥5 committed federal SaaS buyers + 1 agency sponsor before any 3PAO contract.** If not met by FY2 Q1 (Aug 2028), stay client-tenant only |
| K5 | Harness attach ≈ 15% (COI + episodic) | Attach without conflict | Harness deals at agencies where Guidehouse is **not** the builder/SI; OCI mitigation plans accepted by COs | **≥25% attach on FY1 mapper clients by FY2 Q2, and 0 OCI protests or CO rejections**. KILL the standalone harness product if attach <15% or any OCI finding; fold it into the mapper as a module |
| K6 | Harness renews ≈ 50% | Recurring assurance is bought | Renewal rate on first-year assurance contracts | **≥65% renewal on the first cohort (≥4 contracts) by FY2 Q4 (May 2029)**. Below 50% → sell it as per-system sprints only |
| K7 | Code survival ≈ 10–15%; hardening ~$5.2M | Students produced reusable code | Independent code review at capstone delivery: % of LOC kept, SAST criticals, dependency licenses | **≥25% of LOC accepted by CoE engineering and 0 copyleft contamination by 30 Jun 2027**. KILL or rescope if hardening estimate re-baselines above $4.5M |
| K8 | Hardening overruns | Delivery on budget | Burn vs 130 FTE-month plan; date the first client runs the tool | **Mapper used on a paying client by FY1 Q2 (Nov 2027)**, burn ≤110% of plan. KILL the harness hardening if cumulative burn >125% at FY1 Q3 |
| K9 | Content currency costs ≥1.5 FTE | Maintenance is cheap | Hours per framework update; time from rule publication to updated crosswalk | **≤30-day update SLA met on ≥90% of changes at ≤0.75 FTE through FY1**. Otherwise reprice the subscription ≥$250K or cut frameworks |
| K10 | Cannibalization | Freed hours are resold | Advisory-book revenue in tool-using teams vs control teams; utilization | **Tool-using teams' revenue per FTE ≥ control by FY2 Q2**, and the book does not shrink >5% YoY. If T&M revenue falls >10% with no redeployment, restrict the tool to fixed-price work |
| K11 | Channel conflict | Vant4ge pulls Guidehouse in | Joint Vant4ge bids that include a mapper or harness line; Vant4ge-sourced opps | **≥3 joint bids with a governance line by FY1 Q4 (May 2028), ≥1 won**. Drop the channel assumption (and all county revenue) if 0 |
| K12 | Hyperscaler/platform encroachment | Buyers want Guidehouse output over native tools | Win/loss reasons citing Purview, ServiceNow AI Control Tower, Bedrock or Foundry | **<30% of losses cite a native platform tool through FY2.** If >50%, pivot to an OSCAL-export service on those platforms |
| K13 | Key person | Program survives turnover | Named **full-time** PO + deputy; documented runbooks | **Full-time PO and named deputy in place by 31 Dec 2026 (mid-cohort; the current cohort has already started)**. KILL if the PO is ≤0.5 FTE at FY1 start |
| K14 | Policy volatility | Rules stabilize or churn creates paid demand | Paid change orders triggered by new memos (e.g. M-26-04 successor, Dec 2027) | **≥2 paid change orders from the Dec 2027 regime change by FY2 Q1** |
| K15 | Materiality | Line reaches material scale | Run-rate incremental revenue | **≥$10M incremental run-rate exiting FY2 (May 2029) and ≥$30M by FY3 exit.** If FY2 exit is <$5M, stop treating it as a product and keep it as internal tooling |

**Summary gate.** If K1, K3 and K5 are all missed by FY2 Q2 (Nov 2028), the devil's case is confirmed and the program should be moved to internal-tooling status, with spend capped at about $0.5M/yr.

---

## 9. Ideas growth_strategist will likely propose that I think fail

| Likely idea | Why it fails or is overstated |
|---|---|
| Harness **portfolio tier** at $0.6–1.2M/yr | Only about 10–15 agencies qualify (≥8–10 high-impact cases), and the warm ones are COI-conflicted (VA, HHS). Count ≤1–2 deals in the window |
| **Mandatory harness attach on every Vant4ge deployment** | Vant4ge controls the deal and has its own AI (AIDA) to protect. County buyers can't absorb added TCO. Assuring a partner's product is impaired objectivity |
| **Open-source the core and sell services** | It makes Booz, Deloitte and MITRE equally capable at zero cost. It is right for credibility but **reduces** Guidehouse's revenue uniqueness. Only the services (labor) remain, and §5 shows those are cannibalized |
| **Partner with RegScale/Paramify** (OSCAL export) | RegScale already ships AI-assisted control mapping (03 §3.1). Partners will absorb the RAG feature in one or two releases |
| **Raise the assessment price toward $350K** | The SAT cap is $350K. Above it, the cycle goes to 6–12 months (04 §0). Buyer WTP is $150–340K |
| **UK TS4 expansion** (ATRS) | The brand is weak (25% win rate). ATRS templates are free from GOV.UK. Inspect is the UK standard, so the UK sees nothing distinctive |
| **County volume via Sourcewell/OMNIA** | $15–60K tickets carry $50K channel CAC (R11) |
| **Outcome-based pricing** | FAR fixed-price and T&M structures make outcome fees rare in civilian agencies. It also accelerates cannibalization |
| **Improper-payment analytics on real data** | That revenue belongs to the existing CMS incumbency ($63.9M); it is not incremental to the program (R5) |
| **FedRAMP 20x fast-track as a growth lever** | It spends $768K plus ConMon before K4 demand exists. 01 §4 shows FedRAMP timing moves the 3-yr total by only about $0.7M |
| **Training/workforce revenue from the university relationship** | Low dollars (ESTIMATE <$0.5M/yr). Its value is reputational |

What I would **not** contest: using the mapper internally to raise fixed-price assessment margins, and the synthetic generator as free demo and test infrastructure. Both are real profit and win-rate levers. Neither is material revenue.

---

## 10. Recommendation from the devil's chair

1. **Reframe and cap.** Treat this as **internal delivery tooling for the AI CoE**, not a product line.
   - Fund about $0.42M of sponsorship plus at most **$1.0M** of hardening for the mapper only, client-tenant only.
   - Defer the harness and FedRAMP until K1, K3, K4 and K5 pass.
2. **Price for profit, not revenue.** Move AI-governance work to fixed price so the 37.5% hour reduction becomes margin, not lost revenue (§5).
3. **Write the kill gates (§8) into the program charter** before the first cohort starts.
4. **If leadership needs a material ($30M+) AI revenue line,** this program is not it. Larger federal health AI integration and assurance task orders on existing vehicles are the plausible route (ESTIMATE). Measured by the same yardstick, one $63.9M CMS-class award equals more than 10 years of devil's-case program revenue.

### Dependencies / expected contests
- **revenue_modeler:** will contest the 21 wins (vs ~40) and the 20% subscription conversion. The rerun under R1–R7 governs. My §2.4 projection of it is an ESTIMATE.
- **cost_and_margin_analyst:** will contest F = $2.45M/yr and I = $5.2M. Even at their $2.0M and $3.83M, cumulative FY3 cash is about −$8.9M in my model (I $4.25M, F $1.0/2.0/2.0M).
- **growth_strategist:** see §9.
- **Unverified:** Guidehouse's 2025 revenue; the size of the $30M advisory book; the T&M share; PO attrition. All are ESTIMATE.

### Sources
- https://washingtontechnology.com/companies/2023/11/guidehouse-get-more-global-private-equity-owner/391799/
- https://en.wikipedia.org/wiki/Guidehouse
- https://www.consulting.us/news/9917/bain-capital-to-acquire-guidehouse-for-53-billion
- https://www.hjnews.com/news/state/vant4ge-partners-with-guidehouse-to-advance-ai-enabled-solutions-for-public-safety-and-human-services/article_b3a5adc8-787c-505e-95e4-9279a6879242.html
- https://guidehouse.com/news/communities-energy-infrastructure/2026/vant4ge-partnership
- https://learn.microsoft.com/purview/compliance-manager-regulations-list
- https://m365admin.handsontek.net/microsoft-purview-compliance-manager-ai-powered-regulatory-templates/
- https://devblogs.microsoft.com/foundry/assess-agentic-risks-with-the-ai-red-teaming-agent-in-microsoft-foundry/
- https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-bedrock-guardrails/
- https://aws.amazon.com/about-aws/whats-new/2025/10/customer-managed-kms-keys-automated-reasoning-checks
- https://www.servicenow.com/docs/r/store-release-notes/store-integrationhub-rn-ai-control-tower.html
- https://govevents.com/event/27987
- https://csrc.nist.gov/News/2025/nist-releases-revision-to-sp-800-53-controls
- https://www.meritalk.com/?p=207921
- https://www.nist.gov/news-events/news/2026/03/caisi-signs-mou-gsa-boost-ai-evaluation-science-federal-procurement-through
- https://www.gsa.gov/about-us/newsroom/news-releases/gsa-and-nist-partner-to-boost-ai-evaluation-science-in-federal-procurement-03182026
- https://CIO.gov/assets/resources/2023-Guidance-for-AI-Use-Case-Inventories.pdf
- https://ink.library.smu.edu.sg/sis_research/5278
- https://campus.kennesaw.edu/colleges-departments/ccse/partnerships/docs/capstone-sponsorship-overview.pdf
- https://apxml.com/courses/optimizing-rag-for-production/chapter-1-production-rag-foundations/rag-long-term-maintenance
- https://blog.curiosity.ai/blog/2026-07-cost-of-a-diy-rag-stack
- https://www.costbench.com/software/ai-evaluation/ragas/hidden-costs/
- https://www.irishtimes.com/business/2026/08/31/consultants-head-for-a-showdown-with-their-own-clients/
- https://fedscoop.com/gsa-onegov-ai-deals-some-extensions-new-offers/
- https://www.credo.ai/blog/credo-ai-and-booz-allen-transforming-ai-governance-for-federal-agencies
- https://www.nextgov.com/artificial-intelligence/2026/04/agencies-report-over-3000-ai-use-cases-2025/412898/
- https://executivegov.com/articles/omb-federal-ai-use-cases-2025
- Teammate files 01–05 in this folder for all other cited figures.
