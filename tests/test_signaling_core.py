"""Tests for the multilevel signaling framework (signaling_core.py)."""

import numpy as np
import pytest

from src.poverty_point.signaling_core import (
    AggregationParams,
    ConflictParams,
    NetworkParams,
    SignalingParams,
    aggregation_expected_fitness,
    compute_lambda_C,
    compute_lambda_X,
    conflict_probability,
    conflict_reduction,
    critical_threshold,
    effective_monument_stock,
    effective_noise,
    equilibrium_fitness,
    equilibrium_investment,
    exotic_signal_value,
    exotic_signaling_cost,
    expected_monument_stock,
    expected_signaling_benefit,
    expected_signaling_benefit_numerical,
    fitness_advantage,
    fitness_gain,
    independent_expected_fitness,
    initial_model_sigma_star,
    lambda_total_at_sigma,
    monument_stock_step,
    network_degree,
    network_degree_derivative,
    phase_space,
    receiver_inference,
    seasonal_effective_degree,
    signaling_cost,
    survival_probability,
    vulnerability_coefficient,
)


# ── Layer 1: Signaling Equilibrium ─────────────────────────────────────


class TestEquilibriumInvestment:
    def test_zero_at_q_min(self):
        assert equilibrium_investment(0.2, 0.2, 0.5) == pytest.approx(0.0)

    def test_positive_above_q_min(self):
        assert equilibrium_investment(1.0, 0.2, 0.5) > 0

    def test_increases_with_q(self):
        x_low = equilibrium_investment(0.5, 0.2, 0.5)
        x_high = equilibrium_investment(1.5, 0.2, 0.5)
        assert x_high > x_low

    def test_increases_with_lambda(self):
        x_low = equilibrium_investment(1.0, 0.2, 0.3)
        x_high = equilibrium_investment(1.0, 0.2, 0.8)
        assert x_high > x_low

    def test_vectorized(self):
        q = np.array([0.2, 0.5, 1.0, 1.5, 2.0])
        result = equilibrium_investment(q, 0.2, 0.5)
        assert result.shape == (5,)
        assert result[0] == pytest.approx(0.0, abs=1e-10)
        assert np.all(np.diff(result) >= 0)

    def test_formula(self):
        q, q_min, lam = 1.0, 0.2, 0.5
        expected = np.sqrt(lam * (q**2 - q_min**2))
        assert equilibrium_investment(q, q_min, lam) == pytest.approx(expected)


class TestFitnessGain:
    def test_always_positive(self):
        for q in [0.2, 0.5, 1.0, 1.5, 2.0]:
            assert fitness_gain(q, 0.2, 0.5) > 0

    def test_zero_lambda_gives_zero(self):
        assert fitness_gain(1.0, 0.2, 0.0) == pytest.approx(0.0)

    def test_equals_w_star_minus_q(self):
        q, q_min, lam = 1.0, 0.2, 0.5
        w_star = equilibrium_fitness(q, q_min, lam)
        dw = fitness_gain(q, q_min, lam)
        assert dw == pytest.approx(w_star - q)


class TestSignalingCost:
    def test_zero_at_q_min(self):
        assert signaling_cost(0.2, 0.2, 0.5) == pytest.approx(0.0)

    def test_positive_above_q_min(self):
        assert signaling_cost(1.0, 0.2, 0.5) > 0

    def test_less_than_fitness_gain(self):
        """Cost is less than benefit at equilibrium (B(lambda) > 0)."""
        q, q_min, lam = 1.0, 0.2, 0.5
        c = signaling_cost(q, q_min, lam)
        dw = fitness_gain(q, q_min, lam)
        assert dw > c


class TestReceiverInference:
    def test_inverts_investment(self):
        q, q_min, lam = 1.0, 0.2, 0.5
        x = equilibrium_investment(q, q_min, lam)
        q_hat = receiver_inference(x, q_min, lam)
        assert q_hat == pytest.approx(q, abs=1e-8)

    def test_zero_investment_gives_q_min(self):
        assert receiver_inference(0.0, 0.2, 0.5) == pytest.approx(0.2)


class TestExpectedSignalingBenefit:
    def test_positive(self):
        B = expected_signaling_benefit(0.5, 0.2, 2.0)
        assert B > 0

    def test_zero_for_zero_lambda(self):
        assert expected_signaling_benefit(0.0, 0.2, 2.0) == 0.0

    def test_increases_with_lambda(self):
        B_low = expected_signaling_benefit(0.3, 0.2, 2.0)
        B_high = expected_signaling_benefit(0.8, 0.2, 2.0)
        assert B_high > B_low

    def test_analytical_matches_numerical(self):
        lam = 0.5
        B_analytical = expected_signaling_benefit(lam, 0.2, 2.0)
        B_numerical = expected_signaling_benefit_numerical(lam, 0.2, 2.0)
        assert B_analytical == pytest.approx(B_numerical, rel=1e-6)


