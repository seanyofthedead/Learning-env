# 04 — Public-Sector Buyer Role-Play (public_sector_buyer)

**What this is:** Three skeptical buyer personas react to the four capstone-derived products. Likelihoods, willingness to pay (WTP) and timelines are **ESTIMATE**s unless a URL is given. They come from buyer-side reasoning grounded in the policy and funding facts below, not from interviews. The revenue_modeler should treat them as priors to check against market_and_competition_analyst's pricing data.

Today's date: 2026-10-29.

---

## 0. Ground truth that shapes every persona (verified where cited)

| Driver | Status (as of Oct 2026) | Why it matters to the buyer | Source |
|---|---|---|---|
| OMB M-25-21 (federal AI use) | In force. It replaced M-24-10. Agencies must have a CAIO, publish an annual AI use-case inventory (first one due ~30 Sep 2025), and apply minimum practices to high-impact AI within 365 days (~3 Apr 2026): pre-deployment testing, an AI impact assessment and ongoing monitoring. If a use can't comply, it must be paused, or the CAIO must issue a public waiver. Several agencies reportedly missed the deadline. | The **deadline has passed**. The federal market is now *remediation and evidence of continuing compliance*, not "get ready." The CAIO owns the problem. | https://wiley.law/alert-Trump-Administration-Revamps-Guidance-on-Federal-Use-and-Procurement-of-AI ; https://kpmg.com/kpmg-us/content/dam/kpmg/pdf/2025/omb-guidance.pdf ; https://forkast.news/the-federal-ai-compliance-deadline-is-here-the-memo-behind-it-has-vanished/ |
| OMB M-25-22 (AI acquisition) | Companion memo for buying AI. It replaced M-24-18. | Agencies must check AI they *buy*. That creates demand to test vendor AI, and it puts Guidehouse's own tools under the same scrutiny. | https://www.pilieromazza.com/omb-issues-memoranda-on-use-and-acquisition-of-ai-by-federal-agencies-part-1-what-it-means-for-government-contractors/ |
| FAR thresholds | SAT rose to **$350,000** and the micro-purchase threshold to **$15,000**, both effective 1 Oct 2025. | Pricing an assessment **at or below $350K** gets simplified acquisition procedures and a much faster award. | https://www.govinfo.gov/content/pkg/FR-2025-08-27/html/2025-16412.htm |
| Technology Modernization Fund | Authorization lapsed Dec 2025, freezing ~$200M. FY26 bills reportedly earmarked only ~$5M. Extension status unclear. | **Do not model TMF as a funding source.** | https://washingtontechnology.com/contracts/2025/12/technology-modernization-fund-nears-expiration-despite-bipartisan-backing/409978 ; https://fedscoop.com/technology-modernization-fund-2026-approps-budget/ |
| State & Local Cybersecurity Grant Program (SLCGP) | Lapsed for the **third time on 30 Sep 2026**. The IIJA's $1B is largely spent. S.3251 would authorize $300M for FY26. | **Do not model SLCGP** as a dependable state or county funding source for FY27. | https://www.fdd.org/analysis/federal-grant-programs-third-lapse-endangers-state-cybersecurity/ ; https://www.congress.gov/119/bills/s3251/BILLS-119s3251is.htm |
| NASCIO 2026 priorities | **AI is #1** (first time cybersecurity has not been #1 in 12 years). Cybersecurity is #2 and budget/cost control #3. | State CTOs want AI governance but are cost-constrained. They want it cheap and enterprise-wide. | https://www.nascio.org/resource/state-cio-top-ten-policy-and-technology-priorities-for-2026/ ; https://statetechmagazine.com/article/2025/12/nascio-state-cios-put-ai-governance-first-2026-top-10-priorities-list |
| State AI laws | Texas TRAIGA took effect 1 Jan 2026. It requires government entities to disclose AI interactions and bans social scoring. The Colorado AI Act was delayed to 30 Jun 2026 and could be amended (current status unverified). | There are real but *narrow* state-law obligations. | https://www.nortonrosefulbright.com/en-us/knowledge/publications/c6c60e0c/the-texas-responsible-ai-governance-act ; https://www.gtlaw.com/en/insights/2025/9/colorado-delays-comprehensive-ai-law-with-further-changes-anticipated |
| Dec 11 2025 EO on state AI laws | DOJ AI Litigation Task Force formed in Jan 2026. BEAD non-deployment funds are a lever against "onerous" state laws. | Many states are **hesitating to add new AI rules**. That weakens "the new state law forces you to buy" as a sales argument. | https://www.ropesgray.com/en/insights/alerts/2025/12/trump-attempts-to-preempt-state-ai-regulation-through-executive-order ; https://www.hunton.com/privacy-and-cybersecurity-law-blog/trump-signs-executive-order-targeting-state-ai-laws |
| StateRAMP → GovRAMP | Rebranded in 2025. Existing agreements carry over. It has an AI Security Task Force. | SaaS sold to states usually needs a GovRAMP status. | https://govramp.org/blog/stateramp-announces-rebrand-to-govramp-reflecting-mission-to-unite-public-and-private-sectors-in-advancing-cybersecurity/ |
| CJIS Security Policy v6.0 | Released Dec 2024 and organized around NIST-style control families. Compliance and audit transition runs to ~Sep 2027 (sources disagree). | Counties and states face a real deadline for justice systems, and CJIS vendor agreements are a gate. | https://www.compassitc.com/blog/cjis-security-policy-v6.0-key-updates-you-need-to-know ; https://go-planet.com/perspectives-blog/cjis-v6-0-unpacked-whats-new-whats-not-and-why-it-matters/ |
| Medicaid systems funding | **90% federal match** for MES design, development and installation (DDI). **75%** for certified operations. Outcomes-based certification under SMD #22-001. | The best funding source for state HHS work, but the **state Medicaid agency** spends it, not the CTO. | https://www.medicaid.gov/federal-policy-guidance/downloads/smd22001.pdf ; https://syfert.com/cfr/sections/42-433.112.html |
| Improper payments FY25 | **$186B** government-wide. Medicaid **6.12% / $37.39B**, of which 77% is insufficient documentation. Medicare FFS 6.55% / $28.83B. | Real pain, but the buyers are CMS program integrity and state Medicaid PI units, and they need *real* claims. | https://cms.gov/newsroom/fact-sheets/fiscal-year-2025-improper-payments-fact-sheet ; https://www.crfb.org/blogs/federal-improper-payments-total-186-billion-fy-2025 |
| OBBBA Medicaid work requirements | States must start community-engagement requirements by **31 Dec 2026** (good-faith extension possible to end-2028). $200M FY26 for CMS implementation. | Eligibility-error risk spikes in 2027, which helps any eligibility-accuracy analytics. | https://www.nasddds.org/wp-content/uploads/2025/07/Summary-of-OBBBA-July-8-2025-1.pdf |
| Counties | ~82% rely heavily on local revenue. A large share run IT with ≤10 FTE. NACo advises *extending existing* cyber and data policies to cover AI. AI/ML is a top-3 county priority. | Small budgets, small teams. They want a template and a fixed fee, not a platform. | https://www.naco.org/sites/default/files/2026-07/2026%20County%20CIO%20Insights.pdf ; https://www.naco.org/sites/default/files/2026-08/Key_AI_Issues_Facing_US_Counties_FINAL.pdf |

