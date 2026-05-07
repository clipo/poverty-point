"""
Extension 3 (minimal): Regional band-allocation model.

The Round-4 critique was that the joint magnitude prediction's
ρ = +0.91 is dominated by exogenous n_agg from the convergence-model
literature, so the framework was not predicting n_agg from first
principles. This minimal extension endogenizes n_agg per site by
simulating a regional pool of bands choosing among 11 candidate
aggregation sites based on:

  1. Site-local fitness W_agg at the equilibrium ε_water-route
     and a candidate n_agg.
  2. Travel cost from the band's home territory to the candidate site
     (canoe-day distance × C_travel_per_km).
  3. Path-dependence / network bonus: once a site has crossed a
     critical mass threshold (n_agg >= 5), additional bands joining
     get a small fitness bonus reflecting the cooperation-network
     channel (λ_X) that grows with attained network density.

Output: each band's chosen aggregation site, attained n_agg per site,
and Spearman correlation between the endogenized n_agg vector and
observed monument scale (the test the framework needs to make
n_agg endogenous rather than exogenous).

Output file: results/sensitivity/regional_band_allocation.json
"""
from pathlib import Path
import json
import sys
from dataclasses import replace

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from poverty_point.parameters import SimulationParameters
from poverty_point.signaling_core import critical_threshold as full_ct


# 11 candidate sites. (name, lon, lat, eps_water_route, observed_scale)
# Coords from data/sites/late_archaic_sites.csv.
SITES = [
    ('Poverty Point',    -91.4074, 32.6366, 0.154, 3),
    ('Lower Jackson',    -91.4108, 32.6105, 0.145, 0),
    ('Watson Brake',     -92.1311, 32.3684, 0.115, 2),
    ('Frenchman\'s Bend',-92.1100, 32.5530, 0.115, 1),
    ('Caney',            -92.0004, 31.4822, 0.070, 2),
    ('Insley',           -91.4791, 32.3893, 0.083, 2),
    ('Cowpen Slough',    -91.9346, 31.3293, 0.068, 0),
    ('J.W. Copes',       -91.3894, 32.5339, 0.068, 0),
    ('Jaketown',         -90.4872, 33.2349, 0.151, 1),
    ('Claiborne',        -89.5758, 30.2141, 0.050, 1),
    ('Cedarland',        -89.5804, 30.2186, 0.050, 1),
]

# Regional band pool: 50 bands distributed across the LMV interior +
# coastal zone, with home territories sampled from the bounding box of
# the sites. The number 50 is chosen so that maximum n_agg per site
# is bounded above (the model's optimum is ~25 per the §3.4 framework).
N_BANDS = 50
RNG_SEED = 42

# Travel parameters: canoe ~30 km/day along navigable channels.
# Distances are computed great-circle and then divided by 30 km/day to
# get canoe-days; great-circle is an underestimate of actual canoe
# distance (no hydrographic routing), so this is a generous travel-cost
# scenario for distant sites.
KM_PER_DEGREE_LAT = 111.0
KM_PER_DEGREE_LON = 95.0  # at LMV latitude ~32 degrees
CANOE_KM_PER_DAY = 30.0
C_TRAVEL_PER_DAY = 0.005  # fitness penalty per canoe-day; calibrated so
# a 5-day travel costs ~2.5% of W_agg (less than C_signal at 18%)

# Critical-mass network bonus: once n_agg(site) >= 5, additional bands
# joining get a small per-band bonus of NETWORK_BONUS reflecting that
# joining a high-density cooperation network has higher value than
# joining a small network.
NETWORK_BONUS = 0.05
N_AGG_THRESHOLD = 5


def great_circle_km(lon1, lat1, lon2, lat2):
    """Approximate great-circle distance using flat-earth approximation."""
    dx = (lon1 - lon2) * KM_PER_DEGREE_LON
    dy = (lat1 - lat2) * KM_PER_DEGREE_LAT
    return float(np.sqrt(dx * dx + dy * dy))


def site_fitness(eps: float, n_agg: int, sigma: float,
                 params: SimulationParameters) -> float:
    """Approximate W_agg at a candidate site."""
    if n_agg < 1:
        return 0.0
    r = full_ct(epsilon=eps, n_agg=n_agg,
                sig_params=params.signaling, net_params=params.network,
                conf_params=params.conflict, agg_params=params.aggregation)
    sigma_star = r['sigma_star']
    if sigma <= sigma_star:
        # Below threshold: aggregation is not adaptive; W_agg < W_ind
        # We return a small positive fitness to allow bands to still aggregate
        # at sub-optimal sites if travel cost to better sites is too high.
        return 0.5
    # Above threshold: fitness benefit roughly proportional to (sigma - sigma_star)
    margin = sigma - sigma_star
    return float(0.5 + 0.5 * margin)


