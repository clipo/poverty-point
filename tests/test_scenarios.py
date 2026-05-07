"""Tests for environmental scenarios."""

import pytest

from src.poverty_point.environmental_scenarios import (
    ShortfallParams, EnvironmentalScenario,
    create_high_sigma_scenario, create_low_sigma_scenario,
    create_poverty_point_scenario, create_critical_threshold_scenario,
    SCENARIOS, get_scenario, list_scenarios,
)
from src.poverty_point.parameters import (
    calculate_sigma_from_shortfall, critical_threshold, default_parameters,
)


class TestShortfallParams:
    def test_defaults(self):
        sp = ShortfallParams()
        assert sp.mean_interval == 10.0
        assert sp.magnitude_mean == 0.5
        assert sp.magnitude_std == 0.15
        assert sp.duration_scale == 2.5


class TestScenarioCreation:
    def test_high_sigma(self):
        scenario = create_high_sigma_scenario()
        assert scenario.shortfall_params.mean_interval < 10
        assert scenario.shortfall_params.magnitude_mean > 0.5

    def test_low_sigma(self):
        scenario = create_low_sigma_scenario()
        assert scenario.shortfall_params.mean_interval > 15
        assert scenario.shortfall_params.magnitude_mean < 0.4

    def test_poverty_point(self):
        scenario = create_poverty_point_scenario()
        assert scenario.name == "Poverty Point"
        assert scenario.expected_epsilon > 0.3

    def test_critical_threshold(self):
        scenario = create_critical_threshold_scenario(target_sigma=0.57)
        lo, hi = scenario.expected_sigma_range
        assert lo <= 0.57 <= hi

    def test_critical_threshold_various(self):
        """Different target sigmas should produce different parameters."""
        s_low = create_critical_threshold_scenario(target_sigma=0.2)
        s_high = create_critical_threshold_scenario(target_sigma=0.7)
        assert s_high.shortfall_params.magnitude_mean > s_low.shortfall_params.magnitude_mean
        assert s_high.shortfall_params.mean_interval < s_low.shortfall_params.mean_interval

    def test_poverty_point_above_threshold(self):
        """Poverty Point's canonical sigma should exceed sigma*."""
        scenario = create_poverty_point_scenario()
        sp = scenario.shortfall_params
        pp_sigma = calculate_sigma_from_shortfall(sp.mean_interval, sp.magnitude_mean)

        params = default_parameters()
        sigma_star = critical_threshold(scenario.expected_epsilon, 25, params)

        assert pp_sigma > sigma_star, (
            f"PP sigma ({pp_sigma:.3f}) should be above "
            f"sigma* ({sigma_star:.3f}) at eps={scenario.expected_epsilon}"
        )


class TestPredefinedScenarios:
    def test_all_exist(self):
        assert "high" in SCENARIOS
        assert "low" in SCENARIOS
        assert "poverty_point" in SCENARIOS
        assert "critical" in SCENARIOS

    def test_get_scenario(self):
        scenario = get_scenario("poverty_point")
        assert isinstance(scenario, EnvironmentalScenario)
        assert scenario.name == "Poverty Point"

    def test_get_unknown_raises(self):
        with pytest.raises(ValueError):
            get_scenario("nonexistent")

    def test_list_scenarios(self, capsys):
        list_scenarios()
        captured = capsys.readouterr()
        assert "poverty_point" in captured.out
        assert "high" in captured.out