---

## 1. Personas

### (a) Federal civilian CIO + Chief AI Officer — "Dana (CIO) and Raj (CAIO)," a mid-size HHS-type operating division
- **Context (ESTIMATE):** IT budget $0.8–2.5B, mostly O&M on contracts already awarded. The CAIO office has 3–8 FTE and **no dedicated contract budget**; it borrows from the CIO or from program offices. The 2025 inventory listed 40–150 AI use cases, of which 5–20 are presumed "high-impact" (benefits, health, eligibility).
- **Buying reality:** Task orders on existing vehicles (GSA MAS 54151S, OASIS+, agency BPAs, CIO-SP4 / SEWP for products). Under $350K: fast simplified acquisition. Above it: 6–12 months. A new SaaS needs FedRAMP or an agency ATO (**12–24 months, ESTIMATE**) unless it runs *inside* the agency's existing authorization boundary.
- **Raj's open problem:** The April 2026 deadline has passed. He has signed waivers or "pauses" he has to defend to OMB, the OIG and Congress. He needs **evidence** — test results, impact assessments, monitoring — for each high-impact use case.
- **Dana's worry:** Another tool in the boundary, another POA&M, another contractor with access to their System Security Plans.

### (b) State CTO — "Marisol," a mid-to-large state with a centralized IT agency
- **Context (ESTIMATE):** Enterprise IT budget $300M–1.2B, mostly recovered through chargeback to agencies. There is a governor's AI executive order requiring an inventory and a review board. Agencies are piloting Copilot/Gemini and agentic call-center tools.
- **Buying reality:** Cooperative contracts (NASPO ValuePoint), the state's own IT services master contract, or a 9–18-month RFP. SaaS needs a GovRAMP status. Data has to stay in-state or in the US, and IRS Pub 1075, CMS MARS-E / ARC-AMPE and CJIS all apply. The money is mostly agency dollars, not the CTO's.
- **Political overlay:** The preemption EO makes the governor's office wary of new AI *regulations*, but it does not stop internal governance. The legislature cares about cost.

