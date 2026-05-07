"""
Extension 6: Water-route-aware travel-time catchment for epsilon.

The framework's epsilon is the local fraction of regional shortfall risk
buffered by negative covariance with accessible drainages. The static
Shannon-diversity proxy used in §4.5 measures raw zone count within a
25 km terrestrial buffer derived from Kelly's (2013) walking day-trip
radius. This is the wrong catchment for an aggregation site mobilizing
watercraft. Day to multi-day canoe travel along navigable bayous,
rivers, and channels extends the practical aggregation-period catchment
far beyond 25 km along waterways.

This script implements the priority extension #6 by:
  1. Computing canoe-day catchments for each LMV site (canoe speed
     ~30 km/day along navigable waterways vs Kelly's 5 km/day on foot).
  2. Identifying which independent shortfall regimes (per §S7.5b USGS
     gauge analysis: Mississippi mainstem, Yazoo Basin, Macon Ridge =
     Bayou Maçon + Tensas) are accessible from each site.
  3. Computing covariance-based epsilon as the variance reduction in
     total accessible productivity under correlated shortfall, where
     the correlations are taken from the §S7.5b empirical matrix
     (Mississippi-Yazoo r=0.11, Mississippi-Tensas r=0.34,
     Tensas-Yazoo r=0.54, Bayou Macon-Tensas r=0.90).

Output: results/sensitivity/water_route_epsilon.json
"""
from pathlib import Path
import json
import sys

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))


# Canoe-accessible drainage assignment per LMV site.
# Each site gets a vector of access weights (0, 0.5, 1) for the four drainages:
# (Bayou Macon, Mississippi, Tensas, Yazoo).
# Plus a fifth slot for the Macon Ridge upland (terrestrial-only, treated
# as half-correlated with the Bayou Macon-Tensas regime).
#
# Access logic: 1.0 = direct confluence access (within 1 day of canoe travel
# along navigable channels); 0.5 = single-day canoe access via portage or
# secondary channels; 0.0 = beyond the canoe-day catchment.
SITE_ACCESS = {
    'Poverty Point':    {'BayouMacon': 1.0, 'Mississippi': 1.0, 'Tensas': 1.0, 'Yazoo': 1.0, 'Upland': 1.0},
    'Lower Jackson':    {'BayouMacon': 1.0, 'Mississippi': 0.5, 'Tensas': 0.5, 'Yazoo': 0.5, 'Upland': 1.0},
    'Watson Brake':     {'BayouMacon': 0.0, 'Mississippi': 0.0, 'Tensas': 0.0, 'Yazoo': 0.0, 'Upland': 1.0},  # Bayou Bartholomew, treat as own regime
    "Frenchman's Bend": {'BayouMacon': 0.0, 'Mississippi': 0.0, 'Tensas': 0.0, 'Yazoo': 0.0, 'Upland': 1.0},  # Ouachita tributary
    'Caney':            {'BayouMacon': 0.0, 'Mississippi': 0.0, 'Tensas': 0.0, 'Yazoo': 0.0, 'Upland': 1.0},  # Sicily Island Hills
    'Insley':           {'BayouMacon': 0.5, 'Mississippi': 0.0, 'Tensas': 0.5, 'Yazoo': 0.0, 'Upland': 1.0},
    'Cowpen Slough':    {'BayouMacon': 0.0, 'Mississippi': 0.0, 'Tensas': 1.0, 'Yazoo': 0.0, 'Upland': 0.5},
    'J.W. Copes':       {'BayouMacon': 0.0, 'Mississippi': 0.0, 'Tensas': 1.0, 'Yazoo': 0.0, 'Upland': 0.5},
    'Jaketown':         {'BayouMacon': 0.0, 'Mississippi': 0.5, 'Tensas': 0.0, 'Yazoo': 1.0, 'Upland': 0.5},
    'Claiborne':        {'BayouMacon': 0.0, 'Mississippi': 0.0, 'Tensas': 0.0, 'Yazoo': 0.0, 'Upland': 0.0},  # Pearl River + Gulf
    'Cedarland':        {'BayouMacon': 0.0, 'Mississippi': 0.0, 'Tensas': 0.0, 'Yazoo': 0.0, 'Upland': 0.0},  # Pearl River + Gulf
}

