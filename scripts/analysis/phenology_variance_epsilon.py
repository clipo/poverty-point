"""
Variance-based phenology epsilon: a more defensible operationalization.

The framework's epsilon encodes shortfall buffering through *negative
covariance* between local zone productivity and the regional shortfall
driver. The §S7.6 Test A used static peak count, which is the wrong
quantity. This script computes the variance-based alternative:
year-to-year variance in *accessible peaks* under stochastic shortfall
across the five LMV resource categories. Sites whose accessible peaks
co-vary strongly under shortfall have low effective epsilon; sites
whose accessible peaks are independent under shortfall (so when one
zone is in shortfall, the others usually are not) have high effective
epsilon. This is the operational quantity the framework's logic
demands.

Approach:
  1. For each site, compute the access-flag vector (HM, SFS, SA, FWA, WF)
     from §S7.6 (full = 1.0, partial = 0.5).
  2. Simulate 1,000 years of stochastic shortfall draws for each of the
     five resource categories. Each category's annual realization is
     a productivity multiplier in [0, 1] drawn from a Beta(2, 2)
     distribution centered on its access flag, with covariance structure
     among categories driven by a shared regional shortfall driver
     (correlation rho ~ 0.3, matching the LMV gauge analysis in §S7.5b).
  3. Compute year-to-year variance in TOTAL accessible productivity,
     averaged across the five categories with each site's weights.
  4. The variance-based epsilon = 0.5 * (1 - var_observed / var_independent),
     where var_independent is the variance under fully independent
     categories (theoretical maximum). This rewards sites where
     covariance ACROSS categories reduces total productivity variance.

Output: results/phenology/phenology_variance_epsilon.json
"""
from pathlib import Path
import json
import sys

import numpy as np
from scipy.stats import spearmanr


N_YEARS = 1000
RNG_SEED = 42

# Site access flags (from §S7.6 phenology figure)
# (name, [HM, SFS, SA, FWA, WF], n_agg, observed_scale_ordinal)
SITES = [
    ('Poverty Point',    [1.0, 1.0, 1.0, 1.0, 1.0], 25, 3),
    ('Lower Jackson',    [1.0, 0.5, 0.5, 0.5, 1.0],  1, 0),
    ('Watson Brake',     [1.0, 0.5, 0.5, 0.5, 0.5],  8, 2),
    ("Frenchman's Bend", [1.0, 0.5, 0.5, 0.0, 0.5],  5, 1),
    ('Caney',            [1.0, 0.0, 0.5, 0.0, 0.5],  5, 2),
    ('Insley',           [1.0, 0.5, 0.5, 0.0, 0.5],  6, 2),
    ('Cowpen Slough',    [0.5, 1.0, 1.0, 0.5, 0.5],  3, 0),
    ('J.W. Copes',       [0.5, 1.0, 1.0, 0.5, 0.5],  3, 0),
    ('Jaketown',         [1.0, 1.0, 0.5, 0.5, 1.0],  8, 1),
    ('Claiborne',        [0.0, 0.5, 0.5, 0.0, 1.0],  4, 1),
    ('Cedarland',        [0.0, 0.5, 0.5, 0.0, 1.0],  4, 1),
]


def build_correlated_shortfall(n_years: int, n_categories: int,
                               regional_rho: float,
                               rng: np.random.Generator) -> np.ndarray:
    """Generate a (n_years, n_categories) array of productivity multipliers
    in [0, 1] with category-pair correlations ~= regional_rho through a
    shared regional shortfall driver."""
    # Underlying regional driver
    regional = rng.normal(0.0, 1.0, n_years)
    # Each category gets its own independent component plus a regional weight
    weight_regional = np.sqrt(regional_rho)
    weight_local = np.sqrt(1.0 - regional_rho)
    out = np.empty((n_years, n_categories))
    for c in range(n_categories):
        local = rng.normal(0.0, 1.0, n_years)
        z = weight_regional * regional + weight_local * local
        # Map standard normal to [0, 1] productivity using normal CDF
        out[:, c] = _normal_cdf(z)
    return out


def _normal_cdf(z):
    return 0.5 * (1.0 + np.tanh(z * 0.79788))  # quick logistic approx of Phi


def site_total_productivity(access_flags: list, productivity: np.ndarray) -> np.ndarray:
    """Total accessible productivity across categories, weighted by flags."""
    flags = np.asarray(access_flags)
    weighted = productivity * flags  # (n_years, n_cat) elementwise
    return weighted.sum(axis=1)


