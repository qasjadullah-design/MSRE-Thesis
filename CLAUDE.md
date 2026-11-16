# Claude Code working agreement

Start by reading AGENTS.md, README.md, governance/PROJECT_BRIEF.md, governance/MILESTONES.md, docs/MODEL_DESIGN.md, and the current issue.

You are the primary implementation agent. FIRST TASK: determine precise PyPSA-USA upstream revision and whether a runnable/validated PJM-specific testbed exists; write a reproducibility assessment. Then propose mathematical architecture and a 3–5 bus firm-entitlement proof of concept. No large-scale or three-contract implementation before these are reviewed.

Use feature branches, tests, source traceability and detailed handoffs. Report uncertainty and require human signoff for regulatory assumptions. Never invent measured flexibility or outcomes. Follow AGENTS.md.

## Current student-approved technical plan (16 Nov 2026)
Use v0.2 model design, decision register and issue tracker; supersede earlier broad v0.1. S1–S5 are student-approved working choices; supervisor acknowledgment of narrowed formal objective interpretations remains unverified.
- Finish TH-003 Linux PJM smoke success or logged blocker. 22 ReEDS-zone PJM is an approximation; no site-level power-flow claims.
- Next TH-004 firm-contract toy network, physical co-located generator, contracted import vs site balance, automated tests; separate outage from zero installed generation.
- TH-006 after review: NF constraints and interim NITS (two static pre/post-upgrade cases); ε energy tolerance separated from contractual entitlement.
- Apply forward-year capacity expansion then dispatch (resource adequacy proxy requires labeling) and output cost vs interruption; at most 30 regional full-year solves.
- Use evidence grades and two bookend allocations; avoid claiming actual PJM tariffs, actual bills, or measured GW-scale flexibility.
- Ensure acceptance of already chosen working scope instead of restarting scope discovery; escalate unknown prevailing tariff text, empirical evidence gaps, and computational issues.
