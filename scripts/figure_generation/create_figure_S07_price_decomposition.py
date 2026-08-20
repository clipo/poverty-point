#!/usr/bin/env python3
"""Figure S03: Empirical Price-equation decomposition.

Plots the between-cohort selection term S(t) = Cov(w_g, p_g)/w̄ and the
transmission residual across three σ scenarios (below-, near-, and above-
threshold), confirming that the MLS prediction holds in the ABM:

  - Above σ*: selection term is positive (aggregators reproduce better)
  - Below σ*: selection term is negative or near zero
  - Near σ*: selection term hovers near zero with high variance

Input: results/analysis/price_decomposition_*.json
Output: figures/supplemental/figure_S07_price_decomposition.{png,pdf}
"""
import json
import glob
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = Path('/Users/clipo/PycharmProjects/poverty-point')
OUTPUT_DIR = PROJECT_ROOT / 'figures' / 'supplemental'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BURN_IN = 50
SCENARIO_LABELS = {
    'low_sigma': r'$\sigma_{target} = 0.20$ (below $\sigma^*$)',
    'near_threshold': r'$\sigma_{target} = 0.40$ ($\sigma \approx \sigma^*$)',
    'pp_scenario': r'$\sigma_{target} = 0.64$ (above $\sigma^*$, PP scenario)',
}
SCENARIO_ORDER = ['low_sigma', 'near_threshold', 'pp_scenario']
SCENARIO_COLOR = {
    'low_sigma': '#56B4E9',
    'near_threshold': '#888888',
    'pp_scenario': '#E69F00',
}


def load_latest():
    files = sorted(glob.glob(str(PROJECT_ROOT / 'results' / 'analysis'
                                 / 'price_decomposition_*.json')))
    if not files:
        raise SystemExit('No price_decomposition_*.json found; run run_price_decomposition.py first.')
    with open(files[-1]) as f:
        return json.load(f), files[-1]


def aggregate_scenario(reps, key, post_burn_only=True):
    """Concatenate across replicates and return arrays."""
    all_years, all_vals = [], []
    for rep in reps:
        d = rep['decomposition']
        for y, v in zip(d['year'], d[key]):
            if post_burn_only and y < BURN_IN:
                continue
            if v is None or (isinstance(v, float) and not np.isfinite(v)):
                continue
            all_years.append(y)
            all_vals.append(v)
    return np.array(all_years), np.array(all_vals)


