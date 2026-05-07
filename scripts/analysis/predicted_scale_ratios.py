"""
Extension 7: Predicted equilibrium monument-scale ratios per LMV site.

For each of the eleven LMV sites in Table 1, compute analytical
equilibrium M_g using site-specific (epsilon, n_agg, sigma) and convert
to predicted earthwork volume via the PP-fit calibration ($M_{g,PP} \to
750{,}000$ m^3). Compare predicted volumes with observed ordinal scale
to test whether the framework's equilibrium prediction tracks the
qualitative LMV magnitude hierarchy when n_agg is allowed to vary
per-site.

Inputs combine three operationalizations of epsilon:
  - Static rubric (Table 1)
  - Phenology peak count (S7.6, Test A)
  - Bayesian midpoint of GIS-mixture estimates (placeholder; would
    use water-route catchment if implemented per priority extension #6)

Per-site n_agg is set from the convergence-model literature (Grooms et
al. 2023; Kidder and Grooms 2024) for Jaketown and PP, with
small-n_agg (5-8) defaults for other sites consistent with footprint
scale.

Output: results/sensitivity/predicted_scale_ratios.json
"""
from pathlib import Path
import json
import sys

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from poverty_point.parameters import SimulationParameters, critical_threshold
from poverty_point.signaling_core import critical_threshold as full_ct


# Site parameters (per Table 1 and §5.1)
# (name, eps_static, eps_phen_peaks, n_agg, sigma_regional, observed_scale_ordinal,
#  observed_volume_m3 (rough estimate or None))
SITES = [
    ('Poverty Point',    0.49, 5, 25, 0.64, 3, 750000),  # very large
    ('Lower Jackson',    0.48, 2, 1, 0.56, 0, 1000),  # minimal: single mound
    ('Watson Brake',     0.43, 1, 8, 0.56, 2, 7000),  # mid: ~7k m^3
    ('Caney',            0.43, 1, 5, 0.56, 2, 5000),  # mid (estimated)
    ("Frenchman's Bend", 0.43, 1, 5, 0.56, 1, 2000),  # small (estimated)
    ('Insley',           0.43, 1, 6, 0.56, 2, 14000),  # mid: 2x WB per Sassaman 2005
    ('J.W. Copes',       0.42, 2, 3, 0.64, 0, 500),  # minimal
    ('Cowpen Slough',    0.42, 2, 3, 0.64, 0, 500),  # minimal
    ('Jaketown',         0.40, 3, 8, 0.64, 1, 5000),  # small (1 PP-period mound)
    ('Claiborne',        0.30, 1, 4, 0.64, 1, 3000),  # shell ring (rough estimate)
    ('Cedarland',        0.30, 1, 4, 0.64, 1, 1000),  # smaller paired
]

EPS_MIN_PHEN = 0.10
EPS_MAX_PHEN = 0.50
PEAK_MAX = 5
M3_PER_MG_PP = None  # computed at runtime from PP equilibrium


def phen_eps(peaks: int) -> float:
    return EPS_MIN_PHEN + (peaks / PEAK_MAX) * (EPS_MAX_PHEN - EPS_MIN_PHEN)


