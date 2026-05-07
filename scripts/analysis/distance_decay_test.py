#!/usr/bin/env python3
"""
Distance-Decay Test: Model Prediction vs Archaeological Data

Tests whether the model's acquisition probability p(d) = exp(-d/lambda)
is consistent with archaeological artifact counts from Webb (1968, 1982).

The model predicts that exotic material counts should decline exponentially
with distance from source. This script:
  1. Compiles verified artifact counts from Webb inventories
  2. Fits lambda via log-linear regression
  3. Tests whether lambda = 500 km (the manuscript's assumed value) is
     consistent with the data
  4. Computes R-squared
  5. Creates a publication-quality figure

Output:
  - figures/final/figure_distance_decay_test.png
  - docs/manuscript/distance_decay_results.md
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

PROJECT_ROOT = Path('/Users/clipo/PycharmProjects/poverty-point-signaling')
OUTPUT_DIR = PROJECT_ROOT / 'figures' / 'final'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Publication formatting ──
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
})

# ======================================================================
# Archaeological data from Webb (1968, 1982) claims files
# ======================================================================
# Each entry: (material, distance_km, count, source_note)
#
# Sources and counts are documented in:
#   docs/references/claims/webb_1968_claims.md
#   docs/references/claims/webb_1982_claims.md
#
# Novaculite: 6.40% of 10,214 projectile points = 654 points (Webb 1982
#   Table 9, p. 52; Webb 1968 p. 311). Plus 0.57% of ~23,000 microflints
#   = ~131 (Webb 1982 Table 9). Minimum ~785 items total.
#   Source: Ouachita Mountains, AR (~250 km; Webb 1968 p. 311).
#
# Quartz crystals: 395 (Webb 1982 Table 17, p. 64).
#   Source: Arkansas near Hot Springs (~300 km; Webb 1956 p. 104).
#
# Hematite/magnetite plummets: 2,790 (Webb 1982 p. 56, Claim 36).
#   78% hematite, 22% magnetite. Sources: multiple locations in Missouri
#   and central US. Conservative distance estimate ~400 km.
#   Note: Webb interprets as utilitarian bola weights. Lipo (2012)
#   suggests loom weights. Included here as clearly non-local material.
#
# Galena: 702 masses + 38 finished objects = 740 (Webb 1982 Claim 44).
#   Source: Potosi, Missouri (~800 km; Webb 1982 Claim 45, confirmed
#   by trace element analysis).
#
# Steatite: 4,945 fragments total (2,221 from midden + 2,724 cache;
#   Webb 1982 p. 45, Claim 41). Source: NE Alabama / NW Georgia
#   (~900 km; confirmed by mineralogical analysis, Webb 1982 Claim 42).
#   Note: the 2,724-fragment cache west of Mound A may represent a
#   single depositional event. The midden count alone is 2,221.
#
# Copper: 155 objects (Webb 1982 Table 14, Claim 43).
#   Source: Great Lakes region (~1,600 km; Webb 1982 Claim 43).

MATERIALS = [
    ('Novaculite',              250,   785, 'Webb 1982 Table 9; Webb 1968 p. 311'),
    ('Quartz crystals',         300,   395, 'Webb 1982 Table 17, p. 64'),
    ('Hematite/magnetite\nplummets', 400, 2790, 'Webb 1982 p. 56'),
    ('Galena',                  800,   740, 'Webb 1982 Claim 44'),
    ('Steatite',                900,  4945, 'Webb 1982 p. 45'),
    ('Copper',                 1600,   155, 'Webb 1982 Table 14'),
]

# Also run analysis excluding the steatite cache (use midden-only count)
MATERIALS_MIDDEN_ONLY = [
    ('Novaculite',              250,   785, 'Webb 1982 Table 9; Webb 1968 p. 311'),
    ('Quartz crystals',         300,   395, 'Webb 1982 Table 17, p. 64'),
    ('Hematite/magnetite\nplummets', 400, 2790, 'Webb 1982 p. 56'),
    ('Galena',                  800,   740, 'Webb 1982 Claim 44'),
    ('Steatite (midden only)',  900,  2221, 'Webb 1982 p. 45'),
    ('Copper',                 1600,   155, 'Webb 1982 Table 14'),
]


def fit_distance_decay(distances, counts):
    """
    Fit p(d) = A * exp(-d / lambda) via log-linear regression.

    In log space: ln(count) = ln(A) - d / lambda
    This is a linear model: y = b0 + b1 * d
    where b1 = -1/lambda, b0 = ln(A).

    Returns: lambda_fit, A_fit, r_squared, slope, intercept, slope_se
    """
    d = np.array(distances, dtype=float)
    c = np.array(counts, dtype=float)
    ln_c = np.log(c)

    result = stats.linregress(d, ln_c)
    slope = result.slope
    intercept = result.intercept
    r_squared = result.rvalue ** 2
    slope_se = result.stderr

    lambda_fit = -1.0 / slope
    A_fit = np.exp(intercept)

    # Confidence interval for lambda via delta method
    # lambda = -1/slope, so d(lambda)/d(slope) = 1/slope^2
    # se(lambda) = |1/slope^2| * se(slope)
    lambda_se = (1.0 / slope**2) * slope_se

    return lambda_fit, A_fit, r_squared, slope, intercept, slope_se, lambda_se


def test_lambda_500(slope, slope_se, n, lambda_test=500.0):
    """
    Test H0: lambda = lambda_test (i.e., slope = -1/lambda_test).

    Uses a t-test on the slope parameter.
    Returns: t_stat, p_value, reject_at_05
    """
    slope_null = -1.0 / lambda_test
    t_stat = (slope - slope_null) / slope_se
    df = n - 2
    p_value = 2.0 * stats.t.sf(abs(t_stat), df)
    return t_stat, p_value, p_value < 0.05


def create_figure(materials_data, lambda_fit, A_fit, r_squared,
                  lambda_se, lambda_test=500.0):
    """Create publication-quality distance-decay figure."""

    names = [m[0] for m in materials_data]
    distances = np.array([m[1] for m in materials_data], dtype=float)
    counts = np.array([m[2] for m in materials_data], dtype=float)

    # Colorblind-friendly palette (Okabe-Ito)
    colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00']

    fig, axes = plt.subplots(1, 2, figsize=(7, 3.5))
    fig.subplots_adjust(wspace=0.38, left=0.10, right=0.97, top=0.92, bottom=0.16)

    # ── Panel A: Log(count) vs distance with fitted line ──
    ax = axes[0]
    ln_counts = np.log(counts)

    for i, (name, d, c) in enumerate(zip(names, distances, counts)):
        ax.scatter(d, np.log(c), color=colors[i], s=80, zorder=5,
                   edgecolors='black', linewidths=0.6)
        # Label placement (hand-tuned to avoid overlaps)
        offset_x = 50
        offset_y = 0.15
        ha = 'left'
        if 'Steatite' in name:
            offset_x = 50
            offset_y = -0.55
        elif 'Galena' in name:
            offset_x = 50
            offset_y = 0.3
        elif 'Copper' in name:
            offset_x = -120
            offset_y = 0.35
            ha = 'right'
        elif 'plummets' in name:
            offset_x = 50
            offset_y = -0.45
        elif 'Quartz' in name:
            offset_x = 50
            offset_y = -0.45
        ax.annotate(name.replace('\n', ' '), xy=(d, np.log(c)),
                    xytext=(d + offset_x, np.log(c) + offset_y),
                    fontsize=7.5, ha=ha,
                    arrowprops=dict(arrowstyle='-', color='gray', lw=0.4))

    # Fitted line
    d_range = np.linspace(0, 1800, 300)
    ln_fitted = np.log(A_fit) - d_range / lambda_fit
    ax.plot(d_range, ln_fitted, 'k-', linewidth=1.8,
            label=f'Fitted: $\\lambda$ = {lambda_fit:.0f} km ($R^2$ = {r_squared:.2f})')

    # Assumed lambda=500 line (scaled to same intercept for comparison)
    ln_assumed = np.log(A_fit) - d_range / lambda_test
    ax.plot(d_range, ln_assumed, '--', color='#CC79A7', linewidth=1.5,
            label=f'Model: $\\lambda$ = {int(lambda_test)} km')

    ax.set_xlabel('Distance from source (km)')
    ax.set_ylabel('ln(artifact count)')
    ax.legend(fontsize=7.5, loc='upper right', framealpha=0.9)
    ax.text(0.03, 0.03, 'A', transform=ax.transAxes, fontsize=14,
            fontweight='bold', va='bottom')
    ax.set_xlim(-50, 1850)

    # ── Panel B: Count vs distance with exponential curves ──
    ax = axes[1]

    for i, (name, d, c) in enumerate(zip(names, distances, counts)):
        ax.scatter(d, c, color=colors[i], s=80, zorder=5,
                   edgecolors='black', linewidths=0.6)
        offset_x = 50
        offset_y = 80
        ha = 'left'
        if 'Steatite' in name:
            offset_x = -80
            offset_y = 200
            ha = 'right'
        elif 'plummets' in name:
            offset_x = 50
            offset_y = 200
        elif 'Galena' in name:
            offset_x = 50
            offset_y = 200
        elif 'Copper' in name:
            offset_x = -120
            offset_y = 150
            ha = 'right'
        elif 'Quartz' in name:
            offset_x = 50
            offset_y = -200
        ax.annotate(name.replace('\n', ' '), xy=(d, c),
                    xytext=(d + offset_x, c + offset_y),
                    fontsize=7.5, ha=ha,
                    arrowprops=dict(arrowstyle='-', color='gray', lw=0.4))

    # Fitted exponential
    count_fitted = A_fit * np.exp(-d_range / lambda_fit)
    ax.plot(d_range, count_fitted, 'k-', linewidth=1.8,
            label=f'Fitted: $\\lambda$ = {lambda_fit:.0f} km')

    # Assumed lambda=500
    count_assumed = A_fit * np.exp(-d_range / lambda_test)
    ax.plot(d_range, count_assumed, '--', color='#CC79A7', linewidth=1.5,
            label=f'Model: $\\lambda$ = {int(lambda_test)} km')

    ax.set_xlabel('Distance from source (km)')
    ax.set_ylabel('Artifact count')
    ax.legend(fontsize=7.5, loc='upper right', framealpha=0.9)
    ax.text(0.03, 0.03, 'B', transform=ax.transAxes, fontsize=14,
            fontweight='bold', va='bottom')
    ax.set_xlim(-50, 1850)
    ax.set_ylim(-100, max(counts) * 1.15)

    return fig


def main():
    print("=" * 70)
    print("Distance-Decay Test: p(d) = exp(-d/lambda) vs Archaeological Data")
    print("=" * 70)

    for label, materials_data in [
        ("All steatite (including cache)", MATERIALS),
        ("Steatite midden-only (excluding 2,724-fragment cache)", MATERIALS_MIDDEN_ONLY),
    ]:
        print(f"\n{'─' * 60}")
        print(f"  Analysis: {label}")
        print(f"{'─' * 60}")

        names = [m[0] for m in materials_data]
        distances = [m[1] for m in materials_data]
        counts = [m[2] for m in materials_data]
        sources = [m[3] for m in materials_data]

        print(f"\n{'Material':<28} {'Distance (km)':>13} {'Count':>8}  Source")
        print("-" * 80)
        for name, d, c, src in zip(names, distances, counts, sources):
            print(f"{name.replace(chr(10), ' '):<28} {d:>13} {c:>8}  {src}")

        # Fit
        lam, A, r2, slope, intercept, slope_se, lam_se = fit_distance_decay(
            distances, counts)

        print(f"\nFitted parameters:")
        print(f"  lambda = {lam:.1f} +/- {lam_se:.1f} km (1 SE)")
        print(f"  lambda 95% CI: [{lam - 1.96*lam_se:.0f}, {lam + 1.96*lam_se:.0f}] km")
        print(f"  A (intercept scale) = {A:.1f}")
        print(f"  R-squared = {r2:.4f}")
        print(f"  Slope = {slope:.6f} +/- {slope_se:.6f}")

        # Test lambda=500
        t_stat, p_val, reject = test_lambda_500(slope, slope_se,
                                                 len(distances), 500.0)
        print(f"\nHypothesis test (H0: lambda = 500 km):")
        print(f"  t-statistic = {t_stat:.3f}")
        print(f"  p-value = {p_val:.4f}")
        print(f"  Reject at alpha=0.05? {'Yes' if reject else 'No'}")

        # Predicted counts under fitted and assumed models
        print(f"\n{'Material':<28} {'Observed':>8} {'Pred (fitted)':>14} "
              f"{'Pred (lam=500)':>15}")
        print("-" * 70)
        for name, d, c in zip(names, distances, counts):
            pred_fit = A * np.exp(-d / lam)
            pred_500 = A * np.exp(-d / 500.0)
            print(f"{name.replace(chr(10), ' '):<28} {c:>8} {pred_fit:>14.0f} "
                  f"{pred_500:>15.0f}")

    # ── Create figure using the full steatite dataset ──
    names = [m[0] for m in MATERIALS]
    distances = [m[1] for m in MATERIALS]
    counts = [m[2] for m in MATERIALS]

    lam, A, r2, slope, intercept, slope_se, lam_se = fit_distance_decay(
        distances, counts)

    fig = create_figure(MATERIALS, lam, A, r2, lam_se, lambda_test=500.0)

    output_png = OUTPUT_DIR / 'figure_distance_decay_test.png'
    fig.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nFigure saved to: {output_png}")

    plt.close(fig)

    # ── Write results markdown ──
    write_results_md(MATERIALS, MATERIALS_MIDDEN_ONLY)


def write_results_md(materials_all, materials_midden):
    """Write detailed results to markdown file."""

    # Fit both datasets
    d_all = [m[1] for m in materials_all]
    c_all = [m[2] for m in materials_all]
    lam_all, A_all, r2_all, sl_all, _, slse_all, lamse_all = \
        fit_distance_decay(d_all, c_all)
    t_all, p_all, rej_all = test_lambda_500(sl_all, slse_all, len(d_all))

    d_mid = [m[1] for m in materials_midden]
    c_mid = [m[2] for m in materials_midden]
    lam_mid, A_mid, r2_mid, sl_mid, _, slse_mid, lamse_mid = \
        fit_distance_decay(d_mid, c_mid)
    t_mid, p_mid, rej_mid = test_lambda_500(sl_mid, slse_mid, len(d_mid))

    md_path = PROJECT_ROOT / 'docs' / 'manuscript' / 'distance_decay_results.md'

    lines = []
    lines.append("# Distance-Decay Test Results")
    lines.append("")
    lines.append("## Data Sources")
    lines.append("")
    lines.append("All artifact counts are drawn from Webb (1968, 1982) as documented in")
    lines.append("the verified claims files (`docs/references/claims/webb_1968_claims.md`")
    lines.append("and `docs/references/claims/webb_1982_claims.md`).")
    lines.append("")
    lines.append("## Archaeological Data")
    lines.append("")
    lines.append("| Material | Distance (km) | Count | Source |")
    lines.append("|----------|--------------|-------|--------|")
    for name, d, c, src in materials_all:
        clean_name = name.replace('\n', ' ')
        lines.append(f"| {clean_name} | {d} | {c:,} | {src} |")
    lines.append("")
    lines.append("### Notes on counts")
    lines.append("")
    lines.append("**Novaculite (785 items):** Calculated from Webb 1982 Table 9 material")
    lines.append("percentages applied to assemblage totals. Projectile points: 6.40% of")
    lines.append("10,214 total = 654 (Webb 1968 p. 311). Microflints: 0.57% of ~23,000")
    lines.append("= ~131 (Webb 1968 p. 312). Total: ~785. Source: Ouachita Mountains,")
    lines.append("AR (~250 km).")
    lines.append("")
    lines.append("**Quartz crystals (395):** Raw material count from Webb 1982 Table 17")
    lines.append("(p. 64). Source: Arkansas near Hot Springs (~300 km; Webb 1956 p. 104).")
    lines.append("")
    lines.append("**Hematite/magnetite plummets (2,790):** Webb 1982 p. 56, Claim 36.")
    lines.append("78% hematite, 22% magnetite. Sources are multiple locations; conservative")
    lines.append("distance estimate ~400 km. Webb interprets as bola weights; Lipo (2012)")
    lines.append("suggests loom weights. Included as clearly non-local material requiring")
    lines.append("long-distance acquisition of heavy iron ores.")
    lines.append("")
    lines.append("**Galena (740):** 702 masses + 38 finished objects. Webb 1982 Claim 44.")
    lines.append("Source: Potosi, Missouri (~800 km), confirmed by trace element analysis")
    lines.append("(Webb 1982 Claim 45).")
    lines.append("")
    lines.append("**Steatite (4,945):** Total fragments: 2,221 from general midden + 2,724")
    lines.append("from cache west of Mound A. Webb 1982 p. 45, Claim 41. Source: NE Alabama /")
    lines.append("NW Georgia (~900 km), confirmed by mineralogical analysis (Webb 1982 Claim 42).")
    lines.append("The cache may represent a single depositional event, so a midden-only analysis")
    lines.append("(2,221 fragments) is also reported.")
    lines.append("")
    lines.append("**Copper (155):** Webb 1982 Table 14, Claim 43. Source: Great Lakes region")
    lines.append("(~1,600 km).")
    lines.append("")

    lines.append("## Model Fit: Full Dataset (all steatite)")
    lines.append("")
    lines.append(f"- Fitted lambda: {lam_all:.0f} km (SE: {lamse_all:.0f} km)")
    lines.append(f"- 95% CI for lambda: [{lam_all - 1.96*lamse_all:.0f}, "
                 f"{lam_all + 1.96*lamse_all:.0f}] km")
    lines.append(f"- R-squared: {r2_all:.4f}")
    lines.append(f"- Scale parameter A: {A_all:.0f}")
    lines.append("")
    lines.append("### Hypothesis test (H0: lambda = 500 km)")
    lines.append("")
    lines.append(f"- t-statistic: {t_all:.3f}")
    lines.append(f"- p-value: {p_all:.4f}")
    lines.append(f"- Reject at alpha = 0.05: {'Yes' if rej_all else 'No'}")
    lines.append("")

    lines.append("### Predicted vs observed counts (full dataset)")
    lines.append("")
    lines.append("| Material | Distance (km) | Observed | Predicted (fitted) | "
                 "Predicted (lambda=500) |")
    lines.append("|----------|--------------|----------|-------------------|"
                 "----------------------|")
    for name, d, c, _ in materials_all:
        pred_fit = A_all * np.exp(-d / lam_all)
        pred_500 = A_all * np.exp(-d / 500.0)
        clean_name = name.replace('\n', ' ')
        lines.append(f"| {clean_name} | {d} | {c:,} | {pred_fit:,.0f} | "
                     f"{pred_500:,.0f} |")
    lines.append("")

    lines.append("## Model Fit: Steatite Midden-Only (excluding cache)")
    lines.append("")
    lines.append(f"- Fitted lambda: {lam_mid:.0f} km (SE: {lamse_mid:.0f} km)")
    lines.append(f"- 95% CI for lambda: [{lam_mid - 1.96*lamse_mid:.0f}, "
                 f"{lam_mid + 1.96*lamse_mid:.0f}] km")
    lines.append(f"- R-squared: {r2_mid:.4f}")
    lines.append(f"- Scale parameter A: {A_mid:.0f}")
    lines.append("")
    lines.append("### Hypothesis test (H0: lambda = 500 km)")
    lines.append("")
    lines.append(f"- t-statistic: {t_mid:.3f}")
    lines.append(f"- p-value: {p_mid:.4f}")
    lines.append(f"- Reject at alpha = 0.05: {'Yes' if rej_mid else 'No'}")
    lines.append("")

    lines.append("## Assessment")
    lines.append("")
    lines.append("The relationship between artifact count and source distance does not follow")
    lines.append("a simple exponential distance-decay pattern. The most conspicuous deviation")
    lines.append("is steatite, which at 900 km has the highest count of any exotic material")
    lines.append("(4,945 fragments, or 2,221 excluding the cache). Similarly, hematite/magnetite")
    lines.append("plummets at ~400 km have very high counts (2,790), while quartz crystals at")
    lines.append("300 km have relatively few (395).")
    lines.append("")
    lines.append("These deviations indicate that raw artifact counts are governed by multiple")
    lines.append("factors beyond transport distance:")
    lines.append("")
    lines.append("1. **Material utility**: Steatite served a practical cooking vessel function,")
    lines.append("   driving demand independent of signaling value. Plummets had utilitarian")
    lines.append("   functions (bola weights or loom weights).")
    lines.append("2. **Fragmentation**: Steatite vessels break into many fragments; a single")
    lines.append("   vessel may contribute dozens of sherds to the count. Copper objects are")
    lines.append("   small and durable.")
    lines.append("3. **Source abundance**: Steatite outcrops in the southern Appalachians are")
    lines.append("   extensive; native copper deposits are geographically constrained.")
    lines.append("4. **Depositional events**: The 2,724-fragment steatite cache may represent")
    lines.append("   a single ritual or storage deposit.")
    lines.append("")
    lines.append("The exponential decay model p(d) = exp(-d/500) is better understood as a")
    lines.append("model of acquisition *probability* per interaction event, not as a predictor")
    lines.append("of raw artifact counts. To properly test the distance-decay prediction,")
    lines.append("counts would need to be normalized by estimated source abundance, vessel")
    lines.append("fragmentation rates, material durability, and utilitarian demand. With only")
    lines.append("six data points and substantial confounds, the archaeological data neither")
    lines.append("confirm nor refute the lambda = 500 km assumption.")
    lines.append("")

    with open(md_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f"Results written to: {md_path}")


if __name__ == '__main__':
    main()
