# TH-002 — PyPSA contract implementation requirements

**26 November 2026 · issue #1 · design specification, not implemented or solver-validated.** Builds on [approved model design v0.2](MODEL_DESIGN.md), the [16 November S1 memo](../regulatory/PROPOSED_S1_COLOCATION_FRAMING_2026-11-16.md), and the [contract comparison](../regulatory/TH-002_CONTRACT_MATRIX_2026-11-26.md). Source IDs O26/P26 and rule IDs R01–R11 below resolve to exact dated provisions in the [source audit](../references/TH-002_SOURCE_AUDIT_2026-11-26.md).

## 1. Scope and legal versioning

Keep the approved **1,000-MW gross site**, fixed physical onsite generator, separate grid/POI/site boundary, 2030 zonal study, three zones and ≤30 regional full-year solves. No storage, exports, unit commitment or workload backlog is added by this specification. Interim remains two static runs. Official objectives and milestones are unchanged.

**REQ-01 — preserve legal state.** Each rule/scenario must record `source_id`, `docket`, `section_or_paragraph`, `source_date`, `checked_as_of`, `legal_status`, `requested_effective_date`, `accepted_effective_date` and `evidence_grade`. Use at least `ordered_framework`, `filed_proposal`, `effective_verified`, `not_established`; keep evidence grades (`regulatory`, `observed`, `inferred`, `hypothetical`) separate. O26 determinations and November proposal details cannot collapse into a single “effective tariff” switch. Unknown accepted dates are null, never copied from requested dates. A 2030 simulation date does not prove a 2026 proposal will be enacted. **Basis:** O26 ¶¶7–9, 263 n.635; P26 §V p.82; audit Q1/Q2.

**REQ-02 — explicit eligibility.** Record `arrangement` (co-located / qualifying BTMG / ordinary large load), installed G, generator interconnection and capacity-resource status, dedicated portion/CIR status, controls capability, service agreement and requested study status. `G>0` alone is not sufficient legal eligibility. `G=0` fails the core-scope assertion unless the scenario explicitly identifies a hypothetical or proposed broader-load case. A generator outage changes availability, not installed capacity or arrangement. **Basis:** R01, R07, R09; O26 ¶91; P26 §§701.1, 708(a), 710.3, 716–718.1.

## 2. Input and state schema

| Group | Required fields / units | Validation and interpretation |
|---|---|---|
| Site | `gross_demand_mw[t]`, `onsite_installed_mw`, `onsite_availability_pu[t]`, `poi_capacity_mw`, fuel/efficiency/cost/emissions | Nonnegative MW; availability 0–1. G, D and POI capacity are independent. One declared demand profile; no implicit external supply. |
| Service | `service_mode`, `firm_reserved_mw=F`, `nonfirm_reserved_mw=N`, `interim_studied_limit_mw[t]=H[t]`, declared full-NITS withdrawal envelope | `contract_demand` may represent F and/or N; `interim_nits` and `nits` are separate modes. No Interim/NITS overlap or conflicting pending application with F/N on the same designated load. Record prior service/applications for Q2 review; do not assume a lifetime prohibition. Exact mixed F/N agreement fields remain Q2. |
| Operations | `event_id[t]`, cause flags, instructed import ceilings in MW, priority class, response assumption | A zero non-firm ceiling means no withdrawal under that service. Missing ceilings are not silently interpreted as unrestricted service. Distinguish transmission and capacity/reserve events. |
| Physical flexibility | `alpha[t]` in 0–1; allowed duration/response limits where evidenced; `epsilon_percent`; computing-loss cost | `alpha` is deliverable physical reduction; ε is an annual research tolerance. Neither is a legal entitlement. Unknown response timing remains an assumption, not zero-delay observed performance. |
| Generator status | `is_capacity_resource`, `interconnection_status`, `dedicated_fraction`, `onsite_supply_allowed[t]` | Enforce interim curtailment restriction; do not credit dedicated capacity twice. |
| Planning | `planning_basis_mw`, accreditation/margin convention, source/proxy label | FCD basis derives from F; NFCD/Interim add no procurement obligation under O26 ¶597. Full-NITS basis requires a separate source or explicit proxy. |
| Transition / term | `upgrades_complete`, `pjm_analysis_passed`, `pjm_systems_updated`, agreement/implementation date, destination service, current/prior service and pending applications | Interim destination must be `nits`. Contract choice is fixed per scenario; no costless hourly/annual switching. |
| Reproducibility | upstream commit, environment lock, rule-set revision, scenario ID, input hashes, physical hours weights | Pin under TH-003. Custom legal constraints and outputs must be reconstructable after export/reload. |

