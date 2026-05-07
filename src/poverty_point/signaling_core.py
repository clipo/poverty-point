"""
Multilevel signaling framework adapted for Poverty Point aggregation dynamics.

Adapts the three-layer monument-MLS model for seasonal hunter-gatherer
aggregation. Adds Layer 0 (aggregation decision) and modifies Layer 3
for seasonal network persistence.

Layers:
    0 - Aggregation decision (new for mobile HG)
    1 - Individual/band signaling equilibrium (Grafen 1990, Spence 1973)
    2 - Intergroup assessment and conflict (Enquist & Leimar 1983)
    3 - Cooperation networks and crisis buffering (Winterhalder 1986)

Mathematical functions only; no simulation state.
"""

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import norm


# ═══════════════════════════════════════════════════════════════════════
# Parameter Dataclasses
# ═══════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class SignalingParams:
    """Parameters for the signaling equilibrium (Layer 1).

    For Poverty Point, quality q maps to band productive capacity:
    the ability to mobilize labor for construction and procurement of
    exotics. A band with q=2.0 can field twice the surplus labor of
    a band with q=1.0.
    """
    q_min: float = 0.2
    q_max: float = 2.0
    lambda_W: float = 0.15      # Within-group social rewards
    lambda_C: float = 0.10      # Conflict deterrence value (initial seed)
    lambda_X: float = 0.15      # Cooperation network value (initial seed)
    delta: float = 0.08         # Monument depreciation rate per year
    rho_monument: float = 0.90  # Monument signal fidelity (earth < stone)
    rho_exotic: float = 0.70    # Exotic goods signal fidelity


@dataclass(frozen=True)
class NetworkParams:
    """Parameters for cooperation network (Layer 3).

    Lower than monument-mls defaults because aggregation is seasonal:
    networks form during aggregation and partially decay during dispersal.
    """
    gamma: float = 0.05         # Buffering efficiency per partner
    k_0: float = 0.3            # Baseline network degree (kinship only)
    k_max: float = 6.0          # Max additional signal-based partners
    M_half: float = 2.5         # Half-saturation monument stock
    # Extension 5 (restructured network-saturation): the saturation in
    # k(M_g) means the marginal contribution dk/dM_g collapses at large
    # M_g, which makes lambda_X negligible at equilibrium. The xi_X
    # parameter adds a non-marginal "network-density value" term so that
    # lambda_X retains a non-trivial component proportional to the
    # equilibrium survival benefit S(k_eq, sigma). Default xi_X = 0.0
    # preserves backward compatibility with the original §4.3 ablation
    # results; setting xi_X > 0 enables the restructured formulation.
    xi_X: float = 0.0
    # Quality-mediated cooperation reward: a band's monument display
    # increases the value of each partnership it forms (Bliege Bird and
    # Smith 2005). Setting this > 0 adds a saturating M_g multiplier
    # to lambda_X so that signal quality, not just network degree,
    # contributes to the cooperation reward at equilibrium.
    M_quality_scale: float = 50.0  # half-saturation of the quality multiplier


@dataclass(frozen=True)
class ConflictParams:
    """Parameters for intergroup assessment (Layer 2).

    Lower baseline conflict than sedentary populations because mobile
    hunter-gatherers have less territorial fixity.
    """
    sigma_0: float = 1.0        # Baseline assessment noise
    kappa: float = 0.08         # Information gain rate from monuments
    beta_conflict: float = 0.08 # Absolute deterrence coefficient
    P_base: float = 0.008       # Baseline annual conflict probability
    conflict_mortality: float = 0.08  # Mortality cost per conflict event
    V: float = 1.0              # Contested resource value
    D: float = 2.0              # Resource divisibility
    T_0: float = 0.5            # Escalation threshold scaling


@dataclass(frozen=True)
class AggregationParams:
    """Parameters for Layer 0: aggregation decision.

    Unique to the Poverty Point model. Captures the costs and benefits
    of seasonal aggregation for otherwise mobile bands.

    C_signal is the macroscopic cost of supporting the signaling norm:
    the fraction of group productive effort diverted to monument
    construction and exotic procurement. This is distinct from B(lambda),
    which is the microscopic individual reward from participating in
    the signaling game. C_signal reduces group output; B(lambda) is
    the individual incentive to participate.
    """
    C_travel_per_km: float = 0.0004   # Travel cost per km
    C_opportunity: float = 0.12        # Opportunity cost of aggregation
    C_signal: float = 0.18            # Macroscopic signaling cost (labor diversion)
    f_agg: float = 0.25               # Fraction of year in aggregation
    delta_net: float = 0.40           # Network decay during dispersal