class TestMonumentStock:
    def test_expected_stock_positive(self):
        M = expected_monument_stock(25, 0.2, 2.0, 0.5)
        assert M > 0

    def test_effective_stock_scales_with_delta(self):
        M_slow = effective_monument_stock(10.0, 0.05)
        M_fast = effective_monument_stock(10.0, 0.20)
        assert M_slow > M_fast

    def test_step_converges_to_steady_state(self):
        delta = 0.08
        I_g = 10.0
        M = 0.0
        for _ in range(500):
            M = monument_stock_step(M, I_g, delta)
        expected = effective_monument_stock(I_g, delta)
        assert M == pytest.approx(expected, rel=0.01)


# ── Layer 2: Intergroup Assessment ─────────────────────────────────────


class TestEffectiveNoise:
    def test_decreases_with_M(self):
        n_low = effective_noise(0.0, 0.0)
        n_high = effective_noise(10.0, 10.0)
        assert n_high < n_low

    def test_baseline_equals_sigma_0(self):
        assert effective_noise(0.0, 0.0, sigma_0=1.0) == pytest.approx(1.0)


class TestConflictProbability:
    def test_baseline_equals_P_base(self):
        params = ConflictParams()
        P = conflict_probability(0.0, 0.0, params)
        assert P == pytest.approx(params.P_base, rel=0.01)

    def test_decreases_with_investment(self):
        params = ConflictParams()
        P_zero = conflict_probability(0.0, 0.0, params)
        P_high = conflict_probability(10.0, 10.0, params)
        assert P_high < P_zero

    def test_bounded_by_P_base(self):
        params = ConflictParams()
        for M in [0, 1, 5, 10, 50]:
            P = conflict_probability(float(M), float(M), params)
            assert 0 <= P <= params.P_base

    def test_asymmetry_reduces_conflict(self):
        params = ConflictParams()
        P_sym = conflict_probability(5.0, 5.0, params)
        P_asym = conflict_probability(10.0, 1.0, params)
        assert P_asym < P_sym


class TestConflictReduction:
    def test_zero_at_no_investment(self):
        r = conflict_reduction(0.0, 0.0)
        assert r == pytest.approx(0.0, abs=0.05)

    def test_positive_at_high_investment(self):
        r = conflict_reduction(10.0, 10.0)
        assert r > 0

    def test_in_unit_interval(self):
        for M in [0, 1, 5, 10, 50]:
            r = conflict_reduction(float(M), float(M))
            assert 0 <= r <= 1


class TestLambdaC:
    def test_nonnegative(self):
        lam_C = compute_lambda_C(5.0)
        assert lam_C >= 0

    def test_zero_at_very_high_M(self):
        """At very high M, conflict is already near zero; marginal value is small."""
        lam_C = compute_lambda_C(1000.0)
        assert lam_C < 0.01


# ── Layer 3: Cooperation Networks ──────────────────────────────────────


class TestNetworkDegree:
    def test_baseline_at_zero(self):
        assert network_degree(0.0) == pytest.approx(0.3)

    def test_half_saturation(self):
        k = network_degree(2.5, k_0=0.3, k_max=6.0, M_half=2.5)
        assert k == pytest.approx(0.3 + 6.0 / 2.0)

    def test_saturates(self):
        k = network_degree(1000.0)
        assert k == pytest.approx(0.3 + 6.0, rel=0.01)

    def test_monotonically_increasing(self):
        M_values = np.linspace(0, 50, 100)
        k_values = [network_degree(M) for M in M_values]
        assert all(k_values[i + 1] >= k_values[i] for i in range(len(k_values) - 1))


class TestNetworkDegreeDerivative:
    def test_positive(self):
        assert network_degree_derivative(5.0) > 0

    def test_decreasing(self):
        dk_low = network_degree_derivative(1.0)
        dk_high = network_degree_derivative(10.0)
        assert dk_high < dk_low

    def test_consistency_with_finite_difference(self):
        M = 3.0
        dx = 1e-5
        numerical = (network_degree(M + dx) - network_degree(M - dx)) / (2 * dx)
        analytical = network_degree_derivative(M)
        assert analytical == pytest.approx(numerical, rel=1e-4)