Proposed current/pending-application exclusivity is P26 §§701.3, 709.3; §710.3 is summarized with historical wording on p.39, so its prior-service interpretation remains a Q2 clean-sheet check; willingness, controls and technical prerequisites are §§702.3, 710.3, 716–718.1. No reservation identity such as `F+N=D` or `F=D-G` may be imposed as a legal minimum (O26 ¶¶342–344). A selected numerical sizing convention must be labeled a scenario assumption.

## 3. Physical balance and withdrawal constraints

**REQ-03 — conserve MW at the site.** For snapshot t, use nonnegative actual imports I, onsite output g and controlled physical load reduction C:

```text
I[t] + g[t] + C[t] = D[t]
0 <= g[t] <= G * availability[t] * onsite_supply_allowed[t]
0 <= I[t] <= K
0 <= C[t] <= alpha[t] * D[t]
```

K is physical POI MW. The core no-export model has no negative imports. Curtailment represented by a mathematical injection at the site must be named/limited as load reduction; it is not a fuel-free generator and must not earn generation capacity credit or appear as generation in energy/emissions reporting. **Basis:** approved v0.2 physical topology; R02/R05.

**REQ-04 — apply service rights separately.** In contract-demand mode, use I = I_F + I_N and:

```text
0 <= I_F[t] <= F
0 <= I_N[t] <= N
I_F[t] + I_N[t] <= K
I_N[t] <= instructed_nonfirm_limit_mw[t]
```

Apply any independently authorized firm emergency ceiling separately. FCD has firm priority, not unlimited access or emergency immunity. In Interim mode, set F/N imports to zero, require `I[t] = I_J[t]`, and enforce `0 <= I_J[t] <= min(K, H[t], instructed_interim_limit_mw[t])`. H is studied headroom, not an invented guaranteed entitlement. Full NITS requires `I[t] = I_NITS[t]` with its own nonnegative network/operating envelope; it is not implemented by renaming H as F. Only the selected mode's flows contribute to site balance. These bounds are **hard constraints**, including when noncompliance would be cheaper. **Basis:** R02–R04; P26 §§701.1–701.5, 708(b), 719.

For the core, use a dedicated non-capacity onsite generator and state that assumption. If a capacity-resource variant is later considered, O26 ¶576 requires restricting its supply to the site during Interim curtailment unless the stated exception applies. Do not erase a grid capacity resource and its system contribution merely to preserve the no-export topology; such a variant needs a separately justified boundary. **Basis:** R05/R07, audit Q2/Q6.

## 4. Curtailment authority, priority and ε

**REQ-05 — model causes and priority, not just prices.** Include both transmission/security restrictions and generation capacity/reserve shortages as possible interruption causes. Under the November proposal, NFCD, Interim NITS and non-firm point-to-point occupy the **same non-firm tier**; FCD shares the firm tier with NITS/firm point-to-point. Do not hard-code NFCD before Interim. The order requires Interim NITS and NFCD interruption ahead of PJM's Pre-Emergency Load Response Program; the zonal model may represent that boundary as an event rule, but must not claim to reproduce the full PJM emergency procedure. **Basis:** O26 ¶¶551–555; P26 §§719.2, 719.4–719.5.

Use exogenous, sourced/synthetic instruction profiles for the first prototype. For endogenous shortage scenarios, protect requested firm service before choosing technically effective non-firm service to interrupt, through explicit priority logic or a documented lexicographic solve. A high numerical penalty alone is not proof of priority. A lexicographic optimum is also insufficient if its feasible set allows an obligated non-firm site to retain technically effective imports merely because its α or ε is exhausted while firm service is denied. Explicitly reject that outcome: enforce the applicable prior non-firm interruption, and classify physical inability to comply as infeasibility or a failed diagnostic. Curtailment elsewhere that cannot relieve a modeled transmission limit is not a substitute for effective relief. Within the equal non-firm tier, system-limit contribution matters; any zonal tie-breaking approximation must be stated. Missing manuals prevent claims about exact response time, restoration, or the operational ranking algorithm (Q3).

**REQ-06 — keep the ε budget subordinate to instructions.** Use v0.2's sweep `{0, 0.25, 0.5, 1, 2, 5}` percent. Define this implementation's research budget over **all controlled physical reduction C**, including reduction needed to comply with an instruction and any voluntarily selected reduction:

```text
sum_t(hours[t] * C[t]) <= epsilon_percent / 100 * sum_t(hours[t] * D[t])
```

