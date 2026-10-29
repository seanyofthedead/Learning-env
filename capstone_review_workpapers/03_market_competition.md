# 03 — Market & Competition (market_and_competition_analyst)

As of 2026-10-29. "VERIFIED" means a source URL is given. **ESTIMATE** means my judgment, with the assumption stated. Award values come from USAspending `spending_by_award` (API queried 2026-10-29, FY24–FY26 window unless noted). They are *obligated award amounts*, not ceilings, unless I say otherwise. Labor rates come from the GSA CALC+ ceiling-rate API (api.gsa.gov/acquisition/calc/v3, queried 2026-10-29). Those are MAS *ceiling* rates, and actual task-order prices are usually 5–20% lower (**ESTIMATE**).

---

## 0. Bottom line

| Product | Market reality | Recommendation | Why, in one line |
|---|---|---|---|
| 1. Synthetic data generator | Commoditized. Strong free tools exist (Synthea, NeMo Data Designer, MOSTLY AI SDK). Paid licenses that agencies actually buy run about $75K–$150K/yr | **Give away / open-source** the generator. Monetize data packs and services | The no-real-data clause caps fidelity, and free substitutes beat it. Its value is pulling through demos, testing, training and products 2 and 3 |
| 2. Policy-to-AI-governance mapper | Crowded at the platform layer (RegScale, Xacta, ServiceNow IRM, IBM, Credo AI, Paramify). The services layer is fragmented, with $0.3M–$1.7M task orders | **Bundle**: fixed-price assessment plus managed service, delivered *on top of* the client's GRC system of record. Do not sell standalone SaaS | Agencies already pay $0.1M–$4.4M for GRC platforms. What they lack is people who can turn new AI rules into control evidence |
| 3. Agentic AI eval / red-team harness | Open-source baseline (Inspect, garak, PyRIT, Dioptra) plus a government-built baseline (GSA USAi + NIST CAISI). Security vendors are consolidating fast | **Open-source the harness core. Sell recurring assurance as a service** (mission-specific test suites plus audit evidence) | A standalone harness competes with free tools and with GSA. A recurring service attached to agents Guidehouse or Vant4ge deploy is defensible |
| 4. Improper-payment analytics (optional) | Mature, incumbent-heavy (Cotiviti, Noridian, Serco, Northrop FPS, Peraton). **Guidehouse is already a CMS improper-payment incumbent** | **Bundle only** as a proposal and demo sandbox. Do not productize | Payment-integrity buyers pay for accuracy on real claims, which synthetic data cannot prove |

---

## 1. Regulatory demand drivers (and how durable they are)

