# Running PyPSA-USA locally on the Windows workstation (WSL 2)

- **Purpose:** a complete record of how the pinned PyPSA-USA v1.0.0 environment was made to work on the project's Windows 11 workstation, so that any person or agent can repeat or repair it without earlier conversations.
- **Date of setup:** 16 November 2026. **Author:** Claude Code.
- **Status:** environment installed, and the one-day PJM smoke run **builds and solves to Optimal on this machine** (16 November 2026, section 6). It is the same feasibility test as on GitHub, not a validated PJM model.
- **Scripts:** `tools/local_wsl/setup.sh` and `tools/local_wsl/run_smoke.sh`.

## 1. Why WSL is needed

Native Windows cannot run the pinned environment on this machine (details in `docs/PJM_BASELINE_FEASIBILITY.md`, section 5):

- Windows **Smart App Control** is on. It blocks the compiled libraries in the pinned `netCDF4` 1.6.4 and `rasterio` 1.3.8, so `pypsa` and `atlite` cannot be imported. Running Python as administrator does not change this.
- `datrie` 0.8.2, a Snakemake 7 dependency, has no Windows wheel for Python 3.11.

Smart App Control was left on. Linux programs inside WSL 2 are not subject to it.

## 2. Machine

| Item | Value |
|---|---|
| Windows | Windows 11 Pro, build 26200 |
| Hardware | 16 cores, 15 GB RAM |
| WSL | version 3.0.5, kernel 6.18, WSL 2 |
| Distribution | Ubuntu 24.04.5 LTS |
| Linux resources seen | 16 cores, about 7.4 GB RAM and 2 GB swap (WSL's default is half the host memory) |
| Windows accounts | the daily account is a **standard user**; the only administrator is the built-in `Administrator` account |

## 3. Installing WSL and Ubuntu (done by the machine owner)

These steps change Windows features, so the owner performs them. An agent must not.

1. Restart Windows if a restart is pending.
2. Open PowerShell with "Run as administrator" (the Administrator account's password is needed) and run `wsl --install --no-distribution`. Restart Windows when asked.
3. Log in as the **daily account** and, in a normal PowerShell window, run `wsl --install --web-download -d Ubuntu-24.04`. Choose a Linux username and password when Ubuntu opens.

What went wrong on the way, so it is not repeated:

| Symptom | Cause | Fix |
|---|---|---|
| Download stopped at about 80% and nothing was installed | Internet connection dropped; the download does not resume | Run the command again |
| `Missing ] at end of attribute` when pasting the command | Two stray characters (`[O`) were inserted in front of the command by a terminal panel | Use a separate PowerShell window and retype the command |
| `WSL2 is unable to start since virtualization is not enabled` | Windows had not been restarted after the feature was enabled | Restart |
| `Windows Subsystem for Linux has no installed distributions` after a "successful" install | A distribution belongs to the Windows account that installs it. Installing Ubuntu from the administrator window registers it for `Administrator`, not for the daily account | Install the distribution from the daily account (step 3) |

Check from Windows: `wsl -l -v` should list `Ubuntu-24.04`, state Running or Stopped, version 2.

## 4. Installing PyPSA-USA inside Ubuntu

No sudo is needed. In an Ubuntu shell:

```bash
git clone https://github.com/qasjadullah-design/MSRE-Thesis.git ~/thesis/MSRE-Thesis
bash ~/thesis/MSRE-Thesis/tools/local_wsl/setup.sh
```

The script is safe to re-run. It creates:

| Location | Content |
|---|---|
| `~/.local/bin/uv` | `uv` (official installer from astral.sh) |
| `~/thesis/bin/micromamba` | micromamba binary (official mamba-org release) |
| `~/thesis/mamba/envs/tools` | `ipopt`, a C compiler and `unzip` from conda-forge |
| `~/thesis/pypsa-usa` | upstream at commit `04a0edd220b1d331715c269a4eab68344c07a088` (v1.0.0), with its locked environment in `.venv` |
| `~/thesis/MSRE-Thesis` | this repository |
| `~/.duckdb/extensions/v0.10.0/linux_amd64_gcc4/` | the DuckDB `httpfs` extension |

Verified on 16 November 2026: Python 3.11.18, PyPSA 1.3.0, Linopy 0.9.1, Snakemake 7.32.4, DuckDB 0.10.0, and `netCDF4`, `rasterio`, `atlite` and `datrie` all import. Size after setup, before any data: 3.1 GB.

To run commands in Ubuntu from Windows without opening it: `wsl.exe -e bash <script path under /mnt/c or /mnt/d>`. From Git Bash, prefix with `MSYS_NO_PATHCONV=1`, or Linux paths are rewritten.

## 5. Problems met during setup, and how each was solved

| # | Problem | Cause | Solution in `setup.sh` |
|---|---|---|---|
| 1 | No `gcc`, `unzip` or `ipopt`, and `sudo` asks for a password | Fresh Ubuntu image | A micromamba environment in the home directory provides all three without sudo |
| 2 | `tar: bzip2: Cannot exec` when unpacking micromamba | The image has no `bzip2` | Download the plain micromamba binary from the mamba-org GitHub releases |
| 3 | `uv sync` fails building `datrie`: "incompatible pointer type" | `datrie` 0.8.2 is built from source; GCC 14 and later (15.3 here) treat that check as an error | `CFLAGS=-Wno-error=incompatible-pointer-types` for the build. GitHub's runner has GCC 13, where it is a warning |
| 4 | `duckdb.HTTPException: Failed to download extension "httpfs" at URL "http://extensions.duckdb.org/..."` in `build_powerplants` and `build_cost_data` | DuckDB 0.10.0 fetches extensions over plain `http://`. The network this PC was on blocks all plain HTTP: a FortiGate web filter answers "Web Page Blocked, Web Filter Service Error: invalid license". HTTPS is not affected | Download the same file over `https://` from DuckDB's official server into `~/.duckdb/extensions/...`; DuckDB then makes no HTTP request. This is network-specific and harmless elsewhere |

Problems already solved in the configuration and also relevant here (found on GitHub Actions, see `docs/PJM_BASELINE_FEASIBILITY.md` section 6.2): targets must come before `--configfile`; no environment variable may be named `PYPSA_*`; EER demand replaces the unreachable EFS data; legacy bus demand weighting avoids an upstream crash; `ipopt` must be on `PATH`; HiGHS crossover is switched on.

## 6. Running the one-day PJM smoke test

```bash
bash ~/thesis/MSRE-Thesis/tools/local_wsl/run_smoke.sh
```

It runs the dry run, builds the 22-zone PJM data model, solves one day with HiGHS and prints a network summary, the end of the solver log, and peak memory per rule. Console output of the two long steps goes to `~/thesis/smoke_build_console.log` and `~/thesis/smoke_solve_console.log`. Downloaded data is kept in `~/thesis/pypsa-usa/workflow/data`, so a rerun continues where the last one stopped.

**If a run is interrupted** (internet drops, the PC sleeps or is shut down): nothing needs to be cleaned up. Run the same command again. Snakemake skips every finished step, and `--rerun-incomplete` makes it redo any step that was cut off part-way, including a half-downloaded file.

### Result on this machine (16 November 2026)

| Item | Value |
|---|---|
| Thesis repo / upstream | `f227b9f` / `04a0edd` (v1.0.0) |
| Outcome | data model built, one day solved, **HiGHS "Model status: Optimal"** |
| Objective | 1.8735238492 × 10⁹, identical to GitHub run 43819895193 |
| Network | 22 buses, 84 links, 545 generators, 39 storage units, 22 loads, 24 snapshots: identical to the GitHub run |
| Time | build 19 min 19 s for the last 18 of 26 steps, most of it downloads; solve step 8 s (HiGHS 0.7 s) |
| Peak memory of any rule | 1.84 GB (`cluster_resources`); `build_powerplants` 1.70 GB; renewable profiles 1.65 GB |
| Disk | 7.6 GB of data in `workflow/data`, 4.7 GB for everything else under `~/thesis` |
| Parallel jobs | 2 |

The numbers in the solved network are artefacts of a one-day problem with expansion allowed, exactly as on GitHub (`docs/PJM_BASELINE_FEASIBILITY.md` section 6.4). They are not a PJM result.

How the run went, for the record: the dry run passed (26 jobs). Attempt 1 failed after three seconds on problem 4 of section 5. Attempt 2 reached step 8 and then stalled for hours: the internet connection dropped while `USATestSystem.zip` was downloading, and that download has no timeout, so it waited on a dead connection. It was stopped by hand. Attempt 3 stopped in the dry run with `IncompleteFilesException`, because the script passed `--rerun-incomplete` only to the real steps; fixed in `f227b9f`. Attempt 4 completed.

**If a download stalls** (no progress in the console log and the file size not growing): stop the run with `pkill -INT -f bin/snakemake` and run the script again.

## 7. Limits

- **Memory.** Linux sees about 7.4 GB. The one-day test peaks at 1.84 GB per rule, so it fits with room to spare at two parallel jobs. Longer horizons will need more: the solve grows with the number of snapshots. If a rule is killed for lack of memory, the limit can be raised with a `.wslconfig` file in the Windows user profile (`[wsl2]`, `memory=12GB`, `swap=8GB`), followed by `wsl --shutdown`. That restarts Ubuntu, so ask the owner first.
- **Full-year runs.** Whether a full-year 22-zone expansion fits on this laptop has not been tested. Decision D13 (execution environment for full-year runs) stays open until a one-week run has been profiled here.
- **Disk.** The Linux virtual disk lives on drive C:, which had about 55 GB free. One year of ERA5 weather data for a back-cast is 5 to 9 GB.
- **Network.** Plain HTTP is blocked on the network used on 16 November. Any future step that downloads over `http://` will fail the same way; prefer `https://` sources.
- **Keep the PC awake** during a run. WSL stops when Windows sleeps.

## 8. Removing it

Everything installed by the scripts is in `~/thesis`, `~/.local/bin/uv*`, `~/.cache/uv`, `~/.local/share/uv` and `~/.duckdb` inside Ubuntu. Deleting those removes it. Windows itself was not changed by the scripts.
