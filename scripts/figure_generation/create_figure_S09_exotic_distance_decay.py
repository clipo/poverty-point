#!/usr/bin/env python3
"""
Create Figure 15: Exotic Distance Decay

3 panels (1x3):
  A. Theoretical decay curve p(d) = exp(-d/500) with material markers at
     250, 300, 800, 900, 1600 km
  B. Simulated vs predicted material frequencies (multiple seeds, error bars)
  C. Model prediction vs archaeological data (Hill et al. 2016, Webb 1968)

Panel A is analytical. Panels B-C use simulation output + published counts.

Output: figures/supplemental/figure_S09_exotic_distance_decay.png + .pdf
"""

import sys
sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point-signaling')

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from src.poverty_point.integrated_simulation import IntegratedSimulation
from src.poverty_point.parameters import default_parameters
from src.poverty_point.environmental_scenarios import get_scenario
from src.poverty_point.agents import EXOTIC_SOURCES

PROJECT_ROOT = Path('/Users/clipo/PycharmProjects/poverty-point-signaling')
OUTPUT_DIR = PROJECT_ROOT / 'figures' / 'final'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Publication formatting
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11

# Archaeological data (approximate counts from Hill et al. 2016; Webb 1968)
ARCHAEOLOGICAL_COUNTS = {
    'novaculite': 1200,     # Most common local-ish lithic
    'crystal_quartz': 800,  # Moderately common
    'galena': 450,          # Less common, farther source
    'steatite': 350,        # Similar distance to galena
    'copper': 78,           # Rare, very distant source
}

DISTANCE_LAMBDA = 500.0  # km, model decay constant


def run_multi_seed_simulations(n_seeds=5, duration=500):
    """Run simulations with multiple seeds and collect exotic counts."""
    all_counts = []
    scenario = get_scenario('poverty_point')

    for seed in range(42, 42 + n_seeds):
        params = default_parameters(seed=seed)
        params.duration = duration

        sim = IntegratedSimulation(
            params=params,
            shortfall_params=scenario.shortfall_params,
            seed=seed
        )
        results = sim.run(verbose=False)

        # Get final exotic counts by material
        final_state = results.yearly_states[-1]
        counts = final_state.exotic_counts_by_material
        all_counts.append(counts)
        print(f"  Seed {seed}: {counts}")

    return all_counts