### (c) County IT director — "Walt," a county of 300K–700K people
- **Context (ESTIMATE):** IT budget $6–20M and 25–70 IT staff, with no data scientists. The sheriff, jail, courts and DA run CJIS systems. Public health and social services. AI arrives mostly *inside vendor products* (body-cam/report-drafting AI, 311 chatbots, ERP copilots).
- **Buying reality:** Formal bid threshold $50K–$100K (**ESTIMATE, varies by state law**). Below it he can get three quotes, or piggyback on Sourcewell, OMNIA, TIPS or a state contract. The board of supervisors approves anything material. Grants are his main discretionary money, and SLCGP has now lapsed.

---

## 2. Persona × product matrix

Format: **Buy? (likelihood, ESTIMATE)** | funding line | WTP (ESTIMATE) & preferred buying form | blockers | the single feature that would make it a must-have.

### 2.1 Synthetic public-sector data generator

| | Federal CIO/CAIO | State CTO | County IT Director |
|---|---|---|---|
| **Buy?** | **Maybe — 25%** (much higher if bundled at no extra charge) | **Maybe — 35%** | **No — 10%** |
| **Funding** | Absorbed in a dev/test or modernization CLIN on an existing SI task order. No standalone line. | Agency project budgets. If it supports MES testing, it can be **charged to the 90/10 MES DDI APD** through the Medicaid agency. | General fund IT. Realistically, only if it comes free inside a Vant4ge or other vendor implementation. |
| **WTP / form** | $0 standalone. $50–150K as a deliverable embedded in a larger task order. $25–60K/yr license at most. | $40–120K one-time for a state-specific dataset. $20–50K/yr refresh. **Cooperative contract or embedded.** | <$15K (micro-purchase level). Expects it to come with the vendor's case-management implementation. |
| **Blockers** | Free alternatives exist: MITRE **Synthea** (health), CMS synthetic public-use files, open-source SDV. The Privacy Officer will ask for re-identification proof. "Our real data is messier than your synthetic data." | It has to match *their* eligibility or MMIS schema. If it doesn't, it's a toy. Privacy office sign-off if the generator was ever fitted to real data (and the no-real-data clause cuts the other way: fidelity becomes suspect). | No in-house developers or testers to use it. "That's the vendor's job." |
| **Must-have feature** | **Measured privacy guarantees (differential-privacy budget plus re-identification test report) that the agency Privacy Officer accepts in writing**, in the agency's exact production schema (e.g., T-MSIS / X12 837). | **A "standard bake-off dataset":** a state-schema synthetic caseload the state hands to *every* bidder in an RFP to demo against. That turns a test tool into a procurement-integrity tool. | **Pre-built CJIS-safe training and sandbox data for the jail/court case system they already run**, so they can train staff and test upgrades without a CJIS-cleared environment. |

### 2.2 Policy-to-AI-governance mapper (lead product)

