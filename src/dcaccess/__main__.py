"""Reproducible demonstration: ``python -m dcaccess``.

Solves the synthetic system without a site and with a firm-access site in three
states, and prints annual quantities. SYNTHETIC INPUTS: the numbers illustrate
the accounting and are not research results.
"""

from __future__ import annotations

import dataclasses
import logging

import linopy
import pandas as pd
import pypsa

from dcaccess import VOLL, SiteSpec, add_site, build_toy_network, solve, summary

SITE = SiteSpec(
    name="dc",
    grid_bus="C",
    gross_load_mw=1000.0,
    poi_capacity_mw=1000.0,
    firm_mw=700.0,
    voll=VOLL,
    onsite_capacity_mw=400.0,
    onsite_marginal_cost=60.0,
    onsite_efficiency=0.40,
    flexible_share=0.10,
    curtailment_cost=2000.0,
)

CASES = {
    "no site": None,
    "firm 700 MW, generator available": SITE,
    "firm 700 MW, generator out": dataclasses.replace(SITE, onsite_availability=0.0),
    "firm 700 MW, generator out, no flexibility": dataclasses.replace(
        SITE, onsite_availability=0.0, flexible_share=0.0
    ),
}


def main() -> None:
    logging.disable(logging.CRITICAL)
    rows = {}
    for label, spec in CASES.items():
        n = build_toy_network()
        if spec is not None:
            add_site(n, spec)
        rows[label] = summary(solve(n), spec.name if spec else None)
    table = pd.DataFrame(rows).T.fillna(0.0)
    table["cost increase vs no site"] = table["system cost"] - table.loc["no site", "system cost"]
    columns = [
        "system cost",
        "cost increase vs no site",
        "site grid import MWh",
        "site onsite MWh",
        "site curtailed MWh",
        "site unserved MWh",
        "emissions tCO2",
    ]
    print(f"pypsa {pypsa.__version__}, linopy {linopy.__version__}; synthetic three-zone system, 48 h scaled to one year")
    with pd.option_context("display.width", 250, "display.max_columns", 20, "display.float_format", "{:,.0f}".format):
        print(table[columns].to_string())


if __name__ == "__main__":
    main()