def compute_variance_epsilon(access_flags: list, regional_rho: float,
                             n_years: int = N_YEARS,
                             rng_seed: int = RNG_SEED) -> dict:
    rng = np.random.default_rng(rng_seed)
    productivity = build_correlated_shortfall(n_years, len(access_flags),
                                              regional_rho, rng)
    total_prod = site_total_productivity(access_flags, productivity)
    mean_obs = float(np.mean(total_prod))
    sd_obs = float(np.std(total_prod, ddof=1))
    cv_obs = sd_obs / mean_obs if mean_obs > 0 else float('inf')
    snr = mean_obs / sd_obs if sd_obs > 0 else float('inf')

    # Reference: a single-zone site with the smallest flag (worst case)
    # has CV ~= sd_one_zone / mean_one_zone where one_zone has all
    # productivity coming from a single category. We use a single-zone
    # baseline (flags = [1.0, 0, 0, 0, 0]) for normalization.
    rng2 = np.random.default_rng(rng_seed + 1)
    prod_ref = build_correlated_shortfall(n_years, len(access_flags),
                                          regional_rho, rng2)
    one_zone_flags = [1.0] + [0.0] * (len(access_flags) - 1)
    ref_total = site_total_productivity(one_zone_flags, prod_ref)
    cv_ref = float(np.std(ref_total, ddof=1) / np.mean(ref_total))

    # Variance-based epsilon: how much CV reduction does this site
    # achieve relative to a single-zone baseline?
    # Higher = better buffering through diversification.
    cv_reduction = (cv_ref - cv_obs) / cv_ref if cv_ref > 0 else 0.0
    eps_var = 0.5 * max(0.0, min(1.0, cv_reduction))

    return {
        'mean_total_productivity': mean_obs,
        'sd_total_productivity': sd_obs,
        'cv_observed': cv_obs,
        'cv_single_zone_baseline': cv_ref,
        'cv_reduction_vs_baseline': cv_reduction,
        'eps_var': float(eps_var),
        'snr': snr,
    }


def main():
    rng = np.random.default_rng(RNG_SEED)
    rho_regional = 0.30  # matches §S7.5b mean off-diagonal Pearson

    rows = []
    print(f'{"Site":22s} {"flags_sum":>10s} {"eps_var":>8s} {"cv_obs":>8s} '
          f'{"snr":>8s} {"mean_prod":>10s} {"n_agg":>6s} {"scale":>6s}')
    print('-' * 88)
    for name, flags, n_agg, scale in SITES:
        result = compute_variance_epsilon(flags, rho_regional)
        rows.append({
            'name': name,
            'access_flags': flags,
            'flag_sum': float(sum(flags)),
            'n_agg': n_agg,
            'observed_scale': scale,
            **result,
        })
        print(f'{name:22s} {sum(flags):10.2f} {result["eps_var"]:8.3f} '
              f'{result["cv_observed"]:8.3f} '
              f'{result["snr"]:8.3f} '
              f'{result["mean_total_productivity"]:10.2f} '
              f'{n_agg:6d} {scale:6d}')

    # Spearman: variance-based eps vs observed monument scale ordinal
    eps_vars = [r['eps_var'] for r in rows]
    flag_sums = [r['flag_sum'] for r in rows]
    scales = [r['observed_scale'] for r in rows]

    rho_var, p_var = spearmanr(eps_vars, scales)
    rho_static, p_static = spearmanr(flag_sums, scales)

    print()
    print('Spearman correlations against observed ordinal monument scale:')
    print(f'  Variance-based phenology eps: rho = {rho_var:+.3f}, p = {p_var:.3f}')
    print(f'  Static phenology flag sum:    rho = {rho_static:+.3f}, p = {p_static:.3f}')
    print()
    print('NOTE: per §5.1 consolidated statement, monument scale is set by')
    print('  attained n_agg and is not what eps alone is supposed to predict.')
    print('  These tests are screening tests, not magnitude predictions.')

    out_dir = Path('results/phenology')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'phenology_variance_epsilon.json'
    with open(out_file, 'w') as f:
        json.dump({
            'sites': rows,
            'regional_rho': rho_regional,
            'spearman': {
                'eps_var_vs_scale': {'rho': float(rho_var), 'p': float(p_var)},
                'flag_sum_vs_scale': {'rho': float(rho_static), 'p': float(p_static)},
            },
            'n_years': N_YEARS,
            'rng_seed': RNG_SEED,
        }, f, indent=2)
    print(f'\nWrote {out_file}')


if __name__ == '__main__':
    main()
