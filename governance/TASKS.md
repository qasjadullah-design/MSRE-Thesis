# Multi-agent work plan

Source: `governance/SCOPE.md` section 8 (working plan approved by the student on 16 November 2026). Dates are internal targets inside the six fixed milestones and change none of them. A task is complete only when its deliverable exists and has been reviewed.

| ID | Owner | Deliverable | Acceptance | Target | State on 16 Nov 2026 |
|---|---|---|---|---|---|
| TH-001 | ChatGPT | TH-1 context, repository and Drive information, agent governance | In place | done | Done |
| TH-002 | ChatGPT | One-page table for the three service classes: docket, order date, status, withdrawal right, curtailment trigger, capacity obligation; answer to S1 | Every cell has a primary source or "not found" | 27 Nov 2026 | S1 memo drafted (draft PR #10); table open |
| TH-003 | Claude | Smoke run of the PJM extract passing on Linux, or a specific blocker | Run link and log in the handoff | 27 Nov 2026 | Passed; report on branch `th-003-pypsa-usa-pjm-feasibility`, awaiting review |
| TH-005 | ChatGPT | Flexibility table: curtailable share, duration, cost of lost computing, each graded observed / derived / assumed; three cases | No value labelled observed without a metered source | 18 Dec 2026 | Open |
| TH-004 | Claude | `docs/MODEL_DESIGN.md` v0.2; toy network with firm access and tests | Tests run in CI on the pinned versions | 18 Dec 2026 | In progress on branch `th-004-firm-access-toy` |
| Literature chapter | Student + ChatGPT | Draft of chapters 2 and 3 from 12 to 15 core sources | Draft in Drive | 31 Dec 2026 (milestone) | Open |
| TH-007 | ChatGPT | One-page statement of allocation rules A and B with formulas and what each omits | Student approval | 15 Jan 2027 | Open |
| TH-006 | Claude | Non-firm and interim treatments on the toy network; ε sweep working | Acceptance tests in `docs/MODEL_DESIGN.md` pass | 31 Jan 2027 | Blocked on TH-004 review |
| TH-008 | Claude | Forward-year PJM baseline; one-week 2023 back-cast | Baseline reproducible from one command | 15 Mar 2027 | Blocked on D13 (execution environment) and an EIA API key |
| TH-009 | Claude | Regional scenario runs of `governance/SCOPE.md` 3.5 | Result tables and run logs | 31 May 2027 (milestone) | Blocked on TH-006 and TH-008 |

Use GitHub issues as the task records and pull requests for review. TH-008 and TH-009 have no issue yet.
