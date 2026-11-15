"""Print a Markdown summary of the PyPSA-USA networks produced by a run.

Usage: python summarize_network.py <path to pypsa-usa/workflow> [run name]

Reports what the files contain. It makes no claim that the numbers are
calibrated or validated; see docs/PJM_BASELINE_FEASIBILITY.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pypsa


def capacity_by_carrier(n: pypsa.Network, solved: bool) -> str:
    column = "p_nom_opt" if solved else "p_nom"
    rows = []
    for name, frame in (("Generator", n.generators), ("StorageUnit", n.storage_units)):
        if frame.empty:
            continue
        gw = frame.groupby("carrier")[column].sum().div(1e3)
        rows += [f"| {name} | {carrier} | {value:,.2f} |" for carrier, value in gw.sort_values(ascending=False).items()]
    header = f"| Component | Carrier | {column} (GW) |\n|---|---|---:|\n"
    return header + "\n".join(rows)


def describe(path: Path, solved: bool) -> str:
    n = pypsa.Network(path)
    ac_buses = n.buses[n.buses.carrier == "AC"] if "carrier" in n.buses else n.buses
    lines = [
        f"### `{path.name}`",
        "",
        f"- Snapshots: {len(n.snapshots)} ({n.snapshots[0]} to {n.snapshots[-1]})",
        f"- Buses: {len(n.buses)} ({len(ac_buses)} AC)",
        f"- Lines: {len(n.lines)}, links: {len(n.links)}",
        f"- Generators: {len(n.generators)}, storage units: {len(n.storage_units)}, loads: {len(n.loads)}",
    ]
    for column in ("reeds_zone", "trans_reg", "reeds_state"):
        if column in n.buses:
            values = sorted(n.buses[column].dropna().astype(str).unique())
            lines.append(f"- `{column}` values on buses ({len(values)}): {', '.join(values)}")
    if not n.loads_t.p_set.empty:
        load = n.loads_t.p_set.sum(axis=1)
        lines.append(f"- Load over the snapshots: peak {load.max() / 1e3:,.1f} GW, mean {load.mean() / 1e3:,.1f} GW")
    if solved:
        objective = getattr(n, "objective", None)
        lines.append(f"- Objective value reported by the solver: {objective:,.0f}" if objective is not None else "- Objective: not stored")
        if not n.buses_t.marginal_price.empty:
            price = n.buses_t.marginal_price[ac_buses.index.intersection(n.buses_t.marginal_price.columns)]
            lines.append(f"- Bus marginal price: mean {price.mean().mean():,.2f}, max {price.max().max():,.2f} (currency/MWh)")
    lines += ["", capacity_by_carrier(n, solved), ""]
    return "\n".join(lines)


def main() -> int:
    workflow = Path(sys.argv[1])
    run = sys.argv[2] if len(sys.argv) > 2 else "pjm_smoke"
    print(f"## PyPSA-USA run `{run}`: network summary\n")
    found = False
    for label, folder, solved in (
        ("Solved network", workflow / "results" / run, True),
        ("Unsolved data model", workflow / "resources" / run / "networks", False),
    ):
        files = sorted(p for p in folder.rglob("*.nc") if "_ec_" in p.name) if folder.exists() else []
        if not files:
            print(f"**{label}: no file found under `{folder}`.**\n")
            continue
        found = True
        print(f"**{label}**\n")
        for path in files:
            print(describe(path, solved))
    return 0 if found else 1


if __name__ == "__main__":
    raise SystemExit(main())
