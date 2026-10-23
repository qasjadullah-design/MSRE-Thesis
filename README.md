# MS Renewable Energy Thesis — Shared Research Workspace

**Official TH-1 title:** Interconnection by Contract: Priority-Service Design for Gigawatt Data-Center Loads

**Status:** Research and model design phase. This repository is an AI-assisted collaboration workspace, **not** a completed, validated PJM or PyPSA-USA model.

## Thesis in one paragraph
Gigawatt-scale data-center demand creates questions about transmission access, interruption rights, electricity-system reliability, infrastructure costs, emissions and who pays. The submitted NUST TH-1 proposes a reusable, open-source **PyPSA-USA extension** to represent **firm, non-firm, and interim non-firm** grid-access arrangements, to calibrate the physical flexibility of data centers from available real-world evidence (FERC/PJM and Texas SB6-related material), and to compare system and incumbent-ratepayer consequences per GW of new demand using a U.S. grid testbed.

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

## Preferred research workflow
- PJM-relevant region is the **working preference**, not a verified completed PJM testbed.
- 1 GW is a **proposed normalized comparison size**, not a legal threshold or a verified forecast for an individual site.
- Separate contractual **rights to withdraw grid power** from the site's **physical capability to supply, shift or curtail workload**.
- Separate **real system costs** from **tariff revenue requirements, charges and transfers** when measuring incumbent consumer impacts.
- Start with a tiny tested synthetic network; reuse a reproducible, vetted PyPSA-USA regional system only after investigating its geographic and operational validity.

## Current research status
The official topic, objectives and Annex B milestones are documented. **No field-calibrated flexibility dataset, regional baseline, implemented contract constraints, approved ratepayer method, or numerical research results have been verified as complete.**

For task ownership, see the issue tracker. For decisions requiring supervisor approval, see DECISIONS.md.
