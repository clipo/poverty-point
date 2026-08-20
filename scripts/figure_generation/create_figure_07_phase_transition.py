"""Figure 7: phase-transition validation at the calibrated PP scenario.

Reads the n=20 signal-conditional ablation sweep
(results/ablation/ablation_sweep_engine2.json) and renders four panels:

  A. Strategy dominance vs realized sigma (signal-conditional mode),
     mean ± 1 SD across replicates, with the analytical threshold line.
  B. Mean aggregation size (bands per gathering) vs realized sigma.
  C. Final cumulative monument investment vs realized sigma.
  D. Joint signature: monument investment vs strategy dominance, with the
     post-threshold cluster shaded.

Output: figures/manuscript/figure_07_phase_transition.{png,pdf}
"""
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / 'src'))
from poverty_point.signaling_core import critical_threshold  # noqa: E402

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 9,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# Okabe-Ito
ORANGE = '#E69F00'
PURPLE = '#CC79A7'
BLUE = '#0072B2'
RED = '#D55E00'

SWEEP = PROJECT_ROOT / 'results' / 'ablation' / 'ablation_sweep_engine2.json'


def cell_stats(data, mode, aux_key):
    """Per-cell mean/SD keyed by target, ordered by realized sigma."""
    targets = sorted(data[f'mode_{mode}'].keys(), key=float)
    rows = []
    for t in targets:
        dom = np.array(data[f'mode_{mode}'][t], dtype=float)
        sig = np.array(data[f'realized_sigma_{mode}'][t], dtype=float)
        aux = np.array(data[f'{aux_key}_{mode}'].get(t, []), dtype=float)
        rows.append({
            'target': float(t),
            'sigma_mean': sig.mean(),
            'dom_mean': dom.mean(), 'dom_sd': dom.std(ddof=1),
            'aux_mean': aux.mean() if aux.size else np.nan,
            'aux_sd': aux.std(ddof=1) if aux.size > 1 else np.nan,
            'n': len(dom),
        })
    return sorted(rows, key=lambda r: r['sigma_mean'])


def main():
    with open(SWEEP) as f:
        data = json.load(f)

    agg = cell_stats(data, 'signal', 'agg_size')
    mon = cell_stats(data, 'signal', 'monument')

    sigma_star = critical_threshold(epsilon=0.35, n_agg=25)['sigma_star']

    fig, axes = plt.subplots(2, 2, figsize=(7, 6))

    # A: dominance S-curve
    ax = axes[0, 0]
    x = [r['sigma_mean'] for r in agg]
    y = [r['dom_mean'] for r in agg]
    ye = [r['dom_sd'] for r in agg]
    ax.errorbar(x, y, yerr=ye, marker='o', color=ORANGE, capsize=3,
                lw=1.5, ms=5)
    ax.axvline(sigma_star, color=RED, ls='--', lw=1.2)
    ax.axhline(0, color='#888888', lw=0.7)
    ax.set_xlabel(r'Realized $\sigma$')
    ax.set_ylabel('Strategy dominance')
    ax.set_ylim(-1.05, 1.05)
    ax.text(0.02, 0.95, 'A', transform=ax.transAxes, fontweight='bold')
    ax.text(sigma_star + 0.01, -0.9, r'$\sigma^*$', color=RED)

    # B: aggregation size
    ax = axes[0, 1]
    y = [r['aux_mean'] for r in agg]
    ye = [r['aux_sd'] for r in agg]
    ax.errorbar(x, y, yerr=ye, marker='s', color=BLUE, capsize=3,
                lw=1.5, ms=5)
    ax.axvline(sigma_star, color=RED, ls='--', lw=1.2)
    ax.set_xlabel(r'Realized $\sigma$')
    ax.set_ylabel('Mean aggregation size (bands)')
    ax.text(0.02, 0.95, 'B', transform=ax.transAxes, fontweight='bold')

    # C: monument accumulation
    ax = axes[1, 0]
    y = [r['aux_mean'] for r in mon]
    ye = [r['aux_sd'] for r in mon]
    ax.errorbar(x, y, yerr=ye, marker='^', color=PURPLE, capsize=3,
                lw=1.5, ms=5)
    ax.axvline(sigma_star, color=RED, ls='--', lw=1.2)
    ax.set_xlabel(r'Realized $\sigma$')
    ax.set_ylabel('Cumulative monument investment (units)')
    ax.text(0.02, 0.95, 'C', transform=ax.transAxes, fontweight='bold')

    # D: joint signature
    ax = axes[1, 1]
    for r_agg, r_mon in zip(agg, mon):
        above = r_agg['sigma_mean'] > sigma_star
        ax.scatter(r_agg['dom_mean'], r_mon['aux_mean'],
                   s=55, c=ORANGE if above else PURPLE,
                   edgecolors='black', linewidths=0.8, zorder=5)
    ax.axvspan(0, 1.05, color=ORANGE, alpha=0.08)
    ax.set_xlabel('Strategy dominance')
    ax.set_ylabel('Cumulative monument investment (units)')
    ax.set_xlim(-1.05, 1.05)
    ax.text(0.02, 0.95, 'D', transform=ax.transAxes, fontweight='bold')

    fig.tight_layout()
    out_dir = PROJECT_ROOT / 'figures' / 'manuscript'
    out_dir.mkdir(parents=True, exist_ok=True)
    for ext in ('png', 'pdf'):
        fig.savefig(out_dir / f'figure_07_phase_transition.{ext}', dpi=300)
    print(f"Wrote {out_dir}/figure_07_phase_transition.png|pdf")


if __name__ == '__main__':
    main()
