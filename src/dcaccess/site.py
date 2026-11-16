"""Data-centre site with contracted grid access, attached to a PyPSA network.

Topology (all native PyPSA components, no custom constraints):

    grid bus --[firm entitlement link]--> meter bus --[POI link]--> site bus
                                                                     |- gross load D
                                                                     |- co-located generator (installed G)
                                                                     |- voluntary curtailment (<= alpha * D)
                                                                     |- involuntary unserved load

The entitlement link carries the contract (MW the site may withdraw). The POI
link carries the physical import capability. They are separate on purpose:
later service classes add further entitlement links into the same meter bus,
and the POI link caps their sum. Both links are one-directional, so the site
cannot export.

Voluntary curtailment is limited by the site's physical flexibility. A contract
right to interrupt grid service does not by itself reduce computing load: with
zero flexibility any shortfall appears as involuntary unserved load.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import pypsa

FIRM_CARRIER = "site firm import"
POI_CARRIER = "site poi"
LOAD_CARRIER = "site load"
CURTAILMENT_CARRIER = "site curtailment"
UNSERVED_CARRIER = "site unserved"


@dataclass(frozen=True)
class SiteSpec:
    """Inputs for one data-centre site. Power in MW, costs in currency per MWh.

    gross_load_mw
        Gross electrical demand of the facility, before any curtailment.
    poi_capacity_mw
        Physical import capability at the point of interconnection.
    firm_mw
        Contracted firm withdrawal. It is an input of its own: it is not derived
        from gross load or from the co-located generator's capacity.
    onsite_capacity_mw
        Installed capacity of the co-located generator. Zero means a load with
        no generator, which is a hypothetical counterfactual in this project.
    onsite_availability
        Per-unit availability of the generator; 0 in outage hours.
    onsite_marginal_cost
        Operating cost of the generator per MWh of electricity.
    onsite_efficiency, onsite_carrier
        Used for emissions accounting: fuel = electricity / efficiency, and the
        carrier's ``co2_emissions`` is per MWh of fuel.
    flexible_share
        Largest share of gross load the site can physically curtail in an hour.
    curtailment_cost
        The site's own cost of lost computing per MWh curtailed.
    voll
        Penalty per MWh of involuntary unserved site load.
    """

    name: str
    grid_bus: str
    gross_load_mw: float | pd.Series
    poi_capacity_mw: float
    firm_mw: float
    voll: float
    onsite_capacity_mw: float = 0.0
    onsite_availability: float | pd.Series = 1.0
    onsite_marginal_cost: float = 0.0
    onsite_efficiency: float = 1.0
    onsite_carrier: str = "gas"
    flexible_share: float = 0.0
    curtailment_cost: float = 0.0

    def validate(self) -> None:
        if self.poi_capacity_mw < 0 or self.firm_mw < 0 or self.onsite_capacity_mw < 0:
            raise ValueError("Capacities must be non-negative.")
        if self.firm_mw > self.poi_capacity_mw:
            raise ValueError(
                f"Firm entitlement ({self.firm_mw} MW) exceeds the physical POI capability "
                f"({self.poi_capacity_mw} MW)."
            )
        if not 0.0 <= self.flexible_share <= 1.0:
            raise ValueError("flexible_share must lie between 0 and 1.")
        if not 0.0 < self.onsite_efficiency <= 1.0:
            raise ValueError("onsite_efficiency must lie in (0, 1].")
        if self.curtailment_cost < 0 or self.voll <= 0:
            raise ValueError("curtailment_cost must be non-negative and voll positive.")
        if self.flexible_share > 0 and self.curtailment_cost >= self.voll:
            raise ValueError("curtailment_cost must be below voll, or curtailment would never be chosen first.")


def _as_series(value: float | pd.Series, snapshots: pd.Index, label: str) -> pd.Series:
    if isinstance(value, pd.Series):
        if not value.index.equals(snapshots):
            raise ValueError(f"{label} must be indexed by the network snapshots.")
        return value.astype(float)
    return pd.Series(float(value), index=snapshots)


def component_names(name: str) -> dict[str, str]:
    """Names of the components that ``add_site`` creates for a site."""
    return {
        "site_bus": f"{name}",
        "meter_bus": f"{name} meter",
        "firm_link": f"{name} firm import",
        "poi_link": f"{name} poi",
        "load": f"{name} load",
        "onsite": f"{name} onsite",
        "curtailment": f"{name} curtailment",
        "unserved": f"{name} unserved",
    }


def add_site(n: pypsa.Network, spec: SiteSpec) -> dict[str, str]:
    """Attach a firm-access data-centre site to ``n`` and return its component names."""
    spec.validate()
    if spec.grid_bus not in n.buses.index:
        raise ValueError(f"Grid bus '{spec.grid_bus}' is not in the network.")
    names = component_names(spec.name)
    if names["site_bus"] in n.buses.index:
        raise ValueError(f"A bus named '{names['site_bus']}' already exists.")

    load = _as_series(spec.gross_load_mw, n.snapshots, "gross_load_mw")
    if (load < 0).any():
        raise ValueError("gross_load_mw must be non-negative.")
    availability = _as_series(spec.onsite_availability, n.snapshots, "onsite_availability")
    if ((availability < 0) | (availability > 1)).any():
        raise ValueError("onsite_availability must lie between 0 and 1.")
    peak = float(load.max())

    for carrier in (FIRM_CARRIER, POI_CARRIER, LOAD_CARRIER, CURTAILMENT_CARRIER, UNSERVED_CARRIER):
        if carrier not in n.carriers.index:
            n.add("Carrier", carrier)
    if spec.onsite_capacity_mw > 0 and spec.onsite_carrier not in n.carriers.index:
        raise ValueError(f"Carrier '{spec.onsite_carrier}' must exist in the network for emissions accounting.")

    n.add("Bus", names["site_bus"], carrier="AC")
    n.add("Bus", names["meter_bus"], carrier="AC")

    n.add(
        "Link",
        names["firm_link"],
        bus0=spec.grid_bus,
        bus1=names["meter_bus"],
        carrier=FIRM_CARRIER,
        p_nom=spec.firm_mw,
        p_min_pu=0.0,
        efficiency=1.0,
    )
    n.add(
        "Link",
        names["poi_link"],
        bus0=names["meter_bus"],
        bus1=names["site_bus"],
        carrier=POI_CARRIER,
        p_nom=spec.poi_capacity_mw,
        p_min_pu=0.0,
        efficiency=1.0,
    )
    n.add("Load", names["load"], bus=names["site_bus"], carrier=LOAD_CARRIER, p_set=load)

    if spec.onsite_capacity_mw > 0:
        n.add(
            "Generator",
            names["onsite"],
            bus=names["site_bus"],
            carrier=spec.onsite_carrier,
            p_nom=spec.onsite_capacity_mw,
            p_max_pu=availability,
            marginal_cost=spec.onsite_marginal_cost,
            efficiency=spec.onsite_efficiency,
        )

    curtailable_peak = spec.flexible_share * peak
    if curtailable_peak > 0:
        n.add(
            "Generator",
            names["curtailment"],
            bus=names["site_bus"],
            carrier=CURTAILMENT_CARRIER,
            p_nom=curtailable_peak,
            p_max_pu=(spec.flexible_share * load / curtailable_peak),
            marginal_cost=spec.curtailment_cost,
        )
    if peak > 0:
        n.add(
            "Generator",
            names["unserved"],
            bus=names["site_bus"],
            carrier=UNSERVED_CARRIER,
            p_nom=peak,
            p_max_pu=(load / peak),
            marginal_cost=spec.voll,
        )
    return names
