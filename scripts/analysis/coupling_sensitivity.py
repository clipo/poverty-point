"""Coupling-form sensitivity for the W_agg shortfall term.

Computes sigma* under three alternative couplings of vulnerability alpha(k_eff)
and effective shortfall severity sigma_eff:

    Multiplicative (default): factor = 1 - alpha * sigma_eff
    Additive:                 factor = 1 - alpha - sigma_eff
    Hazard composition:       factor = (1 - alpha) * (1 - sigma_eff)

Brent-method root finding on W_agg(sigma) - W_ind(sigma) over sigma in
[0.05, 1.5], at PP-scenario parameters (epsilon=0.35, n_agg=25, defaults
otherwise). Documents §S3.6 of the supplemental.

Result: only the multiplicative form returns a sigma* in the empirically
relevant range. The additive form has no root because alpha(k_eff) ~ 0.82
already exceeds 1 - sigma_eff for any positive sigma_eff. The hazard-
composition form returns sigma* ~ 0.875, far above plausible LMV sigma.
The reason is that alpha is a vulnerability *coefficient* on (0, 1] that
modulates the magnitude of a shortfall-induced loss; it is neither a
fractional loss in its own right (which the additive form requires) nor
an independent survival probability (which the hazard form requires).
"""
from __future__ import annotations

from pathlib import Path
import json

from scipy.optimize import brentq

from poverty_point.signaling_core import (
    AggregationParams,
    ConflictParams,
    NetworkParams,
    SignalingParams,
    conflict_reduction,
    expected_signaling_benefit,
    independent_expected_fitness,
    lambda_total_at_sigma,
    network_degree,
    seasonal_effective_degree,
    vulnerability_coefficient,
)


def W_agg_alt(
    sigma: float,
    epsilon: float,
    coupling: str,
    sig: SignalingParams,
    net: NetworkParams,
    conf: ConflictParams,
    agg: AggregationParams,
    M_g: float,
    lam: float,
    travel_distance: float = 100.0,
) -> float:
    C_travel = agg.C_travel_per_km * travel_distance
    C_total = C_travel + agg.C_opportunity + agg.C_signal
    sigma_eff = sigma * (1.0 - epsilon)
    k_agg = network_degree(M_g, net.k_0, net.k_max, net.M_half)
    k_eff = seasonal_effective_degree(k_agg, net.k_0, agg.delta_net, agg.f_agg)
    alpha_eff = vulnerability_coefficient(k_eff, net.gamma)
    r = conflict_reduction(M_g, M_g, conf)
    B_lam = expected_signaling_benefit(lam, sig.q_min, sig.q_max)

    if coupling == "multiplicative":
        survival = 1.0 - alpha_eff * sigma_eff
    elif coupling == "additive":
        survival = 1.0 - alpha_eff - sigma_eff
    elif coupling == "hazard":
        survival = (1.0 - alpha_eff) * (1.0 - sigma_eff)
    else:
        raise ValueError(f"unknown coupling: {coupling}")

    conflict_effect = 1.0 - conf.conflict_mortality * (1.0 - r) * conf.P_base
    reproduction = 1.0 - C_total
    return max(reproduction * survival * conflict_effect + B_lam, 0.0)


def fitness_diff(sigma: float, coupling: str, epsilon: float = 0.35, n_agg: int = 25) -> float:
    sig = SignalingParams()
    net = NetworkParams()
    conf = ConflictParams()
    agg = AggregationParams()
    eq = lambda_total_at_sigma(sigma, sig, net, conf, agg, n_agg)
    W_agg = W_agg_alt(sigma, epsilon, coupling, sig, net, conf, agg, eq["M_g"], eq["lambda_total"])
    W_ind = independent_expected_fitness(sigma, net, conf)
    return W_agg - W_ind


def find_sigma_star(coupling: str, epsilon: float = 0.35, n_agg: int = 25):
    f_lo = fitness_diff(0.05, coupling, epsilon, n_agg)
    f_hi = fitness_diff(1.5, coupling, epsilon, n_agg)
    if f_lo * f_hi > 0:
        return None
    return float(brentq(fitness_diff, 0.05, 1.5, args=(coupling, epsilon, n_agg)))


def main():
    results = {}
    for coupling in ("multiplicative", "additive", "hazard"):
        sigma_star = find_sigma_star(coupling)
        results[coupling] = sigma_star
        if sigma_star is None:
            print(f"  {coupling:18s} sigma* = no root in [0.05, 1.5]")
        else:
            print(f"  {coupling:18s} sigma* = {sigma_star:.4f}")

    out_dir = Path(__file__).resolve().parents[2] / "results" / "sensitivity"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "coupling_sensitivity.json"
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
