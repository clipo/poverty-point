#!/usr/bin/env python3
"""Factorial channel ablation.

R3 #9: turn each signaling/ecotone channel off (lambda_W, lambda_C, lambda_X, ε)
individually and in factorial combination. Report threshold shift per channel.

Channels:
  W: lambda_W (within-group social reward)
  C: lambda_C (conflict deterrence)
  X: lambda_X (cooperation network value)
  E: epsilon (ecotone buffering)

2^4 = 16 cells, each at PP-scenario parameters, n=8 reps per cell, 200 yr duration.
Outcome: equilibrium strategy dominance (final_strategy_dominance) at sigma_eff = 0.40
(just above canonical sigma*).
"""
import sys
import time
import json
from dataclasses import replace
from pathlib import Path
from datetime import datetime
from itertools import product

sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point/src')

from poverty_point.integrated_simulation import IntegratedSimulation
from poverty_point.parameters import default_parameters
from poverty_point.environmental_scenarios import ShortfallParams

OUTPUT_DIR = Path('/Users/clipo/PycharmProjects/poverty-point/results/ablation')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

N_REPS = 8
DURATION = 200
BURN_IN = 50
SIGMA_EFF_TARGET = 0.40
EPSILON_BASE = 0.35
MAG = 0.5

# sigma_eff = mag * sqrt(20/T) * (1 - eps) → solve for T given eps and target
def interval_for(sigma_eff_target, eps):
    if eps < 1.0:
        sigma_reg = sigma_eff_target / (1 - eps)
    else:
        sigma_reg = sigma_eff_target
    return 20 * (MAG / sigma_reg) ** 2

channels = ['W', 'C', 'X', 'E']
cells = list(product([True, False], repeat=4))  # 16 cells: True = channel ON
print(f"Factorial channel ablation: {len(cells)} cells x {N_REPS} reps = {len(cells)*N_REPS} sims", flush=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
out_file = OUTPUT_DIR / f'factorial_channel_ablation_{timestamp}.json'
partial_file = OUTPUT_DIR / 'factorial_channel_ablation_partial.json'

if partial_file.exists():
    with open(partial_file) as f:
        results = json.load(f)
    print(f"Resuming from {len(results)} entries", flush=True)
else:
    results = []

done = {(r['W'], r['C'], r['X'], r['E'], r['rep']) for r in results}

t_start = time.time()
n_done = len(results)
n_total = len(cells) * N_REPS

for cell in cells:
    W_on, C_on, X_on, E_on = cell
    eps = EPSILON_BASE if E_on else 0.0
    T = interval_for(SIGMA_EFF_TARGET, eps)
    for rep in range(N_REPS):
        key = (W_on, C_on, X_on, E_on, rep)
        if key in done:
            continue
        seed = 42 + rep + 1000 * (1 if W_on else 0) + 2000 * (1 if C_on else 0) \
               + 4000 * (1 if X_on else 0) + 8000 * (1 if E_on else 0)
        n_done += 1
        t1 = time.time()
        try:
            sp = ShortfallParams(mean_interval=T, magnitude_mean=MAG, magnitude_std=0.15)
            p = default_parameters(sigma=0.5, epsilon=eps, seed=seed)
            p.duration = DURATION
            p.burn_in = BURN_IN
            # Zero out channels that are OFF (SignalingParams is frozen, so use replace)
            new_sig = replace(
                p.signaling,
                lambda_W=p.signaling.lambda_W if W_on else 0.0,
                lambda_C=p.signaling.lambda_C if C_on else 0.0,
                lambda_X=p.signaling.lambda_X if X_on else 0.0,
            )
            p.signaling = new_sig
            sim = IntegratedSimulation(params=p, seed=seed,
                                       shortfall_params=sp,
                                       signal_conditional_partners=True)
            sim.aggregation_site.ecotone_advantage = eps
            res = sim.run(verbose=False)
            results.append({
                'W': W_on, 'C': C_on, 'X': X_on, 'E': E_on,
                'rep': rep, 'seed': seed,
                'dominance': float(res.final_strategy_dominance),
                'sigma_eff': float(res.mean_effective_sigma),
                'monument_level': float(res.final_monument_level),
                'aggregation_size': float(res.mean_aggregation_size),
            })
        except Exception as e:
            print(f"ERROR cell={cell} rep={rep}: {e}", flush=True)
            continue
        with open(partial_file, 'w') as f:
            json.dump(results, f, indent=2)
        elapsed = (time.time() - t_start) / 60
        rate = elapsed / max(1, n_done - len(results) + (n_done - len([r for r in results if (r['W'],r['C'],r['X'],r['E'],r['rep']) in done])))
        eta = (n_total - n_done) * (elapsed / max(1, n_done)) / 60
        flags = ''.join(c if cell[i] else c.lower() for i, c in enumerate(channels))
        print(f"  [{n_done}/{n_total}] {flags} rep={rep} dom={res.final_strategy_dominance:+.4f} "
              f"t={time.time()-t1:.0f}s elapsed={elapsed:.1f}m eta={eta:.1f}h", flush=True)

with open(out_file, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nDone in {(time.time()-t_start)/60:.1f}m. Saved: {out_file}", flush=True)
