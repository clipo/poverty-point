#!/usr/bin/env python3
"""Pad signaling-vs-cooperation ablation from 6 reps to 20 reps total.

R3 #4 flagged that the n=6 budget was at the edge of replicate noise.
This script reads the existing overnight_sweep.json and adds runs until
each sigma_eff x mode cell has 20 replicates.

Estimated: 14 extra reps x 7 sigma_effs x 2 modes = 196 sims x ~9 min = ~29 hr.
"""
import sys
import os
import time
import json

sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point/src')

from poverty_point.integrated_simulation import IntegratedSimulation
from poverty_point.parameters import default_parameters
from poverty_point.environmental_scenarios import ShortfallParams

EPS = 0.35
MAG = 0.5
TARGET_REPS = 20
DURATION = 200
BURN_IN = 50

def interval_for_sigma_eff(sigma_eff_target):
    sigma_regional_target = sigma_eff_target / (1 - EPS)
    return 20 * (MAG / sigma_regional_target) ** 2

sigma_effs = [0.20, 0.28, 0.36, 0.40, 0.44, 0.50, 0.55]
intervals = {se: interval_for_sigma_eff(se) for se in sigma_effs}

OUTDIR = '/Users/clipo/PycharmProjects/poverty-point/results/ablation'
OUTFILE = os.path.join(OUTDIR, 'overnight_sweep.json')

if not os.path.exists(OUTFILE):
    print(f"ERROR: {OUTFILE} not found; run signal_conditional_ablation_sweep.py first.")
    sys.exit(1)

with open(OUTFILE) as f:
    results = json.load(f)

# Ensure structure
for key in ('mode_signal', 'mode_random', 'realized_sigma_signal', 'realized_sigma_random'):
    if key not in results:
        results[key] = {str(se): [] for se in sigma_effs}

t_start = time.time()
sim_count = 0
n_total_needed = sum(
    max(0, TARGET_REPS - len(results['mode_signal'].get(str(se), [])))
    + max(0, TARGET_REPS - len(results['mode_random'].get(str(se), [])))
    for se in sigma_effs
)
print(f"Padding to {TARGET_REPS} reps total; need to add {n_total_needed} sims", flush=True)

for mode in [True, False]:
    mode_key = 'mode_signal' if mode else 'mode_random'
    sigma_key = 'realized_sigma_signal' if mode else 'realized_sigma_random'
    label = 'signal_conditional' if mode else 'random_partners'
    for se in sigma_effs:
        T = intervals[se]
        existing = len(results[mode_key].get(str(se), []))
        need = TARGET_REPS - existing
        if need <= 0:
            continue
        print(f"\n[{label}] sigma_eff={se:.2f}: have {existing}, need {need} more", flush=True)
        for rep in range(existing, TARGET_REPS):
            sim_count += 1
            seed = 42 + rep + (10000 if not mode else 0) + int(se * 1000)
            t1 = time.time()
            try:
                sp = ShortfallParams(mean_interval=T, magnitude_mean=MAG, magnitude_std=0.15)
                p = default_parameters(sigma=0.5, epsilon=EPS, seed=seed)
                p.duration = DURATION
                p.burn_in = BURN_IN
                sim = IntegratedSimulation(params=p, seed=seed,
                                           shortfall_params=sp,
                                           signal_conditional_partners=mode)
                res = sim.run(verbose=False)
                results[mode_key][str(se)].append(float(res.final_strategy_dominance))
                results[sigma_key][str(se)].append(float(res.mean_effective_sigma))
            except Exception as e:
                print(f"  ERROR rep={rep}: {e}", flush=True)
                continue
            with open(OUTFILE, 'w') as f:
                json.dump(results, f, indent=2)
            elapsed_min = (time.time() - t_start) / 60
            rate = elapsed_min / sim_count
            eta_h = rate * (n_total_needed - sim_count) / 60
            print(f"  rep={rep} dom={res.final_strategy_dominance:+.4f} "
                  f"sigma_eff={res.mean_effective_sigma:.3f} "
                  f"t={time.time()-t1:.0f}s elapsed={elapsed_min:.1f}m eta={eta_h:.1f}h", flush=True)

print(f"\nDone. Added {sim_count} sims in {(time.time()-t_start)/60:.1f} min", flush=True)
