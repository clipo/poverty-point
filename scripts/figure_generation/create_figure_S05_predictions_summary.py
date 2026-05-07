#!/usr/bin/env python3
"""
Create Figure 16: Predictions Summary

2x3 grid of schematic panels, one per prediction category:
  A (Temporal): Construction pulses aligned with shortfall events
  B (Spatial): Distance-dependent participation gradient from site
  C (Material): Distance-decay curve with archaeological test markers
  D (Demographic): Aggregation size saturating at n_optimal
  E (Network): Small-world network topology schematic
  F (Cross-cultural): Phase space with 5 existing cases + blank positions

Primarily schematic using matplotlib annotations/patches.

Output: figures/supplemental/figure_S05_predictions_summary.png + .pdf
"""

import sys
sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point-signaling')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch
from pathlib import Path

from src.poverty_point.parameters import critical_threshold, default_parameters

PROJECT_ROOT = Path('/Users/clipo/PycharmProjects/poverty-point-signaling')
OUTPUT_DIR = PROJECT_ROOT / 'figures' / 'final'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Publication formatting
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11

# Compute critical threshold from model parameters
_params = default_parameters()
SIGMA_STAR = critical_threshold(0.35, 25, _params)

# Colorblind-safe palette
COLORS = {
    'primary': '#2166ac',
    'secondary': '#e66101',
    'highlight': '#d73027',
    'success': '#1b7837',
    'neutral': '#999999',
    'light': '#c2e0f2',
    'prediction': '#762a83',
    'test': '#f1a340',
}


