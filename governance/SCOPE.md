# Thesis scope and project plan

- **Status:** WORKING PLAN, approved by the student on 16 November 2026. **Supervisor sign-off on decisions S1 to S5 (section 9) has not been verified.** Until it is, those five are working decisions taken on the student's instruction.
- **Author:** Claude Code. Proposed 16 November 2026 on branch `proposal/scope-refocus-2026-11-16`; finalised the same day.
- **Fixed and untouched:** the TH-1 title, the three objectives and the six working milestones.
- **Supersedes:** the scenario framework and variable list of `docs/MODEL_DESIGN.md` v0.1. Version 0.2 of that file implements this plan.

## 0. Approval record and changes made at finalisation

The student instructed on 16 November 2026 that the proposal be treated as approved and finalised. No part of the question, method, scenario set or task plan was changed. Four wording corrections were made, all taken from ChatGPT's independent review against the primary FERC orders (draft PRs #8 and #10):

| # | Proposal text | Corrected to | Where |
|---|---|---|---|
| C1 | "ε = 0 is the firm case" | ε is an energy-curtailment tolerance. Firm access is a separate service state: contracted withdrawal right, adequacy treatment and priority. The firm case is modelled as its own case; a non-firm case with ε = 0 is not a firm contract. | 3.2, 3.4 |
| C2 | "`V(ε)` is the largest discount the system could offer" | `V(ε)` is an illustrative social-cost bound on the value of interruptibility. It is not a tariff, an authorised discount or a ratepayer saving. | 3.4 |
| C3 | Interim: "non-firm treatment until year T, firm after" | After the upgrade the service is full network service (NITS). It does not convert to Firm Contract Demand. | 3.2 |
| C4 | "`G = 0` is an allowed case" that "speaks to ordinary large loads" | The core site has an installed co-located generator. Generator outage (installed, zero output) is a core stress case. Zero installed generation is a labelled hypothetical counterfactual and is not presented as eligible for the co-location services. | 3.3, 5, 9 |

Still open and not settled by this approval: the effective status of the PJM tariff provisions (TH-002), and whether the supervisor accepts S1 to S5.