# Watson Brake and Frenchman's Bend access their own Ouachita-system
# drainages. Add a "OuachitaSystem" slot for them; Caney accesses Sicily
# Island via small tributaries (treated as Tensas-correlated). The
# coastal pair accesses Pearl River + Gulf, structurally distinct.
SITE_ACCESS['Watson Brake']['OuachitaSystem'] = 1.0
SITE_ACCESS["Frenchman's Bend"]['OuachitaSystem'] = 1.0
SITE_ACCESS['Caney']['Tensas'] = 0.5  # via small tributaries
SITE_ACCESS['Claiborne']['PearlGulf'] = 1.0
SITE_ACCESS['Cedarland']['PearlGulf'] = 1.0


# Empirical correlation matrix from §S7.5b USGS gauge analysis.
# Drainages: BayouMacon, Mississippi, Tensas, Yazoo, Upland (Macon Ridge),
# OuachitaSystem (proxy as moderate correlation with Tensas), PearlGulf
# (treated as independent of LMV interior).
DRAINAGE_NAMES = ['BayouMacon', 'Mississippi', 'Tensas', 'Yazoo',
                  'Upland', 'OuachitaSystem', 'PearlGulf']
N_DRAINAGES = len(DRAINAGE_NAMES)

# Correlation matrix (rho_ij)
RHO = np.array([
    # BayouMacon, Mississippi, Tensas, Yazoo, Upland, OuachitaSystem, PearlGulf
    [1.00, 0.11, 0.90, 0.30, 0.45, 0.20, 0.00],  # Bayou Macon
    [0.11, 1.00, 0.34, 0.11, 0.10, 0.20, 0.00],  # Mississippi
    [0.90, 0.34, 1.00, 0.54, 0.45, 0.30, 0.00],  # Tensas
    [0.30, 0.11, 0.54, 1.00, 0.30, 0.15, 0.00],  # Yazoo
    [0.45, 0.10, 0.45, 0.30, 1.00, 0.20, 0.00],  # Upland (Macon Ridge)
    [0.20, 0.20, 0.30, 0.15, 0.20, 1.00, 0.00],  # OuachitaSystem
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00],  # PearlGulf
])
# (Off-diagonal entries for Bayou Macon-Yazoo, Bayou Macon-Upland, Tensas-Upland,
# etc., interpolated from §S7.5b structure: high within Macon-Ridge regime,
# moderate between Mississippi/Yazoo, low elsewhere. PearlGulf assumed
# independent of LMV interior since they sample distinct climatic regimes.)

# Site monument scale ordinal from Table 1
SITE_SCALE = {
    'Poverty Point': 3, 'Lower Jackson': 0, 'Watson Brake': 2,
    "Frenchman's Bend": 1, 'Caney': 2, 'Insley': 2,
    'Cowpen Slough': 0, 'J.W. Copes': 0, 'Jaketown': 1,
    'Claiborne': 1, 'Cedarland': 1,
}


def site_access_vector(site: str) -> np.ndarray:
    """Return the 7-vector of access weights per drainage."""
    a = SITE_ACCESS[site]
    return np.array([a.get(d, 0.0) for d in DRAINAGE_NAMES])


