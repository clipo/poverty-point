"""Overnight sweep: phase transition rerun + signal-conditional ablation.

Runs at PP-scenario parameters with σ_eff controlled via ShortfallParams.
Saves intermediate results after each cell so partial data is preserved
if the run is interrupted.

Sweep design:
- 7 σ_eff values spanning 0.20 to 0.55
- 6 replicates per cell
- 2 modes (signal_conditional={True, False})
- Total: 7 × 6 × 2 = 84 simulations
- Estimated runtime at ~9 min/sim: ~12.6 hours
"""
import sys, os, time, json
sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point-signaling/src')
import numpy as np
from poverty_point.integrated_simulation import IntegratedSimulation
from poverty_point.parameters import default_parameters
from poverty_point.environmental_scenarios import ShortfallParams

# σ_eff_target = magnitude_mean × √(20 / mean_interval) × (1 - ε)
# Hold ε = 0.35, magnitude_mean = 0.5, vary mean_interval
EPS = 0.35
MAG = 0.5

def interval_for_sigma_eff(sigma_eff_target):
    """Solve magnitude × √(20/T) × (1 - ε) = σ_eff for T."""
    sigma_regional_target = sigma_eff_target / (1 - EPS)
    # sigma_regional = MAG × √(20/T) → T = 20 × (MAG/sigma_regional)²
    T = 20 * (MAG / sigma_regional_target) ** 2
    return T

sigma_effs = [0.20, 0.28, 0.36, 0.40, 0.44, 0.50, 0.55]
n_replicates = 6
duration = 200
burn_in = 50

intervals = {se: interval_for_sigma_eff(se) for se in sigma_effs}
print("σ_eff target → mean_interval (years):", flush=True)
for se in sigma_effs:
    print(f"  {se:.2f} → T = {intervals[se]:.2f}", flush=True)
print(flush=True)

# Output paths
OUTDIR = '/Users/clipo/PycharmProjects/poverty-point-signaling/results/ablation'
os.makedirs(OUTDIR, exist_ok=True)
OUTFILE = os.path.join(OUTDIR, 'overnight_sweep.json')

# Load existing partial results if any
if os.path.exists(OUTFILE):
    with open(OUTFILE) as f:
        results = json.load(f)
    print(f"Loaded existing results with {sum(len(v.get('mode_signal',{}).get(str(se),[])) + len(v.get('mode_random',{}).get(str(se),[])) for se in sigma_effs for v in [results])} entries", flush=True)
else:
    results = {
        'sigma_effs': sigma_effs,
        'n_replicates': n_replicates,
        'duration': duration,
        'burn_in': burn_in,
        'epsilon': EPS,
        'magnitude_mean': MAG,
        'intervals': {str(k): v for k, v in intervals.items()},
        'mode_signal': {str(se): [] for se in sigma_effs},
        'mode_random': {str(se): [] for se in sigma_effs},
        'realized_sigma_signal': {str(se): [] for se in sigma_effs},
        'realized_sigma_random': {str(se): [] for se in sigma_effs},
    }

t_start = time.time()
sim_count = 0
n_total = len(sigma_effs) * n_replicates * 2

for mode in [True, False]:
    mode_key = 'mode_signal' if mode else 'mode_random'
    sigma_key = 'realized_sigma_signal' if mode else 'realized_sigma_random'
    label = 'signal_conditional' if mode else 'random_partners'
    print(f"\n=== Mode: {label} ===", flush=True)
    for sigma_eff_target in sigma_effs:
        T = intervals[sigma_eff_target]
        already = len(results[mode_key][str(sigma_eff_target)])
        for rep in range(already, n_replicates):
            sim_count += 1
            seed = 42 + rep + (10000 if not mode else 0) + int(sigma_eff_target * 1000)
            t1 = time.time()
            try:
                sp = ShortfallParams(mean_interval=T, magnitude_mean=MAG, magnitude_std=0.15)
                p = default_parameters(sigma=0.5, epsilon=EPS, seed=seed)  # sigma here is unused
                p.duration = duration
                p.burn_in = burn_in
                sim = IntegratedSimulation(params=p, seed=seed,
                                           shortfall_params=sp,
                                           signal_conditional_partners=mode)
                res = sim.run(verbose=False)
                results[mode_key][str(sigma_eff_target)].append(float(res.final_strategy_dominance))
                results[sigma_key][str(sigma_eff_target)].append(float(res.mean_effective_sigma))
            except Exception as e:
                print(f"  σ_eff={sigma_eff_target:.2f} rep={rep}: ERROR {e}", flush=True)
                continue
            t2 = time.time()
            elapsed_min = (time.time() - t_start) / 60
            est_total_min = elapsed_min * n_total / max(sim_count, 1)
            print(f"  σ_eff={sigma_eff_target:.2f} rep={rep}: dom={res.final_strategy_dominance:+.3f} realized_σ={res.mean_effective_sigma:.3f} ({t2-t1:.1f}s) [{sim_count}/{n_total}, {elapsed_min:.0f}m elapsed, ~{est_total_min:.0f}m total]", flush=True)
            # Save intermediate after every sim
            with open(OUTFILE, 'w') as f:
                json.dump(results, f, indent=2)
        vals = results[mode_key][str(sigma_eff_target)]
        if vals:
            m = np.mean(vals); sd = np.std(vals, ddof=1) if len(vals)>1 else 0
            print(f"  σ_eff={sigma_eff_target:.2f} ({label}): mean dom = {m:+.3f} ± {sd:.3f} (n={len(vals)})", flush=True)

t_total = time.time() - t_start
print(f"\nTotal: {t_total/60:.1f} min ({sim_count} new sims)", flush=True)

# Final analysis
print(f"\n=== Final results ===", flush=True)
for mode_key, label in [('mode_signal', 'signal_conditional'), ('mode_random', 'random_partners')]:
    print(f"\n{label}:", flush=True)
    for se in sigma_effs:
        vals = results[mode_key][str(se)]
        if vals:
            m = np.mean(vals); sd = np.std(vals, ddof=1) if len(vals)>1 else 0
            real_se = np.mean(results[f'realized_sigma_{"signal" if mode_key=="mode_signal" else "random"}'][str(se)])
            print(f"  σ_eff={se:.2f} (realized {real_se:.3f}): dom = {m:+.3f} ± {sd:.3f} (n={len(vals)})", flush=True)

def find_threshold(d):
    sorted_se = sorted(d.keys(), key=lambda x: float(x))
    means = [np.mean(d[se]) if d[se] else None for se in sorted_se]
    pairs = [(float(se), m) for se, m in zip(sorted_se, means) if m is not None]
    for i in range(len(pairs)-1):
        if pairs[i][1] <= 0 < pairs[i+1][1]:
            sa, ma = pairs[i]; sb, mb = pairs[i+1]
            return sa + (0 - ma) / (mb - ma) * (sb - sa) if mb != ma else sa
    return None

ts = find_threshold(results['mode_signal'])
tr = find_threshold(results['mode_random'])
print(f"\n=== Thresholds ===", flush=True)
print(f"Signal-conditional partners: σ_eff* ≈ {ts}", flush=True)
print(f"Random partner formation:    σ_eff* ≈ {tr}", flush=True)
if ts and tr:
    shift = tr - ts; pct = 100*shift/ts
    print(f"Shift (random - signal): {shift:+.3f} ({pct:+.1f}%)", flush=True)
    print(f"Interpretation: positive shift means signaling apparatus lowers threshold; if shift is large, signaling does discriminating work", flush=True)
print("\nDONE.", flush=True)
