"""
Maintenance-to-new-construction ratio R(M_g) under signal depreciation.

The framework's signal-half-life argument (manuscript §2.2) implies that a
mature signaling system must devote a rising share of its labor to
maintenance and signal-renewal events as accumulated stock approaches the
saturation level M_g* = I_g / delta. Decomposing each period's flow under
the geometric depreciation recurrence M_g(t+1) = (1-delta) * M_g(t) + I_g
gives:

    maintenance      = delta * M_g           (offset of depreciation)
    new construction = I_g - delta * M_g     (net stock growth)
    R(M_g)           = maintenance / new = delta * M_g / (I_g - delta * M_g)

R rises monotonically with accumulated stock and diverges at saturation.

This script:
  1. Computes the R(t) trajectory under PP-scenario and WB-scenario
     parameters starting from M_g(0) = 0.
  2. Reports the cumulative maintenance vs cumulative net-new labor
     over each site's documented active interval (PP: 75 yr; WB: 700 yr
     episodic, treated here as continuous for the structural prediction
     and as 4 disjoint episodes for the episodic interpretation).
  3. Operationalizes the prediction archaeologically as event density
     per unit time: a maintenance-dominated regime should produce many
     small renewal events per year, while a growth-dominated regime
     should produce fewer larger initial-construction events with long
     gaps. PP and WB sit on opposite sides of this prediction in the
     existing record (Hargrave et al. 2021; Clay 2023; Saunders et al.
     2005).

Output: results/sensitivity/renovation_ratio.json
"""
from pathlib import Path
import json
import sys

# Add repo root for src import
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.poverty_point.signaling_core import (  # noqa: E402
    SignalingParams,
    NetworkParams,
    ConflictParams,
    AggregationParams,
    lambda_total_at_sigma,
    monument_stock_step,
)


def equilibrium_I_g(sigma: float, n_bands: int) -> tuple[float, float, float]:
    """Return (M_g*, I_g, delta) at fixed-point equilibrium for the scenario."""
    sig_params = SignalingParams()
    eq = lambda_total_at_sigma(
        sigma=sigma,
        sig_params=sig_params,
        net_params=NetworkParams(),
        conf_params=ConflictParams(),
        agg_params=AggregationParams(),
        n_bands=n_bands,
    )
    return float(eq["M_g"]), float(eq["I_g"]), float(sig_params.delta)


def trajectory_R(I_g: float, delta: float, T_years: int) -> dict:
    """Simulate M_g(t) and R(t) for T_years starting from M_g(0) = 0.

    Returns a dict with year-by-year M_g, maintenance flow, new flow,
    R, plus cumulative totals.
    """
    M = 0.0
    M_series = []
    maintenance_series = []
    new_series = []
    R_series = []
    for _ in range(T_years):
        M_series.append(M)
        # Maintenance and new at the START of the year (before this year's flow)
        maintenance = delta * M
        new = I_g - maintenance
        maintenance_series.append(maintenance)
        new_series.append(new)
        # R(M_g) at this year's stock
        if new > 0:
            R_series.append(maintenance / new)
        else:
            R_series.append(float("inf"))
        # Advance stock
        M = monument_stock_step(M, I_g, delta)
    cumulative_maintenance = float(sum(maintenance_series))
    cumulative_new = float(sum(new_series))
    cumulative_R = (
        cumulative_maintenance / cumulative_new
        if cumulative_new > 0 else float("inf")
    )
    return {
        "T_years": T_years,
        "I_g": I_g,
        "delta": delta,
        "M_g_steady_state": I_g / delta,
        "M_g_at_T": float(M),
        "M_g_series": [float(x) for x in M_series],
        "maintenance_flow_series": [float(x) for x in maintenance_series],
        "new_flow_series": [float(x) for x in new_series],
        "R_series": [float(x) for x in R_series],
        "cumulative_maintenance_units": cumulative_maintenance,
        "cumulative_new_units": cumulative_new,
        "cumulative_total_units": cumulative_maintenance + cumulative_new,
        "cumulative_R": cumulative_R,
        "maintenance_share": (
            cumulative_maintenance / (cumulative_maintenance + cumulative_new)
            if (cumulative_maintenance + cumulative_new) > 0 else 0.0
        ),
    }


