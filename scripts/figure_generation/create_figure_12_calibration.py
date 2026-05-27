#!/usr/bin/env python3
"""Figure 12: Archaeological calibration (3-panel).

Reads the cached 8-replicate calibration data
(results/calibration_replicates/replicates_n8_d200.json) for four
scenarios (low, poverty_point, critical, high) and renders the
three-panel calibration figure that the manuscript §6.1 caption
describes:

  (A) Monument volume by scenario, showing the cross-scenario
      gradient (low << PP < critical ~= high) with the PP bar
      calibrated to the 750,000 m^3 archaeological target.
  (B) Total exotic-goods counts across all five tracked materials
      (copper, steatite, galena, novaculite, crystal quartz), per
      scenario, against the 3-material archaeological reference sum.
  (C) Distance-decay prediction tested against published inventories
      using the model's p(d) = exp(-d/500) acquisition function;
      reports the log-space R^2 and Spearman rho.

This regenerates the figure WITHOUT re-running simulations. Output:
  figures/manuscript/figure_12_calibration.{png,pdf}

Conventions: sans-serif Arial, 300 dpi, explicit y-axis headroom on
each panel so value labels do not crowd panel titles.

NOTE on Panel C novaculite count: Webb (1982) does not report a total
novaculite count at PP and Gibson and Griffing (1994:Table 2) report
only 101 novaculite chipped-stone items at PP within a 3,046-item
sample. The 4,500 placeholder retained here (carried over from the
original figure) overstates novaculite abundance and inflates the
log-space R^2; the structural distance-decay claim is robust to
removing novaculite, but the R^2 / rho values shown here depend on
that placeholder. See the §6.1 prose, which discusses the novaculite
issue explicitly.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr


PROJECT_ROOT = Path("/Users/clipo/PycharmProjects/poverty-point-signaling")
OUT_DIR = PROJECT_ROOT / "figures" / "manuscript"
OUT_DIR.mkdir(parents=True, exist_ok=True)

REPLICATES_PATH = (
    PROJECT_ROOT / "results" / "calibration_replicates" / "replicates_n8_d200.json"
)

# Archaeological reference values
ARCHAEOLOGICAL_VOLUME_M3 = 750_000
# Per-material archaeological counts used in Panel C distance-decay
# test. All five entries are direct published counts at the Poverty
# Point type-site. Sources:
#   - Novaculite: 101 chipped-stone items at PP (Gibson and Griffing
#     1994:Table 2, within a 3,046-item sample). This is the only
#     published total novaculite count at PP; Webb (1982) reports
#     novaculite only as a percentage within microflint and
#     projectile-point classes and gives no site total.
#   - Crystal quartz: 395 raw crystals at PP (Webb 1982:Table 17).
#   - Galena: 740 = 702 raw masses + 38 finished objects (Webb 1982).
#   - Steatite: 2,221 fragments (Webb 1982). Note that Webb describes
#     these as "fragments representing several hundred vessels," so
#     the count is on a finer unit than the model's per-acquisition
#     events; the steatite point is therefore expected to plot above
#     a strict count-based model curve.
#   - Copper: 155 objects (Webb 1982).
ARCH_COUNTS = {
    "Novaculite\n(~250 km)":      (250, 101),
    "Crystal quartz\n(~300 km)":  (300, 395),
    "Galena\n(~800 km)":          (800, 740),
    "Steatite\n(~850 km)":        (850, 2_221),
    "Copper\n(~1600 km)":         (1600, 155),
}
ARCHAEOLOGICAL_EXOTICS_3MAT = 155 + 2_221 + 740  # 3,116 (Panel B reference)

# Scenarios (matched to keys in replicates_n8_d200.json)
SCENARIOS = [
    ("low",            "Low\n($\\sigma$≈0.32)",            "#7b3294"),
    ("poverty_point",  "Calibrated PP\n($\\sigma$≈0.64)",  "#1b7837"),
    ("critical",       "Critical\n($\\sigma$≈0.87)",       "#e66101"),
    ("high",           "High\n($\\sigma$≈1.00)",           "#d95f02"),
]


def main() -> None:
    with open(REPLICATES_PATH) as f:
        rows = json.load(f)

    # Aggregate per-scenario stats
    scen_names = [s[0] for s in SCENARIOS]
    labels = [s[1] for s in SCENARIOS]
    colors = [s[2] for s in SCENARIOS]

    monument_means_units = np.array([
        np.mean([r["monument_units"] for r in rows[n]]) for n in scen_names
    ])
    monument_sds_units = np.array([
        np.std([r["monument_units"] for r in rows[n]], ddof=1)
        for n in scen_names
    ])
    exotic_means = np.array([
        np.mean([r["exotics_total"] for r in rows[n]]) for n in scen_names
    ])
    exotic_sds = np.array([
        np.std([r["exotics_total"] for r in rows[n]], ddof=1)
        for n in scen_names
    ])

    # Calibration factor from PP scenario
    pp_idx = scen_names.index("poverty_point")
    pp_units_mean = float(monument_means_units[pp_idx])
    scaling_factor = (
        ARCHAEOLOGICAL_VOLUME_M3 / pp_units_mean if pp_units_mean > 0 else 77.0
    )
    monument_means_m3 = monument_means_units * scaling_factor
    monument_sds_m3 = monument_sds_units * scaling_factor

    # Plot
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]
    plt.rcParams["font.size"] = 10

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # ===== Panel A: Monument volume by scenario =====
    ax1 = axes[0]
    x = np.arange(len(SCENARIOS) + 1)
    all_labels = labels + ["Archaeological\n(750k m³)"]
    all_means_A = list(monument_means_m3) + [ARCHAEOLOGICAL_VOLUME_M3]
    all_sds_A = list(monument_sds_m3) + [0.0]
    all_colors = colors + ["#222222"]
    ax1.bar(
        x, all_means_A, yerr=all_sds_A, color=all_colors,
        edgecolor="black", linewidth=1.0, capsize=6,
    )
    ax1.set_xticks(x)
    ax1.set_xticklabels(all_labels, fontsize=8)
    ax1.set_ylabel("Monument Volume (m³)", fontsize=10)
    ax1.set_title("(A) Monument volume by scenario",
                  fontsize=10, fontweight="bold", loc="left")
    ax1.ticklabel_format(style="scientific", axis="y", scilimits=(0, 0))

    a_max = max(max(m + s for m, s in zip(all_means_A, all_sds_A)),
                ARCHAEOLOGICAL_VOLUME_M3)
    ax1.set_ylim(0, a_max * 1.18)

    # ===== Panel B: Exotic-goods counts per scenario =====
    ax2 = axes[1]
    all_means_B = list(exotic_means) + [ARCHAEOLOGICAL_EXOTICS_3MAT]
    all_sds_B = list(exotic_sds) + [0.0]
    ax2.bar(
        x, all_means_B, yerr=all_sds_B, color=all_colors,
        edgecolor="black", linewidth=1.0, capsize=6,
    )
    ax2.axhline(
        ARCHAEOLOGICAL_EXOTICS_3MAT, color="#222222", linestyle=":",
        linewidth=1.0, alpha=0.6,
        label=f"3-material archaeological reference = "
              f"{ARCHAEOLOGICAL_EXOTICS_3MAT}",
    )
    ax2.set_xticks(x)
    ax2.set_xticklabels(all_labels, fontsize=8)
    ax2.set_ylabel("Exotic items count", fontsize=10)
    ax2.set_title("(B) Exotic-goods counts (5 materials, total)",
                  fontsize=10, fontweight="bold", loc="left")
    b_max = max(max(m + s for m, s in zip(all_means_B, all_sds_B)),
                ARCHAEOLOGICAL_EXOTICS_3MAT)
    ax2.set_ylim(0, b_max * 1.18)
    ax2.legend(loc="upper right", fontsize=8)

    # ===== Panel C: Distance-decay test =====
    ax3 = axes[2]
    d_arr = np.array([ARCH_COUNTS[k][0] for k in ARCH_COUNTS])
    arch_arr = np.array([ARCH_COUNTS[k][1] for k in ARCH_COUNTS], dtype=float)
    pred_rel = np.exp(-d_arr / 500.0)
    pred_norm = pred_rel / pred_rel.max() * arch_arr.max()

    log_arch = np.log(arch_arr)
    log_pred = np.log(pred_norm)
    ss_res = np.sum((log_arch - log_pred) ** 2)
    ss_tot = np.sum((log_arch - log_arch.mean()) ** 2)
    r2_log = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    rho, _ = spearmanr(arch_arr, pred_norm)

    ax3.scatter(d_arr, arch_arr, color="#222222", s=80, marker="D",
                zorder=3, label="Published counts (see caption)")
    ax3.plot(d_arr, pred_norm, color="#d4760a", linewidth=2,
             marker="o", markersize=6, zorder=2,
             label="Model: $\\exp(-d/500)$ (normalized)")
    ax3.set_yscale("log")
    ax3.set_xlabel("Source distance (km)", fontsize=10)
    ax3.set_ylabel("Item count (log scale)", fontsize=10)
    # Report ρ in the panel title; R² is negative (~ -1.2) under this
    # parameterization, which doesn't summarize cleanly in the title
    # and is reported in the caption instead.
    ax3.set_title(
        f"(C) Distance-decay test, 5 published counts "
        f"(Spearman $\\rho = {rho:+.2f}$)",
        fontsize=10, fontweight="bold", loc="left",
    )
    ax3.legend(loc="upper right", fontsize=8)
    # Label each point with the material name. Near-source materials
    # (novaculite, quartz) sit well below the model curve because PP
    # is downstream of their distance-decay rather than the
    # acquisition hub; far-source materials (galena, copper) fall
    # close to the curve.
    ymin, ymax = ax3.get_ylim()
    for (label, (d, n)) in ARCH_COUNTS.items():
        material = label.split("\n")[0]
        # Offset labels above the data point for clarity
        ax3.annotate(
            material, xy=(d, n), xytext=(8, 6), textcoords="offset points",
            fontsize=7, color="#333333",
        )
    # Highlight the two near-source materials as "downstream" cases
    ax3.annotate(
        "PP downstream\nof close-source\ndistance-decay",
        xy=(275, 200), xytext=(450, 30),
        fontsize=7.5, color="#888888", ha="left", va="center", style="italic",
        arrowprops=dict(arrowstyle="-", color="#888888", lw=0.7, alpha=0.7),
    )

    print(f"\nPanel C summary (5 published counts):")
    for (label, (d, n)), p in zip(ARCH_COUNTS.items(), pred_norm):
        print(f"  {label.replace(chr(10), ' '):28s}  obs={n:>5d}  "
              f"pred_norm={p:>7.0f}  obs/pred={n/p:>5.2f}")
    print(f"  Log-space R^2 = {r2_log:+.3f}")
    print(f"  Spearman rho  = {rho:+.3f}")

    fig.tight_layout()
    out_png = OUT_DIR / "figure_12_calibration.png"
    out_pdf = OUT_DIR / "figure_12_calibration.pdf"
    fig.savefig(out_png, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(out_pdf, bbox_inches="tight", facecolor="white")
    print(f"Wrote {out_png}")
    print(f"Wrote {out_pdf}")
    print()
    print("Per-scenario summary (n=8 replicates each, 200 simulated years):")
    for i, n in enumerate(scen_names):
        print(f"  {n:14s}: monument = {monument_means_units[i]:>7.0f} ± "
              f"{monument_sds_units[i]:>5.0f} units "
              f"({monument_means_m3[i]:>7.0f} ± {monument_sds_m3[i]:>5.0f} m³); "
              f"exotics = {exotic_means[i]:>7.0f} ± {exotic_sds[i]:>5.0f}")
    print(f"\nCalibration factor = {scaling_factor:.2f} m³/unit "
          f"(PP units mean = {pp_units_mean:.0f})")
    print(f"\nPanel C: R^2 (log-space) = {r2_log:.3f}; "
          f"Spearman rho = {rho:.3f}")
    plt.close(fig)


if __name__ == "__main__":
    main()
