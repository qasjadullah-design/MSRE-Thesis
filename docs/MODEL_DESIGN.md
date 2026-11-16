# Contract-access module: model design v0.2

- **Status:** firm access is implemented and tested on a synthetic system (TH-004). Non-firm and interim access are designed here and **not implemented**. No regional result exists.
- **Basis:** `governance/SCOPE.md`, the working plan approved by the student on 16 November 2026. Supervisor confirmation of decisions D15 to D19 is outstanding.
- **Replaces:** v0.1 (21 October 2026). Section 9 lists what changed.
- **Every regulatory statement here is a modelling treatment.** It is hypothetical until TH-002 confirms it against effective tariff text.

## 1. What the module does

It attaches a data-centre site to one bus of a PyPSA network and represents the site's grid-access contract as limits on what it may withdraw. The network can be the synthetic test system in this repository or the zonal PJM extract built by PyPSA-USA v1.0.0 (22 zones joined by transfer limits).

Four quantities are kept apart throughout. The FERC orders treat them as distinct, and so does the code:

| Quantity | Symbol | In the code (`SiteSpec`) |
|---|---|---|
| Gross facility demand | `D_t` | `gross_load_mw` |
| Contracted firm withdrawal | `F` | `firm_mw` |
| Physical import capability at the point of interconnection | `P_poi` | `poi_capacity_mw` |
| Installed co-located generation, and its hourly output | `G`, `g_t` | `onsite_capacity_mw`, solved |

`F` is an input. It is not computed from `D` or `G`.

## 2. Site topology

```
grid bus ──[firm entitlement link, p_nom = F]──► meter bus ──[POI link, p_nom = P_poi]──► site bus
                                                                                           ├─ gross load D_t
                                                                                           ├─ co-located generator, 0 ≤ g_t ≤ a_t·G
                                                                                           ├─ voluntary curtailment, 0 ≤ c_t ≤ α·D_t
                                                                                           └─ involuntary unserved load, 0 ≤ u_t ≤ D_t
```

- Both links run one way, so the site cannot export.
- The entitlement link is the contract. The POI link is the hardware. Non-firm service will be a second entitlement link into the same meter bus, so the POI link caps the sum of all services without a custom constraint.
- Everything is a native PyPSA component. The firm case needs no Linopy constraint and no change to upstream PyPSA-USA.

## 3. Equations (firm access, implemented)

For every hour `t`, with `w_t` the hours each snapshot represents:

- Site balance: `p_t + g_t + c_t + u_t = D_t`, where `p_t` is the grid import.
- Contract: `0 ≤ p_t ≤ F`.
- Connection: `p_t ≤ P_poi`, with `F ≤ P_poi` checked on input.
- Generator: `0 ≤ g_t ≤ a_t · G`. Availability `a_t = 0` is an outage.
- Physical flexibility: `0 ≤ c_t ≤ α · D_t`.
- Served load: `D_t − c_t − u_t`.

Added to the system objective: `Σ_t w_t · (m_g · g_t + k · c_t + VOLL · u_t)`, where `m_g` is the generator's operating cost, `k` the site's cost of lost computing, and `VOLL` the penalty for involuntary unserved load. `k < VOLL` is required, so flexibility is used before anyone is shed.

Two consequences that the tests check:

- **A contract limit does not shed computing load.** If `F + a_t·G < D_t` and `α = 0`, the gap is involuntary unserved load. It is never reported as curtailment.
- **Firm priority.** Site unserved load carries the same `VOLL` as other firm load, so the optimiser has no reason to shed the site before, or after, incumbent customers. This is the "curtailed last, with other firm load" treatment of `SCOPE.md` 3.2.

### Adequacy treatment: open design point

`SCOPE.md` 3.2 says firm load is "counted at contracted MW" for adequacy. In the test system adequacy is implicit: with expansion allowed, firm load is met by building capacity because shedding it costs `VOLL`. For the regional model there are two candidate explicit treatments, and neither is implemented:

1. Include `F` in the load that upstream's energy reserve margin constraint (`add_ERM_constraints`, `workflow/scripts/opts/reserves.py`) must cover, and exclude non-firm MW from it.
2. If that needs large upstream changes, require new capacity of `F × (1 + reserve factor)` in the site's zone.

The choice is made in TH-006 after reading that constraint in detail.

## 4. Non-firm and interim access (designed, not implemented: TH-006)

| Access | Added component | Added constraint | Curtailment cost falls on |
|---|---|---|---|
| Non-firm | second entitlement link, `p_nom = N` (contracted non-firm MW) | annual energy budget: `Σ_t w_t · x_t ≤ ε · Σ_t w_t · D_t`, where `x_t` is the withdrawal the system declines to serve | the site: onsite fuel, or lost computing within `α` |
| Interim, before upgrade | as non-firm | as non-firm, on the pre-upgrade transfer limits | the site |
| Interim, after upgrade | none: treated as firm for the whole withdrawal | none, on the upgraded transfer limits | the system |

Points fixed by the approved plan:

- **Service state and ε are separate.** Firm access is its own case. A non-firm case with `ε = 0` is not a firm contract: it has no adequacy treatment and a different priority.
- **Interim converts to full network service (NITS)**, not to Firm Contract Demand.
- **How the system "declines to serve" is a modelling device.** Non-firm withdrawal will be given a lower priority than firm load through cost ranking. The ranking stands in for the service order and is labelled as such; it is not tariff text.
- The energy budget is the only custom Linopy constraint foreseen. In PyPSA-USA it would be added in `extra_functionality` in `workflow/scripts/solve_network.py`, which has no plug-in hook. The plan is one small documented patch that calls a function kept in this repository.

