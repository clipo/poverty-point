#!/usr/bin/env python3
"""Figure 7: Static ecotone-diversity screening of LMV mound-building sites.

Two-panel screening figure showing that all 11 LMV sites pass the
framework's necessity condition under the static-diversity proxy,
while not testing the framework's magnitude prediction (which requires
covariance-based, water-route-aware epsilon; see manuscript section 5.5
priority extension #6).

- Panel A: Shannon diversity index H (bars) and ordinal observed monument
  scale (diamonds, right axis) for the 11 Late/Middle Archaic LMV sites
  in Table 1 of the manuscript. The panel shows that all interior
  monument-building sites cluster in the high-H band; only the coastal
  Pearl River pair falls substantially lower.
- Panel B: Predicted critical threshold sigma* for each site (computed
  via the multilevel-selection threshold solver at site-specific epsilon
  with n_agg=25), with the regional environmental uncertainty band
  (sigma~0.64, 95% CI 0.41-0.94) overlaid. Necessity check: all sites'
  sigma* sit comfortably below the regional sigma central estimate.

Sources for zone-access weights (per Supplemental S2.4 rubric):
- Sassaman 2005:340-341 (Caney, Insley, Frenchman's Bend, Watson Brake
  geometric series)
- Saunders et al. 2005 (Watson Brake site description)
- Saunders et al. 2001 (Lower Jackson antiquity)
- Webb 1982 (Cowpen Slough, Jaketown, Poverty Point)
- Ward et al. 2022 (Jaketown chronology and assemblages)
- Jackson 1981 (J.W. Copes)
- Saucier 1981 (LMV geomorphology)
- Gibson 2000 (PP regional context)
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from poverty_point.signaling_core import critical_threshold


OUTPUT_DIR = Path(
    "/Users/clipo/PycharmProjects/poverty-point-signaling/figures/manuscript"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 10


# Site data from Table 1 of the manuscript.
# Tuple: (display_name, smithsonian, weights_5tuple, observed_ordinal,
#        n_drainages, primary_drainages)
# observed_ordinal: 1 = minimal, 2 = small, 3 = mid, 4 = very large
# n_drainages: count of independent canoe-accessible drainage systems
# within ~1-day travel from the site (the framework's covariance-based
# epsilon dimension; non-synchronized hydrographs imply shortfall
# buffering across drainages).
SITES = [
    ("Poverty Point",      "16WC5",   (1.0, 1.0, 1.0, 1.0, 0.5), 4, 4,
     "Bayou Maçon, Mississippi, Tensas, Yazoo"),
    ("Lower Jackson",      "16WC10",  (1.0, 0.9, 0.9, 1.0, 0.3), 1, 1,
     "Bayou Maçon (shares with PP)"),
    ("Insley",             "16FR3",   (0.9, 0.6, 0.8, 0.9, 0.0), 3, 1,
     "Boeuf River tributary"),
    ("Caney",              "16CT5",   (0.9, 0.6, 0.8, 0.8, 0.0), 3, 1,
     "Bayou Caney"),
    ("Watson Brake",       "16OU175", (0.8, 0.7, 0.7, 0.8, 0.0), 3, 1,
     "Bayou Bartholomew"),
    ("Frenchman's Bend",   "16OU259", (0.7, 0.5, 0.7, 0.7, 0.0), 2, 1,
     "Ouachita tributary"),
    ("J.W. Copes",         "16MA47",  (0.5, 0.6, 0.4, 0.7, 0.0), 1, 1,
     "Tensas Basin"),
    ("Cowpen Slough",      "16CT147", (0.9, 0.5, 0.8, 0.7, 0.0), 1, 1,
     "Tensas Basin"),
    ("Jaketown",           "22HU505", (1.0, 0.3, 0.8, 0.5, 0.0), 2, 1,
     "Yazoo Basin"),
    ("Claiborne",          "22HA501", (1.0, 0.0, 0.5, 0.3, 0.0), 2, 2,
     "Pearl River + Gulf Coast"),
    ("Cedarland",          "22HA506", (1.0, 0.0, 0.5, 0.3, 0.0), 2, 2,
     "Pearl River + Gulf Coast"),
]

# Regional environmental uncertainty for the LMV (from §3.3)
SIGMA_REGIONAL = 0.64
SIGMA_CI_LOW = 0.41
SIGMA_CI_HIGH = 0.94

# Aggregation size convention used in §4.5 Table 1
N_AGG = 25


def shannon_entropy(weights):
    """Compute Shannon entropy from raw zone-access weights."""
    w = np.asarray(weights, dtype=float)
    s = w.sum()
    if s <= 0:
        return 0.0
    p = w / s
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())


def epsilon_from_h(H, H_max):
    """Map H/H_max into the model's epsilon range [0, 0.5]."""
    return float(0.5 * H / H_max)


