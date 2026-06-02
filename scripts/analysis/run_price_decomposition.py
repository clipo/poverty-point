#!/usr/bin/env python3
"""Empirical Price-equation decomposition from ABM output.

Restores the multilevel-selection formal apparatus by running simulations
and decomposing year-to-year change in aggregator frequency into:

  (1) Between-strategy selection term: the change in mean aggregator
      frequency p̄ attributable to differential reproductive success
      between aggregator and independent bands. In the binary-strategy
      formulation this is:
          S(t) = (n_agg n_ind / N²) * (w_agg - w_ind) / w̄

  (2) Within-aggregator selection term: covariance between monument
      contribution and fitness within the aggregator cohort, indexing
      whether the cooperation-network reward operates at the within-
      group level. Positive = more investment is rewarded within the
      cohort; negative = free-riding pays.

  (3) Transmission residual: Δp̄ - S(t), capturing cultural-learning
      effects (strategy switching beyond what selection alone delivers).

The framework's MLS prediction is that S(t) and within-aggregator
covariance both go positive above σ*; below σ* both should be
negative or zero.

Runs three scenarios:
  - PP-scenario at σ = 0.64 (above-threshold)
  - Critical σ at 0.40 (near-threshold)
  - Low σ at 0.20 (below-threshold)

Each scenario: 5 replicates × 200 yr, sampling per-band state each year.
"""
import sys
import time
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point')

import numpy as np

from src.poverty_point.integrated_simulation import IntegratedSimulation
from src.poverty_point.parameters import default_parameters
from src.poverty_point.environmental_scenarios import ShortfallParams
from src.poverty_point.agents import Strategy

OUTPUT_DIR = Path('/Users/clipo/PycharmProjects/poverty-point/results/analysis')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

N_REPS = 5
DURATION = 200
BURN_IN = 50
EPS = 0.35
MAG = 0.5


def interval_for_sigma(sigma_target, eps):
    """Solve magnitude × √(20/T) × (1 - ε) = σ for T (mean interval years)."""
    if eps < 1.0:
        sigma_reg = sigma_target / (1 - eps)
    else:
        sigma_reg = sigma_target
    return 20 * (MAG / sigma_reg) ** 2


def snapshot_band_data(sim, _year):
    """Extract per-band data for the current simulated year."""
    bands = sim.bands
    data = []
    for b in bands:
        # Latest fitness in the band's history (this year's realized fitness)
        if len(b.fitness_history) > 0:
            fit = b.fitness_history[-1]
        else:
            fit = float('nan')
        data.append({
            'band_id': b.band_id,
            'strategy': 'agg' if b.strategy == Strategy.AGGREGATOR else 'ind',
            'fitness': float(fit),
            'monument_contributions': float(b.monument_contributions),
            'total_exotic_count': int(b.total_exotic_count),
            'size': int(b.size),
            'quality': float(b.quality),
            'resources': float(b.resources),
            'n_obligations': len(b.obligations),
        })
    return data


def run_scenario_with_snapshots(sigma_target, seed, duration=DURATION):
    """Run a single replicate and return per-year per-band snapshots."""
    T = interval_for_sigma(sigma_target, EPS)
    sp = ShortfallParams(mean_interval=T, magnitude_mean=MAG, magnitude_std=0.15)
    params = default_parameters(sigma=sigma_target, epsilon=EPS, seed=seed)
    params.duration = duration
    params.burn_in = BURN_IN
    sim = IntegratedSimulation(
        params=params,
        shortfall_params=sp,
        seed=seed,
        signal_conditional_partners=True,
    )
    sim.aggregation_site.ecotone_advantage = EPS

    yearly_snapshots = []
    # Step through years using the public step_year method, snapshotting
    # per-band state after each year.
    for year in range(duration):
        sim.step_year()
        snap = snapshot_band_data(sim, year)
        yearly_snapshots.append({'year': year, 'bands': snap})

    return yearly_snapshots


