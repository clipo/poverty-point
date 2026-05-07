"""
Extension 8 (minimal): Monthly phenology-coupled aggregation timing.

Tests whether the framework's seasonality predictions match the
published archaeological record (Thomas and Campbell 1978; Jackson
1986: PP populations peak in fall and winter, tied to the nut-mast
harvest).

The §S7.6 phenology calendar gives five resource peaks across the
LMV interior:
  - Hardwood mast (HM): Sep-Nov
  - Spring fish spawn (SFS): Feb-May
  - Summer aquatic (SA): May-Aug
  - Falling-water aquatic (FWA): Aug-Oct
  - Migratory waterfowl (WF): Sep-Dec and Feb-Apr

This minimal extension simulates a within-year time step at PP
parameters where bands aggregate when expected monthly resource
access at the gathering site exceeds dispersed foraging by enough
to offset the aggregation cost. The output is the predicted monthly
aggregation share, which can then be tested against the
archaeological fall-winter peak claim.

Output: results/sensitivity/seasonal_aggregation_timing.json
"""
from pathlib import Path
import json
import sys
from dataclasses import replace

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from poverty_point.parameters import SimulationParameters
from poverty_point.signaling_core import critical_threshold as full_ct


# Resource peak windows from §S7.6 (mid-month indices Jan=1)
PEAKS = {
    'HM':  (9, 11),     # mast Sep-Nov
    'SFS': (2, 5),      # spring fish Feb-May
    'SA':  (5, 8),      # summer aquatic May-Aug
    'FWA': (8, 10),     # falling-water Aug-Oct
    'WF_fall':   (9, 12),  # waterfowl fall migration Sep-Dec
    'WF_spring': (2, 4),   # waterfowl spring migration Feb-Apr
}

# PP-scenario site access flags from §S7.6 (HM, SFS, SA, FWA, WF)
PP_FLAGS = {'HM': 1.0, 'SFS': 1.0, 'SA': 1.0, 'FWA': 1.0, 'WF': 1.0}


def monthly_resource_availability(site_flags: dict) -> np.ndarray:
    """Return a 12-vector of resource availability per month at the site.

    Sums access * peak indicator over all peak categories. Multiple
    peaks active in the same month sum into a higher availability.
    """
    avail = np.zeros(12)
    for peak_label, (start, end) in PEAKS.items():
        # Map waterfowl peaks to the WF flag
        if peak_label.startswith('WF'):
            f = site_flags.get('WF', 0.0)
        else:
            f = site_flags.get(peak_label, 0.0)
        for m in range(start, end + 1):
            avail[m - 1] += f
    return avail


def aggregation_share_per_month(site_flags: dict, sigma_eff: float,
                                aggregation_cost: float = 0.18) -> np.ndarray:
    """Predicted aggregation share per month under the framework.

    The framework's logic: bands aggregate when expected resource
    availability at the gathering exceeds dispersed foraging by enough
    to offset aggregation cost C_signal. Here we use a simplified
    decision rule: per month, share_aggregating(month) = sigmoid of
    (availability - cost_threshold) where cost_threshold parameterizes
    how much resource concentration is needed to trigger aggregation.

    The cost_threshold depends on sigma_eff: at higher sigma_eff,
    bands are more risk-averse and willing to aggregate at lower
    monthly availability.
    """
    avail = monthly_resource_availability(site_flags)
    # Sub-threshold: cost_threshold high; bands stay dispersed
    # Above threshold: cost_threshold lower; bands more willing to aggregate
    # Calibration: at sigma_eff = 0.40 (PP threshold), threshold = 0.5;
    # higher sigma_eff drops threshold linearly.
    cost_threshold = max(0.1, 0.5 - 0.5 * (sigma_eff - 0.40))
    # Sigmoid response
    score = avail - cost_threshold
    share = 1.0 / (1.0 + np.exp(-3.0 * score))
    return share


def main():
    params = SimulationParameters()
    eps_pp = 0.49
    n_agg = 25
    sigma_pp = 0.64
    sigma_eff = sigma_pp * (1.0 - eps_pp)  # ~ 0.326

    pp_avail = monthly_resource_availability(PP_FLAGS)
    pp_share = aggregation_share_per_month(PP_FLAGS, sigma_eff)

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    print('PP monthly resource availability and predicted aggregation share:')
    print(f'{"Month":>5s} {"avail":>7s} {"agg_share":>10s}')
    print('-' * 28)
    for i, m in enumerate(months):
        print(f'{m:>5s} {pp_avail[i]:7.2f} {pp_share[i]:10.3f}')

    # Identify peak months (top 3 in agg_share)
    top3_idx = np.argsort(pp_share)[-3:][::-1]
    top3_months = [months[i] for i in top3_idx]
    print()
    print(f'Top 3 predicted aggregation months: {top3_months}')

    # Test against published evidence: Thomas and Campbell (1978)
    # report fall (Sep-Nov) + winter (Dec-Feb) population peak at PP.
    fall_winter_idx = [8, 9, 10, 11, 0, 1]  # Sep-Feb (0-indexed)
    fall_winter_share = float(np.mean(pp_share[fall_winter_idx]))
    spring_summer_idx = [2, 3, 4, 5, 6, 7]  # Mar-Aug
    spring_summer_share = float(np.mean(pp_share[spring_summer_idx]))

    print()
    print(f'Fall-winter (Sep-Feb) mean aggregation share: {fall_winter_share:.3f}')
    print(f'Spring-summer (Mar-Aug) mean aggregation share: {spring_summer_share:.3f}')
    print(f'Fall-winter / Spring-summer ratio: {fall_winter_share / spring_summer_share:.2f}')
    if fall_winter_share > spring_summer_share:
        verdict = 'Predicted seasonal peak in fall-winter, consistent with Thomas and Campbell (1978).'
    else:
        verdict = 'Predicted seasonal peak NOT in fall-winter; framework prediction does not match published evidence.'
    print(verdict)

    out_dir = Path('results/sensitivity')
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'seasonal_aggregation_timing.json'
    with open(out_file, 'w') as f:
        json.dump({
            'parameters': {
                'eps_PP': eps_pp,
                'n_agg': n_agg,
                'sigma_PP': sigma_pp,
                'sigma_eff_PP': float(sigma_eff),
            },
            'monthly_resource_availability': pp_avail.tolist(),
            'monthly_aggregation_share': pp_share.tolist(),
            'months': months,
            'top3_predicted_aggregation_months': top3_months,
            'fall_winter_share': fall_winter_share,
            'spring_summer_share': spring_summer_share,
            'fw_vs_ss_ratio': float(fall_winter_share / spring_summer_share),
            'verdict': verdict,
            'archaeological_reference': (
                'Thomas and Campbell 1978; Jackson 1986: PP population '
                'peaks in fall and winter, tied to the nut-mast harvest.'
            ),
        }, f, indent=2)
    print(f'\nWrote {out_file}')


if __name__ == '__main__':
    main()
