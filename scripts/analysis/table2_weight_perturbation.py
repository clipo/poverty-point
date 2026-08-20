"""Monte Carlo perturbation of the Table 2 zone-access weights (§S13).

Perturbs each of the five zone-access weights per site by U(-0.2, +0.2)
(clipped to [0, 1]), recomputes the Shannon-derived epsilon
(eps = 0.5 * H / ln 5), and summarizes the stability of the resulting
site ranking across draws:

  - fraction of draws in which Poverty Point ranks first on epsilon
  - fraction in which the coastal pair (Claiborne, Cedarland) occupies
    the bottom two ranks
  - fraction in which the full baseline ordering is exactly preserved
  - Spearman rho of epsilon vs observed ordinal monument scale per draw
    (mean and 95% interval)

Output: results/sensitivity/table2_weight_perturbation.json
"""
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

# Corrected Table 2 weight vectors (w_a, w_u, w_d, w_m, w_p): aquatic,
# upland, drainage, mast, prairie (§S6).
SITES = [
    ('Poverty Point',    [1.0, 1.0, 1.0, 1.0, 0.5], 3),
    ('Lower Jackson',    [1.0, 0.9, 0.9, 1.0, 0.3], 0),
    ('Watson Brake',     [0.8, 0.7, 0.7, 0.8, 0.0], 2),
    ('Caney',            [0.9, 0.6, 0.8, 0.8, 0.0], 2),
    ("Frenchman's Bend", [0.7, 0.5, 0.7, 0.7, 0.0], 1),
    ('Insley',           [0.9, 0.6, 0.8, 0.9, 0.0], 2),
    ('J.W. Copes',       [0.5, 0.6, 0.4, 0.7, 0.0], 0),
    ('Cowpen Slough',    [0.9, 0.5, 0.8, 0.7, 0.0], 0),
    ('Jaketown',         [1.0, 0.3, 0.8, 0.5, 0.0], 1),
    ('Claiborne',        [1.0, 0.5, 0.5, 0.3, 0.0], 1),
    ('Cedarland',        [1.0, 0.5, 0.5, 0.3, 0.0], 1),
]

N_DRAWS = 1000
PERTURB = 0.2
H_MAX = np.log(5.0)


def epsilon_from_weights(w: np.ndarray) -> float:
    w = np.clip(w, 0.0, 1.0)
    total = w.sum()
    if total <= 0:
        return 0.0
    p = w[w > 0] / total
    H = float(-(p * np.log(p)).sum())
    return 0.5 * H / H_MAX


def main():
    rng = np.random.default_rng(42)
    names = [s[0] for s in SITES]
    base_w = np.array([s[1] for s in SITES])
    scale = np.array([s[2] for s in SITES])
    coastal_idx = {names.index('Claiborne'), names.index('Cedarland')}
    pp_idx = names.index('Poverty Point')

    base_eps = np.array([epsilon_from_weights(w) for w in base_w])
    base_order = tuple(np.argsort(-base_eps))

    pp_first = 0
    coastal_bottom = 0
    full_order = 0
    rhos = []
    for _ in range(N_DRAWS):
        w = base_w + rng.uniform(-PERTURB, PERTURB, size=base_w.shape)
        eps = np.array([epsilon_from_weights(row) for row in w])
        order = np.argsort(-eps)
        if order[0] == pp_idx:
            pp_first += 1
        if set(order[-2:]) == coastal_idx:
            coastal_bottom += 1
        if tuple(order) == base_order:
            full_order += 1
        rhos.append(spearmanr(eps, scale).statistic)

    rhos = np.array(rhos)
    results = {
        'n_draws': N_DRAWS,
        'perturbation': PERTURB,
        'baseline_epsilon': {n: float(e) for n, e in zip(names, base_eps)},
        'pp_first_fraction': pp_first / N_DRAWS,
        'coastal_bottom_two_fraction': coastal_bottom / N_DRAWS,
        'full_order_preserved_fraction': full_order / N_DRAWS,
        'rho_eps_vs_scale_mean': float(np.mean(rhos)),
        'rho_eps_vs_scale_ci95': [float(np.percentile(rhos, 2.5)),
                                  float(np.percentile(rhos, 97.5))],
    }
    print(f"PP first: {results['pp_first_fraction']:.0%}")
    print(f"Coastal pair bottom two: {results['coastal_bottom_two_fraction']:.0%}")
    print(f"Full order preserved: {results['full_order_preserved_fraction']:.0%}")
    print(f"rho(eps, scale): mean {results['rho_eps_vs_scale_mean']:+.2f}, "
          f"95% CI [{results['rho_eps_vs_scale_ci95'][0]:+.2f}, "
          f"{results['rho_eps_vs_scale_ci95'][1]:+.2f}]")

    out = Path('results/sensitivity/table2_weight_perturbation.json')
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {out}")


if __name__ == '__main__':
    main()
