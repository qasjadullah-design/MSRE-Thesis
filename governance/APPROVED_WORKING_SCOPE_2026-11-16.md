# Research scope approval and cross-agent execution handoff — 16 November 2026
**Decision:** The thesis student explicitly approved the [Claude scope-refocus proposal](https://github.com/qasjadullah-design/MSRE-Thesis/blob/proposal/scope-refocus-2026-11-16/governance/proposals/SCOPE_REFOCUS_2026-11-16.md) and its ChatGPT supporting PRs #8–#11 on 16 November 2026. This makes the narrower plan the project's **active working methodology**, not a formally amended TH-1. Supervisor/university agreement has NOT been independently verified.

## Unchanged authority
TH-1 title: Interconnection by Contract: Priority-Service Design for Gigawatt Data-Center Loads.
TH-1 Objectives: (1) open-source PyPSA-USA firm/NF/interim module; (2) calibrate actual flexibility from FERC/PJM and Texas SB6 filings; (3) assess system cost, reliability, CO2 and incumbent cost per GW. Wording unchanged.
Working milestone dates: 31 Dec 2026, 31 Jan 2027, 15 Mar 2027, **31 May 2027**, 30 Jun 2027, 31 Jul 2027. The earlier university form used 30 May for model deployment; formal amendment is not verified. No defense date is assumed.

## Approved working choices and safeguards
- Study incremental costs of firm vs interruptible grid access for **1 GW** of demand and allocation of remaining costs.
- Physical co-located/eligible BTMG generator in core site model. G_installed=0 is a hypothetical non-tariff counterfactual; the generator output may reach 0 due to an outage.
- Zonal PJM-relevant model for forward-year (2030) capacity expansion then dispatch, with **one-week 2023** historical back-cast, recognizing that the PJM ReEDS footprint is approximate and needs to be reproducible.
- One-zone ε sweep {0, .25, .5, 1, 2, 5}% for non-firm curtailment energy allowance, plus separate firm-contract benchmark (epsilon=0 is NOT legal firm by itself). Three zones, three physical flexibility grades and one ~10 GW **aggregate** sensitivity; ≤30 full-year regional solves.
- Interim NITS modeled in two static upgrade phases; after upgrades it becomes **full NITS**. Three contract categories remain distinct; tariffs/priority still require source verification.
- No detailed batteries/export/backlog, unit commitment, probabilistic adequacy, site-specific power-flow, full revenue-requirement model or Pakistan grid simulation.
- Primary: annualized system cost and contractual curtailment vs involuntary firm unserved load. Secondary: emissions including onsite generation and illustrative allocated incumbent costs under two bookends. Avoided-resource-cost menu is NOT an existing tariff/actual discount.
- Empirical calibration: evidence-class observed / trace-derived / assumed; absence of field measurements must not be concealed. Supervisor review required for how this meets verbatim Objective 2 and for the bounded proxies supporting Objective 3.

## Sources of implementation truth
1. [PROJECT_BRIEF](PROJECT_BRIEF.md)
2. [MODEL_DESIGN v0.2](../docs/MODEL_DESIGN.md)
3. [DECISIONS](DECISIONS.md)
4. [TASKS](TASKS.md)
5. [CHAPTER_OUTLINE](../writing/CHAPTER_OUTLINE.md)
6. [S1 legal framing](../regulatory/PROPOSED_S1_COLOCATION_FRAMING_2026-11-16.md) (historically named proposed; adopted framing subject to effective tariff verification)
The original proposal and supporting PRs remain an audit trail. Later evidence overrides unverified tariff assumptions, not approved research objectives or user-selected deadlines.

## First-stage delivery and responsibility
ChatGPT: TH-002 primary-rule table due 27 Nov, TH-005 flexibility evidence due 18 Dec, TH-007 allocation methods due 15 Jan, Ch.2/3 literature draft by 31 Dec.
Claude: TH-003 Linux PJM smoke or logged blocker due 27 Nov, TH-004 firm toy and reproducible tests by 18 Dec, TH-006 nonfirm/interim toy by 31 Jan, TH-008 2030 baseline & 2023 back-cast by 15 Mar, TH-009 scenarios by 31 May.

**Nothing in this approval log marks unexecuted code, source verification or manuscript chapters complete.**