# ═══════════════════════════════════════════════════════════════════════
# Layer 1: Individual/Band Signaling Equilibrium
# ═══════════════════════════════════════════════════════════════════════

def equilibrium_investment(
    q: float | NDArray, q_min: float, lam: float
) -> float | NDArray:
    """Optimal investment at signaling equilibrium.

    x*(q) = sqrt(lam * (q^2 - q_min^2))

    Derived from the first-order condition of the signaling game
    with quadratic cost c(x,q) = x^2/(2q) and linear benefit b = lam*q_hat.

    Parameters
    ----------
    q : float or array
        Band quality (productive capacity).
    q_min : float
        Minimum quality in the population.
    lam : float
        Total lambda (sum of audience-specific components).

    Returns
    -------
    float or array
        Equilibrium investment level.
    """
    q = np.asarray(q, dtype=float)
    arg = lam * (q**2 - q_min**2)
    return np.sqrt(np.maximum(arg, 0.0))


def equilibrium_fitness(
    q: float | NDArray, q_min: float, lam: float
) -> float | NDArray:
    """Fitness at signaling equilibrium.

    w*(q) = q * (1 + lam/2) + lam * q_min^2 / (2*q)
    """
    q = np.asarray(q, dtype=float)
    return q * (1.0 + lam / 2.0) + lam * q_min**2 / (2.0 * q)


def fitness_gain(
    q: float | NDArray, q_min: float, lam: float
) -> float | NDArray:
    """Fitness gain from signaling relative to no-signal baseline.

    Delta_w(q) = lam*q/2 + lam*q_min^2/(2*q)

    Always positive for q >= q_min when lam > 0: within-group
    selection favors signaling because benefits exceed costs.
    """
    q = np.asarray(q, dtype=float)
    return lam * q / 2.0 + lam * q_min**2 / (2.0 * q)


def signaling_cost(
    q: float | NDArray, q_min: float, lam: float
) -> float | NDArray:
    """Cost of signaling at equilibrium.

    c(x*(q), q) = lam * (q^2 - q_min^2) / (2*q)

    This is the fraction of productive capacity diverted to signaling.
    """
    q = np.asarray(q, dtype=float)
    return lam * (q**2 - q_min**2) / (2.0 * q)


def receiver_inference(
    x: float | NDArray, q_min: float, lam: float
) -> float | NDArray:
    """Receiver's inference of quality from observed investment.

    q_hat(x) = sqrt(x^2/lam + q_min^2)

    Inverts equilibrium_investment.
    """
    x = np.asarray(x, dtype=float)
    if lam <= 0:
        return np.full_like(x, q_min)
    return np.sqrt(x**2 / lam + q_min**2)


def expected_signaling_benefit(
    lam: float, q_min: float = 0.2, q_max: float = 2.0
) -> float:
    """Expected within-group signaling benefit B(lambda).

    B(lam) = E[Delta_w(q)] over uniform(q_min, q_max)
           = lam/2 * (q_min + q_max)/2
             + lam*q_min^2 / (2*(q_max - q_min)) * ln(q_max/q_min)

    This is the key quantity that makes within-group selection
    favor monument investment: B(lam) > 0 reduces the effective
    cost of signaling in the Price equation.
    """
    if lam <= 0 or q_max <= q_min:
        return 0.0

    term1 = (lam / 2.0) * (q_min + q_max) / 2.0
    term2 = (lam * q_min**2) / (2.0 * (q_max - q_min)) * np.log(q_max / q_min)
    return float(term1 + term2)


def expected_signaling_benefit_numerical(
    lam: float, q_min: float = 0.2, q_max: float = 2.0
) -> float:
    """Numerical verification of B(lambda) via quadrature."""
    if lam <= 0 or q_max <= q_min:
        return 0.0

    def integrand(q):
        return fitness_gain(q, q_min, lam)

    result, _ = quad(integrand, q_min, q_max, limit=100)
    return float(result / (q_max - q_min))


