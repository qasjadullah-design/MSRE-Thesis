# TH-002 — primary-source audit and unresolved questions

**Evidence cutoff: 26 November 2026. Internal delivery target: 27 November 2026.** Supports [comparison](../regulatory/TH-002_CONTRACT_MATRIX_2026-11-26.md), [requirements](../docs/TH-002_PYPSA_REQUIREMENTS_2026-11-26.md), [S1](../regulatory/PROPOSED_S1_COLOCATION_FRAMING_2026-11-16.md) and [issue #1](https://github.com/qasjadullah-design/MSRE-Thesis/issues/1). This is a dated research record, not certification that a customer can currently commence service.

## 1. Source register and chronology

| ID | Primary author/document and exact locator | Date and status supported |
|---|---|---|
| O25 | FERC, *PJM Interconnection, L.L.C.*, [193 FERC ¶61,217](https://www.ferc.gov/sites/default/files/2025-12/E-1%20EL25-49-000.pdf), EL25-49-000 et al.; ¶¶189–193. | Issued 18-Dec-2025. Establishes the service framework, subsequently modified by O26. Historical starting point, not sufficient evidence of current implementing tariff. |
| O26 | FERC, *PJM Interconnection, L.L.C.*, [195 FERC ¶61,209](https://www.ferc.gov/sites/default/files/2026-06/EL25-49-002_0.pdf), *Order on Rehearing, Clarification, Compliance Filing, and Paper Hearing*. [eLibrary accession 20260618-3103](https://elibrary.ferc.gov/eLibrary/docinfo?accession_number=20260618-3103). Caption: EL25-49-002/-000; AD24-11-001 and EL25-20-001 consolidated; ER26-1479-000. | Issued 18-Jun-2026. ¶¶7–9: substantive Commission determinations, partial acceptance/rejection and further compliance. ¶263 n.635 and appendix pp.273–274: accepted outline records, including Part XI and F-3A/F-4 v0.0.0. This does not establish operational availability of later detailed services. |
| P26 | PJM, [*Proposed Tariff Revisions for Large Loads and Additional Compliance with Co-Location Order*](https://www.pjm.com/-/media/DotCom/documents/ferc/filings/2026/20261116-er27-531-000.pdf), **ER27-531-000**, [eLibrary accession 20261116-5340, file list](https://elibrary.ferc.gov/eLibrary/filelist?accession_number=20261116-5340). §III.C pp.33–48, §III.E p.57, §V p.82. | Filed 16-Nov-2026. Proposed implementation plus broader Large Load reforms. Part XI, relevant agreements and specified other records request **16-Mar-2027**. Fast Energization Part VIII records request an indefinite effective date represented by **12/31/9998**, a placeholder. Neither is an acceptance date. |
| N26 | PJM, [Notice of Filing](https://www.pjm.com/-/media/DotCom/documents/ferc/filings/2026/20261118-el26-67-000-el25-49-000-et-al-ad24-11-000-el25-20-000-er26-1479-000-er26-3537-000.pdf), pp.1–2. | Dated 18-Nov-2026; confirms ER27-531 and ER27-522 filings. Records a 16-Nov **motion to withdraw** the 17-Aug ER26-1479-002 compliance filing. Withdrawal granted: **not yet established**. |
| C26 | PJM, [November 16 large-load and co-located-load filings chart](https://www.pjm.com/-/media/DotCom/committees-groups/workshops/cllsco/2026/20261123/20261123-item-02---november-16-large-load-and-co-located-load-filings-chart.pdf), rows ER27-520/-522/-531; November 23 workshop materials. | Identifies companion TO rates/cost recovery filing **ER27-520-000**, requesting 16-Mar-2027 / indeterminate dates, and operational/ride-through filing **ER27-522-000**, requesting 16-Jan-2027. Chart retains “as of November 18” procedural wording; use FR26 for the later noticed deadline. |
| FR26 | FERC, Combined Notice of Filings #1, [Federal Register, 23-Nov-2026, p.75507](https://www.govinfo.gov/content/pkg/FR-2026-11-23/pdf/2026-23765.pdf), PDF p.2, ER27-531-000 entry. | Confirms filed 16-Nov-2026, accession **20261116-5340**, requested 16-Mar-2027 date; comments **5 p.m. Eastern Time, 15-Jan-2027**. A procedural notice, not approval. |
| PY26 | PyPSA, [Custom Constraints](https://docs.pypsa.org/latest/user-guide/optimization/custom-constraints/) and [Network indexing / snapshot weightings](https://docs.pypsa.org/latest/api/networks/indexing/). | Official technical documentation retrieved 26-Nov-2026. Supports the implementation interface, not a pinned or tested thesis environment. TH-003 must pin versions. |

### Status conclusion

The June order establishes governing principles and accepts outline tariff records while requiring more compliance. The latest implementing filing retrieved is November 16's ER27-531-000. **No later primary acceptance establishing its detailed service provisions as operationally effective was located in the reviewed material. A complete eLibrary docket sweep and record-level effective-date check remain outstanding.** Use `ordered_framework` and `filed_proposal` as distinct statuses; do not label the entire framework “only proposed,” or promote requested dates to effective dates.

The separate ordinary-large-load proceeding is **EL26-67-000**, 195 FERC ¶61,211 (18-Jun-2026), with errata 196 FERC ¶61,122, as identified in N26. P26 responds to that track and the co-location order together. Their consolidation in a filing does not erase the difference between the June eligibility determination and the new proposed extension.

## 2. Retrieval and evidence quality

Official indexed FERC/PJM text, official filing records and reproduced original PDFs were cross-checked. Several direct official downloads failed: the June FERC PDF intermittently returned HTTP 403; the November PJM PDF redirected to its not-found page. The original documents were therefore also read from archival copies. The archive's analysis was not used as legal authority.

| Original document | Retrieval copy and reproducibility check | Limitation |
|---|---|---|
| O26, FERC-authored order | [Archived original PDF](https://raw.githubusercontent.com/pranava0x0/ferc-large-load-proceedings/main/docs/orders/e-2-pjm-el25-49-002.pdf); 278 PDF pages; 2,513,319 bytes; SHA-256 `924f3bc65ab8aa0c9bf803d704e08db658f5a598ebac95b7a8dbd7b45897e11c`. Caption, selected indexed primary passages and rendered paragraph numbers checked. | Mirror-hosted original, not a certified copy; hash records the retrieved bytes, not independent authentication by FERC. |
| P26, PJM-authored filed transmittal | [Archived original PDF](https://www.pranavaraparla.com/ferc-large-load-proceedings/originals/20261116-5340_01.pdf); 91 PDF pages, including four preliminary pages; 1,400,057 bytes; SHA-256 `816478c587a2668626547b6ece6d63a6504be0156ec6a2ed4175af0f4169485d`. Date, accession, filename and rounded size matched to official eLibrary listing; key passages checked against official PJM indexed text. | **Transmittal only.** Cited proposed tariff sections are those identified by PJM in this filed document; they have not been checked against the complete clean tariff sheets or the current effective eTariff. |

For P26, **printed page n = PDF page n + 4**; citations here use printed pages. For O26 use the printed order page and paragraph, not a search-result excerpt's position. Ordinary text extraction omitted some O26 paragraph numbers; critical locators were checked against indexed primary text and/or rendered pages.

The official accession lists eight public files. The next reviewer should retrieve **`Att. B-1 3.16.2027 Proposed Tariff Revisions (Clean).pdf`** (listed 931 KB) and **`Att. B-2 9998 Proposed Tariff Revisions (Clean).pdf`** (688 KB), plus the marked versions. The transmittal enclosure labels on pp.84–85 differ from the actual A-2/B-1 filenames: identify the explicit filename and requested date. A failed download does not mean an attachment was not filed.

No full-text PDFs are added to this public repository. The Markdown retains primary links, exact locators and retrieval provenance.

## 3. Pinpoint map for implementation

All P26 section numbers below are **proposed provisions reported in the transmittal**, subject to Q2. O26 locators identify Commission determinations rather than party arguments.

| Rule ID | Controlling/underlying order locator | Proposed implementation locator / transmittal pages | Modeling consequence |
|---|---|---|---|
| R01 — eligibility | O26 ¶91, pp.51–52; ¶263 n.635, p.132. | P26 Part I §1 Definitions E–F, p.52; Part XI §§701.1, 708(a), pp.34,37–38. | Preserve co-location/qualifying BTMG core; tag proposed broader Large Load extension separately. |
| R02 — independent reservations | O26 ¶¶342–344, pp.164–168. | P26 §§708(b), 710.1, pp.38–39. | Gross load, generator MW, F, N and POI capacity are independent inputs; no gross-load-matching minimum. Zero-MW service still requires an agreement. |
| R03 — interim nature / exclusivity | O26 ¶571, pp.252–253. | P26 §§701.1–701.4, 702.1–702.3, pp.34–35; §709.3, p.38. | Interim accompanies a full-NITS application; not simultaneous contract-demand service for the same designated load. |
| R04 — curtailment authority / priority | O26 ¶¶551–555, pp.244–246. | P26 §§701.5, 709.5, 719.2, 719.4, 719.5; Part I Definitions C–D; pp.35,39,43–44. | Firm tier protected ahead of non-firm; November proposal puts NFCD/Interim/non-firm point-to-point in one tier, with system-limit contribution relevant. Capacity/reserve shortages can trigger interruption. |
| R05 — generator during interim interruption | O26 ¶576, pp.255–256. | P26 p.44 n.230 cites §705.2. | During Interim curtailment, capacity-resource status can prohibit using the co-located generator to serve the site; no-interconnection/non-capacity exception. Reconcile section numbering under Q2. |
| R06 — RA treatment | O26 ¶597, pp.264–265. | P26 §§701.2, 708(b), pp.34,38; §III.E, p.57. | FCD capacity procurement based on contract demand; NFCD/Interim excluded from this RA procurement. UCAP/forecast mechanics still need verification. |
| R07 — capacity rights at dedicated plant | Read with O26's separation of reservations and generation, ¶¶342–344. | P26 §710.3, pp.39–40 n.200. | Dedicated generator portion must not retain Capacity Interconnection Rights (CIRs); avoid simultaneous grid capacity credit. |
| R08 — transition and contract term | O26 ¶571, pp.252–253. | P26 §702.4(a), F-3A §§2–3, pp.35–36,46; §711(f), F-4 §§2–3, pp.41,48; §§709.3, 711(b), pp.38,40. | Interim→NITS differs from NFCD→FCD. Upgrades, updated analysis and system updates matter. Five-year switch restriction and 42-month FCD notice prevent frictionless annual contract switching. |
| R09 — controls / operating capability | O26 ¶¶551–555 establish priority and require implementation. | P26 §§716–718.1, pp.42–43; §719.5(a)–(b), pp.44–45. | Telemetry/control capability is an eligibility/compliance input, not evidence of delivered computing flexibility. Do not optimize permission to disobey instructions. |
| R10 — charges and transfers | O26 ¶¶572–573, p.253. | P26 §§703.2, 703.4, pp.36–37; §§714.3, 714.5, p.41; §715.4, p.42; C26 ER27-520 row. | Interim NITS transmission rate and ancillary obligations survive lack of capacity procurement; actual numeric tariffs not established by this pack. |
| R11 — full-NITS/BTMG basis | O26 ¶¶207, 220, as cited in P26 p.24 n.112. | P26 Part III §34.2(B)–(F), RAA Schedule 8(A), pp.24–27. | Proposed 50-MW retail-BTMG netting limit has transition/grandfather/cogeneration exceptions. Physical onsite output is not automatically allowed capacity/netting credit. |

**Source corrections and ambiguities:**

- The S1 memo's former “¶635” is **footnote 635 to ¶263**, printed p.132. The BTMG-extension determination is **¶91**, pp.51–52. The correction is factual and does not revise approved S1 scope.
- P26 p.44 n.230 points to **§705.2**, while common curtailment provisions are reorganized in **§719**. Apply O26 ¶576 as the authority and verify the clean-sheet cross-reference; do not silently renumber the proposal.
- P26 §709.3, p.38, describes current service/pending-application exclusivity, while its §710.3 summary on p.39 uses historical “has not been served” wording. Record prior/current service and applications; block the clear current/pending conflicts, and verify the clean text before inferring a lifetime eligibility bar.
- P26 pp.41–42 footnotes label §§714–715 as “Subpart A,” although the narrative places contract-demand provisions in Subpart B. Use the section number plus transmittal page until clean-sheet reconciliation.
- Search snippets can merge adjacent Federal Register entries. For ER27-531 use accession **20261116-5340** and **15-Jan-2027** comments from the PDF; accession 20261116-5337 / a December 16 comment date belongs to a neighboring filing.

## 4. Unresolved questions and release gates

“Not yet established” is an evidence result, not an invitation to fill a legal rule with an unlabeled assumption. A hypothetical toy implementation may proceed with named assumptions; no result may claim effective PJM tariff compliance until the relevant gate is closed.

| ID | Question / evidence needed | Effect and next owner |
|---|---|---|
| Q1 | What subsequent orders accept ER27-531/-520/-522, what are each record's effective dates, and was ER26-1479-002 withdrawal granted? Complete eLibrary history and current record inspection. | Blocks claims of effective service availability. TH-002 legal refresh immediately before implementation/publication. |
| Q2 | Do clean filed sheets match the transmittal, especially §§705.2/719, combined F/N reservation fields, current/prior-service eligibility wording in §§709.3/710.3, F-3A/F-4, and section/subpart labels? Obtain named clean PDFs and amendments. | Blocks treating section descriptions as a fully verified executable tariff specification. TH-002 follow-up; preserve a proposal flag meanwhile. |
| Q3 | Which adopted manual/agreement provisions govern notice, response time, restoration, capacity/reserve triggers, feeder arrangements and contribution to system-limit exceedance? | Blocks calibrated event chronology and exact within-tier algorithm. TH-006 may use a declared synthetic event policy, not claim PJM dispatch replication. |
| Q4 | How are contract MW mapped to UCAP, load forecast and settlement; what Network Load/BTMG netting basis applies after Interim→NITS? Check conforming RAA filings, Part III §34.2 and customer facts. | TH-004/006 must use a documented planning proxy where unresolved; never carry zero interim RA obligation into NITS or net all onsite output automatically. |
| Q5 | What TO rates, upgrade costs, ancillary bases, credits and recovery rules are accepted under ER27-520 and related records? | TH-007 financial illustration stays separate from resource cost. No numerical discount or actual bill is verified here. |
| Q6 | Can the modeled site physically meet each instruction with its generator status, controls, curtailable share and response duration? | TH-005 evidence and TH-004/006 feasibility tests. A legal duty is not measured flexibility; no tariff annual ε guarantee was found. |
| Q7 | Should a generator-free ordinary Large Load sensitivity enter the thesis if the November extension is accepted? | Student/supervisor scope decision if needed. Current v0.2 core retains G>0; generator-free case remains hypothetical or explicitly proposed-policy, with no automatic eligibility claim. |

## 5. Evidence boundary

Regulatory inputs are graded **regulatory**, with separate order/proposal/effective status. Engineering approximations are **inferred** or **hypothetical**; physical flexibility can be **observed** only with measurements. No service dates, interruption frequencies, tariff prices, flexibility performance or solver results have been manufactured. The source pack resolves the ordered conceptual distinctions and identifies the precise remaining legal and calibration checks; it does not claim a validated PJM network, site interconnection, or operational service.
