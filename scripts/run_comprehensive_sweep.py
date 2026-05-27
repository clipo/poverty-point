#!/usr/bin/env python3
"""
Comprehensive Parameter Sweep for Poverty Point ABM.

Runs systematic parameter sweeps with fine intervals and multiple replicates
to map the design space for behavior emergence.

Sweep types:
1. OAT (one-at-a-time): Each parameter varied while others at defaults
2. Pairwise interaction: Key parameter pairs on 2D grids
3. Null models: Configurations where no aggregation should emerge
4. Robustness: Default config with varying seeds and conditions
5. Phase boundary refinement: Fine grid near sigma* transition

Usage:
    python scripts/run_comprehensive_sweep.py             # Full sweep
    python scripts/run_comprehensive_sweep.py --quick      # Quick sanity check
    python scripts/run_comprehensive_sweep.py --seeds 10   # 10 replicates
    python scripts/run_comprehensive_sweep.py --output-dir results/my_sweep
"""

import sys
sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point-signaling')

import argparse
import json
import time
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from src.poverty_point.integrated_simulation import IntegratedSimulation
from src.poverty_point.environmental_scenarios import (
    create_critical_threshold_scenario, ShortfallParams, EnvironmentalScenario
)
from src.poverty_point.parameters import (
    default_parameters, critical_threshold, SimulationParameters
)
from src.poverty_point.environment import EnvironmentConfig


# ── Default seeds for replicates ──────────────────────────────────────────────

DEFAULT_SEEDS = [42, 137, 256, 389, 501]


# ── Default parameter values (baseline for OAT sweeps) ───────────────────────

DEFAULTS = {
    'sigma': 0.50,
    'epsilon': 0.35,
    'C_travel': 0.12,
    'C_signal': 0.18,
    'C_opportunity': 0.12,
    'alpha_agg': 0.40,
    'beta_ind': 0.75,
    'b_coop': 0.08,
    'n_optimal': 25,
    'R_ind': 1.10,
}


# ── OAT grid definitions ─────────────────────────────────────────────────────

def _make_oat_grids(quick: bool = False) -> Dict[str, np.ndarray]:
    """Create parameter grids for OAT sweeps."""
    if quick:
        return {
            'sigma':        np.linspace(0.10, 0.80, 10),
            'epsilon':      np.linspace(0.00, 0.50, 8),
            'C_travel':     np.linspace(0.00, 0.30, 7),
            'C_signal':     np.linspace(0.00, 0.40, 7),
            'C_opportunity': np.linspace(0.00, 0.30, 7),
            'alpha_agg':    np.linspace(0.10, 0.70, 7),
            'beta_ind':     np.linspace(0.30, 0.90, 7),
            'b_coop':       np.linspace(0.00, 0.30, 7),
            'n_optimal':    np.array([3, 8, 15, 20, 25, 30]),
            'R_ind':        np.linspace(0.90, 1.60, 8),
        }
    return {
        'sigma':        np.arange(0.05, 0.825, 0.025),   # 31 points
        'epsilon':      np.arange(0.00, 0.525, 0.025),   # 21 points
        'C_travel':     np.arange(0.00, 0.32, 0.02),     # 16 points
        'C_signal':     np.arange(0.00, 0.42, 0.02),     # 21 points
        'C_opportunity': np.arange(0.00, 0.32, 0.02),    # 16 points
        'alpha_agg':    np.arange(0.10, 0.75, 0.05),     # 13 points
        'beta_ind':     np.arange(0.30, 0.95, 0.05),     # 13 points
        'b_coop':       np.arange(0.00, 0.32, 0.02),     # 16 points
        'n_optimal':    np.array([3, 5, 8, 10, 13, 16, 20, 25, 28, 30]),  # 10
        'R_ind':        np.arange(0.90, 1.625, 0.05),    # 15 points
    }


# ── Pairwise grid definitions ────────────────────────────────────────────────