def covariance_epsilon(access: np.ndarray, rho: np.ndarray, n_years: int = 5000,
                       rng_seed: int = 42) -> dict:
    """Compute variance-reduction-based epsilon for a site.

    Procedure:
      1. Generate n_years samples of standard-normal correlated drainage
         shortfall, with the given rho correlation matrix.
      2. Map each drainage's standard normal to a [0, 1] productivity
         multiplier via the normal CDF.
      3. Site total productivity = sum(access * productivity) per year.
      4. Compare CV (sd/mean) of this total against a single-drainage
         baseline (a single drainage with access=1).
      5. eps = 0.5 * cv_reduction
    """
    rng = np.random.default_rng(rng_seed)
    # Cholesky decomposition of correlation matrix
    L = np.linalg.cholesky(rho + 1e-9 * np.eye(len(rho)))
    z = rng.standard_normal((n_years, len(rho)))
    correlated = z @ L.T
    # Convert to [0,1] via tanh approximation of normal CDF
    productivity = 0.5 * (1.0 + np.tanh(correlated * 0.79788))

    site_prod = (productivity * access).sum(axis=1)
    site_mean = float(np.mean(site_prod))
    site_sd = float(np.std(site_prod, ddof=1))
    cv = site_sd / site_mean if site_mean > 0 else float('inf')

    # Single-drainage baseline (use Bayou Macon as reference; result is
    # invariant to choice if we use the same drainage every time).
    one_zone = np.zeros(len(rho))
    one_zone[0] = 1.0
    base_prod = (productivity * one_zone).sum(axis=1)
    base_cv = float(np.std(base_prod, ddof=1) / np.mean(base_prod))

    cv_reduction = (base_cv - cv) / base_cv if base_cv > 0 else 0.0
    eps = 0.5 * max(0.0, min(1.0, cv_reduction))

    # Independent-regime count: number of drainages with access >= 0.5
    # AND mean cross-correlation with each other (within accessed set)
    # < 0.6 (a heuristic threshold for "substantively independent").
    accessed = [i for i, a in enumerate(access) if a >= 0.5]
    independent_regimes = 0
    used = set()
    for i in accessed:
        if i in used:
            continue
        independent_regimes += 1
        used.add(i)
        for j in accessed:
            if j != i and rho[i, j] >= 0.6:
                used.add(j)

    return {
        'site_mean_productivity': site_mean,
        'site_sd_productivity': site_sd,
        'cv': cv,
        'baseline_cv': base_cv,
        'cv_reduction': cv_reduction,
        'eps_water_route': eps,
        'independent_regimes': int(independent_regimes),
    }


def main():
    rows = []
    print(f'{"Site":22s} {"acc":>4s} {"eps_wr":>8s} {"cv":>8s} {"indep":>6s} '
          f'{"scale":>6s}')
    print('-' * 70)

    for site in SITE_ACCESS.keys():
        access = site_access_vector(site)
        result = covariance_epsilon(access, RHO)
        rows.append({
            'site': site,
            'access_vector': access.tolist(),
            'monument_scale': SITE_SCALE[site],
            **result,
        })
        n_acc = int(np.sum(access >= 0.5))
        print(f'{site:22s} {n_acc:>4d} {result["eps_water_route"]:8.3f} '
              f'{result["cv"]:8.3f} {result["independent_regimes"]:6d} '
              f'{SITE_SCALE[site]:6d}')

    # Spearman: water-route eps vs observed monument scale
    eps_vals = [r['eps_water_route'] for r in rows]
    indep_vals = [r['independent_regimes'] for r in rows]
    scales = [r['monument_scale'] for r in rows]
    rho_eps_scale, p_eps = spearmanr(eps_vals, scales)
    rho_indep_scale, p_indep = spearmanr(indep_vals, scales)

    print()
    print('Spearman correlations:')
    print(f'  Water-route eps vs ordinal monument scale: rho = {rho_eps_scale:+.3f}, p = {p_eps:.3f}')
    print(f'  Independent-regimes vs ordinal scale:      rho = {rho_indep_scale:+.3f}, p = {p_indep:.3f}')

    out_dir = Path('results/sensitivity')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'water_route_epsilon.json'
    with open(out_file, 'w') as f:
        json.dump({
            'sites': rows,
            'drainage_names': DRAINAGE_NAMES,
            'correlation_matrix': RHO.tolist(),
            'spearman': {
                'eps_vs_ordinal_scale': {'rho': float(rho_eps_scale), 'p': float(p_eps)},
                'indep_regimes_vs_ordinal_scale': {'rho': float(rho_indep_scale), 'p': float(p_indep)},
            },
        }, f, indent=2)
    print(f'\nWrote {out_file}')


if __name__ == '__main__':
    main()
