# PyPSA-USA contract-access module — proposed design v0.1
Status: DESIGN ONLY. No validated model, observed parameters or numerical outcomes are claimed.

## Goal and distinction
Reuse an existing U.S. grid modeling framework, not recreate PJM from scratch. Research novelty is mapping legally meaningful firm CDS, nonfirm CDS and interim NITS access into explicit network-connected variables/constraints; calibrating physical flexibility; and allocating costs to incumbent consumers. Verify effective tariff versions before interpreting terms as enforceable.

## Architecture
- Audit, version-pin and reproduce upstream PyPSA-USA. Existing eastern U.S. capabilities do not automatically imply a calibrated PJM testbed.
- Site as grid bus -> constrained point-of-interconnection/contract service -> internal site bus -> data-center demand and optional onsite generation/storage/exports. Account gross MW and net grid MW separately.
- Use independently tested modular Linopy/PyPSA constraints with controlled hooks instead of rewriting upstream files.
- 3–5 bus synthetic network first, then PJM-relevant regional baseline. Use 24–72 hour chronological snapshots in first tests; evaluate full-year practicality later.

## Draft variables / energy balances
D_i,t baseline facility electrical load MW; C_i,t nonrecoverable curtailment; X_i,t workload shift-out; Y_i,t make-up work; L_i,t served electrical load.
L_i,t = D_i,t - C_i,t - X_i,t + Y_i,t >= 0.
Pgrid_i,t + Ponsite_i,t + Pdischarge_i,t = L_i,t + Pcharge_i,t + Pexport_i,t + electrical losses.
0 <= Pfirm_i,t <= FirmCapacity_i; 0 <= Pnonfirm_i,t <= NonFirmReservation_i,t; also <= approved availability/curtailment event bound. Pgrid=Pfirm+Pnonfirm+any properly defined interim stream with no double counting. Combined gross imports <= POI physical import capability.
Interim NITS operates under interim service terms prior to a specified upgrade; post-upgrade scenario has relevant full NITS and network upgrades, not automatically firm CDS.
0 <= C_i,t <= alpha_i,t*D_i,t with empirically justified alpha (or explicitly hypothetical). Energy-shift backlogs need recovery/deadline and power limits. Curtailment priority must reflect actual dated rules or a labeled hypothetical policy; don't assign arbitrary penalty ranking as if law.

## Optimization and accounting
Operational objective: physical generation/storage costs plus attributable flexibility/curtailment disutility, investment where modeled, and distinct involuntary unserved firm-demand penalty. Avoid re-adding costs already in PyPSA.
After solve, account incremental recoverable revenue requirement, developer payments, credits and residual incumbent allocation. Report $/GW and exact time horizon (annual vs net present value). Dispatch cost is NOT the ratepayer's bill.

## Scenario framework (pending approval)
B0 no data center; B1 conventional 1 GW fully firm access; C1 firm CDS, C2 nonfirm CDS, C3 interim NITS; same physical site and grid context. Primary scale 1 GW with 0.1/0.5/2 GW sensitivity, dispersed vs concentrated sites, physical flexibility none/low/evidence based, grid congestion, onsite outages, pre/post upgrade. Clearly distinguish hypothetical parameter sets and observed calibration.

## Metrics
Incremental annual/period operating and infrastructure cost, non-firm contractual curtailment vs involuntary firm unserved MWh, peak MW, congestion and stress indicators, emissions including onsite/backup (tCO2), network/generation investment, net attributed incumbent ratepayer cost per GW.
A dispatch model doesn't prove N-1 security or probabilistic adequacy without separate formal methods.

## Test acceptance
1. Zero-load base matches upstream baseline, within solver tolerance.
2. Never exceed contract-specific or physical POI import capacities.
3. Site nodal energy balance holds.
4. Zero actual flexibility cannot shed computing load by merely exercising a legal grid-disconnection right.
5. Shifting recovers within permitted window.
6. Nonfirm interruption obeys verified trigger/service order.
7. Interim-to-full NITS transition changes rules and network correctly.
8. Cases with no onsite generation, onsite failure, constrained transmission and infeasibility produce explainable behavior.
9. Reconcile emissions and cost components without double counting.
10. Record reproducible run commands, snapshots, solver, data vintage and source provenance.

## Stage 1 delivery from Claude
Inspect upstream and actual PJM build feasibility; provide reproducible configuration, exact commit/environment, proposed Linopy constraints and regulatory question list. Then implement smallest firm-only synthetic proof of concept on a feature branch and submit code/tests/PR for review. Do not implement entire project at once.

## Source starting points
- https://github.com/PyPSA/pypsa-usa
- https://pypsa-usa.readthedocs.io/
- https://docs.pypsa.org/latest/user-guide/optimization/custom-constraints/
- https://www.ferc.gov/
- https://www.pjm.com/
- https://capitol.texas.gov/tlodocs/89R/billtext/html/SB00006F.htm

All regulatory provisions require docket/order/effective-status checks prior to final parameterization.