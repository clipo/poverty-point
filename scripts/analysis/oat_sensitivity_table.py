"""
One-at-a-time (OAT) sensitivity table for the analytical critical threshold.

Computes delta_sigma_star for each model parameter under +/- perturbation
relative to the PP-calibration baseline. Output is a numerical table for
Supplement Section S3.1 (replacing the image-only tornado plot).
"""
from pathlib import Path
import json
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from dataclasses import replace

from poverty_point.parameters import SimulationParameters, critical_threshold

EPS_PP = 0.35
N_AGG = 25


def baseline_sigma_star() -> float:
    return float(critical_threshold(EPS_PP, N_AGG, SimulationParameters()))


def perturb_param(param_group: str, leaf_attr: str, factor: float) -> float:
    """Apply a multiplicative factor to a nested-dataclass parameter using replace()."""
    p = SimulationParameters()
    sub = getattr(p, param_group)
    base_value = getattr(sub, leaf_attr)
    new_sub = replace(sub, **{leaf_attr: base_value * factor})
    new_p = replace(p, **{param_group: new_sub})
    return float(critical_threshold(EPS_PP, N_AGG, new_p))


def perturb_eps(eps_value: float) -> float:
    return float(critical_threshold(eps_value, N_AGG,
                                    SimulationParameters()))


def perturb_n(n_value: int) -> float:
    return float(critical_threshold(EPS_PP, n_value,
                                    SimulationParameters()))


def main():
    base = baseline_sigma_star()
    print(f'Baseline sigma* (eps=0.35, n_agg=25) = {base:.4f}')
    print()

    # Format: name, low_value_descriptor, low_sigma_star, high_value_descriptor, high_sigma_star
    rows = []

    # Parameters with multiplicative perturbations (-50% / +50%)
    mult_params = [
        ("C_signal (signaling cost)", ("aggregation", "C_signal")),
        ("C_opportunity (opportunity cost)", ("aggregation", "C_opportunity")),
        ("C_travel_per_km (travel cost)", ("aggregation", "C_travel_per_km")),
        ("lambda_W (within-group reward)", ("signaling", "lambda_W")),
        ("lambda_C (cooperation reward)", ("signaling", "lambda_C")),
        ("lambda_X (exotic reward)", ("signaling", "lambda_X")),
        ("delta (monument depreciation)", ("signaling", "delta")),
        ("gamma (network buffering)", ("network", "gamma")),
        ("k_max (max network degree)", ("network", "k_max")),
        ("M_half (network saturation)", ("network", "M_half")),
        ("k_0 (baseline degree)", ("network", "k_0")),
        ("f_agg (aggregation fraction)", ("aggregation", "f_agg")),
        ("delta_net (network decay)", ("aggregation", "delta_net")),
    ]
    for name, path in mult_params:
        try:
            ss_low = perturb_param(*path, 0.5)
            ss_high = perturb_param(*path, 1.5)
            rows.append({
                "param": name,
                "low_label": "-50%",
                "low_sigma_star": ss_low,
                "high_label": "+50%",
                "high_sigma_star": ss_high,
                "delta_low": ss_low - base,
                "delta_high": ss_high - base,
                "swing": abs(ss_high - ss_low),
            })
        except Exception as exc:
            rows.append({
                "param": name,
                "error": str(exc),
            })

    # Epsilon: 0.0, 0.25, 0.5
    rows.append({
        "param": "epsilon (ecotone advantage)",
        "low_label": "0.10",
        "low_sigma_star": perturb_eps(0.10),
        "high_label": "0.50",
        "high_sigma_star": perturb_eps(0.50),
        "delta_low": perturb_eps(0.10) - base,
        "delta_high": perturb_eps(0.50) - base,
        "swing": abs(perturb_eps(0.50) - perturb_eps(0.10)),
    })

    # n_agg: 5, 50
    rows.append({
        "param": "n_agg (aggregation size)",
        "low_label": "n=5",
        "low_sigma_star": perturb_n(5),
        "high_label": "n=50",
        "high_sigma_star": perturb_n(50),
        "delta_low": perturb_n(5) - base,
        "delta_high": perturb_n(50) - base,
        "swing": abs(perturb_n(50) - perturb_n(5)),
    })

    # Sort by swing descending
    rows.sort(key=lambda r: -r.get("swing", 0))

    print(f'{"Parameter":40s} {"low->s*":>12s} {"high->s*":>12s} '
          f'{"d_low":>8s} {"d_high":>8s} {"swing":>8s}')
    print('-' * 96)
    for r in rows:
        if "error" in r:
            print(f'  {r["param"]:38s} ERROR: {r["error"]}')
            continue
        print(f'{r["param"]:40s} '
              f'{r["low_label"]:>3s} {r["low_sigma_star"]:8.4f} '
              f'{r["high_label"]:>3s} {r["high_sigma_star"]:8.4f} '
              f'{r["delta_low"]:+8.4f} {r["delta_high"]:+8.4f} '
              f'{r["swing"]:8.4f}')

    out_dir = Path('results/sensitivity')
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / 'oat_sigma_star.json', 'w') as f:
        json.dump({
            "baseline_sigma_star": base,
            "epsilon_baseline": EPS_PP,
            "n_agg_baseline": N_AGG,
            "rows": rows,
        }, f, indent=2)
    print(f'\nWrote {out_dir / "oat_sigma_star.json"}')


if __name__ == '__main__':
    main()
