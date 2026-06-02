#!/usr/bin/env python3
"""Figure 9: joint (sigma, epsilon) phase space, n=5 replicates per cell.

Reviewer R3 (round 6) asked for replicate spread on the phase space; the
original figure was n=1 per cell. This script reads the replicated run
(scripts/analysis/run_phase_space_replicated.py, 12x10 grid x 5 reps) and
produces a 3-panel figure:

  A) mean strategy dominance across (sigma, epsilon), sigma* line overlaid
  B) mean monument investment across (sigma, epsilon)
  C) per-cell standard deviation of strategy dominance across the 5 reps
     (replicate-consistency diagnostic)

Panels A and B preserve the existing main-text figure so the section 4.2 body
prose stays valid; panel C is the new replicate-spread diagnostic.

Input: results/analysis/phase_space_replicated_<timestamp>.json (final output).
Falls back to phase_space_replicated_partial.json if no final file exists yet.
Output: figures/manuscript/figure_09_phase_space.{png,pdf}
"""
import sys
import json
import glob
from pathlib import Path

sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point')

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from src.poverty_point.parameters import default_parameters, critical_threshold

ROOT = Path('/Users/clipo/PycharmProjects/poverty-point')
RESULTS_DIR = ROOT / 'results/analysis'
OUT_MS = ROOT / 'figures/manuscript'

# Consistent sans-serif per project figure conventions
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['svg.fonttype'] = 'none'

_params = default_parameters(seed=42)


def load_results():
    """Load the most recent final replicated run; fall back to the partial."""
    finals = sorted(glob.glob(str(RESULTS_DIR / 'phase_space_replicated_2*.json')))
    if finals:
        path = Path(finals[-1])
    else:
        path = RESULTS_DIR / 'phase_space_replicated_partial.json'
    with open(path) as f:
        data = json.load(f)
    return data, path


def build_grids(data):
    """Return (sigma_vals, eps_vals, mean_dom, mean_mon, sd_dom, n_grid)."""
    sigma_vals = sorted(set(r['target_sigma'] for r in data))
    eps_vals = sorted(set(r['epsilon'] for r in data))
    shape = (len(eps_vals), len(sigma_vals))

    dom = {(i, j): [] for i in range(len(eps_vals)) for j in range(len(sigma_vals))}
    mon = {(i, j): [] for i in range(len(eps_vals)) for j in range(len(sigma_vals))}

    for r in data:
        i = eps_vals.index(r['epsilon'])
        j = sigma_vals.index(r['target_sigma'])
        dom[(i, j)].append(r['dominance'])
        mon[(i, j)].append(r['monument_level'])

    mean_dom = np.full(shape, np.nan)
    mean_mon = np.full(shape, np.nan)
    sd_dom = np.full(shape, np.nan)
    n_grid = np.zeros(shape, dtype=int)

    for (i, j), vals in dom.items():
        if vals:
            mean_dom[i, j] = np.mean(vals)
            sd_dom[i, j] = np.std(vals, ddof=1) if len(vals) > 1 else 0.0
            n_grid[i, j] = len(vals)
    for (i, j), vals in mon.items():
        if vals:
            mean_mon[i, j] = np.mean(vals)

    return sigma_vals, eps_vals, mean_dom, mean_mon, sd_dom, n_grid


