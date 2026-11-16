# Scope refocus proposal and revised project plan

- **Status:** ARCHIVED PROPOSAL, text as proposed on 16 November 2026 (commit `c092698`). The student accepted it the same day as the working scope. The active record is `governance/APPROVED_WORKING_SCOPE_2026-11-16.md`, `governance/DECISIONS.md` and `docs/MODEL_DESIGN.md` v0.2; where they differ from this text (for example D20 and D21), they govern.
- **Author:** Claude Code. **Date:** 16 November 2026.
- **Readers:** ChatGPT (to revise the thesis note and outline), the student (to approve or change), the supervisor (decisions in section 9).
- **Fixed and untouched:** the TH-1 title, the three objectives and the six working milestones.

## 0. What this asks of ChatGPT

Read sections 1 to 5, then:

1. Revise the thesis note in three places so they say the same thing: the "Thesis in one paragraph" in `README.md`, the working choices in `governance/PROJECT_BRIEF.md`, and "Research approach" in the Drive document "MS Thesis - Research Context and Coordination". Section 6 has proposed text.
2. Produce a chapter outline from the draft in section 7, with a page budget and the source IDs from the evidence matrix that feed each section.
3. Re-scope TH-002, TH-005 and TH-007 as in section 8 and update the issues.
4. Answer framing question S1 (section 9) from the primary FERC and PJM documents. It decides whether the site model keeps a co-located generator.

Keep every change labelled "proposed" until the student approves it. Open one PR per document set, as `AGENTS.md` requires. If you disagree with a recommendation, say so in the PR with the source; do not silently drop it.

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

**F8. Schedule.** The literature milestone is 45 days away. No PyPSA-USA model has run: the first Linux smoke run failed in the data-model build and is being diagnosed. The execution environment (D13) is undecided.

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
| Interim non-firm | non-firm treatment until year T, firm after | not counted before T, counted after | as non-firm before T | the site before T |

Notes for implementation:

- Adequacy: upstream has an energy reserve margin constraint (`add_ERM_constraints`, `workflow/scripts/opts/reserves.py`). Whether one load can be excluded from it cleanly is a TH-004 design question.
- Curtailment order is produced by cost ranking in the optimisation. The ranking is a modelling device consistent with the service priority, and must be labelled as such.
- Interim service is two static cases (before and after year T), not a multi-year transition model. The reported result is the cost or value of the bridge period.

### 3.3 Site model (minimum)

Grid bus → point-of-interconnection link → site bus, with:

- gross site load `D` (flat or one stated profile);
- one co-located generator of fixed capacity `G`, with fuel cost and emissions; `G = 0` is an allowed case;
- curtailed load, priced at a stated cost of lost computing.

Left out of the core model: batteries, exports to the grid, and workload shifting with backlog and recovery windows. Shifting may return as one sensitivity, using upstream's existing `demand_response` option, if time allows.

### 3.4 Headline result

Sweep one parameter: the share of annual energy the non-firm load may have curtailed, ε ∈ {0, 0.25, 0.5, 1, 2, 5} %. ε = 0 is the firm case.

- `ΔC(ε)` = total system cost with the load at ε, minus the no-data-centre baseline.
- `V(ε) = ΔC(0) − ΔC(ε)` = system value of interruptibility, reported per GW-year and per kW-year.
- `V(ε)` minus the site's own curtailment cost = net value.

`V(ε)` is the largest discount the system could offer for accepting ε. The table of (ε, discount) pairs is a priority-service menu.

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
| Onsite generation | Keep one fixed unit, pending S1 | F2 |
| Storage, exports, electrical losses | Cut | Co-location study in its own right |
| Shift-out, make-up, backlog variables | Cut from core; one optional sensitivity | F4; evidence is trace-based only |
| Curtailment bound `alpha` | Keep, as three evidence-graded cases | Objective 2 |
| Sizes 0.1, 0.5, 2 GW | Replace with 1 GW and about 10 GW | Small increments are below solver noise in a system of this size |
| Dispersed vs concentrated siting | Replace with three zones | F3 |
| Grid congestion, onsite outage cases | Cut as axes; covered by zone choice and `G = 0` | F1 |
| Ten acceptance tests | Keep 1 to 6, 8 to 10; reword 7 for two static cases | Still valid |
| Post-solve revenue accounting | Shrink to the two rules of section 3.7 | F6 |

