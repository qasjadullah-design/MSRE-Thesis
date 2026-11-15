# TH-003: PyPSA-USA upstream audit and PJM baseline feasibility

**Issue:** #2 (TH-003). **Author:** Claude Code. **Date:** 16 November 2026.
**Status:** desk audit complete; PJM smoke run prepared but **not yet executed**. No baseline is reproduced or validated by this document.

## 1. Answer in brief

- Upstream PyPSA-USA has **no ready-to-run PJM model**. Its only maintained regional configuration is California.
- A PJM-relevant footprint **can be configured without changing upstream code**: the footprint filter accepts ReEDS transmission regions, and `PJM` is one of them (22 zones in the Eastern Interconnection). This is established from the source, not yet from a run.
- The pinned environment **does not run on the project's Windows workstation**. Windows Application Control blocks compiled libraries in two pinned packages, so PyPSA cannot be imported. This is a security policy and was not bypassed.
- The smoke run is therefore set up for a **Linux runner** (GitHub Actions workflow on this branch). It has not run yet because the branch has not been pushed.
- A **historical back-cast** of PJM, needed before any claim of validation, has three extra requirements listed in section 6. Upstream's historical data ends in 2023.

Exit gate of the issue ("reproducible baseline, or specific blockers and a minimal plan"): met on the second branch. Blockers are in section 5, the plan in section 8.

## 2. What was inspected

| Item | Value | Evidence |
|---|---|---|
| Upstream repository | https://github.com/PyPSA/pypsa-usa | cloned 16 Nov 2026 |
| Pinned revision | tag `v1.0.0`, commit `04a0edd220b1d331715c269a4eab68344c07a088` (5 Oct 2026) | `git describe --tags` |
| Newer upstream commits | 4 on `master` after the tag (head `3d67e20`, 26 Oct 2026); they change only README, citation and docs | `git diff --stat v1.0.0 origin/master` |
| Code licence | MIT | `LICENSE.md` |
| Data bundle licence | CC-BY-4.0 (Zenodo records 14611937, 4538590) | Zenodo API |
| Python | 3.11 only (`>=3.11, <3.12`) | `pyproject.toml` |
| Key pins | pypsa 1.3.0, linopy 0.9.1, snakemake 7.32.4, atlite 0.3.0, pandas 3.0.5, numpy 1.26.0, highspy >= 1.9.0, gurobipy 11.0.3 | `pyproject.toml`, `uv.lock` |
| Environment manager | `uv` with `uv.lock` (preferred) or mamba with `workflow/envs/environment.yaml` | `docs/source/about-install.md` |
| Default solver | Gurobi; HiGHS supported and already installed with the environment | `config.default.yaml`, install guide |

Licences of the individual datasets inside the bundles (ReEDS/NARIS tables, TAMU network, PUDL, EFS, GODEEEP) were **not** audited one by one.

## 3. Architecture relevant to the thesis

- **Workflow:** Snakemake. Rules retrieve data, build the base network, cluster it, attach demand, plants, renewables and costs, then solve with PyPSA/Linopy.
- **Configuration:** layered YAML. A scenario file is a sparse overlay on `workflow/repo_data/config/config.default.yaml`; nested mappings merge and lists are replaced.
- **Transmission options** (`model_topology.transmission_network`):
  - `reeds`: zonal transfer limits derived by NREL from the non-public NARIS nodal model, at county, ReEDS-zone or state resolution. This is a transport representation between zones, not a nodal power-flow model.
  - `tamu`: the synthetic Breakthrough/TAMU nodal network (about 82,500 buses US-wide), clustered before use. Upstream states it is synthetic and not aligned with the real grid.
- **Footprint filter:** `model_topology.include` keeps only buses whose attribute matches the listed values. The code loops over any bus column (`build_base_network.py`, lines 620-640), and buses carry `reeds_zone`, `reeds_state`, `reeds_ba`, `trans_reg`, `trans_grp` and `nerc_reg`.
- **Custom constraints:** `extra_functionality(n, snapshots)` in `workflow/scripts/solve_network.py` is the single place where upstream adds Linopy constraints (policy, reserves, interchange, interface limits). Constraint code lives in `workflow/scripts/opts/`. There is **no plug-in hook** for user modules, so the contract module will need either a small, documented patch at that function or a wrapper script that calls upstream's solve functions. This is a design question for TH-004.
- **Boundary trade:** `electricity.imports` / `exports` add priced virtual links to external neighbours, sized from historical EIA interchange. Both are off by default.
- **Operations detail available:** linearised unit commitment, must-run, rolling horizon, load shedding, transmission losses. All are optional and off or relaxed by default.

