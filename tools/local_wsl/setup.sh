#!/bin/bash
# Set up PyPSA-USA v1.0.0 in an Ubuntu (WSL 2) home directory without sudo.
#
# Usage, from an Ubuntu shell:   bash tools/local_wsl/setup.sh
# Everything goes under ~/thesis, ~/.local/bin (uv) and ~/.duckdb. Safe to re-run.
# Background and known pitfalls: docs/LOCAL_WSL_SETUP.md
set -euo pipefail

PIN=04a0edd220b1d331715c269a4eab68344c07a088   # PyPSA-USA v1.0.0
THESIS_BRANCH="${THESIS_BRANCH:-main}"
ROOT="${THESIS_ROOT:-$HOME/thesis}"
TOOLS="$ROOT/mamba/envs/tools"
mkdir -p "$ROOT" && cd "$ROOT"
export PATH="$HOME/.local/bin:$PATH"

echo "=== 1. uv (official installer, installs to ~/.local/bin)"
if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
uv --version

echo "=== 2. tools environment without sudo: ipopt, a C compiler, unzip"
# - ipopt: upstream's cluster-count step calls the ipopt executable when HiGHS is the solver.
# - C compiler: datrie (a Snakemake 7 dependency) has no wheel for Python 3.11 and is built from source.
# The plain micromamba binary is used because a fresh Ubuntu image has no bzip2 to unpack the tarball.
if [ ! -x "$ROOT/bin/micromamba" ]; then
  mkdir -p "$ROOT/bin"
  curl -LsSf -o "$ROOT/bin/micromamba" https://github.com/mamba-org/micromamba-releases/releases/latest/download/micromamba-linux-64
  chmod +x "$ROOT/bin/micromamba"
fi
"$ROOT/bin/micromamba" --version
if [ ! -x "$TOOLS/bin/ipopt" ]; then
  "$ROOT/bin/micromamba" create -y -q -r "$ROOT/mamba" -p "$TOOLS" -c conda-forge ipopt c-compiler unzip
fi
"$TOOLS/bin/ipopt" --version | head -1

echo "=== 3. repositories"
if [ ! -d pypsa-usa/.git ]; then
  git clone --quiet --filter=blob:none https://github.com/PyPSA/pypsa-usa.git
fi
git -C pypsa-usa checkout --quiet "$PIN"
echo "pypsa-usa at $(git -C pypsa-usa rev-parse HEAD)"
if [ ! -d MSRE-Thesis/.git ]; then
  git clone --quiet --branch "$THESIS_BRANCH" https://github.com/qasjadullah-design/MSRE-Thesis.git
fi
echo "MSRE-Thesis at $(git -C MSRE-Thesis rev-parse --short HEAD) ($(git -C MSRE-Thesis branch --show-current))"

echo "=== 4. locked Python environment"
cd "$ROOT/pypsa-usa"
bash init_pypsa_usa.sh | tail -3
# datrie 0.8.2 (2020) trips a pointer-type check that GCC 14 and later treat as an error.
# Downgrade it to a warning, which is what older compilers (GCC 13 on GitHub's runner) do.
"$ROOT/bin/micromamba" run -r "$ROOT/mamba" -p "$TOOLS" bash -c \
  'echo "compiler: $(cc --version | head -1)"; CFLAGS="${CFLAGS:-} -Wno-error=incompatible-pointer-types" uv sync --frozen 2>&1 | tail -5'

echo "=== 5. DuckDB httpfs extension over HTTPS"
# DuckDB 0.10.0 fetches extensions over plain http://, which some networks block. Placing the same
# file from the official server (over https) where DuckDB looks makes its own download unnecessary.
DUCKDB_VERSION=$(uv run python -c "import duckdb; print(duckdb.__version__)")
EXT_DIR="$HOME/.duckdb/extensions/v$DUCKDB_VERSION/linux_amd64_gcc4"
if [ ! -s "$EXT_DIR/httpfs.duckdb_extension" ]; then
  mkdir -p "$EXT_DIR"
  curl -sSf -o "$EXT_DIR/httpfs.duckdb_extension.gz" \
    "https://extensions.duckdb.org/v$DUCKDB_VERSION/linux_amd64_gcc4/httpfs.duckdb_extension.gz"
  gunzip -f "$EXT_DIR/httpfs.duckdb_extension.gz"
fi
ls -la "$EXT_DIR" | tail -1

echo "=== 6. check"
uv run python -c "import sys, pypsa, linopy, snakemake, highspy, netCDF4, rasterio, atlite, datrie, duckdb; duckdb.query('INSTALL httpfs; LOAD httpfs;'); print('python', sys.version.split()[0], '| pypsa', pypsa.__version__, '| linopy', linopy.__version__, '| snakemake', snakemake.__version__, '| duckdb', duckdb.__version__, '| imports and httpfs OK')"
du -sh "$ROOT" | cut -f1
echo "=== SETUP DONE"