def price_decomposition(snapshots, _burn_in=BURN_IN):
    """Compute Price-equation components year-by-year.

    Returns a dict with year-indexed arrays of:
      delta_p: change in aggregator frequency at year t to t+1
      selection: between-strategy selection term S(t)
      transmission: Δp̄ - S(t)
      within_agg_cov: within-aggregator covariance(M, fitness)
      n_agg, n_ind: counts per year
      w_agg, w_ind: mean fitness per strategy group per year
    """
    years = []
    p_t = []
    delta_p = []
    selection = []
    transmission = []
    within_agg_cov = []
    n_agg = []
    n_ind = []
    w_agg_list = []
    w_ind_list = []

    for t in range(len(snapshots) - 1):
        bands_t = snapshots[t]['bands']
        bands_t1 = snapshots[t + 1]['bands']

        n_t = len(bands_t)
        n_t1 = len(bands_t1)
        if n_t == 0 or n_t1 == 0:
            continue

        # Filter out NaN fitness (initial year, etc.)
        finite_t = [b for b in bands_t if np.isfinite(b['fitness'])]
        if len(finite_t) < 2:
            continue

        agg_t = [b for b in finite_t if b['strategy'] == 'agg']
        ind_t = [b for b in finite_t if b['strategy'] == 'ind']
        if len(agg_t) == 0 or len(ind_t) == 0:
            # No within-strategy variation; selection undefined
            continue

        n_a = len(agg_t)
        n_i = len(ind_t)
        N = n_a + n_i

        w_a = float(np.mean([b['fitness'] for b in agg_t]))
        w_i = float(np.mean([b['fitness'] for b in ind_t]))
        w_bar = (n_a * w_a + n_i * w_i) / N

        if w_bar <= 0 or not np.isfinite(w_bar):
            continue

        # Two-group Price selection term (between strategies)
        # Cov(w_g, p_g) = (n_a n_i / N²) * (w_a - w_i)
        cov_wp = (n_a * n_i / N ** 2) * (w_a - w_i)
        S = cov_wp / w_bar

        # Aggregator frequency at t and t+1
        p_now = n_a / N
        finite_t1 = [b for b in bands_t1 if np.isfinite(b['fitness'])]
        if not finite_t1:
            continue
        n_a1 = sum(1 for b in finite_t1 if b['strategy'] == 'agg')
        p_next = n_a1 / len(finite_t1)
        d_p = p_next - p_now

        # Within-aggregator covariance: corr(monument_contribution, fitness)
        if len(agg_t) >= 3:
            M = np.array([b['monument_contributions'] for b in agg_t])
            W = np.array([b['fitness'] for b in agg_t])
            if M.std(ddof=1) > 1e-9 and W.std(ddof=1) > 1e-9:
                cov_MW = float(np.cov(M, W, ddof=1)[0, 1])
            else:
                cov_MW = 0.0
        else:
            cov_MW = float('nan')

        years.append(snapshots[t]['year'])
        p_t.append(p_now)
        delta_p.append(d_p)
        selection.append(S)
        transmission.append(d_p - S)
        within_agg_cov.append(cov_MW)
        n_agg.append(n_a)
        n_ind.append(n_i)
        w_agg_list.append(w_a)
        w_ind_list.append(w_i)

    return {
        'year': years,
        'p_t': p_t,
        'delta_p': delta_p,
        'selection': selection,
        'transmission': transmission,
        'within_agg_cov': within_agg_cov,
        'n_agg': n_agg,
        'n_ind': n_ind,
        'w_agg': w_agg_list,
        'w_ind': w_ind_list,
    }


def main():
    scenarios = [
        ('low_sigma', 0.20),
        ('near_threshold', 0.40),
        ('pp_scenario', 0.64),
    ]
    t_start = time.time()

    all_results = {}
    for name, sigma_target in scenarios:
        print(f"\n=== Scenario: {name} (σ_target = {sigma_target}) ===", flush=True)
        reps = []
        for rep in range(N_REPS):
            seed = 42 + rep * 100 + int(sigma_target * 1000)
            t1 = time.time()
            snaps = run_scenario_with_snapshots(sigma_target, seed=seed)
            decomp = price_decomposition(snaps)
            reps.append({
                'rep': rep, 'seed': seed,
                'decomposition': decomp,
                'final_p': decomp['p_t'][-1] if decomp['p_t'] else float('nan'),
                'mean_selection_post_burn': (
                    float(np.mean([s for s, y in zip(decomp['selection'], decomp['year'])
                                   if y >= BURN_IN]))
                    if any(y >= BURN_IN for y in decomp['year']) else float('nan')
                ),
                'mean_transmission_post_burn': (
                    float(np.mean([t for t, y in zip(decomp['transmission'], decomp['year'])
                                   if y >= BURN_IN]))
                    if any(y >= BURN_IN for y in decomp['year']) else float('nan')
                ),
                'mean_within_agg_cov_post_burn': (
                    float(np.nanmean([c for c, y in zip(decomp['within_agg_cov'], decomp['year'])
                                      if y >= BURN_IN]))
                    if any(y >= BURN_IN for y in decomp['year']) else float('nan')
                ),
            })
            elapsed = (time.time() - t1) / 60
            print(f"  rep {rep+1}/{N_REPS} (seed={seed}): "
                  f"final p̄ = {reps[-1]['final_p']:.3f}, "
                  f"mean S = {reps[-1]['mean_selection_post_burn']:+.5f}, "
                  f"mean trans = {reps[-1]['mean_transmission_post_burn']:+.5f}, "
                  f"mean within-agg cov = {reps[-1]['mean_within_agg_cov_post_burn']:+.4f}, "
                  f"({elapsed:.1f}m)", flush=True)
        all_results[name] = {'sigma_target': sigma_target, 'reps': reps}

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_file = OUTPUT_DIR / f'price_decomposition_{timestamp}.json'
    with open(out_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\nDone in {(time.time()-t_start)/60:.1f}m. Saved: {out_file}", flush=True)


if __name__ == '__main__':
    main()
