# Project brief — approved TH-1 scope

Official title: **Interconnection by Contract: Priority-Service Design for Gigawatt Data-Center Loads**.
Supervisor: Dr. Kashif Imran.
TH-1 research scope: an open-source PyPSA-USA module to compare firm, non-firm and interim non-firm grid-access designs for gigawatt-scale data centers. Use evidence of real-world flexibility where available from FERC/PJM and Texas SB6-related filings; quantify system cost, reliability, CO2 and incumbent ratepayer cost per GW on a U.S. grid testbed. No findings have yet been established.

Verbatim objectives:
1. Develop an open-source PyPSA-USA module for firm, non-firm, and interim non-firm data-center grid-access contracts.
2. Calibrate data-center flexibility using observed behavior from FERC/PJM and Texas SB6 filings.
3. Quantify system cost, reliability, emissions, and incumbent ratepayer cost per GW of new load under each contract design.

Rationale: rapid large-load growth raises grid planning, reliability and who-pays questions; regulatory rights and actual flexible behavior must be separately established. Relevance to Pakistan is transfer of a transparent analytic framework, NOT a primary Pakistan grid simulation.

## Student-approved working scope — 16 November 2026

> Gigawatt-scale data centres are asking for grid access faster than generation and transmission can be built. Regulators are responding with access contracts that trade firmness for speed. This thesis adds an open-source module to PyPSA-USA that represents firm, non-firm and interim non-firm access for a data-centre site, and applies it to a zonal PJM-relevant system for a forward year. Data-centre flexibility is entered as evidence-graded ranges, because metered curtailment at this scale is not public. The main result is the system cost avoided per GW as a function of the curtailment a data centre accepts, which gives a priority-service menu, together with curtailment, emissions and the incumbent-customer cost under two allocation rules. The model is zonal and deterministic: it does not establish site-level deliverability, N-1 security or probabilistic adequacy.

**Adopted working choices:** forward-year capacity expansion followed by dispatch; zonal PJM-relevant testbed; primary 1 GW and ~10 GW aggregate regional sensitivity; three selected zones; epsilon tolerance sweep; two deliberately simplified incumbent-cost allocation scenarios. Physical site topology includes a co-located generator or qualifying BTMG and separates generator capability from actual output, contract entitlement and physical site curtailment. G_installed=0 is a hypothetical comparison only. The proposed headline is annualized avoided system cost vs accepted interruption, with any illustrative discount conditional, not an actual tariff. The formal TH-1 objectives remain unchanged; supervisor confirmation for evidence-bounded calibration and cost/reliability proxies is not verified.

**Status:** Student-approved working plan, sourced to the [16 November proposal](https://github.com/qasjadullah-design/MSRE-Thesis/blob/proposal/scope-refocus-2026-11-16/governance/proposals/SCOPE_REFOCUS_2026-11-16.md) and [S1 primary-source analysis](../regulatory/PROPOSED_S1_COLOCATION_FRAMING_2026-11-16.md). Working decisions S1–S5 recorded in [DECISIONS](DECISIONS.md); supervisor acknowledgement remains pending for the objective/proxy interpretations. Implementation details: [MODEL_DESIGN v0.2](../docs/MODEL_DESIGN.md).

Private official TH-1: https://drive.google.com/drive/folders/1W2uX-lJbb5A0ygus0ScFan5AO_eSfZ95 (the actual PDF still needs uploading). Do NOT add signed forms to this public repository.