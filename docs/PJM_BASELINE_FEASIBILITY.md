# TH-003: PyPSA-USA upstream audit and PJM baseline feasibility

**Issue:** #2 (TH-003). **Author:** Claude Code. **Date:** 16 November 2026 (second version, after the Linux runs).
**Status:** desk audit complete. A one-day smoke run of a 22-zone PJM extract builds and solves to optimality on Linux. **The extract is not calibrated and not validated against PJM outcomes.**

## 1. Answer in brief

- Upstream PyPSA-USA has **no ready-to-run PJM model**. Its only maintained regional configuration is California.
- A PJM-relevant footprint **can be built without changing upstream code**. The filter `model_topology.include.trans_reg: ['PJM']` cuts 22 ReEDS zones out of the Eastern Interconnection. Shown by run, not only from the source.
- It does **not work with upstream's defaults**. Five settings had to differ from v1.0.0's defaults or its own test harness (section 6.2), and one of them works around an upstream crash that affects any Eastern Interconnection model.
- The pinned environment **does not run on the project's Windows workstation**. Windows Application Control blocks compiled libraries in two pinned packages. This is a security policy and was not bypassed. All runs were on a GitHub-hosted Linux runner.
- The smoke run proves the pipeline executes. Its numbers are **not a PJM result**: it is one day, 2030 demand, with capacity allowed to be built and retired (section 6.4).
- A **historical back-cast**, needed before any claim of validation, has extra requirements listed in section 7. Upstream's historical data ends in 2023.

Exit gate of the issue ("reproducible baseline, or specific blockers and a minimal plan"): a reproducible one-day build and solve now exists (section 6). A validated baseline does not.

## 2. What was inspected

| Item | Value | Evidence |
|---|---|---|
| Upstream repository | https://github.com/PyPSA/pypsa-usa | cloned 16 Nov 2026 |
| Pinned revision | tag `v1.0.0`, commit `04a0edd220b1d331715c269a4eab68344c07a088` (5 Oct 2026) | `git describe --tags` |
| Newer upstream commits | 4 on `master` after the tag (head `3d67e20`, 26 Oct 2026); they change only README, citation and docs | `git diff --stat v1.0.0 origin/master` |
| Code licence | MIT | `LICENSE.md` |
| Data bundle licence | CC-BY-4.0 (Zenodo records 14611937, 4538590, 18435264) | Zenodo API |
| Python | 3.11 only (`>=3.11, <3.12`) | `pyproject.toml` |
| Key pins | pypsa 1.3.0, linopy 0.9.1, snakemake 7.32.4, atlite 0.3.0, pandas 3.0.5, numpy 1.26.0, highspy 1.9.0, gurobipy 11.0.3 | `pyproject.toml`, `uv.lock` |
| Environment manager | `uv` with `uv.lock` (preferred) or mamba with `workflow/envs/environment.yaml` | `docs/source/about-install.md` |
| Default solver | Gurobi; HiGHS supported and installed with the environment | `config.default.yaml`, install guide |

Licences of the individual datasets inside the bundles (ReEDS/NARIS tables, TAMU network, PUDL, EER, GODEEEP) were **not** audited one by one.

## 3. Architecture relevant to the thesis

- **Workflow:** Snakemake. Rules retrieve data, build the base network, cluster it, attach demand, plants, renewables and costs, then solve with PyPSA/Linopy.
- **Configuration:** layered YAML. A scenario file is a sparse overlay on `workflow/repo_data/config/config.default.yaml`; nested mappings merge and lists are replaced.
- **Transmission options** (`model_topology.transmission_network`):
  - `reeds`: zonal transfer limits derived by NREL from the non-public NARIS nodal model, at county, ReEDS-zone or state resolution. This is a transport representation between zones, not a nodal power-flow model.
  - `tamu`: the synthetic Breakthrough/TAMU nodal network (about 82,500 buses US-wide), clustered before use. Upstream states it is synthetic and not aligned with the real grid.
- **Footprint filter:** `model_topology.include` keeps only buses whose attribute matches the listed values (`build_base_network.py`, lines 620-640). Buses carry `reeds_zone`, `reeds_state`, `reeds_ba`, `trans_reg`, `trans_grp` and `nerc_reg`.
- **Custom constraints:** `extra_functionality(n, snapshots)` in `workflow/scripts/solve_network.py` is the single place where upstream adds Linopy constraints. Constraint code lives in `workflow/scripts/opts/`. There is **no plug-in hook** for user modules.
- **Boundary trade:** `electricity.imports` / `exports` add priced virtual links to external neighbours, sized from historical EIA interchange. Both are off by default, and were off in the smoke run.
- **Operations detail available:** linearised unit commitment, must-run, rolling horizon, load shedding, transmission losses. All optional.

