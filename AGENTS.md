# Shared instructions for all AI agents

Read README.md, governance/PROJECT_BRIEF.md, governance/MILESTONES.md, governance/DECISIONS.md and the assigned issue before making changes.

Research authority: submitted NUST TH-1 and any subsequently approved supervisor decisions. Do not alter three approved objectives or six milestones.

Do not fabricate regulatory sources, tariff status, empirical flexibility, simulation results or test execution. Label parameters as observed, regulatory, inferred or hypothetical and record source/date/units/evidence quality.

Distinguish gross site demand, firm and nonfirm import entitlements, physical point-of-interconnection capacity and actual ability to curtail or shift computing load. Texas SB6 legal curtailment requirements do NOT demonstrate actual delivered flexibility. Distinguish FERC co-location order classes from separate PJM large-load proposals.

Keep physical grid-system costs separate from tariffs, revenue requirements, and incumbent-ratepayer allocation. Do not infer actual bills from PyPSA's dispatch objective.

Pin PyPSA-USA upstream commit and environment. Do not claim an existing validated PJM testbed until reproduced. Build an independently testable small synthetic system first. Document limitations of deterministic reliability metrics.

Repository is PUBLIC: no university identification numbers, signed TH-1, private emails, secrets, licensed full-text PDFs or restricted datasets. Private originals remain in Drive.

One owner per task/branch. Changes via feature branches and PRs, with independent review prior to merge. No silent upstream rewrites. Handoff must list issue, branch/commit, files, sources, tests (actually executed), assumptions, blockers, and next action. Never claim work complete without an artifact.

## Adopted working scope (student approved 16 Nov 2026)
Read `docs/MODEL_DESIGN.md` **v0.2**, `governance/DECISIONS.md` and `writing/CHAPTER_OUTLINE.md` as the active methodology. Archived scope proposals and v0.1 are historical. Three TH-1 objectives and six working deadlines are fixed.
- Central question: incremental system avoided cost for interruptible vs firm 1 GW new data-center load; allocate residual costs via two clearly illustrative bookends.
- 2030 zonal PJM-relevant case, forward-year capacity expansion then dispatch; three zones, <=30 regional full-year solves, 2023 one-week backcast if executable.
- Core FERC co-located / qualifying BTMG model includes physical onsite generator. G_installed=0 is NOT assumed tariff-eligible. Interim upgrade transition is to full NITS, not automatic FCD.
- Legal firm service is NOT equivalent to epsilon=0 permitted annual curtailment. Contracts require separate rights/planning/priority parameters. No made-up tariff discount.
- Actual field-metered demand flexibility and computing-trace-modeled capability must stay distinct; no assertion that evidence-bounded ranges fully satisfy formal Objective 2 without supervisor agreement.
- Approved working design is **not** university/supervisor proof of scope acceptance or proof of successful simulation. No new full-scale development without adequate validation and PR review.
