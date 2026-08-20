"""Memory-effect sensitivity probe (§3 / §S3.1).

The strategy-decision rule nudges the fitness difference by ±0.05 based on
a band's recent five-year fitness relative to its long-term mean. This
probe measures whether removing that memory adjustment shifts the
simulated threshold location: it runs the PP-scenario sweep across five
sigma targets spanning the threshold, with the memory effect on and off
(5 replicates per cell), and interpolates the dominance zero-crossing in
realized sigma for each arm.

Output: results/sensitivity/memory_effect_probe.json
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.poverty_point.integrated_simulation import IntegratedSimulation  # noqa: E402
from src.poverty_point.parameters import default_parameters  # noqa: E402
from src.poverty_point.environmental_scenarios import ShortfallParams  # noqa: E402

EPS = 0.35
MAG = 0.5
SIGMA_TARGETS = [0.12, 0.16, 0.20, 0.24, 0.28, 0.36]
N_REPS = 5
DURATION = 200
BURN_IN = 50


def interval_for_sigma_eff(sigma_eff_target):
    sigma_regional = sigma_eff_target / (1 - EPS)
    return 20 * (MAG / sigma_regional) ** 2


def crossing(pairs):
    """Interpolate the dominance zero-crossing in realized sigma."""
    pairs = sorted(pairs)
    for (s0, d0), (s1, d1) in zip(pairs, pairs[1:]):
        if d0 <= 0 < d1:
            return s0 + (0 - d0) / (d1 - d0) * (s1 - s0)
    return None


def main():
    t0 = time.time()
    results = {}
    for memory in (True, False):
        label = 'memory_on' if memory else 'memory_off'
        cells = []
        for target in SIGMA_TARGETS:
            T = interval_for_sigma_eff(target)
            doms, sigmas = [], []
            for rep in range(N_REPS):
                seed = 7000 + rep + int(target * 1000) + (50000 if not memory else 0)
                params = default_parameters(seed=seed)
                params.duration = DURATION
                params.burn_in = BURN_IN
                sim = IntegratedSimulation(
                    params=params,
                    shortfall_params=ShortfallParams(
                        mean_interval=T, magnitude_mean=MAG),
                    seed=seed,
                    signal_conditional_partners=True,
                    memory_effect=memory,
                )
                sim.aggregation_site.ecotone_advantage = EPS
                res = sim.run(verbose=False)
                doms.append(float(res.final_strategy_dominance))
                sigmas.append(float(res.mean_effective_sigma))
            cells.append({
                'sigma_target': target,
                'mean_realized_sigma': float(np.mean(sigmas)),
                'mean_dominance': float(np.mean(doms)),
                'sd_dominance': float(np.std(doms, ddof=1)),
            })
            print(f"{label} target={target:.2f}: dom={np.mean(doms):+.3f} "
                  f"± {np.std(doms, ddof=1):.3f} (realized σ {np.mean(sigmas):.3f})",
                  flush=True)
        thr = crossing([(c['mean_realized_sigma'], c['mean_dominance'])
                        for c in cells])
        results[label] = {'cells': cells, 'threshold_realized_sigma': thr}
        print(f"{label}: threshold ≈ {thr}", flush=True)

    on = results['memory_on']['threshold_realized_sigma']
    off = results['memory_off']['threshold_realized_sigma']
    shift = (off - on) if (on is not None and off is not None) else None
    results['threshold_shift_off_minus_on'] = shift
    print(f"\nThreshold shift (memory off − on): {shift}")

    out = Path('results/sensitivity/memory_effect_probe.json')
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {out} ({time.time()-t0:.0f}s)")


if __name__ == '__main__':
    main()
