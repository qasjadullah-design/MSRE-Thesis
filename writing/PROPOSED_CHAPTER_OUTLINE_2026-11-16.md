> **ARCHIVED DRAFT / STUDENT-APPROVED 16 NOV 2026.** Statements below saying 'proposed' or 'not approved' describe the file's historical state prior to user approval. Current authoritative instructions: [Working Scope](https://github.com/qasjadullah-design/MSRE-Thesis/blob/main/governance/APPROVED_WORKING_SCOPE_2026-11-16.md), [Model Design v0.2](https://github.com/qasjadullah-design/MSRE-Thesis/blob/main/docs/MODEL_DESIGN.md), and [Chapter Outline](https://github.com/qasjadullah-design/MSRE-Thesis/blob/main/writing/CHAPTER_OUTLINE.md). Supervisor/university signoff remains unverified.

# PROPOSED THESIS CHAPTER OUTLINE — NOT APPROVED
**Prepared 16 November 2026** for Section 0.2 of [SCOPE_REFOCUS_2026-11-16](https://github.com/qasjadullah-design/MSRE-Thesis/blob/proposal/scope-refocus-2026-11-16/governance/proposals/SCOPE_REFOCUS_2026-11-16.md). **No changes to official TH-1 title, three objectives or six working milestone dates.**
    
## Page budget
Target **94 pages of main body**, excluding preliminary pages, references, code, full regulatory tables and appendices. This is a planning budget, not a university-imposed length or supervisor approval.

| Chapter | Title | Target pages | Primary literature-matrix IDs | Research role |
|---|---|---:|---|---|
| 1 | Introduction | 8 | L13, L18, L19, L24, L25 | Explain large-load challenge, problem statement, approved objectives, proposed focused question, scope and contribution |
| 2 | Regulatory and theoretical background | 14 | L07, L20, L21, L22, L23, L14; **T01 new** | FERC/PJM co-location classes, broader large-load track, BTMG, pricing/priority theory, comparisons and legal status |
| 3 | Technical literature review and research gap | 17 | L01–L05, L08, L14–L17, L25–L27, L29 | Flexibility evidence, system-cost and emissions literature, ratepayer cost methods, gap synthesis |
| 4 | Methods and optimization framework | 20 | L12, L28, L02, L07, L20–L22, L25 | PJM regional testbed, modular PyPSA-USA extension, service rules, site accounting, scenario design and validation |
| 5 | Data, evidence and calibration | 9 | L03–L05, L08, L18, L19, L22, L23; Parameter Harvest P01–P16 | Source/dataset inventory, observed vs derived vs assumed, transferable flexibility bounds, uncertainty |
| 6 | Model results | 17 | **Simulation outputs, not pre-existing sources**; L01, L16, L25 as comparators | Toy tests; firm benchmark; curtailment-cost frontier; zonal/scale sensitivities; interim bridge; reliability proxy; CO2; allocation bookends |
| 7 | Discussion, regulatory implications and limitations | 6 | L07, L14–L17, L20–L23, L26–L27 | Interpretation, realism of curtailment, cost incidence, model limits, potential relevance to Pakistan |
| 8 | Conclusions and further research | 3 | Synthesizes results and all three objectives | Answers the actual questions, evaluates contribution and identifies valid extensions |
| | **TOTAL** | **94** | | |

## Proposed section-by-section skeleton with pages
**Chapter 1 (8 pp)** — 1.1 Data-center demand growth and U.S. electricity system (2 pp; L18/L19/L24); 1.2 PJM problem and contract motivation (2; L13/L20/L21/L25); 1.3 research question and three unchanged TH-1 objectives (1); 1.4 claimed contribution and evaluation outcomes (1); 1.5 scope boundaries and organization (2). Avoid treating proposed regulatory classes or forecast load as already operated demand.

**Chapter 2 (14 pp)** — 2.1 Existing electricity access and planning concepts (2; L07); 2.2 FERC co-location proceeding and definitions (3; L20/L21); 2.3 FCD, NFCD and interim NITS service rights/transition (3; L20–L22); 2.4 PJM broader large-load proposals and difference from co-location (2; L18/L22, verify primary status); 2.5 Texas SB6 as a jurisdiction-specific *evidence source* rather than a PJM tariff (1; L23); 2.6 economic rationale for priority service, insurance and capacity investment (2; T01); 2.7 verified regulatory implications and unsettled points (1). Do not assume 2025 order's initial tariff provisions survived 2026 rehearing unchanged.

**Chapter 3 (17 pp)** — 3.1 Flexibility classes and actual/assumed operating envelopes (5; L03–L05/L08); 3.2 mathematical modeling of flexible large loads and system cost (4; L01/L02/L25); 3.3 research on emissions, adequacy/reliability and operational risk (3; L01/L06/L26/L27); 3.4 ratepayer-incidence and cost-causation methods (3; L14–L17); 3.5 comparison matrix, gap assessment and research hypotheses (2; L07/L20–L22/L29). Record which papers have been read in full before describing an absence of research as established fact.

**Chapter 4 (20 pp)** — 4.1 choice/limitations of a 22-zone PJM-relevant extraction (3; L12/L28, TH-003); 4.2 network input, capacities, time horizon and boundary assumptions (3); 4.3 site-bus/POI and physical electricity balance (3); 4.4 firm/nonfirm/interim regulatory constraints (5; L20–L22); 4.5 curtailment tolerance/energy and priority-service computation (2; L02/T01); 4.6 gross system cost vs tariff/incumbent-allocation bookends (2; L14–L17); 4.7 scenario matrix, solver and acceptance tests (2). Crucial: ε=0 is not, by itself, a legal firm-service contract; preserve entitlement/planning and priority distinctions. Interim post-upgrade is full NITS, not FCD.

**Chapter 5 (9 pp)** — 5.1 raw data and provenance (2; L18/L19/L28); 5.2 parameter mapping P01–P16 and missing data (3); 5.3 observed/derived/assumed physical-flexibility cases (2; L03–L05/L08); 5.4 calibration limitations and transferability of Texas evidence to PJM (1; L23); 5.5 preprocessing and independent data QA (1). Objective 2 explicitly says observed calibration; if only bounds are feasible, obtain supervisor acceptance before presenting objective met.

**Chapter 6 (17 pp)** — 6.1 solver/reproducibility and toy-model tests (2); 6.2 baseline firm scenario and dispatch-cost/deployment implications (3); 6.3 *proposed* annual curtailment-energy tolerance sweep and cost curve (4); 6.4 three-zone and at-scale sensitivities (3); 6.5 interim pre/post upgrade difference (2); 6.6 emissions/unserved-firm-energy outcomes (1); 6.7 incumbent cost allocation A/B with separate transfers (2). Report the modeled total/annual periods and avoid calling energy-curtailment tolerance the complete service-class definition.

**Chapter 7 (6 pp)** — 7.1 what costs really change and what does not (2); 7.2 interpretation under actual FERC/PJM constraints (1; L20–L22); 7.3 potential transferability to Pakistan (1; no Pakistan simulation); 7.4 limitations of zonal deterministic modeling and data availability (2).

**Chapter 8 (3 pp)** — 8.1 answers to TH-1 objective 1, 2, 3 (2); 8.2 limitations, replicability and publication extensions (1).

## New theory source to add
**T01 — Chao, Hung-po and Robert Wilson (1987), “Priority Service: Pricing, Investment, and Market Organization,” American Economic Review 77(5):899–916.** Bibliographic details verified at https://ideas.repec.org/a/aea/aecrev/v77y1987i5p899-916.html. **Full paper's detailed propositions not yet extracted; it must be added to the source register after source-level verification.** Do not equate a social avoided-cost frontier with an existing FERC/PJM retail tariff.

## Evidence and writing controls
- Matrix IDs refer to the **12 November 2026 screening workbook** in Drive, not a fully verified systematic review. “NR” does not establish a method absent from a paper.
- Chapter source tables should retain DOI/link, study method, grid level, flexibility mechanism, actual measured vs simulated behavior, outputs, assumptions and limitations.
- Regulatory status must be checked from primary FERC/PJM filings with effective dates.
- Any result tables/figures are placeholders pending actual reproducible model solves.
- User/supervisor decisions S1–S5, including co-location and acceptable proxies, remain open. Do not revise TH-1 language or deadlines.

## Proposed writing sequence (internal only)
First complete Ch.2–3 with source verification by 31-Dec-2026 literature milestone; data table for Ch.5 by 31-Jan-2027; Ch.4 working methodology by 15-Mar-2027; Ch.6 after verified scenario runs; Ch.1, 7, 8 refined through July. Not an official TH-1 change.
