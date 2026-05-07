#!/usr/bin/env python3
"""Tier 3 substantive analytical extensions for the AA / v2 manuscripts.

Addresses peer-review concerns by running:

1. n_agg sensitivity at Watson Brake parameters (Domain reviewer W7).
   Disentangles the demographic-uncertainty contribution from the
   regime-switching contribution to the 30x volume overprediction.

2. lambda_W sweep at Poverty Point and Watson Brake parameters
   (Methods reviewer W3, ablation robustness). Reports sigma_star
   ordering across the plausible range.

3. Stochastic regime-switching pilot at WB parameters (Methods W4).
   Simulates annual sigma fluctuations and computes fraction of time
   spent in the aggregator regime, plus an order-of-magnitude
   estimate of cumulative monument output.

Outputs a concise tabular report and a small JSON for manuscript
inclusion. No figures are produced here; figure regeneration with
new sites would require updating create_figure_15_site_hierarchy.py.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from poverty_point.signaling_core import (
    AggregationParams,
    ConflictParams,
    NetworkParams,
    SignalingParams,
    critical_threshold,
    fitness_advantage,
    lambda_total_at_sigma,
)


PP_PARAMS = dict(epsilon=0.49, n_agg=25, sigma_obs=0.64)
WB_PARAMS = dict(epsilon=0.43, n_agg=8, sigma_obs=0.56)
RNG = np.random.default_rng(20260429)


def run_n_agg_sweep_at_wb():
    """Tier 3 #13. n_agg sensitivity at Watson Brake parameters."""
    rows = []
    for n_agg in [3, 4, 5, 6, 8, 10, 15, 25]:
        ct = critical_threshold(epsilon=WB_PARAMS["epsilon"], n_agg=n_agg)
        eq = lambda_total_at_sigma(
            sigma=WB_PARAMS["sigma_obs"], n_bands=n_agg
        )
        fitness_diff = fitness_advantage(
            sigma=WB_PARAMS["sigma_obs"],
            epsilon=WB_PARAMS["epsilon"],
            n_agg=n_agg,
            travel_distance=100.0,
            sig_params=SignalingParams(),
            net_params=NetworkParams(),
            conf_params=ConflictParams(),
            agg_params=AggregationParams(),
        )
        rows.append(
            {
                "n_agg": n_agg,
                "sigma_star": float(ct["sigma_star"]),
                "margin": float(WB_PARAMS["sigma_obs"] - ct["sigma_star"]),
                "M_g_eq": float(eq["M_g"]),
                "fitness_diff": float(fitness_diff),
                "lambda_total": float(eq["lambda_total"]),
                "lambda_C": float(eq["lambda_C"]),
                "lambda_X": float(eq["lambda_X"]),
            }
        )
    return rows


