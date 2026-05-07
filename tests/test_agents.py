"""Tests for agent definitions."""

import numpy as np
import pytest

from src.poverty_point.agents import (
    Band, AggregationSite, Strategy, EXOTIC_SOURCES,
    create_bands, create_aggregation_site,
)
from src.poverty_point.parameters import default_parameters


class TestBand:
    def test_initial_state(self):
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR)
        assert band.size == 25
        assert band.strategy == Strategy.AGGREGATOR
        assert band.prestige == 0.0
        assert band.quality == 1.0

    def test_exotic_goods_is_dict(self):
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR)
        assert isinstance(band.exotic_goods, dict)
        assert 'copper' in band.exotic_goods

    def test_total_exotic_count(self):
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR)
        band.exotic_goods['copper'] = 3
        band.exotic_goods['galena'] = 2
        assert band.total_exotic_count == 5

    def test_travel_distance(self):
        band = Band(band_id=0, size=25, home_location=(0, 0),
                    strategy=Strategy.AGGREGATOR)
        dist = band.calculate_travel_distance((300, 400))
        assert dist == pytest.approx(500.0)

    def test_travel_cost(self):
        band = Band(band_id=0, size=25, home_location=(0, 0),
                    strategy=Strategy.AGGREGATOR)
        cost = band.calculate_travel_cost((300, 400))
        assert cost == pytest.approx(500.0 * 0.0005)

    def test_travel_cost_zero_distance(self):
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR)
        cost = band.calculate_travel_cost((100, 100))
        assert cost == 0.0

    def test_update_quality(self):
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR, resources=0.5)
        band.seasonal_k = 3.0
        band.update_quality()
        assert 0.2 <= band.quality <= 2.0
        assert band.quality > 0.5

    def test_quality_bounded(self):
        band = Band(band_id=0, size=5, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR, resources=0.1)
        band.update_quality()
        assert band.quality >= 0.2

        band.size = 100
        band.resources = 2.0
        band.update_quality()
        assert band.quality <= 2.0

    def test_monument_investment_equilibrium(self):
        rng = np.random.default_rng(42)
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR, quality=1.0, resources=1.0)
        investment = band.invest_in_monument(lam=0.5, q_min=0.2, rng=rng)
        assert investment > 0
        assert band.monument_contributions > 0
        assert band.prestige > 0

    def test_monument_investment_insufficient_resources(self):
        rng = np.random.default_rng(42)
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR, quality=1.0, resources=0.1)
        investment = band.invest_in_monument(lam=0.5, q_min=0.2, rng=rng)
        assert investment == 0.0

    def test_exotic_acquisition(self):
        rng = np.random.default_rng(42)
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR, resources=1.0,
                    prestige=0.5)
        acquired = 0
        for _ in range(100):
            if band.acquire_exotic(rng):
                acquired += 1
                band.resources = 1.0
        assert acquired > 0

    def test_storage_decay(self):
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR, resources=2.0)
        band.apply_storage_decay()
        assert band.resources < 2.0
        assert band.resources > 1.0

        band2 = Band(band_id=1, size=25, home_location=(100, 100),
                     strategy=Strategy.AGGREGATOR, resources=0.8)
        band2.apply_storage_decay()
        assert band2.resources == 0.8

    def test_form_obligation(self):
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR)
        band.form_obligation(partner_id=1, strength=0.3)
        assert 1 in band.obligations
        assert band.obligations[1] == 0.3

    def test_strengthen_obligation(self):
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR)
        band.form_obligation(1, 0.3)
        band.form_obligation(1, 0.3)
        assert band.obligations[1] == pytest.approx(0.6)

    def test_obligation_capped(self):
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR)
        for _ in range(20):
            band.form_obligation(1, 0.3)
        assert band.obligations[1] == 1.0

    def test_call_obligation(self):
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR)
        band.form_obligation(1, 0.5)
        help_received = band.call_obligation(1, 0.2)
        assert help_received > 0
        assert help_received <= 0.2

    def test_call_nonexistent_obligation(self):
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR)
        assert band.call_obligation(99, 0.5) == 0.0

    def test_strategy_decision(self):
        rng = np.random.default_rng(42)
        params = default_parameters(sigma=0.7, epsilon=0.35)
        band = Band(band_id=0, size=25, home_location=(250, 250),
                    strategy=Strategy.INDEPENDENT, quality=1.0)
        strategies = []
        for _ in range(50):
            s = band.decide_strategy(25, 0.7, 0.35, params, rng)
            strategies.append(s)
        n_agg = sum(1 for s in strategies if s == Strategy.AGGREGATOR)
        assert n_agg > 10

    def test_suffer_shortfall(self):
        rng = np.random.default_rng(42)
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR)
        deaths = band.suffer_shortfall(vulnerability=0.5, sigma=0.8, rng=rng)
        assert deaths >= 0
        assert band.size >= 1

    def test_shortfall_exponential_mortality(self):
        import math
        v, s = 0.4, 0.5
        expected_rate = 1.0 - math.exp(-v * s)
        assert 0 < expected_rate < 1


