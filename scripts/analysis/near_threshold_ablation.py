"""
Extension 4: Near-threshold ablation sweep.

The §4.3 ablation reports threshold shift +36% from removing lambda_W
(0.543 -> 0.400) and concedes that at PP-scenario parameters the
signaling apparatus produces no measurable change in cumulative monument
or exotic outputs because PP sits comfortably above threshold. The
prediction is that the apparatus matters most at near-threshold
parameter regimes, where small fitness differentials matter.

This script tests that prediction analytically by computing equilibrium
M_g across a sigma sweep that straddles sigma_star, under both
signal-conditional and signal-blind parameterizations. The signal-blind
condition is implemented by setting lambda_W = 0 in the analytical
critical_threshold function.

Output: results/sensitivity/near_threshold_ablation.json
"""
from pathlib import Path
import json
import sys
from dataclasses import replace

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from poverty_point.parameters import SimulationParameters
from poverty_point.signaling_core import critical_threshold as full_ct


EPS_PP = 0.35
N_AGG = 25
SIGMA_RANGE = np.linspace(0.30, 0.65, 15)


def equilibrium_at(eps: float, n: int, lambda_w: float, params: SimulationParameters):
    new_sig = replace(params.signaling, lambda_W=lambda_w)
    new_p = replace(params, signaling=new_sig)
    r = full_ct(epsilon=eps, n_agg=n,
                sig_params=new_p.signaling, net_params=new_p.network,
                conf_params=new_p.conflict, agg_params=new_p.aggregation)
    return r['sigma_star'], r['M_g']


def main():
    params = SimulationParameters()

    rows = []
    print(f'{"sigma":>7s} {"M_g_signal":>12s} {"M_g_blind":>12s} '
          f'{"diff":>10s} {"sig*_sg":>10s} {"sig*_bl":>10s}')
    print('-' * 72)
    for sigma in SIGMA_RANGE:
        # Signal-conditional: lambda_W = 0.15 (default)
        ss_sg, Mg_sg = equilibrium_at(EPS_PP, N_AGG, 0.15, params)
        # Signal-blind: lambda_W = 0
        ss_bl, Mg_bl = equilibrium_at(EPS_PP, N_AGG, 0.0, params)
        # Note: at sigma below sigma*, we're in the independent regime
        # and equilibrium M_g still represents the aggregator-state
        # equilibrium (since the analytical model computes M_g
        # unconditionally on whether aggregation is realized).
        # The substantive comparison: at sigma values straddling sigma*,
        # does removing the signaling apparatus change M_g?
        # M_g is independent of sigma in the analytical model
        # (it's the equilibrium attractor of the lambda-sigma loop at
        # given eps and n_agg with the lambda_W asserted).
        # The relevant comparison is the sigma_star shift and the
        # resulting fitness-differential at each sigma.
        diff = Mg_sg - Mg_bl
        rows.append({
            'sigma': float(sigma),
            'M_g_signal': float(Mg_sg),
            'M_g_blind': float(Mg_bl),
            'diff': float(diff),
            'sigma_star_signal': float(ss_sg),
            'sigma_star_blind': float(ss_bl),
        })
        print(f'{sigma:7.3f} {Mg_sg:12.2f} {Mg_bl:12.2f} {diff:10.3f} '
              f'{ss_sg:10.3f} {ss_bl:10.3f}')

    # The analytical M_g is sigma-independent because the equilibrium
    # is solved for the aggregator regime; the threshold sigma_star is
    # what shifts when lambda_W changes. So the direct M_g comparison
    # is constant across sigma. The relevant near-threshold question
    # is whether sigma_star moves, and where each sigma sits relative
    # to the two thresholds.
    print()
    print(f'Signal-conditional sigma* = {rows[0]["sigma_star_signal"]:.3f}')
    print(f'Signal-blind sigma*       = {rows[0]["sigma_star_blind"]:.3f}')
    print(f'Threshold shift           = {rows[0]["sigma_star_signal"] - rows[0]["sigma_star_blind"]:+.3f}')
    print(f'Sigma values for which signaling moves regime classification:')
    for r in rows:
        signal_above = r['sigma'] > r['sigma_star_signal']
        blind_above = r['sigma'] > r['sigma_star_blind']
        if signal_above != blind_above:
            print(f'  sigma = {r["sigma"]:.3f}: signaling above ({signal_above}), blind above ({blind_above})')

    out_dir = Path('results/sensitivity')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'near_threshold_ablation.json'
    with open(out_file, 'w') as f:
        json.dump({
            'epsilon': EPS_PP,
            'n_agg': N_AGG,
            'rows': rows,
        }, f, indent=2)
    print(f'\nWrote {out_file}')


if __name__ == '__main__':
    main()