def run_lambda_w_sweep(epsilon, n_agg, sigma_obs, label):
    """Tier 3 #15a. lambda_W sweep robustness check at given site params."""
    rows = []
    for lam_w in [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
        sig = SignalingParams(lambda_W=lam_w)
        ct = critical_threshold(
            epsilon=epsilon, n_agg=n_agg, sig_params=sig
        )
        eq = lambda_total_at_sigma(
            sigma=sigma_obs, sig_params=sig, n_bands=n_agg
        )
        fitness_diff = fitness_advantage(
            sigma=sigma_obs,
            epsilon=epsilon,
            n_agg=n_agg,
            travel_distance=100.0,
            sig_params=sig,
            net_params=NetworkParams(),
            conf_params=ConflictParams(),
            agg_params=AggregationParams(),
        )
        rows.append(
            {
                "site": label,
                "lambda_W": lam_w,
                "sigma_star": float(ct["sigma_star"]),
                "margin": float(sigma_obs - ct["sigma_star"]),
                "M_g_eq": float(eq["M_g"]),
                "fitness_diff": float(fitness_diff),
                "lambda_C_eq": float(eq["lambda_C"]),
                "lambda_X_eq": float(eq["lambda_X"]),
            }
        )
    return rows


def run_m_half_sensitivity(epsilon, n_agg, sigma_obs, label):
    """Tier 3 #15b. M_half sensitivity to test ablation under
    parameter regimes where lambda_C, lambda_X don't collapse."""
    rows = []
    for m_half in [10.0, 25.0, 50.0, 100.0, 200.0]:
        # Default and ablated cases
        for lam_w_label, lam_w in [("default", 0.15), ("ablated", 0.00)]:
            net = NetworkParams(M_half=m_half)
            sig = SignalingParams(lambda_W=lam_w)
            ct = critical_threshold(
                epsilon=epsilon, n_agg=n_agg, sig_params=sig, net_params=net
            )
            eq = lambda_total_at_sigma(
                sigma=sigma_obs, sig_params=sig, net_params=net, n_bands=n_agg
            )
            rows.append(
                {
                    "site": label,
                    "M_half": m_half,
                    "lambda_W": lam_w_label,
                    "sigma_star": float(ct["sigma_star"]),
                    "lambda_C_eq": float(eq["lambda_C"]),
                    "lambda_X_eq": float(eq["lambda_X"]),
                    "lambda_total_eq": float(eq["lambda_total"]),
                }
            )
    return rows


def run_stochastic_wb_pilot(n_replicates=500, n_years=700):
    """Tier 3 #14 pilot. Stochastic regime-switching at WB params.

    Simulates annual environmental fluctuations as Gaussian noise
    around mean sigma_obs, computes the fitness differential each
    year, and tracks fraction of years in the aggregator regime.
    Reports cumulative monument output assuming aggregator-years
    contribute at the equilibrium rate and independent-years
    contribute zero. Compares to PP for context.

    This is a pilot, not the full regime-switching ABM. It treats
    each year as independent and uses the equilibrium M_g as the
    per-year contribution while in the aggregator regime, with no
    band-level dynamics. Use for order-of-magnitude only.
    """

    def simulate(epsilon, n_agg, sigma_mean, sigma_sd, label):
        ct = critical_threshold(epsilon=epsilon, n_agg=n_agg)
        eq = lambda_total_at_sigma(sigma=sigma_mean, n_bands=n_agg)
        sigma_star = ct["sigma_star"]
        # Annual M_g flux while in aggregator regime: scale by
        # the fitness differential (proxy for aggregator share)
        per_year_per_band_units = float(eq["I_g"])

        cumulative_units = []
        agg_fractions = []
        for _ in range(n_replicates):
            sigmas = RNG.normal(sigma_mean, sigma_sd, size=n_years)
            sigmas = np.clip(sigmas, 0.0, 1.5)
            # Effective sigma at site (apply ecotone reduction)
            sigma_effs = sigmas * (1.0 - epsilon)
            in_aggregator = sigma_effs > sigma_star
            agg_fraction = float(in_aggregator.mean())
            cum_units = float(in_aggregator.sum() * per_year_per_band_units * n_agg)
            cumulative_units.append(cum_units)
            agg_fractions.append(agg_fraction)

        return {
            "site": label,
            "epsilon": epsilon,
            "n_agg": n_agg,
            "sigma_mean": sigma_mean,
            "sigma_sd": sigma_sd,
            "sigma_star": float(sigma_star),
            "per_year_per_band_units": per_year_per_band_units,
            "agg_fraction_mean": float(np.mean(agg_fractions)),
            "agg_fraction_p05": float(np.percentile(agg_fractions, 5)),
            "agg_fraction_p95": float(np.percentile(agg_fractions, 95)),
            "cum_units_mean": float(np.mean(cumulative_units)),
            "cum_units_p05": float(np.percentile(cumulative_units, 5)),
            "cum_units_p95": float(np.percentile(cumulative_units, 95)),
        }

    # Use sigma_sd derived from the §3.3 paleoclimate CI
    # (PP 95% CI 0.41-0.94 → sd ~ 0.13; same magnitude for WB)
    sigma_sd = 0.13
    results = {
        "WB_700yr": simulate(0.43, 8, 0.56, sigma_sd, "Watson Brake (700yr)"),
        "PP_75yr": simulate(0.49, 25, 0.64, sigma_sd, "Poverty Point (75yr)"),
    }
    # Run PP at 75 years for a fair comparison to its active window
    eq_pp = lambda_total_at_sigma(sigma=0.64, n_bands=25)
    ct_pp = critical_threshold(epsilon=0.49, n_agg=25)
    pp_per_year = float(eq_pp["I_g"]) * 25
    cum_75 = []
    agg_75 = []
    for _ in range(n_replicates):
        sigmas = RNG.normal(0.64, sigma_sd, size=75)
        sigmas = np.clip(sigmas, 0.0, 1.5)
        sigma_effs = sigmas * (1.0 - 0.49)
        in_agg = sigma_effs > ct_pp["sigma_star"]
        agg_75.append(float(in_agg.mean()))
        cum_75.append(float(in_agg.sum() * pp_per_year))
    results["PP_75yr_replicate"] = {
        "site": "Poverty Point (75yr active window)",
        "agg_fraction_mean": float(np.mean(agg_75)),
        "cum_units_mean": float(np.mean(cum_75)),
    }
    return results


def format_table(rows, columns, title):
    out = [title, "=" * len(title)]
    out.append(" | ".join(columns))
    out.append(" | ".join("-" * len(c) for c in columns))
    for row in rows:
        formatted = []
        for c in columns:
            v = row.get(c)
            if isinstance(v, float):
                formatted.append(f"{v:.4f}" if abs(v) < 100 else f"{v:.1f}")
            else:
                formatted.append(str(v))
        out.append(" | ".join(formatted))
    return "\n".join(out)


def main():
    out_dir = Path(__file__).resolve().parent.parent.parent / "results" / "tier3"
    out_dir.mkdir(parents=True, exist_ok=True)

    print("Running Tier 3 #13: n_agg sensitivity at Watson Brake...")
    n_agg_rows = run_n_agg_sweep_at_wb()
    print(format_table(
        n_agg_rows,
        ["n_agg", "sigma_star", "margin", "M_g_eq", "fitness_diff", "lambda_C", "lambda_X"],
        "n_agg sensitivity at WB (epsilon=0.43, sigma=0.56)",
    ))
    print()

    print("Running Tier 3 #15a: lambda_W sweep at PP and WB...")
    pp_lam = run_lambda_w_sweep(0.49, 25, 0.64, "PP")
    wb_lam = run_lambda_w_sweep(0.43, 8, 0.56, "WB")
    print(format_table(
        pp_lam,
        ["site", "lambda_W", "sigma_star", "margin", "M_g_eq", "fitness_diff"],
        "lambda_W sweep at PP",
    ))
    print()
    print(format_table(
        wb_lam,
        ["site", "lambda_W", "sigma_star", "margin", "M_g_eq", "fitness_diff"],
        "lambda_W sweep at WB",
    ))
    print()

    print("Running Tier 3 #15b: M_half sensitivity (ablation under regimes "
          "where lambda_C, lambda_X don't collapse)...")
    m_half_rows = run_m_half_sensitivity(0.49, 25, 0.64, "PP")
    print(format_table(
        m_half_rows,
        ["site", "M_half", "lambda_W", "sigma_star", "lambda_C_eq", "lambda_X_eq", "lambda_total_eq"],
        "M_half sensitivity at PP",
    ))
    print()

    print("Running Tier 3 #14 pilot: stochastic regime-switching at WB...")
    stoch = run_stochastic_wb_pilot(n_replicates=500, n_years=700)
    print(format_table(
        list(stoch.values()),
        ["site", "agg_fraction_mean", "cum_units_mean", "sigma_star"],
        "Stochastic regime-switching pilot (WB 700 years, PP 700 years, PP 75 years)",
    ))
    print()

    # Persist results as JSON for manuscript inclusion
    results = {
        "n_agg_sensitivity_wb": n_agg_rows,
        "lambda_w_sweep_pp": pp_lam,
        "lambda_w_sweep_wb": wb_lam,
        "m_half_sensitivity_pp": m_half_rows,
        "stochastic_wb_pilot": stoch,
    }
    with open(out_dir / "tier3_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {out_dir / 'tier3_results.json'}")


if __name__ == "__main__":
    main()