def make_figure(data):
    sigma_vals, eps_vals, mean_dom, mean_mon, sd_dom, n_grid = build_grids(data)
    extent = [min(sigma_vals), max(sigma_vals), min(eps_vals), max(eps_vals)]

    fig, axes = plt.subplots(1, 3, figsize=(18, 5.4))

    # Theoretical critical-threshold line: sigma* as a function of epsilon
    eps_line = np.linspace(max(0.05, min(eps_vals)), max(eps_vals), 60)
    sigma_stars = [critical_threshold(epsilon=e, n=25, params=_params) for e in eps_line]

    # --- Panel A: mean strategy dominance ---
    colors = ['#7b3294', '#c2a5cf', '#f7f7f7', '#fdae61', '#e66101']
    cmap_dom = LinearSegmentedColormap.from_list('strategy', colors, N=256)
    ax = axes[0]
    im = ax.imshow(mean_dom, extent=extent, origin='lower', aspect='auto',
                   cmap=cmap_dom, vmin=-1, vmax=0.5, interpolation='bilinear')
    ax.plot(sigma_stars, eps_line, 'k-', linewidth=2.5, label='Theoretical $\\sigma^*$')
    ax.plot(sigma_stars, eps_line, 'w--', linewidth=1.5)
    ax.set_xlabel('Environmental uncertainty ($\\sigma$)', fontsize=12)
    ax.set_ylabel('Ecotone advantage ($\\varepsilon$)', fontsize=12)
    ax.set_title('A. Mean strategy dominance', fontsize=12)
    cbar = plt.colorbar(im, ax=ax, label='Strategy dominance')
    cbar.ax.set_ylabel('← Independent | Aggregation →', fontsize=9)
    ax.legend(loc='upper left', fontsize=10)

    # --- Panel B: mean monument investment ---
    ax = axes[1]
    im = ax.imshow(mean_mon, extent=extent, origin='lower', aspect='auto',
                   cmap='YlOrBr', interpolation='bilinear')
    ax.plot(sigma_stars, eps_line, 'k-', linewidth=2.5, label='Theoretical $\\sigma^*$')
    ax.plot(sigma_stars, eps_line, 'w--', linewidth=1.5)
    ax.set_xlabel('Environmental uncertainty ($\\sigma$)', fontsize=12)
    ax.set_ylabel('Ecotone advantage ($\\varepsilon$)', fontsize=12)
    ax.set_title('B. Mean monument investment', fontsize=12)
    plt.colorbar(im, ax=ax, label='Monument level')
    ax.legend(loc='upper left', fontsize=10)

    # --- Panel C: replicate spread (SD of dominance) ---
    ax = axes[2]
    im = ax.imshow(sd_dom, extent=extent, origin='lower', aspect='auto',
                   cmap='viridis', interpolation='nearest')
    ax.plot(sigma_stars, eps_line, 'w-', linewidth=2.0, label='Theoretical $\\sigma^*$')
    ax.set_xlabel('Environmental uncertainty ($\\sigma$)', fontsize=12)
    ax.set_ylabel('Ecotone advantage ($\\varepsilon$)', fontsize=12)
    ax.set_title('C. Replicate spread (SD of dominance, $n=5$)', fontsize=12)
    plt.colorbar(im, ax=ax, label='SD of strategy dominance')
    ax.legend(loc='upper left', fontsize=10)

    plt.tight_layout()
    return fig, n_grid


def main():
    data, path = load_results()
    n_cells_complete = len({(r['target_sigma'], r['epsilon']) for r in data})
    print(f"Loaded {len(data)} cell-reps from {path.name}")
    fig, n_grid = make_figure(data)

    incomplete = int(np.sum((n_grid > 0) & (n_grid < 5)))
    empty = int(np.sum(n_grid == 0))
    print(f"Grid cells with data: {n_cells_complete}; "
          f"cells with <5 reps: {incomplete}; empty cells: {empty}")
    if empty or incomplete:
        print("WARNING: figure rendered from a NON-FINAL (partial) run. "
              "Re-run after the replicated job completes.")

    OUT_MS.mkdir(parents=True, exist_ok=True)
    png = OUT_MS / 'figure_09_phase_space.png'
    pdf = OUT_MS / 'figure_09_phase_space.pdf'
    fig.savefig(png, dpi=300, bbox_inches='tight')
    fig.savefig(pdf, bbox_inches='tight')
    print(f"Saved: {png}")
    print(f"Saved: {pdf}")


if __name__ == '__main__':
    main()
