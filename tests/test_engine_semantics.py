"""
Tests for engine semantics introduced by the ODD-alignment revision:

- one execution of each annual process per simulated year
- heterogeneous band quality drawn from U[q_min, q_max]
- deterministic fission above max_band_size with half-weight inheritance
- dissolution below min_band_size
- realized network degree feeding aggregator vulnerability (seasonal_k)
- reciprocal obligation formation
- monument signal-stock depreciation applied annually
- fitness-weighted deaths
- prev-year attendance driving the decision-stage aggregation size
"""

import numpy as np
import pytest

from src.poverty_point.integrated_simulation import IntegratedSimulation
from src.poverty_point.parameters import default_parameters
from src.poverty_point.agents import Band, Strategy


def make_sim(duration=10, seed=7, signal_conditional=True):
    params = default_parameters(seed=seed)
    params.duration = duration
    params.burn_in = 0
    return IntegratedSimulation(
        params=params, seed=seed,
        signal_conditional_partners=signal_conditional,
    )


class TestAnnualScheduling:
    def test_one_strategy_decision_per_year(self):
        sim = make_sim(duration=5)
        for _ in range(5):
            sim.step_year()
        # A founding band that survived has exactly one decision per year.
        founders = [b for b in sim.bands if b.band_id < 50]
        assert founders, "no founding bands survived a 5-year run"
        for band in founders:
            assert len(band.strategy_history) == 5
            assert len(band.fitness_history) == 5

    def test_one_yearly_state_per_year(self):
        sim = make_sim(duration=5)
        for _ in range(5):
            sim.step_year()
        assert len(sim.results.yearly_states) == 5


class TestQualityHeterogeneity:
    def test_quality_drawn_from_uniform(self):
        sim = make_sim()
        qualities = np.array([b.quality for b in sim.bands])
        assert qualities.min() >= sim.params.signaling.q_min
        assert qualities.max() <= sim.params.signaling.q_max
        assert qualities.std() > 0.1, "quality should be heterogeneous"


class TestFissionAndDissolution:
    def test_fission_above_max_size(self):
        sim = make_sim()
        band = sim.bands[0]
        band.size = sim.params.population.max_band_size + 10
        band.obligations = {1: 0.8, 2: 0.4}
        band.monument_contributions = 10.0
        n_before = len(sim.bands)

        sim._apply_fission_and_dissolution()

        assert len(sim.bands) == n_before + 1
        daughter = sim.bands[-1]
        assert daughter.band_id == sim.next_band_id - 1
        # Half-weight inheritance
        assert daughter.obligations == {1: 0.4, 2: 0.2}
        assert daughter.monument_contributions == pytest.approx(5.0)
        # Parent and daughter together hold the original members
        assert band.size + daughter.size == sim.params.population.max_band_size + 10
        assert band.size <= sim.params.population.max_band_size

    def test_dissolution_below_min_size(self):
        sim = make_sim()
        band = sim.bands[0]
        band.size = sim.params.population.min_band_size - 2
        gone_id = band.band_id
        n_before = len(sim.bands)

        sim._apply_fission_and_dissolution()

        assert len(sim.bands) == n_before - 1
        assert gone_id not in sim.band_by_id


class TestNetworkVulnerability:
    def test_aggregator_seasonal_k_reflects_obligations(self):
        sim = make_sim(duration=15)
        for _ in range(15):
            sim.step_year()
        k_0 = sim.params.network.k_0
        aggregators = [b for b in sim.bands
                       if b.strategy == Strategy.AGGREGATOR and b.obligations]
        if not aggregators:
            pytest.skip("no aggregators with obligations in this run")
        assert any(b.seasonal_k > k_0 for b in aggregators), (
            "aggregators with obligations should have seasonal_k above k_0"
        )

    def test_independent_seasonal_k_is_baseline(self):
        sim = make_sim(duration=15)
        for _ in range(15):
            sim.step_year()
        k_0 = sim.params.network.k_0
        for band in sim.bands:
            if band.strategy == Strategy.INDEPENDENT:
                assert band.seasonal_k == pytest.approx(k_0)


class TestReciprocalObligations:
    def test_form_obligations_is_reciprocal(self):
        sim = make_sim(seed=3)
        # Register all bands as attending, then run partner formation.
        for band in sim.bands:
            band.strategy = Strategy.AGGREGATOR
            sim.aggregation_site.add_attending_band(band)
        for band in sim.bands:
            band.obligations = {}
        sim._form_obligations()
        edges = [(b.band_id, p) for b in sim.bands for p in b.obligations]
        assert edges, "expected some ties to form across 50 attending bands"
        for i, j in edges:
            assert i in sim.band_by_id[j].obligations, (
                f"tie {i}->{j} lacks the reciprocal edge"
            )


class TestDepreciation:
    def test_signal_stock_depreciates_below_cumulative(self):
        sim = make_sim(duration=30)
        for _ in range(30):
            sim.step_year()
        site = sim.aggregation_site
        if site.monument_level <= 0:
            pytest.skip("no construction occurred in this run")
        assert site.effective_M_g < site.monument_level
        assert site.effective_M_g > 0


class TestFitnessWeightedDeaths:
    def test_low_fitness_bands_lose_more_members(self):
        rng_hi = np.random.default_rng(11)
        rng_lo = np.random.default_rng(11)
        hi = Band(band_id=0, size=10_000, home_location=(0, 0),
                  strategy=Strategy.AGGREGATOR)
        lo = Band(band_id=1, size=10_000, home_location=(0, 0),
                  strategy=Strategy.AGGREGATOR)
        # Same births by fixing birth_rate=0; compare deaths via size change
        hi.reproduce(fitness=1.5, birth_rate=0.0, death_rate=0.02, rng=rng_hi)
        lo.reproduce(fitness=0.5, birth_rate=0.0, death_rate=0.02, rng=rng_lo)
        assert (10_000 - lo.size) > (10_000 - hi.size)


class TestDecisionState:
    def test_prev_attendance_feeds_next_year(self):
        sim = make_sim(duration=3)
        sim.step_year()
        assert sim.prev_n_attending == sim.aggregation_site.n_attending