Other documents to bring into line (owner ChatGPT, on the student's approval): draft PRs #8 (README, project brief, Drive note), #9 (chapter outline) and #11 (task re-scoping) can drop their "proposed" labels, keeping the supervisor caveat above.

## 1. Summary

The topic is sound and timely. The current plan is too wide for one MS thesis in the time left: it crosses three contracts with four outcome families and six sensitivity axes, and its regional model cannot show the effect that most distinguishes the contracts.

The proposal keeps the title and objectives and narrows the work to:

- **One question:** how much system cost does 1 GW of data-centre load avoid when it accepts interruptible instead of firm grid access, and who bears the remaining cost?
- **One mechanism:** contracts differ in adequacy treatment, curtailment priority and cost allocation.
- **One headline result:** avoided cost per GW as a function of the curtailment the data centre accepts. This curve is a priority-service menu, which is what the title promises.

## 2. Review of the current scope

Each finding names its evidence.

**F1. The scenario space is combinatorial.** `docs/MODEL_DESIGN.md` lists three contracts, two baselines, four load sizes, two siting patterns, three flexibility levels, grid congestion, onsite outages and pre/post upgrade, against four outcome families. No run count or priority is given.

**F2. The three service classes are co-location services, and the PJM path for ordinary large loads is separate and unsettled.**

- FERC's December 2025 order (matrix L20, docket EL25-49) directed PJM to create interim non-firm service, Firm Contract Demand and Non-Firm Contract Demand for load co-located with generation. A 2026 order on rehearing and compliance followed (matrix L21). Rates and terms went to a paper hearing; I did not find its outcome.
- PJM's separate large-load track (bring-your-own-generation or connect-and-manage) is a different proceeding. One secondary summary reports that FERC in October 2026 accepted a large-load registry and rejected the curtail-first connection proposal. I saw this in a search snippet only.
- Consequence: `AGENTS.md` already says to keep these two apart, but `MODEL_DESIGN.md` treats onsite generation as optional. For a contract-demand service, the gap between gross load and contracted withdrawal is met by the co-located generator, so that generator is part of the contract's definition. See decision S1.

**F3. The regional testbed is zonal.** The PJM extract is 22 ReEDS zones joined by transfer limits (`docs/PJM_BASELINE_FEASIBILITY.md` on branch `th-003-pypsa-usa-pjm-feasibility`, risk R4). It cannot represent congestion at a point of interconnection. Contract effects must be expressed at zone and interface level, and site-level claims must be dropped.

**F4. Objective 2 has little to calibrate against.** The evidence matrix classifies zero sources as directly instrumented flexibility and records the best field example as a 130 kW demonstration (gap G02). Texas SB6 is law in a different market and shows rights, not delivered response.

**F5. The title says "design"; the plan only compares.** No step produces a menu, a price or a discount. The matrix also holds no source on priority-service theory.

**F6. Ratepayer cost has no bounded method.** TH-007 is "awaiting methodology agreement". A full revenue-requirement and tariff model is a thesis on its own.

**F7. Dispatch-only would erase the contract difference.** With a fixed fleet, 1 GW of firm load shows up only as scarcity hours. The main cost of firm service is the capacity and transfer capability built to serve it. Decision D09 is still open.

**F8. Schedule.** The literature milestone is 45 days away. When this was proposed no PyPSA-USA model had run. Since then the one-day PJM smoke run has passed on a GitHub-hosted Linux runner (see `docs/PJM_BASELINE_FEASIBILITY.md`). The execution environment for full-year runs (D13) is still undecided.

## 3. The focused thesis

### 3.1 Question and sub-questions

**Main question:** for 1 GW of new data-centre load in a PJM-relevant zonal system, how much incremental system cost is avoided when the load takes interruptible instead of firm grid access, and how is the remaining cost split between the data centre and incumbent customers?

| # | Sub-question | Objective |
|---|---|---|
| Q1 | How are firm, non-firm and interim non-firm access written as constraints in PyPSA-USA? | 1 |
| Q2 | What range of curtailment can a data centre physically deliver, and at what cost to itself, according to graded evidence? | 2 |
| Q3 | What are the incremental system cost, curtailment, emissions and incumbent cost per GW under each access type? | 3 |

### 3.2 How each contract enters the model

These are modelling treatments. They are hypothetical until TH-002 confirms them against tariff text.

| Access type | Grid withdrawal | Adequacy requirement | Curtailment order | Who pays for curtailment |
|---|---|---|---|---|
| Firm | up to contracted MW, always | counted at contracted MW | last, with other firm load, at the system value of lost load | system |
| Non-firm | up to contracted MW when the zone and its interfaces have headroom | not counted | first, before any firm load | the site (onsite fuel or lost computing) |
| Interim non-firm | non-firm treatment until the upgrade year T; full network service (NITS) after | not counted before T, counted after | as non-firm before T | the site before T |

Notes for implementation:

- Service state and curtailment tolerance are separate inputs (correction C1). The contracted firm MW, the contracted non-firm MW and the tolerance ε are three different quantities, and none is derived from the co-located generator's capacity or from gross load.
- After the upgrade, interim service becomes full NITS, not Firm Contract Demand (correction C3). The "after" case is modelled with firm treatment of the whole grid withdrawal and the upgraded transfer capability.

- Adequacy: upstream has an energy reserve margin constraint (`add_ERM_constraints`, `workflow/scripts/opts/reserves.py`). Whether one load can be excluded from it cleanly is a TH-004 design question.
- Curtailment order is produced by cost ranking in the optimisation. The ranking is a modelling device consistent with the service priority, and must be labelled as such.
- Interim service is two static cases (before and after year T), not a multi-year transition model. The reported result is the cost or value of the bridge period.

### 3.3 Site model (minimum)

Grid bus → point-of-interconnection link → site bus, with:

- gross site load `D` (flat or one stated profile);
- one co-located generator of fixed installed capacity `G > 0`, with fuel cost and emissions. Its hourly output is a variable, and an outage (installed but producing nothing) is a core stress case;
- curtailed load, bounded by the site's physical flexibility and priced at a stated cost of lost computing;
- involuntary unserved site load, tracked separately from voluntary curtailment.

`G = 0` installed is allowed only as a labelled hypothetical counterfactual for a load with no generator. It is not presented as eligible for the co-location services (correction C4).

Left out of the core model: batteries, exports to the grid, and workload shifting with backlog and recovery windows. Shifting may return as one sensitivity, using upstream's existing `demand_response` option, if time allows.

### 3.4 Headline result

Run the firm case once, then sweep one parameter for the non-firm case: the share of annual energy the load may have curtailed, ε ∈ {0.25, 0.5, 1, 2, 5} %. The firm case is its own case, defined by its service state, not by ε (correction C1).

- `ΔC_firm` = total system cost with the load on firm access, minus the no-data-centre baseline.
- `ΔC(ε)` = the same difference with the load on non-firm access at tolerance ε.
- `V(ε) = ΔC_firm − ΔC(ε)` = system value of interruptibility, reported per GW-year and per kW-year.
- The site's own curtailment cost is reported beside `V(ε)`. Whether system cost already contains it must be stated for every figure, so it is never subtracted twice.

`V(ε)` is an illustrative social-cost bound on what accepting ε is worth to the system. It is not a tariff, an authorised discount or a saving on any customer's bill (correction C2). The table of (ε, `V`) pairs is read as a priority-service menu in the sense of the theory in chapter 2.

### 3.5 Scenario set

| Axis | Values | Purpose |
|---|---|---|
| Access type | none, firm, non-firm (ε sweep), interim | core |
| Zone | three PJM zones chosen from the PJM load forecast (matrix L18) | location |
| Size | 1 GW, and one at-scale case of about 10 GW | marginal vs non-marginal |
| Site flexibility | none, low, evidence-based | objective 2 |
| Year | one forward year (2030 path in upstream) | all cases |

Budget: at most 30 full-year solves. The full ε sweep is run for one zone at 1 GW; other axes use firm plus one or two ε values.

Method: capacity expansion on the forward year, then dispatch of the resulting system. Validation is limited to a one-week 2023 back-cast and the toy-network tests, because the claims are differences between cases on the same grid.

### 3.6 Metrics

| Metric | Unit | Rank |
|---|---|---|
| Incremental system cost (investment + operation) | $/GW-year; also $/MW-year and $/kW-year | primary |
| Curtailed data-centre energy and hours | MWh, hours per year | primary |
| Involuntary unserved firm energy | MWh | primary (reliability proxy) |
| Incremental CO2, grid plus onsite | tCO2 per GW-year | secondary |
| Incumbent cost under two allocation rules | $/GW-year | secondary |

Reliability is reported only as the two energy quantities above, from a deterministic weather year. The thesis will state that this is not N-1 security or probabilistic adequacy.

### 3.7 Incumbent cost: two bookends

- **Rule A, socialised:** the incremental cost is spread over all load.
- **Rule B, cost causation:** the data centre pays the incremental capacity and transfer cost attributable to it; incumbents bear only the residual.

Price effects on incumbents (change in zonal marginal price times incumbent load) are reported separately as a transfer, not added to cost. No tariff or revenue-requirement model is built.

### 3.8 Out of scope

Site-level power flow and congestion; unit commitment; probabilistic adequacy; batteries and exports; dynamic load behaviour; a tariff model; any Pakistan grid simulation; extension of the earlier from-scratch 2025 EIA model.

## 4. How the approved objectives are still met

| Objective (verbatim) | Focused delivery | Wording issue for the supervisor |
|---|---|---|
| 1. Develop an open-source PyPSA-USA module for firm, non-firm, and interim non-firm data-center grid-access contracts. | One tested module with the three treatments of section 3.2, on a toy network and the PJM extract. | None. |
| 2. Calibrate data-center flexibility using observed behavior from FERC/PJM and Texas SB6 filings. | Evidence-graded parameter ranges (observed, derived, assumed), used as three flexibility cases. | "Calibrate… observed" overstates what the evidence allows. Ask whether "evidence-bounded ranges" satisfies the objective. |
| 3. Quantify system cost, reliability, emissions, and incumbent ratepayer cost per GW of new load under each contract design. | The five metrics of section 3.6. | Reliability and ratepayer cost are delivered as bounded proxies. Ask for explicit acceptance. |

## 5. Keep, shrink, cut against `MODEL_DESIGN.md` v0.1

| Item in v0.1 | Action | Reason |
|---|---|---|
| Grid bus, POI link, site bus; gross vs net accounting | Keep | Core of the contract representation |
| Firm and non-firm import bounds | Keep | Core |
| Interim NITS pre/post upgrade | Shrink to two static cases | F1 |
| Onsite generation | Keep one installed unit with variable output (S1, correction C4) | F2 |
| Storage, exports, electrical losses | Cut | Co-location study in its own right |
| Shift-out, make-up, backlog variables | Cut from core; one optional sensitivity | F4; evidence is trace-based only |
| Curtailment bound `alpha` | Keep, as three evidence-graded cases | Objective 2 |
| Sizes 0.1, 0.5, 2 GW | Replace with 1 GW and about 10 GW | Small increments are below solver noise in a system of this size |
| Dispersed vs concentrated siting | Replace with three zones | F3 |
| Grid congestion cases | Cut as an axis; covered by zone choice | F1 |
| Onsite generator outage | Keep as a core stress case, not a full axis (correction C4) | F2 |
| Ten acceptance tests | Keep 1 to 6, 8 to 10; reword 7 for two static cases | Still valid |
| Post-solve revenue accounting | Shrink to the two rules of section 3.7 | F6 |

`docs/MODEL_DESIGN.md` v0.2 is written from this table.

## 6. Text for the thesis note

> Gigawatt-scale data centres are asking for grid access faster than generation and transmission can be built. Regulators are responding with access contracts that trade firmness for speed. This thesis adds an open-source module to PyPSA-USA that represents firm, non-firm and interim non-firm access for a data-centre site, and applies it to a zonal PJM-relevant system for a forward year. Data-centre flexibility is entered as evidence-graded ranges, because metered curtailment at this scale is not public. The main result is the system cost avoided per GW as a function of the curtailment a data centre accepts, which gives a priority-service menu, together with curtailment, emissions and the incumbent-customer cost under two allocation rules. The model is zonal and deterministic: it does not establish site-level deliverability, N-1 security or probabilistic adequacy.

Working choices to record in `PROJECT_BRIEF.md`: forward-year capacity expansion then dispatch; zonal testbed; 1 GW and one at-scale case; three zones; ε sweep; two allocation rules.

## 7. Draft chapter outline

| Ch. | Title | Content | Main sources |
|---|---|---|---|
| 1 | Introduction | Problem, question, contributions, scope limits | L13, L18, L24 |
| 2 | Regulatory and theoretical background | FERC co-location classes; PJM large-load track; Texas SB6; non-firm connections; priority-service theory | L07, L20 to L23, theory sources to add |
| 3 | Literature review | Flexibility evidence; system-impact studies; ratepayer studies; the gap | L01 to L05, L08, L14 to L17, L25 to L27 |
| 4 | Method | Testbed; contract-to-constraint mapping; site model; scenario design; allocation rules; tests | L12, L28 |
| 5 | Data and parameters | Parameter table with evidence grade | Parameter Harvest P01 to P16, pruned |
| 6 | Results | Toy network; firm increment; interruptibility curve; zone and size; interim bridge; emissions; allocation | model outputs |
| 7 | Discussion | Limits; policy reading; transfer of the framework to Pakistan | |
| 8 | Conclusion | | |

Literature to add: priority-service theory, starting with Chao and Wilson (1987), "Priority Service: Pricing, Investment, and Market Organization", American Economic Review. I cite this from memory; verify it.

Literature to stop expanding: heat recovery and all-element flexibility (L10), spatial load migration (L11), detailed load modelling (L09), facility reliability design (L06). Keep them as one paragraph of context.

## 8. Revised task plan

Dates are internal targets inside the existing milestones. They change no milestone.

| ID | Owner | Re-scoped deliverable | Acceptance | Target |
|---|---|---|---|---|
| TH-002 | ChatGPT | One-page table for the three service classes: docket, order date, status, withdrawal right, curtailment trigger, capacity obligation. Plus the answer to S1. | Every cell has a primary source or "not found" | 27 Nov 2026 |
| TH-003 | Claude | Smoke run of the PJM extract passing on Linux, or a specific blocker | Run link and log in the handoff | 27 Nov 2026 (passed 16 Nov 2026, see the TH-003 handoff) |
| TH-005 | ChatGPT | Flexibility table: curtailable share, duration, cost of lost computing, each graded observed / derived / assumed; three cases proposed | No value labelled observed without a metered source | 18 Dec 2026 |
| TH-004 | Claude | `MODEL_DESIGN.md` v0.2; toy network with firm access and tests | Tests run in CI on the pinned versions | 18 Dec 2026 |
| Literature chapter | Student + ChatGPT | Draft of chapters 2 and 3 from 12 to 15 core sources | Draft in Drive | 31 Dec 2026 (milestone) |
| TH-007 | ChatGPT | One-page statement of allocation rules A and B with formulas and what each omits | Student approval | 15 Jan 2027 |
| TH-006 | Claude | Non-firm and interim treatments on the toy network; ε sweep working | Acceptance tests 2 to 8 pass | 31 Jan 2027 |
| TH-008 (new) | Claude | Forward-year PJM baseline; one-week 2023 back-cast | Baseline reproducible from one command | 15 Mar 2027 |
| TH-009 (new) | Claude | Regional scenario runs of section 3.5 | Result tables and run logs | 31 May 2027 (milestone) |

## 9. Decisions

| # | Decision | Recommendation | Who |
|---|---|---|---|
| S1 | Is the thesis about co-located load under the FERC contract-demand classes, or about any grid-connected large load with firm and non-firm access? | Model the co-location and eligible behind-the-meter-generation services, with an installed generator in the core site. Zero installed generation is a labelled hypothetical only (correction C4). Confirm tariff status in TH-002. | Supervisor |
| S2 | Dispatch-only or capacity expansion (D09) | Forward-year expansion, then dispatch | Supervisor |
| S3 | Is a zonal testbed with no site-level claims acceptable? | Yes | Supervisor |
| S4 | Does "evidence-bounded ranges" satisfy objective 2? | Yes, with grades shown | Supervisor |
| S5 | Are bounded proxies acceptable for reliability and ratepayer cost? | Yes | Supervisor |
| S6 | Execution environment (D13) | Decide this week; it blocks every regional run | Student |
| S7 | Back-cast year (D14) | 2023, one week | Student |

**Status on 16 November 2026.** The student adopted every recommendation in this table as a working decision. S1 to S5 are recorded in `governance/DECISIONS.md` as D15 to D19 with supervisor confirmation outstanding. S6 remains open as D13: GitHub-hosted runners cover the toy network and one-day or one-week regional tests, and full-year runs still need an environment. S7 is recorded in D14 as 2023, one week.

## 10. Risks of the narrowed plan

| Risk | Fallback |
|---|---|
| The adequacy constraint cannot exclude a single load without large upstream changes | Represent firmness through a required capacity addition equal to the contracted MW times a stated reserve factor |
| Full-year expansion of 22 zones does not fit the chosen environment | Reduce to representative weeks or 3-hourly resolution; state it |
| The PJM extract never builds | Run the contract module on upstream's maintained regional configuration and present PJM as the regulatory case only; needs supervisor approval |
| `V(ε)` is nearly flat | That is a result: report it and explain which constraint is not binding |
| The regulatory status changes again before submission | Fix a cut-off date for regulatory facts in chapter 2 |

## 11. What was and was not verified

**Read directly on 16 Nov 2026:** `README.md`, `AGENTS.md`, `CLAUDE.md`, all `governance/` files on `main`, the weekly review on branch `review/weekly-2026-11-13`, `docs/MODEL_DESIGN.md`, the TH-003 report and handoff, the Drive context document, and four sheets of the literature workbook (Start Here, Parameter Harvest, Gap Map, Source Register). In upstream PyPSA-USA at `v1.0.0`: the existence of `add_ERM_constraints` and of the `demand_response` and `load_shedding` options.

**Not verified:**

- The FERC and PJM points in F2 come from web-search summaries of law-firm and trade articles, not from the orders. Dates differ between summaries. TH-002 must fix them from the dockets.
- I did not open any PDF in the literature folder or read any matrix source in full.
- No model was run for this document. Every modelling statement in section 3 is a design proposal.

**Web sources seen (secondary):**

- https://www.klgates.com/FERC-Orders-PJM-to-Reform-Tariff-for-Co-Located-Generation-and-Load-1-15-2026
- https://www.mayerbrown.com/en/insights/publications/2026/01/ferc-directs-pjm-to-facilitate-co-location-arrangements
- https://www.willkie.com/publications/2026/07/ferc-greenlights-pjm-co-located-load-framework-in-part-calls-for-further-tariff-updates
- https://www.ferc.gov/sites/default/files/2026-06/EL25-49-002_0.pdf
- https://insidelines.pjm.com/pjm-board-outlines-plans-to-integrate-large-loads-reliably/
- https://www.pjm.com/-/media/DotCom/committees-groups/committees/mrc/2026/20260325/20260325-item-01---2-connect-and-manage---problem-statement.pdf
- https://baxtel.com/news/ferc-backs-pjm-data-center-registry-rejects-curtailment-plan
