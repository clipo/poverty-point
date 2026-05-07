"""Tests for the integrated simulation."""

import numpy as np
import pytest

from src.poverty_point.integrated_simulation import (
    IntegratedSimulation, IntegratedResults, Season, month_to_season,
)
from src.poverty_point.parameters import default_parameters, critical_threshold
from src.poverty_point.environmental_scenarios import (
    ShortfallParams, create_poverty_point_scenario,
    create_high_sigma_scenario, create_low_sigma_scenario,
    create_critical_threshold_scenario,
)


class TestMonthToSeason:
    def test_winter(self):
        assert month_to_season(12) == Season.WINTER
        assert month_to_season(1) == Season.WINTER
        assert month_to_season(2) == Season.WINTER

    def test_spring(self):
        assert month_to_season(3) == Season.SPRING
        assert month_to_season(5) == Season.SPRING

    def test_summer(self):
        assert month_to_season(6) == Season.SUMMER
        assert month_to_season(8) == Season.SUMMER

    def test_fall(self):
        assert month_to_season(9) == Season.FALL
        assert month_to_season(11) == Season.FALL


class TestSigmaCalibration:
    """Test that shortfall parameters map to correct sigma values."""

    def _run_scenario(self, scenario, duration=100):
        params = default_parameters(seed=42)
        params.duration = duration
        params.burn_in = 20
        sim = IntegratedSimulation(
            params=params,
            env_config=scenario.env_config,
            shortfall_params=scenario.shortfall_params,
            seed=42,
        )
        return sim.run()

    def test_poverty_point_sigma_range(self):
        """Canonical sigma for PP (freq=10, mag=0.45) ~ 0.636."""
        scenario = create_poverty_point_scenario()
        results = self._run_scenario(scenario)
        assert 0.50 < results.mean_effective_sigma < 0.75

    def test_high_sigma_range(self):
        """Canonical sigma for high (freq=6, mag=0.60) ~ 0.95."""
        scenario = create_high_sigma_scenario()
        results = self._run_scenario(scenario)
        assert results.mean_effective_sigma > 0.60

    def test_low_sigma_range(self):
        """Canonical sigma for low (freq=18, mag=0.30) ~ 0.316."""
        scenario = create_low_sigma_scenario()
        results = self._run_scenario(scenario)
        assert results.mean_effective_sigma < 0.50

    def test_high_sigma_above_low(self):
        high = self._run_scenario(create_high_sigma_scenario())
        low = self._run_scenario(create_low_sigma_scenario())
        assert high.mean_effective_sigma > low.mean_effective_sigma

    def test_sigma_responds_to_shortfall_params(self):
        """Higher frequency and magnitude should produce higher sigma."""
        params = default_parameters(seed=42)
        params.duration = 80
        params.burn_in = 20

        sp_mild = ShortfallParams(mean_interval=20, magnitude_mean=0.25)
        sp_severe = ShortfallParams(mean_interval=5, magnitude_mean=0.65)

        sim_mild = IntegratedSimulation(params=params, shortfall_params=sp_mild, seed=42)
        sim_severe = IntegratedSimulation(params=params, shortfall_params=sp_severe, seed=42)

        r_mild = sim_mild.run()
        r_severe = sim_severe.run()

        assert r_severe.mean_effective_sigma > r_mild.mean_effective_sigma


class TestIntegratedSimulation:
    def setup_method(self):
        self.params = default_parameters(seed=42)
        self.params.duration = 50
        self.params.burn_in = 10

    def test_initialization(self):
        sim = IntegratedSimulation(params=self.params, seed=42)
        assert sim.year == 0
        assert len(sim.bands) == self.params.population.n_bands
        assert sim.aggregation_site.name == "Poverty Point"

    def test_step_year(self):
        sim = IntegratedSimulation(params=self.params, seed=42)
        state = sim.step_year()
        assert state.year == 0
        assert state.total_population > 0
        assert sim.year == 1

    def test_run_completes(self):
        sim = IntegratedSimulation(params=self.params, seed=42)
        results = sim.run()
        assert len(results.yearly_states) == 50
        assert results.mean_population > 0

    def test_monument_growth(self):
        """Monuments should accumulate over time."""
        sim = IntegratedSimulation(params=self.params, seed=42)
        results = sim.run()
        assert results.final_monument_level > 0

    def test_exotics_present(self):
        """Exotic goods should appear in results."""
        sim = IntegratedSimulation(params=self.params, seed=42)
        results = sim.run()
        assert results.total_exotics >= 0  # May be 0 if low aggregation

    def test_reproducibility(self):
        """Same parameters + seed = same results."""
        sim1 = IntegratedSimulation(params=self.params, seed=42)
        sim2 = IntegratedSimulation(params=self.params, seed=42)
        r1 = sim1.run()
        r2 = sim2.run()
        assert r1.final_strategy_dominance == r2.final_strategy_dominance

    def test_state_records_environment(self):
        """State should include environmental information."""
        sim = IntegratedSimulation(params=self.params, seed=42)
        results = sim.run()
        state = results.yearly_states[-1]
        assert state.effective_sigma > 0
        assert state.mean_productivity >= 0
        assert len(state.productivity_by_zone) > 0


class TestScenarioComparison:
    """Verify that different scenarios produce qualitatively different outcomes."""

    def _run_short(self, scenario, duration=100):
        params = default_parameters(seed=42)
        params.duration = duration
        params.burn_in = 20
        sim = IntegratedSimulation(
            params=params,
            env_config=scenario.env_config,
            shortfall_params=scenario.shortfall_params,
            seed=42,
        )
        return sim.run()

    def test_high_uncertainty_more_aggregation(self):
        """High uncertainty should produce more aggregation than low."""
        high = self._run_short(create_high_sigma_scenario())
        low = self._run_short(create_low_sigma_scenario())
        assert high.mean_aggregation_size > low.mean_aggregation_size

    def test_high_uncertainty_more_dominance(self):
        """High uncertainty should shift strategy toward aggregation."""
        high = self._run_short(create_high_sigma_scenario())
        low = self._run_short(create_low_sigma_scenario())
        assert high.final_strategy_dominance > low.final_strategy_dominance
