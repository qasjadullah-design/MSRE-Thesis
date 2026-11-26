# PyPSA-USA priority-service model — working design v0.2
**Status: STUDENT-APPROVED WORKING RESEARCH DESIGN (16 November 2026).** Supervisor/university endorsement of the narrowed interpretation of Objectives 2 and 3 remains **unverified**. This supersedes v0.1 as the active implementation brief; [original Claude proposal](https://github.com/qasjadullah-design/MSRE-Thesis/blob/proposal/scope-refocus-2026-11-16/governance/proposals/SCOPE_REFOCUS_2026-11-16.md) remains archived. Do not change submitted TH-1 title, three verbatim objectives, or six working milestone dates. Code, calibration and results are not yet validated.

## Dated regulatory implementation addendum — TH-002

The [26 November contract comparison](../regulatory/TH-002_CONTRACT_MATRIX_2026-11-26.md), [primary-source audit](../references/TH-002_SOURCE_AUDIT_2026-11-26.md), and [PyPSA requirements](TH-002_PYPSA_REQUIREMENTS_2026-11-26.md) translate this approved v0.2 design into a dated order-based / November-proposal research specification. They distinguish ordered principles from proposed detailed clauses and unverified effective records. They define the ε budget over all controlled physical site reduction, preserve hard operator limits, distinguish site deficits from denied firm service, and specify Interim→NITS planning requirements. This addendum does not claim implemented code, enacted November provisions, or a revised student/supervisor scope approval.

## One research question and headline
For **1 GW of incremental data-center demand** in a **PJM-relevant zonal** system, how much incremental **system cost** is avoided when the load accepts interruptible versus firm grid service, and how is remaining cost assigned to the new data center versus incumbent customers?

Deliver a **curtailment–cost frontier**, and a **hypothetical priority-service menu** connecting curtailment allowances and economically defensible *upper bounds* for a discount. This is NOT an adopted PJM tariff or an approved price. Retain distinct contract rights, capacity/planning treatment and curtailment priority independent of epsilon.

## Exact TH-1 objectives (unchanged)
1. Develop an open-source PyPSA-USA module for firm, non-firm, and interim non-firm data-center grid-access contracts.
2. Calibrate data-center flexibility using observed behavior from FERC/PJM and Texas SB6 filings.
3. Quantify system cost, reliability, emissions, and incumbent ratepayer cost per GW of new load under each contract design.

## Regulatory framing — approved by student for modeling, subject to source-status verification
Core test case addresses **FERC/PJM co-located loads and qualifying behind-the-meter-generation (BTMG)** service arrangements, NOT arbitrary ordinary grid-connected large loads. Include a generator in the core physical topology. Separate **installed generation** from **actual onsite generation**. Generator dispatch at zero during an outage is a valid core case. A model with **no installed generator** is an explicitly hypothetical engineering comparison and does not establish legal eligibility for FCD/NFCD or Interim NITS. Consult [S1 source memo](../regulatory/PROPOSED_S1_COLOCATION_FRAMING_2026-11-16.md) (now student-accepted framing; historically named PROPOSED), FERC December 2025 and June 2026 orders; the TH-002 addendum records the latest retrieved proposal and remaining effective-record verification gates.
- Firm Contract Demand (FCD): physical withdrawals bounded by reserved firm MW; planning treatment and protection based on verified service rules.
- Non-Firm Contract Demand (NFCD): withdrawals limited by reserved MW and available capacity/qualifying curtailment events; not simply an exogenously given shed percentage. Use the ordered priority/adequacy distinctions and separately tagged proposed implementation in TH-002; operational-manual details remain unresolved.
- Interim NITS: **two static cases**, before upgrades (interim non-firm treatment) and after upgrades (**full NITS**, NOT automatic FCD). Report value/cost of interim bridge.
- Do not tie reserved FCD/NFCD MW automatically to co-located generator capacity or gross load. Keep three quantities separate.

## Minimum physical model
A single **grid bus → point-of-interconnection (POI) link → site bus**, plus gross site demand `D[t]`, one co-located generator of installed fixed MW `G` (fuel, efficiency, operating cost, emissions), and an explicit `C[t]` curtailed physical computing load (MW; lost-computing disutility). Keep physical POI capacity and contractual entitlements independent.

Core site balance (units MW):
`grid_import[t] + onsite_gen[t] = served_site_load[t]`,
`served_site_load[t] = D[t] - C[t]`,
`0 <= onsite_gen[t] <= G * availability[t]`,
`0 <= grid_import[t] <= POI_capacity`,
`0 <= C[t] <= alpha[t] * D[t]`.
Model relevant parasitic loads only if explicitly included in D. Use a constant demand or ONE declared demand profile. No batteries, exports, electrical-loss detail, workload migration, dynamic recovery/backlog or unit commitment in the core model.

**Separation of controls:** `alpha` is *physical* interruptible share; `epsilon` is a service-policy annual energy curtailment tolerance. An energy tolerance alone cannot create an actual contract or justify ignoring site energy balance.

## Contract module and capacity adequacy
Use modular PyPSA/Linopy components and test contracts on 3–5 synthetic buses before integrating regional PyPSA-USA.
- Record `firm_reserved_mw`, `nonfirm_reserved_mw`, tariff status, physical POI MW, interconnection category, eligibility, outage/availability and priority policy in validated input schema.
- Model `0 <= P_firm[t] <= F`; `0 <= P_nonfirm[t] <= min(R_NF[t], availability_NF[t])` with applicable event restriction; both part of physical gross grid imports and POI cap, and no simultaneous double-counting.
- In forward-year expansion, model the *distinct firm resource-adequacy obligation* using existing PyPSA-USA reserve-margin formulation where viable; any simplified fallback capacity addition must be identified as a **proxy**, not a verified PJM planning rule.
- Model disconnection order with explicit event rules or validated priority penalty/lexicographic optimization; any ranking is a modeling assumption pending tariff verification. Never silently classify curtailed NF demand as involuntary unserved firm energy.
- If shortage requires firm shedding, distinguish it as a separate variable with very high penalty and measurable MWh.

## Annual curtailment tolerance sweep
Proposed **epsilon (%) = {0, 0.25, 0.5, 1, 2, 5}** for one principal zone, 1 GW case. Distinguish an upper bound on annually *permissible contract interruption* from what physical flexibility can deliver. Add an explicit annual energy constraint such as `sum_t(C_contract[t] * weight[t]) <= epsilon/100 * sum_t(D[t] * weight[t])` only if this interpretation is made clear. Do not force infeasible service to pass by adding free shedding.

Define from consistently annualized optimized physical-system cost:
- `DeltaC_k = C_system_with_load_k - C_system_no_new_load`.
- `V(epsilon) = DeltaC_firm - DeltaC_NF(epsilon)` comparing **separate firm and nonfirm legal/technical service cases** (do not pretend epsilon=0 equals FCD automatically).
- Net social benefit: subtract separately measured site disutility **only if not already included** in C_system. Explicitly report social-resource cost boundary vs payments/transfers.
- Discount menu values are **indicative avoided-resource-cost bounds**; pricing feasibility also depends on developer willingness, incidence, tariffs and credible delivered interruptions.

## Scenario limit (prevent combinatorial explosion)
At most **30 regional full-year solves**, using **2030 forward planning horizon** if upstream support and data permit.
1. Base case B0 no new load.
2. Firm benchmark, and NF epsilon sweep for ONE representative PJM-ReEDS zone at 1 GW.
3. Three selected PJM zones based on documented load forecast data: compare firm plus one or two approved nonfirm epsilons per zone.
4. Size: primary 1 GW; ~10 GW **aggregate regional-scale** sensitivity, not a single campus or single 10 GW POI.
5. Flexibility: none, low, evidence-bounded upper case; labels must show measured/derived/assumed. No invented physical response data.
6. Interim bridge: two separately configured pre/post-upgrade static network and service runs.
7. Annual investment/expansion followed by dispatch. If runtime infeasible, use a documented representative-week or 3-hour time resolution sensitivity, without claiming a full-hourly-year result.

No explicit transmission-line contingency, storage, export, day-ahead market clearing, sub-hour transient model, Pakistan network or comprehensive financial tariff model in core scope.

## Calibration: three evidence grades and data provenance
`TH-005` must extract physically curtailable fraction (MW/%), feasible duration (h), response/ramp and value/cost of lost computing (USD/unit) where credible. Every candidate value: source/DOI/docket/section, jurisdiction/technology, measurement boundary, sample size, observed full-site delivered MW vs computing-trace + modeled power vs derived vs hypothesis, uncertainty and applicability to PJM. Legislation such as Texas SB6 is a regulatory requirement, not actual data-center delivered-response measurement. If empirical evidence fails, report limits and obtain supervisor guidance on TH-1 Objective 2—do not relabel assumptions as observed.

## Metrics and economic allocation
PRIMARY: annualized system cost (capital additions + operating cost) as USD/GW-year, MWh/hours contractual curtailment, MWh **involuntary firm unserved energy**. SECONDARY: grid + onsite tCO2/GW-year and two **illustrative** incumbent allocations.
- Rule A (socialized): assign a clearly defined share of incremental **recoverable** cost across incumbent and new loads, with an explicit load denominator and separate new-load contributions.
- Rule B (cost causation): assign attributable incremental capacity/intertie investment to data center, with justified residual to incumbents. Define every ledger item.
- Reconcile `incremental recoverable costs = DC contribution + incumbent allocation + other sources/credits`. Physical cost, tariff collections and zonal price transfers are **not identical**. Price change × existing load is a separate transfer estimate; never add to physical resource costs or claim a simulated actual utility bill.

Reliability: report contractual curtailed MWh separately from involuntary firm unserved MWh for a **deterministic** scenario year. Do not claim LOLP/LOLE, N-1 security or site-level power-flow feasibility from zonal expansion results.

## Validation / release gates
- TH-003 upstream PyPSA-USA commit/environment, PJM ReEDS 22-zone approximation, data/footprint gaps and Linux execution blocked/confirmed with logs.
- TH-004 toy site balance, FCD import bound, generator capacity/outage, zero actual flexibility, physical curtailment and solver tests; pinned upstream environment compatibility.
- TH-006 NF service & intermittent/interim treatment, event priority, annual epsilon cap, generator-site MW conservation, static post-upgrade NITS transition.
- TH-008 zonal regional network reproducibility, carefully limited **one-week 2023** back-cast, boundary and validation checks. 2023 is student-approved *working choice*, not yet a successful back-cast.
- TH-009 core regional scenario matrix, run count, results and logs with allocation reconciliation. All runs in reproducible scripts.
- Findings and published curves must identify what was actually run vs design-only material.

## Dates / source authority
Current user-approved working milestones: literature **31 Dec 2026**; data **31 Jan 2027**; analysis **15 Mar 2027**; model deployment **31 May 2027**; result evaluation **30 Jun 2027**; thesis and article **31 Jul 2027**. Existing filed TH-1 text for M4 was 30 May: formal amendment unverified; don't silently claim university acceptance. Supervisor's endorsement of simplified proxies and scoped language must be sought before asserting objective completion.

Sources: [FERC Dec 2025 order](https://www.ferc.gov/sites/default/files/2025-12/E-1%20EL25-49-000.pdf), [FERC Jun 2026 order](https://www.ferc.gov/sites/default/files/2026-06/EL25-49-002_0.pdf), [PJM Feb 2026 planning slides](https://www.pjm.com/-/media/DotCom/committees-groups/workshops/cllsco/2026/20260210/20260210-item-01---3-co-located-load-planning-study-considerations-for-reference-purposes.pdf); `regulatory/PROPOSED_S1_COLOCATION_FRAMING_2026-11-16.md` (historical filename, student accepted). See the TH-002 addendum for the dated source-status findings and unresolved effective-tariff conditions.