def _make_pairwise_grids(quick: bool = False) -> Dict[str, Tuple[np.ndarray, np.ndarray]]:
    """Create parameter grids for pairwise interaction sweeps."""
    if quick:
        return {
            'sigma_epsilon': (
                np.linspace(0.15, 0.75, 8),
                np.linspace(0.05, 0.45, 6),
            ),
            'sigma_C_signal': (
                np.linspace(0.15, 0.75, 8),
                np.linspace(0.02, 0.36, 6),
            ),
            'sigma_b_coop': (
                np.linspace(0.15, 0.75, 8),
                np.linspace(0.00, 0.25, 6),
            ),
            'sigma_R_ind': (
                np.linspace(0.15, 0.75, 8),
                np.linspace(0.90, 1.50, 6),
            ),
            'alpha_agg_beta_ind': (
                np.linspace(0.15, 0.65, 6),
                np.linspace(0.35, 0.85, 6),
            ),
        }
    return {
        'sigma_epsilon': (
            np.linspace(0.10, 0.80, 20),
            np.linspace(0.00, 0.50, 15),
        ),
        'sigma_C_signal': (
            np.linspace(0.10, 0.80, 20),
            np.linspace(0.00, 0.40, 12),
        ),
        'sigma_b_coop': (
            np.linspace(0.10, 0.80, 20),
            np.linspace(0.00, 0.30, 12),
        ),
        'sigma_R_ind': (
            np.linspace(0.10, 0.80, 20),
            np.linspace(0.90, 1.60, 12),
        ),
        'alpha_agg_beta_ind': (
            np.linspace(0.10, 0.70, 12),
            np.linspace(0.30, 0.90, 12),
        ),
    }


# ── Simulation creation and parameter override ───────────────────────────────

def create_configured_simulation(
    overrides: Dict[str, float],
    seed: int = 42,
    duration: int = 300,
    burn_in: int = 50,
) -> IntegratedSimulation:
    """
    Create a simulation with specific parameter overrides applied.

    For 'sigma', uses create_critical_threshold_scenario to set environment.
    For 'epsilon', overrides the aggregation site's ecotone_advantage.
    For other parameters, modifies the corresponding SimulationParameters field.

    Args:
        overrides: Parameter name -> value mapping
        seed: Random seed
        duration: Simulation duration in years
        burn_in: Burn-in years before recording

    Returns:
        Configured IntegratedSimulation ready to run
    """
    target_sigma = overrides.get('sigma', DEFAULTS['sigma'])
    scenario = create_critical_threshold_scenario(target_sigma=target_sigma)

    params = default_parameters(seed=seed)
    params.duration = duration
    params.burn_in = burn_in

    # Apply parameter overrides to SimulationParameters
    for key, value in overrides.items():
        _apply_override(params, key, value)

    sim = IntegratedSimulation(
        params=params,
        env_config=scenario.env_config,
        shortfall_params=scenario.shortfall_params,
        seed=seed,
    )

    # Override epsilon on the aggregation site
    if 'epsilon' in overrides:
        sim.aggregation_site.ecotone_advantage = overrides['epsilon']

    return sim


def _apply_override(params: SimulationParameters, key: str, value: float) -> None:
    """Apply a single parameter override to SimulationParameters."""
    if key == 'sigma':
        params.sigma = value
    elif key == 'epsilon':
        params.epsilon = value
    elif key == 'C_travel':
        params.costs.C_travel = value
    elif key == 'C_signal':
        params.costs.C_signal = value
    elif key == 'C_opportunity':
        params.costs.C_opportunity = value
    elif key == 'alpha_agg':
        params.vulnerability.alpha_agg = value
    elif key == 'beta_ind':
        params.vulnerability.beta_ind = value
    elif key == 'b_coop':
        params.cooperation.b_coop = value
    elif key == 'n_optimal':
        params.cooperation.n_optimal = int(value)
    elif key == 'R_ind':
        params.cooperation.R_ind = value


# ── Running individual simulations ────────────────────────────────────────────

def run_single_point(
    overrides: Dict[str, float],
    seed: int = 42,
    duration: int = 300,
    burn_in: int = 50,
) -> Dict[str, Any]:
    """Run a single simulation and return key metrics."""
    sim = create_configured_simulation(
        overrides=overrides,
        seed=seed,
        duration=duration,
        burn_in=burn_in,
    )
    results = sim.run(verbose=False)

    # Compute sigma* for comparison
    sigma_star = critical_threshold(
        epsilon=sim.aggregation_site.ecotone_advantage,
        n=max(1, results.mean_aggregation_size),
        params=sim.params,
    )

    return {
        'strategy_dominance': float(results.final_strategy_dominance),
        'mean_aggregation_size': float(results.mean_aggregation_size),
        'final_monument_level': float(results.final_monument_level),
        'total_exotics': int(results.total_exotics),
        'mean_population': float(results.mean_population),
        'mean_effective_sigma': float(results.mean_effective_sigma),
        'sigma_star_theoretical': float(sigma_star),
        'aggregation_emerged': bool(results.final_strategy_dominance > -0.5),
    }