## 4. Is there a PJM model?

**No ready-made one.** A search of the upstream tree at the pinned commit finds "PJM" only in region tables, constants and plotting code. The shipped configurations are default (Western Interconnection), tutorial and test (California), California, and two equivalence harnesses.

**A PJM extract is configurable.** From `workflow/repo_data/ReEDS_Constraints/membership.csv`:

- 22 ReEDS zones have `transreg = PJM`: p80, p99, p100, p104, p109 to p126.
- They split into `PJM_West` (p80 northern Illinois, p104 Michigan) and `PJM_East` (the rest).
- States covered: DE, IL, KY, MD, MI, NJ, OH, PA, VA, WV.

From `transmission_capacity_init_AC_ba_NARIS2024.csv`:

- 42 transfer interfaces lie inside this footprint.
- 24 interfaces connect it to neighbours in MISO, NYISO and SERTP.

The overlay that selects it is `configs/pypsa-usa/config.pjm_smoke.yaml`:

```yaml
scenario:
  interconnect: [eastern]
  clusters: [22]
model_topology:
  include:
    trans_reg: ['PJM']
```

Upstream documents `trans_reg` as a valid filter in `docs/source/config-spatial.md`, but ships no example that uses it. **Whether it works end to end is exactly what the smoke run tests.**

### The ReEDS "PJM" region is not PJM's actual footprint

ReEDS zones follow state and county lines, so the match is approximate.

- **Missing from the extract:** PJM territory in Indiana (AEP), North Carolina (Dominion) and Tennessee. ReEDS assigns all Indiana zones to MISO and the North Carolina and Tennessee zones to SERTP.
- **Size of the gap (indicative):** in the EIA-860 2025 fleet processed for the earlier local model, about 12.9 GW of 210 GW (6.2%) of capacity reporting PJM as balancing authority sits in those three states: IN 9.6 GW, NC 3.2 GW, TN 0.2 GW.
- **Not quantified:** the reverse error, plants inside the 22 zones that are not PJM members.

That 6.2% figure comes from a local dataset that is not in this repository, so treat it as an order of magnitude until it is reproduced from PyPSA-USA's own plant table.

## 5. Reproduction attempt on the Windows workstation: blocked

Machine: Windows 11 Pro, 16 cores, 15 GB RAM, no WSL, no Docker, no conda. `uv` 0.13.1.

| Step | Command (from `pypsa-usa/`) | Result |
|---|---|---|
| Create environment | `python -m uv venv --python 3.11 .venv` | OK (CPython 3.11.17) |
| Install from lock | `python -m uv sync --frozen` | **Failed.** `datrie` 0.8.2 (a Snakemake 7 dependency) has no Windows wheel for Python 3.11 on PyPI. The source build stopped with `ImportError: DLL load failed while importing Utils: An Application Control policy has blocked this file` |
| Install without `datrie` | `python -m uv sync --frozen --no-install-package datrie` | OK |
| Import test | `python -c "import <module>"` for each compiled dependency | numpy, pandas, scipy, pyarrow, duckdb, shapely, pyproj, geopandas, tables, cartopy, highspy, gurobipy, linopy imported. **`netCDF4` and `rasterio` failed** with the same Application Control error, and so did `pypsa` and `atlite`, which import them |
| Dry run | `python -m snakemake -n -j1 --scheduler greedy --configfile <overlay>` with a pure-Python stand-in for `datrie` on `PYTHONPATH` | **Failed** at `rules/common.smk` line 17: the Snakefile imports `pypsa` at parse time, which hits the blocked `_netCDF4` library |

What this establishes:

- The pinned PyPSA-USA v1.0.0 environment cannot be used on this workstation as it is configured. The cause is the operating system's Application Control policy rejecting specific compiled files, not a defect in PyPSA-USA.
- The policy was left untouched. Changing it is the machine owner's decision.
- Independently of the policy, native Windows is a weak target: `retrieve_databundles.py` notes that its `unzip` call "will only work on linux and mac", and upstream's tooling is built around Linux and SLURM.

The `datrie` stand-in was a throwaway file used for that one dry run. It is not in this repository and must not be used for model runs.

## 6. What a real PJM baseline needs beyond the smoke run

The smoke run copies upstream's own test harness (one day, 2030 demand, capacity expansion allowed) and swaps the footprint. A baseline that can be compared with PJM outcomes is a different configuration:

1. **Historical demand** (`electricity.demand.profile: eia`): EIA-930 by balancing authority, **2018 to 2023 only**. Upstream's docs say this path needs a free EIA API key.
2. **Historical weather:** the default renewable dataset (GODEEEP) publishes only **2012** as a historical year; the full 1980-2022 archive sits on a Stanford-internal server. Public historical years 2018-2023 need `renewable.dataset: atlite` with ERA5 cutouts of 5 to 9 GB per year from Zenodo.
3. **Validation mode** (`run.validation: true`): produces comparison plots against EIA data and also needs the EIA API key.
4. **Fixed fleet:** no expansion candidates, technical retirement only, and a decision on boundary trade with MISO, NYISO and SERTP.

Consequences to decide, not assumed here:

- The latest back-cast year upstream supports is **2023**. A 2025 base year would require extending upstream's demand and weather inputs.
- The contract scenarios concern the late 2020s. Upstream's forward path (EFS or EER demand, 2030 horizon) is the natural place for them, with the back-cast used only to check the PJM extract.

## 7. Risks

| # | Risk | Severity | Mitigation |
|---|---|---|---|
| R1 | No execution environment on the workstation | High, blocks all runs | GitHub Actions for small runs now; decide on WSL2, a cloud VM or university HPC for full-year runs |
| R2 | `trans_reg: ['PJM']` filter never exercised upstream | Medium | Smoke run; fall back to listing the 22 `reeds_zone` ids |
| R3 | ReEDS PJM region omits IN, NC, TN territory (about 6% of capacity) | Medium | Quantify from PyPSA-USA's plant table; consider adding Indiana zones with a documented caveat |
| R4 | Zonal transfer limits, not nodal: congestion at a specific data-center site cannot be represented | High for site-level claims | State the limit; test county resolution or the TAMU network for one site only if the thesis needs it |
| R5 | Historical inputs end in 2023; default weather data not public for those years | Medium | atlite cutouts; choose 2023 as back-cast year |
| R6 | No plug-in hook for custom constraints | Medium | Keep the contract module in this repository and call it through one minimal, documented patch or a wrapper |
| R7 | GitHub-hosted runner limits (4 cores, 16 GB RAM, limited disk, 6 h) | Medium | Enough for one-day and one-week tests; not for a full-year 22-zone solve with unit commitment |
| R8 | Smoke run allows capacity expansion and uses 2030 demand | Low, by design | Do not read its numbers as a PJM result |

## 8. Minimal plan

1. **Push this branch.** The workflow `.github/workflows/th003-pjm-smoke.yml` then installs the locked environment on Linux, dry-runs, builds the PJM data model and solves one day with HiGHS. Logs and the network files are stored as a run artifact. Add the run link and outcome to this document.
2. **If the build fails on the filter,** switch the overlay to the explicit `reeds_zone` list and rerun.
3. **Decide the execution environment** for larger runs (decision D13).
4. **Back-cast test:** one week of 2023, fixed fleet, EIA demand, atlite weather, validation plots. Needs an EIA API key stored as a repository secret.
5. **Then TH-004:** the 3 to 5 bus firm-access prototype. It needs only PyPSA and Linopy, not the PyPSA-USA workflow, so R1 does not block it. A separate Python 3.12 environment on the workstation imports PyPSA 1.4.0 and solved a 2-bus toy with HiGHS on 16 Nov 2026. Those versions are newer than upstream's pins (PyPSA 1.3.0, Linopy 0.9.1), so the prototype's tests should also run in CI against the pinned versions.

## 9. Questions for human review

- Which Linux environment will the thesis use for full-year runs?
- Is 2023 acceptable as the back-cast year, given upstream's data limits?
- Is a zonal PJM testbed sufficient for the thesis claims, or is site-level congestion required?
- Should Indiana be added to the footprint to cover AEP's PJM territory?
- May the earlier local 2025 EIA dataset (load by zone, fleet) be used as an independent benchmark for the extract (decision D12)?

## 10. Files in this branch

| File | Purpose |
|---|---|
| `docs/PJM_BASELINE_FEASIBILITY.md` | this report |
| `configs/pypsa-usa/config.pjm_smoke.yaml` | PJM overlay for the smoke run |
| `.github/workflows/th003-pjm-smoke.yml` | Linux run of the smoke test |
| `tools/summarize_network.py` | prints what the produced networks contain |
| `governance/handoffs/TH-003.md` | handoff |
| `governance/DECISIONS.md` | proposed decisions D12 to D14 added |
