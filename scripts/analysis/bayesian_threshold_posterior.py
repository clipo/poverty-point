"""
Bayesian posterior over (sigma_eff, sigma_star) at Poverty Point.

Reproduces the §4.5 posterior-predictive check under two prior choices:
  (i)  Original manuscript prior: T ~ U[6,18], m ~ U[0.30, 0.60],
       five PP zone weights ~ U(rubric_value ± 0.20). This prior is
       informative on epsilon: it centers on the qualitative rubric's
       0.49 value with a +/- 0.10 (max) range in epsilon space.
  (ii) Flat-epsilon prior: T ~ U[6,18], m ~ U[0.30, 0.60],
       epsilon ~ U[0.10, 0.50]. This treats the GIS-vs-qualitative
       disagreement (Saucier-categorical 0.22; EPA-L4 0.33; rubric
       0.49; phenology 0.50) as expressing genuine uncertainty over
       the operative epsilon and uses a uniform prior over the
       plausible range.

Outputs to results/bayesian/threshold_posterior.json with key summary
statistics for both priors, plus the prior-sensitivity comparison.
"""
from pathlib import Path
import json
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from poverty_point.parameters import SimulationParameters, critical_threshold


N_SAMPLES = 1000  # Reduced from 5000; each prior takes ~3 minutes of fixed-point iteration
RNG_SEED = 42
N_AGG = 25

# Rubric weights for the five PP zones (Table 1, AA §4.5)
PP_RUBRIC = np.array([1.0, 1.0, 1.0, 1.0, 0.5])
H_MAX = np.log(5)  # max Shannon entropy with 5 zones


def shannon_eps(weights: np.ndarray) -> float:
    """Compute epsilon from zone weights (Shannon entropy, 0.5 scaling)."""
    w = np.maximum(weights, 0.0)
    if w.sum() <= 0:
        return 0.0
    p = w / w.sum()
    p = p[p > 0]
    H = float(-np.sum(p * np.log(p)))
    return (H / H_MAX) * 0.5


def sigma_from_T_m(T: float, m: float) -> float:
    """Hurricane+drought equivalent annualized sigma (manuscript §3.3)."""
    # Combined drought+hurricane reasoning: variability scales as m * sqrt(2)
    # at 20-year reference window (per AA §3.3 / Supplemental §S2).
    return m * np.sqrt(2.0)


def run_posterior(prior_label: str, rng: np.random.Generator,
                  n: int = N_SAMPLES, params=None,
                  n_agg: int = N_AGG):
    """Sample n times from the prior, push through model, return posterior."""
    if params is None:
        params = SimulationParameters()

    sigmas = np.empty(n)
    epsilons = np.empty(n)
    sigma_stars = np.empty(n)
    sigma_effs = np.empty(n)

    for i in range(n):
        T = rng.uniform(6.0, 18.0)
        m = rng.uniform(0.30, 0.60)
        sigma = sigma_from_T_m(T, m)

        if prior_label == "rubric":
            # Manuscript prior: zone weights from rubric +/- 0.20
            perturb = rng.uniform(-0.20, 0.20, size=5)
            w = np.clip(PP_RUBRIC + perturb, 0.0, None)
            eps = shannon_eps(w)
        elif prior_label == "flat":
            # Flat prior: epsilon ~ U[0.10, 0.50]
            eps = rng.uniform(0.10, 0.50)
        elif prior_label == "gis_mixture":
            # Mixture of GIS-derived estimates (Saucier-cat 0.22, L4 0.33,
            # rubric 0.49, phenology 0.50)
            estimates = np.array([0.22, 0.33, 0.49, 0.50])
            base = rng.choice(estimates)
            eps = float(np.clip(base + rng.uniform(-0.05, 0.05), 0.05, 0.55))
        else:
            raise ValueError(f"Unknown prior: {prior_label}")

        ss = critical_threshold(eps, n_agg, params)
        s_eff = sigma * (1.0 - eps)

        sigmas[i] = sigma
        epsilons[i] = eps
        sigma_stars[i] = ss
        sigma_effs[i] = s_eff

    p_above = float(np.mean(sigma_effs > sigma_stars))
    return {
        "prior": prior_label,
        "n_samples": n,
        "epsilon": {
            "mean": float(epsilons.mean()),
            "median": float(np.median(epsilons)),
            "ci95": [float(np.percentile(epsilons, 2.5)),
                     float(np.percentile(epsilons, 97.5))],
        },
        "sigma": {
            "mean": float(sigmas.mean()),
            "median": float(np.median(sigmas)),
            "ci95": [float(np.percentile(sigmas, 2.5)),
                     float(np.percentile(sigmas, 97.5))],
        },
        "sigma_eff": {
            "mean": float(sigma_effs.mean()),
            "median": float(np.median(sigma_effs)),
            "ci95": [float(np.percentile(sigma_effs, 2.5)),
                     float(np.percentile(sigma_effs, 97.5))],
        },
        "sigma_star": {
            "mean": float(sigma_stars.mean()),
            "median": float(np.median(sigma_stars)),
            "ci95": [float(np.percentile(sigma_stars, 2.5)),
                     float(np.percentile(sigma_stars, 97.5))],
        },
        "P_above_threshold": p_above,
    }


def main():
    params = SimulationParameters()

    rng_rubric = np.random.default_rng(RNG_SEED)
    rng_flat = np.random.default_rng(RNG_SEED + 1)
    rng_mixture = np.random.default_rng(RNG_SEED + 2)

    out = {
        "rubric": run_posterior("rubric", rng_rubric, params=params),
        "flat": run_posterior("flat", rng_flat, params=params),
        "gis_mixture": run_posterior("gis_mixture", rng_mixture, params=params),
        "n_agg": N_AGG,
        "rng_seed": RNG_SEED,
    }

    print(f'{"Prior":15s} {"eps_mean":>10s} {"eps_ci95":>20s} '
          f'{"P(s_eff>s*)":>14s}')
    print('-' * 70)
    for k in ["rubric", "flat", "gis_mixture"]:
        r = out[k]
        e = r["epsilon"]
        print(f'{k:15s} {e["mean"]:10.3f} '
              f'  [{e["ci95"][0]:.3f}, {e["ci95"][1]:.3f}]   '
              f'{r["P_above_threshold"]:14.3f}')
    print()
    print(f'Manuscript-reported P(s_eff > s*) ≈ 0.25 (rubric prior)')
    print(f'Sensitivity check: under flat eps prior, P shifts to '
          f'{out["flat"]["P_above_threshold"]:.3f}')
    print(f'Under GIS-mixture prior, P shifts to '
          f'{out["gis_mixture"]["P_above_threshold"]:.3f}')

    out_dir = Path('results/bayesian')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'threshold_posterior.json'
    with open(out_file, 'w') as f:
        json.dump(out, f, indent=2)
    print(f'\nWrote {out_file}')


if __name__ == '__main__':
    main()
