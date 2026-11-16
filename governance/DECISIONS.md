# Research decisions and open questions

| ID | Status | Decision or question |
|---|---|---|
| D01 | TH-1 approved | Official title and three objectives are fixed |
| D02 | User-updated working schedule (23-Oct-2026) | Six working dates; deployment is **31-May-2027**. Earlier TH-1 text said 30 May; formal amendment not verified. |
| D03 | Working decision (student, 16-Nov-2026) | PJM-relevant zonal testbed: 22 ReEDS zones extracted from PyPSA-USA v1.0.0. A one-day smoke run passes (TH-003); the extract is not validated against PJM outcomes |
| D04 | Working decision (student, 16-Nov-2026) | 1 GW nominal case plus one at-scale case of about 10 GW, in three zones. See governance/SCOPE.md 3.5 |
| D05 | Working decision (student, 16-Nov-2026) | Start with a tested 3–5 bus site/connection model (TH-004) |
| D06 | Open | Which FERC/PJM service rules and tariffs are effective, and when? |
| D07 | Open | Where are actual observed large-load curtailment/flexibility measurements? |
| D08 | Open | How to allocate recoverable costs/credits to incumbent customers? |
| D09 | Closed by D16 | Dispatch-only vs network/generation expansion scope |
| D10 | Open | University defense date and publication deliverable |
| D11 | Operational | GitHub is public, so keep university records in access-controlled Drive |
| D12 | Proposed (user preference 16-Nov-2026; supervisor approval pending) | The earlier from-scratch 2025 EIA dataset (zonal load, EIA-860 fleet) is not extended as a model. It is kept as an independent benchmark for the PyPSA-USA PJM extract. See docs/PJM_BASELINE_FEASIBILITY.md |
| D13 | Open | Execution environment for PyPSA-USA. The pinned environment cannot be imported on the Windows workstation (TH-003). Options: GitHub Actions for small runs, WSL2, cloud VM, university HPC |
| D14 | Working decision (student, 16-Nov-2026) | Back-cast for checking the PJM extract: one week of 2023. Upstream historical demand covers 2018-2023 only |
| D15 | Working decision (student, 16-Nov-2026); supervisor confirmation outstanding | S1: the three contract types are framed as the FERC/PJM co-location and eligible behind-the-meter-generation services. The core site has an installed generator; zero installed generation is a labelled hypothetical. Tariff effective status still to be checked in TH-002 |
| D16 | Working decision (student, 16-Nov-2026); supervisor confirmation outstanding | S2: forward-year capacity expansion, then dispatch of the resulting system |
| D17 | Working decision (student, 16-Nov-2026); supervisor confirmation outstanding | S3: zonal testbed; no site-level deliverability or congestion claims |
| D18 | Working decision (student, 16-Nov-2026); supervisor confirmation outstanding | S4: objective 2 is delivered as evidence-graded flexibility ranges (observed, derived, assumed), not as calibration to metered behaviour |
| D19 | Working decision (student, 16-Nov-2026); supervisor confirmation outstanding | S5: reliability is reported as curtailed and involuntarily unserved energy from a deterministic year; incumbent cost under two allocation rules. Neither is a probabilistic adequacy study or a tariff model |
| D20 | Approved by the student, 16-Nov-2026 | governance/SCOPE.md is the working plan and supersedes the scenario framework of docs/MODEL_DESIGN.md v0.1 |

No unapproved research assumptions may be presented as actual legal facts or calibrated measurements.