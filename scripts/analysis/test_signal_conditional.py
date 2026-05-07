#!/usr/bin/env python3
"""Compare signal-blind vs signal-conditional partner formation at PP parameters.

Quick feasibility test: does the signal-conditional rule produce qualitatively
different outcomes? Runs three replicates of 100 simulated years per mode at
PP parameters and reports cumulative monument units, exotics, and the
mean obligation count per band (which should respond to the new rule).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))

import numpy as np

from poverty_point.environmental_scenarios import ShortfallParams
from poverty_point.integrated_simulation import IntegratedSimulation
from poverty_point.parameters import default_parameters

# PP-scenario shortfall parameters (from create_fig_calibration.py)
PP_MEAN_INTERVAL = 9.0
PP_MAGNITUDE_MEAN = 0.45
PP_MAGNITUDE_STD = 0.12

YEARS = 50


def run_one(signal_conditional: bool, seed: int):
    sf = ShortfallParams(
        mean_interval=PP_MEAN_INTERVAL,
        magnitude_mean=PP_MAGNITUDE_MEAN,
        magnitude_std=PP_MAGNITUDE_STD,
    )
    params = default_parameters(seed=seed)
    params.duration = YEARS
    sim = IntegratedSimulation(
        params=params,
        shortfall_params=sf,
        seed=seed,
        signal_conditional_partners=signal_conditional,
    )
    sim.run(verbose=False)
    # Read directly from simulation state to avoid burn-in eating the
    # short test interval (default burn_in=100 vs YEARS=50).
    monument_units = float(sim.aggregation_site.monument_level)
    total_exotics = int(sum(
        sum(b.exotic_goods.values()) for b in sim.bands
    ))
    mean_obligations = float(np.mean([
        len(b.obligations) for b in sim.bands
    ]))
    return {
        'monument_units': monument_units,
        'total_exotics': total_exotics,
        'mean_obligations': mean_obligations,
    }


def main():
    print('Comparing signal-blind vs signal-conditional partner formation')
    print(f'  PP scenario, {YEARS} simulated years, 3 replicates per mode')
    print()

    summary = {}
    for mode_name, sc in (('blind', False), ('conditional', True)):
        print(f'  Mode: {mode_name}')
        results = []
        for seed in (1001, 1002):
            t0 = time.time()
            r = run_one(sc, seed)
            dt = time.time() - t0
            print(f'    seed={seed}  units={r["monument_units"]:>7.0f}  '
                  f'exotics={r["total_exotics"]:>5d}  '
                  f'obligs/band={r["mean_obligations"]:>4.1f}  '
                  f'({dt:.1f}s)')
            results.append(r)
        units = np.array([r['monument_units'] for r in results])
        exo = np.array([r['total_exotics'] for r in results])
        obl = np.array([r['mean_obligations'] for r in results])
        print(f'    mean units={units.mean():.0f}+/-{units.std():.0f}, '
              f'exotics={exo.mean():.0f}+/-{exo.std():.0f}, '
              f'obligs={obl.mean():.1f}+/-{obl.std():.1f}')
        summary[mode_name] = {
            'units_mean': units.mean(), 'units_sd': units.std(),
            'exotics_mean': exo.mean(), 'exotics_sd': exo.std(),
            'obligs_mean': obl.mean(), 'obligs_sd': obl.std(),
        }
        print()

    # Compare
    b = summary['blind']
    c = summary['conditional']
    print('Comparison (conditional / blind):')
    print(f"  monument units: {c['units_mean']/b['units_mean']:.2f}x")
    print(f"  total exotics: {c['exotics_mean']/b['exotics_mean']:.2f}x")
    print(f"  obligations/band: {c['obligs_mean']/b['obligs_mean']:.2f}x")


if __name__ == '__main__':
    main()
