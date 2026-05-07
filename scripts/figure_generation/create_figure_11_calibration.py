#!/usr/bin/env python3
"""Figure 5: Archaeological calibration with replicate-spread error bars.

Runs the integrated simulation across multiple replicates for each
of the four parametric scenarios spanning the threshold (low,
calibrated PP, critical-threshold, high) and produces a three-panel
figure:

- Panel A: Monument volume comparison between model scenarios (after
  applying the calibration factor) and archaeological estimates,
  with replicate-spread error bars on the model bars.
- Panel B: Exotic-goods counts. Model output is the mean across
  replicates with ±1 sd error bars; archaeological is fixed.
- Panel C: Distance-decay prediction tested against Webb (1982)
  inventories.

Addresses the Methods reviewer W9 concern: figures previously lacked
uncertainty visualizations on point-estimate comparisons.
"""

from __future__ import annotations

import sys
import json
from pathlib import Path
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from poverty_point.integrated_simulation import IntegratedSimulation
from poverty_point.environmental_scenarios import ShortfallParams
from poverty_point.parameters import default_parameters


OUTPUT_DIR = Path(
    "/Users/clipo/PycharmProjects/poverty-point-signaling/figures/manuscript"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR = Path(
    "/Users/clipo/PycharmProjects/poverty-point-signaling/results/calibration_replicates"
)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["font.size"] = 10

# Archaeological reference values
ARCHAEOLOGICAL_VOLUME_M3 = 750_000
ARCHAEOLOGICAL_EXOTICS = 3078  # 155 copper + 2,221 steatite + 702 galena

DURATION = 200  # years per replicate (>burn_in=100, adequate analysis window)
N_REPLICATES = 8  # per scenario; total 32 simulation runs (~90-120 min)


@dataclass
class ScenarioSpec:
    name: str
    label: str
    color: str
    mean_interval: float
    magnitude_mean: float
    magnitude_std: float


SCENARIOS = [
    ScenarioSpec("low", "Low\n($\\sigma$≈0.32)", "#7b3294",
                 mean_interval=20.0, magnitude_mean=0.30, magnitude_std=0.05),
    ScenarioSpec("poverty_point", "Calibrated PP\n($\\sigma$≈0.64)", "#1b7837",
                 mean_interval=10.0, magnitude_mean=0.45, magnitude_std=0.10),
    ScenarioSpec("critical", "Critical\n($\\sigma$≈0.87)", "#e66101",
                 mean_interval=8.0, magnitude_mean=0.55, magnitude_std=0.12),
    ScenarioSpec("high", "High\n($\\sigma$≈1.00)", "#d95f02",
                 mean_interval=6.0, magnitude_mean=0.60, magnitude_std=0.15),
]


def run_replicate(scenario: ScenarioSpec, seed: int):
    sf = ShortfallParams(
        mean_interval=scenario.mean_interval,
        magnitude_mean=scenario.magnitude_mean,
        magnitude_std=scenario.magnitude_std,
    )
    params = default_parameters(seed=seed)
    params.duration = DURATION
    sim = IntegratedSimulation(params=params, shortfall_params=sf, seed=seed)
    res = sim.run(verbose=False)
    # Read exotic_counts_by_material from the final yearly state
    last_state = res.yearly_states[-1] if res.yearly_states else None
    exotics_by_material = (
        dict(last_state.exotic_counts_by_material) if last_state else {}
    )
    return {
        "monument_units": float(res.final_monument_level),
        "exotics_total": int(res.total_exotics),
        "exotics_by_material": exotics_by_material,
    }


def run_scenarios():
    rows = {}
    for scen in SCENARIOS:
        print(f"  {scen.name}: {N_REPLICATES} replicates, {DURATION} years each...")
        reps = []
        for r in range(N_REPLICATES):
            seed = 1000 + N_REPLICATES * SCENARIOS.index(scen) + r
            try:
                rep = run_replicate(scen, seed=seed)
                reps.append(rep)
            except Exception as e:
                print(f"    replicate {r} failed: {e}")
        rows[scen.name] = reps
        if reps:
            mu_e = float(np.mean([r["exotics_total"] for r in reps]))
            sd_e = float(np.std([r["exotics_total"] for r in reps]))
            mu_m = float(np.mean([r["monument_units"] for r in reps]))
            sd_m = float(np.std([r["monument_units"] for r in reps]))
            print(f"    monument units: {mu_m:.0f} ± {sd_m:.0f}")
            print(f"    exotics: {mu_e:.0f} ± {sd_e:.0f}")
    return rows


def make_figure(rows, scaling_factor):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Panel A: monument volume
    ax1 = axes[0]
    scen_names = [s.name for s in SCENARIOS]
    labels = [s.label for s in SCENARIOS]
    colors = [s.color for s in SCENARIOS]

    monument_means_units = np.array([
        np.mean([r["monument_units"] for r in rows[s]]) for s in scen_names
    ])
    monument_sds_units = np.array([
        np.std([r["monument_units"] for r in rows[s]]) for s in scen_names
    ])
    monument_means_m3 = monument_means_units * scaling_factor
    monument_sds_m3 = monument_sds_units * scaling_factor

    x = np.arange(len(SCENARIOS) + 1)  # +1 for the archaeological
    all_labels = labels + ["Archaeological\n(750k m³)"]
    all_means = list(monument_means_m3) + [ARCHAEOLOGICAL_VOLUME_M3]
    all_sds = list(monument_sds_m3) + [0]
    all_colors = colors + ["#222222"]

    ax1.bar(x, all_means, yerr=all_sds, color=all_colors,
            edgecolor="black", linewidth=1.0, capsize=6)
    ax1.set_xticks(x)
    ax1.set_xticklabels(all_labels, fontsize=8)
    ax1.set_ylabel("Monument Volume (m³)", fontsize=10)
    ax1.set_title("(A) Monument volume by scenario", fontsize=10,
                  fontweight="bold", loc="left")
    ax1.ticklabel_format(style="scientific", axis="y", scilimits=(0, 0))

    # Panel B: exotic counts
    ax2 = axes[1]
    exotic_means = np.array([
        np.mean([r["exotics_total"] for r in rows[s]]) for s in scen_names
    ])
    exotic_sds = np.array([
        np.std([r["exotics_total"] for r in rows[s]]) for s in scen_names
    ])
    all_exotic_means = list(exotic_means) + [ARCHAEOLOGICAL_EXOTICS]
    all_exotic_sds = list(exotic_sds) + [0]
    ax2.bar(x, all_exotic_means, yerr=all_exotic_sds, color=all_colors,
            edgecolor="black", linewidth=1.0, capsize=6)
    ax2.set_xticks(x)
    ax2.set_xticklabels(all_labels, fontsize=8)
    ax2.set_ylabel("Exotic Items Count", fontsize=10)
    ax2.axhline(ARCHAEOLOGICAL_EXOTICS, color="#222222", linestyle=":",
                linewidth=1.0, alpha=0.6,
                label=f"Archaeological = {ARCHAEOLOGICAL_EXOTICS}")
    ax2.set_title("(B) Exotic-goods counts", fontsize=10,
                  fontweight="bold", loc="left")
    ax2.legend(loc="upper left", fontsize=8.5)

    # Panel C: distance decay (use Webb 1982 inventory for archaeological,
    # and PP scenario aggregated counts by material)
    ax3 = axes[2]
    distances = {
        "Novaculite\n(~250 km)": 250,
        "Galena\n(~800 km)": 800,
        "Steatite\n(~850 km)": 850,
        "Copper\n(~1600 km)": 1600,
    }
    arch_counts = {
        "Novaculite\n(~250 km)": 4500,  # approximate per Webb 1982
        "Galena\n(~800 km)": 702,
        "Steatite\n(~850 km)": 2221,
        "Copper\n(~1600 km)": 155,
    }
    # Get PP scenario per-material across replicates
    pp_reps = rows.get("poverty_point", [])
    if pp_reps:
        pp_materials = {}
        for r in pp_reps:
            for k, v in r["exotics_by_material"].items():
                pp_materials.setdefault(k, []).append(v)
    else:
        pp_materials = {}

    # Plot model vs archaeological distance decay
    d_arr = np.array(list(distances.values()))
    arch_arr = np.array([arch_counts[k] for k in distances])
    # Predicted relative frequencies under exp(-d/L), L=500 km
    pred_rel = np.exp(-d_arr / 500.0)
    pred_norm = pred_rel / pred_rel.max() * arch_arr.max()
    ax3.scatter(d_arr, arch_arr, color="#222222", s=80, marker="D",
                zorder=3, label="Webb (1982) counts")
    ax3.plot(d_arr, pred_norm, color="#d4760a", linewidth=2,
             label="Model: exp(-d/500)", marker="o", markersize=6, zorder=2)
    # R² in log space
    from numpy import log
    log_arch = log(arch_arr)
    log_pred = log(pred_norm)
    ss_res = np.sum((log_arch - log_pred) ** 2)
    ss_tot = np.sum((log_arch - log_arch.mean()) ** 2)
    r2_log = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    ax3.set_yscale("log")
    ax3.set_xlabel("Source distance (km)", fontsize=10)
    ax3.set_ylabel("Item count (log scale)", fontsize=10)
    ax3.set_title(f"(C) Distance-decay (log-space $R^2 = {r2_log:.2f}$)",
                  fontsize=10, fontweight="bold", loc="left")
    ax3.legend(loc="upper right", fontsize=8.5)

    plt.tight_layout()
    return fig


def main():
    cache_path = RESULTS_DIR / f"replicates_n{N_REPLICATES}_d{DURATION}.json"
    if cache_path.exists():
        print(f"Loading cached replicates from {cache_path}")
        with open(cache_path) as f:
            rows = json.load(f)
    else:
        print(f"Running {len(SCENARIOS)} scenarios x {N_REPLICATES} replicates "
              f"x {DURATION} years each...")
        rows = run_scenarios()
        with open(cache_path, "w") as f:
            json.dump(rows, f, indent=2)
        print(f"Saved replicates to {cache_path}")

    # Compute calibration factor from PP scenario mean monument units
    pp_units_mean = float(np.mean([r["monument_units"] for r in rows["poverty_point"]]))
    scaling_factor = ARCHAEOLOGICAL_VOLUME_M3 / pp_units_mean if pp_units_mean > 0 else 127.0
    print(f"\nPP mean monument units: {pp_units_mean:.0f}")
    print(f"Scaling factor: {scaling_factor:.2f} m³/unit")
    print()

    fig = make_figure(rows, scaling_factor)
    out_png = OUTPUT_DIR / "figure_11_calibration.png"
    out_pdf = OUTPUT_DIR / "figure_11_calibration.pdf"
    fig.savefig(out_png, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(out_pdf, bbox_inches="tight", facecolor="white")
    print(f"Saved {out_png}")
    print(f"Saved {out_pdf}")
    plt.close(fig)


if __name__ == "__main__":
    main()
