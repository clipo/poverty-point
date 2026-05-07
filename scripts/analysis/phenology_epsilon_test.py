"""
Test A: Phenology-derived epsilon vs. observed monument scale.

Apples-to-apples replacement for the §4.5 cross-site rank correlation
between static Shannon-derived epsilon and observed ordinal monument
investment (baseline rho ~0.36).

Procedure:
  1. Read 11 LMV sites with their static epsilon, observed ordinal
     scale, and the phenology peak count from
     scripts/figure_generation/create_fig_seasonal_phenology.py.
  2. Rescale phenology peak count (1..5) to epsilon in [0.10, 0.50],
     matching the framework's tested epsilon range.
  3. Compute sigma_star per site under both operationalizations.
  4. Spearman rank-correlate epsilon against ordinal scale and
     sigma - sigma* margin against ordinal scale, under each
     operationalization.

Output: results/phenology/phenology_epsilon_test.json
"""
from pathlib import Path
import json

import numpy as np
from scipy.stats import spearmanr

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))

from poverty_point.parameters import SimulationParameters, critical_threshold


# Sites: name, static_epsilon (Table 1 col 5), phenology_peak_count,
# observed_monument_scale_ordinal (0=minimal, 1=small, 2=mid, 3=very_large)
SITES = [
    ('Poverty Point',     0.49, 5, 3),  # very large
    ('Lower Jackson',     0.48, 2, 0),  # minimal (single mound, ~5500 cal BP)
    ('Watson Brake',      0.43, 1, 2),  # mid (~7k m^3, episodic)
    ('Caney',             0.43, 1, 2),  # mid
    ("Frenchman's Bend",  0.43, 1, 1),  # small
    ('Insley',            0.43, 1, 2),  # mid (2x WB scale)
    ('J.W. Copes',        0.42, 2, 0),  # minimal
    ('Cowpen Slough',     0.42, 2, 0),  # minimal
    ('Jaketown',          0.40, 3, 1),  # small
    ('Claiborne',         0.30, 1, 1),  # shell ring (treat as small)
    ('Cedarland',         0.30, 1, 1),  # small coastal
]

# Late Archaic (PP-period) regional sigma; Middle Archaic sigma is
# slightly lower (~0.56) but we use a single sigma to match the
# §4.5 baseline test, which compared all 11 sites against PP-period
# sigma. A time-stratified version is a separate refinement.
SIGMA_REGIONAL = 0.64

# Rescale phenology peak count k in [1, 5] to epsilon in [eps_min, eps_max]
EPS_MIN = 0.10
EPS_MAX = 0.50
PEAK_MAX = 5


def phen_epsilon(peak_count: int) -> float:
    return EPS_MIN + (peak_count / PEAK_MAX) * (EPS_MAX - EPS_MIN)


def main():
    params = SimulationParameters()
    n_agg = 25  # framework default; matches §3.4 and §4.5 baseline

    rows = []
    for name, eps_static, peaks, scale in SITES:
        eps_phen = phen_epsilon(peaks)
        sigma_star_static = critical_threshold(eps_static, n_agg, params)
        sigma_star_phen = critical_threshold(eps_phen, n_agg, params)
        margin_static = SIGMA_REGIONAL - sigma_star_static
        margin_phen = SIGMA_REGIONAL - sigma_star_phen
        rows.append({
            'name': name,
            'eps_static': eps_static,
            'eps_phen': eps_phen,
            'peak_count': peaks,
            'monument_scale': scale,
            'sigma_star_static': sigma_star_static,
            'sigma_star_phen': sigma_star_phen,
            'margin_static': margin_static,
            'margin_phen': margin_phen,
        })

    print(f'{"Site":22s} {"eps_st":>7s} {"eps_ph":>7s} {"peaks":>5s} '
          f'{"scale":>5s} {"s*_st":>7s} {"s*_ph":>7s} {"mg_st":>7s} {"mg_ph":>7s}')
    print('-' * 90)
    for r in rows:
        print(f'{r["name"]:22s} {r["eps_static"]:7.3f} {r["eps_phen"]:7.3f} '
              f'{r["peak_count"]:5d} {r["monument_scale"]:5d} '
              f'{r["sigma_star_static"]:7.3f} {r["sigma_star_phen"]:7.3f} '
              f'{r["margin_static"]:7.3f} {r["margin_phen"]:7.3f}')

    scale = [r['monument_scale'] for r in rows]
    eps_static = [r['eps_static'] for r in rows]
    eps_phen = [r['eps_phen'] for r in rows]
    margin_static = [r['margin_static'] for r in rows]
    margin_phen = [r['margin_phen'] for r in rows]

    rho_eps_static, p_eps_static = spearmanr(eps_static, scale)
    rho_eps_phen, p_eps_phen = spearmanr(eps_phen, scale)
    rho_margin_static, p_margin_static = spearmanr(margin_static, scale)
    rho_margin_phen, p_margin_phen = spearmanr(margin_phen, scale)
    rho_peaks, p_peaks = spearmanr([r['peak_count'] for r in rows], scale)

    print()
    print('Spearman rank correlations against observed ordinal monument scale:')
    print(f'  Static epsilon (Table 1 col 5):        rho = {rho_eps_static:+.3f}, p = {p_eps_static:.3f}')
    print(f'  Phenology epsilon (rescaled peaks):    rho = {rho_eps_phen:+.3f}, p = {p_eps_phen:.3f}')
    print(f'  Static sigma - sigma* margin:          rho = {rho_margin_static:+.3f}, p = {p_margin_static:.3f}')
    print(f'  Phenology sigma - sigma* margin:       rho = {rho_margin_phen:+.3f}, p = {p_margin_phen:.3f}')
    print(f'  Phenology peak count (raw):            rho = {rho_peaks:+.3f}, p = {p_peaks:.3f}')

    out_dir = Path('results/phenology')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'phenology_epsilon_test.json'
    with open(out_file, 'w') as f:
        json.dump({
            'sites': rows,
            'sigma_regional': SIGMA_REGIONAL,
            'n_agg': n_agg,
            'eps_rescaling': {
                'eps_min': EPS_MIN, 'eps_max': EPS_MAX,
                'peak_max': PEAK_MAX,
            },
            'spearman': {
                'eps_static_vs_scale': {'rho': float(rho_eps_static),
                                        'p': float(p_eps_static), 'n': len(rows)},
                'eps_phen_vs_scale': {'rho': float(rho_eps_phen),
                                      'p': float(p_eps_phen), 'n': len(rows)},
                'margin_static_vs_scale': {'rho': float(rho_margin_static),
                                           'p': float(p_margin_static), 'n': len(rows)},
                'margin_phen_vs_scale': {'rho': float(rho_margin_phen),
                                         'p': float(p_margin_phen), 'n': len(rows)},
                'peaks_vs_scale': {'rho': float(rho_peaks),
                                   'p': float(p_peaks), 'n': len(rows)},
            },
        }, f, indent=2)
    print(f'\nWrote {out_file}')


if __name__ == '__main__':
    main()
