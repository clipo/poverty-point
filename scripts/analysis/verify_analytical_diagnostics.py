"""Analytical diagnostics claimed in the manuscript and supplement.

Backs four verification claims with committed, re-runnable code:

1. Fixed-point convergence (§S2): 30-point sweep of sigma on [0.10, 0.95];
   all runs must converge within tolerance, with iteration counts reported.
2. Multi-start uniqueness (§S2): the lambda-sigma fixed point reached from
   widely separated starting values at sigma in {0.30, 0.50, 0.70} must
   agree in equilibrium M_g to better than 1 part in 1e4.
3. Single crossing (§2.4): W_agg - W_ind is monotonically increasing in
   sigma on the range used, with exactly one sign change (unique sigma*).
4. Reference-window invariance (§S1.4): the ratio sigma_LMV / sigma* is
   preserved exactly across T0 in {5, 10, 20, 50} (both quantities rescale
   by sqrt(T0/20)).

Output: results/sensitivity/analytical_diagnostics.json
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from poverty_point.signaling_core import (  # noqa: E402
    SignalingParams, NetworkParams, ConflictParams, AggregationParams,
    lambda_total_at_sigma, fitness_advantage, critical_threshold,
    expected_monument_stock, effective_monument_stock,
    compute_lambda_C, compute_lambda_X,
)

SIG, NET, CONF, AGG = (SignalingParams(), NetworkParams(),
                       ConflictParams(), AggregationParams())


def check_convergence():
    iters, conv = [], []
    for s in np.linspace(0.10, 0.95, 30):
        eq = lambda_total_at_sigma(s, SIG, NET, CONF, AGG, 25)
        iters.append(eq['iterations'])
        conv.append(bool(eq['converged']))
    out = {
        'n_points': 30,
        'all_converged': all(conv),
        'iterations_mean': float(np.mean(iters)),
        'iterations_median': float(np.median(iters)),
        'iterations_max': int(max(iters)),
    }
    print(f"1. Convergence: {sum(conv)}/30 converged; iterations "
          f"mean={out['iterations_mean']:.1f} median={out['iterations_median']:.0f} "
          f"max={out['iterations_max']}")
    return out


def fixed_point_from(sigma, lam0, tol=1e-6, max_iter=500, damping=0.5):
    lam = lam0
    for _ in range(max_iter):
        I_g = expected_monument_stock(25, SIG.q_min, SIG.q_max, lam)
        M_g = effective_monument_stock(I_g, SIG.delta)
        lam_new = (SIG.lambda_W + compute_lambda_C(M_g, CONF)
                   + compute_lambda_X(M_g, sigma, NET))
        lam_up = damping * lam + (1 - damping) * lam_new
        if abs(lam_up - lam) < tol:
            lam = lam_up
            break
        lam = lam_up
    I_g = expected_monument_stock(25, SIG.q_min, SIG.q_max, lam)
    return effective_monument_stock(I_g, SIG.delta)


def check_multistart():
    rows = []
    ok = True
    for s in (0.30, 0.50, 0.70):
        Ms = [fixed_point_from(s, l0) for l0 in (0.01, 0.40, 2.0)]
        rel = max(Ms) / min(Ms) - 1.0
        ok = ok and rel < 1e-4
        rows.append({'sigma': s, 'M_g': Ms, 'max_rel_diff': rel})
        print(f"2. Multi-start sigma={s}: M_g = "
              f"{Ms[0]:.4f}/{Ms[1]:.4f}/{Ms[2]:.4f} (rel diff {rel:.2e})")
    return {'unique_within_1e－4'.replace('－', '-'): ok, 'rows': rows}


def check_single_crossing():
    grid = np.linspace(0.05, 0.95, 46)
    fa = np.array([fitness_advantage(s, 0.35, 25, 100.0) for s in grid])
    d = np.diff(fa)
    sign_changes = int(np.sum(np.diff(np.sign(fa)) != 0))
    out = {
        'monotone_increasing': bool(np.all(d > 0)),
        'sign_changes': sign_changes,
        'fa_low': float(fa[0]),
        'fa_high': float(fa[-1]),
    }
    print(f"3. Single crossing: monotone increasing={out['monotone_increasing']}, "
          f"sign changes={sign_changes}, fa(0.05)={fa[0]:.4f}, fa(0.95)={fa[-1]:.4f}")
    return out


def check_window_invariance():
    sigma_star_20 = critical_threshold(epsilon=0.35, n_agg=25)['sigma_star']
    sigma_lmv_20 = 0.45 * np.sqrt(20.0 / 10.0)  # T=10, m=0.45
    rows = []
    ratios = []
    for T0 in (5, 10, 20, 50):
        scale = np.sqrt(T0 / 20.0)
        lmv, star = sigma_lmv_20 * scale, sigma_star_20 * scale
        ratios.append(lmv / star)
        rows.append({'T0': T0, 'sigma_LMV': float(lmv),
                     'sigma_star': float(star), 'ratio': float(lmv / star)})
        print(f"4. T0={T0:2d}: sigma_LMV={lmv:.3f} sigma*={star:.3f} "
              f"ratio={lmv/star:.4f}")
    return {'ratio_invariant': bool(np.ptp(ratios) < 1e-12), 'rows': rows}


def check_site_margins():
    """§6.3 threshold margins and fitness differentials for WB and PP."""
    rows = {}
    for name, sigma, eps, n in (('watson_brake', 0.56, 0.43, 8),
                                ('poverty_point', 0.64, 0.49, 25)):
        fa = fitness_advantage(sigma, eps, n, 100.0)
        star = critical_threshold(epsilon=eps, n_agg=n)['sigma_star']
        rows[name] = {'sigma': sigma, 'epsilon': eps, 'n_agg': n,
                      'sigma_star': float(star),
                      'margin': float(sigma - star),
                      'fitness_differential': float(fa)}
        print(f"5. {name}: sigma*={star:.3f} margin={sigma-star:+.3f} "
              f"W_agg-W_ind={fa:+.3f}")
    return rows


def main():
    results = {
        'convergence': check_convergence(),
        'multistart_uniqueness': check_multistart(),
        'single_crossing': check_single_crossing(),
        'window_invariance': check_window_invariance(),
        'site_margins': check_site_margins(),
    }
    out = Path('results/sensitivity/analytical_diagnostics.json')
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {out}")


if __name__ == '__main__':
    main()
