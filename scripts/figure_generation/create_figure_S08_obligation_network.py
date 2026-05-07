#!/usr/bin/env python3
"""
Create Figure 14: Obligation Network

3 panels (1x3):
  A. Network graph at year 300 - nodes sized by prestige, colored by strategy,
     edges by obligation strength
  B. Network density over time (mean obligations: aggregators vs independents)
  C. Social insurance: obligation count vs shortfall survival probability

Requires Phase 2 infrastructure additions to IntegratedState.

Output: figures/supplemental/figure_S08_obligation_network.png + .pdf
"""

import sys
sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point-signaling')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from scipy.ndimage import uniform_filter1d

from src.poverty_point.integrated_simulation import IntegratedSimulation
from src.poverty_point.parameters import default_parameters
from src.poverty_point.environmental_scenarios import get_scenario
from src.poverty_point.agents import Strategy

PROJECT_ROOT = Path('/Users/clipo/PycharmProjects/poverty-point-signaling')
OUTPUT_DIR = PROJECT_ROOT / 'figures' / 'final'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Publication formatting
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11


def run_simulation_with_snapshots(seed=42, duration=500, snapshot_year=300):
    """Run simulation and capture band-level data at a snapshot year."""
    scenario = get_scenario('poverty_point')
    params = default_parameters(seed=seed)
    params.duration = duration

    sim = IntegratedSimulation(
        params=params,
        shortfall_params=scenario.shortfall_params,
        seed=seed
    )

    snapshot_bands = None

    for yr in range(duration):
        sim.step_year()
        if sim.year == snapshot_year:
            # Capture band-level snapshot
            snapshot_bands = []
            for b in sim.bands:
                snapshot_bands.append({
                    'band_id': b.band_id,
                    'strategy': b.strategy,
                    'prestige': b.prestige,
                    'size': b.size,
                    'obligations': dict(b.obligations),
                    'total_exotics': b.total_exotic_count,
                })

    sim.results.compute_summary(burn_in=params.burn_in)
    return sim.results.yearly_states, snapshot_bands