def main():
    rng = np.random.default_rng(RNG_SEED)
    params = SimulationParameters()
    sigma_regional = 0.64  # Late Archaic LMV regional sigma

    site_names = [s[0] for s in SITES]
    site_coords = [(s[1], s[2]) for s in SITES]
    site_eps = [s[3] for s in SITES]

    # Sample band home territories: 50 bands, distributed so most are
    # in the LMV interior near monument-building sites, with some
    # bands in the deltaic / coastal zones.
    lon_min, lon_max = -93.0, -89.0
    lat_min, lat_max = 30.0, 33.5
    band_homes = []
    for _ in range(N_BANDS):
        # 80% sampled near interior monument sites (anchored on PP),
        # 20% sampled across the bounding box.
        if rng.random() < 0.8:
            anchor_idx = rng.integers(0, 9)  # interior sites only
            anchor_lon, anchor_lat = site_coords[anchor_idx]
            jitter_lon = rng.normal(0, 0.5)
            jitter_lat = rng.normal(0, 0.5)
            band_homes.append((anchor_lon + jitter_lon, anchor_lat + jitter_lat))
        else:
            band_homes.append((rng.uniform(lon_min, lon_max),
                               rng.uniform(lat_min, lat_max)))

    # Iterative band allocation:
    # Initialize all sites at n_agg = 0; iterate band-choice rounds until
    # convergence. Each round, each band chooses the site that maximizes
    # (W_agg(site) - travel_cost), with the network bonus applied if
    # n_agg(site) >= threshold.
    band_choice = [-1] * N_BANDS  # -1 means not yet allocated
    max_rounds = 20

    for round_idx in range(max_rounds):
        # Tally current n_agg per site
        n_agg = [0] * len(SITES)
        for c in band_choice:
            if c >= 0:
                n_agg[c] += 1

        new_choices = list(band_choice)
        changed = 0
        for b in range(N_BANDS):
            band_lon, band_lat = band_homes[b]
            best_score = -float('inf')
            best_site = -1
            for s_idx, (s_lon, s_lat) in enumerate(site_coords):
                eps = site_eps[s_idx]
                # Tentative n_agg if this band joins (or stays at) site
                tentative_n = n_agg[s_idx]
                if band_choice[b] != s_idx:
                    tentative_n += 1
                if tentative_n < 1:
                    tentative_n = 1
                fitness = site_fitness(eps, tentative_n, sigma_regional, params)
                # Network bonus
                if tentative_n >= N_AGG_THRESHOLD:
                    fitness += NETWORK_BONUS
                # Travel cost
                dist_km = great_circle_km(band_lon, band_lat, s_lon, s_lat)
                canoe_days = dist_km / CANOE_KM_PER_DAY
                travel_penalty = canoe_days * C_TRAVEL_PER_DAY
                score = fitness - travel_penalty
                if score > best_score:
                    best_score = score
                    best_site = s_idx
            if best_site != band_choice[b]:
                changed += 1
            new_choices[b] = best_site
        band_choice = new_choices
        if changed == 0:
            break

    # Final n_agg per site
    final_n_agg = [0] * len(SITES)
    for c in band_choice:
        if c >= 0:
            final_n_agg[c] += 1

    # Compare endogenized n_agg with observed monument scale ordinal
    observed_scale = [s[4] for s in SITES]
    rho_endog, p_endog = spearmanr(final_n_agg, observed_scale)

    # Compare endogenized n_agg with the literature-based n_agg used in §S7.7
    LITERATURE_N_AGG = {
        'Poverty Point': 25, 'Lower Jackson': 1, 'Watson Brake': 8,
        "Frenchman's Bend": 5, 'Caney': 5, 'Insley': 6,
        'Cowpen Slough': 3, 'J.W. Copes': 3, 'Jaketown': 8,
        'Claiborne': 4, 'Cedarland': 4,
    }
    lit_n_agg = [LITERATURE_N_AGG[s[0]] for s in SITES]
    rho_endog_vs_lit, p_endog_vs_lit = spearmanr(final_n_agg, lit_n_agg)

    print(f'{"Site":22s} {"endog_n":>8s} {"lit_n":>6s} {"obs_scale":>10s} '
          f'{"eps_wr":>7s}')
    print('-' * 60)
    for i, (name, _, _, eps, scale) in enumerate(SITES):
        print(f'{name:22s} {final_n_agg[i]:8d} {LITERATURE_N_AGG[name]:6d} '
              f'{scale:10d} {eps:7.3f}')

    print()
    print(f'Spearman rank correlations:')
    print(f'  Endogenized n_agg vs observed monument scale: '
          f'rho = {rho_endog:+.3f}, p = {p_endog:.3f}')
    print(f'  Endogenized n_agg vs literature n_agg:        '
          f'rho = {rho_endog_vs_lit:+.3f}, p = {p_endog_vs_lit:.3f}')
    print()
    print(f'Total bands allocated: {sum(final_n_agg)} / {N_BANDS}')
    print(f'Convergence: round {round_idx + 1}')

    rows = []
    for i, name in enumerate(site_names):
        rows.append({
            'site': name,
            'eps_water_route': site_eps[i],
            'endogenized_n_agg': int(final_n_agg[i]),
            'literature_n_agg': LITERATURE_N_AGG[name],
            'observed_scale_ordinal': observed_scale[i],
        })

    out_dir = Path('results/sensitivity')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'regional_band_allocation.json'
    with open(out_file, 'w') as f:
        json.dump({
            'parameters': {
                'N_BANDS': N_BANDS, 'RNG_SEED': RNG_SEED,
                'CANOE_KM_PER_DAY': CANOE_KM_PER_DAY,
                'C_TRAVEL_PER_DAY': C_TRAVEL_PER_DAY,
                'NETWORK_BONUS': NETWORK_BONUS,
                'N_AGG_THRESHOLD': N_AGG_THRESHOLD,
                'sigma_regional': sigma_regional,
            },
            'sites': rows,
            'spearman': {
                'endog_vs_observed_scale': {'rho': float(rho_endog),
                                            'p': float(p_endog)},
                'endog_vs_literature_nagg': {'rho': float(rho_endog_vs_lit),
                                             'p': float(p_endog_vs_lit)},
            },
            'convergence_rounds': int(round_idx + 1),
        }, f, indent=2)
    print(f'\nWrote {out_file}')


if __name__ == '__main__':
    main()