def run_replicated_point(
    overrides: Dict[str, float],
    seeds: List[int],
    duration: int = 300,
    burn_in: int = 50,
) -> Dict[str, Any]:
    """
    Run multiple replicates of a single parameter configuration.

    Returns aggregated statistics (mean, std) across replicates.
    """
    individual_runs = []
    for seed in seeds:
        result = run_single_point(
            overrides=overrides,
            seed=seed,
            duration=duration,
            burn_in=burn_in,
        )
        individual_runs.append(result)

    # Aggregate across replicates
    metrics = [
        'strategy_dominance', 'mean_aggregation_size', 'final_monument_level',
        'total_exotics', 'mean_population', 'mean_effective_sigma',
    ]

    aggregated = {
        'overrides': _jsonify(overrides),
        'n_replicates': len(seeds),
    }

    for metric in metrics:
        values = [r[metric] for r in individual_runs]
        aggregated[f'{metric}_mean'] = float(np.mean(values))
        aggregated[f'{metric}_std'] = float(np.std(values))

    # Fraction of runs where aggregation emerged
    aggregated['aggregation_emerged_fraction'] = float(
        np.mean([r['aggregation_emerged'] for r in individual_runs])
    )

    # Theoretical sigma* (same for all seeds)
    aggregated['sigma_star_theoretical'] = individual_runs[0]['sigma_star_theoretical']

    aggregated['individual_runs'] = individual_runs

    return aggregated


# ── Sweep runners ─────────────────────────────────────────────────────────────

def run_oat_sweeps(
    grids: Dict[str, np.ndarray],
    seeds: List[int],
    duration: int = 300,
    burn_in: int = 50,
    output_dir: Optional[Path] = None,
) -> Dict[str, List[Dict]]:
    """
    Run one-at-a-time parameter sweeps.

    Each parameter is varied independently while all others are at defaults.
    """
    total_runs = sum(len(g) for g in grids.values()) * len(seeds)
    print(f"\n{'='*60}")
    print(f"OAT SWEEPS: {len(grids)} parameters, {total_runs} total runs")
    print(f"{'='*60}")

    all_results = {}
    run_count = 0
    t_start = time.time()

    for param_name, values in grids.items():
        param_results = []
        print(f"\n  Sweeping {param_name}: {len(values)} points × {len(seeds)} seeds")

        for val in values:
            overrides = {param_name: float(val)}
            result = run_replicated_point(
                overrides=overrides,
                seeds=seeds,
                duration=duration,
                burn_in=burn_in,
            )
            param_results.append(result)

            run_count += len(seeds)
            _print_progress(run_count, total_runs, t_start)

        all_results[param_name] = param_results

        # Save per-parameter results
        if output_dir:
            oat_dir = output_dir / 'oat'
            oat_dir.mkdir(parents=True, exist_ok=True)
            with open(oat_dir / f'{param_name}.json', 'w') as f:
                json.dump(param_results, f, indent=2)

    return all_results


def run_pairwise_sweeps(
    grids: Dict[str, Tuple[np.ndarray, np.ndarray]],
    seeds: List[int],
    duration: int = 300,
    burn_in: int = 50,
    output_dir: Optional[Path] = None,
) -> Dict[str, List[Dict]]:
    """
    Run pairwise interaction sweeps on 2D grids.

    Each pair is swept on a full grid of both parameters.
    """
    total_runs = sum(len(g[0]) * len(g[1]) for g in grids.values()) * len(seeds)
    print(f"\n{'='*60}")
    print(f"PAIRWISE SWEEPS: {len(grids)} pairs, {total_runs} total runs")
    print(f"{'='*60}")

    all_results = {}
    run_count = 0
    t_start = time.time()

    for pair_name, (grid_a, grid_b) in grids.items():
        param_a, param_b = pair_name.split('_', 1)
        # Handle alpha_agg_beta_ind: split at known boundary
        if pair_name == 'alpha_agg_beta_ind':
            param_a, param_b = 'alpha_agg', 'beta_ind'

        pair_results = []
        n_points = len(grid_a) * len(grid_b)
        print(f"\n  Sweeping {param_a} × {param_b}: "
              f"{len(grid_a)}×{len(grid_b)} = {n_points} points × {len(seeds)} seeds")

        for val_a in grid_a:
            for val_b in grid_b:
                overrides = {param_a: float(val_a), param_b: float(val_b)}
                result = run_replicated_point(
                    overrides=overrides,
                    seeds=seeds,
                    duration=duration,
                    burn_in=burn_in,
                )
                pair_results.append(result)

                run_count += len(seeds)
                _print_progress(run_count, total_runs, t_start)

        all_results[pair_name] = pair_results

        # Save per-pair results
        if output_dir:
            pair_dir = output_dir / 'pairwise'
            pair_dir.mkdir(parents=True, exist_ok=True)
            with open(pair_dir / f'{pair_name}.json', 'w') as f:
                json.dump(pair_results, f, indent=2)

    return all_results


