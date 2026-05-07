"""
Extension 5: Test the restructured network-saturation function.

Compares lambda_X behavior at equilibrium under three settings:
  1. Original (xi_X = 0): the documented §4.3 result, lambda_X ~ 0.
  2. Restructured low (xi_X = 0.25): modest non-marginal contribution.
  3. Restructured high (xi_X = 0.5): substantial non-marginal contribution.

For each setting, recomputes:
  - Equilibrium lambda_X at PP parameters
  - Critical threshold sigma* at PP parameters (eps=0.35, n_agg=25)
  - Critical threshold sigma* with signaling apparatus zeroed (lambda_W=0)
  - Threshold shift attributable to the apparatus
  - Whether the signaling-vs-cooperation discrimination is now genuine
    (i.e., the +36% shift no longer reduces to "removing one constant")

Output: results/sensitivity/restructured_saturation_test.json
"""
from pathlib import Path
import json
import sys
from dataclasses import replace

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from poverty_point.parameters import SimulationParameters
from poverty_point.signaling_core import critical_threshold as full_ct


EPS_PP = 0.35
N_AGG = 25


def measure(xi_X: float, lambda_W: float, params: SimulationParameters):
    new_net = replace(params.network, xi_X=xi_X)
    new_sig = replace(params.signaling, lambda_W=lambda_W)
    new_p = replace(params, network=new_net, signaling=new_sig)
    r = full_ct(epsilon=EPS_PP, n_agg=N_AGG,
                sig_params=new_p.signaling, net_params=new_p.network,
                conf_params=new_p.conflict, agg_params=new_p.aggregation)
    return r


def main():
    base_params = SimulationParameters()

    print(f'{"xi_X":>6s} {"lam_W":>6s} {"sigma*":>8s} {"M_g":>8s} '
          f'{"lambda_total":>14s} {"lambda_W":>10s} {"lambda_X":>10s}')
    print('-' * 85)

    rows = []
    for xi in [0.0, 0.25, 0.50]:
        # Full apparatus
        r_full = measure(xi, 0.15, base_params)
        # Signaling-blind ablation (lambda_W=0)
        r_blind = measure(xi, 0.0, base_params)

        rows.append({
            'xi_X': xi,
            'full_apparatus': {
                'sigma_star': r_full['sigma_star'],
                'M_g': r_full['M_g'],
                'lambda_total': r_full['lambda_total'],
                'lambda_W': 0.15,
                'lambda_X_at_equilibrium': r_full['lambda_total'] - 0.15,  # subtract lambda_W
            },
            'signal_blind': {
                'sigma_star': r_blind['sigma_star'],
                'M_g': r_blind['M_g'],
                'lambda_total': r_blind['lambda_total'],
                'lambda_W': 0.0,
                'lambda_X_at_equilibrium': r_blind['lambda_total'],
            },
            'threshold_shift_pct': float(
                (r_blind['sigma_star'] - r_full['sigma_star']) / r_full['sigma_star'] * 100
            ),
            'threshold_shift_abs': float(r_blind['sigma_star'] - r_full['sigma_star']),
        })
        # Print full + blind rows
        print(f'{xi:6.2f} {0.15:6.2f} {r_full["sigma_star"]:8.4f} '
              f'{r_full["M_g"]:8.2f} {r_full["lambda_total"]:14.4f} '
              f'{0.15:10.4f} {r_full["lambda_total"] - 0.15:10.4f}')
        print(f'{xi:6.2f} {0.00:6.2f} {r_blind["sigma_star"]:8.4f} '
              f'{r_blind["M_g"]:8.2f} {r_blind["lambda_total"]:14.4f} '
              f'{0.00:10.4f} {r_blind["lambda_total"]:10.4f}')
        print(f'  threshold shift: '
              f'{rows[-1]["threshold_shift_abs"]:+.4f} ({rows[-1]["threshold_shift_pct"]:+.1f}%)')
        print()

    # Interpretation
    print('Interpretation:')
    print(f'  At xi_X = 0.0 (original): lambda_X at equilibrium = '
          f'{rows[0]["full_apparatus"]["lambda_X_at_equilibrium"]:.4f}')
    print(f'  At xi_X = 0.5 (restructured): lambda_X at equilibrium = '
          f'{rows[2]["full_apparatus"]["lambda_X_at_equilibrium"]:.4f}')
    print()
    print('  The §4.3 ablation result was that the +36% threshold shift came')
    print('  from removing lambda_W alone because lambda_X collapsed at')
    print('  equilibrium. With xi_X > 0 (restructured), lambda_X is')
    print('  non-trivial at equilibrium, so the ablation tests the effect')
    print('  of removing lambda_W from a system where lambda_X is also')
    print('  doing real work. Whether the qualitative threshold-shift result')
    print('  survives depends on whether the M_g equilibrium itself shifts.')

    out_dir = Path('results/sensitivity')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'restructured_saturation_test.json'
    with open(out_file, 'w') as f:
        json.dump({'rows': rows, 'epsilon': EPS_PP, 'n_agg': N_AGG}, f, indent=2)
    print(f'\nWrote {out_file}')


if __name__ == '__main__':
    main()
