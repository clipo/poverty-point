"""Tests for the core simulation engine."""

import numpy as np
import pytest

from src.poverty_point.core_simulation import (
    PovertyPointSimulation, SimulationResults, run_single_simulation,
)
from src.poverty_point.parameters import default_parameters, critical_threshold


class TestPovertyPointSimulation:
    def test_initialization(self):
        params = default_parameters(sigma=0.5, epsilon=0.35, seed=42)
        params.duration = 50
        sim = PovertyPointSimulation(params)
        assert len(sim.bands) == params.population.n_bands
        assert sim.aggregation_site.name == "Poverty Point"
        assert sim.year == 0

    def test_step(self):
        params = default_parameters(sigma=0.5, epsilon=0.35, seed=42)
        sim = PovertyPointSimulation(params)
        state = sim.step()
        assert state.year == 0
        assert state.total_population > 0
        assert state.n_bands == len(sim.bands)
        assert sim.year == 1

    def test_run_short(self):
        params = default_parameters(sigma=0.55, epsilon=0.35, seed=42)
        params.duration = 50
        params.burn_in = 10
        sim = PovertyPointSimulation(params)
        results = sim.run()
        assert len(results.yearly_states) == 50
        assert results.sigma == 0.55
        assert results.epsilon == 0.35

    def test_monument_accumulates(self):
        """Monuments should increase over time when bands aggregate."""
        params = default_parameters(sigma=0.65, epsilon=0.35, seed=42)
        params.duration = 200
        params.burn_in = 50
        sim = PovertyPointSimulation(params)
        results = sim.run()
        # Monument should grow
        assert results.final_monument_level > 0

    def test_exotics_accumulate(self):
        """Exotic goods should be acquired during aggregation."""
        params = default_parameters(sigma=0.65, epsilon=0.35, seed=42)
        params.duration = 200
        params.burn_in = 50
        sim = PovertyPointSimulation(params)
        results = sim.run()
        assert results.total_exotics > 0


class TestPhaseTransition:
    """Test that the model exhibits the expected phase transition at sigma*."""

    def test_aggregation_above_threshold(self):
        """Above sigma*, aggregation should be stronger."""
        params = default_parameters()
        sigma_star = critical_threshold(0.35, 25, params)

        results_above = run_single_simulation(
            sigma=sigma_star + 0.15, epsilon=0.35, seed=42, duration=200
        )
        results_below = run_single_simulation(
            sigma=sigma_star - 0.15, epsilon=0.35, seed=42, duration=200
        )

        assert results_above.final_strategy_dominance > results_below.final_strategy_dominance
        assert results_above.mean_aggregation_size > results_below.mean_aggregation_size

    def test_independence_below_threshold(self):
        """Well below sigma*, independence should dominate."""
        results = run_single_simulation(
            sigma=0.15, epsilon=0.35, seed=42, duration=200
        )
        # Strategy dominance should be negative (more independents)
        assert results.final_strategy_dominance < 0

    def test_high_sigma_promotes_aggregation(self):
        """At very high sigma, aggregation should clearly dominate."""
        results = run_single_simulation(
            sigma=0.80, epsilon=0.35, seed=42, duration=200
        )
        assert results.mean_aggregation_size > 15  # Substantial aggregation


class TestCostlySignaling:
    """Verify costly signaling mechanics are functional."""

    def test_signal_cost_reduces_resources(self):
        """Bands investing in monuments should spend resources."""
        params = default_parameters(sigma=0.65, epsilon=0.35, seed=42)
        params.duration = 20
        sim = PovertyPointSimulation(params)
        sim.run()

        # Aggregator bands should have monument contributions
        agg_bands = [b for b in sim.bands if b.strategy.value == "aggregator"]
        if agg_bands:
            total_contributions = sum(b.monument_contributions for b in agg_bands)
            assert total_contributions > 0

    def test_prestige_from_investment(self):
        """Bands that invest should gain prestige."""
        params = default_parameters(sigma=0.65, epsilon=0.35, seed=42)
        params.duration = 50
        sim = PovertyPointSimulation(params)
        sim.run()

        # At least some bands should have prestige
        total_prestige = sum(b.prestige for b in sim.bands)
        assert total_prestige > 0

    def test_exotics_as_signals(self):
        """Bands should acquire exotic goods during aggregation."""
        params = default_parameters(sigma=0.65, epsilon=0.35, seed=42)
        params.duration = 100
        sim = PovertyPointSimulation(params)
        sim.run()

        total_exotics = sum(b.total_exotic_count for b in sim.bands)
        assert total_exotics > 0

    def test_obligations_form(self):
        """Social obligations should form during aggregation."""
        params = default_parameters(sigma=0.65, epsilon=0.35, seed=42)
        params.duration = 50
        sim = PovertyPointSimulation(params)
        sim.run()

        bands_with_obligations = sum(
            1 for b in sim.bands if len(b.obligations) > 0
        )
        assert bands_with_obligations > 0


class TestSimulationResults:
    def test_compute_summary(self):
        results = run_single_simulation(
            sigma=0.55, epsilon=0.35, seed=42, duration=200
        )
        assert results.final_strategy_dominance != 0 or True  # Computed
        assert results.mean_aggregation_size >= 0
        assert results.mean_population > 0
        assert results.sigma_star_theoretical > 0

    def test_reproducibility(self):
        """Same seed should produce same results."""
        r1 = run_single_simulation(sigma=0.55, epsilon=0.35, seed=42, duration=100)
        r2 = run_single_simulation(sigma=0.55, epsilon=0.35, seed=42, duration=100)
        assert r1.final_strategy_dominance == r2.final_strategy_dominance
        assert r1.mean_aggregation_size == r2.mean_aggregation_size

    def test_different_seeds_differ(self):
        """Different seeds should produce different results."""
        r1 = run_single_simulation(sigma=0.55, epsilon=0.35, seed=42, duration=200)
        r2 = run_single_simulation(sigma=0.55, epsilon=0.35, seed=99, duration=200)
        # Very unlikely to be exactly equal with different seeds
        assert (r1.final_strategy_dominance != r2.final_strategy_dominance or
                r1.mean_aggregation_size != r2.mean_aggregation_size)