## 4. The PJM extract

From `workflow/repo_data/ReEDS_Constraints/membership.csv`, 22 ReEDS zones have `transreg = PJM`: p80, p99, p100, p104, p109 to p126, in DE, IL, KY, MD, MI, NJ, OH, PA, VA and WV. From `transmission_capacity_init_AC_ba_NARIS2024.csv`, 42 transfer interfaces lie inside that footprint and 24 connect it to MISO, NYISO and SERTP.

What the runs showed (run 43811176921 and later):

| Stage | Result |
|---|---|
| Eastern Interconnection base network | 70,047 buses |
| After the `trans_reg: ['PJM']` filter | 16,621 buses kept, 53,771 removed; 17,104 lines; 2,083 transformers |
| Footprint | all 22 ReEDS zones present; 497 counties, 9 of them without a bus |
| After aggregation to substations | 9,219 buses, 11,790 lines, **34 electrically separate sub-networks** |
| Final clustered model | 22 buses, 0 lines, 84 one-directional links (the 42 internal interfaces, both directions), 545 generators, 39 storage units, 22 loads |

The cut leaves 34 islands in the synthetic nodal network. In the zonal model this did not stop the build, because internal lines are replaced by zone-to-zone transfer limits.

### The ReEDS "PJM" region is not PJM's actual footprint

ReEDS zones follow state and county lines, so the match is approximate.

- **Missing from the extract:** PJM territory in Indiana (AEP), North Carolina (Dominion) and Tennessee. ReEDS assigns all Indiana zones to MISO and the North Carolina and Tennessee zones to SERTP.
- **Size of the gap (indicative):** in the EIA-860 2025 fleet processed for the earlier local model, about 12.9 GW of 210 GW (6.2%) of capacity reporting PJM as balancing authority sits in those three states.
- **Not quantified:** plants inside the 22 zones that are not PJM members.
- **No trade with neighbours** was modelled: the 24 external interfaces are cut.

The 6.2% figure comes from a local dataset that is not in this repository.

## 5. Windows workstation: blocked

Machine: Windows 11 Pro, 16 cores, 15 GB RAM, no WSL, no Docker, no conda. `uv` 0.13.1.

| Step | Command (from `pypsa-usa/`) | Result |
|---|---|---|
| Create environment | `python -m uv venv --python 3.11 .venv` | OK |
| Install from lock | `python -m uv sync --frozen` | **Failed.** `datrie` 0.8.2 (a Snakemake 7 dependency) has no Windows wheel for Python 3.11; the source build stopped with "An Application Control policy has blocked this file" |
| Install without `datrie` | `python -m uv sync --frozen --no-install-package datrie` | OK |
| Import test | each compiled dependency | **`netCDF4` and `rasterio` blocked** by Application Control, so `pypsa` and `atlite` fail to import |
| Dry run | `python -m snakemake -n ...` with a throwaway `datrie` stand-in | **Failed** at parse: the Snakefile imports `pypsa` |

The policy was left untouched; changing it is the machine owner's decision. Plain PyPSA does run on this machine in a separate Python 3.12 environment (PyPSA 1.4.0), which is enough for the synthetic-network work of TH-004.

## 6. Linux smoke run

### 6.1 How to reproduce

Workflow `.github/workflows/th003-pjm-smoke.yml` on `ubuntu-24.04` (4 cores, 16 GB). By hand, on Linux:

```bash
git clone https://github.com/PyPSA/pypsa-usa.git && cd pypsa-usa
git checkout 04a0edd220b1d331715c269a4eab68344c07a088
bash init_pypsa_usa.sh && uv sync --frozen
# plus an `ipopt` executable on PATH (section 6.2, item 4)
cd workflow
uv run snakemake data_model -j4 --scheduler greedy --configfile <thesis repo>/configs/pypsa-usa/config.pjm_smoke.yaml
uv run snakemake results/pjm_smoke/eastern/networks/elec_s75_c22_ec_lv1.0_1h_E.nc -j4 --scheduler greedy --configfile <thesis repo>/configs/pypsa-usa/config.pjm_smoke.yaml
```

Targets go before `--configfile`, which accepts several values. Do not export environment variables named `PYPSA_*`: PyPSA reads them as its own options.

### 6.2 What had to differ from upstream defaults

The overlay copies upstream's test harness (`config.test.yaml`: one day, 2030 horizon, a short list of expansion candidates) and changes the following. Items 2 to 5 were each found by a failed run.

