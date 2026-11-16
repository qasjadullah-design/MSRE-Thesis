"""Tests of the firm-access site model on the synthetic three-zone system.

All inputs are synthetic. The tests check that the model behaves as specified
in docs/SITE_MODEL_IMPLEMENTATION.md (acceptance tests A1 to A9); they establish no
research result.
"""

from __future__ import annotations

import dataclasses

import numpy as np
import pandas as pd
import pytest

from dcaccess import (
    VOLL,
    SiteSpec,
    add_site,
    build_toy_network,
    component_names,
    cost_breakdown,
    emissions,
    site_balance,
    solve,
    summary,
)
from dcaccess.toy import PEAK_LOAD, load_factor

TOL = 1e-4  # MW
SITE = "dc"

# Core site: installed co-located generator, firm entitlement below gross load.
CORE = SiteSpec(
    name=SITE,
    grid_bus="C",
    gross_load_mw=1000.0,
    poi_capacity_mw=1000.0,
    firm_mw=700.0,
    voll=VOLL,
    onsite_capacity_mw=400.0,
    onsite_marginal_cost=60.0,  # above every grid price in the unconstrained toy system
    onsite_efficiency=0.40,
    flexible_share=0.10,
    curtailment_cost=2000.0,
)


def solved(spec: SiteSpec | None = None, **network_kwargs):
    n = build_toy_network(**network_kwargs)
    if spec is not None:
        add_site(n, spec)
    return solve(n)


@pytest.fixture(scope="module")
def baseline():
    return solved()


@pytest.fixture(scope="module")
def core():
    return solved(CORE)


# --- A1: a site with no load leaves the system unchanged -------------------------------


def test_zero_load_site_matches_baseline(baseline):
    n = solved(dataclasses.replace(CORE, gross_load_mw=0.0))
    assert n.objective == pytest.approx(baseline.objective, rel=1e-9)
    assert site_balance(n, SITE).onsite.abs().max() < TOL  # nothing to serve and no export path


# --- A2: withdrawals respect the contract and the physical connection ------------------


def test_firm_withdrawal_never_exceeds_entitlement(core):
    balance = site_balance(core, SITE)
    assert balance.firm_withdrawal.max() <= CORE.firm_mw + TOL
    assert balance.grid_import.max() <= CORE.poi_capacity_mw + TOL


def test_entitlement_binds_when_grid_is_cheaper_than_onsite(core):
    # Grid energy is cheaper than the onsite unit in every hour, so the site
    # imports its full entitlement and the generator covers only the rest.
    balance = site_balance(core, SITE)
    assert np.allclose(balance.firm_withdrawal, CORE.firm_mw, atol=TOL)
    assert np.allclose(balance.onsite, 300.0, atol=TOL)
    assert balance.curtailed.abs().max() < TOL
    assert balance.unserved.abs().max() < TOL


def test_poi_limit_binds_when_generator_is_out():
    spec = dataclasses.replace(
        CORE, firm_mw=900.0, poi_capacity_mw=900.0, onsite_availability=0.0, flexible_share=0.0
    )
    balance = site_balance(solved(spec), SITE)
    assert np.allclose(balance.grid_import, 900.0, atol=TOL)
    assert np.allclose(balance.unserved, 100.0, atol=TOL)


def test_site_cannot_export():
    cheap_and_oversized = dataclasses.replace(CORE, onsite_capacity_mw=1200.0, onsite_marginal_cost=5.0)
    n = solved(cheap_and_oversized)
    balance = site_balance(n, SITE)
    assert balance.onsite.max() <= 1000.0 + TOL  # no more than the site's own load
    assert balance.grid_import.min() >= -TOL
    assert n.links_t.p0[component_names(SITE)["firm_link"]].min() >= -TOL


# --- A3: site energy balance ------------------------------------------------------------


@pytest.mark.parametrize(
    "changes",
    [
        {},
        {"onsite_availability": 0.0},
        {"flexible_share": 0.0, "onsite_availability": 0.0},
        {"onsite_capacity_mw": 0.0, "firm_mw": 1000.0},
    ],
)
def test_site_balance_closes(changes):
    balance = site_balance(solved(dataclasses.replace(CORE, **changes)), SITE)
    assert balance.residual.abs().max() < TOL
    assert (balance.served >= -TOL).all()


# --- A4: a contract limit does not shed computing load by itself -----------------------


def test_zero_flexibility_shortfall_is_involuntary_not_curtailment():
    spec = dataclasses.replace(CORE, flexible_share=0.0, onsite_availability=0.0)
    balance = site_balance(solved(spec), SITE)
    assert balance.curtailed.abs().max() < TOL
    assert np.allclose(balance.unserved, 300.0, atol=TOL)  # 1000 load - 700 firm, generator out


def test_curtailment_is_capped_by_physical_flexibility():
    spec = dataclasses.replace(CORE, onsite_availability=0.0)  # 10 % flexible
    balance = site_balance(solved(spec), SITE)
    assert np.allclose(balance.curtailed, 100.0, atol=TOL)
    assert np.allclose(balance.unserved, 200.0, atol=TOL)


