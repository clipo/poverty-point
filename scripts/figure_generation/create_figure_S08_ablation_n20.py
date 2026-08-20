#!/usr/bin/env python3
"""Figure 7: Phase transition validation with n=20 ablation data.

Re-creates Figure 7 from the round-6 ablation pad output (n=20 replicates
per cell in both signal-conditional and random-partner modes). The
manuscript previously had a 4-panel Figure 7 sourced from a separate
sweep dataset; this script produces a focused 4-panel version sourced
from the canonical ablation pad data:

  (A) Strategy dominance vs σ_eff for both modes with replicate envelope
  (B) Realized σ_eff vs target σ_eff (sweep diagnostic)
  (C) Per-cell dominance difference (random − signal) with ±1 SD
  (D) Crossover detail (zoomed view near the threshold)

Input: results/ablation/ablation_sweep_engine2.json (n=20 per cell)
Output: figures/supplemental/figure_S08_ablation_n20.{png,pdf}
"""
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

PROJECT_ROOT = Path('/Users/clipo/PycharmProjects/poverty-point')
OUTPUT_DIR = PROJECT_ROOT / 'figures' / 'supplemental'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SIGMA_STAR_ANALYTICAL = 0.40


def main():
    with open(PROJECT_ROOT / 'results' / 'ablation' / 'ablation_sweep_engine2.json') as f:
        data = json.load(f)
    sigma_targets = data['sigma_effs']

    sig_means, sig_sds = [], []
    rand_means, rand_sds = [], []
    sig_sigma, rand_sigma = [], []
    for se in sigma_targets:
        sig_doms = data['mode_signal'][str(se)]
        rand_doms = data['mode_random'][str(se)]
        sig_means.append(np.mean(sig_doms))
        sig_sds.append(np.std(sig_doms, ddof=1))
        rand_means.append(np.mean(rand_doms))
        rand_sds.append(np.std(rand_doms, ddof=1))
        sig_sigma.append(np.mean(data['realized_sigma_signal'][str(se)]))
        rand_sigma.append(np.mean(data['realized_sigma_random'][str(se)]))

    sig_means = np.array(sig_means)
    sig_sds = np.array(sig_sds)
    rand_means = np.array(rand_means)
    rand_sds = np.array(rand_sds)
    sig_sigma = np.array(sig_sigma)
    rand_sigma = np.array(rand_sigma)
    sigma_targets = np.array(sigma_targets)

    # Find crossovers by linear interpolation
    def crossover(x, y):
        for i in range(len(y) - 1):
            if y[i] < 0 and y[i + 1] > 0:
                return x[i] + (0 - y[i]) / (y[i + 1] - y[i]) * (x[i + 1] - x[i])
        return None

    sig_cross = crossover(sig_sigma, sig_means)
    rand_cross = crossover(rand_sigma, rand_means)

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 10
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # ── Panel A: strategy dominance vs σ_eff for both modes ──
    ax = axes[0, 0]
    ax.fill_between(sig_sigma, sig_means - sig_sds, sig_means + sig_sds,
                    color='#0072B2', alpha=0.18, label=None)
    ax.plot(sig_sigma, sig_means, marker='o', color='#0072B2',
            linewidth=2.0, markersize=7, label='Signal-conditional')
    ax.fill_between(rand_sigma, rand_means - rand_sds, rand_means + rand_sds,
                    color='#E69F00', alpha=0.18, label=None)
    ax.plot(rand_sigma, rand_means, marker='s', color='#E69F00',
            linewidth=2.0, markersize=7, label='Random-partner')
    ax.axhline(0, color='black', linewidth=0.7, linestyle='--', alpha=0.5)
    ax.axvline(SIGMA_STAR_ANALYTICAL, color='red', linewidth=1.2, linestyle=':',
               label=f'Analytical σ* = {SIGMA_STAR_ANALYTICAL}')
    if sig_cross is not None:
        ax.axvline(sig_cross, color='#0072B2', linewidth=0.8, linestyle='--',
                   alpha=0.6)
    if rand_cross is not None:
        ax.axvline(rand_cross, color='#E69F00', linewidth=0.8, linestyle='--',
                   alpha=0.6)
    ax.set_xlabel(r'Realized $\sigma_{eff}$ (raw-σ scale; see §S1.4)', fontsize=10)
    ax.set_ylabel('Strategy dominance\n(−1 = all independent, +1 = all aggregator)',
                  fontsize=10)
    ax.set_title('(A) Phase transition: signal-conditional vs random-partner',
                 fontsize=11, loc='left')
    ax.set_ylim(-1.0, 1.0)
    ax.legend(loc='lower right', fontsize=9, framealpha=0.92)
    ax.grid(True, alpha=0.3)
    # Annotate crossovers
    if sig_cross is not None and rand_cross is not None:
        ax.text(sig_cross + 0.01, -0.85,
                f'signal σ_eff* = {sig_cross:.3f}', fontsize=8,
                color='#0072B2', rotation=0)
        ax.text(rand_cross - 0.05, -0.95,
                f'random σ_eff* = {rand_cross:.3f}', fontsize=8,
                color='#E69F00', rotation=0)

    # ── Panel B: realized σ_eff vs target σ_eff ──
    ax = axes[0, 1]
    ax.plot(sigma_targets, sig_sigma, marker='o', color='#0072B2',
            linewidth=2.0, markersize=7, label='Signal-conditional')
    ax.plot(sigma_targets, rand_sigma, marker='s', color='#E69F00',
            linewidth=2.0, markersize=7, label='Random-partner', linestyle='--')
    ax.plot([0, 1], [0, 1], color='black', linewidth=0.6, linestyle=':',
            label='1:1 line')
    ax.set_xlabel(r'Target $\sigma_{eff}$', fontsize=10)
    ax.set_ylabel(r'Realized $\sigma_{eff}$', fontsize=10)
    ax.set_title('(B) Realized σ_eff vs target (sweep diagnostic)',
                 fontsize=11, loc='left')
    ax.set_xlim(0.15, 0.6)
    ax.set_ylim(0.2, 0.9)
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)

    # ── Panel C: per-cell dominance difference (random − signal) ──
    ax = axes[1, 0]
    diffs = rand_means - sig_means
    # Combined SD using pooled SE
    diff_sds = np.sqrt(sig_sds**2 + rand_sds**2) / np.sqrt(20)
    ax.bar(sig_sigma, diffs, width=0.04, yerr=diff_sds,
           color=['#D55E00' if d < 0 else '#0072B2' for d in diffs],
           edgecolor='black', linewidth=0.7, capsize=4)
    ax.axhline(0, color='black', linewidth=0.7)
    ax.axvline(SIGMA_STAR_ANALYTICAL, color='red', linewidth=1.2, linestyle=':',
               label=f'Analytical σ* = {SIGMA_STAR_ANALYTICAL}')
    ax.set_xlabel(r'Realized $\sigma_{eff}$', fontsize=10)
    ax.set_ylabel('Dominance difference (random − signal)\nwith ±1 SE',
                  fontsize=10)
    ax.set_title('(C) Per-cell ablation difference (n=20 each)',
                 fontsize=11, loc='left')
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, axis='y', alpha=0.3)

    # ── Panel D: crossover detail (zoomed near threshold) ──
    ax = axes[1, 1]
    # Mask for near-threshold cells
    near_mask = (sig_sigma > 0.3) & (sig_sigma < 0.7)
    ax.fill_between(sig_sigma[near_mask],
                    sig_means[near_mask] - sig_sds[near_mask],
                    sig_means[near_mask] + sig_sds[near_mask],
                    color='#0072B2', alpha=0.20)
    ax.plot(sig_sigma[near_mask], sig_means[near_mask],
            marker='o', color='#0072B2', linewidth=2.2, markersize=8,
            label='Signal-conditional')
    ax.fill_between(rand_sigma[near_mask],
                    rand_means[near_mask] - rand_sds[near_mask],
                    rand_means[near_mask] + rand_sds[near_mask],
                    color='#E69F00', alpha=0.20)
    ax.plot(rand_sigma[near_mask], rand_means[near_mask],
            marker='s', color='#E69F00', linewidth=2.2, markersize=8,
            label='Random-partner')
    ax.axhline(0, color='black', linewidth=0.7, linestyle='--', alpha=0.5)
    ax.axvline(SIGMA_STAR_ANALYTICAL, color='red', linewidth=1.5, linestyle=':',
               label=f'Analytical σ* = {SIGMA_STAR_ANALYTICAL}')
    if sig_cross is not None:
        ax.axvline(sig_cross, color='#0072B2', linewidth=1.2, linestyle='--',
                   label=f'Signal σ_eff* = {sig_cross:.3f}')
    if rand_cross is not None:
        ax.axvline(rand_cross, color='#E69F00', linewidth=1.2, linestyle='--',
                   label=f'Random σ_eff* = {rand_cross:.3f}')
    ax.set_xlabel(r'Realized $\sigma_{eff}$', fontsize=10)
    ax.set_ylabel('Strategy dominance', fontsize=10)
    ax.set_title('(D) Crossover detail (near-threshold zoom)',
                 fontsize=11, loc='left')
    ax.legend(loc='lower right', fontsize=9, framealpha=0.92)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    out_png = OUTPUT_DIR / 'figure_S08_ablation_n20.png'
    out_pdf = OUTPUT_DIR / 'figure_S08_ablation_n20.pdf'
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.savefig(out_pdf, bbox_inches='tight')
    print(f'Saved: {out_png}')
    print(f'Saved: {out_pdf}')
    print(f'Crossovers: signal {sig_cross:.4f}, random {rand_cross:.4f}, '
          f'shift {rand_cross - sig_cross:+.4f}')


if __name__ == '__main__':
    main()
