"""Tests for parameter definitions and fitness functions."""

import numpy as np
import pytest

from src.poverty_point.parameters import (
    SimulationParameters, default_parameters,
    W_aggregator, W_independent, critical_threshold,
    calculate_sigma_from_shortfall, calculate_sigma_from_cv,
    ARCHAEOLOGICAL_MONUMENT_VOLUME_M3,
)
from src.poverty_point.signaling_core import (
    SignalingParams, NetworkParams, ConflictParams, AggregationParams,
)


class TestMLSParameters:
    """Test the MLS parameter dataclasses."""

    def test_signaling_defaults(self):
        p = SignalingParams()
        assert p.q_min == 0.2
        assert p.q_max == 2.0
        assert p.lambda_W == 0.15
        assert p.delta == 0.08

    def test_network_defaults(self):
        p = NetworkParams()
        assert p.gamma == 0.05
        assert p.k_0 == 0.3
        assert p.k_max == 6.0

    def test_conflict_defaults(self):
        p = ConflictParams()
        assert p.P_base == 0.008
        assert p.conflict_mortality == 0.08

    def test_aggregation_defaults(self):
        p = AggregationParams()
        assert p.C_opportunity == 0.12
        assert p.C_signal == 0.18
        assert p.f_agg == 0.25
        assert p.delta_net == 0.40


class TestFitnessPositivity:
    """Test that fitness is always positive and bounded."""

    def setup_method(self):
        self.params = default_parameters()

    def test_aggregator_always_positive(self):
        for sigma in [0.0, 0.3, 0.5, 0.7, 0.9]:
            w = W_aggregator(sigma, 0.35, 25, self.params)
            assert w >= 0, f"W_agg({sigma}) = {w} should be >= 0"

    def test_independent_always_positive(self):
        for sigma in [0.0, 0.3, 0.5, 0.7, 0.9]:
            w = W_independent(sigma, self.params)
            assert w >= 0, f"W_ind({sigma}) = {w} should be >= 0"

    def test_bounded_above(self):
        w0 = W_aggregator(0.0, 0.35, 25, self.params)
        assert w0 < 2.0


class TestCanonicalSigma:
    """Test the canonical sigma formula."""

    def test_poverty_point(self):
        sigma = calculate_sigma_from_shortfall(10, 0.45)
        assert 0.60 < sigma < 0.68

    def test_rapa_nui(self):
        sigma = calculate_sigma_from_shortfall(6, 0.60)
        assert sigma == pytest.approx(1.0, abs=0.05)

    def test_rapa_iti(self):
        sigma = calculate_sigma_from_shortfall(18, 0.30)
        assert 0.28 < sigma < 0.35

    def test_monotonicity_magnitude(self):
        s1 = calculate_sigma_from_shortfall(10, 0.30)
        s2 = calculate_sigma_from_shortfall(10, 0.60)
        assert s2 > s1

    def test_monotonicity_frequency(self):
        s1 = calculate_sigma_from_shortfall(20, 0.45)
        s2 = calculate_sigma_from_shortfall(5, 0.45)
        assert s2 > s1

    def test_clipped_to_unit(self):
        assert 0 <= calculate_sigma_from_shortfall(2, 0.99) <= 1
        assert 0 <= calculate_sigma_from_shortfall(50, 0.01) <= 1

    def test_zero_frequency_raises(self):
        with pytest.raises(ValueError):
            calculate_sigma_from_shortfall(0, 0.5)

    def test_cv_based_estimation(self):
        rng = np.random.default_rng(42)
        ts = rng.normal(1.0, 0.3, size=100)
        sigma = calculate_sigma_from_cv(ts)
        assert 0 <= sigma <= 1
        assert sigma > 0.1


