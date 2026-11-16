# MS Renewable Energy Thesis — Shared Research Workspace

**Official TH-1 title:** Interconnection by Contract: Priority-Service Design for Gigawatt Data-Center Loads

**Status:** Research and model design phase. This repository is an AI-assisted collaboration workspace, **not** a completed, validated PJM or PyPSA-USA model.

## Thesis in one paragraph — student-approved working scope (16 November 2026)

> Gigawatt-scale data centres are asking for grid access faster than generation and transmission can be built. Regulators are responding with access contracts that trade firmness for speed. This thesis adds an open-source module to PyPSA-USA that represents firm, non-firm and interim non-firm access for a data-centre site, and applies it to a zonal PJM-relevant system for a forward year. Data-centre flexibility is entered as evidence-graded ranges, because metered curtailment at this scale is not public. The main result is the system cost avoided per GW as a function of the curtailment a data centre accepts, which gives a priority-service menu, together with curtailment, emissions and the incumbent-customer cost under two allocation rules. The model is zonal and deterministic: it does not establish site-level deliverability, N-1 security or probabilistic adequacy.

**Approval status:** Draft from [Claude's 16 November 2026 scope-refocus proposal](https://github.com/qasjadullah-design/MSRE-Thesis/blob/proposal/scope-refocus-2026-11-16/governance/proposals/SCOPE_REFOCUS_2026-11-16.md) for student/supervisor review. This is *not* a change to the official TH-1 objectives, title or six working milestone dates. In particular, the exact tariff treatment, generator eligibility, evidence-limited flexibility calibration, and cost-incidence method remain subject to verification/approval.

## Official research objectives (verbatim from submitted TH-1)
1. Develop an open-source PyPSA-USA module for firm, non-firm, and interim non-firm data-center grid-access contracts.
2. Calibrate data-center flexibility using observed behavior from FERC/PJM and Texas SB6 filings.
3. Quantify system cost, reliability, emissions, and incumbent ratepayer cost per GW of new load under each contract design.

## Current working milestones (user update: 23-Oct-2026)
| Milestone | Deadline |
|---|---|
| Literature Review | 31-Dec-2026 |
| Data Collection | 31-Jan-2027 |
| Data Analysis | 15-Mar-2027 |
| Model Deployment | **31-May-2027** |
| Result Evaluation | 30-Jun-2027 |
| Thesis and Article Write-up | 31-Jul-2027 |

**Schedule control (updated 23-Oct-2026):** The user explicitly set **31 May 2027** as the current model-deployment deadline. The earlier submitted TH-1 text in this repository cited 30 May; formal amendment/approval of the university form has not been verified. Keep the six current working dates unchanged absent another explicit revision. Defense date is not confirmed.

## Start here — every human or AI contributor
1. Read [AGENTS.md](AGENTS.md) and [governance/PROJECT_BRIEF.md](governance/PROJECT_BRIEF.md).
2. Check [governance/MILESTONES.md](governance/MILESTONES.md), [governance/DECISIONS.md](governance/DECISIONS.md), and [governance/TASKS.md](governance/TASKS.md).
3. Read [docs/MODEL_DESIGN.md](docs/MODEL_DESIGN.md) before editing optimization code.
4. Work on **one issue and a separate branch** at a time. Open a pull request and provide [governance/AGENT_HANDOFF.md](governance/AGENT_HANDOFF.md)-format results.
5. Do not claim a scenario is calibrated, a contract is effective, or a model is validated without source-specific evidence.

## Storage boundaries
- **GitHub:** Public-safe protocols, source registries, model code, configuration, checks, limited derived data and reproducible documentation.
- **Google Drive:** University-approved/signed documents, PDFs, large or restricted raw datasets, manuscript working copies and presentations.
- **Research Drive root:** https://drive.google.com/drive/folders/15TbBYQ9AJXmkqxy6zb2Wa5pEs9qv5PFd
- **TH-1/approvals folder:** https://drive.google.com/drive/folders/1W2uX-lJbb5A0ygus0ScFan5AO_eSfZ95

The GitHub repository is **public**. Do not upload the original signed TH-1, personal registration numbers, private correspondence, passwords, confidential filings, copyrighted full-text PDFs, or non-redistributable datasets here. Sharing Drive folder URLs here does not itself grant access.

## Student-approved research approach (working)
- **One question:** avoided incremental system cost for 1 GW of firm versus contractually interruptible large load, and residual incumbent-cost allocation.
- **One headline result:** annualized cost-versus-interruption frontier / hypothetical priority-service menu, not a real PJM tariff or approved discount.
- **Testbed:** PJM-relevant zonal 22 ReEDS-zone candidate (footprint/validation incomplete), modeled via forward-year capacity expansion and dispatch; one-week 2023 back-cast.
- **Site:** explicit co-located or qualified BTMG generator, POI and gross demand; generator outage permitted. G_installed=0 only a hypothetical load-only comparison, not automatic eligibility.
- **Experiments:** 1 GW principal, ~10 GW aggregate regional sensitivity, three chosen zones, epsilon sweep 0/0.25/0.5/1/2/5%, three evidence grades, interim pre/post-upgrade static cases; aim ≤30 regional full-year solves.
- **Outputs:** incremental real system costs, contractual curtailed MWh, involuntary firm-unserved MWh, CO2, and two illustrative socialized/cost-causation allocation bookends. Never equate physical resource costs with actual tariffs or bills.
- **Boundaries:** no site-level power flow/N-1, full tariff model, unit commitment, batteries/exports, dynamic workload shifting or Pakistan network.
- **Authority:** [Approved working decisions](governance/DECISIONS.md), [Chapter outline](writing/CHAPTER_OUTLINE.md), [Contract/module design](docs/MODEL_DESIGN.md). Supervisor/university confirmation of constrained proxies remains a separate administrative task.

## Current research status
The official topic, objectives and Annex B milestones are documented. **No field-calibrated flexibility dataset, validated regional baseline, implemented three-contract optimization, or numerical research findings have been verified as complete. The simplified allocation method is student-approved but has not generated validated outputs.**

For task ownership, see the issue tracker. For decisions requiring supervisor approval, see DECISIONS.md.