def episodic_trajectory(
    I_g: float, delta: float, episodes: list[tuple[int, int]]
) -> dict:
    """Simulate stock with explicit on/off episodes.

    episodes : list of (start_year, duration_years) tuples
        I_g is applied during the episode; zero otherwise. M_g still
        depreciates each year. Used for the Watson Brake episodic
        interpretation (Saunders et al. 2005 documents 200+ year
        inter-stage gaps).
    """
    if not episodes:
        return {"empty": True}
    total_T = max(start + dur for start, dur in episodes) + 100
    active_years = set()
    for start, dur in episodes:
        for t in range(start, start + dur):
            active_years.add(t)
    M = 0.0
    M_series = []
    maintenance_series = []
    new_series = []
    R_series = []
    for t in range(total_T):
        M_series.append(M)
        I_t = I_g if t in active_years else 0.0
        maintenance = delta * M
        new = I_t - maintenance
        maintenance_series.append(maintenance)
        new_series.append(new)
        if I_t > 0 and new > 0:
            R_series.append(maintenance / new)
        else:
            R_series.append(0.0 if I_t == 0 else float("inf"))
        M = monument_stock_step(M, I_t, delta)
    cumulative_maintenance = float(sum(max(0.0, x) for x in maintenance_series))
    cumulative_new = float(sum(max(0.0, x) for x in new_series))
    cumulative_R = (
        cumulative_maintenance / cumulative_new
        if cumulative_new > 0 else float("inf")
    )
    return {
        "total_T_years": total_T,
        "I_g_active": I_g,
        "delta": delta,
        "active_year_count": len(active_years),
        "episodes": [{"start": s, "duration": d} for s, d in episodes],
        "M_g_at_T": float(M),
        "cumulative_maintenance_units": cumulative_maintenance,
        "cumulative_new_units": cumulative_new,
        "cumulative_R": cumulative_R,
        "maintenance_share": (
            cumulative_maintenance / (cumulative_maintenance + cumulative_new)
            if (cumulative_maintenance + cumulative_new) > 0 else 0.0
        ),
        "M_g_series_decimated": [float(M_series[t]) for t in range(0, total_T, 25)],
    }


