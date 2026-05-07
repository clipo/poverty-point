"""
Agent definitions for the Poverty Point ABM.

Agents:
- Band: Mobile hunter-gatherer group with quality-based signaling
- AggregationSite: Location where bands gather, with monument depreciation
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from enum import Enum
import numpy as np

from .parameters import SimulationParameters, W_aggregator, W_independent
from .signaling_core import (
    equilibrium_investment,
    exotic_signaling_cost,
    exotic_signal_value,
    monument_stock_step,
)


class Strategy(Enum):
    """Band strategy for aggregation."""
    AGGREGATOR = "aggregator"      # Participates in aggregation
    INDEPENDENT = "independent"    # Remains dispersed


# ── Archaeological exotic-goods sources ──────────────────────────────────
# Distances (km) from Poverty Point (Macon Ridge, Louisiana).
EXOTIC_SOURCES: Dict[str, float] = {
    'novaculite':    250.0,   # Ouachita Mountains, AR
    'crystal_quartz': 300.0,  # Arkansas
    'galena':        800.0,   # Missouri / Illinois
    'steatite':      900.0,   # Appalachian region
    'copper':       1600.0,   # Great Lakes
}


@dataclass
class Band:
    """
    A mobile hunter-gatherer band.

    Bands are the primary decision-making units. They choose whether
    to aggregate at the central site or remain independent. Investment
    in monuments follows the signaling equilibrium x*(q) from the MLS
    framework, where q is band productive capacity.
    """
    band_id: int
    size: int                               # Number of individuals
    home_location: Tuple[float, float]      # Base foraging location
    strategy: Strategy                       # Current strategy

    # Band quality (productive capacity for signaling)
    quality: float = 1.0                    # q in [q_min, q_max]

    # Network state
    network_degree_value: float = 0.3       # Current effective k
    seasonal_k: float = 0.3                 # After seasonal averaging

    # Cached equilibrium lambda for this band's decisions
    effective_lambda: float = 0.0

    # Resource state
    resources: float = 0.5                  # Current resource holdings (>= 0)

    # Signaling state
    prestige: float = 0.0                   # Accumulated prestige
    monument_contributions: float = 0.0     # Total monument investment
    exotic_goods: Dict[str, int] = field(default_factory=lambda: {
        k: 0 for k in EXOTIC_SOURCES
    })

    # Social network (band_id -> obligation strength)
    obligations: Dict[int, float] = field(default_factory=dict)

    # History tracking
    aggregation_history: List[bool] = field(default_factory=list)
    fitness_history: List[float] = field(default_factory=list)
    strategy_history: List[Strategy] = field(default_factory=list)

    @property
    def total_exotic_count(self) -> int:
        """Total number of exotic items across all material types."""
        return sum(self.exotic_goods.values())

    def update_quality(self, q_min: float = 0.2, q_max: float = 2.0) -> None:
        """Update band productive capacity based on current state.

        q = base_scale * size * (0.5 + resources) * (1 + 0.1 * k)

        Quality reflects the band's ability to mobilize labor for
        construction and procurement. It depends on band size,
        resource surplus, and network connections.
        """
        base_scale = 0.04
        raw_q = base_scale * self.size * (0.5 + self.resources) * (
            1.0 + 0.1 * self.seasonal_k
        )
        self.quality = float(np.clip(raw_q, q_min, q_max))

    def decide_strategy(self,
                        expected_n: float,
                        sigma: float,
                        epsilon: float,
                        params: SimulationParameters,
                        rng: np.random.Generator,
                        M_g: float = 0.0,
                        lam: float = -1.0) -> Strategy:
        """
        Decide whether to aggregate based on MLS fitness comparison.

        Uses soft-max decision rule with memory effects.
        """
        # Calculate expected fitness using MLS framework
        travel_dist = self.calculate_travel_distance(
            (params.environment.region_size / 2,
             params.environment.region_size / 2)
        )
        E_W_agg = W_aggregator(
            sigma, epsilon, expected_n, params,
            band_quality=self.quality,
            travel_distance=travel_dist,
            M_g=M_g, lam=lam,
        )
        E_W_ind = W_independent(sigma, params)

        # Base fitness difference
        fitness_diff = E_W_agg - E_W_ind

        # Memory effect: recent experience influences decision
        if len(self.fitness_history) >= 5:
            recent_fitness = np.mean(self.fitness_history[-5:])
            long_term_fitness = np.mean(self.fitness_history)

            if self.aggregation_history[-1]:
                if recent_fitness > long_term_fitness:
                    fitness_diff += 0.05
                else:
                    fitness_diff -= 0.05
            else:
                if recent_fitness > long_term_fitness:
                    fitness_diff -= 0.05
                else:
                    fitness_diff += 0.05

        # Probabilistic choice (sigmoid with temperature)
        temperature = 10.0
        p_aggregate = 1.0 / (1.0 + np.exp(-temperature * fitness_diff))

        if rng.random() < p_aggregate:
            return Strategy.AGGREGATOR
        else:
            return Strategy.INDEPENDENT

    def calculate_travel_distance(self,
                                  destination: Tuple[float, float]) -> float:
        """Euclidean distance to destination in km."""
        dx = destination[0] - self.home_location[0]
        dy = destination[1] - self.home_location[1]
        return float(np.sqrt(dx**2 + dy**2))

    def calculate_travel_cost(self,
                              destination: Tuple[float, float],
                              cost_per_km: float = 0.0005) -> float:
        """
        Calculate travel cost to a destination.

        Args:
            destination: (x, y) coordinates
            cost_per_km: Resource cost per km traveled

        Returns:
            Travel cost as fraction of resources
        """
        return self.calculate_travel_distance(destination) * cost_per_km

    def invest_in_monument(self,
                           lam: float,
                           q_min: float,
                           rng: np.random.Generator) -> float:
        """
        Invest in monument construction at signaling equilibrium level.

        Uses x*(q) = sqrt(lam * (q^2 - q_min^2)) with stochastic noise.

        Args:
            lam: Current total lambda
            q_min: Minimum population quality
            rng: Random number generator

        Returns:
            Amount invested
        """
        if self.resources < 0.3 or lam <= 0:
            return 0.0

        # Equilibrium investment from signaling game
        x_star = float(equilibrium_investment(self.quality, q_min, lam))

        # Stochastic variation (0.7 to 1.3 of equilibrium)
        noise = 0.7 + 0.6 * rng.random()
        investment = x_star * noise

        # Cannot invest more than available resources allow
        max_investment = self.resources * self.size * 0.5
        investment = min(investment, max_investment)

        # Update state
        self.monument_contributions += investment
        self.prestige += investment * 0.1

        return investment

    def acquire_exotic(self,
                       rng: np.random.Generator,
                       rho_exotic: float = 0.70) -> bool:
        """
        Attempt to acquire an exotic good using MLS signal cost/value.

        Probability weighted by signal value vs cost: more distant
        materials are costlier but carry higher signal value.
        """
        if self.resources < 0.2:
            return False

        acquired_any = False
        base_prob = 0.25 * (1 + self.prestige / (1 + self.prestige))

        for material, distance in EXOTIC_SOURCES.items():
            cost = exotic_signaling_cost(distance)
            value = exotic_signal_value(distance, rho_exotic)

            if self.resources < cost + 0.1:
                continue

            # Probability based on value/cost ratio with distance decay
            p = base_prob * np.exp(-distance / 500.0) * min(value / (cost + 0.01), 2.0)
            p = min(p, 0.5)

            if rng.random() < p:
                self.exotic_goods[material] += 1
                self.resources -= cost
                self.prestige += value * 0.2
                acquired_any = True
                break

        return acquired_any

    def apply_storage_decay(self, decay_rate: float = 0.05) -> None:
        """Apply storage decay on resources exceeding 1.0."""
        if self.resources > 1.0:
            excess = self.resources - 1.0
            self.resources = 1.0 + excess * (1.0 - decay_rate)

    def form_obligation(self,
                        partner_id: int,
                        strength: float = 0.1) -> None:
        """Form or strengthen reciprocal obligation with another band."""
        if partner_id in self.obligations:
            self.obligations[partner_id] += strength
        else:
            self.obligations[partner_id] = strength
        self.obligations[partner_id] = min(1.0, self.obligations[partner_id])

    def call_obligation(self,
                        partner_id: int,
                        need: float) -> float:
        """Call on an obligation for help during shortfall."""
        if partner_id not in self.obligations:
            return 0.0

        help_received = min(need, self.obligations[partner_id] * 0.5)
        self.obligations[partner_id] *= 0.7

        if self.obligations[partner_id] < 0.05:
            del self.obligations[partner_id]

        return help_received

    def reproduce(self,
                  fitness: float,
                  birth_rate: float,
                  death_rate: float,
                  rng: np.random.Generator) -> None:
        """Update population based on fitness."""
        effective_birth_rate = birth_rate * fitness * (0.5 + self.resources)
        births = rng.binomial(self.size, min(effective_birth_rate, 0.99))
        deaths = rng.binomial(self.size, death_rate)
        self.size = max(1, self.size + births - deaths)

    def suffer_shortfall(self,
                         vulnerability: float,
                         sigma: float,
                         rng: np.random.Generator) -> int:
        """
        Suffer mortality during environmental shortfall.

        Vulnerability is derived from network degree:
        alpha(k) = 1/(1 + gamma*k).
        """
        mortality_rate = 1.0 - np.exp(-vulnerability * sigma)
        deaths = rng.binomial(self.size, min(mortality_rate, 0.99))
        self.size = max(1, self.size - deaths)
        return deaths


@dataclass
class AggregationSite:
    """
    A location where bands aggregate seasonally.

    Tracks monument stock with depreciation: M_g(t+1) = (1-delta)*M_g(t) + I_g(t).
    """
    site_id: int
    name: str
    location: Tuple[float, float]
    ecotone_advantage: float          # epsilon for this location

    # Infrastructure (cumulative and depreciated)
    monument_level: float = 0.0       # Cumulative total investment
    effective_M_g: float = 0.0        # Depreciated monument stock (signal value)
    annual_investment_flow: float = 0.0  # I_g this year
    monument_history: List[float] = field(default_factory=lambda: [0.0])

    # Current aggregation state
    attending_bands: List[int] = field(default_factory=list)
    current_population: int = 0

    # Exotic goods
    total_exotics: int = 0
    exotic_sources: Dict[str, int] = field(default_factory=dict)

    def depreciate_monument(self, delta: float) -> None:
        """Apply annual monument depreciation and add new investment.

        M_g(t+1) = (1 - delta) * M_g(t) + I_g(t)
        """
        self.effective_M_g = monument_stock_step(
            self.effective_M_g, self.annual_investment_flow, delta
        )
        self.annual_investment_flow = 0.0

    def add_attending_band(self, band: Band) -> None:
        """Record a band attending this aggregation."""
        if band.band_id not in self.attending_bands:
            self.attending_bands.append(band.band_id)
            self.current_population += band.size
            self.total_exotics += band.total_exotic_count

    def record_construction(self, investment: float) -> None:
        """Record monument construction for this year."""
        self.monument_level += investment
        self.annual_investment_flow += investment
        self.monument_history.append(self.monument_level)

    def reset_annual_state(self) -> None:
        """Reset attendance for new year."""
        self.attending_bands = []
        self.current_population = 0

    @property
    def n_attending(self) -> int:
        """Number of bands currently attending."""
        return len(self.attending_bands)


def create_bands(n_bands: int,
                 initial_size: int,
                 region_size: float,
                 rng: np.random.Generator,
                 q_min: float = 0.2,
                 q_max: float = 2.0) -> List[Band]:
    """
    Create initial population of bands with quality distribution.

    Bands are distributed across the region with random initial strategies
    and quality values proportional to band size.
    """
    bands = []
    strategy_probs = [0.4, 0.6]  # [AGGREGATOR, INDEPENDENT]

    for i in range(n_bands):
        x = rng.uniform(0, region_size)
        y = rng.uniform(0, region_size)

        strategy = (Strategy.AGGREGATOR if rng.random() < strategy_probs[0]
                    else Strategy.INDEPENDENT)

        size = initial_size + rng.integers(-5, 6)
        resources = 0.4 + 0.2 * rng.random()

        # Initialize quality from band size and resources
        base_scale = 0.04
        quality = base_scale * size * (0.5 + resources)
        quality = float(np.clip(quality, q_min, q_max))

        band = Band(
            band_id=i,
            size=size,
            home_location=(x, y),
            strategy=strategy,
            quality=quality,
            resources=resources,
        )
        bands.append(band)

    return bands


def create_aggregation_site(location: Tuple[float, float],
                            epsilon: float,
                            name: str = "Poverty Point") -> AggregationSite:
    """Create the main aggregation site."""
    return AggregationSite(
        site_id=0,
        name=name,
        location=location,
        ecotone_advantage=epsilon
    )
