#!/usr/bin/env python3
"""Extended sigma sweep for Figure 4A — show full phase transition.

Existing cached sweep (sigma_sweep_20260115_165629.json) tops out at
sigma_eff ~ 0.55 with dominance = -0.23 (mixed but still independent-
majority). To show the figure's narrative -- dominance crossing from
independent-favored to aggregator-favored -- we need a longer sweep
that reaches sigma_eff well above sigma* and a long enough duration
for population dynamics to equilibrate.

This script runs:
- 14 sigma values from 0.20 to 1.00 (target_sigma input; actual_sigma
  comes back lower due to ecotone advantage built into the scenario).
- 800-year duration with 100-year burn-in.
- 3 replicates per sigma.

Runtime: ~60-90 minutes total. Saves result as sigma_sweep_extended_<ts>.json
in results/analysis/.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

import numpy as np

from poverty_point.environmental_scenarios import (
    create_critical_threshold_scenario,
)
from poverty_point.integrated_simulation import IntegratedSimulation
from poverty_point.parameters import default_parameters

OUTPUT_DIR = Path(__file__).resolve().parent.parent / 'results' / 'analysis'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SIGMA_VALUES = np.linspace(0.30, 1.00, 10)
DURATION = 400
BURN_IN = 100
N_REPLICATES = 2
BASE_SEED = 4242


def run_one(target_sigma: float, seed: int) -> dict:
    scenario = create_critical_threshold_scenario(target_sigma=target_sigma)
    params = default_parameters(seed=seed)
    params.duration = DURATION
    params.burn_in = BURN_IN
    sim = IntegratedSimulation(
        params=params,
        env_config=scenario.env_config,
        shortfall_params=scenario.shortfall_params,
        seed=seed,
    )
    res = sim.run(verbose=False)
    return {
        'target_sigma': float(target_sigma),
        'actual_sigma': float(res.mean_effective_sigma),
        'dominance': float(res.final_strategy_dominance),
        'aggregation_size': float(res.mean_aggregation_size),
        'monument_level': float(res.final_monument_level),
        'total_exotics': int(res.total_exotics),
        'mean_population': float(res.mean_population),
    }


def main():
    print(f'Extended sigma sweep: {len(SIGMA_VALUES)} sigma values, '
          f'{DURATION} years, {N_REPLICATES} replicates each')
    print(f'  sigma range: {SIGMA_VALUES[0]:.2f} -> {SIGMA_VALUES[-1]:.2f}')
    print()

    results = []
    t_start = time.time()
    for i, sigma in enumerate(SIGMA_VALUES):
        print(f'[{i+1}/{len(SIGMA_VALUES)}] target_sigma = {sigma:.3f}')
        reps = []
        for r in range(N_REPLICATES):
            seed = BASE_SEED + i * N_REPLICATES + r
            t0 = time.time()
            rep = run_one(sigma, seed=seed)
            dt = time.time() - t0
            print(f'    rep {r+1}: actual_sigma={rep["actual_sigma"]:.3f}  '
                  f'dom={rep["dominance"]:+.2f}  agg={rep["aggregation_size"]:.1f}  '
                  f'mon={rep["monument_level"]:.0f}  ({dt:.0f}s)')
            reps.append(rep)
        avg = {
            'target_sigma': float(sigma),
            'actual_sigma': float(np.mean([r['actual_sigma'] for r in reps])),
            'actual_sigma_std': float(np.std([r['actual_sigma'] for r in reps])),
            'dominance': float(np.mean([r['dominance'] for r in reps])),
            'dominance_std': float(np.std([r['dominance'] for r in reps])),
            'aggregation_size': float(np.mean([r['aggregation_size'] for r in reps])),
            'aggregation_size_std': float(np.std([r['aggregation_size'] for r in reps])),
            'monument_level': float(np.mean([r['monument_level'] for r in reps])),
            'monument_level_std': float(np.std([r['monument_level'] for r in reps])),
            'total_exotics': float(np.mean([r['total_exotics'] for r in reps])),
            'mean_population': float(np.mean([r['mean_population'] for r in reps])),
            'replicates': reps,
        }
        results.append(avg)
        print(f'    avg: actual_sigma={avg["actual_sigma"]:.3f} +/- {avg["actual_sigma_std"]:.3f}, '
              f'dom={avg["dominance"]:+.2f} +/- {avg["dominance_std"]:.2f}')

    total_dt = time.time() - t_start
    print()
    print(f'Total runtime: {total_dt/60:.1f} minutes')

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_path = OUTPUT_DIR / f'sigma_sweep_{timestamp}.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'Saved: {out_path}')


if __name__ == '__main__':
    main()
