"""Solve wrapper and post-solve accounting: site balance, costs, emissions.

Costs here are the physical-system objective of the optimisation. They are not
tariffs, revenue requirements or customer bills.
"""

from __future__ import annotations

import pandas as pd
import pypsa

from dcaccess.site import (
    CURTAILMENT_CARRIER,
    UNSERVED_CARRIER,
    component_names,
)
from dcaccess.toy import SYSTEM_UNSERVED_CARRIER

NON_PHYSICAL_CARRIERS = (CURTAILMENT_CARRIER, UNSERVED_CARRIER, SYSTEM_UNSERVED_CARRIER)


def solve(n: pypsa.Network) -> pypsa.Network:
    """Solve with HiGHS and fail loudly unless the solver reports an optimal solution."""
    status, condition = n.optimize(solver_name="highs", log_to_console=False)
    if status != "ok" or condition != "optimal":
        raise RuntimeError(f"Solve did not reach optimality: status={status}, condition={condition}")
    return n


def _weights(n: pypsa.Network) -> pd.Series:
    return n.snapshot_weightings["objective"]


def site_balance(n: pypsa.Network, name: str) -> pd.DataFrame:
    """Hourly MW accounts of one site. ``residual`` must be zero.

    gross_load = grid_import + onsite + curtailed + unserved
    served     = gross_load - curtailed - unserved
    """
    names = component_names(name)
    gens = n.generators_t.p
    zero = pd.Series(0.0, index=n.snapshots)
    frame = pd.DataFrame(
        {
            "gross_load": n.loads_t.p_set[names["load"]],
            "firm_withdrawal": n.links_t.p0[names["firm_link"]],
            "grid_import": -n.links_t.p1[names["poi_link"]],
            "onsite": gens[names["onsite"]] if names["onsite"] in gens else zero,
            "curtailed": gens[names["curtailment"]] if names["curtailment"] in gens else zero,
            "unserved": gens[names["unserved"]] if names["unserved"] in gens else zero,
        }
    )
    frame["served"] = frame.gross_load - frame.curtailed - frame.unserved
    frame["residual"] = frame.grid_import + frame.onsite + frame.curtailed + frame.unserved - frame.gross_load
    return frame


def annual_energy(n: pypsa.Network, series: pd.Series) -> float:
    """Weighted MWh over the modelled year for an hourly MW series."""
    return float((series * _weights(n)).sum())


def cost_breakdown(n: pypsa.Network) -> pd.Series:
    """Annual objective cost split into non-overlapping parts that sum to ``total``."""
    gens = n.generators
    energy = n.generators_t.p.multiply(_weights(n), axis=0).sum()
    operating = energy * gens.marginal_cost
    by_carrier = operating.groupby(gens.carrier).sum()

    parts = {
        "generation": float(by_carrier.drop(index=list(NON_PHYSICAL_CARRIERS), errors="ignore").sum()),
        "site curtailment": float(by_carrier.get(CURTAILMENT_CARRIER, 0.0)),
        "site unserved": float(by_carrier.get(UNSERVED_CARRIER, 0.0)),
        "system unserved": float(by_carrier.get(SYSTEM_UNSERVED_CARRIER, 0.0)),
    }
    extendable = gens[gens.p_nom_extendable]
    parts["investment"] = float((extendable.p_nom_opt * extendable.capital_cost).sum())
    result = pd.Series(parts)
    result["total"] = result.sum()
    return result


def emissions(n: pypsa.Network) -> pd.Series:
    """Annual tCO2 per generator: electricity / efficiency x carrier emission factor."""
    gens = n.generators
    energy = n.generators_t.p.multiply(_weights(n), axis=0).sum()
    factor = gens.carrier.map(n.carriers.co2_emissions).fillna(0.0)
    return energy / gens.efficiency * factor


def summary(n: pypsa.Network, name: str | None = None) -> pd.Series:
    """Headline annual quantities for one solved case."""
    costs = cost_breakdown(n)
    co2 = emissions(n)
    gens = n.generators
    system_unserved = n.generators_t.p[gens.index[gens.carrier == SYSTEM_UNSERVED_CARRIER]].sum(axis=1)
    out = {
        "system cost": costs["total"],
        "investment": costs["investment"],
        "new capacity MW": float(gens.loc[gens.p_nom_extendable, "p_nom_opt"].sum()),
        "system unserved MWh": annual_energy(n, system_unserved),
        "emissions tCO2": float(co2.sum()),
    }
    if name is not None:
        balance = site_balance(n, name)
        onsite_name = component_names(name)["onsite"]
        out.update(
            {
                "site gross MWh": annual_energy(n, balance.gross_load),
                "site grid import MWh": annual_energy(n, balance.grid_import),
                "site onsite MWh": annual_energy(n, balance.onsite),
                "site curtailed MWh": annual_energy(n, balance.curtailed),
                "site unserved MWh": annual_energy(n, balance.unserved),
                "site peak import MW": float(balance.grid_import.max()),
                "site onsite tCO2": float(co2.get(onsite_name, 0.0)),
            }
        )
    return pd.Series(out)