def run_null_models(
    seeds: List[int],
    duration: int = 300,
    burn_in: int = 50,
    output_dir: Optional[Path] = None,
) -> List[Dict]:
    """
    Run null model configurations where aggregation should NOT emerge.

    These test that the model correctly produces independence-dominated
    outcomes under conditions with no incentive for aggregation.
    """
    null_configs = [
        {'name': 'no_uncertainty',
         'overrides': {'sigma': 0.05, 'epsilon': 0.0}},
        {'name': 'no_ecotone',
         'overrides': {'sigma': 0.50, 'epsilon': 0.0}},
        {'name': 'high_cost',
         'overrides': {'C_travel': 0.25, 'C_signal': 0.30, 'C_opportunity': 0.25}},
        {'name': 'no_cooperation',
         'overrides': {'b_coop': 0.0}},
        {'name': 'high_ind_advantage',
         'overrides': {'R_ind': 1.50}},
        {'name': 'low_vulnerability_diff',
         'overrides': {'alpha_agg': 0.60, 'beta_ind': 0.65}},
    ]

    total_runs = len(null_configs) * len(seeds)
    print(f"\n{'='*60}")
    print(f"NULL MODELS: {len(null_configs)} configs, {total_runs} total runs")
    print(f"{'='*60}")

    results = []
    run_count = 0
    t_start = time.time()

    for config in null_configs:
        print(f"\n  {config['name']}: {config['overrides']}")
        result = run_replicated_point(
            overrides=config['overrides'],
            seeds=seeds,
            duration=duration,
            burn_in=burn_in,
        )
        result['null_model_name'] = config['name']
        results.append(result)

        run_count += len(seeds)
        _print_progress(run_count, total_runs, t_start)

    # Save
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_dir / 'null_models.json', 'w') as f:
            json.dump(results, f, indent=2)

    return results


def run_robustness_checks(
    seeds: List[int],
    duration: int = 300,
    burn_in: int = 50,
    output_dir: Optional[Path] = None,
) -> List[Dict]:
    """
    Run robustness checks: default config under varying sigma with two
    ecotone conditions (low epsilon, high epsilon).
    """
    sigma_values = np.linspace(0.20, 0.70, 8)
    epsilon_conditions = [0.20, 0.45]

    total_runs = len(sigma_values) * len(epsilon_conditions) * len(seeds)
    print(f"\n{'='*60}")
    print(f"ROBUSTNESS: {len(sigma_values)} sigmas × {len(epsilon_conditions)} "
          f"conditions, {total_runs} total runs")
    print(f"{'='*60}")

    results = []
    run_count = 0
    t_start = time.time()

    for eps in epsilon_conditions:
        for sig in sigma_values:
            overrides = {'sigma': float(sig), 'epsilon': float(eps)}
            result = run_replicated_point(
                overrides=overrides,
                seeds=seeds,
                duration=duration,
                burn_in=burn_in,
            )
            result['condition'] = f'epsilon={eps:.2f}'
            results.append(result)

            run_count += len(seeds)
            _print_progress(run_count, total_runs, t_start)

    # Save
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_dir / 'robustness.json', 'w') as f:
            json.dump(results, f, indent=2)

    return results