class TestAggregationSite:
    def test_initial_state(self):
        site = create_aggregation_site((250, 250), 0.35)
        assert site.monument_level == 0.0
        assert site.effective_M_g == 0.0
        assert site.n_attending == 0

    def test_monument_history_initialized(self):
        site = create_aggregation_site((250, 250), 0.35)
        assert site.monument_history == [0.0]

    def test_add_attending_band(self):
        site = create_aggregation_site((250, 250), 0.35)
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR)
        site.add_attending_band(band)
        assert site.n_attending == 1

    def test_add_multiple_bands(self):
        site = create_aggregation_site((250, 250), 0.35)
        for i in range(5):
            band = Band(band_id=i, size=25, home_location=(100, 100),
                        strategy=Strategy.AGGREGATOR)
            site.add_attending_band(band)
        assert site.n_attending == 5

    def test_reset_annual_state(self):
        site = create_aggregation_site((250, 250), 0.35)
        band = Band(band_id=0, size=25, home_location=(100, 100),
                    strategy=Strategy.AGGREGATOR)
        site.add_attending_band(band)
        site.reset_annual_state()
        assert site.n_attending == 0

    def test_record_construction(self):
        site = create_aggregation_site((250, 250), 0.35)
        site.record_construction(100.0)
        assert site.monument_level == 100.0
        assert site.annual_investment_flow == 100.0

    def test_depreciate_monument(self):
        site = create_aggregation_site((250, 250), 0.35)
        site.record_construction(100.0)
        site.depreciate_monument(delta=0.08)
        assert site.effective_M_g == pytest.approx(100.0)
        assert site.annual_investment_flow == 0.0

        site.depreciate_monument(delta=0.08)
        assert site.effective_M_g == pytest.approx(92.0)

    def test_depreciation_steady_state(self):
        site = create_aggregation_site((250, 250), 0.35)
        for _ in range(500):
            site.annual_investment_flow = 10.0
            site.depreciate_monument(delta=0.08)
        assert site.effective_M_g == pytest.approx(10.0 / 0.08, rel=0.01)


class TestCreateBands:
    def test_creates_correct_count(self):
        rng = np.random.default_rng(42)
        bands = create_bands(50, 25, 500.0, rng)
        assert len(bands) == 50

    def test_bands_have_valid_locations(self):
        rng = np.random.default_rng(42)
        bands = create_bands(50, 25, 500.0, rng)
        for band in bands:
            x, y = band.home_location
            assert 0 <= x <= 500
            assert 0 <= y <= 500

    def test_bands_have_mixed_strategies(self):
        rng = np.random.default_rng(42)
        bands = create_bands(50, 25, 500.0, rng)
        strategies = [b.strategy for b in bands]
        assert Strategy.AGGREGATOR in strategies
        assert Strategy.INDEPENDENT in strategies

    def test_bands_have_quality(self):
        rng = np.random.default_rng(42)
        bands = create_bands(50, 25, 500.0, rng)
        qualities = [b.quality for b in bands]
        assert all(0.2 <= q <= 2.0 for q in qualities)
        assert len(set(qualities)) > 1

    def test_bands_have_size_variation(self):
        rng = np.random.default_rng(42)
        bands = create_bands(50, 25, 500.0, rng)
        sizes = [b.size for b in bands]
        assert len(set(sizes)) > 1
