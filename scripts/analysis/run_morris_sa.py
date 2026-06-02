#!/usr/bin/env python3
"""Morris elementary-effects global sensitivity analysis.

R3 #5 requested a global SA beyond the OAT tornado. Morris elementary-effects
visits R trajectories of length k+1 in a k-dimensional unit cube; each step
varies one parameter by delta. We compute mu* (mean absolute EE) and sigma
(std of EE) for each parameter.

Parameters varied (6): the ones reported in S3.1 as driving sigma*:
  lambda_W, lambda_C_init, lambda_X_init, M_half, beta_C, beta_net

Outcome variable: equilibrium lambda_total at fixed sigma=0.45 (just above sigma*).

R=10 trajectories x 7 evaluations per trajectory = 70 model calls.
Each call is a closed-form lambda_total_at_sigma evaluation (~ms), so this
runs fast compared to the ABM. Total ~minutes.
"""
import sys
import json
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point/src')

import numpy as np

from poverty_point.signaling_core import (
    lambda_total_at_sigma,
    SignalingParams,
    NetworkParams,
    ConflictParams,
)

OUTPUT_DIR = Path('/Users/clipo/PycharmProjects/poverty-point/results/analysis')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Parameter ranges (±50% of canonical values)
PARAM_RANGES = {
    'lambda_W': (0.075, 0.225),         # canonical 0.15
    'lambda_C_init': (0.05, 0.15),      # canonical 0.10
    'lambda_X_init': (0.075, 0.225),    # canonical 0.15
    'M_half': (1.25, 3.75),             # canonical 2.5
    'beta_conflict': (0.04, 0.12),      # canonical 0.08
    'xi_X': (0.0, 1.0),                 # canonical 0.0 (extension)
}
PARAM_NAMES = list(PARAM_RANGES.keys())
K = len(PARAM_NAMES)

# Morris settings
R = 10
LEVELS = 4
DELTA = LEVELS / (2 * (LEVELS - 1))  # = 0.667 for p=4

SIGMA_EVAL = 0.45  # evaluate near threshold


def to_native(x, lo, hi):
    """Map from unit cube to native parameter range."""
    return lo + x * (hi - lo)


def evaluate(params_unit):
    """Evaluate lambda_total at sigma=SIGMA_EVAL given unit-cube params."""
    native = {}
    for i, name in enumerate(PARAM_NAMES):
        lo, hi = PARAM_RANGES[name]
        native[name] = to_native(params_unit[i], lo, hi)

    sig = SignalingParams(
        lambda_W=native['lambda_W'],
        lambda_C=native['lambda_C_init'],
        lambda_X=native['lambda_X_init'],
    )
    conf = ConflictParams(beta_conflict=native['beta_conflict'])
    net = NetworkParams(M_half=native['M_half'], xi_X=native['xi_X'])

    try:
        eq = lambda_total_at_sigma(
            sigma=SIGMA_EVAL,
            sig_params=sig,
            conf_params=conf,
            net_params=net,
        )
        return float(eq['lambda_total'])
    except Exception:
        return float('nan')


def morris_trajectory(rng):
    """Generate one Morris trajectory of length k+1."""
    # Random starting point on grid (avoiding upper-half of cube)
    grid_levels = np.linspace(0, 1 - DELTA, LEVELS // 2)
    x_star = rng.choice(grid_levels, size=K)
    # Random permutation of parameter order
    order = rng.permutation(K)
    # Random sign for delta
    sign = rng.choice([-1, 1], size=K)

    traj = [x_star.copy()]
    x = x_star.copy()
    for idx in order:
        x = x.copy()
        x[idx] = x[idx] + sign[idx] * DELTA
        # Reflect if out of bounds
        if x[idx] > 1.0:
            x[idx] = x[idx] - 2 * DELTA
        elif x[idx] < 0.0:
            x[idx] = x[idx] + 2 * DELTA
        traj.append(x.copy())
    return np.array(traj), order, sign


def main():
    rng = np.random.default_rng(42)
    t0 = time.time()

    elementary_effects = {name: [] for name in PARAM_NAMES}

    for r in range(R):
        traj, order, sign = morris_trajectory(rng)
        y = np.array([evaluate(x) for x in traj])
        # Elementary effects
        for step, idx in enumerate(order):
            ee = (y[step + 1] - y[step]) / (sign[idx] * DELTA)
            elementary_effects[PARAM_NAMES[idx]].append(float(ee))
        print(f"Trajectory {r+1}/{R} done, y={y}", flush=True)

    # Summary statistics
    summary = {}
    for name in PARAM_NAMES:
        ees = np.array(elementary_effects[name])
        ees_finite = ees[np.isfinite(ees)]
        summary[name] = {
            'mu': float(np.mean(ees_finite)) if len(ees_finite) else float('nan'),
            'mu_star': float(np.mean(np.abs(ees_finite))) if len(ees_finite) else float('nan'),
            'sigma': float(np.std(ees_finite, ddof=1)) if len(ees_finite) > 1 else float('nan'),
            'n_finite': int(len(ees_finite)),
            'n_total': int(len(ees)),
        }

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_file = OUTPUT_DIR / f'morris_sa_{timestamp}.json'
    payload = {
        'method': 'Morris elementary effects',
        'R_trajectories': R,
        'levels': LEVELS,
        'delta': DELTA,
        'sigma_eval': SIGMA_EVAL,
        'outcome': 'lambda_total_at_sigma',
        'param_ranges': PARAM_RANGES,
        'summary': summary,
        'elementary_effects': elementary_effects,
        'runtime_seconds': time.time() - t0,
    }
    with open(out_file, 'w') as f:
        json.dump(payload, f, indent=2)
    print(f"\nDone in {time.time()-t0:.1f}s. Saved: {out_file}", flush=True)
    # Print ranking
    print("\nMorris ranking (mu*, sigma):")
    for name in sorted(summary, key=lambda n: -summary[n]['mu_star']):
        s = summary[name]
        print(f"  {name:20s}  mu*={s['mu_star']:.5f}  sigma={s['sigma']:.5f}")


if __name__ == '__main__':
    main()