def compute_site_metrics():
    H_max = np.log(5.0)  # 5 zones
    rows = []
    for name, smithsonian, weights, observed, n_drainages, drainage_names in SITES:
        H = shannon_entropy(weights)
        H_norm = H / H_max
        eps = epsilon_from_h(H, H_max)
        ct = critical_threshold(epsilon=eps, n_agg=N_AGG)
        rows.append(
            {
                "name": name,
                "smithsonian": smithsonian,
                "H": H,
                "H_norm": H_norm,
                "epsilon": eps,
                "sigma_star": float(ct["sigma_star"]),
                "observed": observed,
                "n_drainages": n_drainages,
                "drainage_names": drainage_names,
            }
        )
    return rows


def make_figure(rows):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.0, 8.0))

    names_with_id = [f"{r['name']}\n({r['smithsonian']})" for r in rows]
    Hs = np.array([r["H"] for r in rows])
    H_max = float(np.log(5.0))
    observed = np.array([r["observed"] for r in rows], dtype=float)
    sigma_stars = np.array([r["sigma_star"] for r in rows])

    # PP highlighted in orange, rest in gray
    bar_colors = ["#d4760a" if r["name"] == "Poverty Point" else "#9a9a9a" for r in rows]

    x = np.arange(len(rows))

    # Panel A: H bars + observed scale on right axis
    ax1.bar(x, Hs, color=bar_colors, edgecolor="black", linewidth=0.5, alpha=0.85)
    ax1.axhline(H_max, color="#1b7837", linestyle=":", linewidth=1.0,
                label=f"$H_{{max}} = \\ln 5 \\approx {H_max:.2f}$")
    ax1.set_ylabel("Shannon diversity index $H$", fontsize=10)
    ax1.set_ylim(0, 1.75)
    ax1.set_xticks(x)
    ax1.set_xticklabels(names_with_id, rotation=45, ha="right", fontsize=8)
    ax1.tick_params(axis="x", labelsize=8)

    # Right axis: observed ordinal monument scale (diamond markers)
    ax1b = ax1.twinx()
    ax1b.plot(x, observed, marker="D", linestyle="none", color="#222222",
              markersize=8, markeredgecolor="black", label="Observed monument scale")
    ax1b.set_yticks([1, 2, 3, 4])
    ax1b.set_yticklabels(["minimal", "small", "mid", "very large"], fontsize=8)
    ax1b.set_ylabel("Observed monument scale", fontsize=10)
    ax1b.set_ylim(0.5, 4.5)

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1b.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right",
               fontsize=8, framealpha=0.9)

    ax1.set_title("(A) Static ecotone-diversity screening",
                  fontsize=10, fontweight="bold", loc="left")

    # Panel B: predicted sigma* vs regional sigma band
    sigma_star_colors = bar_colors  # same orange/gray scheme
    # Panel B: count of independent canoe-accessible drainage systems
    # per site. This is the framework's *operative* dimension: shortfall
    # buffering depends on negative covariance among accessible zones,
    # which scales with the number of independent drainages reachable
    # within a canoe-day catchment. Static-diversity proxies (Panel A)
    # do not differentiate sites well; drainage independence does.
    n_drainages = np.array([r["n_drainages"] for r in rows])
    drainage_colors = ["#d4760a" if r["name"] == "Poverty Point" else "#9a9a9a"
                       for r in rows]
    bars = ax2.bar(x, n_drainages, color=drainage_colors, edgecolor="black",
                   linewidth=0.5, alpha=0.85)
    # Annotate each bar with the drainage names
    for r, bar in zip(rows, bars):
        ax2.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.08,
                 r["drainage_names"], ha="center", va="bottom",
                 fontsize=6.5, rotation=20, color="#333333")
    ax2.axhline(1, color="gray", linestyle=":", linewidth=0.8, alpha=0.5)
    ax2.set_ylabel("Independent drainage systems\n(canoe-day catchment)",
                   fontsize=9.5)
    ax2.set_xticks(x)
    ax2.set_xticklabels(names_with_id, rotation=45, ha="right", fontsize=8)
    ax2.set_xlim(x[0]-0.5, x[-1]+0.5)
    ax2.set_ylim(0, 5.2)
    ax2.set_yticks([0, 1, 2, 3, 4, 5])
    ax2.set_title(
        "(B) Multi-drainage shortfall buffering: PP integrates four "
        "independent drainages\nwith non-synchronized hydrographs; other "
        "LMV sites integrate one or two",
        fontsize=10, fontweight="bold", loc="left",
    )

    plt.tight_layout()
    return fig


def main():
    rows = compute_site_metrics()
    print("Computed site metrics:")
    print(f"{'Site':<22} {'H':>5} {'H/Hmax':>7} {'eps':>6} {'sigma*':>7}  obs")
    for r in rows:
        print(f"{r['name']:<22} {r['H']:>5.2f} {r['H_norm']:>7.2f} "
              f"{r['epsilon']:>6.2f} {r['sigma_star']:>7.3f}  {r['observed']}")

    fig = make_figure(rows)
    out_png = OUTPUT_DIR / "figure_04_ecotone_seasonal.png"
    out_pdf = OUTPUT_DIR / "figure_04_ecotone_seasonal.pdf"
    fig.savefig(out_png, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(out_pdf, bbox_inches="tight", facecolor="white")
    print(f"\nFigure saved to {out_png} and {out_pdf}")
    plt.close(fig)


if __name__ == "__main__":
    main()