# --- A5: stress cases give the quantities that arithmetic predicts ----------------------


def test_partial_generator_outage_only_affects_outage_hours():
    snapshots = build_toy_network().snapshots
    availability = pd.Series(1.0, index=snapshots)
    outage = snapshots[10:16]
    availability.loc[outage] = 0.0
    balance = site_balance(solved(dataclasses.replace(CORE, onsite_availability=availability)), SITE)
    assert np.allclose(balance.loc[outage, "curtailed"], 100.0, atol=TOL)
    assert np.allclose(balance.loc[outage, "unserved"], 200.0, atol=TOL)
    normal = balance.drop(index=outage)
    assert normal.curtailed.abs().max() < TOL
    assert normal.unserved.abs().max() < TOL


def test_hypothetical_site_without_generator_is_served_from_the_grid(baseline):
    spec = dataclasses.replace(CORE, onsite_capacity_mw=0.0, firm_mw=1000.0, flexible_share=0.0)
    n = solved(spec)
    balance = site_balance(n, SITE)
    assert np.allclose(balance.grid_import, 1000.0, atol=TOL)
    assert balance.unserved.abs().max() < TOL
    assert n.objective > baseline.objective


def test_constrained_transfer_gives_the_predicted_shortfall():
    # Zone C is islanded. It has 1600 MW of local capacity for its own load plus
    # the site. The site first uses its generator (400) and its flexibility (100),
    # so it needs at least 500 MW from the grid. Whatever is still missing must be
    # unserved, split in any way between zone C's load and the site.
    n = solved(CORE, transfer_scale={("A", "C"): 0.0, ("B", "C"): 0.0})
    zone_load = PEAK_LOAD["C"] * load_factor(len(n.snapshots))
    expected = np.clip(zone_load + 500.0 - 1600.0, 0.0, None)
    assert expected.max() > 0  # the case really is constrained
    balance = site_balance(n, SITE)
    unserved = n.generators_t.p["C unserved"] + balance.unserved
    assert np.allclose(unserved, expected, atol=TOL)
    assert n.generators_t.p[["A unserved", "B unserved"]].abs().max().max() < TOL
    short = expected > TOL
    assert np.allclose(balance.curtailed[short], 100.0, atol=TOL)  # flexibility is used before anyone is shed
    assert balance.residual.abs().max() < TOL


# --- A8: costs and emissions reconcile --------------------------------------------------


@pytest.mark.parametrize("expansion", [False, True])
def test_cost_parts_sum_to_objective(expansion):
    n = solved(dataclasses.replace(CORE, onsite_availability=0.0), expansion=expansion, load_scale=1.5)
    costs = cost_breakdown(n)
    assert (costs["investment"] > 0) == expansion  # the tight system builds only when allowed to
    assert costs.drop("total").sum() == pytest.approx(costs["total"])
    assert costs["total"] == pytest.approx(n.objective, rel=1e-6)


def test_emissions_reconcile(baseline, core):
    balance = site_balance(core, SITE)
    onsite_mwh = float((balance.onsite * core.snapshot_weightings["objective"]).sum())
    co2 = emissions(core)
    onsite_name = component_names(SITE)["onsite"]
    assert co2[onsite_name] == pytest.approx(onsite_mwh / 0.40 * 0.18)
    assert co2.sum() == pytest.approx(co2.drop(onsite_name).sum() + co2[onsite_name])
    assert co2.sum() > emissions(baseline).sum()
    assert summary(core, SITE)["site onsite tCO2"] == pytest.approx(co2[onsite_name])


# --- A9: with expansion allowed, firm load is met by building, not by shedding ----------


def test_firm_load_triggers_capacity_instead_of_unserved_energy():
    # Loads scaled by 1.5: the system alone is just adequate, the firm site is not.
    kwargs = {"expansion": True, "load_scale": 1.5}
    base = summary(solved(**kwargs))
    with_site = summary(solved(CORE, **kwargs), SITE)
    assert base["system unserved MWh"] < TOL
    assert with_site["system unserved MWh"] < TOL
    assert with_site["site unserved MWh"] < TOL
    assert with_site["new capacity MW"] > base["new capacity MW"] + 1.0
    assert with_site["investment"] > base["investment"]
    assert with_site["system cost"] > base["system cost"]


# --- input checks -----------------------------------------------------------------------


@pytest.mark.parametrize(
    "changes",
    [
        {"firm_mw": 1200.0},  # above the physical connection
        {"flexible_share": 1.5},
        {"onsite_efficiency": 0.0},
        {"curtailment_cost": VOLL},  # curtailment would never be chosen before shedding
        {"grid_bus": "Z"},
    ],
)
def test_invalid_inputs_are_rejected(changes):
    with pytest.raises(ValueError):
        add_site(build_toy_network(), dataclasses.replace(CORE, **changes))
