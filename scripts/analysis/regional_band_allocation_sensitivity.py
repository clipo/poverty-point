"""
Sensitivity sweep for the Extension #3 minimal band-allocation model.

Round-5 reviewers (Methods, Adversarial) flagged that the winner-takes-most
outcome (PP=43, Jaketown=7, others=0) emerges from two hand-set parameters
(NETWORK_BONUS = 0.05, N_AGG_THRESHOLD = 5). This script sweeps both
parameters and reports the resulting Spearman ρ vs observed monument scale,
to bound the parameter sensitivity.

Caches site_fitness lookups by (eps, n_agg) since these are deterministic
and the same lookups recur many times during iteration.

Output: results/sensitivity/regional_band_allocation_sensitivity.json
"""
from pathlib import Path
import json
import sys

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from poverty_point.parameters import SimulationParameters
from poverty_point.signaling_core import critical_threshold as full_ct


SITES = [
    ('Poverty Point',    -91.4074, 32.6366, 0.154, 3),
    ('Lower Jackson',    -91.4108, 32.6105, 0.145, 0),
    ('Watson Brake',     -92.1311, 32.3684, 0.115, 2),
    ("Frenchman's Bend", -92.0437, 32.6357, 0.115, 1),
    ('Caney',            -92.0004, 31.4822, 0.070, 2),
    ('Insley',           -91.4791, 32.3893, 0.083, 2),
    ('Cowpen Slough',    -91.9346, 31.3293, 0.068, 0),
    ('J.W. Copes',       -91.3894, 32.5339, 0.068, 0),
    ('Jaketown',         -90.4872, 33.2349, 0.151, 1),
    ('Claiborne',        -89.5758, 30.2141, 0.050, 1),
    ('Cedarland',        -89.5804, 30.2186, 0.050, 1),
]

KM_PER_DEGREE_LAT = 111.0
KM_PER_DEGREE_LON = 95.0
CANOE_KM_PER_DAY = 30.0
C_TRAVEL_PER_DAY = 0.005
N_BANDS = 50
RNG_SEED = 42
SIGMA_REGIONAL = 0.64

_FITNESS_CACHE = {}


def gc_km(lo1, la1, lo2, la2):
    dx = (lo1 - lo2) * KM_PER_DEGREE_LON
    dy = (la1 - la2) * KM_PER_DEGREE_LAT
    return float(np.sqrt(dx * dx + dy * dy))


def site_fitness_cached(eps: float, n_agg: int, sigma: float,
                        params: SimulationParameters) -> float:
    """Cached W_agg approximation."""
    key = (round(eps, 4), n_agg)
    if key in _FITNESS_CACHE:
        return _FITNESS_CACHE[key]
    if n_agg < 1:
        _FITNESS_CACHE[key] = 0.0
        return 0.0
    r = full_ct(epsilon=eps, n_agg=n_agg,
                sig_params=params.signaling, net_params=params.network,
                conf_params=params.conflict, agg_params=params.aggregation)
    sigma_star = r['sigma_star']
    val = 0.5 if sigma <= sigma_star else 0.5 + 0.5 * (sigma - sigma_star)
    _FITNESS_CACHE[key] = val
    return val


def run(network_bonus: float, n_agg_threshold: int,
        params: SimulationParameters, rng_seed: int = RNG_SEED):
    rng = np.random.default_rng(rng_seed)
    site_coords = [(s[1], s[2]) for s in SITES]
    site_eps = [s[3] for s in SITES]

    band_homes = []
    for _ in range(N_BANDS):
        if rng.random() < 0.8:
            ai = rng.integers(0, 9)
            anchor_lon, anchor_lat = site_coords[ai]
            band_homes.append((anchor_lon + rng.normal(0, 0.5),
                               anchor_lat + rng.normal(0, 0.5)))
        else:
            band_homes.append((rng.uniform(-93, -89),
                               rng.uniform(30, 33.5)))

    band_choice = [-1] * N_BANDS
    for round_idx in range(20):
        n_agg = [0] * len(SITES)
        for c in band_choice:
            if c >= 0:
                n_agg[c] += 1
        new_choices = list(band_choice)
        changed = 0
        for b in range(N_BANDS):
            blon, blat = band_homes[b]
            best, best_site = -1e9, -1
            for s_idx, (slon, slat) in enumerate(site_coords):
                eps = site_eps[s_idx]
                tn = n_agg[s_idx] + (1 if band_choice[b] != s_idx else 0)
                if tn < 1:
                    tn = 1
                fit = site_fitness_cached(eps, tn, SIGMA_REGIONAL, params)
                if tn >= n_agg_threshold:
                    fit += network_bonus
                d = gc_km(blon, blat, slon, slat) / CANOE_KM_PER_DAY
                score = fit - d * C_TRAVEL_PER_DAY
                if score > best:
                    best, best_site = score, s_idx
            if best_site != band_choice[b]:
                changed += 1
            new_choices[b] = best_site
        band_choice = new_choices
        if changed == 0:
            break

    final = [0] * len(SITES)
    for c in band_choice:
        if c >= 0:
            final[c] += 1
    return final


def main():
    params = SimulationParameters()

    print(f'{"NB":>6s} {"NT":>4s} {"PP":>4s} {"JT":>4s} {"WB":>4s} '
          f'{"FB":>4s} {"CN":>4s} {"IN":>4s} {"others_zero":>12s} '
          f'{"rho_scale":>10s}')
    print('-' * 80)

    sweep = []
    nb_values = [0.00, 0.025, 0.05, 0.10, 0.20]
    nt_values = [2, 3, 5, 8]
    for nb in nb_values:
        for nt in nt_values:
            final_n = run(nb, nt, params)
            scale = [s[4] for s in SITES]
            rho, p = spearmanr(final_n, scale)
            n_others_zero = sum(1 for x in final_n[2:] if x == 0)
            print(f'{nb:6.3f} {nt:4d} {final_n[0]:4d} {final_n[8]:4d} '
                  f'{final_n[2]:4d} {final_n[3]:4d} {final_n[4]:4d} '
                  f'{final_n[5]:4d} {n_others_zero:>5d}/9        '
                  f'{rho:+.3f}')
            sweep.append({
                'network_bonus': nb,
                'n_agg_threshold': nt,
                'PP_n': final_n[0],
                'Jaketown_n': final_n[8],
                'WB_n': final_n[2],
                'others_zero_count': int(n_others_zero),
                'spearman_rho_vs_scale': float(rho),
                'p_vs_scale': float(p),
                'final_n_agg_per_site': final_n,
            })

    rhos = [r['spearman_rho_vs_scale'] for r in sweep]
    print()
    print(f'Spearman ρ vs observed scale across {len(sweep)} (NB, NT) cells:')
    print(f'  min: {min(rhos):+.3f}')
    print(f'  max: {max(rhos):+.3f}')
    print(f'  median: {sorted(rhos)[len(rhos)//2]:+.3f}')

    out_dir = Path('results/sensitivity')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'regional_band_allocation_sensitivity.json'
    with open(out_file, 'w') as f:
        json.dump({
            'sweep': sweep,
            'summary': {
                'rho_min': float(min(rhos)),
                'rho_max': float(max(rhos)),
                'rho_median': float(sorted(rhos)[len(rhos)//2]),
                'n_cells': len(sweep),
            },
        }, f, indent=2)
    print(f'\nWrote {out_file}')


if __name__ == '__main__':
    main()