## 5. Stress cases

| Case | How it is set | Status |
|---|---|---|
| Generator available | `a_t = 1` | tested |
| Generator outage, all or some hours | `a_t = 0` in those hours | tested |
| No physical flexibility | `α = 0` | tested |
| Constrained transfer into the zone | scale the zone's transfer links | tested |
| Tight system with expansion allowed | scale loads, `expansion=True` | tested |
| Zero installed generation | `G = 0` | tested; **hypothetical counterfactual only**, not an eligible co-location arrangement |

Cut from v0.1: batteries, exports, electrical losses, and workload shifting with backlog and recovery. Shifting may return as one sensitivity through upstream's `demand_response` option.

## 6. Accounting

`dcaccess.accounting` produces, per solved case:

- **Site balance** by hour: gross load, firm withdrawal, grid import, onsite output, curtailed, unserved, served, residual.
- **Cost breakdown**, annual: generation (including onsite fuel), site curtailment disutility, site unserved penalty, system unserved penalty, investment. The parts do not overlap and sum to the solver's objective.
- **Emissions**, tCO2 per generator: electricity ÷ efficiency × the carrier's factor, so onsite and grid emissions use one rule.

These are physical-system costs of the optimisation. They are not tariffs, revenue requirements or bills. The incumbent-cost rules A and B of `SCOPE.md` 3.7 are applied after the solve and belong to TH-007.

When the interruptibility value `V(ε)` is computed later, each figure must state whether the site's curtailment disutility is inside the system cost. In this module it is inside (`site curtailment` is part of the objective), so it must not be subtracted again.

## 7. Acceptance tests

| # | Requirement | Test in `tests/test_firm_access.py` | State |
|---|---|---|---|
| A1 | A site with zero load leaves the system objective unchanged | `test_zero_load_site_matches_baseline` | passes |
| A2 | Withdrawals never exceed the entitlement or the POI capability; no export | `test_firm_withdrawal_never_exceeds_entitlement`, `test_entitlement_binds_…`, `test_poi_limit_binds_…`, `test_site_cannot_export` | passes |
| A3 | Site energy balance closes in every hour | `test_site_balance_closes` (4 cases) | passes |
| A4 | With zero flexibility, a contract limit cannot shed computing load; flexibility caps curtailment | `test_zero_flexibility_shortfall_is_involuntary_not_curtailment`, `test_curtailment_is_capped_by_physical_flexibility` | passes |
| A5 | Stress cases give the quantities arithmetic predicts | `test_partial_generator_outage_…`, `test_hypothetical_site_without_generator_…`, `test_constrained_transfer_gives_the_predicted_shortfall` | passes |
| A6 | Non-firm interruption respects the energy budget and the service order | none yet | TH-006 |
| A7 | Interim before and after upgrade use the right treatment and network | none yet | TH-006 |
| A8 | Cost parts sum to the objective; emissions reconcile | `test_cost_parts_sum_to_objective` (2 cases), `test_emissions_reconcile` | passes |
| A9 | With expansion allowed, firm load is met by new capacity, not unserved energy | `test_firm_load_triggers_capacity_instead_of_unserved_energy` | passes |
| A10 | On the PJM extract, a zero-load site reproduces the upstream baseline within solver tolerance | none yet | TH-008 |
| A11 | Runs are reproducible: command, versions, solver and data vintage recorded | `python -m dcaccess`; CI workflow `tests.yml` | in place for the synthetic system |

"Passes" means the test ran and passed on the versions named in `governance/handoffs/TH-004.md`.

## 8. The synthetic test system

`dcaccess.toy.build_toy_network` builds three zones (A generation-rich, B load centre, C the site's host) joined by transfer limits, with seven generators, a diurnal load shape and a deterministic wind profile, over 48 hours weighted to one year. Optional switches scale loads, scale individual transfer limits and allow new peaking capacity at an annualised cost.

**Every number in it is invented**: capacities, costs, emission factors, the 10,000 per MWh penalty, the 2,000 per MWh cost of lost computing. It exists to test behaviour. Nothing it produces is a finding about PJM or about data centres.

## 9. Changes from v0.1

| v0.1 | v0.2 |
|---|---|
| Design only | Firm access implemented, 23 tests |
| Onsite generation optional | Installed generator is part of the core site; `G = 0` is a labelled hypothetical |
| Firm and non-firm as bounds on one import variable plus a combined POI constraint | Separate entitlement links into a meter bus; the POI link caps their sum |
| Shift-out, make-up and backlog variables | Cut from the core |
| Storage, exports, losses | Cut |
| Interim as a transition | Two static cases; after upgrade is full NITS |
| Sizes 0.1 to 2 GW; dispersed vs concentrated; congestion and outage axes | 1 GW and about 10 GW; three zones; outage is a stress case |
| Post-solve revenue accounting | Two allocation rules, TH-007 |
| Ten acceptance tests | Eleven, renumbered; A6, A7 and A10 not yet testable |

## 10. Sources

- Scope and decisions: `governance/SCOPE.md`, `governance/DECISIONS.md`.
- Regulatory framing of the four separate quantities and of `G = 0`: ChatGPT's primary-source memo on S1 (draft PR #10), citing FERC 193 FERC ¶ 61,217 (2025) and 195 FERC ¶ 61,209 (2026). I have not read those orders myself.
- Upstream hook points: PyPSA-USA v1.0.0, `workflow/scripts/solve_network.py` and `workflow/scripts/opts/reserves.py` (existence checked; the reserve constraint not yet read in detail).
