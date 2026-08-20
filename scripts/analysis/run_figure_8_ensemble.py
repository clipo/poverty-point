#!/usr/bin/env python3
"""Re-run Figure 8 temporal-dynamics scenario with 5 replicates.

R3 #4 requested replicate-ensemble shading for the temporal-dynamics
figure (currently a single trajectory). This script runs the PP scenario
for 500 simulated years with 5 random seeds and saves per-year trajectories
for downstream ensemble plotting.
"""
import sys
import time
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point')

from src.poverty_point.integrated_simulation import IntegratedSimulation
from src.poverty_point.parameters import default_parameters
from src.poverty_point.environmental_scenarios import get_scenario

OUTPUT_DIR = Path('/Users/clipo/PycharmProjects/poverty-point/results/analysis')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

N_REPS = 5
DURATION = 500

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
out_file = OUTPUT_DIR / f'figure_8_ensemble_{timestamp}.json'

ensemble = []
t_start = time.time()
for rep in range(N_REPS):
    seed = 42 + rep * 1000
    print(f"=== Replicate {rep+1}/{N_REPS} (seed={seed}) ===", flush=True)
    scenario = get_scenario('poverty_point')
    params = default_parameters(seed=seed)
    params.duration = DURATION
    sim = IntegratedSimulation(
        params=params,
        shortfall_params=scenario.shortfall_params,
        seed=seed,
        signal_conditional_partners=True,
    )
    sim.aggregation_site.ecotone_advantage = scenario.expected_epsilon
    res = sim.run(verbose=False)
    traj = {
        'rep': rep,
        'seed': seed,
        'years': [int(s.year) for s in res.yearly_states],
        'dominance': [float(s.strategy_dominance) for s in res.yearly_states],
        'agg_size': [float(s.aggregation_size) for s in res.yearly_states],
        'monument': [float(s.monument_level) for s in res.yearly_states],
        'shortfall': [bool(s.in_shortfall) for s in res.yearly_states],
    }
    ensemble.append(traj)
    elapsed = (time.time() - t_start) / 60
    print(f"  done. final dominance={traj['dominance'][-1]:+.3f} "
          f"final monument={traj['monument'][-1]:.0f} "
          f"elapsed={elapsed:.1f}m", flush=True)

with open(out_file, 'w') as f:
    json.dump(ensemble, f)
print(f"\nSaved: {out_file} ({(time.time()-t_start)/60:.1f}m total)", flush=True)
