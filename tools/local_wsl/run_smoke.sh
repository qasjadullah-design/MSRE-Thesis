#!/bin/bash
# One-day PJM smoke test of PyPSA-USA v1.0.0 in Ubuntu (WSL 2), using the same config as the CI workflow.
#
# Usage, after tools/local_wsl/setup.sh:   bash tools/local_wsl/run_smoke.sh
# Optional: JOBS=4 bash tools/local_wsl/run_smoke.sh   (default 2, to stay inside about 7 GB of RAM)
# Logs: ~/thesis/smoke_build_console.log and ~/thesis/smoke_solve_console.log
set -uo pipefail

ROOT="${THESIS_ROOT:-$HOME/thesis}"
export PATH="$ROOT/mamba/envs/tools/bin:$HOME/.local/bin:$PATH"
CONFIG="$ROOT/MSRE-Thesis/configs/pypsa-usa/config.pjm_smoke.yaml"
SOLVED="results/pjm_smoke/eastern/networks/elec_s75_c22_ec_lv1.0_1h_E.nc"
JOBS="${JOBS:-2}"
cd "$ROOT/pypsa-usa/workflow"

stamp() { date +"%H:%M:%S"; }
echo "[$(stamp)] start | thesis repo $(git -C "$ROOT/MSRE-Thesis" rev-parse --short HEAD) | upstream $(git -C "$ROOT/pypsa-usa" rev-parse --short HEAD) | jobs $JOBS"
free -m | awk '/Mem:/ {print "RAM MB total " $2 ", available " $7}'
command -v ipopt || { echo "ipopt not on PATH: run tools/local_wsl/setup.sh first"; exit 1; }

# Targets go before --configfile, which accepts several values.
echo "[$(stamp)] dry run"
uv run snakemake "$SOLVED" -n -j"$JOBS" --scheduler greedy --rerun-incomplete --configfile "$CONFIG" 2>&1 | tail -n 25
[ "${PIPESTATUS[0]}" -eq 0 ] || { echo "DRY RUN FAILED"; exit 1; }

echo "[$(stamp)] build data model"
uv run snakemake data_model -j"$JOBS" --scheduler greedy --rerun-incomplete --configfile "$CONFIG" > "$ROOT/smoke_build_console.log" 2>&1
rc=$?
echo "[$(stamp)] build exit code $rc"
if [ $rc -ne 0 ]; then
  python3 "$ROOT/MSRE-Thesis/tools/ci_annotate_logs.py" . "$ROOT/smoke_build_console.log" | sed 's/%0A/\n/g' | tail -n 60
  dmesg 2>/dev/null | grep -i -E "out of memory|oom" | tail -n 5
  exit 1
fi

echo "[$(stamp)] solve"
uv run snakemake "$SOLVED" -j"$JOBS" --scheduler greedy --rerun-incomplete --configfile "$CONFIG" > "$ROOT/smoke_solve_console.log" 2>&1
rc=$?
echo "[$(stamp)] solve exit code $rc"
if [ $rc -ne 0 ]; then
  python3 "$ROOT/MSRE-Thesis/tools/ci_annotate_logs.py" . "$ROOT/smoke_solve_console.log" | sed 's/%0A/\n/g' | tail -n 60
  exit 1
fi

echo "[$(stamp)] summary"
( cd "$ROOT/pypsa-usa" && uv run python "$ROOT/MSRE-Thesis/tools/summarize_network.py" workflow 2>/dev/null | sed -n '1,32p' )
echo "--- solver log tail"
find logs -name "*solver.log" | head -n 1 | xargs -r tail -n 12
echo "--- peak memory by rule (MB) and run time, from Snakemake benchmarks"
for f in $(find benchmarks/pjm_smoke -type f 2>/dev/null); do
  awk -v n="$f" 'NR==2 {printf "%8.0f  %6.0f s  %s\n", $3, $1, n}' "$f"
done | sort -rn | head -n 8
du -sh "$ROOT/pypsa-usa/workflow/data" "$ROOT" 2>/dev/null
echo "[$(stamp)] SMOKE DONE"