def expected_monument_stock(
    n: int, q_min: float, q_max: float, lam: float
) -> float:
    """Expected total monument investment flow from n bands.

    E[M_g] = n * E[x*(q)] integrated over the quality distribution.
    """
    if lam <= 0 or n <= 0:
        return 0.0

    def integrand(q):
        return float(equilibrium_investment(q, q_min, lam))

    result_val, _ = quad(integrand, q_min, q_max, limit=100)
    mean_x = result_val / (q_max - q_min)
    return float(n * mean_x)


def effective_monument_stock(I_g: float, delta: float) -> float:
    """Steady-state monument stock under depreciation.

    M_g* = I_g / delta

    For earthen mounds with delta=0.08, annual flow of 10 units
    gives steady-state stock of 125.
    """
    if delta <= 0:
        return I_g
    return I_g / delta


def monument_stock_step(
    M_g: float, I_g: float, delta: float
) -> float:
    """One-step monument stock update with depreciation.

    M_g(t+1) = (1 - delta) * M_g(t) + I_g(t)
    """
    return (1.0 - delta) * M_g + I_g


# ═══════════════════════════════════════════════════════════════════════
# Layer 2: Intergroup Assessment and Conflict
# ═══════════════════════════════════════════════════════════════════════

def effective_noise(
    M_g: float, M_h: float,
    sigma_0: float = 1.0, kappa: float = 0.08
) -> float:
    """Assessment noise reduced by monument investment.

    sigma_eff = sigma_0 / sqrt(1 + kappa*(M_g + M_h))

    Higher monument stocks improve information quality,
    reducing assessment error and hence conflict probability.
    """
    return sigma_0 / np.sqrt(1.0 + kappa * (M_g + M_h))


def conflict_probability(
    M_g: float, M_h: float,
    params: ConflictParams = ConflictParams()
) -> float:
    """Mutual assessment conflict probability (Enquist-Leimar 1983).

    P = P_raw * normalization / (1 + beta*(M_g + M_h))

    where P_raw is the probability that both groups misestimate
    the asymmetry to be within the escalation threshold T.

    Normalized so P(0, 0) = P_base.
    """
    sigma_eff = effective_noise(M_g, M_h, params.sigma_0, params.kappa)
    T = params.T_0 * params.V / params.D
    delta_M = abs(M_g - M_h)
    scale = np.sqrt(2.0) * sigma_eff

    if scale < 1e-12:
        P_raw = 0.0
    else:
        P_raw = float(
            norm.cdf((T - delta_M) / scale)
            - norm.cdf((-T - delta_M) / scale)
        )

    # Deterrence from absolute investment
    deterrence = 1.0 / (1.0 + params.beta_conflict * (M_g + M_h))

    # Normalize so P(0, 0) = P_base
    sigma_eff_0 = effective_noise(0, 0, params.sigma_0, params.kappa)
    scale_0 = np.sqrt(2.0) * sigma_eff_0
    if scale_0 < 1e-12:
        P_raw_0 = 1.0
    else:
        P_raw_0 = float(norm.cdf(T / scale_0) - norm.cdf(-T / scale_0))

    if P_raw_0 < 1e-12:
        return 0.0

    P = params.P_base * (P_raw * deterrence) / P_raw_0
    return float(np.clip(P, 0.0, params.P_base))


def conflict_reduction(
    M_g: float, M_h: float,
    params: ConflictParams = ConflictParams()
) -> float:
    """Conflict reduction factor r from monument investment.

    r = 1 - P_conflict / P_base

    Replaces the assumed r=0.75 in the initial model with a
    value derived from the mutual assessment framework.
    """
    P = conflict_probability(M_g, M_h, params)
    if params.P_base <= 0:
        return 0.0
    return float(1.0 - P / params.P_base)


def compute_lambda_C(
    M_g: float,
    params: ConflictParams = ConflictParams(),
    n_neighbors: int = 3,
    dispute_freq: float = 0.03,
    dx: float = 0.01,
) -> float:
    """Marginal conflict deterrence value per unit monument investment.

    lambda_C = -d(expected_loss)/dM_g

    Computed via central finite differences.
    """
    M_h_mean = M_g  # Symmetric case: neighbors have similar M

    def expected_loss(M):
        P = conflict_probability(M, M_h_mean, params)
        return n_neighbors * dispute_freq * P * params.conflict_mortality

    loss_plus = expected_loss(M_g + dx)
    loss_minus = expected_loss(max(0, M_g - dx))
    lam_C = -(loss_plus - loss_minus) / (2.0 * dx)
    return float(max(lam_C, 0.0))