| # | Setting | Upstream | Used | Why |
|---|---|---|---|---|
| 1 | Footprint | California, Western | `trans_reg: ['PJM']`, Eastern, `clusters: 22`, `simpl: 75` | The purpose of the test. `simpl` must be at least 54 for this footprint (run 43811176921 rejected 50). |
| 2 | Demand source | NREL EFS from `data.nlr.gov` | EER 2025 baseline from Zenodo (`profile: eer`) | `data.nlr.gov` returned HTTP 503 for every request on 15-16 Nov 2026 (run 43757942436). |
| 3 | Bus demand weighting | `bus_allocation: population` | `breakthrough` (legacy) | **Upstream defect.** `build_bus_population.assign_load_weight` fails with "cannot reindex on an axis with duplicate labels" for the Eastern Interconnection, before the footprint filter runs (run 43809435330). |
| 4 | Ipopt executable | provided by the conda environment only | installed separately on the runner | With HiGHS configured, the cluster-count step calls `ipopt`, which the `uv` environment lacks (run 43813019517). Not mentioned in the install guide. |
| 5 | Solver | Gurobi; HiGHS with crossover off | HiGHS with `run_crossover: "on"` | No Gurobi licence. Without crossover HiGHS ended with "Model status: Unknown" (run 43817556991); with it, "Optimal" (run 43819895193). |

Item 3 means the split of each state's demand across zones rests on the synthetic network's nominal bus loads, not on census population, until upstream fixes the defect or the project patches it.

### 6.3 Run history

