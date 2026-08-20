"""Calibration replicates for the S7.2 table and the §6.1 anchor.

Runs each of the four environmental scenarios (low, poverty_point,
critical, high) for 8 stochastic replicates of 200 simulated years,
recording final cumulative monument units, total exotic items, and
per-material exotic counts. The aggregation-site ecotone advantage is
pinned to the scenario's expected epsilon rather than the emergent
environment-derived value.

Output: results/calibration_replicates/replicates_n8_d200.json
(schema: {scenario: [{monument_units, exotics_total,
exotics_by_material}, ...]})
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.poverty_point.integrated_simulation import IntegratedSimulation
from src.poverty_point.parameters import default_parameters
from src.poverty_point.environmental_scenarios import get_scenario

N_REPLICATES = 8
DURATION = 200
BURN_IN = 50
SCENARIO_NAMES = ['low', 'poverty_point', 'critical', 'high']

OUT = Path('results/calibration_replicates/replicates_n8_d200.json')


def main():
    results = {}
    t0 = time.time()
    for name in SCENARIO_NAMES:
        scenario = get_scenario(name)
        rows = []
        for rep in range(N_REPLICATES):
            seed = 1000 + rep
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
            sim.aggregation_site.ecotone_advantage = scenario.expected_epsilon
            res = sim.run(verbose=False)
            final = res.yearly_states[-1]
            rows.append({
                'monument_units': float(final.monument_level),
                'exotics_total': int(final.total_exotics),
                'exotics_by_material': {
                    k: int(v) for k, v in
                    final.exotic_counts_by_material.items()
                },
                'mean_aggregation_size': float(res.mean_aggregation_size),
                'mean_effective_sigma': float(res.mean_effective_sigma),
            })
            print(f"{name} rep {rep}: monument={final.monument_level:.0f} "
                  f"exotics={final.total_exotics}", flush=True)
        results[name] = rows
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {OUT} in {time.time()-t0:.0f}s")


if __name__ == '__main__':
    main()