This definition closes a loophole in which the optimizer could relabel reduction as “economic” or “mandatory” to evade the budget. It is an explicit operationalization of v0.2's tolerance, **not a claim that PJM promises an annual interruption allowance**. Use physical represented hours, not discounted financial objective weights. A required instruction exceeding α/duration/ε capability makes the configured service infeasible; never relax the instruction, create free backup supply, or treat non-firm ε=0 as FCD. **Basis:** v0.2; R04/R09; no tariff ε guarantee located (Q6).

Report controlled C during instruction events and outside them separately, without double-counting overlapping causes. “C during an event” is event-associated, not automatically the causal incremental compute loss from that event. A narrower causal contract-interruption estimate needs a declared counterfactual, not two freely interchangeable curtailment variables.

## 5. Resource adequacy and the upgrade transition

**REQ-07 — give capacity obligations an independent input.** O26 ¶597 requires FCD procurement based on contract demand and excludes NFCD/Interim from that RA planning/procurement. For the toy model, `planning_basis_mw=F` for FCD and `0` for the NFCD/Interim portions expresses that distinction. It is not a declaration that F MW equals F MW of UCAP purchases: accreditation, margin, peak allocation and settlement factors require separate specification. Neither low actual imports nor ε should reduce F's contractual basis. **Basis:** R06; P26 §III.E p.57 acknowledges potential further capacity/forecast filings.

Integrate the basis into the pinned PyPSA-USA adequacy formulation if viable. Otherwise use an explicitly labeled deterministic planning proxy with a coherent capacity basis, reserve-margin convention and technology credits. Excluding NFCD/Interim from procurement is not permission to ignore their actual energy demand, network limits, operating reserves or emissions. Remove the dedicated onsite portion from simultaneous system capacity credit/CIR accounting (P26 §710.3); include its actual supply in site energy balance.

**REQ-08 — run two distinct Interim states.** The pre-upgrade run uses interim headroom and no RA procurement addition for that service. The post-upgrade run uses the upgraded network, completed PJM analysis/internal-system conditions, and **full NITS** service/planning treatment. Record all three conditions independently; an upgrade-completion boolean alone is insufficient. Compare the two static cases without modeling an intertemporal investment/transition option. **Basis:** O26 ¶571; P26 §702.4(a), F-3A §§2–3.

The post-upgrade network-load/BTMG basis is **not yet established for the modeled customer**. P26 Part III §34.2(B)–(F) and RAA Schedule 8(A), pp.24–27, propose a 50-MW retail-BTMG netting limit with exceptions. Do not automatically subtract all onsite generation from NITS capacity obligations or assume a new 2030 campus is grandfathered. Until Q4 is resolved, use a stated full-gross-demand planning proxy if needed and label it hypothetical. Keep the separately proposed NFCD→FCD route (P26 §711(f), F-4) distinct. Measure the five-year FCD-to-NFCD restriction from the relevant service agreement's effective date and the 42-month FCD termination notice before commencement of the Delivery Year (P26 §§709.3, 711(b)). These clocks belong in contract metadata; the approved static runs must not optimize around them as free annual switches.

## 6. Reliability and accounting outputs

**REQ-09 — do not equate compute loss with denied firm service.** Keep three measurements distinct:

| Quantity | Meaning / safeguard |
|---|---|
| Controlled site reduction, `sum(hours*C)` | Physical computing load deliberately reduced within α and the declared budget; includes event-associated and voluntary components. |
| Requested service denied, split by firm/non-firm/interim | Compare delivery with a declared, physically supportable request/nomination bounded by the entitlement. An unused reservation `F-I_F` is not automatically unserved firm energy. Specify the request and attribution rule before reporting this metric. |
| Involuntary site supply deficit | Diagnostic residual when supply and physically feasible C cannot meet D. An onsite-generator failure or an undersized reservation may cause this without denial of the firm's requested grid service. |

For a diagnostic stress solve only, an explicit nonnegative `U_site[t]` can extend the balance to `I+g+C+U_site=D`, with its own high penalty and cause reporting. **Main feasible-frontier runs require U_site=0**; a positive diagnostic value classifies the configured scenario as a service/physical-feasibility failure. It cannot bypass ε and be reported as a successful low-curtailment contract. Grid-wide involuntary protected firm load loss is tracked separately. The implementation must test the firmness attribution rule; TH-002 does not claim it has been coded.

Example: D=1,000 MW, G=900 MW, F=100 MW. If the generator fails and all 100 MW of requested FCD arrives, the remaining 900 MW must be physically curtailed within the configured capability or reported as a site deficit. It is **not 900 MW of denied FCD**. This is a synthetic accounting example, not a claim that this sizing is required or a measured installation. Report deterministic MWh/hours and maximum-event duration, not LOLE, N-1 security or probabilistic adequacy.