| | Federal CIO/CAIO | State CTO | County IT Director |
|---|---|---|---|
| **Buy?** | **Maybe — 45%** (CAIO 55% / CIO 30%) | **Yes/Maybe — 50%** | **Maybe — 30%** (as a fixed-fee package, not software) |
| **Funding** | CIO cybersecurity/GRC O&M, or the CAIO borrowing from program offices. Sometimes OIG-driven remediation. **Not TMF** (lapsed). | Enterprise IT / security office (chargeback). Governor's-office AI initiative money. **Not SLCGP** (lapsed 30 Sep 2026). | General fund IT, or a risk-management/insurance line (cyber-insurance pressure). |
| **WTP / form** | **Assessment task order $150–340K (kept under the $350K SAT on purpose).** Managed subscription $100–250K/yr *only* if it runs in the agency's boundary or under an existing ATO. Prefers it **embedded in an existing GRC/ATO support contract.** | Statewide assessment and inventory $100–250K. Subscription $75–200K/yr enterprise-wide, with **agencies added at $10–25K each**. NASPO or the state IT services master contract. | **$15–60K fixed fee, deliberately under the bid threshold.** Optional $10–30K/yr update service. Sourcewell/OMNIA piggyback. |
| **Blockers** | (1) **ATO/FedRAMP** for any SaaS that ingests SSPs and control implementations (sensitive, often CUI). (2) They already pay for **ServiceNow IRM, Archer, Xacta or Telos** and want an integration, not a new pane of glass. (3) **LLM hallucinations in a compliance artifact** — "who signs the gap analysis?" (4) The CAIO has GSA/CAIO Council templates for free. (5) Lock-in: proprietary control mappings. | (1) GovRAMP. (2) The crosswalk must include **IRS 1075, CMS MARS-E/ARC-AMPE and CJIS**, not just NIST/OMB. OMB memos *don't bind states*. (3) Preemption uncertainty makes state-law mapping a moving target. (4) "Why not do it on our Copilot/Gemini tenant with a good prompt?" (5) Chargeback resistance from agencies. | (1) **Free alternatives:** NACo toolkits, GovAI Coalition templates, state-issued model policies. (2) No staff to run or maintain a RAG tool. (3) Board optics of a "Big 4–style consultant" fee. |
| **Must-have feature** | **OSCAL-native output that drops into their existing ATO/GRC tool**, with every mapping cited to the clause. It should auto-generate the **M-25-21 high-impact determination, the impact assessment and the inventory entry** in OMB's format, plus waiver justifications. | **One maintained crosswalk across NIST 800-53 / AI RMF, GovRAMP, IRS 1075, MARS-E/ARC-AMPE, CJIS 6.0 and the state's own AI EO or law, with a 30-day SLA on rule changes.** Inventory intake via a form agencies fill in themselves. | **A 30-day turnkey package:** a board-ready county AI policy, an inventory of AI *already inside vendor products*, and a **CJIS v6.0 gap crosswalk** before the 2027 audit cycle. |

### 2.3 Agentic AI evaluation and red-team harness (differentiator)

| | Federal CIO/CAIO | State CTO | County IT Director |
|---|---|---|---|
| **Buy?** | **Yes/Maybe — 50%** where Guidehouse is *not* the builder. **≤15%** where Guidehouse is the systems integrator for the system under test. | **Maybe — 40%** (rises to ~55% for agentic HHS or call-center deployments) | **Maybe — 20%** |
| **Funding** | The program office that owns the AI system (testing is part of the project cost), or the CAIO's borrowed funds for a portfolio. **M-25-22 acquisition** reviews of vendor AI. | Agency project budget. **MES 90/10 DDI** when the agent touches Medicaid eligibility or enrollment (testing is an allowable DDI cost; the Medicaid agency's money). | General fund. Possibly justice grants (Byrne JAG, ESTIMATE) for public-safety AI. |
| **WTP / form** | **$100–300K per system** (per high-impact use case, at pre-deployment and on major change). Portfolio assurance **$200–500K/yr** only if the agency has ≥8–10 high-impact cases. A firm-fixed-price task order. | $75–200K per system. A statewide "AI assurance" pre-qualified pool, with agencies ordering per system. | **$20–75K per vendor product tested.** One-time, at contract renewal. |
| **Blockers** | (1) **Organizational conflict of interest (FAR 9.5):** "You can't grade your own homework." The OIG and the CAIO will reject Guidehouse auditing an AI system Guidehouse built or integrates. (2) Free or government options: NIST/CAISI tooling, open-source eval frameworks (garak, Inspect, PyRIT), GSA evaluation work. (3) Getting access to the production agent and its data needs an ATO'd test environment. (4) "Recurring" sounds like a forever bill; testing happens at events. | (1) Same conflict-of-interest issue if Guidehouse is the state's integrator. (2) The state AI review board wants *its* criteria, not a vendor's. (3) Agentic vendors (Salesforce, Google, Microsoft) offer their own "trust" reports. | (1) The vendor won't allow testing of its product, or its terms forbid it. (2) The county can't fix what the test finds; only the vendor can. (3) Price. |
| **Must-have feature** | **Each finding mapped one-to-one to an M-25-21 minimum practice and to an ATO control, producing the evidence package the CAIO signs** — plus **a contractual independence firewall** (separate team, no build role). | **Bias and accuracy testing across language-access populations and benefit-denial outcomes**, producing a report the state AI review board and the legislature can read. | **Black-box testing of vendor AI already in use (police report drafting, 311 chatbot) without vendor cooperation**, and a plain-language public summary for the board. |