# ═══════════════════════════════════════════════════════════════════════
# Layer 3: Cooperation Networks and Crisis Buffering
# ═══════════════════════════════════════════════════════════════════════

def network_degree(
    M_g: float,
    k_0: float = 0.3, k_max: float = 6.0, M_half: float = 2.5
) -> float:
    """Network degree as saturating function of monument stock.

    k(M_g) = k_0 + k_max * M_g / (M_half + M_g)

    Michaelis-Menten form: k(0) = k_0, k(inf) -> k_0 + k_max.
    """
    M_g = max(M_g, 0.0)
    return k_0 + k_max * M_g / (M_half + M_g)


def network_degree_derivative(
    M_g: float,
    k_max: float = 6.0, M_half: float = 2.5
) -> float:
    """Derivative of network degree with respect to monument stock.

    dk/dM_g = k_max * M_half / (M_half + M_g)^2
    """
    M_g = max(M_g, 0.0)
    return k_max * M_half / (M_half + M_g) ** 2


def seasonal_effective_degree(
    k_agg: float, k_0: float, delta_net: float, f_agg: float
) -> float:
    """Effective annual network degree with seasonal dynamics.

    During aggregation (f_agg of year): full network at k_agg.
    During dispersal (1-f_agg): ties decay, k_disp = k_0 + (k_agg - k_0)*(1 - delta_net).
    Effective annual: k_eff = f_agg*k_agg + (1-f_agg)*k_disp.

    This captures the transience of hunter-gatherer social networks:
    ties formed during aggregation weaken during dispersal without
    reinforcement.
    """
    k_disp = k_0 + (k_agg - k_0) * (1.0 - delta_net)
    k_eff = f_agg * k_agg + (1.0 - f_agg) * k_disp
    return max(k_eff, k_0)


def survival_probability(
    sigma: float, k: float, gamma: float = 0.05
) -> float:
    """Crisis survival probability.

    S(sigma, k) = 1 - sigma / (1 + gamma*k)

    Each exchange partner provides gamma units of buffering.
    """
    S = 1.0 - sigma / (1.0 + gamma * k)
    return float(np.clip(S, 0.0, 1.0))


def vulnerability_coefficient(
    k: float, gamma: float = 0.05
) -> float:
    """Vulnerability to environmental uncertainty.

    alpha(k) = 1 / (1 + gamma*k)

    Replaces assumed alpha_agg and beta_ind with values
    derived from network degree. Signalers (high k) have
    lower vulnerability than non-signalers (low k).
    """
    return 1.0 / (1.0 + gamma * k)


def compute_lambda_X(
    M_g: float, sigma: float,
    params: NetworkParams = NetworkParams(),
) -> float:
    """Cooperative between-group lambda.

    Original (saturating) form (xi_X = 0.0, default):
        lambda_X = (dk/dM_g) * (dS/dk)
        where dS/dk = sigma * gamma / (1 + gamma*k)^2.
        At equilibrium with M_g >> M_half, dk/dM_g -> 0 and lambda_X
        collapses to ~0. This is the §4.3 'ablation reduces to one
        constant' problem.

    Extension 5 (restructured, xi_X > 0): adds a non-marginal
    network-density value term proportional to the equilibrium
    survival benefit S(k, sigma) = sigma * (1 - 1/(1 + gamma*k)),
    weighted by xi_X and a saturating monument-quality multiplier
    M_g / (M_g + M_quality_scale). This captures the Bliege Bird and
    Smith (2005) intuition that signal quality enhances per-partnership
    value independent of the marginal partner-formation rate.

        lambda_X = (dk/dM_g) * (dS/dk)                          # original marginal term
                 + xi_X * S(k, sigma) * Q(M_g)                   # restructured non-marginal term

        where Q(M_g) = M_g / (M_g + M_quality_scale).

    At equilibrium (large M_g), the first term -> 0 and lambda_X is
    dominated by xi_X * S(k_eq, sigma) * Q(M_g_eq). For PP-scale
    M_g_eq = 130 and M_quality_scale = 50, Q(130) = 130/180 = 0.72
    and S(k_eq, sigma) ~ 0.6 * 0.20 = 0.12, so lambda_X(xi_X = 0.5) ~
    0.5 * 0.12 * 0.72 = 0.043, comparable to lambda_W = 0.15.
    """
    k = network_degree(M_g, params.k_0, params.k_max, params.M_half)
    dk_dM = network_degree_derivative(M_g, params.k_max, params.M_half)
    dS_dk = sigma * params.gamma / (1.0 + params.gamma * k) ** 2
    marginal = max(dk_dM * dS_dk, 0.0)

    if params.xi_X <= 0.0:
        return float(marginal)

    # Extension 5: non-marginal network-density value
    S = sigma * (1.0 - 1.0 / (1.0 + params.gamma * k))
    Q = M_g / (M_g + params.M_quality_scale) if (M_g + params.M_quality_scale) > 0 else 0.0
    non_marginal = params.xi_X * S * Q
    return float(marginal + non_marginal)


