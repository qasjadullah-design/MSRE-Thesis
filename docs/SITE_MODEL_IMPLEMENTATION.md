# Site model: implementation note (TH-004)

- **What this is:** how the code in `src/dcaccess/` implements the firm-access part of `docs/MODEL_DESIGN.md` v0.2. The design document is the authority; this note records what exists, how it maps to the design, and what is still open.
- **Status:** firm access implemented and tested on a synthetic system. Non-firm and interim access are **not implemented** (TH-006). No regional result exists.
- **Every regulatory statement here is a modelling treatment**, hypothetical until TH-002 confirms it against effective tariff text.

## 1. Quantities kept separate

| Quantity | Symbol in the design | In the code (`SiteSpec`) |
|---|---|---|
| Gross facility demand | `D[t]` | `gross_load_mw` |
| Reserved firm MW | `F` (`firm_reserved_mw`) | `firm_mw` |
| Physical import capability | `POI_capacity` | `poi_capacity_mw` |
| Installed co-located generation; hourly output | `G`; `onsite_gen[t]` | `onsite_capacity_mw`; solved |
| Generator availability (0 = outage) | `availability[t]` | `onsite_availability` |
| Physical interruptible share | `alpha` | `flexible_share` |

`firm_mw` is an input. It is not computed from gross load or from the generator's capacity, as decision D15 and the design require.

## 2. Topology

```
grid bus ──[firm entitlement link, p_nom = F]──► meter bus ──[POI link, p_nom = POI_capacity]──► site bus
                                                                                                  ├─ gross load D[t]
                                                                                                  ├─ co-located generator, 0 ≤ onsite_gen[t] ≤ availability[t]·G
                                                                                                  ├─ voluntary curtailment, 0 ≤ C[t] ≤ alpha·D[t]
                                                                                                  └─ involuntary unserved load, 0 ≤ U[t] ≤ D[t]
```

The design draws "grid bus → POI link → site bus". The code adds one meter bus so that the contract (entitlement link) and the hardware (POI link) are two components. Non-firm service will be a second entitlement link into the same meter bus; the POI link then caps the sum of the services, which is the design's "both part of physical gross grid imports and POI cap, no double-counting", without a custom constraint.

Both links run one way: the site cannot export. Everything is a native PyPSA component, so the firm case needs no Linopy constraint and no change to upstream PyPSA-USA.

## 3. Equations as implemented

For every hour `t`, with `w[t]` the hours each snapshot represents:

- `grid_import[t] + onsite_gen[t] = D[t] − C[t] − U[t]` (the design's site balance, with firm shedding `U` made explicit)
- `0 ≤ grid_import[t] ≤ F`, and `grid_import[t] ≤ POI_capacity`; `F ≤ POI_capacity` is checked on input
- `0 ≤ onsite_gen[t] ≤ availability[t] · G`
- `0 ≤ C[t] ≤ alpha · D[t]`

Added to the system objective: `Σ w[t] · (m_g · onsite_gen[t] + k · C[t] + VOLL · U[t])`, with `m_g` the generator's operating cost, `k` the site's cost of lost computing and `VOLL` the penalty on involuntary unserved load. `k < VOLL` is enforced, so flexibility is used before anyone is shed.

Consequences checked by the tests:

- **A contract limit does not shed computing load.** If `F + availability·G < D` and `alpha = 0`, the gap is involuntary unserved load `U`, never curtailment `C`. This is the design's "never silently classify" rule seen from the firm side.
- **Firm priority.** Site unserved load carries the same penalty as other firm load, so the optimiser has no preference about who is shed in a shortage. This ranking is a modelling assumption pending tariff verification.

## 4. Resource-adequacy treatment (issue #3 asks for this to be explained)

In the synthetic system adequacy is **implicit**: with expansion allowed, firm load is met by building capacity because shedding it costs `VOLL`. Test A9 shows this. That is a proxy, not a planning rule.

For the regional model the design asks for the "distinct firm resource-adequacy obligation using existing PyPSA-USA reserve-margin formulation where viable". Not implemented. Two candidates:

1. Add `F` to the load that upstream's energy reserve margin constraint (`add_ERM_constraints`, `workflow/scripts/opts/reserves.py`) must cover, and leave non-firm MW out of it.
2. If that needs large upstream changes, require new capacity of `F × (1 + reserve factor)` in the site's zone, labelled as a proxy.

I have confirmed that the upstream function exists but have not read it in detail. The choice belongs to TH-006.

## 5. Cases covered

| Case | How it is set | State |
|---|---|---|
| Generator available | `onsite_availability = 1` | tested |
| Generator outage, all or some hours (installed, zero output) | `onsite_availability = 0` in those hours | tested |
| No physical flexibility | `flexible_share = 0` | tested |
| Constrained transfer into the zone | scale the zone's transfer links | tested |
| Tight system with expansion allowed | scale loads, `expansion=True` | tested |
| Zero installed generation | `onsite_capacity_mw = 0` | tested; **hypothetical comparison only**, not an eligible co-location arrangement (D15) |

## 6. Accounting (`dcaccess.accounting`)

- **Site balance** by hour: gross load, firm withdrawal, grid import, onsite output, curtailed, unserved, served, residual.
- **Cost breakdown**, annual: generation (including onsite fuel), site curtailment disutility, site unserved penalty, system unserved penalty, investment. The parts do not overlap and sum to the solver's objective.
- **Emissions**, tCO2 per generator: electricity ÷ efficiency × the carrier's factor, one rule for onsite and grid units.

These are physical-system costs of the optimisation, not tariffs, revenue requirements or bills. The site's curtailment disutility is **inside** the system cost here, so when `V(epsilon)` is computed later it must not be subtracted a second time (design, "Annual curtailment tolerance sweep").

The solve wrapper raises an error unless HiGHS reports an optimal solution.

## 7. Acceptance tests

| # | Requirement | Tests in `tests/test_firm_access.py` | State |
|---|---|---|---|
| A1 | A site with zero load leaves the system objective unchanged | `test_zero_load_site_matches_baseline` | passes |
| A2 | Withdrawals never exceed the reserved firm MW or the POI capability; no export | `test_firm_withdrawal_never_exceeds_entitlement`, `test_entitlement_binds_…`, `test_poi_limit_binds_…`, `test_site_cannot_export` | passes |
| A3 | Site energy balance closes in every hour | `test_site_balance_closes` (4 cases) | passes |
| A4 | With zero flexibility a contract limit cannot shed computing load; flexibility caps curtailment | `test_zero_flexibility_shortfall_is_involuntary_not_curtailment`, `test_curtailment_is_capped_by_physical_flexibility` | passes |
| A5 | Stress cases give the quantities arithmetic predicts | `test_partial_generator_outage_…`, `test_hypothetical_site_without_generator_…`, `test_constrained_transfer_gives_the_predicted_shortfall` | passes |
| A6 | Non-firm interruption respects the energy tolerance and the service order | none yet | TH-006 |
| A7 | Interim before and after upgrade use the right treatment and network | none yet | TH-006 |
| A8 | Cost parts sum to the objective; emissions reconcile | `test_cost_parts_sum_to_objective` (2 cases), `test_emissions_reconcile` | passes |
| A9 | With expansion allowed, firm load is met by new capacity, not unserved energy | `test_firm_load_triggers_capacity_instead_of_unserved_energy` | passes |
| A10 | On the PJM extract, a zero-load site reproduces the upstream baseline within solver tolerance | none yet | TH-008 |
| A11 | Runs are reproducible: command, versions, solver recorded | `python -m dcaccess`; workflow `tests.yml` | in place for the synthetic system |

"Passes" means the test ran and passed on the versions named in `governance/handoffs/TH-004.md` (CI run 43822507888: Python 3.11.18, PyPSA 1.3.0, Linopy 0.9.1, the versions pinned by PyPSA-USA v1.0.0; and on current releases).

## 8. The synthetic test system

`dcaccess.toy.build_toy_network` builds three zones (A generation-rich, B load centre, C the site's host) joined by transfer limits, with seven generators, a diurnal load shape and a deterministic wind profile, over 48 hours weighted to one year. Switches scale loads, scale individual transfer limits and allow new peaking capacity at an annualised cost.

**Every number in it is invented**: capacities, costs, emission factors, the 10,000 per MWh penalty, the 2,000 per MWh cost of lost computing. It exists to test behaviour. Nothing it produces is a finding about PJM or about data centres.

## 9. Planned extension for TH-006 (not implemented)

- Second entitlement link with `p_nom = nonfirm_reserved_mw`, optionally with a time-varying availability for curtailment events.
- One Linopy constraint for the annual tolerance: `Σ w[t]·C_contract[t] ≤ epsilon/100 · Σ w[t]·D[t]`, with `epsilon ∈ {0, 0.25, 0.5, 1, 2, 5}` and the firm case kept as a separate benchmark (D20).
- Interim NITS as two static cases; after the upgrade the whole withdrawal is treated as full NITS.
- In PyPSA-USA the constraint would be added in `extra_functionality` in `workflow/scripts/solve_network.py`, which has no plug-in hook: one small documented patch calling a function kept in this repository.

## 10. Sources

- Design and decisions: `docs/MODEL_DESIGN.md` v0.2, `governance/DECISIONS.md`, `governance/APPROVED_WORKING_SCOPE_2026-11-16.md`.
- Regulatory framing: `regulatory/PROPOSED_S1_COLOCATION_FRAMING_2026-11-16.md`. I relied on that memo and have not read the FERC orders myself.
- Upstream hook points: PyPSA-USA v1.0.0, `workflow/scripts/solve_network.py` and `workflow/scripts/opts/reserves.py`.
