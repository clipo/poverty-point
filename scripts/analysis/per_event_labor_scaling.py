"""
Extension 2: Per-event labor scaling for predicted volumes.

Previously: a single 77 m^3-per-investment-unit calibration was applied
uniformly to all LMV sites in extension (7). This systematically
overpredicted small-n_agg sites (10x or more) because PP's mass
mobilization (1,000-3,000 laborers per Mound A; Ortmann and Kidder 2013)
produces more m^3 per crew-day than a small-band gathering at WB or
Lower Jackson would.

This script implements a per-event labor-scaling factor that varies the
m^3-per-investment-unit conversion with attained n_agg. The simplest
defensible form:

    m3_per_unit(n_agg) = base * (n_agg / N_AGG_REF)^alpha

where N_AGG_REF = 25 (PP), and alpha encodes how strongly per-crew
output scales with crew size. alpha = 1 means linear scaling (small
crews produce proportionally less); alpha = 0 means no scaling (the
old uniform 77 m^3/unit calibration); alpha around 1-2 captures the
empirical observation that mass mobilization is more efficient because
of coordinated basket-loading and shorter-radius spoil hauling.

We sweep alpha and report which value best predicts observed volumes
across the LMV sites.

Output: results/sensitivity/per_event_labor_scaling.json
"""
from pathlib import Path
import json
import sys

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from poverty_point.parameters import SimulationParameters
from poverty_point.signaling_core import critical_threshold as full_ct


SITES = [
    # name, eps, n_agg, sigma, observed_volume_m3, observed_scale_ordinal
    ('Poverty Point',    0.49, 25, 0.64, 750000, 3),
    ('Lower Jackson',    0.48,  1, 0.56,   1000, 0),
    ('Watson Brake',     0.43,  8, 0.56,   7000, 2),
    ('Caney',            0.43,  5, 0.56,   5000, 2),
    ("Frenchman's Bend", 0.43,  5, 0.56,   2000, 1),
    ('Insley',           0.43,  6, 0.56,  14000, 2),
    ('J.W. Copes',       0.42,  3, 0.64,    500, 0),
    ('Cowpen Slough',    0.42,  3, 0.64,    500, 0),
    ('Jaketown',         0.40,  8, 0.64,   5000, 1),
    ('Claiborne',        0.30,  4, 0.64,   3000, 1),
    ('Cedarland',        0.30,  4, 0.64,   1000, 1),
]
N_AGG_REF = 25


def predict_volumes(alpha: float, params: SimulationParameters):
    """Compute predicted volumes under per-event labor scaling exponent alpha.

    The base m^3-per-M_g calibration is set so that PP at alpha=alpha
    still equals 750,000 m^3.
    """
    pp_eps, pp_n, pp_sigma = 0.49, 25, 0.64
    pp_res = full_ct(epsilon=pp_eps, n_agg=pp_n,
                     sig_params=params.signaling, net_params=params.network,
                     conf_params=params.conflict, agg_params=params.aggregation)
    Mg_pp = pp_res['M_g']
    # Scale factor: PP_Mg * (n=25/n=25)^alpha * base = 750000
    # => base = 750000 / (Mg_pp * 1) since (25/25)^alpha = 1
    base_m3_per_Mg = 750000.0 / Mg_pp

    rows = []
    for name, eps, n, sigma, obs_vol, scale in SITES:
        r = full_ct(epsilon=eps, n_agg=n,
                    sig_params=params.signaling, net_params=params.network,
                    conf_params=params.conflict, agg_params=params.aggregation)
        Mg = r['M_g']
        m3_per_Mg = base_m3_per_Mg * (n / N_AGG_REF) ** alpha
        pred_vol = Mg * m3_per_Mg
        rows.append({
            'name': name, 'n_agg': n, 'eps': eps, 'M_g': Mg,
            'm3_per_Mg': m3_per_Mg, 'predicted_volume_m3': pred_vol,
            'observed_volume_m3': obs_vol, 'observed_scale': scale,
            'log_overpred': np.log10(pred_vol / obs_vol) if obs_vol > 0 else np.nan,
        })
    return rows, base_m3_per_Mg


def main():
    params = SimulationParameters()

    # Sweep alpha from 0 (no scaling) to 2.5
    alphas = [0.0, 0.5, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5]

    print(f'{"alpha":>6s} {"mean log10(pred/obs)":>22s} {"std log":>10s} '
          f'{"rho_vol":>10s} {"p_vol":>8s} {"rho_scale":>10s} {"p_scale":>8s}')
    print('-' * 80)

    sweep_rows = []
    best_alpha = None
    best_meanlog = float('inf')

    for alpha in alphas:
        rows, base = predict_volumes(alpha, params)
        log_overs = np.array([r['log_overpred'] for r in rows
                              if r['observed_volume_m3'] > 0])
        mean_log = float(np.mean(log_overs))
        std_log = float(np.std(log_overs, ddof=1))

        pred = np.array([r['predicted_volume_m3'] for r in rows])
        obs_vol = np.array([r['observed_volume_m3'] for r in rows])
        obs_sc = np.array([r['observed_scale'] for r in rows])

        rho_vol, p_vol = spearmanr(pred, obs_vol)
        rho_sc, p_sc = spearmanr(pred, obs_sc)

        if abs(mean_log) < best_meanlog:
            best_meanlog = abs(mean_log)
            best_alpha = alpha

        print(f'{alpha:6.2f} {mean_log:22.3f} {std_log:10.3f} '
              f'{rho_vol:10.3f} {p_vol:8.3f} {rho_sc:10.3f} {p_sc:8.3f}')

        sweep_rows.append({
            'alpha': alpha,
            'rows': rows,
            'mean_log_overpred': mean_log,
            'std_log_overpred': std_log,
            'spearman_rho_volume': float(rho_vol),
            'spearman_p_volume': float(p_vol),
            'spearman_rho_scale': float(rho_sc),
            'spearman_p_scale': float(p_sc),
        })

    print()
    print(f'Best-calibrated alpha (mean log10 closest to 0): alpha = {best_alpha}')

    out_dir = Path('results/sensitivity')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'per_event_labor_scaling.json'
    with open(out_file, 'w') as f:
        json.dump({
            'sweep': sweep_rows,
            'best_alpha': best_alpha,
            'N_AGG_REF': N_AGG_REF,
        }, f, indent=2)
    print(f'Wrote {out_file}')


if __name__ == '__main__':
    main()
