"""Diagnostic figure for the §6.2 joint Monte Carlo posterior on threshold proximity.

Three-panel figure:
A. Joint posterior on (sigma_eff, sigma_star) with a y = x reference line; the fraction
   of samples with sigma_eff > sigma_star equals the §6.2 result P = 0.33.
B. Marginal posterior on (sigma_eff - sigma_star) overlaid against the prior on the
   same quantity (priors-only Monte Carlo at fixed default model parameters).
C. Per-parameter posterior marginals for the six joint-MC parameters, showing how
   much the joint posterior moves the marginal of each from its uniform prior.

Re-runs the §6.2 joint MC at N = 1,000 to capture per-sample data (the existing
summary JSON contains only summary statistics).
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from poverty_point.signaling_core import (
    SignalingParams,
    NetworkParams,
    AggregationParams,
    ConflictParams,
    critical_threshold,
)

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "figures" / "final"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans"],
    "font.size": 9,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

C_POST = "#2166AC"
C_PRIOR = "#999999"
C_THRESH = "#B2182B"


def sample_sigma(rng, n):
    T = rng.uniform(6, 18, n)
    m = rng.uniform(0.30, 0.60, n)
    sigma = m * np.sqrt(20.0 / T)
    return np.clip(sigma, 0.01, 0.99)


def sample_epsilon(rng, n):
    pp_weights = np.array([1.0, 1.0, 1.0, 1.0, 0.5])
    eps = []
    for _ in range(n):
        w = pp_weights + rng.uniform(-0.2, 0.2, 5)
        w = np.clip(w, 0.0, 1.0)
        p = w / w.sum()
        H = -np.sum(p * np.log(p + 1e-12))
        H_max = np.log(5)
        eps.append((H / H_max) * 0.5)
    return np.array(eps)


def run_joint_mc(N=1000, seed=42):
    rng = np.random.default_rng(seed)
    sigma = sample_sigma(rng, N)
    epsilon = sample_epsilon(rng, N)

    # Six load-bearing parameters from §S3.1, sampled at ±50% uniform
    defaults = {
        "C_signal": 0.18,
        "C_opportunity": 0.12,
        "lambda_W": 0.15,
        "k_max": 6.0,
        "M_half": 100.0,
        "gamma": 0.4,
    }
    params_samples = {
        k: rng.uniform(0.5 * v, 1.5 * v, N) for k, v in defaults.items()
    }

    sigma_star = np.full(N, np.nan)
    for i in range(N):
        sig_p = SignalingParams(
            lambda_W=params_samples["lambda_W"][i],
        )
        net_p = NetworkParams(
            k_max=params_samples["k_max"][i],
            M_half=params_samples["M_half"][i],
            gamma=params_samples["gamma"][i],
        )
        agg_p = AggregationParams(
            C_signal=params_samples["C_signal"][i],
            C_opportunity=params_samples["C_opportunity"][i],
        )
        try:
            res = critical_threshold(
                epsilon=epsilon[i],
                n_agg=25,
                travel_distance=100.0,
                sig_params=sig_p,
                net_params=net_p,
                agg_params=agg_p,
            )
            sigma_star[i] = res["sigma_star"]
        except Exception:
            pass

    valid = ~np.isnan(sigma_star)
    sigma_eff = sigma * (1.0 - epsilon)
    return {
        "sigma_eff": sigma_eff[valid],
        "sigma_star": sigma_star[valid],
        "epsilon": epsilon[valid],
        "params": {k: v[valid] for k, v in params_samples.items()},
        "defaults": defaults,
    }


def run_prior_only(N=1000, seed=43):
    """Priors-only MC at fixed default model parameters: shows what sigma_eff - sigma_star
    distribution looks like before the parameter-set uncertainty is propagated."""
    rng = np.random.default_rng(seed)
    sigma = sample_sigma(rng, N)
    epsilon = sample_epsilon(rng, N)
    sigma_eff = sigma * (1.0 - epsilon)
    sigma_star = np.full(N, np.nan)
    for i in range(N):
        try:
            res = critical_threshold(epsilon=epsilon[i], n_agg=25, travel_distance=100.0)
            sigma_star[i] = res["sigma_star"]
        except Exception:
            pass
    valid = ~np.isnan(sigma_star)
    return {
        "sigma_eff": sigma_eff[valid],
        "sigma_star": sigma_star[valid],
    }


def main() -> None:
    print("Running joint Monte Carlo (N=1000)...")
    joint = run_joint_mc(N=1000, seed=42)
    print(f"  Valid samples: {len(joint['sigma_eff'])}")
    P_joint = float(np.mean(joint["sigma_eff"] > joint["sigma_star"]))
    print(f"  P(sigma_eff > sigma_star) = {P_joint:.3f}")

    print("Running priors-only baseline (N=1000)...")
    prior = run_prior_only(N=1000, seed=43)
    P_prior = float(np.mean(prior["sigma_eff"] > prior["sigma_star"]))
    print(f"  P(sigma_eff > sigma_star) baseline = {P_prior:.3f}")

    # Build figure
    fig = plt.figure(figsize=(13, 4.0))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.0, 1.4], wspace=0.30)

    # Panel A: joint posterior scatter
    ax_a = fig.add_subplot(gs[0, 0])
    above = joint["sigma_eff"] > joint["sigma_star"]
    ax_a.scatter(joint["sigma_eff"][~above], joint["sigma_star"][~above],
                 s=4, c=C_PRIOR, alpha=0.4, label=f"$\\sigma_{{eff}} \\leq \\sigma^*$ ({(~above).sum()})")
    ax_a.scatter(joint["sigma_eff"][above], joint["sigma_star"][above],
                 s=4, c=C_POST, alpha=0.55, label=f"$\\sigma_{{eff}} > \\sigma^*$ ({above.sum()})")
    lim = (0.0, max(joint["sigma_eff"].max(), joint["sigma_star"].max()) * 1.05)
    ax_a.plot(lim, lim, color=C_THRESH, linewidth=1.2, linestyle="--", zorder=5)
    ax_a.set_xlim(lim)
    ax_a.set_ylim(lim)
    ax_a.set_xlabel(r"$\sigma_{eff}$ (paleoclimate)")
    ax_a.set_ylabel(r"$\sigma^*$ (model-derived)")
    ax_a.set_aspect("equal")
    ax_a.legend(loc="upper left", framealpha=0.92)
    ax_a.text(0.02, 0.98, "A", transform=ax_a.transAxes, fontsize=13, fontweight="bold",
              va="top")
    ax_a.set_title(f"Joint posterior: $P(\\sigma_{{eff}} > \\sigma^*) = {P_joint:.2f}$",
                   fontsize=10, pad=8)

    # Panel B: posterior on sigma_eff - sigma_star vs prior
    ax_b = fig.add_subplot(gs[0, 1])
    diff_post = joint["sigma_eff"] - joint["sigma_star"]
    diff_prior = prior["sigma_eff"] - prior["sigma_star"]
    bins = np.linspace(min(diff_post.min(), diff_prior.min()),
                       max(diff_post.max(), diff_prior.max()), 36)
    ax_b.hist(diff_prior, bins=bins, density=True, alpha=0.45, color=C_PRIOR,
              label=f"Priors only ($P = {P_prior:.2f}$)", edgecolor="white", linewidth=0.4)
    ax_b.hist(diff_post, bins=bins, density=True, alpha=0.55, color=C_POST,
              label=f"Joint posterior ($P = {P_joint:.2f}$)", edgecolor="white", linewidth=0.4)
    ax_b.axvline(0, color=C_THRESH, linewidth=1.0, linestyle="--", zorder=5)
    ax_b.set_xlabel(r"$\sigma_{eff} - \sigma^*$")
    ax_b.set_ylabel("Posterior density")
    ax_b.legend(loc="upper left", framealpha=0.92)
    ax_b.text(0.02, 0.98, "B", transform=ax_b.transAxes, fontsize=13, fontweight="bold",
              va="top")
    ax_b.set_title(r"Marginal $\sigma_{eff} - \sigma^*$: prior vs posterior",
                   fontsize=10, pad=8)

    # Panel C: per-parameter posterior marginals
    ax_c = fig.add_subplot(gs[0, 2])
    param_order = ["C_signal", "C_opportunity", "lambda_W", "k_max", "M_half", "gamma"]
    param_labels = [
        r"$C_{signal}$", r"$C_{opp}$", r"$\lambda_W$",
        r"$k_{max}$", r"$M_{half}$", r"$\gamma$",
    ]
    # Show posterior medians vs prior bounds
    n_p = len(param_order)
    y = np.arange(n_p)[::-1]
    for i, p in enumerate(param_order):
        defaults = joint["defaults"][p]
        lo, hi = 0.5 * defaults, 1.5 * defaults
        # Plot full prior support as gray bar
        ax_c.barh(y[i], hi - lo, left=lo, height=0.6, color=C_PRIOR, alpha=0.35,
                  edgecolor="none", zorder=1)
        # Conditional on above-threshold (sigma_eff > sigma_star)
        post = joint["params"][p][joint["sigma_eff"] > joint["sigma_star"]]
        if len(post) > 0:
            q_lo, q_hi = np.percentile(post, [2.5, 97.5])
            med = np.median(post)
            ax_c.barh(y[i], q_hi - q_lo, left=q_lo, height=0.4, color=C_POST,
                      alpha=0.85, edgecolor="white", linewidth=0.5, zorder=2)
            ax_c.scatter(med, y[i], s=22, c="white", edgecolors="black", linewidths=0.7,
                         zorder=3)
        ax_c.scatter(defaults, y[i], s=30, marker="x", c=C_THRESH, linewidths=1.5,
                     zorder=4)

    ax_c.set_yticks(y)
    ax_c.set_yticklabels(param_labels)
    ax_c.set_xlabel("Parameter value")
    ax_c.set_xscale("log")
    ax_c.text(0.02, 0.98, "C", transform=ax_c.transAxes, fontsize=13, fontweight="bold",
              va="top")
    ax_c.set_title(r"Per-parameter posterior conditional on $\sigma_{eff} > \sigma^*$",
                   fontsize=10, pad=8)

    # Manual legend for panel C
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    legend_elements = [
        Patch(facecolor=C_PRIOR, alpha=0.35, label=r"Prior support ($\pm$50%)"),
        Patch(facecolor=C_POST, alpha=0.85, label="95% posterior CI (above-threshold subset)"),
        Line2D([0], [0], marker="x", color=C_THRESH, linestyle="", markersize=7,
               markeredgewidth=1.5, label="Default value"),
    ]
    ax_c.legend(handles=legend_elements, loc="lower right", framealpha=0.92, fontsize=7.5)

    fig.tight_layout()
    out_png = OUTPUT_DIR / "figure_S02_joint_mc_diagnostic.png"
    out_pdf = OUTPUT_DIR / "figure_S02_joint_mc_diagnostic.pdf"
    fig.savefig(out_png)
    fig.savefig(out_pdf)
    print(f"\nWrote {out_png}")
    print(f"Wrote {out_pdf}")


if __name__ == "__main__":
    main()
