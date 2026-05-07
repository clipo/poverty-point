"""Tests for the environmental model."""

import numpy as np
import pytest

from src.poverty_point.environment import (
    Environment, EnvironmentConfig, ResourceZone, EcologicalPatch,
    SEASONAL_PROFILES,
)


class TestSeasonalProfiles:
    def test_all_zones_have_profiles(self):
        for zone in ResourceZone:
            assert zone in SEASONAL_PROFILES

    def test_mast_peaks_in_fall(self):
        profile = SEASONAL_PROFILES[ResourceZone.MAST]
        assert profile.fall > profile.spring
        assert profile.fall > profile.summer
        assert profile.fall > profile.winter

    def test_aquatic_peaks_in_spring_summer(self):
        profile = SEASONAL_PROFILES[ResourceZone.AQUATIC]
        assert profile.spring > profile.winter
        assert profile.summer > profile.winter


class TestEcologicalPatch:
    def test_seasonal_productivity(self):
        patch = EcologicalPatch(
            patch_id=0,
            zone_type=ResourceZone.MAST,
            location=(100.0, 100.0),
            base_productivity=0.5,
            variability=0.1,
        )
        # Fall should have high productivity for mast
        fall_prod = patch.get_seasonal_productivity(month=10)
        winter_prod = patch.get_seasonal_productivity(month=1)
        assert fall_prod > winter_prod

    def test_productivity_non_negative(self):
        rng = np.random.default_rng(42)
        patch = EcologicalPatch(
            patch_id=0,
            zone_type=ResourceZone.AQUATIC,
            location=(0.0, 0.0),
            base_productivity=0.3,
            variability=0.5,  # High variability
        )
        for _ in range(100):
            patch.update_annual_shock(rng)
            for month in range(1, 13):
                prod = patch.get_seasonal_productivity(month)
                assert prod >= 0


class TestEnvironment:
    def setup_method(self):
        self.config = EnvironmentConfig()
        self.env = Environment(self.config, seed=42)

    def test_patch_creation(self):
        total_expected = (
            self.config.n_aquatic_patches +
            self.config.n_terrestrial_patches +
            self.config.n_mast_patches +
            self.config.n_ecotone_patches
        )
        assert len(self.env.patches) == total_expected

    def test_all_zone_types_present(self):
        zone_types = {p.zone_type for p in self.env.patches}
        for zone in ResourceZone:
            assert zone in zone_types

    def test_zone_productivity(self):
        self.env.month = 6  # Summer
        for zone in ResourceZone:
            prod = self.env.get_zone_productivity(zone)
            assert prod >= 0

    def test_advance_year(self):
        """Advancing year should change patch annual shocks."""
        self.env.month = 6
        prods_before = [p.get_seasonal_productivity(6) for p in self.env.patches]
        self.env.advance_year()
        prods_after = [p.get_seasonal_productivity(6) for p in self.env.patches]
        # At least some should change due to new shocks
        assert prods_before != prods_after

    def test_location_value(self):
        center = self.config.region_size / 2
        values = self.env.get_location_value((center, center), access_radius=100.0)
        assert 'total' in values
        assert values['total'] >= 0
        assert 'diversity_bonus' in values

    def test_ecotone_has_diversity(self):
        """Location near ecotone patches should access multiple zones."""
        center = self.config.region_size / 2
        values = self.env.get_location_value((center, center), access_radius=100.0)
        assert values.get('n_zones_accessible', 0) >= 2

    def test_find_optimal_site(self):
        best_loc, best_val = self.env.find_optimal_aggregation_site(
            n_candidates=50, access_radius=80.0
        )
        assert 0 <= best_loc[0] <= self.config.region_size
        assert 0 <= best_loc[1] <= self.config.region_size
        assert best_val > 0

    def test_covariance_matrix_valid(self):
        """Covariance matrix should be positive semi-definite."""
        eigvals = np.linalg.eigvalsh(self.env.cov_matrix)
        assert eigvals.min() >= -1e-10  # Allow small numerical error
