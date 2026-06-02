#!/usr/bin/env python3
"""Figure S04: Factorial channel ablation.

R3 #9 requested ablating each signaling/buffering channel (λ_W, λ_C,
λ_X, ε) individually and in factorial combination. 16 cells × 8
replicates at sigma_eff_target = 0.40 (just above the analytical
threshold). Visualizes:

  (A) Per-cell mean dominance ± SD, sorted by mean, with cell labels
      indicating which channels are on (uppercase) vs off (lowercase).
  (B) Main effects: average dominance with channel ON minus OFF, for
      each of the four channels.

Input: results/ablation/factorial_channel_ablation_*.json (latest)
Output: figures/supplemental/figure_S04_factorial_ablation.{png,pdf}
"""
import json
import glob
from pathlib import Path
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = Path('/Users/clipo/PycharmProjects/poverty-point')
OUTPUT_DIR = PROJECT_ROOT / 'figures' / 'supplemental'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_latest():
    paths = sorted(glob.glob(str(PROJECT_ROOT / 'results' / 'ablation'
                                 / 'factorial_channel_ablation_2*.json')))
    if not paths:
        raise SystemExit('no factorial_channel_ablation_*.json found')
    with open(paths[-1]) as f:
        return json.load(f), paths[-1]


def cell_label(W, C, X, E):
    return ('W' if W else 'w') + ('C' if C else 'c') \
         + ('X' if X else 'x') + ('E' if E else 'e')


def main():
    data, fname = load_latest()
    print(f'Loaded {fname}, n records = {len(data)}')

    cells = defaultdict(list)
    for r in data:
        cells[(r['W'], r['C'], r['X'], r['E'])].append(r['dominance'])

    rows = []
    for key, doms in cells.items():
        W, C, X, E = key
        rows.append({
            'key': key, 'label': cell_label(*key),
            'mean': float(np.mean(doms)),
            'sd': float(np.std(doms, ddof=1)),
            'n_on': sum(key),
        })
    rows.sort(key=lambda r: r['mean'])

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 10
    fig, (ax_cells, ax_main) = plt.subplots(1, 2, figsize=(13, 5.5),
                                            gridspec_kw={'width_ratios': [2.2, 1.0]})

    # Panel A: per-cell mean dominance with error bars
    labels = [r['label'] for r in rows]
    means = [r['mean'] for r in rows]
    sds = [r['sd'] for r in rows]
    # Color by ε state: ON in orange, OFF in blue
    colors = ['#E69F00' if r['key'][3] else '#56B4E9' for r in rows]
    y_pos = np.arange(len(rows))
    ax_cells.barh(y_pos, means, xerr=sds, color=colors,
                  edgecolor='black', linewidth=0.7, capsize=3)
    ax_cells.set_yticks(y_pos)
    ax_cells.set_yticklabels(labels, fontsize=9, family='monospace')
    ax_cells.axvline(0, color='black', linewidth=0.8)
    ax_cells.set_xlabel('Strategy dominance (mean ± 1 SD, n=8 replicates)',
                        fontsize=10)
    ax_cells.set_title(r'(A) Factorial channel ablation: per-cell dominance',
                       fontsize=11, loc='left')
    ax_cells.set_xlim(-1.0, 1.0)
    ax_cells.grid(True, axis='x', alpha=0.3)
    # Legend for color
    from matplotlib.patches import Patch
    leg = [Patch(color='#E69F00', label=r'$\varepsilon$ ON'),
           Patch(color='#56B4E9', label=r'$\varepsilon$ OFF')]
    ax_cells.legend(handles=leg, loc='lower right', fontsize=9)
    # Annotate channel-on count
    for i, r in enumerate(rows):
        ax_cells.text(0.98 * np.sign(r['mean']) if r['mean'] != 0 else 0.02,
                      i, f"{r['n_on']}/4 on",
                      ha='right' if r['mean'] > 0 else 'left',
                      va='center', fontsize=7, color='#555555')

    # Panel B: main effects
    main_effects = {}
    channels = ['W', 'C', 'X', 'E']
    for idx, ch in enumerate(channels):
        on = np.mean([r['mean'] for r in rows if r['key'][idx]])
        off = np.mean([r['mean'] for r in rows if not r['key'][idx]])
        main_effects[ch] = on - off
    ch_labels = {
        'W': r'$\lambda_W$' + '\n(within-group)',
        'C': r'$\lambda_C$' + '\n(conflict)',
        'X': r'$\lambda_X$' + '\n(network)',
        'E': r'$\varepsilon$' + '\n(ecotone)',
    }
    x = np.arange(len(channels))
    vals = [main_effects[ch] for ch in channels]
    colors_main = ['#0072B2' if v >= 0 else '#D55E00' for v in vals]
    ax_main.bar(x, vals, color=colors_main, edgecolor='black', linewidth=0.8)
    ax_main.axhline(0, color='black', linewidth=0.7)
    ax_main.set_xticks(x)
    ax_main.set_xticklabels([ch_labels[c] for c in channels], fontsize=9)
    ax_main.set_ylabel('Main effect on strategy dominance\n(channel ON minus OFF)',
                       fontsize=10)
    ax_main.set_title('(B) Main effects', fontsize=11, loc='left')
    ax_main.grid(True, axis='y', alpha=0.3)
    for xi, v in zip(x, vals):
        ax_main.text(xi, v + (0.04 if v >= 0 else -0.04),
                     f'{v:+.3f}', ha='center',
                     va='bottom' if v >= 0 else 'top', fontsize=9,
                     fontweight='bold')
    ax_main.set_ylim(-0.2, 1.1)

    plt.tight_layout()
    out_png = OUTPUT_DIR / 'figure_S04_factorial_ablation.png'
    out_pdf = OUTPUT_DIR / 'figure_S04_factorial_ablation.pdf'
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.savefig(out_pdf, bbox_inches='tight')
    print(f'Saved: {out_png}')
    print(f'Saved: {out_pdf}')

    # Print summary
    print('\nPer-cell means (sorted):')
    for r in rows:
        print(f"  {r['label']:>4s}  ({r['n_on']}/4 on)  mean={r['mean']:+.4f}  sd={r['sd']:.4f}")
    print('\nMain effects (mean dom with channel ON minus OFF):')
    for ch in channels:
        print(f"  {ch} ({ch_labels[ch].split(chr(10))[1].strip('()')}): {main_effects[ch]:+.4f}")


if __name__ == '__main__':
    main()
