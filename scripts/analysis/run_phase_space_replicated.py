#!/usr/bin/env python3
"""Phase space at 5 replicates per cell.

Reviewer R3 requested replicate spread on the (sigma, epsilon) phase space.
Original run was n=1 per cell with seed=42. This rerun uses n=5 per cell.

12x10 grid x 5 reps x 300 yr duration. Saves intermediate results after each
cell so partial data is preserved if interrupted.
"""
import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point')

import numpy as np

from src.poverty_point.integrated_simulation import IntegratedSimulation
from src.poverty_point.environmental_scenarios import create_critical_threshold_scenario
from src.poverty_point.parameters import default_parameters, critical_threshold

OUTPUT_DIR = Path('/Users/clipo/PycharmProjects/poverty-point/results/analysis')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

N_SIGMA = 12
N_EPS = 10
N_REPS = 5
DURATION = 300
BURN_IN = 50

sigma_values = np.linspace(0.25, 0.85, N_SIGMA)
epsilon_values = np.linspace(0.05, 0.50, N_EPS)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
out_file = OUTPUT_DIR / f'phase_space_replicated_{timestamp}.json'
partial_file = OUTPUT_DIR / 'phase_space_replicated_partial.json'

# Resume if partial exists
if partial_file.exists():
    with open(partial_file) as f:
        results = json.load(f)
    print(f"Resuming from partial: {len(results)} cell-reps already done", flush=True)
else:
    results = []

done_keys = {(r['target_sigma'], r['epsilon'], r['rep']) for r in results}

total = N_SIGMA * N_EPS * N_REPS
t_start = time.time()
sim_count = 0

print(f"Phase space replicated: {N_SIGMA}x{N_EPS} grid, {N_REPS} reps, {DURATION} yr", flush=True)
print(f"Total simulations: {total}", flush=True)
print(f"Output: {out_file}", flush=True)

for i, target_sigma in enumerate(sigma_values):
    for j, epsilon in enumerate(epsilon_values):
        for rep in range(N_REPS):
            key = (float(target_sigma), float(epsilon), rep)
            if key in done_keys:
                continue

            sim_count += 1
            seed = 42 + rep * 1000 + i * 100 + j

            scenario = create_critical_threshold_scenario(target_sigma=target_sigma)
            scenario.env_config.ecotone_base_productivity = 0.5 + epsilon * 0.4
            scenario.expected_epsilon = epsilon

            params = default_parameters(seed=seed)
            params.duration = DURATION
            params.burn_in = BURN_IN

            sim = IntegratedSimulation(
                params=params,
                env_config=scenario.env_config,
                shortfall_params=scenario.shortfall_params,
                seed=seed,
                signal_conditional_partners=True,
            )
            sim.aggregation_site.ecotone_advantage = epsilon
            res = sim.run(verbose=False)

            sigma_star = critical_threshold(epsilon=epsilon, n=25, params=params)

            results.append({
                'target_sigma': float(target_sigma),
                'epsilon': float(epsilon),
                'rep': rep,
                'seed': seed,
                'actual_sigma': float(res.mean_effective_sigma),
                'dominance': float(res.final_strategy_dominance),
                'aggregation_size': float(res.mean_aggregation_size),
                'monument_level': float(res.final_monument_level),
                'sigma_star_theoretical': float(sigma_star),
                'above_threshold': bool(float(res.mean_effective_sigma) > float(sigma_star)),
            })

            # Save partial every 5 cells
            if sim_count % 5 == 0:
                with open(partial_file, 'w') as f:
                    json.dump(results, f, indent=2)
                elapsed = (time.time() - t_start) / 60
                rate = elapsed / sim_count
                eta = rate * (total - len(results)) / 60
                print(f"  [{len(results)}/{total}] sigma={target_sigma:.2f} eps={epsilon:.2f} rep={rep} "
                      f"elapsed={elapsed:.1f}m rate={rate:.2f}m/sim eta={eta:.1f}h", flush=True)

# Final save
with open(out_file, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nDone. {len(results)} sims in {(time.time()-t_start)/60:.1f} min", flush=True)
print(f"Saved: {out_file}", flush=True)