def create_exotic_distance_decay_figure():
    """Create Figure 15: Exotic Distance Decay."""
    print("Running multi-seed simulations...")
    all_counts = run_multi_seed_simulations(n_seeds=5)

    # Material properties
    materials = list(EXOTIC_SOURCES.keys())
    distances = np.array([EXOTIC_SOURCES[m] for m in materials])
    sort_idx = np.argsort(distances)
    materials_sorted = [materials[i] for i in sort_idx]
    distances_sorted = distances[sort_idx]

    # Colors for materials (colorblind-safe)
    material_colors = {
        'novaculite': '#d95f02',
        'crystal_quartz': '#7570b3',
        'galena': '#1b9e77',
        'steatite': '#e7298a',
        'copper': '#66a61e',
    }

    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    fig.subplots_adjust(wspace=0.30, top=0.88, bottom=0.14, left=0.06, right=0.97)

    # ── Panel A: Theoretical decay curve ──
    ax = axes[0]
    d = np.linspace(0, 2000, 500)
    p = np.exp(-d / DISTANCE_LAMBDA)

    ax.plot(d, p, 'k-', linewidth=2, label=f'$p(d) = \\exp(-d/{int(DISTANCE_LAMBDA)})$')

    for mat in materials_sorted:
        dist = EXOTIC_SOURCES[mat]
        prob = np.exp(-dist / DISTANCE_LAMBDA)
        ax.plot(dist, prob, 'o', color=material_colors[mat], markersize=10,
                markeredgecolor='black', markeredgewidth=0.8, zorder=3)
        label_name = mat.replace('_', ' ').title()
        # Offset labels to avoid overlap
        offset_y = 0.02 if mat not in ('galena', 'steatite') else -0.04
        offset_x = 30
        ax.annotate(f'{label_name}\n({int(dist)} km)',
                    xy=(dist, prob), xytext=(dist + offset_x, prob + offset_y),
                    fontsize=8, ha='left',
                    arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))

    ax.set_xlabel('Distance from Poverty Point (km)')
    ax.set_ylabel('Acquisition Probability')
    ax.set_title('A. Distance-Decay Model', fontsize=12, fontweight='bold')
    ax.legend(loc='upper right', fontsize=9)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(-50, 2050)

    # ── Panel B: Simulated vs predicted frequencies ──
    ax = axes[1]

    # Collect simulated counts per material across seeds
    sim_counts = {m: [] for m in materials_sorted}
    for counts in all_counts:
        for mat in materials_sorted:
            sim_counts[mat].append(counts.get(mat, 0))

    sim_means = [np.mean(sim_counts[m]) for m in materials_sorted]
    sim_stds = [np.std(sim_counts[m]) for m in materials_sorted]

    # Predicted relative frequencies from model
    raw_probs = np.array([np.exp(-EXOTIC_SOURCES[m] / DISTANCE_LAMBDA)
                          for m in materials_sorted])
    # Scale predicted to match simulated total
    total_sim = sum(sim_means)
    predicted = raw_probs / raw_probs.sum() * total_sim

    x_pos = np.arange(len(materials_sorted))
    bar_width = 0.35

    bars_sim = ax.bar(x_pos - bar_width / 2, sim_means, bar_width,
                      yerr=sim_stds, capsize=4,
                      color=[material_colors[m] for m in materials_sorted],
                      edgecolor='black', linewidth=0.5, alpha=0.8,
                      label='Simulated (5 seeds)')
    bars_pred = ax.bar(x_pos + bar_width / 2, predicted, bar_width,
                       color='white',
                       edgecolor=[material_colors[m] for m in materials_sorted],
                       linewidth=1.5, hatch='///', alpha=0.8,
                       label='Predicted (decay model)')

    ax.set_xlabel('Material')
    ax.set_ylabel('Count')
    ax.set_title('B. Simulated vs. Predicted', fontsize=12, fontweight='bold')
    labels = [m.replace('_', ' ').title() for m in materials_sorted]
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=9)
    ax.legend(loc='upper center', fontsize=8, ncol=2)

    # ── Panel C: Model vs archaeological data ──
    ax = axes[2]

    arch_counts = [ARCHAEOLOGICAL_COUNTS.get(m, 0) for m in materials_sorted]
    # Scale model predictions to archaeological total
    arch_total = sum(arch_counts)
    predicted_arch = raw_probs / raw_probs.sum() * arch_total

    bars_arch = ax.bar(x_pos - bar_width / 2, arch_counts, bar_width,
                       color=[material_colors[m] for m in materials_sorted],
                       edgecolor='black', linewidth=0.5, alpha=0.8,
                       label='Archaeological (Hill et al. 2016;\nWebb 1968)')
    bars_model = ax.bar(x_pos + bar_width / 2, predicted_arch, bar_width,
                        color='white',
                        edgecolor=[material_colors[m] for m in materials_sorted],
                        linewidth=1.5, hatch='///', alpha=0.8,
                        label='Model prediction')

    ax.set_xlabel('Material')
    ax.set_ylabel('Count')
    ax.set_title('C. Model vs. Archaeological Record', fontsize=12,
                 fontweight='bold')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels, rotation=30, ha='right', fontsize=9)
    ax.legend(loc='upper right', fontsize=8)

    # Add R-squared annotation
    if sum(arch_counts) > 0:
        arch_arr = np.array(arch_counts, dtype=float)
        pred_arr = np.array(predicted_arch, dtype=float)
        ss_res = np.sum((arch_arr - pred_arr) ** 2)
        ss_tot = np.sum((arch_arr - arch_arr.mean()) ** 2)
        if ss_tot > 0:
            r2 = 1 - ss_res / ss_tot
            ax.text(0.95, 0.75, f'$R^2 = {r2:.2f}$',
                    transform=ax.transAxes, fontsize=10,
                    ha='right', va='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    return fig


def main():
    print("Creating Figure 15: Exotic Distance Decay")
    print("=" * 60)

    fig = create_exotic_distance_decay_figure()

    output_png = OUTPUT_DIR / 'figure_S09_exotic_distance_decay.png'
    output_pdf = OUTPUT_DIR / 'figure_S09_exotic_distance_decay.pdf'

    fig.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(output_pdf, bbox_inches='tight', facecolor='white')

    print(f"\nFigure saved to:")
    print(f"  PNG: {output_png}")
    print(f"  PDF: {output_pdf}")

    plt.close(fig)


if __name__ == '__main__':
    main()