def main() -> None:
    out_dir = Path("results/sensitivity")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Renovation-to-new-construction ratio R(M_g) for PP and WB")
    print("=" * 70)

    # --- Scenario equilibria ---------------------------------------------
    # PP scenario: sigma = 0.64 (paleoclimate central), n_bands = 25
    pp_M_eq, pp_I_g, pp_delta = equilibrium_I_g(sigma=0.64, n_bands=25)
    print(f"\nPP equilibrium: M_g* = {pp_M_eq:.2f}, I_g = {pp_I_g:.3f}, "
          f"delta = {pp_delta:.3f}")
    print(f"  Depreciation timescale 1/delta = {1.0/pp_delta:.1f} yr")

    # WB scenario: sigma ≈ 0.56 (mid-Holocene LMV), n_bands ≈ 8
    wb_M_eq, wb_I_g, wb_delta = equilibrium_I_g(sigma=0.56, n_bands=8)
    print(f"\nWB equilibrium: M_g* = {wb_M_eq:.2f}, I_g = {wb_I_g:.3f}, "
          f"delta = {wb_delta:.3f}")

    # --- Trajectories ----------------------------------------------------
    # PP: 75-year active interval (Kidder & Grooms 2024 Bayesian analysis)
    pp_traj = trajectory_R(I_g=pp_I_g, delta=pp_delta, T_years=75)
    print(f"\nPP 75-year trajectory:")
    print(f"  M_g at year 75   = {pp_traj['M_g_at_T']:.2f}")
    print(f"  fraction of M_g* = {pp_traj['M_g_at_T']/pp_traj['M_g_steady_state']:.3f}")
    print(f"  Cumulative R     = {pp_traj['cumulative_R']:.2f}")
    print(f"  Maintenance share of total labor = "
          f"{pp_traj['maintenance_share']*100:.1f}%")

    # WB continuous interpretation: 700 years constant I_g
    wb_traj_cont = trajectory_R(I_g=wb_I_g, delta=wb_delta, T_years=700)
    print(f"\nWB 700-year continuous trajectory:")
    print(f"  M_g at year 700  = {wb_traj_cont['M_g_at_T']:.2f}")
    print(f"  Cumulative R     = {wb_traj_cont['cumulative_R']:.2f}")
    print(f"  Maintenance share of total labor = "
          f"{wb_traj_cont['maintenance_share']*100:.1f}%")

    # WB episodic interpretation: 4 episodes spread over 700 years
    # Saunders et al. 2005: WB construction proceeded in episodes
    # separated by 200+ year hiatuses. We model 4 episodes of 50 yr each.
    wb_episodes = [(0, 50), (250, 50), (450, 50), (650, 50)]
    wb_traj_epi = episodic_trajectory(
        I_g=wb_I_g, delta=wb_delta, episodes=wb_episodes
    )
    print(f"\nWB episodic trajectory (4 episodes x 50 yr, 200 yr gaps):")
    print(f"  Total span        = {wb_traj_epi['total_T_years']} yr")
    print(f"  Active years      = {wb_traj_epi['active_year_count']}")
    print(f"  Cumulative R      = {wb_traj_epi['cumulative_R']:.2f}")
    print(f"  Maintenance share = "
          f"{wb_traj_epi['maintenance_share']*100:.1f}%")

    # --- Event-density operationalization --------------------------------
    # The framework's R prediction maps onto archaeological event density:
    # a maintenance-dominated regime produces many small renewal events
    # per unit time; a growth-dominated regime produces fewer initial-
    # construction events with long gaps.
    #
    # PP archaeology (Hargrave et al. 2021; Clay 2023):
    #   - 64 distinct ridge construction components
    #   - 16 sequential prepared surfaces beneath Mound C
    #   - Repeated build-decommission-rebuild cycles in plaza post circles
    #   - Estimated >= 100 distinct construction events in the 75-year
    #     active interval -> event density >= 1.3/yr
    #
    # WB archaeology (Saunders et al. 2005):
    #   - 11 mounds + connecting ridges over 700-year episodic interval
    #   - 200+ year inter-stage gaps
    #   - Estimated ~11-20 distinct construction events over 700 yr
    #     -> event density ~ 0.02-0.03/yr
    #
    # Ratio: PP event density / WB event density ~ 50-100x.
    pp_event_count_lower = 100
    wb_event_count_lower = 11
    wb_event_count_upper = 20
    pp_density = pp_event_count_lower / 75.0
    wb_density_low = wb_event_count_lower / 700.0
    wb_density_high = wb_event_count_upper / 700.0
    print(f"\nEvent-density operationalization:")
    print(f"  PP (>=100 events / 75 yr)  = {pp_density:.3f} events/yr")
    print(f"  WB (11-20 events / 700 yr) = {wb_density_low:.4f}-"
          f"{wb_density_high:.4f} events/yr")
    print(f"  PP/WB ratio                = "
          f"{pp_density/wb_density_high:.1f}x to {pp_density/wb_density_low:.1f}x")

    # --- Save JSON -------------------------------------------------------
    output = {
        "description": (
            "Maintenance-to-new-construction ratio R(M_g) under signal "
            "depreciation. Derived from the geometric recurrence "
            "M_g(t+1) = (1-delta)*M_g(t) + I_g. R rises monotonically "
            "with M_g and diverges at the steady state M_g* = I_g/delta. "
            "PP operated at near-saturation for most of its 75-year "
            "active interval; WB operated far from saturation throughout "
            "its 700-year episodic interval. The framework therefore "
            "predicts PP should show maintenance/renewal-dominated labor "
            "and high event density per unit time, while WB should show "
            "initial-construction-dominated labor and low event density."
        ),
        "PP_scenario": {
            "sigma": 0.64,
            "n_bands": 25,
            "active_interval_years": 75,
            "M_g_steady_state": pp_M_eq,
            "I_g_per_year": pp_I_g,
            "delta": pp_delta,
            "depreciation_timescale_years": 1.0 / pp_delta,
            "trajectory": pp_traj,
        },
        "WB_scenario_continuous": {
            "sigma": 0.56,
            "n_bands": 8,
            "active_interval_years": 700,
            "M_g_steady_state": wb_M_eq,
            "I_g_per_year": wb_I_g,
            "delta": wb_delta,
            "trajectory": wb_traj_cont,
        },
        "WB_scenario_episodic": {
            "sigma": 0.56,
            "n_bands": 8,
            "interpretation": "Saunders et al. 2005 documents episodic WB "
                              "construction with 200+ yr inter-stage gaps; "
                              "modeled as 4 episodes x 50 yr separated by "
                              "200 yr hiatuses.",
            "M_g_steady_state": wb_M_eq,
            "I_g_per_year_active": wb_I_g,
            "delta": wb_delta,
            "trajectory": wb_traj_epi,
        },
        "event_density_test": {
            "framing": (
                "R operationalized archaeologically as event density per "
                "unit time: maintenance-dominated regime -> many small "
                "renewal events; growth-dominated -> fewer initial "
                "construction events with long gaps."
            ),
            "PP": {
                "source": "Hargrave et al. 2021; Clay 2023; Ortmann & Kidder 2013",
                "evidence": "64 ridge components + 16 surfaces beneath Mound C "
                            "+ build-decommission-rebuild plaza post circles",
                "event_count_lower_bound": pp_event_count_lower,
                "active_interval_years": 75,
                "event_density_per_year_lower_bound": pp_density,
            },
            "WB": {
                "source": "Saunders et al. 2005",
                "evidence": "11 mounds + connecting ridges over 700 yr "
                            "episodic interval with 200+ yr inter-stage gaps",
                "event_count_range": [wb_event_count_lower, wb_event_count_upper],
                "active_interval_years": 700,
                "event_density_per_year_range": [
                    wb_density_low, wb_density_high
                ],
            },
            "PP_to_WB_density_ratio_range": [
                pp_density / wb_density_high,
                pp_density / wb_density_low,
            ],
            "framework_prediction": (
                "PP/WB event-density ratio should be substantially > 1 "
                "(framework predicts ~10x or more given the M_g and "
                "active-interval contrasts). Observed ratio of ~50-100x "
                "is qualitatively consistent. The prediction is "
                "structural rather than precise because the model's "
                "I_g and the archaeological event count are not "
                "calibrated to a common unit; what is tested is the "
                "direction and order of magnitude of the contrast."
            ),
        },
        "caveats": [
            "R is derived under constant-I_g assumption; PP's active "
            "interval may have been compressed with peak labor at the "
            "start and gradual tail (Kidder et al. 2021), which the "
            "constant-I_g approximation does not capture.",
            "Archaeological event counts include both maintenance/renewal "
            "(prepared surfaces, post-circle rebuilds, re-cappings) and "
            "new-construction (initial mound stages, new ridges) events; "
            "the framework's maintenance-vs-new split is not directly "
            "separable in the published archaeology.",
            "WB episodic structure is approximated as 4 x 50 yr blocks "
            "with 200 yr gaps; the published WB chronology (Saunders et "
            "al. 2005) shows actual episode timing differing from this "
            "simplification.",
            "The prediction is structural (R rises with stock; PP > WB) "
            "rather than quantitative; precise R values would require "
            "labor-resolved chronology not currently available.",
        ],
    }

    out_path = out_dir / "renovation_ratio.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