### 2.4 (Optional) Improper-payment analytics on synthetic claims

**The buyer is not the CIO, the CTO or the county IT director.** It is CMS's Center for Program Integrity / HHS program offices (federal), the state Medicaid director and PI unit (state), and the county social-services director (only in the roughly 10 states where counties run eligibility, ESTIMATE).

| | Federal (HHS/CMS program side) | State (Medicaid agency) | County |
|---|---|---|---|
| **Buy?** | **No as a synthetic-only product (≤10%).** Maybe 25% as an accelerator inside a real-data program-integrity pursuit. | **Maybe — 30%** on real data, aimed at eligibility error before the 2027 work-requirement start. | **No — 5%** (10–15% in county-administered states) |
| **Funding** | HCFAC account / program-integrity contracts (ESTIMATE). | **MES 90/10 DDI, then 75% operations once certified.** Payment Error Rate Measurement (PERM) corrective-action funding. | Admin allocations passed through from the state. |
| **WTP / form** | **$0 for synthetic-only analytics.** It is a demo asset. Value appears only inside a multi-million program-integrity task order on real claims. | $250K–1M/yr as an MES module or a corrective-action-plan deliverable. Embedded in the eligibility vendor or SI contract. | <$25K. |
| **Blockers** | Incumbent program-integrity contractors and CMS's Fraud Prevention System. Models trained on synthetic data have **no proven lift**. Conflict of interest if Guidehouse also audits or reviews the same payments. | 77% of Medicaid improper payments are documentation errors, a *process* problem rather than a model problem. Data-use agreements. | No analytics capacity. |
| **Must-have feature** | **Demonstrated lift on the agency's real held-out claims within a 60-day pilot**, reported as dollars recovered or avoided. | **PERM/MEQC eligibility-error prediction tied to the work-requirement verification workflow**, structured to qualify for 90/10 funding and CMS outcomes-based certification. | n/a |

---

## 3. What each persona buys FIRST

| Persona | First buy | Why | Entry deal (ESTIMATE) |
|---|---|---|---|
| **Federal CAIO** | **Red-team harness packaged as a "high-impact AI minimum-practices evidence package"** for 3–5 use cases, *on systems Guidehouse did not build* | The deadline has passed and he is exposed. Evidence is what he lacks. Governance documents alone don't close waivers. | $200–340K, firm fixed price, under the SAT |
| **Federal CIO** | **Governance mapper as an assessment** (an OSCAL crosswalk into the existing GRC tool) | Low risk, no new system in the boundary, buys down the POA&M burden | $150–300K |
| **State CTO** | **Governance mapper: statewide AI inventory, crosswalk and review-board kit** | AI is NASCIO's #1 priority. The governor's EO requires an inventory. Enterprise-wide spend can be split across agencies through chargeback. | $100–250K + $75–150K/yr |
| **County IT Director** | **Governance mapper as a fixed-fee "AI policy + CJIS 6.0 crosswalk" package** | The CJIS audit cycle is coming. The board wants an AI policy. It fits under the bid threshold. | $25–50K one-time |

**Nobody buys synthetic data first.** It is an *enabler* (demos, sandboxes, red-team test fixtures), not a product a budget holder pays for on its own.

---

## 4. Honest reaction to "it was built from a university capstone"

- **Federal CAIO (Raj):** *"So graduate students wrote the thing that's supposed to tell my OIG that our benefits AI is safe? I don't care where the code came from. I care who signs the report and whose ATO it runs under. If Guidehouse's name, insurance and cleared staff stand behind it, fine. But if you lead with 'capstone,' I hear 'unmaintained in 18 months.' And my privacy officer will ask whether students ever touched our data."*
- **Federal CIO (Dana):** *"Capstone means no SBOM, no secure development lifecycle, no FedRAMP. Show me the SBOM, the pen test and the vulnerability-management SLA. If you have those, I'll never mention the university again."*
- **State CTO (Marisol):** *"Honestly, that's a plus with my legislature: the in-state university, workforce pipeline, a good story for the governor. But it's a minus with my CISO. Pitch it as 'co-developed with State U, hardened and supported by Guidehouse.' And if it's built on public money, why isn't it open-source? Then I'm not locked in."*
- **County IT Director (Walt):** *"I don't care who wrote it, as long as it works and someone answers the phone at 2 a.m. when the sheriff's audit is due. Students graduate. Who's supporting it in year three?"*