# ═══════════════════════════════════════════════════════════════════════
# Lambda-Sigma Feedback Loop
# ═══════════════════════════════════════════════════════════════════════

def lambda_total_at_sigma(
    sigma: float,
    sig_params: SignalingParams = SignalingParams(),
    net_params: NetworkParams = NetworkParams(),
    conf_params: ConflictParams = ConflictParams(),
    agg_params: AggregationParams = AggregationParams(),
    n_bands: int = 25,
    tol: float = 1e-6,
    max_iter: int = 100,
    damping: float = 0.5,
) -> Dict[str, float]:
    """Fixed-point iteration for equilibrium lambda at given sigma.

    Loop: lam -> I_g -> M_g -> lambda_C, lambda_X -> lam_new
    until convergence.

    Returns dict with lambda_total, lambda_W, lambda_C, lambda_X,
    M_g, I_g, k_agg, k_eff, alpha_eff, beta_eff, converged, iterations.
    """
    lam = sig_params.lambda_W + sig_params.lambda_C + sig_params.lambda_X
    converged = False
    iterations = 0

    for i in range(max_iter):
        # Monument stock from current lambda
        I_g = expected_monument_stock(
            n_bands, sig_params.q_min, sig_params.q_max, lam
        )
        if sig_params.delta > 0:
            M_g = effective_monument_stock(I_g, sig_params.delta)
        else:
            M_g = I_g

        # Layer 2: conflict deterrence value
        lam_C = compute_lambda_C(M_g, conf_params)

        # Layer 3: cooperation network value
        lam_X = compute_lambda_X(M_g, sigma, net_params)

        # New total lambda
        lam_new = sig_params.lambda_W + lam_C + lam_X

        # Damped update
        lam_updated = damping * lam + (1.0 - damping) * lam_new
        iterations = i + 1

        if abs(lam_updated - lam) < tol:
            converged = True
            lam = lam_updated
            break

        lam = lam_updated

    # Final quantities
    I_g = expected_monument_stock(
        n_bands, sig_params.q_min, sig_params.q_max, lam
    )
    if sig_params.delta > 0:
        M_g = effective_monument_stock(I_g, sig_params.delta)
    else:
        M_g = I_g

    k_agg = network_degree(M_g, net_params.k_0, net_params.k_max, net_params.M_half)
    k_eff = seasonal_effective_degree(
        k_agg, net_params.k_0, agg_params.delta_net, agg_params.f_agg
    )
    alpha_eff = vulnerability_coefficient(k_eff, net_params.gamma)
    beta_eff = vulnerability_coefficient(net_params.k_0, net_params.gamma)

    return {
        'lambda_total': lam,
        'lambda_W': sig_params.lambda_W,
        'lambda_C': compute_lambda_C(M_g, conf_params),
        'lambda_X': compute_lambda_X(M_g, sigma, net_params),
        'M_g': M_g,
        'I_g': I_g,
        'k_agg': k_agg,
        'k_eff': k_eff,
        'alpha_eff': alpha_eff,
        'beta_eff': beta_eff,
        'converged': converged,
        'iterations': iterations,
    }


# ═══════════════════════════════════════════════════════════════════════
# Layer 0: Aggregation Decision (Assembled Fitness)
# ═══════════════════════════════════════════════════════════════════════

