> **ARCHIVED DRAFT / STUDENT-APPROVED 16 NOV 2026.** Statements below saying 'proposed' or 'not approved' describe the file's historical state prior to user approval. Current authoritative instructions: [Working Scope](https://github.com/qasjadullah-design/MSRE-Thesis/blob/main/governance/APPROVED_WORKING_SCOPE_2026-11-16.md), [Model Design v0.2](https://github.com/qasjadullah-design/MSRE-Thesis/blob/main/docs/MODEL_DESIGN.md), and [Chapter Outline](https://github.com/qasjadullah-design/MSRE-Thesis/blob/main/writing/CHAPTER_OUTLINE.md). Supervisor/university signoff remains unverified.

> **26 November 2026 source correction and follow-up:** TH-002 corrects the June-order locator below: the former “¶635” was **footnote 635 to paragraph 263**, printed p.132; the BTMG-extension determination is **¶91**, pp.51–52. See the [dated contract comparison](TH-002_CONTRACT_MATRIX_2026-11-26.md), [source audit](../references/TH-002_SOURCE_AUDIT_2026-11-26.md), and [implementation requirements](../docs/TH-002_PYPSA_REQUIREMENTS_2026-11-26.md). November 16 implementing provisions request future effectiveness; the proposed ordinary-Large-Load extension does not silently change the student-approved core. This correction/addendum preserves the memo's historical recommendation and approval history.

# S1 — PRIMARY-SOURCE FRAMING MEMO (PROPOSED; NOT APPROVED)
Date 16 November 2026. A response to Section 9 / S1 of the Claude scope-refocus proposal. It is not a change to the submitted TH-1.

## Question
Does the core thesis model FERC co-located load contract-demand classes, or any grid-connected large load? Must it include a co-located generator? What does G=0 mean?

## Recommendation requiring supervisor approval
Keep the core regulatory case as co-located loads and qualifying behind-the-meter-generation (BTMG) arrangements, with explicit generator-site representation. A zero-output generator outage (installed generator >0 but dispatched MW=0) is a valid stress test. A zero-installed-generator case is a hypothetical engineering counterfactual and should NOT be portrayed as automatically eligible for the cited FCD/NFCD/Interim NITS arrangements.

## Primary evidence
1. **FERC December 18, 2025, 193 FERC ¶61,217** ([order](https://www.ferc.gov/sites/default/files/2025-12/E-1%20EL25-49-000.pdf), ¶189–193). The proceeding concerns loads served by existing/planned generating facilities in co-location arrangements and directs service choices NITS/Interim NITS, Firm Contract Demand (FCD), and Non-Firm Contract Demand (NFCD). Include generator-POI/site boundaries in the core model.
2. **FERC June 18, 2026, 195 FERC ¶61,209** ([order](https://www.ferc.gov/sites/default/files/2026-06/EL25-49-002_0.pdf), ¶91, printed pp.51–52; ¶263 n.635, printed p.132; locator corrected 26 November 2026). This partly sets aside the December order and directs expansion of the new services to eligible customers taking service for load with BTMG capable of limiting withdrawals. It does NOT establish that all ordinary generator-free front-of-meter loads automatically qualify.
3. **Reservation sizing** ([June order](https://www.ferc.gov/sites/default/files/2026-06/EL25-49-002_0.pdf), ¶342–343, printed pp.164–166). FERC rejects conditions that tie FCD/NFCD reservation amounts to the capacity of the co-located generator or gross load, and discusses NFCD of 0 MW when no withdrawals are sought. Hence onsite MW, gross load and firm/non-firm grid entitlement are distinct quantities.
4. **Interim treatment** ([June order](https://www.ferc.gov/sites/default/files/2026-06/EL25-49-002_0.pdf), printed pp.251–253, determination). Interim NITS is service pending upgrades and then converts to full NITS; it does not automatically convert to FCD.
5. **PJM system operator interpretation** ([PJM planning presentation, Feb 5, 2026](https://www.pjm.com/-/media/DotCom/committees-groups/workshops/cllsco/2026/20260210/20260210-item-01---3-co-located-load-planning-study-considerations-for-reference-purposes.pdf), slides 3 and 5). PJM illustrates a generator serving 900 MW and 100 MW contracted firm imports for 1,000 MW of load; separate opportunity-based NFCD and emergency priority are shown. These predate the June decision and are planning material, not conclusive current tariff text.

## Minimal modeling requirements
- Track installed generation MW independently of generator output each hour, gross electricity demand, actual net/gross grid imports, physical POI capacity and contracted service entitlements.
- Ensure site MW balance; legal interruption of a grid service does not prove that physical compute can be curtailed. Load reduction, onsite supply or permitted alternatives must explain any reduction in grid imports.
- Model three cases: available generator, failed generator with zero output, and physically bounded load curtailment. Installed generator = 0 is optional, clearly labeled an extra-policy counterfactual.
- Do not require gross demand to equal generator capacity plus FCD reservation. June FERC order rejects that formula as a legal minimum.
- Distinguish interim pre-upgrade and post-upgrade full NITS. Check effective later tariff/compliance filing before implementing exact emergency triggers/rates.

## Explicit qualifications to scope-refocus proposal
- An annual energy curtailment tolerance of epsilon=0 does not legally establish a firm contract, its capacity procurement or service priority. Keep separate entitlement variables and energy constraints.
- A system avoided-cost frontier is not an authorized tariff discount. Avoid double-counting computing-loss costs and treating modeled cost savings as actual incumbent bill effects.
- The accepted June order's service-eligibility expansion covers qualified BTMG; treating ordinary G=0 load as FERC co-located service requires separate primary legal support.

## Proposed supervisor question
May the model's three contract types be framed as FERC/PJM co-location and eligible BTMG services, with a fixed generator included in the core topology and any G_installed=0 case designated a hypothetical general-load sensitivity? Broader large-load policy would require separate regulatory grounding.

## Remaining verification
Exact latest PJM tariff effectiveness and any post-June compliance disposition are not established here; TH-002 must check them. This is a recommendation only, not approval of any change to TH-1.

**TH-002 follow-up (26 November 2026):** The linked comparison now records the ordered framework and latest retrieved November implementing proposal. Clean-sheet/current-effective-record and manual checks remain explicitly open in audit Q1–Q3. The original text above describes the 16 November memo; it should not be read as withholding the student's subsequently recorded working-scope approval.