def run_phase_boundary(
    seeds: List[int],
    duration: int = 300,
    burn_in: int = 50,
    quick: bool = False,
    output_dir: Optional[Path] = None,
) -> List[Dict]:
    """
    Fine-grid sweep near the sigma* phase transition boundary.

    Focuses on sigma 0.20-0.50 × epsilon 0.10-0.40 where the transition
    from independence to aggregation occurs.
    """
    if quick:
        n_sigma, n_epsilon = 10, 10
    else:
        n_sigma, n_epsilon = 20, 20

    sigma_values = np.linspace(0.20, 0.50, n_sigma)
    epsilon_values = np.linspace(0.10, 0.40, n_epsilon)

    total_runs = n_sigma * n_epsilon * len(seeds)
    print(f"\n{'='*60}")
    print(f"PHASE BOUNDARY: {n_sigma}×{n_epsilon} grid, {total_runs} total runs")
    print(f"{'='*60}")

    results = []
    run_count = 0
    t_start = time.time()

    for sig in sigma_values:
        for eps in epsilon_values:
            overrides = {'sigma': float(sig), 'epsilon': float(eps)}
            result = run_replicated_point(
                overrides=overrides,
                seeds=seeds,
                duration=duration,
                burn_in=burn_in,
            )

            # Also compute theoretical prediction for this point
            params = default_parameters()
            params.epsilon = float(eps)
            sigma_star = critical_threshold(
                epsilon=float(eps), n=25, params=params
            )
            result['sigma_star_at_epsilon'] = float(sigma_star)
            result['above_threshold'] = bool(float(sig) > sigma_star)

            results.append(result)

            run_count += len(seeds)
            _print_progress(run_count, total_runs, t_start)

    # Save
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_dir / 'phase_boundary.json', 'w') as f:
            json.dump(results, f, indent=2)

    return results


# ── Summary generation ────────────────────────────────────────────────────────

def generate_summary(
    oat_results: Dict,
    pairwise_results: Dict,
    null_results: List,
    robustness_results: List,
    phase_results: List,
    elapsed_seconds: float,
    output_dir: Optional[Path] = None,
) -> Dict:
    """Generate and save a consolidated summary of all sweep results."""
    summary = {
        'timestamp': datetime.now().isoformat(),
        'total_elapsed_seconds': round(elapsed_seconds, 1),
        'oat': {},
        'pairwise': {},
        'null_models': {},
        'robustness': {},
        'phase_boundary': {},
    }

    # OAT summaries: for each parameter, report the value at which
    # aggregation_emerged_fraction crosses 0.5 (transition point)
    for param_name, results in oat_results.items():
        values = [r['overrides'].get(param_name, None) for r in results]
        dom_means = [r['strategy_dominance_mean'] for r in results]
        emerged = [r['aggregation_emerged_fraction'] for r in results]

        # Find transition point
        transition_value = None
        for i in range(len(emerged) - 1):
            if emerged[i] < 0.5 <= emerged[i + 1]:
                # Linear interpolation
                frac = (0.5 - emerged[i]) / (emerged[i + 1] - emerged[i])
                transition_value = values[i] + frac * (values[i + 1] - values[i])
                break

        summary['oat'][param_name] = {
            'n_points': len(results),
            'range': [float(min(values)), float(max(values))],
            'dominance_range': [float(min(dom_means)), float(max(dom_means))],
            'transition_value': float(transition_value) if transition_value else None,
        }

    # Pairwise summaries
    for pair_name, results in pairwise_results.items():
        n_emerged = sum(1 for r in results if r['aggregation_emerged_fraction'] > 0.5)
        summary['pairwise'][pair_name] = {
            'n_points': len(results),
            'n_aggregation_emerged': n_emerged,
            'fraction_emerged': round(n_emerged / len(results), 3) if results else 0,
        }

    # Null model summary
    for r in null_results:
        name = r.get('null_model_name', 'unknown')
        summary['null_models'][name] = {
            'strategy_dominance_mean': r['strategy_dominance_mean'],
            'aggregation_emerged_fraction': r['aggregation_emerged_fraction'],
            'passed': r['aggregation_emerged_fraction'] < 0.3,
        }

    # Robustness summary
    summary['robustness']['n_configs'] = len(robustness_results)
    summary['robustness']['mean_dominance_std'] = float(np.mean([
        r['strategy_dominance_std'] for r in robustness_results
    ]))

    # Phase boundary summary
    if phase_results:
        n_above = sum(1 for r in phase_results if r.get('above_threshold', False))
        n_emerged_above = sum(
            1 for r in phase_results
            if r.get('above_threshold', False) and r['aggregation_emerged_fraction'] > 0.5
        )
        n_below = sum(1 for r in phase_results if not r.get('above_threshold', False))
        n_emerged_below = sum(
            1 for r in phase_results
            if not r.get('above_threshold', False) and r['aggregation_emerged_fraction'] > 0.5
        )
        summary['phase_boundary'] = {
            'n_points': len(phase_results),
            'above_threshold_total': n_above,
            'above_threshold_emerged': n_emerged_above,
            'below_threshold_total': n_below,
            'below_threshold_emerged': n_emerged_below,
            'theory_accuracy': round(
                (n_emerged_above + (n_below - n_emerged_below)) / len(phase_results), 3
            ) if phase_results else None,
        }

    # Save
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_dir / 'sweep_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)

    return summary