class TestSeasonalNetwork:
    def test_between_k0_and_k_agg(self):
        k_eff = seasonal_effective_degree(5.0, 0.3, 0.4, 0.25)
        assert 0.3 <= k_eff <= 5.0

    def test_full_decay_approaches_k0(self):
        k_eff = seasonal_effective_degree(5.0, 0.3, 1.0, 0.25)
        # With full decay: k_disp = k_0, k_eff = f_agg*k_agg + (1-f_agg)*k_0
        expected = 0.25 * 5.0 + 0.75 * 0.3
        assert k_eff == pytest.approx(expected)

    def test_zero_decay_gives_k_agg(self):
        k_eff = seasonal_effective_degree(5.0, 0.3, 0.0, 0.25)
        # No decay: k_disp = k_agg, k_eff = k_agg
        assert k_eff == pytest.approx(5.0)

    def test_full_aggregation_gives_k_agg(self):
        k_eff = seasonal_effective_degree(5.0, 0.3, 0.4, 1.0)
        assert k_eff == pytest.approx(5.0)

    def test_lower_than_permanent_network(self):
        """Seasonal networks are weaker than permanent ones."""
        k_agg = 5.0
        k_eff = seasonal_effective_degree(k_agg, 0.3, 0.4, 0.25)
        assert k_eff < k_agg


class TestSurvivalProbability:
    def test_certain_at_zero_sigma(self):
        assert survival_probability(0.0, 3.0) == pytest.approx(1.0)

    def test_max_vulnerability_at_zero_k(self):
        S = survival_probability(0.5, 0.0)
        assert S == pytest.approx(1.0 - 0.5)

    def test_in_unit_interval(self):
        for sigma in [0, 0.3, 0.5, 0.8]:
            for k in [0, 1, 5, 10]:
                S = survival_probability(sigma, float(k))
                assert 0 <= S <= 1

    def test_increases_with_k(self):
        S_low = survival_probability(0.5, 1.0)
        S_high = survival_probability(0.5, 5.0)
        assert S_high > S_low

    def test_decreases_with_sigma(self):
        S_low = survival_probability(0.3, 3.0)
        S_high = survival_probability(0.7, 3.0)
        assert S_low > S_high


class TestVulnerabilityCoefficient:
    def test_one_at_zero_k(self):
        assert vulnerability_coefficient(0.0) == pytest.approx(1.0)

    def test_decreases_with_k(self):
        a_low = vulnerability_coefficient(1.0)
        a_high = vulnerability_coefficient(5.0)
        assert a_high < a_low

    def test_consistency_with_survival(self):
        sigma, k, gamma = 0.5, 3.0, 0.25
        alpha = vulnerability_coefficient(k, gamma)
        S = survival_probability(sigma, k, gamma)
        assert S == pytest.approx(1.0 - alpha * sigma)

    def test_derived_values_produce_modest_vulnerability_ratio(self):
        """Verify framework produces a modest vulnerability ratio (1.1-1.5)."""
        net = NetworkParams()
        # Aggregator: k_eff from seasonal_effective_degree with M_g ~ 100
        k_agg = network_degree(100.0, net.k_0, net.k_max, net.M_half)
        k_eff = seasonal_effective_degree(k_agg, net.k_0, 0.4, 0.25)
        alpha = vulnerability_coefficient(k_eff, net.gamma)
        # Independent: k_0 only
        beta = vulnerability_coefficient(net.k_0, net.gamma)
        # With gamma=0.05, expect modest ratio ~1.2
        assert alpha < beta  # Aggregators less vulnerable
        ratio = beta / alpha
        assert 1.05 < ratio < 1.50  # Modest, ethnographically realistic ratio


class TestLambdaX:
    def test_positive(self):
        lam_X = compute_lambda_X(5.0, 0.5)
        assert lam_X > 0

    def test_zero_without_crisis(self):
        lam_X = compute_lambda_X(5.0, 0.0)
        assert lam_X == pytest.approx(0.0)

    def test_increases_with_sigma(self):
        lam_X_low = compute_lambda_X(5.0, 0.3)
        lam_X_high = compute_lambda_X(5.0, 0.7)
        assert lam_X_high > lam_X_low


# ── Lambda-Sigma Feedback ──────────────────────────────────────────────


class TestLambdaFeedback:
    def test_converges(self):
        result = lambda_total_at_sigma(0.5)
        assert result['converged']

    def test_lambda_ge_lambda_W(self):
        result = lambda_total_at_sigma(0.5)
        assert result['lambda_total'] >= SignalingParams().lambda_W

    def test_lambda_increases_with_sigma(self):
        r_low = lambda_total_at_sigma(0.2)
        r_high = lambda_total_at_sigma(0.7)
        assert r_high['lambda_total'] >= r_low['lambda_total']

    def test_lambda_X_positive(self):
        result = lambda_total_at_sigma(0.5)
        assert result['lambda_X'] >= 0

    def test_alpha_less_than_beta(self):
        result = lambda_total_at_sigma(0.5)
        assert result['alpha_eff'] < result['beta_eff']


# ── Layer 0: Aggregation Decision ──────────────────────────────────────


