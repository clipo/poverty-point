#!/usr/bin/env python3
"""Figure 3: Fitness crossover and the critical threshold, with the
sigma_eff posterior from the §4.5 Monte Carlo overlaid.

Two-panel figure:
- Panel A: Expected fitness W_agg(sigma) and W_ind(sigma) curves with
  the sigma_eff posterior distribution shown as a shaded histogram
  along the bottom axis. The crossover at sigma* = 0.40 (epsilon=0.35)
  is marked.
- Panel B: Fitness difference W_agg - W_ind with the sigma_eff
  posterior shown as a shaded distribution and the PP central
  estimate marked.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from poverty_point.signaling_core import (
    AggregationParams,
    ConflictParams,
    NetworkParams,
    SignalingParams,
    fitness_advantage,
    lambda_total_at_sigma,
    independent_expected_fitness,
    expected_signaling_benefit,
)


OUTPUT_DIR = Path(
    "/Users/clipo/PycharmProjects/poverty-point-signaling/figures/manuscript"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 10

EPSILON = 0.35
N_AGG = 25


def main():
    # Sweep sigma; compute W_agg - W_ind via fitness_advantage,
    # and reconstruct individual curves from the lambda fixed point.
    sigmas = np.linspace(0.05, 1.2, 60)
    sig_p = SignalingParams()
    net_p = NetworkParams()
    conf_p = ConflictParams()
    agg_p = AggregationParams()

    diff = np.array([
        fitness_advantage(s, EPSILON, N_AGG, 100.0,
                          sig_p, net_p, conf_p, agg_p)
        for s in sigmas
    ])

    # Reconstruct W_ind curve from the standalone independent function;
    # it does not depend on epsilon or n_agg
    w_ind = np.array([
        independent_expected_fitness(s, net_p, conf_p)
        for s in sigmas
    ])

    # W_agg = W_ind + diff (by definition of fitness_advantage)
    w_agg = w_ind + diff

    # Sigma_eff posterior from the §4.5 Monte Carlo
    # Reported: mean sigma_eff = 0.307, 95% CI 0.184-0.477
    # Approximate the distribution by drawing from a normal centered
    # at the mean with sd implied by the CI: (0.477-0.184)/(2*1.96)
    sigma_eff_mean = 0.307
    sigma_eff_sd = (0.477 - 0.184) / (2 * 1.96)
    rng = np.random.default_rng(20260429)
    sigma_eff_samples = rng.normal(sigma_eff_mean, sigma_eff_sd, size=5000)
    sigma_eff_samples = np.clip(sigma_eff_samples, 0.0, 1.5)

    # Critical threshold sigma* at epsilon=0.35
    # Find from the curve: where w_agg crosses w_ind
    sigma_star = float(sigmas[np.argmin(np.abs(diff))])

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.0, 4.5))

    # Panel A: fitness curves
    ax1.plot(sigmas, w_agg, color="#d4760a", linewidth=2.0,
             label="$W_{agg}$ (aggregator)")
    ax1.plot(sigmas, w_ind, color="#7b3294", linewidth=2.0,
             label="$W_{ind}$ (independent)")
    ax1.axvline(sigma_star, color="black", linestyle="--", linewidth=1.0,
                alpha=0.7, label=f"$\\sigma^* \\approx {sigma_star:.2f}$")
    # PP central estimate
    sigma_pp = 0.64
    ax1.axvline(sigma_pp, color="#d62728", linestyle=":", linewidth=1.5,
                label=f"PP estimate $\\sigma \\approx {sigma_pp}$")

    # Sigma_eff posterior as a small histogram at the bottom
    ax1_twin = ax1.twinx()
    ax1_twin.hist(sigma_eff_samples, bins=40, color="#7b3294", alpha=0.18,
                  density=True, label="$\\sigma_{eff}$ posterior")
    ax1_twin.set_ylabel("$\\sigma_{eff}$ posterior density",
                        color="#7b3294", fontsize=9)
    ax1_twin.tick_params(axis="y", labelcolor="#7b3294")
    ax1_twin.set_ylim(0, ax1_twin.get_ylim()[1] * 4)

    ax1.set_xlabel("Environmental uncertainty $\\sigma$ or $\\sigma_{eff}$", fontsize=10)
    ax1.set_ylabel("Expected fitness $W$", fontsize=10)
    ax1.set_title("(A) Fitness curves and crossover", fontsize=10,
                  fontweight="bold", loc="left")
    ax1.legend(loc="lower left", fontsize=8.5, framealpha=0.9)
    ax1.set_xlim(0.05, 1.0)

    # Panel B: fitness difference with posterior
    ax2.plot(sigmas, diff, color="black", linewidth=2.0,
             label="$W_{agg} - W_{ind}$")
    ax2.axhline(0, color="gray", linestyle="-", linewidth=0.5)
    ax2.axvline(sigma_star, color="black", linestyle="--", linewidth=1.0,
                alpha=0.7, label=f"$\\sigma^* \\approx {sigma_star:.2f}$")

    # Posterior distribution at bottom
    ax2_twin = ax2.twinx()
    ax2_twin.hist(sigma_eff_samples, bins=40, color="#7b3294", alpha=0.20,
                  density=True, label="$\\sigma_{eff}$ posterior")

    # Indicate ~25% above threshold
    above_frac = (sigma_eff_samples > sigma_star).mean()
    ax2_twin.set_ylabel(f"$\\sigma_{{eff}}$ posterior density (~{100*above_frac:.0f}% above $\\sigma^*$)",
                        color="#7b3294", fontsize=9)
    ax2_twin.tick_params(axis="y", labelcolor="#7b3294")
    ax2_twin.set_ylim(0, ax2_twin.get_ylim()[1] * 4)

    ax2.set_xlabel("$\\sigma$ or $\\sigma_{eff}$", fontsize=10)
    ax2.set_ylabel("Fitness difference $W_{agg} - W_{ind}$", fontsize=10)
    ax2.set_title("(B) Fitness advantage with $\\sigma_{eff}$ posterior",
                  fontsize=10, fontweight="bold", loc="left")
    ax2.legend(loc="lower right", fontsize=8.5, framealpha=0.9)
    ax2.set_xlim(0.05, 1.0)

    plt.tight_layout()

    out_png = OUTPUT_DIR / "figure_05_fitness_crossover.png"
    out_pdf = OUTPUT_DIR / "figure_05_fitness_crossover.pdf"
    fig.savefig(out_png, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(out_pdf, bbox_inches="tight", facecolor="white")
    print(f"Saved {out_png}")
    print(f"Saved {out_pdf}")
    print(f"sigma_star at epsilon={EPSILON}: {sigma_star:.4f}")
    print(f"Fraction of sigma_eff posterior above sigma*: {100*above_frac:.1f}%")
    plt.close(fig)


if __name__ == "__main__":
    main()
