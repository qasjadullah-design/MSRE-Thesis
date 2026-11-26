# Decisions register — MSRE thesis
**Status as of 16 November 2026:** The student explicitly **approved the 16 November scope-refocus proposal and supporting PRs #8–#11 as the active working project direction**. This does not represent a verified supervisor/university approval of changes in interpretation of TH-1 objectives, nor an enacted legal tariff.

| ID | Status | Decision and limits |
|---|---|---|
| D01 | Official TH-1 unchanged | Title: *Interconnection by Contract: Priority-Service Design for Gigawatt Data-Center Loads*; three verbatim objectives unchanged |
| D02 | User-approved schedule | M1 Dec 31 2026; M2 Jan 31 2027; M3 Mar 15; M4 **May 31**; M5 Jun 30; M6 Jul 31. Earlier submitted TH-1 said May 30 for M4; formal amendment not verified |
| D03 | User-approved working method | PJM-relevant **zonal** regional testbed; no site-specific network congestion claims; real PJM baseline validation still pending |
| D04 | User-approved working method | Principal 1 GW scenario, plus ~10 GW **aggregate regional load** case; 3 location zones; normalized incremental costs per GW-year |
| D05 | User-approved working method | Develop/test 3–5-bus physical site and firm-service prototype first |
| D06 | Dated research findings; implementation evidence gates remain | [TH-002 comparison, 26 Nov 2026](../regulatory/TH-002_CONTRACT_MATRIX_2026-11-26.md) distinguishes ordered framework from November proposed implementation. Current effective-record/clean-sheet verification, manual details and settlement mechanics remain open in its source audit; no new scope approval is implied |
| D07 | Open empirical limitation | Evidence-graded physical flexibility parameters: actual delivered measured vs trace-modeled vs assumed (TH-005); supervisor acceptance for Objective 2 pending |
| D08 | User-approved working method | TWO illustrative allocation bookends socialized vs direct cost causation; not actual PJM tariffs/bills; financial incidence assumptions require checks |
| D09 | User-approved working method | Forward-year capacity expansion followed by dispatch; reserve-margin integration feasibility requires TH-004 testing |
| D10 | Open administration | Defense date, university TH-1 revised submission and supervisor acknowledgement not verified |
| D11 | Operational | Repository public. Original signed university documents, private messages and restricted raw data stay on controlled Drive |
| D12 | User-approved working boundary | Earlier local 2025 EIA reconstruction is an independent *benchmark only*, not a parallel model-development workstream; source and licensing checks pending |
| D13 | Partially resolved / infrastructure | GitHub Linux Actions for smoke/toy tests. Full-year expansion execution environment (Linux VM/HPC) still to be selected based on demonstrated resource requirements |
| D14 | User-approved method | Candidate historical validation: **one-week 2023 back-cast**, provided accessible data and EIA API key. Not a completed validation |
| D15 / S1 | User-approved framing; supervisor endorsement unverified | Core FERC co-located / eligible BTMG access classes with one physically modeled generator; G_installed=0 is hypothetical load-only analog, not automatically FERC eligible. Onsite outage with G_installed>0 and P_onsite=0 is allowed. Current tariff status and remaining evidence gates recorded in the 26 Nov TH-002 comparison |
| D16 / S2 | User-approved method; supervisor endorsement unverified | Forward-year capacity expansion, then dispatch. Fallback to representative periods if full-year computationally infeasible and disclosed |
| D17 / S3 | User-approved method; supervisor endorsement unverified | Zonal PJM testbed, no claim of POI congestion, N-1 security, or site deliverability |
| D18 / S4 | User-approved working method; supervisor endorsement **required** | Evidence-bounded observed/derived/assumed ranges, transparently graded. Cannot claim this satisfies Objective 2's wording on observed behavior without supervisor discussion |
| D19 / S5 | User-approved working method; supervisor endorsement **required** | Deterministic energy-reliability proxies + two cost allocation bookends; no claim of probabilistic adequacy or actual incumbent electricity bills |
| D20 | Technical safeguard | Epsilon=0 curtailment tolerance is not itself legal firm service; compare distinct firm and nonfirm cases. Interim NITS converts to **full NITS**, not automatically FCD |
| D21 | Economic safeguard | Avoided social system cost provides at most a conditional reference bound for a *hypothetical* priority service discount, not an established rate or ratepayer benefit |

## Internal scope control
- **Main question:** for 1 GW of new site demand, how much system cost is avoided under contractually accepted interruptions, and who bears the remaining cost?
- **Headline:** annualized avoided-cost vs physical and contractual interruption frontier, not generic data-center forecast.
- **Execution:** contract module on toy network → PJM 22 ReEDS-zone approximation → limited regional scenario run budget (≤30 full-year solves).
- **Excluded core extensions:** site-specific power flow; full tariff model; unit commitment; storage/export; dynamic workload backlog and spatial relocation; probabilistic reliability; Pakistan grid case.
- **Sources:** original [Claude proposal](https://github.com/qasjadullah-design/MSRE-Thesis/blob/proposal/scope-refocus-2026-11-16/governance/proposals/SCOPE_REFOCUS_2026-11-16.md), [S1 memo](../regulatory/PROPOSED_S1_COLOCATION_FRAMING_2026-11-16.md), [model design v0.2](../docs/MODEL_DESIGN.md).

**Approval rule:** Student approved working scope on Nov 16, 2026; supervisor/university signatures are **not assumed**. Future agents must execute the accepted plan, not seek routine user reapproval of already selected working assumptions. Escalate only new evidence conflicts, missing real-world data, budget feasibility, or changes requiring supervisor signoff.
