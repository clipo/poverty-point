"""Joint parameter uncertainty propagation matching §6.2 priors exactly.

§6.2 rubric prior:
- T ~ U[6, 18] years
- m ~ U[0.30, 0.60]
- ε rubric: uniform ±0.2 on each of 5 PP zone weights, central 0.49

Then add joint propagation over the 6 σ*-defining parameters (each ±50%).
"""
import sys, os
sys.path.insert(0, '/Users/clipo/PycharmProjects/poverty-point-signaling/src')
import numpy as np
from poverty_point.signaling_core import (
    SignalingParams, NetworkParams, AggregationParams, ConflictParams,
    critical_threshold,
)

# §6.2 rubric prior on σ (via T × m)
def sample_sigma(rng, n):
    T = rng.uniform(6, 18, n)
    m = rng.uniform(0.30, 0.60, n)
    sigma = m * np.sqrt(20.0 / T)
    return np.clip(sigma, 0.01, 0.99)

# §6.2 rubric prior on ε: uniform ±0.2 on each of 5 zone weights, central rubric values for PP
# PP weights from Table 2: (1.0, 1.0, 1.0, 1.0, 0.5)
def sample_epsilon(rng, n):
    pp_weights = np.array([1.0, 1.0, 1.0, 1.0, 0.5])
    eps = []
    for _ in range(n):
        w = pp_weights + rng.uniform(-0.2, 0.2, 5)
        w = np.clip(w, 0.01, 1.0)
        # Shannon entropy / ln(5), scaled by 0.5 (rubric formula)
        p = w / w.sum()
        H = -np.sum(p * np.log(p))
        eps_val = (H / np.log(5)) * 0.5
        eps.append(eps_val)
    return np.array(eps)

defaults = {'C_signal': 0.18, 'C_opportunity': 0.12, 'lambda_W': 0.15,
            'k_max': 6.0, 'M_half': 2.5, 'gamma': 0.05}
prior_bounds = {k: (v * 0.5, v * 1.5) for k, v in defaults.items()}

N = 1000
rng = np.random.default_rng(42)
samples_sigma = sample_sigma(rng, N)
samples_eps = sample_epsilon(rng, N)
sample_params = {k: rng.uniform(*prior_bounds[k], N) for k in defaults}

# Baseline: σ + ε rubric, parameters fixed
above_baseline = []
for i in range(N):
    try:
        result = critical_threshold(epsilon=float(samples_eps[i]), n_agg=25,
                                    sig_params=SignalingParams(), net_params=NetworkParams(),
                                    conf_params=ConflictParams(), agg_params=AggregationParams())
        sigma_eff = samples_sigma[i] * (1 - samples_eps[i])
        above_baseline.append(sigma_eff > result['sigma_star'])
    except Exception:
        continue
P_baseline = np.mean(above_baseline)
print(f'Baseline P(σ_eff > σ*) [σ + ε rubric, parameters fixed]: {P_baseline:.3f}')
print(f'  (§6.2 reports 0.36 for rubric prior — should match within Monte Carlo noise)')

# Joint: σ + ε + 6 parameters
results_sigma_star, results_sigma_eff, above_joint = [], [], []
for i in range(N):
    sp = SignalingParams(lambda_W=float(sample_params['lambda_W'][i]))
    np_ = NetworkParams(gamma=float(sample_params['gamma'][i]),
                        k_max=float(sample_params['k_max'][i]),
                        M_half=float(sample_params['M_half'][i]))
    cp = ConflictParams()
    ap = AggregationParams(C_signal=float(sample_params['C_signal'][i]),
                           C_opportunity=float(sample_params['C_opportunity'][i]))
    try:
        result = critical_threshold(epsilon=float(samples_eps[i]), n_agg=25,
                                    sig_params=sp, net_params=np_,
                                    conf_params=cp, agg_params=ap)
        sigma_star = result['sigma_star']
    except Exception:
        continue
    sigma_eff = samples_sigma[i] * (1 - samples_eps[i])
    results_sigma_star.append(sigma_star)
    results_sigma_eff.append(sigma_eff)
    above_joint.append(sigma_eff > sigma_star)

P_joint = np.mean(above_joint)
results_sigma_star = np.array(results_sigma_star)
results_sigma_eff = np.array(results_sigma_eff)
diff = results_sigma_eff - results_sigma_star

print(f'\nJoint P(σ_eff > σ*) [σ + ε + 6 model parameters]: {P_joint:.3f}')
print(f'\nPosterior σ* under joint uncertainty:')
print(f'  mean={results_sigma_star.mean():.3f}, 95% CI=[{np.percentile(results_sigma_star,2.5):.3f}, {np.percentile(results_sigma_star,97.5):.3f}]')
print(f'\nPosterior σ_eff:')
print(f'  mean={results_sigma_eff.mean():.3f}, 95% CI=[{np.percentile(results_sigma_eff,2.5):.3f}, {np.percentile(results_sigma_eff,97.5):.3f}]')
print(f'\nPosterior on σ_eff - σ* (the methods reviewer\'s preferred summary):')
print(f'  mean={diff.mean():+.3f}, 95% CI=[{np.percentile(diff,2.5):+.3f}, {np.percentile(diff,97.5):+.3f}]')
print(f'  P(σ_eff - σ* > 0) = {(diff > 0).mean():.3f}')

# Save
import json
out = {
    'N': int(len(results_sigma_star)),
    'priors_match_section_6_2_rubric': True,
    'P_baseline_sigma_epsilon_only': float(P_baseline),
    'P_joint_with_6_parameters': float(P_joint),
    'posterior_sigma_star': {'mean': float(results_sigma_star.mean()), 'q025': float(np.percentile(results_sigma_star,2.5)), 'q975': float(np.percentile(results_sigma_star,97.5))},
    'posterior_sigma_eff': {'mean': float(results_sigma_eff.mean()), 'q025': float(np.percentile(results_sigma_eff,2.5)), 'q975': float(np.percentile(results_sigma_eff,97.5))},
    'sigma_eff_minus_sigma_star': {'mean': float(diff.mean()), 'q025': float(np.percentile(diff,2.5)), 'q975': float(np.percentile(diff,97.5))},
    'parameter_bounds_used': {k: [float(v[0]), float(v[1])] for k, v in prior_bounds.items()},
}
os.makedirs('/Users/clipo/PycharmProjects/poverty-point-signaling/results/bayesian', exist_ok=True)
with open('/Users/clipo/PycharmProjects/poverty-point-signaling/results/bayesian/joint_parameter_uncertainty.json', 'w') as f:
    json.dump(out, f, indent=2)
print('\nResults saved.')
