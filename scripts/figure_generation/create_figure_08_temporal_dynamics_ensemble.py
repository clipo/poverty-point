#!/usr/bin/env python3
"""Figure 8: Temporal dynamics with replicate ensemble.

R3 #4 requested ensemble shading on the temporal-dynamics figure
(previously single-trajectory). Reads the 5-replicate ensemble produced
by `scripts/analysis/run_figure_8_ensemble.py` and plots:
  - Strategy dominance over 500 yr with replicate envelope
  - Monument level over 500 yr with replicate envelope
  - Aggregation size over 500 yr with replicate envelope
  - Shortfall years as light vertical bars

Input: results/analysis/figure_8_ensemble_*.json (latest)
Output: figures/manuscript/figure_08_temporal_dynamics.{png,pdf}
"""
import json
import glob
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = Path('/Users/clipo/PycharmProjects/poverty-point')
OUTPUT_DIR = PROJECT_ROOT / 'figures' / 'manuscript'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_latest_ensemble():
    files = sorted(glob.glob(str(PROJECT_ROOT / 'results' / 'analysis'
                                 / 'figure_8_ensemble_*.json')))
    if not files:
        raise SystemExit('No figure_8_ensemble_*.json found; run scripts/analysis/run_figure_8_ensemble.py first.')
    with open(files[-1]) as f:
        return json.load(f), files[-1]


def main():
    ensemble, fname = load_latest_ensemble()
    print(f'Loaded {fname}: {len(ensemble)} replicates')

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 10

    # Stack trajectories — assume all reps have same year length
    years = np.array(ensemble[0]['years'])
    dom = np.array([r['dominance'] for r in ensemble])
    mon = np.array([r['monument'] for r in ensemble])
    agg = np.array([r['agg_size'] for r in ensemble])
    short = np.array([r['shortfall'] for r in ensemble])

    # Median and percentile envelopes
    dom_med = np.median(dom, axis=0)
    dom_lo = np.percentile(dom, 10, axis=0)
    dom_hi = np.percentile(dom, 90, axis=0)

    mon_med = np.median(mon, axis=0)
    mon_lo = np.percentile(mon, 10, axis=0)
    mon_hi = np.percentile(mon, 90, axis=0)

    agg_med = np.median(agg, axis=0)
    agg_lo = np.percentile(agg, 10, axis=0)
    agg_hi = np.percentile(agg, 90, axis=0)

    # Fraction of replicates in shortfall, per year
    short_frac = short.mean(axis=0)

    fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True)
    ax_dom, ax_mon, ax_agg = axes

    # Strategy dominance
    for r in dom:
        ax_dom.plot(years, r, color='#888888', alpha=0.25, linewidth=0.6)
    ax_dom.fill_between(years, dom_lo, dom_hi, alpha=0.30, color='#0072B2',
                        label='10-90 percentile')
    ax_dom.plot(years, dom_med, color='#0072B2', linewidth=2.0, label='median')
    ax_dom.axhline(0, color='black', linewidth=0.6, linestyle='--', alpha=0.5)
    # Mark shortfall-heavy years
    for y, f in zip(years, short_frac):
        if f > 0.5:
            ax_dom.axvspan(y - 0.5, y + 0.5, color='#D55E00', alpha=0.08)
    ax_dom.set_ylabel('Strategy dominance\n(aggregator - independent)',
                      fontsize=10)
    ax_dom.set_title('(A) Strategy dominance — Poverty Point scenario (5-replicate ensemble)',
                     fontsize=11, loc='left', pad=4)
    ax_dom.legend(fontsize=9, loc='lower right')
    ax_dom.grid(True, alpha=0.3)

    # Monument level
    for r in mon:
        ax_mon.plot(years, r, color='#888888', alpha=0.25, linewidth=0.6)
    ax_mon.fill_between(years, mon_lo, mon_hi, alpha=0.30, color='#009E73',
                        label='10-90 percentile')
    ax_mon.plot(years, mon_med, color='#009E73', linewidth=2.0, label='median')
    ax_mon.set_ylabel('Cumulative monument\ninvestment (units)',
                      fontsize=10)
    ax_mon.set_title('(B) Cumulative monument investment (5-replicate ensemble)',
                     fontsize=11, loc='left', pad=4)
    ax_mon.legend(fontsize=9, loc='lower right')
    ax_mon.grid(True, alpha=0.3)

    # Aggregation size
    for r in agg:
        ax_agg.plot(years, r, color='#888888', alpha=0.25, linewidth=0.6)
    ax_agg.fill_between(years, agg_lo, agg_hi, alpha=0.30, color='#E69F00',
                        label='10-90 percentile')
    ax_agg.plot(years, agg_med, color='#E69F00', linewidth=2.0, label='median')
    ax_agg.set_ylabel('Aggregation size\n(bands per gathering)',
                      fontsize=10)
    ax_agg.set_xlabel('Simulated year', fontsize=10)
    ax_agg.set_title('(C) Aggregation size (5-replicate ensemble)',
                     fontsize=11, loc='left', pad=4)
    ax_agg.legend(fontsize=9, loc='lower right')
    ax_agg.grid(True, alpha=0.3)

    plt.tight_layout()
    out_png = OUTPUT_DIR / 'figure_08_temporal_dynamics.png'
    out_pdf = OUTPUT_DIR / 'figure_08_temporal_dynamics.pdf'
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.savefig(out_pdf, bbox_inches='tight')
    print(f'Saved: {out_png}')
    print(f'Saved: {out_pdf}')

    # Summary statistics
    print('\nFinal values per replicate (year', int(years[-1]), '):')
    for i, r in enumerate(ensemble):
        print(f"  rep {r['rep']} (seed={r['seed']}): "
              f"dominance={r['dominance'][-1]:+.3f}, "
              f"monument={r['monument'][-1]:.0f}, "
              f"agg_size={r['agg_size'][-1]:.1f}")
    print(f"\nPost-burn-in (year>=100) median dominance:")
    post = years >= 100
    print(f"  median across reps: {np.median(dom[:, post]):+.3f}")
    print(f"  10/90 percentile: {np.percentile(dom[:, post], 10):+.3f} to "
          f"{np.percentile(dom[:, post], 90):+.3f}")


if __name__ == '__main__':
    main()
