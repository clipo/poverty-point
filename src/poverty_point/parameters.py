"""
Parameter definitions for the Poverty Point ABM.

Uses the multilevel signaling framework (signaling_core.py) for fitness
calculations. Vulnerability and cooperation benefits are derived from
network degree rather than assumed.

All parameters derive from the theoretical derivation in:
docs/THEORETICAL_DERIVATION.md
"""

from dataclasses import dataclass, field
from typing import Dict, List
import numpy as np

from .signaling_core import (
    AggregationParams,
    ConflictParams,
    NetworkParams,
    SignalingParams,
    aggregation_expected_fitness,
    critical_threshold as mls_critical_threshold,
    independent_expected_fitness,
    lambda_total_at_sigma,
)


# ── Archaeological constants ─────────────────────────────────────────────
# Total monument volume at Poverty Point from Ortmann & Kidder 2013.
# Used only for normalizing model output; the simulation tracks
# dimensionless cumulative investment units.
ARCHAEOLOGICAL_MONUMENT_VOLUME_M3 = 750_000


# ── Canonical sigma formula ──────────────────────────────────────────────

def calculate_sigma_from_shortfall(frequency: float, magnitude: float) -> float:
    """
    Canonical formula: sigma = magnitude * sqrt(20 / frequency), clipped to [0, 1].

    This is the single source of truth for converting shortfall parameters
    (frequency = mean interval in years, magnitude = proportional productivity
    reduction 0-1) into the abstract environmental-uncertainty scalar sigma.

    All other files must import this function rather than re-derive sigma.

    Parameters
    ----------
    frequency : float
        Mean interval between shortfall events (years).  Must be > 0.
    magnitude : float
        Proportional reduction in productivity during shortfalls (0 to 1).

    Returns
    -------
    float
        Environmental uncertainty parameter sigma in [0, 1].

    Examples
    --------
    >>> calculate_sigma_from_shortfall(10, 0.45)   # Poverty Point  -> ~0.636
    >>> calculate_sigma_from_shortfall(6, 0.60)    # Rapa Nui       -> ~1.095 -> clipped 0.95
    >>> calculate_sigma_from_shortfall(18, 0.30)   # Rapa Iti       -> ~0.316
    """
    if frequency <= 0:
        raise ValueError(f"frequency must be > 0, got {frequency}")
    sigma = magnitude * np.sqrt(20.0 / frequency)
    return float(np.clip(sigma, 0.0, 1.0))


def calculate_sigma_from_cv(timeseries: np.ndarray) -> float:
    """
    Independent sigma estimate from the coefficient of variation of a
    productivity proxy timeseries.

    Useful for cross-checking the formula-based sigma against observed data.

    Parameters
    ----------
    timeseries : array-like
        Proxy productivity values (e.g., water-balance reconstruction).

    Returns
    -------
    float
        sigma estimate in [0, 1].
    """
    ts = np.asarray(timeseries, dtype=float)
    ts = ts[np.isfinite(ts)]
    if len(ts) < 3 or np.mean(ts) == 0:
        return 0.0
    cv = np.std(ts) / np.abs(np.mean(ts))
    return float(np.clip(cv, 0.0, 1.0))


# ── Parameter dataclasses ────────────────────────────────────────────────


@dataclass
class EnvironmentParameters:
    """Environmental parameters."""

    # Region size (km)
    region_size: float = 500.0

    # Zone accessibility radius (km)
    access_radius: float = 50.0

    # Number of patches per zone
    n_aquatic_patches: int = 10
    n_terrestrial_patches: int = 12
    n_mast_patches: int = 8
    n_wetland_patches: int = 5

    # Base productivity by zone (relative units)
    base_productivity: Dict[str, float] = field(default_factory=lambda: {
        'aquatic': 0.70,
        'terrestrial': 0.60,
        'mast': 0.50,
        'wetland': 0.65
    })

    # Inter-annual variability by zone
    variability: Dict[str, float] = field(default_factory=lambda: {
        'aquatic': 0.15,
        'terrestrial': 0.10,
        'mast': 0.30,  # Mast highly variable
        'wetland': 0.12
    })

    # Zone covariance (negative = buffering effect)
    # Format: (zone1, zone2) -> covariance
    zone_covariance: Dict[tuple, float] = field(default_factory=lambda: {
        ('aquatic', 'terrestrial'): -0.3,   # Good buffering
        ('aquatic', 'mast'): 0.1,           # Slight positive
        ('terrestrial', 'mast'): 0.2,       # Moderate positive
        ('aquatic', 'wetland'): 0.3,        # Both water-dependent
        ('terrestrial', 'wetland'): -0.2,   # Some buffering
        ('mast', 'wetland'): 0.0            # Independent
    })


@dataclass
class PopulationParameters:
    """Population dynamics parameters."""

    # Initial number of bands
    n_bands: int = 50

    # Initial band size (individuals)
    initial_band_size: int = 25

    # Demographic rates
    birth_rate: float = 0.03      # Per capita annual
    death_rate: float = 0.02      # Per capita annual (non-shortfall)

    # Band size constraints
    min_band_size: int = 5        # Below this, band dissolves
    max_band_size: int = 50       # Above this, band fissions