class TestParameterValidation:
    """Test SimulationParameters.validate()."""

    def test_valid_defaults_no_error(self):
        params = default_parameters()
        warnings = params.validate()
        assert isinstance(warnings, list)

    def test_sigma_out_of_range_raises(self):
        params = default_parameters()
        params.sigma = 1.5
        with pytest.raises(ValueError):
            params.validate()

    def test_q_min_ge_q_max_raises(self):
        params = default_parameters()
        params.signaling = SignalingParams(q_min=2.0, q_max=1.0)
        with pytest.raises(ValueError):
            params.validate()


class TestFitnessFunctions:
    def setup_method(self):
        self.params = default_parameters(sigma=0.5, epsilon=0.35)

    def test_aggregator_positive(self):
        w = W_aggregator(0.5, 0.35, 25, self.params)
        assert w > 0

    def test_independent_positive(self):
        w = W_independent(0.5, self.params)
        assert w > 0

    def test_aggregator_decreases_with_sigma(self):
        w_low = W_aggregator(0.2, 0.35, 25, self.params)
        w_high = W_aggregator(0.8, 0.35, 25, self.params)
        assert w_low > w_high

    def test_independent_decreases_with_sigma(self):
        w_low = W_independent(0.2, self.params)
        w_high = W_independent(0.8, self.params)
        assert w_low > w_high

    def test_ecotone_buffers_aggregator(self):
        w_no_ecotone = W_aggregator(0.5, 0.0, 25, self.params)
        w_ecotone = W_aggregator(0.5, 0.35, 25, self.params)
        assert w_ecotone > w_no_ecotone

    def test_aggregator_above_threshold(self):
        sigma_star = critical_threshold(0.35, 25, self.params)
        if sigma_star < 0.95:
            sigma_above = min(sigma_star + 0.05, 0.99)
            w_agg = W_aggregator(sigma_above, 0.35, 25, self.params)
            w_ind = W_independent(sigma_above, self.params)
            assert w_agg > w_ind

    def test_independent_below_threshold(self):
        sigma_star = critical_threshold(0.35, 25, self.params)
        if sigma_star > 0.05:
            sigma_below = max(sigma_star - 0.10, 0.01)
            w_agg = W_aggregator(sigma_below, 0.35, 25, self.params)
            w_ind = W_independent(sigma_below, self.params)
            assert w_ind > w_agg

    def test_fitness_floor_at_zero(self):
        assert W_aggregator(0.99, 0.0, 1, self.params) >= 0
        assert W_independent(0.99, self.params) >= 0


class TestCriticalThreshold:
    def setup_method(self):
        self.params = default_parameters()

    def test_default_sigma_star(self):
        sigma_star = critical_threshold(0.35, 25, self.params)
        assert 0.1 < sigma_star < 0.9

    def test_higher_epsilon_lowers_threshold(self):
        s1 = critical_threshold(0.10, 25, self.params)
        s2 = critical_threshold(0.40, 25, self.params)
        assert s2 < s1

    def test_threshold_between_zero_and_one(self):
        sigma_star = critical_threshold(0.35, 25, self.params)
        assert 0 < sigma_star < 1

    def test_zero_epsilon(self):
        s_no = critical_threshold(0.0, 25, self.params)
        s_with = critical_threshold(0.35, 25, self.params)
        assert s_no > s_with


class TestMonumentScaling:
    def test_constant_defined(self):
        assert ARCHAEOLOGICAL_MONUMENT_VOLUME_M3 == 750_000


class TestDefaultParameters:
    def test_creates_valid_params(self):
        params = default_parameters(sigma=0.5, epsilon=0.35, seed=42)
        assert params.sigma == 0.5
        assert params.epsilon == 0.35
        assert params.seed == 42
        assert isinstance(params, SimulationParameters)

    def test_has_mls_params(self):
        params = default_parameters()
        assert hasattr(params, 'signaling')
        assert hasattr(params, 'network')
        assert hasattr(params, 'conflict')
        assert hasattr(params, 'aggregation')
        assert params.aggregation.C_signal == 0.18
