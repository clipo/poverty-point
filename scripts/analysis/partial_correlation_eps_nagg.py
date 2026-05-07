"""
Partial-correlation decomposition: how much of the joint magnitude
prediction comes from epsilon vs n_agg?

The Round-4 reviews flagged that the joint M_g(eps, n_agg, alpha) prediction
gives Spearman rho = +0.91 vs observed monument volume across 11 sites,
but this could be dominated by n_agg alone. This script computes:

  - Spearman rho of n_agg alone vs observed (baseline, no framework needed)
  - Spearman rho of static epsilon alone vs observed
  - Spearman rho of phenology epsilon alone vs observed
  - Spearman rho of water-route epsilon alone vs observed
  - Spearman rho of joint M_g(eps, n_agg) vs observed
  - Marginal contribution of epsilon: joint rho - n_agg-alone rho

Output: results/sensitivity/partial_correlation_eps_nagg.json
"""
from pathlib import Path
import json
import sys

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from poverty_point.parameters import SimulationParameters
from poverty_point.signaling_core import critical_threshold as full_ct


# 11 LMV sites with: name, n_agg, ordinal scale, observed_volume_m3
SITES = [
    ('Poverty Point',    25, 3, 750000),
    ('Lower Jackson',     1, 0, 1000),
    ('Watson Brake',      8, 2, 7000),
    ("Frenchman's Bend",  5, 1, 2000),
    ('Caney',             5, 2, 5000),
    ('Insley',            6, 2, 14000),
    ('Cowpen Slough',     3, 0, 500),
    ('J.W. Copes',        3, 0, 500),
    ('Jaketown',          8, 1, 5000),
    ('Claiborne',         4, 1, 3000),
    ('Cedarland',         4, 1, 1000),
]

# Per-site epsilon values (from §4.5 Table 1 static, §S7.6 phenology, §S7.7 water-route)
EPS_STATIC = {
    'Poverty Point': 0.49, 'Lower Jackson': 0.48, 'Watson Brake': 0.43,
    "Frenchman's Bend": 0.43, 'Caney': 0.43, 'Insley': 0.43,
    'Cowpen Slough': 0.42, 'J.W. Copes': 0.42, 'Jaketown': 0.40,
    'Claiborne': 0.30, 'Cedarland': 0.30,
}

EPS_PHEN = {  # phenology peak count rescaled to [0.10, 0.50]
    'Poverty Point': 0.50, 'Lower Jackson': 0.26, 'Watson Brake': 0.18,
    "Frenchman's Bend": 0.18, 'Caney': 0.18, 'Insley': 0.18,
    'Cowpen Slough': 0.26, 'J.W. Copes': 0.26, 'Jaketown': 0.34,
    'Claiborne': 0.18, 'Cedarland': 0.18,
}

EPS_WR = {  # water-route epsilon from S7.7 extension 6
    'Poverty Point': 0.154, 'Lower Jackson': 0.145, 'Watson Brake': 0.115,
    "Frenchman's Bend": 0.115, 'Caney': 0.070, 'Insley': 0.083,
    'Cowpen Slough': 0.068, 'J.W. Copes': 0.068, 'Jaketown': 0.151,
    'Claiborne': 0.050, 'Cedarland': 0.050,
}

ALPHA = 2.0
N_REF = 25


def joint_predicted_volume(eps_dict: dict, params: SimulationParameters):
    """Predicted volume per site under joint eps + n_agg + alpha=2 model."""
    pp_res = full_ct(epsilon=0.49, n_agg=25,
                     sig_params=params.signaling, net_params=params.network,
                     conf_params=params.conflict, agg_params=params.aggregation)
    base_m3_per_Mg = 750000.0 / pp_res['M_g']
    out = {}
    for name, n_agg, scale, obs in SITES:
        eps = max(0.05, eps_dict[name])  # min for the model
        r = full_ct(epsilon=eps, n_agg=n_agg,
                    sig_params=params.signaling, net_params=params.network,
                    conf_params=params.conflict, agg_params=params.aggregation)
        Mg = r['M_g']
        m3_per_Mg = base_m3_per_Mg * (n_agg / N_REF) ** ALPHA
        out[name] = Mg * m3_per_Mg
    return out


