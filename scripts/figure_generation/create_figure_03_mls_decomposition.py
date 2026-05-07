#!/usr/bin/env python3
"""Multilevel-selection (Price equation) decomposition figure for the JAMT
manuscript. Two panels:

A. Schematic of two groups: an aggregator-majority group and an
   independent-majority group. Within each group, cooperators pay a fitness
   cost relative to free-riders (within-group selection penalizes the
   aggregator strategy). Across groups, the aggregator-majority group has
   higher mean fitness when environmental uncertainty is high enough that
   network-mediated buffering matters (between-group selection rewards
   cooperator-majority groups).

B. Within-group, between-group, and net selection on the aggregator
   strategy as a function of environmental uncertainty sigma. The within
   component is a constant cost -C; the between component grows with sigma
   as shortfall risk makes cooperative buffering more valuable; the net
   crosses zero at sigma* where the two components balance.

The figure is illustrative rather than calibration-bound: parameter values
are chosen so the threshold lands near the manuscript's sigma* ~ 0.40
without invoking the full feedback-loop equilibrium machinery.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import FancyArrowPatch


OUTPUT_DIR = Path(__file__).resolve().parents[2] / "figures" / "final"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ── Style ──────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 10,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

C_AGG = "#D55E00"   # Aggregator (orange)
C_IND = "#5E3C99"   # Independent (purple)
C_WITHIN = "#B2182B"  # within-group selection (red)
C_BETWEEN = "#2166AC"  # between-group selection (blue)
C_NET = "#1B7837"   # net selection (green)
C_THRESH = "#666666"


# ── Illustrative parameters ───────────────────────────────────────────────
# Cost of cooperation paid by aggregators (within-group penalty)
C_COOP = 0.10
# Cooperation benefit coefficient (scales between-group selection); tuned so
# the illustrative threshold lands near the manuscript value sigma* ~ 0.40.
B_COEF = 0.26
# Ecotone advantage at the gathering site
EPSILON = 0.35
# Network saturation curvature (mild superlinearity in benefit)
GAMMA = 1.4

# σ* under this illustrative form: solve B_COEF * sigma^GAMMA * (1 + EPSILON) = C_COOP
SIGMA_STAR = (C_COOP / (B_COEF * (1.0 + EPSILON))) ** (1.0 / GAMMA)


def within_group_selection(_sigma: np.ndarray) -> np.ndarray:
    """Constant cost penalty on aggregator strategy within mixed groups."""
    return np.full_like(_sigma, -C_COOP)


def between_group_selection(sigma: np.ndarray) -> np.ndarray:
    """Cooperation benefit growing with environmental uncertainty.

    Aggregator-majority groups outperform independent-majority groups by an
    amount that scales with sigma (more shortfall years → more value to
    network-mediated buffering) and with ecotone advantage epsilon.
    """
    return B_COEF * np.power(np.clip(sigma, 0.0, None), GAMMA) * (1.0 + EPSILON)


def net_selection(sigma: np.ndarray) -> np.ndarray:
    return within_group_selection(sigma) + between_group_selection(sigma)


# ── Panel A: schematic of two groups ──────────────────────────────────────
def draw_panel_a(ax) -> None:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 9)
    ax.set_aspect("equal")
    ax.axis("off")

    # Two group circles
    gx_agg, gy_agg, gr = 2.6, 4.5, 1.55
    gx_ind, gy_ind = 7.4, 4.5

    ax.add_patch(
        plt.Circle((gx_agg, gy_agg), gr, facecolor="#FFF1E0",
                   edgecolor=C_AGG, linewidth=2.0)
    )
    ax.add_patch(
        plt.Circle((gx_ind, gy_ind), gr, facecolor="#F2EBFB",
                   edgecolor=C_IND, linewidth=2.0)
    )

    rng = np.random.default_rng(42)

    def scatter_bands(cx, cy, n_agg, n_ind):
        thetas = rng.uniform(0, 2 * np.pi, n_agg + n_ind)
        rs = rng.uniform(0.20, gr - 0.45, n_agg + n_ind)
        xs = cx + rs * np.cos(thetas)
        ys = cy + rs * np.sin(thetas)
        ax.scatter(xs[:n_agg], ys[:n_agg], s=70, c=C_AGG,
                   edgecolors="black", linewidths=0.5, zorder=3)
        ax.scatter(xs[n_agg:], ys[n_agg:], s=70, c=C_IND,
                   edgecolors="black", linewidths=0.5, zorder=3)

    scatter_bands(gx_agg, gy_agg, n_agg=8, n_ind=2)
    scatter_bands(gx_ind, gy_ind, n_agg=2, n_ind=8)

    # Group labels just above the circles
    ax.text(gx_agg, gy_agg + gr + 0.20,
            "Aggregator-majority group\n($q = 0.8$)",
            ha="center", va="bottom", fontsize=9.5, fontweight="bold",
            color=C_AGG)
    ax.text(gx_ind, gy_ind + gr + 0.20,
            "Independent-majority group\n($q = 0.2$)",
            ha="center", va="bottom", fontsize=9.5, fontweight="bold",
            color=C_IND)

    # Within-group annotations under each circle
    ax.text(gx_agg, gy_agg - gr - 0.30,
            r"Within-group: $w_A - w_I = -C$" + "\n(cooperators pay cost)",
            ha="center", va="top", fontsize=8.5, color=C_WITHIN)
    ax.text(gx_ind, gy_ind - gr - 0.30,
            r"Within-group: $w_A - w_I = -C$" + "\n(cooperators pay cost)",
            ha="center", va="top", fontsize=8.5, color=C_WITHIN)

    # Between-group arrow
    arrow_y = gy_agg + gr + 1.40
    arrow = FancyArrowPatch((gx_agg + gr + 0.10, arrow_y),
                            (gx_ind - gr - 0.10, arrow_y),
                            arrowstyle="-|>", mutation_scale=18,
                            color=C_BETWEEN, linewidth=2.0)
    ax.add_patch(arrow)
    ax.text((gx_agg + gx_ind) / 2, arrow_y + 0.30,
            r"Between-group: $\overline{W}_A > \overline{W}_I$"
            r"  (when $\sigma > \sigma^*$)",
            ha="center", va="bottom", fontsize=9, color=C_BETWEEN,
            fontweight="bold")

    # Legend (bands) at bottom
    leg_handles = [
        mpatches.Patch(color=C_AGG, label="Aggregator band"),
        mpatches.Patch(color=C_IND, label="Independent band"),
    ]
    ax.legend(handles=leg_handles, loc="lower center",
              bbox_to_anchor=(0.5, 0.04), ncol=2, frameon=False, fontsize=9)

    # Panel label
    ax.text(0.0, 8.6, "A", fontsize=14, fontweight="bold")


# ── Panel B: decomposition vs sigma ───────────────────────────────────────
def draw_panel_b(ax) -> None:
    sigma_grid = np.linspace(0.0, 0.8, 400)
    within = within_group_selection(sigma_grid)
    between = between_group_selection(sigma_grid)
    net = net_selection(sigma_grid)

    ax.axhline(0.0, color="black", linewidth=0.7, zorder=1)
    ax.fill_between(sigma_grid, 0.0, between, color=C_BETWEEN,
                    alpha=0.12, zorder=1)
    ax.fill_between(sigma_grid, within, 0.0, color=C_WITHIN,
                    alpha=0.12, zorder=1)

    ax.plot(sigma_grid, within, color=C_WITHIN, linewidth=2.2,
            label=r"Within-group: $-C$  (cooperation cost)")
    ax.plot(sigma_grid, between, color=C_BETWEEN, linewidth=2.2,
            label=r"Between-group: $B(\sigma) \cdot (1 + \varepsilon)$")
    ax.plot(sigma_grid, net, color=C_NET, linewidth=2.6,
            label=r"Net: within + between")

    # Threshold marker
    ax.axvline(SIGMA_STAR, color=C_THRESH, linewidth=1.0, linestyle="--",
               zorder=1)
    ax.text(SIGMA_STAR, ax.get_ylim()[1] if False else 0.16,
            rf"  $\sigma^* \approx {SIGMA_STAR:.2f}$",
            ha="left", va="bottom", fontsize=9.5, color=C_THRESH,
            fontweight="bold")

    # Annotations for selection regimes
    ax.annotate("Independents favored\n(net selection < 0)",
                xy=(0.18, -0.07), ha="center", va="center",
                fontsize=9, color=C_IND)
    ax.annotate("Aggregators favored\n(net selection > 0)",
                xy=(0.62, 0.10), ha="center", va="center",
                fontsize=9, color=C_AGG)

    ax.set_xlim(0.0, 0.8)
    ax.set_ylim(-0.18, 0.20)
    ax.set_xlabel(r"Environmental uncertainty $\sigma$")
    ax.set_ylabel("Selection coefficient on aggregator strategy")
    ax.legend(loc="lower right", framealpha=0.92)

    ax.text(-0.10, 0.225, "B", fontsize=14, fontweight="bold",
            transform=ax.transData)


def main() -> None:
    fig = plt.figure(figsize=(13.5, 5.6))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.05], wspace=0.18)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])

    draw_panel_a(ax_a)
    draw_panel_b(ax_b)

    fig.tight_layout()

    out_png = OUTPUT_DIR / "figure_03_mls_decomposition.png"
    out_pdf = OUTPUT_DIR / "figure_03_mls_decomposition.pdf"
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    print(f"wrote {out_png}")
    print(f"wrote {out_pdf}")
    print(f"sigma* (illustrative) = {SIGMA_STAR:.4f}")


if __name__ == "__main__":
    main()