def main():
    params = SimulationParameters()

    # First pass: compute PP equilibrium to set the global m^3-per-M_g calibration
    pp_static = full_ct(epsilon=0.49, n_agg=25,
                        sig_params=params.signaling, net_params=params.network,
                        conf_params=params.conflict, agg_params=params.aggregation)
    M_g_PP = pp_static['M_g']
    m3_per_Mg = 750000.0 / M_g_PP
    print(f'Calibration: PP M_g = {M_g_PP:.2f} ↔ 750,000 m^3, '
          f'so {m3_per_Mg:.1f} m^3 per M_g unit')
    print()

    rows = []
    for name, eps_static, peaks, n_agg, sigma, scale, obs_vol in SITES:
        eps_phen = phen_eps(peaks)

        # Equilibrium with static eps
        r_static = full_ct(epsilon=eps_static, n_agg=n_agg,
                           sig_params=params.signaling, net_params=params.network,
                           conf_params=params.conflict, agg_params=params.aggregation)
        Mg_static = r_static['M_g']
        ss_static = r_static['sigma_star']

        # Equilibrium with phenology eps
        r_phen = full_ct(epsilon=eps_phen, n_agg=n_agg,
                         sig_params=params.signaling, net_params=params.network,
                         conf_params=params.conflict, agg_params=params.aggregation)
        Mg_phen = r_phen['M_g']
        ss_phen = r_phen['sigma_star']

        pred_vol_static = Mg_static * m3_per_Mg
        pred_vol_phen = Mg_phen * m3_per_Mg

        # Margin = sigma - sigma_star (positive = above threshold)
        margin_static = sigma - ss_static
        margin_phen = sigma - ss_phen

        rows.append({
            'name': name,
            'eps_static': eps_static,
            'eps_phen': eps_phen,
            'phen_peaks': peaks,
            'n_agg': n_agg,
            'sigma_regional': sigma,
            'sigma_star_static': ss_static,
            'sigma_star_phen': ss_phen,
            'margin_static': margin_static,
            'margin_phen': margin_phen,
            'M_g_static': Mg_static,
            'M_g_phen': Mg_phen,
            'predicted_volume_static_m3': pred_vol_static,
            'predicted_volume_phen_m3': pred_vol_phen,
            'observed_scale_ordinal': scale,
            'observed_volume_m3': obs_vol,
            'log_overpred_static': np.log10(pred_vol_static / obs_vol) if obs_vol > 0 else np.nan,
            'log_overpred_phen': np.log10(pred_vol_phen / obs_vol) if obs_vol > 0 else np.nan,
        })

    print(f'{"Site":22s} {"n_agg":>6s} {"eps_st":>7s} {"M_g_st":>7s} '
          f'{"pred_st(m3)":>12s} {"obs_m3":>8s} {"log10(p/o)":>10s} {"scale":>6s}')
    print('-' * 95)
    for r in rows:
        log_str = f'{r["log_overpred_static"]:+.2f}' if not np.isnan(r["log_overpred_static"]) else '  N/A'
        print(f'{r["name"]:22s} {r["n_agg"]:6d} {r["eps_static"]:7.3f} '
              f'{r["M_g_static"]:7.2f} {r["predicted_volume_static_m3"]:12,.0f} '
              f'{r["observed_volume_m3"]:8,d} {log_str:>10s} {r["observed_scale_ordinal"]:6d}')

    # Spearman: predicted volume (static) vs observed scale ordinal
    pred_static = [r['predicted_volume_static_m3'] for r in rows]
    pred_phen = [r['predicted_volume_phen_m3'] for r in rows]
    obs_scale = [r['observed_scale_ordinal'] for r in rows]
    obs_vol = [r['observed_volume_m3'] for r in rows]

    rho_pv_os, p_pv_os = spearmanr(pred_static, obs_scale)
    rho_pp_os, p_pp_os = spearmanr(pred_phen, obs_scale)
    rho_pv_ov, p_pv_ov = spearmanr(pred_static, obs_vol)
    rho_pp_ov, p_pp_ov = spearmanr(pred_phen, obs_vol)

    print()
    print('Spearman correlations:')
    print(f'  Pred static volume   vs observed ordinal scale: rho = {rho_pv_os:+.3f}, p = {p_pv_os:.3f}')
    print(f'  Pred phenology volume vs observed ordinal scale: rho = {rho_pp_os:+.3f}, p = {p_pp_os:.3f}')
    print(f'  Pred static volume   vs observed m3:              rho = {rho_pv_ov:+.3f}, p = {p_pv_ov:.3f}')
    print(f'  Pred phenology volume vs observed m3:             rho = {rho_pp_ov:+.3f}, p = {p_pp_ov:.3f}')

    out_dir = Path('results/sensitivity')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'predicted_scale_ratios.json'
    with open(out_file, 'w') as f:
        json.dump({
            'sites': rows,
            'PP_calibration_M_g': M_g_PP,
            'PP_calibration_volume_m3': 750000.0,
            'm3_per_M_g_unit': m3_per_Mg,
            'spearman': {
                'pred_static_vs_ordinal': {'rho': float(rho_pv_os), 'p': float(p_pv_os)},
                'pred_phen_vs_ordinal': {'rho': float(rho_pp_os), 'p': float(p_pp_os)},
                'pred_static_vs_volume': {'rho': float(rho_pv_ov), 'p': float(p_pv_ov)},
                'pred_phen_vs_volume': {'rho': float(rho_pp_ov), 'p': float(p_pp_ov)},
            },
        }, f, indent=2)
    print(f'\nWrote {out_file}')


if __name__ == '__main__':
    main()