Claude will write `MODEL_DESIGN.md` v0.2 from this table after approval.

## 6. Proposed text for the thesis note

> Gigawatt-scale data centres are asking for grid access faster than generation and transmission can be built. Regulators are responding with access contracts that trade firmness for speed. This thesis adds an open-source module to PyPSA-USA that represents firm, non-firm and interim non-firm access for a data-centre site, and applies it to a zonal PJM-relevant system for a forward year. Data-centre flexibility is entered as evidence-graded ranges, because metered curtailment at this scale is not public. The main result is the system cost avoided per GW as a function of the curtailment a data centre accepts, which gives a priority-service menu, together with curtailment, emissions and the incumbent-customer cost under two allocation rules. The model is zonal and deterministic: it does not establish site-level deliverability, N-1 security or probabilistic adequacy.

Working choices to record in `PROJECT_BRIEF.md` as proposed: forward-year capacity expansion then dispatch; zonal testbed; 1 GW and one at-scale case; three zones; ε sweep; two allocation rules.

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
| TH-003 | Claude | Smoke run of the PJM extract passing on Linux, or a specific blocker | Run link and log in the handoff | 27 Nov 2026 |
| TH-005 | ChatGPT | Flexibility table: curtailable share, duration, cost of lost computing, each graded observed / derived / assumed; three cases proposed | No value labelled observed without a metered source | 18 Dec 2026 |
| TH-004 | Claude | `MODEL_DESIGN.md` v0.2; toy network with firm access and tests | Tests run in CI on the pinned versions | 18 Dec 2026 |
| Literature chapter | Student + ChatGPT | Draft of chapters 2 and 3 from 12 to 15 core sources | Draft in Drive | 31 Dec 2026 (milestone) |
| TH-007 | ChatGPT | One-page statement of allocation rules A and B with formulas and what each omits | Student approval | 15 Jan 2027 |
| TH-006 | Claude | Non-firm and interim treatments on the toy network; ε sweep working | Acceptance tests 2 to 8 pass | 31 Jan 2027 |
| TH-008 (new) | Claude | Forward-year PJM baseline; one-week 2023 back-cast | Baseline reproducible from one command | 15 Mar 2027 |
| TH-009 (new) | Claude | Regional scenario runs of section 3.5 | Result tables and run logs | 31 May 2027 (milestone) |

## 9. Decisions needed

| # | Decision | Recommendation | Who |
|---|---|---|---|
| S1 | Is the thesis about co-located load under the FERC contract-demand classes, or about any grid-connected large load with firm and non-firm access? | Model the co-location classes, with `G = 0` as a limiting case that speaks to ordinary large loads. Confirm after TH-002. | Supervisor |
| S2 | Dispatch-only or capacity expansion (D09) | Forward-year expansion, then dispatch | Supervisor |
| S3 | Is a zonal testbed with no site-level claims acceptable? | Yes | Supervisor |
| S4 | Does "evidence-bounded ranges" satisfy objective 2? | Yes, with grades shown | Supervisor |
| S5 | Are bounded proxies acceptable for reliability and ratepayer cost? | Yes | Supervisor |
| S6 | Execution environment (D13) | Decide this week; it blocks every regional run | Student |
| S7 | Back-cast year (D14) | 2023, one week | Student |

Proposed new rows for `governance/DECISIONS.md`: S1 to S5 as D15 to D19, status "Proposed".

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