def main():
    params = SimulationParameters()

    # Extract per-site arrays in order
    n_agg = [s[1] for s in SITES]
    scale = [s[2] for s in SITES]
    vol = [s[3] for s in SITES]
    eps_st = [EPS_STATIC[s[0]] for s in SITES]
    eps_ph = [EPS_PHEN[s[0]] for s in SITES]
    eps_wr = [EPS_WR[s[0]] for s in SITES]

    # Joint predicted volumes under each epsilon
    pred_static = [joint_predicted_volume(EPS_STATIC, params)[s[0]] for s in SITES]
    pred_phen = [joint_predicted_volume(EPS_PHEN, params)[s[0]] for s in SITES]
    pred_wr = [joint_predicted_volume(EPS_WR, params)[s[0]] for s in SITES]

    # Spearman correlations
    print(f'{"Predictor":40s} {"vs ordinal":>14s} {"vs volume":>14s}')
    print('-' * 70)
    rows = []
    for name, x in [
        ('n_agg alone', n_agg),
        ('static epsilon alone', eps_st),
        ('phenology epsilon alone', eps_ph),
        ('water-route epsilon alone', eps_wr),
        ('joint M_g(static_eps, n_agg)', pred_static),
        ('joint M_g(phen_eps, n_agg)', pred_phen),
        ('joint M_g(water-route_eps, n_agg)', pred_wr),
    ]:
        r1, p1 = spearmanr(x, scale)
        r2, p2 = spearmanr(x, vol)
        print(f'{name:40s} {r1:+.3f} (p={p1:.3f}) {r2:+.3f} (p={p2:.3f})')
        rows.append({
            'predictor': name, 'rho_vs_ordinal_scale': float(r1),
            'p_vs_ordinal': float(p1),
            'rho_vs_volume': float(r2), 'p_vs_volume': float(p2),
        })

    # Marginal contribution: joint rho - n_agg-alone rho
    print()
    rho_n = spearmanr(n_agg, vol).statistic
    rho_joint_st = spearmanr(pred_static, vol).statistic
    rho_joint_ph = spearmanr(pred_phen, vol).statistic
    rho_joint_wr = spearmanr(pred_wr, vol).statistic
    print('Marginal contribution of epsilon to magnitude prediction:')
    print(f'  Joint with static eps   - n_agg alone = {rho_joint_st - rho_n:+.3f}')
    print(f'  Joint with phenology eps - n_agg alone = {rho_joint_ph - rho_n:+.3f}')
    print(f'  Joint with water-route eps - n_agg alone = {rho_joint_wr - rho_n:+.3f}')
    print()
    print('Interpretation: epsilon adds at most ~0.02 to the magnitude correlation')
    print('vs. n_agg alone. The framework\'s magnitude prediction is essentially')
    print('an n_agg ranking exercise; epsilon does not contribute substantively.')

    out_dir = Path('results/sensitivity')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'partial_correlation_eps_nagg.json'
    with open(out_file, 'w') as f:
        json.dump({
            'rows': rows,
            'marginal_contribution_eps': {
                'static': float(rho_joint_st - rho_n),
                'phenology': float(rho_joint_ph - rho_n),
                'water_route': float(rho_joint_wr - rho_n),
            },
            'interpretation': (
                'n_agg alone gives Spearman rho ~ +0.87 to +0.89 against '
                'observed monument scale and volume. Epsilon adds at most ~0.02 '
                'to the joint correlation. The framework\'s magnitude prediction '
                'is dominated by exogenous n_agg from the convergence-model '
                'literature; epsilon provides essentially no marginal predictive '
                'power for cross-site monument scale.'
            ),
        }, f, indent=2)
    print(f'\nWrote {out_file}')


if __name__ == '__main__':
    main()