**REQ-10 — preserve cost boundaries.** Report annualized real resource costs (grid investment/operation, onsite generation and fuel, and explicitly included loss-of-computing cost) separately from transmission/capacity/ancillary payments and the two illustrative incidence allocations. Include any new fixed onsite generator capital cost consistently even if it is a constant omitted from the solver objective. State whether the no-new-load counterfactual retains, adds, or diverts that generator; do not hide lost grid supply from an existing plant. This is accounting within v0.2, not an additional technology scenario.

Compute avoided cost only between matched boundaries. If computing disutility is already included in reported system/social cost, do not subtract it again; otherwise report physical avoided cost and net avoided cost after one disutility deduction separately. Retain `incremental recoverable cost = DC contribution + incumbent allocation + other sources/credits` for the later TH-007 ledger. Zero NFCD/Interim capacity procurement does not imply zero transmission/ancillary cost or an approved discount (O26 ¶¶572–573; P26 §§703.2, 703.4, 714.3, 714.5, 715.4; companion ER27-520). Include onsite emissions and exclude the artificial curtailment injection from generation totals.

## 7. PyPSA implementation interface and required tests

**REQ-11 — build a reconstructable module.** Use one import path or separately identified service-flow variables sharing one physical K bound. Use the pinned PyPSA/Linopy model extension interface for service bounds, event ceilings, site balance, ε, and planning obligations. Official [PyPSA Custom Constraints](https://docs.pypsa.org/latest/user-guide/optimization/custom-constraints/) documents `n.optimize.create_model()`, adding variables/constraints, `solve_model()`, and the `extra_functionality` hook. Names and indexing must be verified against TH-003's pinned version. Save custom constraint inputs and results explicitly: a network export does not preserve the live optimization model/custom outputs automatically. No runnable code or version compatibility is claimed by this requirements document.

**Acceptance tests to implement under TH-004/TH-006 — not executed in TH-002:**

| Test | Required observable outcome |
|---|---|
| MW conservation / independent limits | D, G, F, N and K vary independently; no invented `F+N=D` rule; imports respect total K and each entitlement. |
| Generator outage / firm attribution | The 1,000/900/100 example produces no denied FCD if 100 MW is delivered; any unmet site demand is separately visible. |
| Zero reservation / eligibility | N=0 allows no NF imports but does not waive agreement/controls metadata; conflicting pending NITS/Interim applications are rejected for contract-demand mode; G=0 rejected in core, allowed only with an explicit non-core label. |
| Zero physical response | α=0 cannot satisfy a mandatory import reduction through fictional computing curtailment; feasibility depends on permissible onsite supply. |
| Mandatory instruction / ε conflict | Hard instruction holds even at high computing-loss cost; insufficient α/ε is infeasible, or a clearly failed diagnostic with U_site>0. |
| Priority / equal non-firm tier | Technically effective required non-firm interruption precedes firm denial; inability to comply cannot preserve NF imports through an exhausted α/ε. Swapping NFCD/Interim labels alone creates no new priority. Irrelevant distant relief is not forced. |
| Capacity-resource restriction | Interim event blocks prohibited generator-to-site supply; a dedicated non-capacity permitted case behaves differently and receives no duplicate grid capacity credit. |
| RA distinction | Changing N or interim H does not add FCD procurement; changing F changes the planning basis. Post-NITS activates its separately declared basis. |
| Upgrade state | Missing upgrades, PJM analysis or system updates prevents a legal transition flag; completed transition selects NITS, not FCD. |
| Annual hours and event accounting | Representative durations correctly weight MWh and ε; financial discounting does not change the physical budget; overlapping cause flags do not double-count C. |
| Ledger / emissions boundary | Fixed onsite cost included consistently; disutility counted once; allocation reconciles; onsite emissions included; curtailed load earns no generation/capacity credit. |
| Export / reload | Rebuilding from saved network plus versioned custom inputs reproduces contract constraints and preserves required custom result fields. |

## 8. Handoff and release conditions

TH-003 pins the environment; TH-004 implements firm/physical toy behavior; TH-005 supplies physical response evidence; TH-006 adds non-firm/Interim events and tests; TH-007 supplies the financial allocation ledger. Those assignments and the ≤30-run regional limit remain unchanged.

Proceed with a clearly identified **order-based / November-proposal research specification**, recording every synthetic operational input. Close Q1/Q2 before claiming an effective tariff implementation, Q3 before claiming exact PJM event sequencing, Q4 before claiming actual capacity settlement, and Q5 before claiming tariff prices. Source and engineering uncertainty must survive into configuration and results, not disappear during translation to code.