def create_obligation_network_figure():
    """Create Figure 14: Obligation Network."""
    states, snapshot_bands = run_simulation_with_snapshots()

    # Colors
    color_agg = '#e66101'
    color_ind = '#2166ac'
    color_edge = '#999999'

    fig, axes = plt.subplots(1, 3, figsize=(16, 5.5))
    fig.subplots_adjust(wspace=0.32, top=0.88, bottom=0.12, left=0.06, right=0.97)

    # ── Panel A: Network graph at snapshot year ──
    ax = axes[0]

    if snapshot_bands:
        n_bands = len(snapshot_bands)

        # Position nodes in a circle
        angles = np.linspace(0, 2 * np.pi, n_bands, endpoint=False)
        radius = 1.0
        x_pos = radius * np.cos(angles)
        y_pos = radius * np.sin(angles)

        # Draw edges first (obligations)
        band_id_to_idx = {b['band_id']: i for i, b in enumerate(snapshot_bands)}
        for i, band in enumerate(snapshot_bands):
            for partner_id, strength in band['obligations'].items():
                if partner_id in band_id_to_idx:
                    j = band_id_to_idx[partner_id]
                    if j > i:  # Draw each edge once
                        ax.plot([x_pos[i], x_pos[j]], [y_pos[i], y_pos[j]],
                                color=color_edge, alpha=min(0.8, strength),
                                linewidth=0.5 + strength * 2, zorder=1)

        # Draw nodes
        for i, band in enumerate(snapshot_bands):
            is_agg = band['strategy'] == Strategy.AGGREGATOR
            color = color_agg if is_agg else color_ind
            size = 20 + band['prestige'] * 8
            size = min(size, 200)
            ax.scatter(x_pos[i], y_pos[i], s=size, c=color, edgecolors='black',
                       linewidth=0.5, zorder=2, alpha=0.85)

        # Legend
        agg_patch = mpatches.Patch(color=color_agg, label='Aggregator')
        ind_patch = mpatches.Patch(color=color_ind, label='Independent')
        ax.legend(handles=[agg_patch, ind_patch], loc='upper left', fontsize=8,
                  framealpha=0.9)

        ax.set_xlim(-1.4, 1.4)
        ax.set_ylim(-1.4, 1.4)
        ax.set_aspect('equal')

    ax.set_title('A. Obligation Network (Year 300)', fontsize=12, fontweight='bold')
    ax.text(0, -1.3, 'Node size = prestige\nEdge width = obligation strength',
            ha='center', fontsize=8, style='italic', color='gray')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # ── Panel B: Network density over time ──
    ax = axes[1]
    years = np.array([s.year for s in states])
    cal_years = 1700 - years

    obl_agg = np.array([s.mean_obligations_per_aggregator for s in states])
    obl_ind = np.array([s.mean_obligations_per_independent for s in states])
    edges = np.array([s.network_edge_count for s in states])

    smooth = 15
    obl_agg_smooth = uniform_filter1d(obl_agg, smooth)
    obl_ind_smooth = uniform_filter1d(obl_ind, smooth)

    ax.plot(cal_years, obl_agg_smooth, color=color_agg, linewidth=2,
            label='Aggregators')
    ax.fill_between(cal_years, obl_agg, alpha=0.10, color=color_agg)
    ax.plot(cal_years, obl_ind_smooth, color=color_ind, linewidth=2,
            label='Independents')
    ax.fill_between(cal_years, obl_ind, alpha=0.10, color=color_ind)

    ax.set_ylabel('Mean Obligations per Band')
    ax.set_xlabel('Calendar Year (BCE)')
    ax.set_title('B. Network Density Over Time', fontsize=12, fontweight='bold')
    ax.legend(loc='upper right', fontsize=9)
    ax.set_ylim(bottom=0)
    ax.invert_xaxis()

    # ── Panel C: Social insurance ──
    ax = axes[2]

    # For each band at each year, compute: obligation count vs survival
    # We'll use shortfall years to look at whether bands with more obligations
    # had better outcomes (lower size loss)
    # Approximate using time-series data: during shortfall years, compare
    # obligation levels with fitness
    shortfall_years_idx = [i for i, s in enumerate(states) if s.in_shortfall]

    if shortfall_years_idx:
        # Use obligation count and fitness during shortfall years
        obl_during_shortfall = [states[i].mean_obligations_per_aggregator
                                for i in shortfall_years_idx]
        fitness_during_shortfall = [states[i].mean_fitness_aggregators
                                    for i in shortfall_years_idx]

        # Also get non-shortfall baseline
        non_shortfall_idx = [i for i, s in enumerate(states) if not s.in_shortfall]
        obl_non_shortfall = [states[i].mean_obligations_per_aggregator
                             for i in non_shortfall_idx[:len(shortfall_years_idx)]]
        fitness_non_shortfall = [states[i].mean_fitness_aggregators
                                 for i in non_shortfall_idx[:len(shortfall_years_idx)]]

        ax.scatter(obl_during_shortfall, fitness_during_shortfall,
                   c=color_agg, alpha=0.5, s=25, label='During shortfall', zorder=2)
        ax.scatter(obl_non_shortfall, fitness_non_shortfall,
                   c=color_ind, alpha=0.3, s=15, label='Normal years', zorder=1)

        # Fit trend line for shortfall years
        if len(obl_during_shortfall) > 5:
            obl_arr = np.array(obl_during_shortfall)
            fit_arr = np.array(fitness_during_shortfall)
            valid = np.isfinite(obl_arr) & np.isfinite(fit_arr) & (obl_arr > 0)
            if np.sum(valid) > 5:
                z = np.polyfit(obl_arr[valid], fit_arr[valid], 1)
                p = np.poly1d(z)
                x_trend = np.linspace(obl_arr[valid].min(), obl_arr[valid].max(), 50)
                ax.plot(x_trend, p(x_trend), '--', color=color_agg, linewidth=1.5,
                        alpha=0.8, label=f'Trend (slope={z[0]:.3f})')

    ax.set_xlabel('Mean Obligations per Band')
    ax.set_ylabel('Mean Fitness (Aggregators)')
    ax.set_title('C. Social Insurance Effect', fontsize=12, fontweight='bold')
    ax.legend(loc='lower right', fontsize=8)

    return fig


def main():
    print("Creating Figure 14: Obligation Network")
    print("=" * 60)

    fig = create_obligation_network_figure()

    output_png = OUTPUT_DIR / 'figure_S08_obligation_network.png'
    output_pdf = OUTPUT_DIR / 'figure_S08_obligation_network.pdf'

    fig.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(output_pdf, bbox_inches='tight', facecolor='white')

    print(f"\nFigure saved to:")
    print(f"  PNG: {output_png}")
    print(f"  PDF: {output_pdf}")

    plt.close(fig)


if __name__ == '__main__':
    main()