@dataclass
class SimulationParameters:
    """Complete parameter set for simulation.

    Uses the multilevel signaling framework. Vulnerability (alpha, beta)
    and cooperation benefits are derived from network degree rather than
    assumed as fixed parameters.
    """

    # MLS framework parameters
    signaling: SignalingParams = field(default_factory=SignalingParams)
    network: NetworkParams = field(default_factory=NetworkParams)
    conflict: ConflictParams = field(default_factory=ConflictParams)
    aggregation: AggregationParams = field(default_factory=AggregationParams)

    # Environment and population
    environment: EnvironmentParameters = field(default_factory=EnvironmentParameters)
    population: PopulationParameters = field(default_factory=PopulationParameters)

    # Simulation control
    duration: int = 600           # Years (1700-1100 BCE)
    burn_in: int = 100            # Years before recording
    seed: int = 42                # Random seed

    # Phase space parameters (set per run)
    sigma: float = 0.5            # Environmental uncertainty
    epsilon: float = 0.35         # Ecotone advantage at aggregation site

    def validate(self) -> List[str]:
        """
        Check parameter bounds. Raises ValueError for impossible values,
        returns a list of warning strings for suspicious ones.
        """
        warnings_list: List[str] = []

        # ── Hard errors ──
        if self.aggregation.C_opportunity < 0:
            raise ValueError(
                f"C_opportunity must be >= 0, got {self.aggregation.C_opportunity}"
            )
        if self.aggregation.C_signal < 0:
            raise ValueError(
                f"C_signal must be >= 0, got {self.aggregation.C_signal}"
            )

        C_total = (
            self.aggregation.C_opportunity
            + self.aggregation.C_signal
            + self.aggregation.C_travel_per_km * 100  # at 100 km reference
        )
        if C_total >= 1.0:
            raise ValueError(f"C_total must be < 1.0, got {C_total}")

        if not (0 <= self.sigma <= 1):
            raise ValueError(f"sigma must be in [0,1], got {self.sigma}")

        if not (0 <= self.epsilon <= 1):
            raise ValueError(f"epsilon must be in [0,1], got {self.epsilon}")

        if self.signaling.q_min >= self.signaling.q_max:
            raise ValueError(
                f"q_min ({self.signaling.q_min}) must be < q_max ({self.signaling.q_max})"
            )

        # ── Soft warnings ──
        if C_total > 0.6:
            warnings_list.append(
                f"C_total ({C_total:.2f}) is very high; "
                f"aggregation may never be adaptive"
            )

        if self.network.gamma <= 0:
            warnings_list.append(
                "gamma <= 0: network partners provide no buffering"
            )

        return warnings_list


# ── Fitness functions (delegating to MLS framework) ──────────────────────


def W_aggregator(sigma: float, epsilon: float, n: float,
                 params: SimulationParameters,
                 band_quality: float = 1.0,
                 travel_distance: float = 100.0,
                 M_g: float = -1.0,
                 lam: float = -1.0) -> float:
    """
    Calculate fitness for aggregator strategy using MLS framework.

    W_agg = (1 - C_total)(1 - alpha_eff * sigma_eff)(1 - m*(1-r)*P_base) + B(lambda)

    If M_g and lam are not provided, computes them via the lambda-sigma
    feedback loop at the given sigma.

    Args:
        sigma: Environmental uncertainty
        epsilon: Ecotone advantage
        n: Number of bands aggregating
        params: Full parameter set
        band_quality: Band productive capacity (default 1.0)
        travel_distance: Distance to aggregation site in km
        M_g: Pre-computed monument stock (auto-computed if < 0)
        lam: Pre-computed total lambda (auto-computed if < 0)

    Returns:
        Fitness value (always >= 0)
    """
    if M_g < 0 or lam < 0:
        eq = lambda_total_at_sigma(
            sigma, params.signaling, params.network,
            params.conflict, params.aggregation, int(n),
        )
        M_g = eq['M_g']
        lam = eq['lambda_total']

    return aggregation_expected_fitness(
        sigma, epsilon, int(n), band_quality, travel_distance,
        M_g, lam,
        params.signaling, params.network, params.conflict, params.aggregation,
    )


def W_independent(sigma: float, params: SimulationParameters) -> float:
    """
    Calculate fitness for independent strategy using MLS framework.

    W_ind = (1 - beta_eff * sigma)(1 - m * P_base)

    Args:
        sigma: Environmental uncertainty
        params: Full parameter set

    Returns:
        Fitness value (always >= 0)
    """
    return independent_expected_fitness(
        sigma, params.network, params.conflict,
    )


def critical_threshold(epsilon: float, n: float,
                       params: SimulationParameters) -> float:
    """
    Calculate critical sigma* where aggregation becomes adaptive.

    Uses the MLS lambda-sigma feedback loop with Brent's method.

    Args:
        epsilon: Ecotone advantage
        n: Expected aggregation size
        params: Full parameter set

    Returns:
        Critical threshold sigma* in [0, 1].
    """
    result = mls_critical_threshold(
        epsilon=epsilon,
        n_agg=int(n),
        sig_params=params.signaling,
        net_params=params.network,
        conf_params=params.conflict,
        agg_params=params.aggregation,
    )
    return result['sigma_star']


# ── Convenience function ─────────────────────────────────────────────

def default_parameters(sigma: float = 0.5, epsilon: float = 0.35,
                       seed: int = 42) -> SimulationParameters:
    """Create parameter set with specified phase space position."""
    params = SimulationParameters(seed=seed)
    params.sigma = sigma
    params.epsilon = epsilon
    return params