| Run | Commit | Outcome |
|---|---|---|
| [43755498614](https://github.com/qasjadullah-design/MSRE-Thesis/actions/runs/43755498614) | `2f25dd7` | Failed in the build; cause identified in run 3 |
| [43757441883](https://github.com/qasjadullah-design/MSRE-Thesis/actions/runs/43757441883) | `0851247` | Failed at the dry run: workflow error (target after `--configfile`) |
| [43757942436](https://github.com/qasjadullah-design/MSRE-Thesis/actions/runs/43757942436) | `bbdef6a` | Failed: EFS demand download, HTTP 503 |
| [43759225466](https://github.com/qasjadullah-design/MSRE-Thesis/actions/runs/43759225466) | `7096072` | Failed in `build_base_network`; traceback not captured |
| [43809435330](https://github.com/qasjadullah-design/MSRE-Thesis/actions/runs/43809435330) | `1245505` | Failed: duplicate-label crash in `assign_load_weight` |
| [43811176921](https://github.com/qasjadullah-design/MSRE-Thesis/actions/runs/43811176921) | `3f4a634` | PJM filter worked; failed in `cluster_resources` (`simpl` 50 below 54) |
| [43813019517](https://github.com/qasjadullah-design/MSRE-Thesis/actions/runs/43813019517) | `0f0deb2` | Failed: no `ipopt` executable |
| [43815319465](https://github.com/qasjadullah-design/MSRE-Thesis/actions/runs/43815319465) | `8755368` | **Built and solved.** Solver status not recorded |
| [43817556991](https://github.com/qasjadullah-design/MSRE-Thesis/actions/runs/43817556991) | `a9c0aa9` | Built and solved; HiGHS "Model status: Unknown" |
| [43819895193](https://github.com/qasjadullah-design/MSRE-Thesis/actions/runs/43819895193) | `af1677c` | **Built and solved; HiGHS "Model status: Optimal"** |

Timing of the last run: data-model build 13 min 23 s, solve step 8 s (HiGHS itself 0.9 s), whole job about 17 min. Each run's logs and network files are stored as a workflow artifact for 30 days; the network summary and the end of the solver log are also published as notices on the run.

### 6.4 What the last run contains

From the notices of run 43819895193 (the unsolved figures are identical in run 43817556991):

- Snapshots: 24 hours of 1 January, planning year 2030.
- Load: peak 124.7 GW, mean 105.9 GW (EER 2025 baseline scenario).
- HiGHS: interior point 41 iterations, crossover, final status Optimal, objective 1.8735 × 10⁹, relative primal-dual gap 1.4 × 10⁻¹⁴.

Existing capacity in the data model, before the solve:

| Carrier | GW | | Carrier | GW |
|---|---:|---|---|---:|
| CCGT | 65.13 | | hydro | 8.09 |
| OCGT | 42.05 | | oil | 4.93 |
| nuclear | 33.43 | | biomass | 1.12 |
| coal | 33.42 | | waste | 0.72 |
| solar | 20.21 | | pumped hydro (storage) | 5.05 |
| onshore wind | 8.15 | | battery (storage) | 0.99 |

For orientation only, the EIA-860 2025 fleet in the earlier local model (PJM balancing authority, not in this repository) has nuclear 33 GW, coal 36 GW, combined cycle 59 GW, solar 18 GW, wind 12 GW and pumped hydro 5 GW. The footprints, data vintages and technology groupings differ, so this is not a validation. Two items to examine before any use: hydro at 8.1 GW looks high for PJM, and wind is about 4 GW below the local figure.

**Why the solved numbers are not a PJM result.** After the solve, CCGT capacity is 2.36 GW, down from 65.13 GW. The configuration allows economic retirement, and a single winter day gives the optimiser no reason to keep capacity it does not need that day. The mean bus price is about 1,700 per MWh for the same reason: annualised investment terms on a one-day problem. These are artefacts of a smoke-test configuration, exactly the kind of output that must not be quoted.

## 7. What a real PJM baseline needs beyond the smoke run

1. **A fixed fleet for operations:** no expansion candidates and technical retirement only, or a full-year horizon if expansion is wanted.
2. **Historical demand** (`electricity.demand.profile: eia`): EIA-930 by balancing authority, **2018 to 2023 only**. Upstream's docs say this path needs a free EIA API key.
3. **Historical weather:** the default renewable dataset (GODEEEP) publishes only **2012** as a historical year; the 1980-2022 archive sits on a Stanford-internal server. Public historical years 2018-2023 need `renewable.dataset: atlite` with ERA5 cutouts of 5 to 9 GB per year from Zenodo.
4. **Validation mode** (`run.validation: true`): comparison plots against EIA data; also needs the EIA API key.
5. **A decision on boundary trade** with MISO, NYISO and SERTP.

The approved plan (`governance/SCOPE.md`, decisions D14 and D16) uses a forward year for the scenarios and a one-week 2023 back-cast only to check the extract.

## 8. Risks

| # | Risk | Severity | Mitigation |
|---|---|---|---|
| R1 | No execution environment on the workstation | High for full-year runs | GitHub Actions covers one-day and one-week tests. Full-year runs need WSL2, a cloud VM or university HPC (decision D13) |
| R2 | `trans_reg: ['PJM']` filter untested upstream | **Closed**: it works (section 4) | |
| R3 | ReEDS PJM region omits IN, NC, TN territory (about 6% of capacity) and cuts all external ties | Medium | Quantify from PyPSA-USA's plant table; consider adding Indiana zones; decide on imports and exports |
| R4 | Zonal transfer limits, not nodal: congestion at a specific site cannot be represented | High for site-level claims | Accepted in the plan (decision D17): no site-level claims |
| R5 | Historical inputs end in 2023; default weather data not public for those years | Medium | atlite cutouts; one week of 2023 |
| R6 | No plug-in hook for custom constraints | Medium | Contract module kept in this repository; one small documented patch or a wrapper |
| R7 | Runner limits (4 cores, 16 GB, 6 h, limited disk) | Medium | Not enough for a full-year 22-zone expansion; see R1 |
| R8 | Smoke-run numbers are artefacts of a one-day expansion problem | Low if respected | Never quote them (section 6.4) |
| R9 | Upstream crash in population-based demand weighting for the Eastern Interconnection | Medium | Legacy weighting for now; report upstream; patch if it matters for zonal demand |
| R10 | Hidden dependency on an `ipopt` executable when HiGHS is the solver | Low | Installed in the workflow; document for any other machine |
| R11 | External data hosts fail (`data.nlr.gov` 503) | Medium | Prefer Zenodo-hosted inputs; cache downloaded data between runs |
| R12 | HiGHS without crossover returns an uncertified solution, and upstream only logs a warning | Medium | Keep crossover on, or check the status explicitly in every run |
| R13 | Fleet in the data model not yet reconciled with an independent source | Medium | Compare by zone and carrier with the EIA-860 benchmark (decision D12) |

## 9. Next steps

1. Review and merge this branch.
2. Decide the execution environment for full-year runs (D13).
3. Cache the downloaded data in the workflow so runs do not depend on external hosts each time.
4. One-week 2023 back-cast with a fixed fleet, EIA demand and atlite weather. Needs an EIA API key stored as a repository secret. This is TH-008 in the plan.
5. Report the `assign_load_weight` defect to the PyPSA-USA maintainers, if the student agrees.

## 10. Questions for human review

- Which Linux environment will the thesis use for full-year runs?
- Should Indiana be added to the footprint to cover AEP's PJM territory?
- Should trade with MISO, NYISO and SERTP be modelled, fixed to historical values, or left out?
- Should the upstream defect be reported under the student's GitHub account?

## 11. Files in this branch

| File | Purpose |
|---|---|
| `docs/PJM_BASELINE_FEASIBILITY.md` | this report |
| `configs/pypsa-usa/config.pjm_smoke.yaml` | PJM overlay for the smoke run |
| `.github/workflows/th003-pjm-smoke.yml` | Linux run of the smoke test |
| `tools/summarize_network.py` | prints what the produced networks contain |
| `tools/ci_annotate_logs.py` | publishes log tails and summaries as run annotations |
| `governance/handoffs/TH-003.md` | handoff |
| `governance/DECISIONS.md` | D12 to D14 added |