| Driver | Status (verified) | What it creates demand for | Durability |
|---|---|---|---|
| **OMB M-25-21** (AI use, governance, public trust), 3 Apr 2025 | In force. Requires an annual AI use-case inventory, a public posting, compliance plans, and minimum practices for "high-impact" AI, with **365 days to mitigate or terminate** non-compliant high-impact systems ([JD Supra](https://jdsupra.com/legalnews/new-federal-agency-policies-and-6853165); [OMB 2025 reporting guidance](https://fedscoop.com/wp-content/uploads/sites/5/2026/04/Guidance-on-2025-Agency-Artificial-Intelligence-Reporting-FINAL-3.pdf)) | P2 (inventory, impact assessments), P3 (minimum-practice testing) | **High.** The inventory requirement is also *statutory* (Advancing American AI Act §7225, FY23 NDAA), so it survives memo churn ([cio.gov](https://cio.gov/assets/resources/2024-Guidance-for-AI-Use-Case-Inventories.pdf)) |
| **OMB M-25-22** (AI acquisition) | In force. Contracts must flow down M-25-21 high-impact practices ([JD Supra](https://jdsupra.com/legalnews/new-federal-agency-policies-and-6853165)) | P2 (acquisition-side assessments), P3 (pre-award vendor testing) | Medium-high |
| **OMB M-26-04** (Unbiased AI Principles, implementing EO 14319), Dec 2025 | LLM solicitations after 11 Dec 2025 must include terms on "truth-seeking/ideological neutrality". Agency policy deadline was 11 Mar 2026. **Sunsets 2 years after issuance (~Dec 2027)** unless extended ([whitehouse.gov PDF](https://www.whitehouse.gov/wp-content/uploads/2025/12/M-26-04-Increasing-Public-Trust-in-Artificial-Intelligence-Through-Unbiased-AI-Principles-1.pdf); [Nextgov](https://www.nextgov.com/artificial-intelligence/2025/12/white-house-instructs-agencies-stop-using-biased-ai/410135/)) | P3: the "bias" test suite has to measure *ideological* neutrality, not only demographic bias | **Low-medium.** Built-in sunset. Design the bias module to be configurable to either policy regime |
| Inventory scale | 2025 inventory: **3,611 use cases, 56 agencies, 445 high-impact** (VA has 215) ([Nextgov](https://www.nextgov.com/artificial-intelligence/2026/04/agencies-report-over-3000-ai-use-cases-2025/412898/); [ExecutiveGov](https://executivegov.com/articles/omb-federal-ai-use-cases-2025)) | Sizing for P2/P3. 445 high-impact systems each need testing and documentation | Growing (2,133 in 2024 → 3,611 in 2025) |
| **NIST SP 800-53 AI control overlays (COSAIS)** | Concept paper Aug 2025. Predictive-AI overlay discussion draft Jan 2026. Public draft planned for FY26 ([Campus Technology](https://campustechnology.com/articles/2025/08/19/nist-proposes-new-cybersecurity-guidelines-for-ai-systems.aspx); [CSA](https://cloudsecurityalliance.org/articles/a-look-at-the-new-ai-control-frameworks-from-nist-and-csa)) | **P2's best hook**: a new overlay set has to be mapped onto existing 800-53 baselines and SSPs | High. NIST control work persists across administrations |
| FedRAMP 20x / GovRAMP (ex-StateRAMP, rebranded Feb 2025) | FedRAMP 20x is live (Paramify is authorized on 20x) ([Carahsoft/Paramify](https://www.carahsoft.com/paramify)). StateRAMP now operates as "GovRAMP" ([GovRAMP](https://govramp.org/blog/stateramp-announces-rebrand-to-govramp-reflecting-mission-to-unite-public-and-private-sectors-in-advancing-cybersecurity/)) | P2 must say "GovRAMP", not "StateRAMP". 20x lowers the ATO barrier for any SaaS Guidehouse hosts | High |
| **State laws** | Texas TRAIGA (HB 149) has applied to state and local government entities since **1 Jan 2026**, with a NIST AI RMF safe harbor ([Ropes & Gray](https://www.ropesgray.com/en/insights/alerts/2025/06/navigating-traiga-texas-new-ai-compliance-framework)). Colorado AI Act is delayed to 30 Jun 2026 and under litigation (xAI suit). The Dec 2025 EO set up a DOJ AI Litigation Task Force (est. 9 Jan 2026) to challenge state AI laws ([Introl](https://introl.com/blog/trump-ai-preemption-executive-order-state-laws-2026); [Kelley Drye](https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/new-executive-order-targets-state-ai-laws-states-show-no-signs-of-backing-down)) | P2 state SKUs (the NIST AI RMF safe harbor is a selling point), P3 for state benefits/justice AI | **Medium, contested.** Federal preemption pressure targets *private-sector* AI rules most. A state's rules for *its own* agencies' AI use are the least exposed (**ESTIMATE**) |
| UK | ATRS is **mandatory** for central government departments and for ALBs that serve the public ([GOV.UK](https://gov.uk/government/publications/algorithmic-transparency-recording-standard-mandatory-scope-and-exemptions-policy/algorithmic-transparency-recording-standard-atrs-mandatory-scope-and-exemptions-policy)). Compliance has historically been weak (9 of 75 known algorithms recorded per [Public Law Project](https://publiclawproject.org.uk/resources/around-the-world-in-ai-regulation-how-the-uk-can-become-a-leader-in-transparency/), an older figure) | P2 UK SKU: an ATRS record generator plus an inventory | Medium-high |

**Net demand view:** demand for *inventory, mapping and testing* is durable because it has a statutory floor (§7225), NIST control work behind it, and continuous ATO. The specific *content* of bias and impact tests is policy-volatile (M-24-10 → M-25-21 → M-26-04 in 20 months). So the products must be **rule-pack driven**, with policy content updated as a managed service. That volatility is exactly what justifies a subscription.

---

## 2. Product 1: Synthetic public-sector data generator

### 2.1 Alternatives (verified current status)

| Alternative | Type | What it does now | Source |
|---|---|---|---|
| **Synthea** (MITRE) | GOTS-like OSS, Apache-2.0 | Synthetic patient/EHR records (FHIR, C-CDA). Pre-generated 1M-patient populations, output in the public domain | [GitHub wiki](https://github.com/synthetichealth/synthea/wiki/DPG) |
| **NVIDIA NeMo Data Designer** | OSS, Apache-2.0, about 2.4k stars | Generates synthetic datasets from scratch or from seed data, with samplers, LLM columns and validators. NVIDIA bought **Gretel** in Mar 2025 (reported nine figures, above its $320M valuation) | [GitHub](https://github.com/NVIDIA-NeMo/DataDesigner); [TechCrunch](https://techcrunch.com/2025/03/19/nvidia-reportedly-acquires-synthetic-data-startup-gretel) |
| **MOSTLY AI SDK** | OSS, Apache-2.0 (Feb 2025) plus a commercial platform | Tabular and relational synthetic data, runs locally for free | [insideHPC](https://insidehpc.com/2025/02/mostly-ai-releases-open-source-toolkit-for-synthetic-data-creation/) |
| **SDV (DataCebo)** | Source-available (BSL, converts to MIT after 4 yrs) | Tabular, relational and time-series synthesizers. Production use is restricted | [The New Stack](https://thenewstack.io/whats-next-for-companies-built-on-open-source/) |
| **Tonic.ai** (Fabricate / Structural / Textual) | Commercial | Fabricate is an agentic, prompt-driven generator of referentially intact databases. Since Sep 2026 Carahsoft has been its master government aggregator, with access via **SEWP V**. No FedRAMP found | [Carahsoft](https://www.carahsoft.com/news/tonicai-and-carahsoft-partner-to-bring-ai-native-synthetic-data-to-the-public-sector-2026) |
| Defense SBIR shops (Intelligent Payload "Data Forge", Carley, IvySys) | Commercial R&D | Domain-specific synthetic data, mostly sensor and imagery | USAspending (below) |

**Gap no one fills:** none of these ships *ready-made public-sector schemas* that are realistic. That means benefits eligibility (SNAP/TANF/Medicaid household composition and churn), permit workflows, court and corrections case histories (which line up with the Vant4ge domain), and Medicaid/Medicare claims with embedded improper-payment patterns. Synthea covers clinical data, not program operations.

### 2.2 What agencies pay (VERIFIED, USAspending)

| Award | Buyer | Amount | What |
|---|---|---|---|
| 15JUST24P00000068 (via Carahsoft) | DOJ Offices, Boards & Divisions, Oct 2024 | **$148,387** | Gretel Enterprise tier subscription plus enterprise worker containers |
| FA864925P0018 | Air Force, Jan 2025 | **$74,249** | Tonic.ai: de-identifying PII for LLM/RAG |
| 70RSAT26C00000029 | DHS S&T, Sep 2026 | **$583,817** | Cignal: synthetic data generation for property and passenger screening |
| W5170125CA086 | Army, Jul 2025 | **$1,001,782** | Data Forge synthetic data platform (SBIR II) |
| FA875026CB029 | Air Force, Jun 2026 | **$1,249,969** | Carley: scenario and synthetic data generation (SBIR D2P2) |
| 1333BJ19P00280003 | USPTO, 2019 | $1,608,923 | Test data management software |

**Market price range for the revenue model:**
- COTS synthetic-data license: **$75K–$150K/yr per agency program** (2 verified points).
- Custom domain generator built as R&D: **$0.6M–$1.25M per effort** (verified SBIR/DHS points, defense-heavy).
- Civilian HHS/benefits buyers rarely buy synthetic data as a line item. It comes embedded in modernization and testing task orders (**ESTIMATE**: in the USAspending keyword search, 0 of the top 10 "synthetic data" awards came from civilian benefits agencies).

### 2.3 Vehicles
GSA MAS SIN 511210 (software) through a reseller, 54151S (IT professional services), SEWP (Tonic's route, now being transferred to GSA per [FNN](https://federalnewsnetwork.com/acquisition-policy/2025/05/gsa-in-negotiations-with-nasa-to-take-over-sewp-contract)). UK TS4 Lot 5/5a (Application & Data Management).

### 2.4 Recommendation: **GIVE AWAY / OPEN-SOURCE** (Apache-2.0 "Guidehouse Public Sector Synthetic Data Kit")
- At $0 it beats the price of NeMo, MOSTLY or Synthea. As a paid product it would compete with free tools on an untested fidelity claim. Because of the no-real-data clause, the generator can't be calibrated to real distributions without a later client data-use agreement, so its "realism" rests on published statistics only.
- The kit's value is as an internal and external accelerator: demo data for every P2/P3/Vant4ge pitch, test data for 508 and security testing, and the training corpus for P3 test suites.
- Monetizable layer (**ESTIMATE**): (a) custom calibrated packs built under a client DUA, priced at **$50K–$150K** per pack; (b) a test-data-as-a-service line inside modernization task orders. Do **not** put a standalone license price in the revenue model. The model should carry revenue of $0 plus an influence/attach metric.
- Open-sourcing also fits university publication norms and builds credibility (GitHub stars, citations). Confirm the IP assignment allows Guidehouse to relicense.

---

## 3. Product 2: Policy-to-AI-governance mapper (lead product)

### 3.1 Alternatives (verified)

| Vendor | Position now | Federal footprint (verified) |
|---|---|---|
| **RegScale** | CCM/GRC platform with AI-assisted control mapping. **FedRAMP High**, $30M Series B, contributor to FedRAMP 20x ([Carahsoft](https://www.carahsoft.com/regscale)) | Navy $4.35M (enterprise, all modules, 2024); DOE BPA call $3.0M (Dec 2025); USPTO $2.40M (Mar 2026); DOL "GRC platform RegScale or equivalent" $0.86M (Sep 2026); AF renewals $175K–$190K |
| **Paramify** | Described as the first GRC platform authorized on FedRAMP 20x; $12M Series A in Dec 2025 ([Carahsoft](https://www.carahsoft.com/paramify); [TechBuzz](https://www.techbuzznews.com/paramify-raises-12-million-series-a-after-fedramp-overhaul-forces-strategic-pivot/)) | NEA $105K (May 2026); NEH $95.5K (Mar 2026) |
| **Telos Xacta** | Incumbent A&A/RMF tool | FBI $2.87M (Sep 2026); AF $3.44M (Jun 2026); State "system inventory & risk mgmt" $654K (Oct 2026); SSA $954K |
| **ServiceNow IRM** | Enterprise GRC | DISA $2.0M (Jun 2026); Navy $2.34M |
| **IBM watsonx.governance** (+ Credo AI policy packs via OEM, Apr 2025) | AI governance on FedRAMP-authorized infrastructure ([BusinessWire](https://www.businesswire.com/news/home/20250428912812/en/Credo-AI-IBM-Collaborate-to-Advance-AI-Compliance-for-Global-Enterprises)) | **Treasury, "AI governance platform – AI use case management tool," $308,796 (2099AC26F00073, 30 Sep 2026)** |
| **Credo AI** | AI governance and inventory. Partnered with **Booz Allen** on an "AI Inventory Jumpstart" for OMB compliance, which is the closest analog to Guidehouse's plan ([Credo AI blog](https://www.credo.ai/blog/credo-ai-and-booz-allen-transforming-ai-governance-for-federal-agencies)) | Army SBIR DP2 $2.0M (Sep 2025) |
| **OneTrust** | Privacy/AI governance. Custom-quoted | FHWA $174.5K (2020, privacy) |

### 3.2 What agencies pay for AI-governance *services* (VERIFIED, USAspending)

| Award | Buyer | Amount | Scope |
|---|---|---|---|
| 1331L526F13OS1319 (Four Points) | Commerce OS, Sep 2026 | $1.74M | Oracle cloud plus enterprise AI governance, strategy and assurance |
| 693KA926F00123 (EY) | FAA, Sep 2026 | $1.17M | ADO AI governance support |
| 75FCMC26F0127 (Tech2i) | **CMS**, Aug 2026 | $1.07M | Data and AI governance, standards, DUAs |
| 1333ND23FNB770397 (MITRE) | NIST, 2023 | $1.06M | AI RMF support |
| 1333ND25FNB770143 / -0132 / 26FNB770011 | NIST, 2025–26 | $268K–$389K each | AI RMF catalog and governance structures |
| 49100426F0196 (NAPA) | NSF OIG, Sep 2026 | $348K | OIG AI governance services |

**GSA CALC ceiling rates (VERIFIED, 2026-10-29):** "AI Governance" labor categories $160–$204/hr (n=5); "Responsible AI" $177–$354/hr (median $281, n=10); "AI Specialist" median $199 (n=20); "AI Architect" median $189 (n=16); "Data Scientist" p25/median/p75 = $138/$169/$205 (n=1,520).

**Market price ranges for the revenue model:**
- AI-governance/inventory **software** at bureau level: **$100K–$310K/yr** (Paramify, IBM at Treasury). Enterprise GRC: **$0.9M–$4.4M** per order.
- AI-governance **advisory** task order: **$0.27M–$1.7M**, with the median verified point at about **$1.06M**. FAA, CMS and Commerce are the 2026 civilian comparables.
- **ESTIMATE, recommended Guidehouse price points:**
  - Fixed-price "AI Inventory & Gap Assessment," 8–12 weeks: **$150K–$350K**. Assumption: 3–5 FTE at about $175/hr for 10 weeks is roughly $210K–$350K.
  - Managed service: **$250K–$600K/yr** per agency. Covers annual inventory refresh, monitoring for new rules (COSAIS, M-26-xx, GovRAMP), impact assessments for up to about 10 high-impact use cases, and OSCAL export.
  - State: **$75K–$200K** assessment, **$100K–$250K/yr** managed.

### 3.3 Vehicles
- **GSA MAS**: SIN 541611 (management consulting, which is where "AI Governance Lead" LCATs sit today), 54151S (IT professional services), 518210C (cloud and cloud-related IT professional services, for a hosted SaaS), 511210 (license). Guidehouse already wins CMS work on MAS (see §5).
- **OASIS+**: Guidehouse holds contract 47QRCA25DU150 through 18 Dec 2034 ([Guidehouse](https://guidehouse.com/government-contract-vehicles/oasis-plus)). The specific domains are not verified here. Management & Advisory and Technical & Engineering domains would carry the assessment.
- **CIO-SP4: DEAD.** NITAAC cancelled it on 30 Jan 2026 with no award, and NITAAC GWACs sunset 29 Oct 2026 ([ExecutiveGov](https://www.executivegov.com/articles/nitaac-cio-sp4-cancellation); [itpfed](https://itpfed.com/why-nitaac-pulled-the-plug-on-cio-sp4-and-what-it-means-for-federal-it-contracting)). **Drop it from the plan.** Reports conflict on whether a CIO-SP3 bridge into GSA runs to Apr 2027. Alliant 3 is upcoming (unverified).
- **State**: NASPO ValuePoint Cloud & Software Solutions (2026 awards; 58 of about 300 bidders; 10-yr term) for SaaS via a reseller ([GlobeNewswire](https://www.globenewswire.com/news-release/2026/01/07/3214571/0/en/Four-Inc-Awarded-NASPO-ValuePoint-Cloud-and-Software-Solutions-Master-Agreement.html)). State IT consulting MSAs such as Illinois PASS / IT RAC (May 2026) and NY OGS (Jul 2026) ([SamSearch](https://samsearch.co/gov-explore/sled/naspo-valuepoint-procurement-assistance-and-support-services-statewide/2136707)). The NASPO ITMSP price list 24-15 expires 31 Oct 2026 and won't be replaced ([Hawaii SPO](https://spo.hawaii.gov/wp-content/uploads/2026/07/Price-List-24-15-A-Notice-signed-07.07.26-Remediated.pdf)). Texas DIR and California CMAS/SLP are likely routes (**not verified**).
- **UK TS4 (RM6190, now run by GCA since 1 Apr 2026)**: **Lot 1 (Technology & Digital Consultancy)** for the assessment and ATRS work; **Lot 5/5a (Application & Data Management)** for the managed service ([Insight](https://uk.insight.com/en_GB/about/newsroom/press-releases/2026/insight-named-as-supplier-on-all-lots-of-crown-commercial-service-s-technology-services-4-framework.html); [GCA](https://www.gca.gov.uk/agreements/RM6190)). Lot 6 expires 11 Jun 2028.

### 3.4 Recommendation: **BUNDLE** (assessment plus managed service). No standalone SaaS SKU
- Every verified platform buyer (Navy, DOE, USPTO, DOL, FBI, DISA, Treasury) already owns a GRC or AI-governance system of record. A seventh tool loses the procurement. Credo AI with Booz Allen already offers the "inventory jumpstart" bundle.
- Position the RAG mapper as **Guidehouse's delivery engine**. It should output OSCAL/CSV into RegScale, Xacta, ServiceNow, watsonx or Paramify ("bring your own GRC"). Partnering with RegScale and Paramify, which have no service arm, is better than competing with them.
- The tool's lead is real but narrow. No competitor verifiably maps **CJIS + HIPAA + GovRAMP + M-25-21/M-26-04 + COSAIS** together for *state health, human services and justice agencies*. That niche is the Vant4ge footprint.
- Keep the tool internal, hosted in Guidehouse's FedRAMP/GovRAMP boundary, or delivered as a client-side deployment. That avoids a 12–18-month FedRAMP path for a product priced in the low six figures.

---

## 4. Product 3: Agentic AI evaluation & red-team harness

### 4.1 Alternatives (verified)

| Alternative | Type | Status now | Source |
|---|---|---|---|
| **Inspect** (UK AI Security Institute) | OSS, MIT, 3.1k stars | LLM eval framework with tool use, multi-turn dialog and 200+ pre-built evals. A de facto standard among AISIs | [GitHub](https://github.com/UKGovernmentBEIS/inspect_ai) |
| **garak** (NVIDIA) | OSS, Apache-2.0, 9.8k stars | LLM vulnerability scanner | [GitHub](https://github.com/NVIDIA/garak) |
| **PyRIT** (Microsoft) | OSS, MIT | Multi-turn gen-AI red-teaming orchestration. The repo moved to microsoft/PyRIT (old Azure repo archived Mar 2026) | [GitHub](https://github.com/Azure/PyRIT) |
| **NIST Dioptra** | GOTS/OSS | Reproducible AI test platform that supports the AI RMF "Measure" function | [NIST](https://pages.nist.gov/dioptra/) |
| **GSA USAi + NIST CAISI** | Government-built | USAi gen-AI evaluation suite launched Aug 2025. GSA–CAISI MOU (Mar 2026) to standardize evaluation of AI tools for federal use. GSA has its own red-team method | [GSA](https://www.gsa.gov/about-us/newsroom/news-releases/gsa-launches-usai-to-advance-white-house-americas-ai-action-plan-08142025); [ExecutiveGov](https://www.executivegov.com/articles/gsa-caisi-usai-federal-evaluation); [FedScoop](https://fedscoop.com/government-coders-ai-models-grok-output-hate-speech/) |
| ViolentUTF | Gov-employee-built wrapper over PyRIT and garak | Used to red-team "a US Government flagship LLM application" | [arXiv 2504.10603](https://arxiv.org/html/2504.10603v2) |
| **Scale AI** | Commercial T&E | CDAO T&E partner since 2024; enterprise agreement raised from $100M to **$500M** potential value | [Scale](https://scale.com/blog/Scale-ai-pentagon-cdao-500-million-agreement); [DefenseScoop](https://defensescoop.com/2024/02/20/scale-ai-pentagon-testing-evaluating-large-language-models/) |
| **HiddenLayer** | Commercial AI security | $100M Series B (Sep 2026), Tradewinds awardable (Jun 2026), MDA SHIELD, DOE Prometheus | [Unite.AI](https://www.unite.ai/hiddenlayer-raises-100m-series-b-to-expand-ai-agent-security-platform/) |
| **Cisco AI Defense** (Robust Intelligence, est. ~$350M) / **Check Point** (Lakera, closed Oct 2025, ~$201.8M per 20-F) / **Palo Alto Prisma AIRS** (Protect AI) | Big-security consolidation | Runtime guardrails plus automated red-teaming bundled into firewall/SASE estates | [SEC 20-F](https://www.sec.gov/Archives/edgar/data/0001015922/000117891326001932/zk2634942.htm); [Dark Reading](https://www.darkreading.com/cyber-risk/check-point-cisco-boost-ai-investments-with-latest-deals) |

### 4.2 What agencies pay (VERIFIED, USAspending)

| Award | Buyer | Amount | Scope |
|---|---|---|---|
| 1333ND24FNB770022 (Strativia) | NIST, Jan 2024 | $109,908 | AI red-teaming planning and development |
| N0002426F8020 (JHU APL) | USMC TECOM, Feb 2026 | $500,000 | LLM AI assurance testing |
| HQ003424F0535 (UMD) | WHS/DoD, Sep 2024 | $795,340 | AI assurance support services |
| 75N98024F00195 (MITRE) | NIH ODSS, Jun 2024 | $1,827,677 | AI Assurance Lab (tools to test AI systems) |
| FA864924P0543 (HiddenLayer) | Air Force, Feb 2024 | $1,799,680 | ML security attack workbench for red-teaming autonomy |
| Scale AI / CDAO | DoD | up to $500M (ceiling) | Enterprise T&E |

CALC ceiling rates: "Red Team" LCATs $88–$153/hr (n=4); "Penetration Tester" p25/median/p75 = $126/$157/$196 (n=437); "AI Engineer" median $175 (n=83); "Machine Learning Engineer" median $170 (n=62).

**Market price ranges for the revenue model:**
- One-off AI red-team or assurance engagement: **$110K–$800K**.
- Programmatic assurance lab: **$0.8M–$1.8M/yr**.
- Commercial AI-security platform license (**ESTIMATE**, no public federal price lists found): $100K–$500K/yr, increasingly bundled at no extra cost by Cisco, Palo Alto and Check Point.
- **ESTIMATE, recommended Guidehouse price points:**
  - "Pre-deployment assurance sprint" per agent: **$75K–$150K** (4–6 weeks).
  - "Continuous assurance" subscription: **$120K–$300K/yr** per agent or system. Covers quarterly red-team runs, regression on every model or prompt change, an M-25-21 minimum-practice evidence pack, and M-26-04 neutrality tests.
  - Portfolio tier for agencies with 5 or more high-impact systems: **$0.6M–$1.2M/yr**.

### 4.3 Vehicles
- **CDAO AI T&E BPA** (Tradewinds/ACC-RI): **79 holders**, including Booz Allen, Accenture Federal, Leidos, IBM, EY, CACI and Scale. No ordering fee ([Sweetspot](https://www.sweetspot.so/markets/federal/vehicles/ai-test-and-evaluation/)). **Whether Guidehouse is a holder is not verified. If it isn't, that is a gap for DoD and DHA health work.** The Tradewinds Solutions Marketplace is the on-ramp.
- GSA MAS 54151HACS (Highly Adaptive Cybersecurity Services) for the red-team framing, and 54151S. OASIS+.
- State: same as P2. Federal-health and Vant4ge state HHS/justice deals carry it as a task line.
- UK TS4 **Lot 1** (assurance consultancy) and **Lot 5/5a** (operating the harness). Note that UK AISI's Inspect is the home-market standard there, so build on Inspect.

### 4.4 Recommendation: **OPEN-SOURCE THE HARNESS CORE. SELL RECURRING ASSURANCE (bundled)**
- The baseline harness is free (Inspect, garak, PyRIT, Dioptra). The federal civilian baseline is being standardized by GSA and CAISI inside USAi. Endpoint and runtime security is being absorbed by Cisco, Palo Alto and Check Point. A standalone harness license has **no viable price point** (**ESTIMATE**).
- **What's defensible:** (1) **mission-specific test suites**, such as benefits-eligibility agents (wrongful denial, disparate impact), Medicaid/claims agents, and corrections/court case-management agents, all running on P1 synthetic records; (2) **audit-ready evidence** that maps automatically into P2's control and inventory outputs; (3) **agentic** tests (tool misuse, privilege escalation across case-management APIs), which the OSS tools cover only thinly.
- Build it as Inspect-compatible plugins. Publishing the core lifts credibility with CAISI and GSA and lets agencies insist on it in RFPs. Revenue comes from the recurring service.
- Attach rule: every Guidehouse- or Vant4ge-delivered AI agent ships with a 12-month continuous-assurance line item. That is where the attach-rate assumption should come from, rather than from cold standalone sales.

---

## 5. Optional Product 4: Improper-payment analytics on synthetic claims

**Guidehouse is already an incumbent (VERIFIED):** CMS FEIPM/SEIPM Review Contractor **75FCMC26F0099**, **$63.9M TCV**, 4.5 yrs, awarded Jun 2026 on **GSA MAS GS00F045DA** ([OrangeSlices](https://orangeslices.ai/guidehouse-secures-64m-cms-federal-and-state-exchange-improper-payment-measurement-rc-support-contract/)). The predecessor was 75FCMC23F0123 at $28.7M. Guidehouse also has NASA PIIA/management-controls work ($0.8M–$1.8M/yr).

| Competitor / program | Verified amount |
|---|---|
| Noridian: lower improper payment rates (CMS) | $407.4M (2018) |
| Empower AI: CERT | $230.2M (2016) |
| Northrop-led FPS modernization | $91.6M potential, 5-yr ([Healthcare Finance](https://www.healthcarefinancenews.com/news/cms-selects-northrop-grumman-implement-fraud-prevention-system)) |
| Serco: CERT | $26.2M (Nov 2025) |
| Cotiviti: RAC Regions 3/5 and others | $3.9M–$10.6M each (May 2025); HCV $38.6M |
| CMS claims modernization with "real-time fraud review tools" | HealthEdge $1.1B ceiling vs Peraton $825M ceiling ([Nextgov](https://www.nextgov.com/digital-government/2026/09/cms-eyes-new-technologies-reduce-improper-payments-and-fraud/416286/)) |
| CMS Fraud Defense Operations Center (in-house AI, since Mar 2025) | ~$2.5B in payments stopped (same Nextgov source) |

**Recommendation: BUNDLE only, as a demo and model-development sandbox.** Buyers here (CMS CPI, state Medicaid PI units) pay for detection accuracy on real claims, which synthetic data can't prove. The large commercial PI vendors (Cotiviti; Optum, Gainwell and Conduent at state level, from my knowledge and **not verified** here) own production analytics. Use synthetic claims to (a) demo in FPS 2.0, CERT and state Medicaid PI recompetes, (b) train analysts, and (c) prototype models before a DUA. Revenue model: $0 direct, with win-probability uplift on recompetes (**ESTIMATE** +2–5 pts).

---

## 6. Price-range reconciliation table (for revenue_modeler)

| Item | Verified market range | Recommended Guidehouse price (ESTIMATE) | Basis |
|---|---|---|---|
| P1 synthetic-data COTS license | $74K–$148K/yr | $0 (OSS); custom calibrated pack $50K–$150K | DOJ/Gretel, AF/Tonic |
| P1 custom generator R&D | $0.58M–$1.25M | not pursued standalone | DHS, Army, AF SBIR |
| P2 AI-gov software, bureau level | $95K–$309K/yr | not sold standalone | NEH/NEA Paramify; Treasury/IBM |
| P2 enterprise GRC | $0.86M–$4.35M | partner, don't compete | RegScale, Xacta, ServiceNow awards |
| P2 AI-gov advisory TO | $0.27M–$1.74M | Assessment $150K–$350K; managed $250K–$600K/yr (federal); state $75K–$250K | FAA/EY, CMS/Tech2i, Commerce, NIST |
| P3 red-team / assurance engagement | $110K–$800K | Sprint $75K–$150K/agent; continuous $120K–$300K/yr/agent; portfolio $0.6M–$1.2M/yr | NIST/Strativia, USMC/APL, WHS/UMD |
| P3 assurance lab / platform | $0.8M–$1.8M; Scale CDAO up to $500M ceiling | — | MITRE/NIH, HiddenLayer/AF |
| P4 improper-payment contracts | $4M–$407M | $0 direct (bundled) | CMS awards above |
| Labor (CALC ceiling) | AI Governance $160–$204/hr; Responsible AI median $281/hr; Data Scientist median $169/hr; AI Engineer median $175/hr; Pen Tester median $157/hr | Blended about $175/hr for builds | CALC API 2026-10-29 |

If revenue_modeler's P2 subscription exceeds about $600K/yr per agency, or P3 exceeds about $300K/yr per system, the assumption needs a named comparable. The verified ceiling for *services-only* AI-governance task orders is about $1.7M total, and that one is bundled with cloud.

---

## 7. Competitive gaps Guidehouse can own

1. **State HHS and justice AI governance bundled with case management (Vant4ge, announced 7 Apr 2026)** ([Vant4ge release](https://lifestyle.q923radio.com/story/157747/vant4ge-partners-with-guidehouse-to-advance-ai-enabled-solutions-for-public-safety-and-human-services-2/)). No GRC vendor ships CJIS + HIPAA + GovRAMP + TRAIGA/state rule packs alongside a case-management platform. Each Vant4gePoint deployment should carry a P2 assessment plus a P3 continuous-assurance line.
2. **Federal health incumbency.** Guidehouse holds CMS improper-payment measurement work ($63.9M), and CMS bought a $1.07M data and AI governance TO in Aug 2026 from someone else (Tech2i). HHS reported the most use cases (447 per one source) and VA the most high-impact (215). Target HHS, VA and DHA for P2/P3.
3. **AI Readiness Maturity Model → inventory → controls → testing as one evidence chain.** Competitors offer pieces: Credo/Booz Allen do inventory, RegScale does controls, Scale and HiddenLayer do testing. A single chain from maturity score to OMB inventory to COSAIS-mapped controls to red-team evidence is not offered by any one verified competitor.
4. **UK TS4 on all six lots.** ATRS is mandatory, compliance is weak, and Inspect is the UK standard. A "P2 ATRS + P3 on Inspect" offer fits Lot 1 and Lot 5 with little localization. TS4 runs to at least Jun 2028 (Lot 6).
5. **Public-sector synthetic data commons.** Nobody publishes realistic open benefits, permit, court or claims datasets. An OSS kit makes Guidehouse the default demo and test data source, the way Synthea did for MITRE in health IT.

## 8. Risks / contestable assumptions
- **Government-built baseline:** GSA USAi + CAISI may become the mandated federal evaluation path. P3 has to plug into it, not compete with it.
- **Policy volatility:** M-26-04 sunsets around Dec 2027. Bias test content changed twice in 20 months.
- **Vehicle gaps:** Guidehouse's OASIS+ domains and CDAO T&E BPA status are unverified. CIO-SP4 is gone.
- **Consolidation:** Big-security vendors bundle AI red-teaming into existing ELAs at near-zero marginal price, which compresses any standalone P3 price.
- **GSA price pressure:** OneGov set an anchor of "$1 per agency" for frontier AI in 2025 (now extended or rewritten) ([FedScoop](https://fedscoop.com/gsa-onegov-ai-deals-some-extensions-new-offers/)). Buyers expect software to be cheap and pay for labor and outcomes. That supports bundling.