def aggregation_expected_fitness(
    sigma: float,
    epsilon: float,
    n_agg: int,
    band_quality: float,
    travel_distance: float,
    M_g: float,
    lam: float,
    sig_params: SignalingParams = SignalingParams(),
    net_params: NetworkParams = NetworkParams(),
    conf_params: ConflictParams = ConflictParams(),
    agg_params: AggregationParams = AggregationParams(),
) -> float:
    """Expected fitness of a band choosing to aggregate.

    W_agg = (1 - C_total) * (1 - alpha_eff * sigma_eff)
            * (1 - m*(1-r)*P_base) + B(lambda)

    where:
        C_total = C_travel(d) + C_opportunity + C_signal
        sigma_eff = sigma * (1 - epsilon)
        alpha_eff = 1/(1 + gamma*k_eff) derived from network
        r = conflict_reduction(M_g, M_g) from Layer 2
        B(lambda) = expected signaling benefit from Layer 1

    C_total is the macroscopic group-level cost of aggregation.
    B(lambda) is the microscopic individual-level signaling reward.
    These operate at different levels of the Price equation.
    """
    # Costs: travel + opportunity + signaling labor diversion
    C_travel = agg_params.C_travel_per_km * travel_distance
    C_total = C_travel + agg_params.C_opportunity + agg_params.C_signal

    # Effective uncertainty (ecotone buffering)
    sigma_eff = sigma * (1.0 - epsilon)

    # Network degree and vulnerability
    k_agg = network_degree(
        M_g, net_params.k_0, net_params.k_max, net_params.M_half
    )
    k_eff = seasonal_effective_degree(
        k_agg, net_params.k_0, agg_params.delta_net, agg_params.f_agg
    )
    alpha_eff = vulnerability_coefficient(k_eff, net_params.gamma)

    # Conflict reduction
    r = conflict_reduction(M_g, M_g, conf_params)

    # Signaling benefit (individual-level reward within group)
    B_lam = expected_signaling_benefit(lam, sig_params.q_min, sig_params.q_max)

    # Assembled fitness (mixed mode: multiplicative survival, additive reward)
    reproduction = 1.0 - C_total
    survival = 1.0 - alpha_eff * sigma_eff
    conflict_effect = 1.0 - conf_params.conflict_mortality * (1.0 - r) * conf_params.P_base

    W = reproduction * survival * conflict_effect + B_lam
    return float(max(W, 0.0))


def independent_expected_fitness(
    sigma: float,
    net_params: NetworkParams = NetworkParams(),
    conf_params: ConflictParams = ConflictParams(),
) -> float:
    """Expected fitness of a band choosing not to aggregate.

    W_ind = (1 - beta_eff * sigma) * (1 - m * P_base)

    No signaling benefit, no ecotone buffering, baseline network only.
    """
    beta_eff = vulnerability_coefficient(net_params.k_0, net_params.gamma)
    survival = 1.0 - beta_eff * sigma
    conflict_effect = 1.0 - conf_params.conflict_mortality * conf_params.P_base

    W = survival * conflict_effect
    return float(max(W, 0.0))


def fitness_advantage(
    sigma: float,
    epsilon: float,
    n_agg: int,
    travel_distance: float,
    sig_params: SignalingParams = SignalingParams(),
    net_params: NetworkParams = NetworkParams(),
    conf_params: ConflictParams = ConflictParams(),
    agg_params: AggregationParams = AggregationParams(),
) -> float:
    """Fitness difference: W_agg - W_ind.

    Positive when aggregation is adaptive.
    Computes equilibrium lambda via feedback loop.
    """
    eq = lambda_total_at_sigma(
        sigma, sig_params, net_params, conf_params, agg_params, n_agg
    )
    lam = eq['lambda_total']
    M_g = eq['M_g']

    W_agg = aggregation_expected_fitness(
        sigma, epsilon, n_agg, 1.0, travel_distance, M_g, lam,
        sig_params, net_params, conf_params, agg_params
    )
    W_ind = independent_expected_fitness(sigma, net_params, conf_params)
    return W_agg - W_ind