def create_predictions_summary_figure():
    """Create Figure 16: Predictions Summary."""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.subplots_adjust(hspace=0.35, wspace=0.30, top=0.92, bottom=0.06,
                        left=0.06, right=0.97)

    # ── Panel A: Temporal - Construction pulses aligned with shortfalls ──
    ax = axes[0, 0]
    t = np.linspace(0, 500, 1000)
    # Schematic shortfall events
    shortfall_times = [80, 150, 230, 310, 400, 460]
    shortfall_width = 15

    # Background resource level
    resource = 0.7 + 0.1 * np.sin(t / 50)
    for st in shortfall_times:
        mask = (t > st) & (t < st + shortfall_width)
        resource[mask] -= 0.3

    # Construction pulses lag shortfalls
    construction = np.zeros_like(t)
    for st in shortfall_times:
        lag = 5
        mask = (t > st + lag) & (t < st + shortfall_width + 20)
        pulse = np.exp(-((t[mask] - (st + lag + 10)) ** 2) / 100)
        construction[mask] += pulse * 0.8

    ax.fill_between(t, resource, alpha=0.2, color=COLORS['primary'],
                    label='Resource level')
    ax.plot(t, resource, color=COLORS['primary'], linewidth=1, alpha=0.6)
    ax.bar(t[::5], construction[::5], width=4, color=COLORS['secondary'],
           alpha=0.6, label='Construction rate')

    for st in shortfall_times:
        ax.axvspan(st, st + shortfall_width, color=COLORS['highlight'],
                   alpha=0.10, linewidth=0)

    ax.set_xlabel('Time (years)')
    ax.set_ylabel('Relative magnitude')
    ax.set_title('A. Temporal: Pulsed Construction', fontsize=12,
                 fontweight='bold')
    ax.legend(loc='upper right', fontsize=8)
    ax.set_ylim(0, 1.1)
    ax.text(0.5, -0.18, 'Prediction: construction pulses follow shortfall events',
            transform=ax.transAxes, ha='center', fontsize=8, style='italic',
            color='gray')

    # ── Panel B: Spatial - Distance-dependent participation gradient ──
    ax = axes[0, 1]
    distances = np.linspace(0, 250, 200)
    participation = np.exp(-distances / 100) * 0.9

    ax.plot(distances, participation, color=COLORS['primary'], linewidth=2.5)
    ax.fill_between(distances, participation, alpha=0.15, color=COLORS['primary'])

    # Mark catchment zones
    ax.axvline(100, linestyle='--', color=COLORS['neutral'], alpha=0.7)
    ax.axvline(150, linestyle=':', color=COLORS['neutral'], alpha=0.7)
    ax.text(50, 0.85, 'Core\ncatchment', ha='center', fontsize=8, color=COLORS['primary'])
    ax.text(125, 0.5, 'Peripheral', ha='center', fontsize=8, color=COLORS['neutral'])
    ax.text(200, 0.15, 'Beyond\nrange', ha='center', fontsize=8, color=COLORS['neutral'])

    # Mark test sites
    test_sites = [('PP', 0), ('Jaketown', 90), ('Claiborne', 160), ('J.W. Copes', 70)]
    for name, dist in test_sites:
        y = np.exp(-dist / 100) * 0.9
        ax.plot(dist, y, 'D', color=COLORS['test'], markersize=7,
                markeredgecolor='black', markeredgewidth=0.5, zorder=3)
        ax.annotate(name, (dist, y), textcoords='offset points',
                    xytext=(5, 8), fontsize=7)

    ax.set_xlabel('Distance from Poverty Point (km)')
    ax.set_ylabel('Participation probability')
    ax.set_title('B. Spatial: Participation Gradient', fontsize=12,
                 fontweight='bold')
    ax.set_ylim(0, 1.05)
    ax.text(0.5, -0.18, 'Prediction: site affiliation decays with distance',
            transform=ax.transAxes, ha='center', fontsize=8, style='italic',
            color='gray')

    # ── Panel C: Material - Distance-decay with test markers ──
    ax = axes[0, 2]
    d = np.linspace(0, 2000, 300)
    p = np.exp(-d / 500)

    ax.plot(d, p, color=COLORS['primary'], linewidth=2.5,
            label='$p(d) = \\exp(-d/500)$')
    ax.fill_between(d, p, alpha=0.10, color=COLORS['primary'])

    # Material markers with expected relative frequencies
    materials = {
        'Novaculite': (250, '#d95f02'),
        'Crystal Quartz': (300, '#7570b3'),
        'Galena': (800, '#1b9e77'),
        'Steatite': (900, '#e7298a'),
        'Copper': (1600, '#66a61e'),
    }
    for name, (dist, color) in materials.items():
        prob = np.exp(-dist / 500)
        ax.plot(dist, prob, 's', color=color, markersize=9,
                markeredgecolor='black', markeredgewidth=0.8, zorder=3)
        ax.annotate(name, (dist, prob), textcoords='offset points',
                    xytext=(8, 3), fontsize=7.5)

    # Test zone
    ax.annotate('Testable: compare\nobserved ratios', xy=(1200, 0.15),
                fontsize=8, ha='center', color=COLORS['prediction'],
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=COLORS['prediction'], alpha=0.8))

    ax.set_xlabel('Distance (km)')
    ax.set_ylabel('Relative frequency')
    ax.set_title('C. Material: Distance Decay', fontsize=12, fontweight='bold')
    ax.legend(loc='upper right', fontsize=8)
    ax.set_ylim(-0.05, 1.05)
    ax.text(0.5, -0.18, 'Prediction: novaculite ~13x more common than copper',
            transform=ax.transAxes, ha='center', fontsize=8, style='italic',
            color='gray')

    # ── Panel D: Demographic - Aggregation size saturation ──
    ax = axes[1, 0]
    sigma = np.linspace(0, 1.0, 200)
    n_optimal = 25  # bands
    pop_per_band = 20

    # Aggregation size as function of sigma
    n_agg = np.zeros_like(sigma)
    above = sigma > SIGMA_STAR
    n_agg[above] = n_optimal * (1 - np.exp(-(sigma[above] - SIGMA_STAR) / 0.15))

    pop_agg = n_agg * pop_per_band

    ax.plot(sigma, pop_agg, color=COLORS['primary'], linewidth=2.5)
    ax.axhline(n_optimal * pop_per_band, linestyle='--', color=COLORS['neutral'],
               alpha=0.7, label=f'$n_{{optimal}} \\times$ band size = {n_optimal * pop_per_band}')
    ax.axvline(SIGMA_STAR, linestyle=':', color=COLORS['highlight'], alpha=0.7,
               label=f'$\\sigma^* = {SIGMA_STAR:.2f}$')

    ax.fill_between(sigma, pop_agg, alpha=0.10, color=COLORS['primary'])
    ax.annotate(f'Carrying capacity\n~{n_optimal * pop_per_band} individuals',
                xy=(0.85, n_optimal * pop_per_band),
                xytext=(0.75, n_optimal * pop_per_band * 0.7),
                fontsize=8, ha='center',
                arrowprops=dict(arrowstyle='->', color='gray'))

    ax.set_xlabel('Environmental uncertainty ($\\sigma$)')
    ax.set_ylabel('Aggregation population')
    ax.set_title('D. Demographic: Population Ceiling', fontsize=12,
                 fontweight='bold')
    ax.legend(loc='center right', fontsize=8)
    ax.set_ylim(0, n_optimal * pop_per_band * 1.3)
    ax.text(0.5, -0.18, 'Prediction: aggregation saturates, does not grow indefinitely',
            transform=ax.transAxes, ha='center', fontsize=8, style='italic',
            color='gray')

    # ── Panel E: Network - Small-world topology schematic ──
    ax = axes[1, 1]

    # Draw a schematic small-world network
    n_nodes = 16
    angles = np.linspace(0, 2 * np.pi, n_nodes, endpoint=False)
    r = 0.8
    x = r * np.cos(angles)
    y = r * np.sin(angles)

    # Local connections (ring lattice)
    for i in range(n_nodes):
        for j in [1, 2]:
            ni = (i + j) % n_nodes
            ax.plot([x[i], x[ni]], [y[i], y[ni]], '-',
                    color=COLORS['neutral'], alpha=0.4, linewidth=0.8)

    # Long-range connections (small-world shortcuts)
    shortcuts = [(0, 8), (3, 11), (5, 13), (7, 15)]
    for i, j in shortcuts:
        ax.plot([x[i], x[j]], [y[i], y[j]], '-',
                color=COLORS['highlight'], alpha=0.6, linewidth=1.5)

    # Draw nodes
    for i in range(n_nodes):
        circle = Circle((x[i], y[i]), 0.06, facecolor=COLORS['primary'],
                         edgecolor='black', linewidth=0.5, zorder=3)
        ax.add_patch(circle)

    # Labels
    ax.text(0, 0, 'Small-world\ntopology', ha='center', va='center',
            fontsize=9, fontweight='bold', color=COLORS['primary'])

    local_line = plt.Line2D([], [], color=COLORS['neutral'], linewidth=1,
                            label='Local obligations')
    long_line = plt.Line2D([], [], color=COLORS['highlight'], linewidth=1.5,
                           label='Long-range exchange')
    ax.legend(handles=[local_line, long_line], loc='lower center', fontsize=8)

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.set_title('E. Network: Exchange Topology', fontsize=12, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.text(0.5, -0.12, 'Prediction: LA-ICP-MS should reveal multi-pathway exchange',
            transform=ax.transAxes, ha='center', fontsize=8, style='italic',
            color='gray')

    # ── Panel F: Cross-cultural - Phase space with cases ──
    ax = axes[1, 2]
    sigma_range = np.linspace(0, 1.0, 200)
    epsilon_range = np.linspace(0, 0.5, 200)
    S, E = np.meshgrid(sigma_range, epsilon_range)

    # Phase boundary: compute sigma* for each epsilon (only varies with eps)
    sigma_star_by_eps = np.array([critical_threshold(eps, 25, _params) for eps in epsilon_range])
    sigma_star_grid = np.tile(sigma_star_by_eps[:, np.newaxis], (1, len(sigma_range)))
    signaling_region = S > sigma_star_grid

    ax.contourf(S, E, signaling_region.astype(float),
                levels=[-0.5, 0.5, 1.5], colors=[COLORS['light'], '#fde0c5'],
                alpha=0.5)
    ax.contour(S, E, signaling_region.astype(float),
               levels=[0.5], colors=['black'], linewidths=1.5)

    # Plot existing cases
    cases = {
        'Poverty Point': (0.64, 0.35, COLORS['secondary']),
        'Watson Brake': (0.55, 0.25, COLORS['secondary']),
        'Rapa Nui': (0.95, 0.10, COLORS['secondary']),
        'Chaco Canyon': (0.75, 0.30, COLORS['secondary']),
        'Rapa Iti': (0.32, 0.05, COLORS['primary']),
    }

    for name, (sig, eps, color) in cases.items():
        ax.plot(sig, eps, 'o', color=color, markersize=9,
                markeredgecolor='black', markeredgewidth=0.8, zorder=3)
        offset = (5, 5) if name != 'Rapa Iti' else (5, -10)
        ax.annotate(name, (sig, eps), textcoords='offset points',
                    xytext=offset, fontsize=7.5,
                    fontweight='bold' if name == 'Poverty Point' else 'normal')

    # Blank positions for new tests
    new_tests = {
        'Gobekli Tepe?': (0.80, 0.20),
        'Florida\nshell rings?': (0.50, 0.30),
        'Hopewell?': (0.60, 0.25),
    }
    for name, (sig, eps) in new_tests.items():
        ax.plot(sig, eps, 'x', color=COLORS['prediction'], markersize=8,
                markeredgewidth=2, zorder=3)
        ax.annotate(name, (sig, eps), textcoords='offset points',
                    xytext=(5, 5), fontsize=7, color=COLORS['prediction'])

    ax.set_xlabel('Environmental uncertainty ($\\sigma$)')
    ax.set_ylabel('Ecotone advantage ($\\varepsilon$)')
    ax.set_title('F. Cross-Cultural: Phase Space', fontsize=12,
                 fontweight='bold')

    # Legend
    monument_patch = mpatches.Patch(color=COLORS['secondary'], label='Monument-building')
    no_monument = mpatches.Patch(color=COLORS['primary'], label='Non-monument')
    test_marker = plt.Line2D([], [], marker='x', color=COLORS['prediction'],
                             linestyle='None', markersize=8, markeredgewidth=2,
                             label='Untested cases')
    ax.legend(handles=[monument_patch, no_monument, test_marker],
              loc='upper left', fontsize=8)

    ax.text(0.3, 0.42, 'Signaling\nfavored', fontsize=9,
            color=COLORS['secondary'], alpha=0.7, ha='center')
    ax.text(0.15, 0.08, 'No signaling', fontsize=9,
            color=COLORS['primary'], alpha=0.7, ha='center')

    ax.text(0.5, -0.18, 'Prediction: all hunter-gatherer monument sites fall above threshold',
            transform=ax.transAxes, ha='center', fontsize=8, style='italic',
            color='gray')

    return fig


def main():
    print("Creating Figure 16: Predictions Summary")
    print("=" * 60)

    fig = create_predictions_summary_figure()

    output_png = OUTPUT_DIR / 'figure_S05_predictions_summary.png'
    output_pdf = OUTPUT_DIR / 'figure_S05_predictions_summary.pdf'

    fig.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(output_pdf, bbox_inches='tight', facecolor='white')

    print(f"\nFigure saved to:")
    print(f"  PNG: {output_png}")
    print(f"  PDF: {output_pdf}")

    plt.close(fig)


if __name__ == '__main__':
    main()