def main():
    data, fname = load_latest()
    print(f'Loaded {fname}')

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 10
    fig, axes = plt.subplots(1, 4, figsize=(17, 4.5), sharey=False)
    ax_S, ax_cum, ax_T, ax_bar = axes

    # Panel A: selection term S(t) per scenario, replicate-pooled trajectory
    for scen in SCENARIO_ORDER:
        reps = data[scen]['reps']
        years, S = aggregate_scenario(reps, 'selection', post_burn_only=False)
        # Bin years into 10-yr bins for trajectory plot
        if len(years):
            bins = np.arange(0, max(years) + 11, 10)
            inds = np.digitize(years, bins)
            mean_y = [years[inds == i].mean() if (inds == i).any() else np.nan
                      for i in range(1, len(bins))]
            mean_S = [S[inds == i].mean() if (inds == i).any() else np.nan
                      for i in range(1, len(bins))]
            sd_S = [S[inds == i].std(ddof=1) if (inds == i).sum() >= 2 else np.nan
                    for i in range(1, len(bins))]
            ax_S.errorbar(mean_y, mean_S, yerr=sd_S,
                          marker='o', markersize=4, capsize=2,
                          label=SCENARIO_LABELS[scen],
                          color=SCENARIO_COLOR[scen], alpha=0.85)
    ax_S.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.5)
    ax_S.axvline(BURN_IN, color='red', linewidth=0.8, linestyle=':', alpha=0.5)
    ax_S.text(BURN_IN + 2, ax_S.get_ylim()[1] * 0.92, 'burn-in', color='red',
              fontsize=8)
    ax_S.set_xlabel('Year', fontsize=10)
    ax_S.set_ylabel(r'Between-band-lineage selection $S(t) = Cov(w_g, p_g)/\bar{w}$',
                    fontsize=10)
    ax_S.set_title('(A) Short timescale: per-year $S(t)$',
                   fontsize=10, loc='left')
    ax_S.legend(fontsize=8, loc='best')
    ax_S.grid(True, alpha=0.3)

    # Panel B: cumulative S(t) integral from burn-in onward (long-timescale signal)
    for scen in SCENARIO_ORDER:
        reps = data[scen]['reps']
        # Per-rep cumulative sum of post-burn-in S(t)
        rep_cumulatives = []
        rep_years = None
        for rep in reps:
            d = rep['decomposition']
            ys = np.array(d.get('year', []))
            Ss = np.array(d.get('selection', []))
            mask = (ys >= BURN_IN) & np.isfinite(Ss)
            ys_post = ys[mask]
            Ss_post = Ss[mask]
            if len(Ss_post) == 0:
                continue
            cum = np.cumsum(Ss_post)
            if rep_years is None or len(ys_post) > len(rep_years):
                rep_years = ys_post
            rep_cumulatives.append(cum)
        if not rep_cumulatives or rep_years is None:
            continue
        # Align to common length (shortest rep)
        min_len = min(len(c) for c in rep_cumulatives)
        cum_mat = np.array([c[:min_len] for c in rep_cumulatives])
        years_plot = rep_years[:min_len]
        med = np.median(cum_mat, axis=0)
        lo = np.percentile(cum_mat, 10, axis=0)
        hi = np.percentile(cum_mat, 90, axis=0)
        ax_cum.fill_between(years_plot, lo, hi, alpha=0.20,
                            color=SCENARIO_COLOR[scen])
        ax_cum.plot(years_plot, med, color=SCENARIO_COLOR[scen],
                    linewidth=2.0, label=SCENARIO_LABELS[scen])
    ax_cum.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.5)
    ax_cum.set_xlabel('Year (post burn-in)', fontsize=10)
    ax_cum.set_ylabel(r'Cumulative $\sum S(t)$', fontsize=10)
    ax_cum.set_title(r'(B) Long timescale: cumulative $\sum S(t)$',
                     fontsize=10, loc='left')
    ax_cum.legend(fontsize=8, loc='best')
    ax_cum.grid(True, alpha=0.3)

    # Panel C: transmission term trajectory
    for scen in SCENARIO_ORDER:
        reps = data[scen]['reps']
        years, T = aggregate_scenario(reps, 'transmission', post_burn_only=False)
        if len(years):
            bins = np.arange(0, max(years) + 11, 10)
            inds = np.digitize(years, bins)
            mean_y = [years[inds == i].mean() if (inds == i).any() else np.nan
                      for i in range(1, len(bins))]
            mean_T = [T[inds == i].mean() if (inds == i).any() else np.nan
                      for i in range(1, len(bins))]
            sd_T = [T[inds == i].std(ddof=1) if (inds == i).sum() >= 2 else np.nan
                    for i in range(1, len(bins))]
            ax_T.errorbar(mean_y, mean_T, yerr=sd_T,
                          marker='s', markersize=4, capsize=2,
                          label=SCENARIO_LABELS[scen],
                          color=SCENARIO_COLOR[scen], alpha=0.85)
    ax_T.axhline(0, color='black', linewidth=0.8, linestyle='--', alpha=0.5)
    ax_T.axvline(BURN_IN, color='red', linewidth=0.8, linestyle=':', alpha=0.5)
    ax_T.set_xlabel('Year', fontsize=10)
    ax_T.set_ylabel(r'Transmission residual $\Delta\bar{p} - S(t)$', fontsize=10)
    ax_T.set_title('(C) Transmission residual per year',
                   fontsize=10, loc='left')
    ax_T.legend(fontsize=8, loc='best')
    ax_T.grid(True, alpha=0.3)

    # Panel C: post-burn-in mean ± SD per scenario, with within-aggregator cov
    x_pos = np.arange(len(SCENARIO_ORDER))
    width = 0.28
    sel_means, sel_sds = [], []
    trn_means, trn_sds = [], []
    wac_means, wac_sds = [], []
    for scen in SCENARIO_ORDER:
        reps = data[scen]['reps']
        _, S = aggregate_scenario(reps, 'selection')
        _, T = aggregate_scenario(reps, 'transmission')
        _, W = aggregate_scenario(reps, 'within_agg_cov')
        sel_means.append(S.mean() if len(S) else 0.0)
        sel_sds.append(S.std(ddof=1) if len(S) > 1 else 0.0)
        trn_means.append(T.mean() if len(T) else 0.0)
        trn_sds.append(T.std(ddof=1) if len(T) > 1 else 0.0)
        wac_means.append(W.mean() if len(W) else 0.0)
        wac_sds.append(W.std(ddof=1) if len(W) > 1 else 0.0)
    ax_bar.bar(x_pos - width, sel_means, width, yerr=sel_sds,
               label=r'Between-cohort $S$', color='#0072B2',
               edgecolor='black', linewidth=0.8, capsize=4)
    ax_bar.bar(x_pos, trn_means, width, yerr=trn_sds,
               label=r'Transmission $\Delta\bar{p} - S$', color='#D55E00',
               edgecolor='black', linewidth=0.8, capsize=4)
    ax_bar.bar(x_pos + width, wac_means, width, yerr=wac_sds,
               label=r'Within-agg $Cov(M, w)$', color='#009E73',
               edgecolor='black', linewidth=0.8, capsize=4)
    ax_bar.axhline(0, color='black', linewidth=0.6)
    ax_bar.set_xticks(x_pos)
    ax_bar.set_xticklabels(['below', 'near', 'above'], fontsize=10)
    ax_bar.set_xlabel(r'Scenario relative to $\sigma^*$', fontsize=10)
    ax_bar.set_ylabel('Post-burn-in mean ± SD', fontsize=10)
    ax_bar.set_title('(D) Post-burn-in summary across components',
                     fontsize=10, loc='left')
    ax_bar.legend(fontsize=8, loc='best')
    ax_bar.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    out_png = OUTPUT_DIR / 'figure_S07_price_decomposition.png'
    out_pdf = OUTPUT_DIR / 'figure_S07_price_decomposition.pdf'
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.savefig(out_pdf, bbox_inches='tight')
    print(f'Saved: {out_png}')
    print(f'Saved: {out_pdf}')

    # Numerical summary table
    print('\n=== Post-burn-in summary ===')
    print(f"{'scenario':>16s}  {'sigma':>6s}  {'S(mean)':>10s}  {'S(sd)':>10s}  "
          f"{'Trans(mean)':>12s}  {'Trans(sd)':>10s}  {'WithinCov':>10s}")
    for i, scen in enumerate(SCENARIO_ORDER):
        sig = data[scen]['sigma_target']
        print(f"{scen:>16s}  {sig:>6.2f}  {sel_means[i]:>+10.5f}  "
              f"{sel_sds[i]:>10.5f}  {trn_means[i]:>+12.5f}  "
              f"{trn_sds[i]:>10.5f}  {wac_means[i]:>+10.5f}")


if __name__ == '__main__':
    main()