def critical_threshold(
    epsilon: float = 0.35,
    n_agg: int = 25,
    travel_distance: float = 100.0,
    sig_params: SignalingParams = SignalingParams(),
    net_params: NetworkParams = NetworkParams(),
    conf_params: ConflictParams = ConflictParams(),
    agg_params: AggregationParams = AggregationParams(),
    sigma_bounds: Tuple[float, float] = (0.01, 0.99),
) -> Dict[str, float]:
    """Solve for sigma* where aggregation becomes adaptive.

    Uses Brent's method with the lambda-sigma feedback loop.

    Returns dict with sigma_star, lambda_total, B_lambda,
    alpha_eff, beta_eff, k_eff, converged.
    """
    def objective(sigma):
        return fitness_advantage(
            sigma, epsilon, n_agg, travel_distance,
            sig_params, net_params, conf_params, agg_params
        )

    # Check boundary conditions
    diff_low = objective(sigma_bounds[0])
    diff_high = objective(sigma_bounds[1])

    if diff_low >= 0:
        sigma_star = 0.0
    elif diff_high <= 0:
        sigma_star = 1.0
    else:
        sigma_star = float(brentq(
            objective, sigma_bounds[0], sigma_bounds[1], xtol=1e-6
        ))

    # Compute associated quantities at sigma*
    eq = lambda_total_at_sigma(
        sigma_star, sig_params, net_params, conf_params, agg_params, n_agg
    )
    B_lam = expected_signaling_benefit(
        eq['lambda_total'], sig_params.q_min, sig_params.q_max
    )

    return {
        'sigma_star': sigma_star,
        'lambda_total': eq['lambda_total'],
        'B_lambda': B_lam,
        'alpha_eff': eq['alpha_eff'],
        'beta_eff': eq['beta_eff'],
        'k_eff': eq['k_eff'],
        'M_g': eq['M_g'],
        'converged': eq['converged'],
    }


def initial_model_sigma_star(
    C: float = 0.42, alpha: float = 0.40, beta: float = 0.90
) -> float:
    """Sigma* from the initial (non-MLS) model for comparison.

    sigma* = C / (beta - (1-C)*alpha)
    """
    denom = beta - (1.0 - C) * alpha
    if denom <= 0:
        return 1.0
    return C / denom


# ═══════════════════════════════════════════════════════════════════════
# Exotic Signal Functions
# ═══════════════════════════════════════════════════════════════════════

def exotic_signaling_cost(
    distance_km: float, base_cost: float = 0.05
) -> float:
    """Cost of acquiring an exotic good as a signal.

    c_exotic = base_cost * sqrt(distance_km / 250)

    Sublinear in distance because exchange networks reduce
    marginal procurement cost for more distant materials.
    """
    return base_cost * np.sqrt(max(distance_km, 0.0) / 250.0)


def exotic_signal_value(
    distance_km: float, rho_exotic: float = 0.70
) -> float:
    """Signal value of an exotic good.

    v_exotic = rho_exotic * ln(1 + distance_km / 100)

    More distant exotics carry higher signal value because they
    are harder to obtain (and hence harder to fake).
    """
    return rho_exotic * np.log(1.0 + max(distance_km, 0.0) / 100.0)


# ═══════════════════════════════════════════════════════════════════════
# Phase Space Analysis
# ═══════════════════════════════════════════════════════════════════════

def phase_space(
    sigma_range: NDArray,
    C_opportunity_range: NDArray,
    epsilon: float = 0.35,
    n_agg: int = 25,
    travel_distance: float = 100.0,
    sig_params: SignalingParams = SignalingParams(),
    net_params: NetworkParams = NetworkParams(),
    conf_params: ConflictParams = ConflictParams(),
) -> Dict[str, NDArray]:
    """Evaluate fitness advantage over (sigma, C) grid.

    Returns dict with sigma_grid, C_grid, fitness_advantage, lambda_total.
    """
    n_sigma = len(sigma_range)
    n_C = len(C_opportunity_range)
    advantage = np.zeros((n_sigma, n_C))
    lam_total = np.zeros((n_sigma, n_C))

    for i, sigma in enumerate(sigma_range):
        for j, C_opp in enumerate(C_opportunity_range):
            agg_p = AggregationParams(C_opportunity=C_opp)
            eq = lambda_total_at_sigma(
                sigma, sig_params, net_params, conf_params, agg_p, n_agg
            )
            W_agg = aggregation_expected_fitness(
                sigma, epsilon, n_agg, 1.0, travel_distance,
                eq['M_g'], eq['lambda_total'],
                sig_params, net_params, conf_params, agg_p
            )
            W_ind = independent_expected_fitness(sigma, net_params, conf_params)
            advantage[i, j] = W_agg - W_ind
            lam_total[i, j] = eq['lambda_total']

    S, C = np.meshgrid(sigma_range, C_opportunity_range, indexing='ij')
    return {
        'sigma_grid': S,
        'C_grid': C,
        'fitness_advantage': advantage,
        'lambda_total': lam_total,
    }