class TestAggregationFitness:
    def test_positive(self):
        W = aggregation_expected_fitness(
            sigma=0.5, epsilon=0.35, n_agg=25,
            band_quality=1.0, travel_distance=100.0,
            M_g=50.0, lam=0.5,
        )
        assert W > 0

    def test_independent_positive(self):
        W = independent_expected_fitness(0.5)
        assert W > 0

    def test_aggregation_wins_at_high_sigma(self):
        eq = lambda_total_at_sigma(0.8)
        W_agg = aggregation_expected_fitness(
            sigma=0.8, epsilon=0.35, n_agg=25,
            band_quality=1.0, travel_distance=100.0,
            M_g=eq['M_g'], lam=eq['lambda_total'],
        )
        W_ind = independent_expected_fitness(0.8)
        assert W_agg > W_ind

    def test_independent_wins_at_low_sigma(self):
        eq = lambda_total_at_sigma(0.1)
        W_agg = aggregation_expected_fitness(
            sigma=0.1, epsilon=0.35, n_agg=25,
            band_quality=1.0, travel_distance=100.0,
            M_g=eq['M_g'], lam=eq['lambda_total'],
        )
        W_ind = independent_expected_fitness(0.1)
        assert W_ind > W_agg

    def test_ecotone_helps_aggregators(self):
        eq = lambda_total_at_sigma(0.5)
        W_no_eco = aggregation_expected_fitness(
            sigma=0.5, epsilon=0.0, n_agg=25,
            band_quality=1.0, travel_distance=100.0,
            M_g=eq['M_g'], lam=eq['lambda_total'],
        )
        W_with_eco = aggregation_expected_fitness(
            sigma=0.5, epsilon=0.35, n_agg=25,
            band_quality=1.0, travel_distance=100.0,
            M_g=eq['M_g'], lam=eq['lambda_total'],
        )
        assert W_with_eco > W_no_eco


class TestCriticalThreshold:
    def test_exists(self):
        result = critical_threshold()
        assert 0 < result['sigma_star'] < 1

    def test_converged(self):
        result = critical_threshold()
        assert result['converged']

    def test_ecotone_lowers_threshold(self):
        r_no_eco = critical_threshold(epsilon=0.0)
        r_with_eco = critical_threshold(epsilon=0.35)
        assert r_with_eco['sigma_star'] < r_no_eco['sigma_star']

    def test_lower_than_initial_model(self):
        """MLS framework produces lower threshold due to B(lambda) > 0."""
        result = critical_threshold(epsilon=0.0)
        sigma_initial = initial_model_sigma_star()
        # The MLS threshold should be lower because signaling benefit offsets cost
        assert result['sigma_star'] < sigma_initial

    def test_B_lambda_positive(self):
        result = critical_threshold()
        assert result['B_lambda'] > 0

    def test_alpha_less_than_beta(self):
        result = critical_threshold()
        assert result['alpha_eff'] < result['beta_eff']


class TestInitialModelSigmaStar:
    def test_default_value(self):
        sigma_star = initial_model_sigma_star(C=0.42, alpha=0.40, beta=0.90)
        assert 0.4 < sigma_star < 0.7

    def test_increases_with_C(self):
        s_low = initial_model_sigma_star(C=0.30)
        s_high = initial_model_sigma_star(C=0.50)
        assert s_high > s_low


# ── Exotic Signals ─────────────────────────────────────────────────────


class TestExoticSignals:
    def test_cost_increases_with_distance(self):
        c_near = exotic_signaling_cost(250.0)
        c_far = exotic_signaling_cost(1600.0)
        assert c_far > c_near

    def test_value_increases_with_distance(self):
        v_near = exotic_signal_value(250.0)
        v_far = exotic_signal_value(1600.0)
        assert v_far > v_near

    def test_cost_at_reference_distance(self):
        c = exotic_signaling_cost(250.0)
        assert c == pytest.approx(0.05)  # base_cost * sqrt(1)

    def test_value_positive(self):
        for d in [250, 500, 800, 1600]:
            assert exotic_signal_value(float(d)) > 0


# ── Phase Space ────────────────────────────────────────────────────────


class TestPhaseSpace:
    def test_returns_correct_shape(self):
        sigma_r = np.linspace(0.1, 0.9, 5)
        C_r = np.linspace(0.05, 0.20, 4)
        result = phase_space(sigma_r, C_r)
        assert result['fitness_advantage'].shape == (5, 4)
        assert result['lambda_total'].shape == (5, 4)

    def test_high_sigma_low_C_favors_aggregation(self):
        sigma_r = np.array([0.8])
        C_r = np.array([0.05])
        result = phase_space(sigma_r, C_r)
        assert result['fitness_advantage'][0, 0] > 0