**Implication:** Don't lead with "capstone" in federal sales. Use it as a *workforce and community* story with states. Every persona converts the question into **"who supports it, and under whose authorization?"**

---

## 5. Contradictions with typical vendor assumptions (for revenue_modeler and cost_and_margin_analyst)

1. **Subscription-first is wrong for federal.** Buyers want a **task order under the $350K SAT**. A managed subscription only follows if the tool runs inside an existing ATO boundary. If the model assumes SaaS subscriptions from year 1, push federal subscription revenue back **12–24 months** for FedRAMP or agency ATO (ESTIMATE). Assume ~30–40% of assessments convert to a subscription, not 70%+ (ESTIMATE).
2. **The red-team harness is episodic, not recurring.** Buyers pay per system at deployment or major change. Recurring portfolio contracts make sense only for agencies with ≥8–10 high-impact cases (perhaps 10–15 federal civilian agencies, ESTIMATE). Annual renewal is roughly 50–60%, not 90% (ESTIMATE).
3. **The conflict-of-interest haircut is real.** Guidehouse's warm accounts (federal health, the Vant4ge justice/HHS clients) are exactly where it is most likely to be the builder or integrator. Remove **30–50% of warm accounts** from the red-team addressable market (ESTIMATE), or price in a separate independent-assurance unit with a firewall.
4. **Synthetic data should be priced near $0 standalone.** Model it as a cost center or bundle enabler, not a revenue line. A revenue line above ~$0.5M/yr by year 3 would contradict buyer behavior (ESTIMATE).
5. **Improper-payment analytics on synthetic data has ~$0 WTP.** Revenue appears only if it moves to real data with the CMS/state Medicaid program side. Different buyer, longer cycle (12–24 months), and a different conflict-of-interest profile.
6. **Dead funding sources:** **TMF** (lapsed, ~$5M) and **SLCGP** (lapsed 30 Sep 2026; ARPA SLFRF spending also ends 2026). Any model that assumes grant-funded state or county uptake in FY27 is optimistic. **Live source:** Medicaid 90/10 and 75/25, but only through the state Medicaid agency.
7. **County deal sizes are tiny ($15–60K)** with 3–9-month cycles. Direct sales cost will exceed gross margin unless deals go through **cooperative contracts, a state-level contract counties can piggyback on, or the Vant4ge channel**. Model counties as a channel or attach segment, not a direct-sales segment.
8. **State AI-law compliance is a weaker driver than vendor decks assume** because of the Dec 2025 preemption EO. State demand is governance-hygiene driven (inventory, review board) and HHS-data-framework driven (IRS 1075, MARS-E), not new-law driven.
9. **The governance mapper competes with free.** That includes GSA/CAIO Council templates, NACo and GovAI Coalition toolkits, the NIST AI RMF Playbook, and generic LLM copilots already licensed. WTP holds only for **maintained, cited, OSCAL/GRC-integrated** output with a human signing it. Price the *signature and the maintenance*, not the RAG.

## 6. Dependencies and flags for other teammates
- **revenue_modeler:** Use the likelihoods and deal ranges above as priors. Federal assessment ~$150–340K. State $100–250K + $75–200K/yr. County $15–60K. Red-team $100–300K per system. Apply the conflict-of-interest haircut in (3).
- **market_and_competition_analyst:** Please verify the county bid thresholds, competitor pricing for red-team services, and whether GSA/CAISI evaluation tooling is available to civilian agencies at no cost.
- **cost_and_margin_analyst:** FedRAMP or agency ATO is a precondition for any federal subscription. GovRAMP for states. Budget the hardening before counting subscription margin.
- **devil_advocate:** The strongest attack is #3 plus #4. The "differentiator" is conflicted exactly where Guidehouse already sells, and the "foundation" has no buyer.

*Unverified items: county bid thresholds; CAIO office staffing; federal IT budget ranges; conflict-of-interest share; all likelihood and WTP figures (ESTIMATE). I did not independently confirm M-25-21's posting status, since one source reports the White House page now returns a 404 while others list it as in force.*
