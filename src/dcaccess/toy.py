"""Synthetic three-zone test system.

EVERY NUMBER IN THIS FILE IS SYNTHETIC. The system is invented to exercise the
site model. It represents no real grid, fleet, price or data centre, and no
result from it is a research finding.

Zones are joined by transfer limits (bidirectional links), the same transport
representation as the zonal PJM extract from PyPSA-USA.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pypsa

VOLL = 10_000.0  # currency/MWh, synthetic penalty for involuntary unserved energy
SYSTEM_UNSERVED_CARRIER = "system unserved"
HOURS_PER_YEAR = 8760.0

# carrier: tCO2 per MWh of fuel (synthetic round values)
CARRIERS = {"nuclear": 0.0, "coal": 0.34, "gas": 0.18, "wind": 0.0}

# name: (bus, carrier, p_nom MW, marginal cost per MWh_e, efficiency)
GENERATORS = {
    "A nuclear": ("A", "nuclear", 2000.0, 10.0, 0.33),
    "A coal": ("A", "coal", 1500.0, 30.0, 0.38),
    "A wind": ("A", "wind", 1000.0, 0.0, 1.0),
    "B ccgt": ("B", "gas", 1500.0, 45.0, 0.55),
    "B ocgt": ("B", "gas", 700.0, 90.0, 0.35),
    "C ccgt": ("C", "gas", 1200.0, 48.0, 0.55),
    "C ocgt": ("C", "gas", 400.0, 95.0, 0.35),
}
PEAK_LOAD = {"A": 500.0, "B": 3000.0, "C": 1500.0}  # MW
TRANSFER = {("A", "B"): 2000.0, ("A", "C"): 1000.0, ("B", "C"): 600.0}  # MW, both directions

NEW_CAPACITY_CAPITAL_COST = 60_000.0  # currency/MW-year, synthetic
NEW_CAPACITY_MARGINAL_COST = 100.0
NEW_CAPACITY_EFFICIENCY = 0.35


def load_factor(hours: int) -> np.ndarray:
    """Diurnal shape: 1.0 at 18:00, 0.5 at 06:00."""
    hour_of_day = np.arange(hours) % 24
    return 0.75 + 0.25 * np.cos(2 * np.pi * (hour_of_day - 18) / 24)


def wind_factor(hours: int) -> np.ndarray:
    """Deterministic synthetic availability between 0.15 and 0.55."""
    return 0.35 + 0.20 * np.sin(2 * np.pi * np.arange(hours) / 31)


def build_toy_network(
    hours: int = 48,
    transfer_scale: dict[tuple[str, str], float] | None = None,
    load_scale: float = 1.0,
    expansion: bool = False,
) -> pypsa.Network:
    """Return the unsolved synthetic system.

    Snapshot weightings scale the modelled hours to one year, so costs are
    annual and comparable with annualised capital cost.

    transfer_scale
        Optional multipliers on individual transfer limits, e.g. ``{("A", "C"): 0.5}``.
    load_scale
        Multiplier on every zone's load.
    expansion
        If true, each zone may build new peaking capacity at an annualised cost.
    """
    n = pypsa.Network()
    n.set_snapshots(pd.date_range("2030-01-01", periods=hours, freq="h"))
    n.snapshot_weightings.loc[:, :] = HOURS_PER_YEAR / hours

    for carrier, co2 in CARRIERS.items():
        n.add("Carrier", carrier, co2_emissions=co2)
    n.add("Carrier", SYSTEM_UNSERVED_CARRIER)
    n.add("Carrier", "transfer")
    n.add("Carrier", "AC")

    shape = pd.Series(load_factor(hours), index=n.snapshots)
    wind = pd.Series(wind_factor(hours), index=n.snapshots)

    for bus, peak in PEAK_LOAD.items():
        n.add("Bus", bus, carrier="AC")
        n.add("Load", f"{bus} load", bus=bus, p_set=peak * load_scale * shape)
        n.add(
            "Generator",
            f"{bus} unserved",
            bus=bus,
            carrier=SYSTEM_UNSERVED_CARRIER,
            p_nom=peak * load_scale,
            marginal_cost=VOLL,
        )

    for name, (bus, carrier, p_nom, marginal_cost, efficiency) in GENERATORS.items():
        n.add(
            "Generator",
            name,
            bus=bus,
            carrier=carrier,
            p_nom=p_nom,
            marginal_cost=marginal_cost,
            efficiency=efficiency,
            p_max_pu=wind if carrier == "wind" else 1.0,
        )

    scales = transfer_scale or {}
    for (bus0, bus1), limit in TRANSFER.items():
        n.add(
            "Link",
            f"{bus0}-{bus1}",
            bus0=bus0,
            bus1=bus1,
            carrier="transfer",
            p_nom=limit * scales.get((bus0, bus1), 1.0),
            p_min_pu=-1.0,
            efficiency=1.0,
        )

    if expansion:
        for bus in PEAK_LOAD:
            n.add(
                "Generator",
                f"{bus} new",
                bus=bus,
                carrier="gas",
                p_nom=0.0,
                p_nom_extendable=True,
                capital_cost=NEW_CAPACITY_CAPITAL_COST,
                marginal_cost=NEW_CAPACITY_MARGINAL_COST,
                efficiency=NEW_CAPACITY_EFFICIENCY,
            )
    return n
