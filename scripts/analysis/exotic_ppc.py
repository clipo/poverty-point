"""Per-material posterior-predictive check and joint Mahalanobis distance (§6.1).

Consumes the PP-scenario calibration replicates
(results/calibration_replicates/replicates_n8_d200.json) and the
archaeological exotic-material counts, and computes every quantitative
claim in the §6.1 per-material comparison:

  - per-material replicate mean, sample SD (ddof = 1), and 95% predictive
    interval (mean ± 1.96 SD)
  - per-material z-score of the archaeological count
  - overprediction ratios (model mean / archaeological count)
  - cross-material replicate correlation matrix
  - joint Mahalanobis d² of the four-material archaeological vector
    (copper, steatite, galena, crystal quartz) against the replicate
    mean and covariance

Output: results/calibration_replicates/exotic_ppc.json
"""
import json
from pathlib import Path

import numpy as np

# Archaeological counts (Webb 1982; Gibson and Griffing 1994; §5.4).
ARCHAEOLOGICAL = {
    'copper': 155,
    'steatite': 2221,
    'galena': 740,
    'novaculite': 101,
    'crystal_quartz': 395,
}
JOINT_MATERIALS = ['copper', 'steatite', 'galena', 'crystal_quartz']

REPLICATES = Path('results/calibration_replicates/replicates_n8_d200.json')


def main():
    with open(REPLICATES) as f:
        data = json.load(f)
    reps = data['poverty_point']
    materials = sorted(ARCHAEOLOGICAL)

    counts = {m: np.array([r['exotics_by_material'].get(m, 0) for r in reps],
                          dtype=float)
              for m in materials}

    per_material = {}
    print(f"{'material':>14s} {'mean':>9s} {'sd':>7s} {'95% PI':>18s} "
          f"{'obs':>6s} {'z':>7s} {'ratio':>7s}")
    for m in materials:
        x = counts[m]
        mean, sd = float(np.mean(x)), float(np.std(x, ddof=1))
        lo, hi = mean - 1.96 * sd, mean + 1.96 * sd
        obs = ARCHAEOLOGICAL[m]
        z = (obs - mean) / sd if sd > 0 else float('nan')
        ratio = mean / obs if obs > 0 else float('nan')
        per_material[m] = {
            'model_mean': mean, 'model_sd_ddof1': sd,
            'predictive_interval_95': [lo, hi],
            'archaeological_count': obs,
            'z_score': float(z),
            'overprediction_ratio': float(ratio),
            'observation_inside_interval': bool(lo <= obs <= hi),
        }
        print(f"{m:>14s} {mean:9.1f} {sd:7.1f} [{lo:7.1f}, {hi:8.1f}] "
              f"{obs:6d} {z:+7.1f} {ratio:6.2f}x")

    # Cross-material correlations among the four joint materials
    X = np.column_stack([counts[m] for m in JOINT_MATERIALS])
    corr = np.corrcoef(X, rowvar=False)
    offdiag = corr[np.triu_indices_from(corr, k=1)]
    print(f"\nCross-material correlations ({', '.join(JOINT_MATERIALS)}): "
          f"r = {offdiag.min():.2f} to {offdiag.max():.2f}")

    # Joint Mahalanobis d²
    mu = X.mean(axis=0)
    cov = np.cov(X, rowvar=False, ddof=1)
    obs_vec = np.array([ARCHAEOLOGICAL[m] for m in JOINT_MATERIALS],
                       dtype=float)
    diff = obs_vec - mu
    d2 = float(diff @ np.linalg.solve(cov, diff))
    print(f"Joint Mahalanobis d^2 = {d2:,.0f}")

    out = {
        'per_material': per_material,
        'joint_materials': JOINT_MATERIALS,
        'cross_material_correlations': {
            'matrix': corr.tolist(),
            'offdiag_min': float(offdiag.min()),
            'offdiag_max': float(offdiag.max()),
        },
        'mahalanobis_d2': d2,
        'n_replicates': len(reps),
    }
    out_path = Path('results/calibration_replicates/exotic_ppc.json')
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