# ── Utilities ─────────────────────────────────────────────────────────────────

def _jsonify(obj: Any) -> Any:
    """Convert numpy types to JSON-serializable Python types."""
    if isinstance(obj, dict):
        return {k: _jsonify(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [_jsonify(v) for v in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.bool_):
        return bool(obj)
    return obj


def _print_progress(done: int, total: int, t_start: float) -> None:
    """Print progress bar with ETA."""
    elapsed = time.time() - t_start
    if done > 0:
        rate = done / elapsed
        remaining = (total - done) / rate
        eta_str = f"{remaining/60:.1f}min" if remaining > 60 else f"{remaining:.0f}s"
    else:
        eta_str = "?"

    pct = done / total * 100
    bar_len = 30
    filled = int(bar_len * done / total)
    bar = '#' * filled + '-' * (bar_len - filled)

    print(f"\r    [{bar}] {pct:5.1f}% ({done}/{total}) "
          f"ETA: {eta_str}   ", end='', flush=True)

    if done == total:
        print()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Comprehensive parameter sweep for Poverty Point ABM'
    )
    parser.add_argument('--quick', action='store_true',
                        help='Quick mode: coarser grids, 3 seeds')
    parser.add_argument('--seeds', type=int, default=None,
                        help='Number of seeds (default: 5, quick: 3)')
    parser.add_argument('--duration', type=int, default=300,
                        help='Simulation duration in years (default: 300)')
    parser.add_argument('--burn-in', type=int, default=50,
                        help='Burn-in years (default: 50)')
    parser.add_argument('--output-dir', type=str,
                        default='results/comprehensive_sweep',
                        help='Output directory')
    parser.add_argument('--skip', nargs='+', default=[],
                        choices=['oat', 'pairwise', 'null', 'robustness', 'phase'],
                        help='Skip specific sweep types')
    args = parser.parse_args()

    # Determine seeds
    if args.seeds is not None:
        seeds = DEFAULT_SEEDS[:args.seeds]
    elif args.quick:
        seeds = DEFAULT_SEEDS[:3]
    else:
        seeds = DEFAULT_SEEDS

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Estimate total runs
    oat_grids = _make_oat_grids(quick=args.quick)
    pairwise_grids = _make_pairwise_grids(quick=args.quick)

    n_oat = sum(len(g) for g in oat_grids.values()) * len(seeds)
    n_pairwise = sum(len(a) * len(b) for a, b in pairwise_grids.values()) * len(seeds)
    n_null = 6 * len(seeds)
    n_robust = 8 * 2 * len(seeds)
    n_phase_grid = (10 if args.quick else 20)
    n_phase = n_phase_grid * n_phase_grid * len(seeds)

    skipped_runs = 0
    if 'oat' in args.skip:
        skipped_runs += n_oat
    if 'pairwise' in args.skip:
        skipped_runs += n_pairwise
    if 'null' in args.skip:
        skipped_runs += n_null
    if 'robustness' in args.skip:
        skipped_runs += n_robust
    if 'phase' in args.skip:
        skipped_runs += n_phase

    total_runs = n_oat + n_pairwise + n_null + n_robust + n_phase - skipped_runs

    print("=" * 60)
    print("POVERTY POINT ABM - COMPREHENSIVE PARAMETER SWEEP")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)
    print(f"  Mode: {'QUICK' if args.quick else 'FULL'}")
    print(f"  Seeds: {seeds}")
    print(f"  Duration: {args.duration} years, burn-in: {args.burn_in} years")
    print(f"  Output: {output_dir}")
    print(f"  Estimated runs: {total_runs}")
    print(f"    OAT:        {n_oat:>6} {'(skipped)' if 'oat' in args.skip else ''}")
    print(f"    Pairwise:   {n_pairwise:>6} {'(skipped)' if 'pairwise' in args.skip else ''}")
    print(f"    Null:       {n_null:>6} {'(skipped)' if 'null' in args.skip else ''}")
    print(f"    Robustness: {n_robust:>6} {'(skipped)' if 'robustness' in args.skip else ''}")
    print(f"    Phase:      {n_phase:>6} {'(skipped)' if 'phase' in args.skip else ''}")

    # Estimate runtime
    est_per_run = 0.18  # seconds
    est_total = total_runs * est_per_run
    print(f"  Estimated time: {est_total/60:.1f} minutes")
    print()

    t_global_start = time.time()

    # ── Run sweeps ────────────────────────────────────────────────────────

    oat_results = {}
    if 'oat' not in args.skip:
        oat_results = run_oat_sweeps(
            grids=oat_grids,
            seeds=seeds,
            duration=args.duration,
            burn_in=args.burn_in,
            output_dir=output_dir,
        )

    pairwise_results = {}
    if 'pairwise' not in args.skip:
        pairwise_results = run_pairwise_sweeps(
            grids=pairwise_grids,
            seeds=seeds,
            duration=args.duration,
            burn_in=args.burn_in,
            output_dir=output_dir,
        )

    null_results = []
    if 'null' not in args.skip:
        null_results = run_null_models(
            seeds=seeds,
            duration=args.duration,
            burn_in=args.burn_in,
            output_dir=output_dir,
        )

    robustness_results = []
    if 'robustness' not in args.skip:
        robustness_results = run_robustness_checks(
            seeds=seeds,
            duration=args.duration,
            burn_in=args.burn_in,
            output_dir=output_dir,
        )

    phase_results = []
    if 'phase' not in args.skip:
        phase_results = run_phase_boundary(
            seeds=seeds,
            duration=args.duration,
            burn_in=args.burn_in,
            quick=args.quick,
            output_dir=output_dir,
        )

    # ── Generate summary ──────────────────────────────────────────────────

    elapsed = time.time() - t_global_start
    summary = generate_summary(
        oat_results=oat_results,
        pairwise_results=pairwise_results,
        null_results=null_results,
        robustness_results=robustness_results,
        phase_results=phase_results,
        elapsed_seconds=elapsed,
        output_dir=output_dir,
    )

    # ── Print final report ────────────────────────────────────────────────

    print("\n" + "=" * 60)
    print("SWEEP COMPLETE")
    print("=" * 60)
    print(f"  Total time: {elapsed/60:.1f} minutes ({elapsed:.0f}s)")
    print(f"  Avg per run: {elapsed/max(1,total_runs):.3f}s")

    if oat_results:
        print("\n  OAT Transition Points:")
        for param, info in summary.get('oat', {}).items():
            tv = info.get('transition_value')
            tv_str = f"{tv:.3f}" if tv is not None else "none found"
            print(f"    {param}: {tv_str}  "
                  f"(dom range: {info['dominance_range'][0]:+.2f} to "
                  f"{info['dominance_range'][1]:+.2f})")

    if null_results:
        print("\n  Null Model Validation:")
        for name, info in summary.get('null_models', {}).items():
            status = "PASS" if info['passed'] else "FAIL"
            print(f"    {name}: dom={info['strategy_dominance_mean']:+.2f}, "
                  f"emerged={info['aggregation_emerged_fraction']:.0%} [{status}]")

    if phase_results:
        pb = summary.get('phase_boundary', {})
        print(f"\n  Phase Boundary Accuracy: {pb.get('theory_accuracy', 'N/A')}")
        print(f"    Above threshold: {pb.get('above_threshold_emerged', 0)}/"
              f"{pb.get('above_threshold_total', 0)} emerged")
        print(f"    Below threshold: {pb.get('below_threshold_emerged', 0)}/"
              f"{pb.get('below_threshold_total', 0)} emerged")

    print(f"\n  Results saved to: {output_dir}")


if __name__ == '__main__':
    main()
