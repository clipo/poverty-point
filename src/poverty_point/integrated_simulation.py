"""
Integrated Simulation for Poverty Point ABM.

This module connects:
- environment.py: Multi-zone ecology with seasonal cycles
- core_simulation.py: Theoretical framework and agent decisions
- parameters.py: Calibrated parameter values
- agents.py: Band and AggregationSite agents

The result is a simulation where environmental conditions drive
aggregation decisions through actual productivity variations rather
than abstract σ parameters.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum

from .environment import Environment, EnvironmentConfig, ResourceZone
from .parameters import (
    SimulationParameters, default_parameters,
    W_aggregator, W_independent,
    calculate_sigma_from_shortfall,
)
from .signaling_core import (
    vulnerability_coefficient,
    compute_lambda_C,
    compute_lambda_X,
    seasonal_effective_degree,
)
from .agents import Band, AggregationSite, Strategy
from .environmental_scenarios import ShortfallParams


@dataclass
class IntegratedState:
    """State snapshot for integrated simulation."""
    year: int
    month: int

    # Population
    total_population: int
    n_bands: int
    mean_band_size: float

    # Strategy
    n_aggregators: int
    n_independents: int
    strategy_dominance: float

    # Aggregation
    aggregation_size: int
    aggregation_population: int

    # Investment
    monument_level: float
    annual_construction: float
    total_exotics: int

    # Environment (from actual model)
    mean_productivity: float
    productivity_by_zone: Dict[str, float]
    effective_sigma: float  # Derived from productivity variance
    ecotone_value: float    # Value at aggregation site

    # Shortfall
    in_shortfall: bool
    shortfall_severity: float

    # Fitness
    mean_fitness_aggregators: float
    mean_fitness_independents: float

    # Obligation network (Phase 2 additions)
    mean_obligations_per_aggregator: float = 0.0
    mean_obligations_per_independent: float = 0.0
    mean_obligation_strength: float = 0.0
    network_edge_count: int = 0
    exotic_counts_by_material: Dict[str, int] = field(default_factory=dict)


@dataclass
class IntegratedResults:
    """Complete results from integrated simulation."""
    # Parameters
    seed: int
    duration_years: int

    # Time series
    yearly_states: List[IntegratedState] = field(default_factory=list)
    monthly_states: List[IntegratedState] = field(default_factory=list)

    # Summary (post-burn-in)
    final_strategy_dominance: float = 0.0
    mean_aggregation_size: float = 0.0
    final_monument_level: float = 0.0
    total_exotics: int = 0
    mean_population: float = 0.0
    mean_effective_sigma: float = 0.0

    def compute_summary(self, burn_in: int = 100) -> None:
        """Compute summary statistics from time series."""
        analysis_states = [s for s in self.yearly_states if s.year >= burn_in]

        if not analysis_states:
            return

        self.final_strategy_dominance = np.mean([
            s.strategy_dominance for s in analysis_states
        ])
        self.mean_aggregation_size = np.mean([
            s.aggregation_size for s in analysis_states
        ])
        self.final_monument_level = analysis_states[-1].monument_level
        self.total_exotics = analysis_states[-1].total_exotics
        self.mean_population = np.mean([
            s.total_population for s in analysis_states
        ])
        self.mean_effective_sigma = np.mean([
            s.effective_sigma for s in analysis_states
        ])


class Season(Enum):
    """Season within annual cycle."""
    WINTER = "winter"       # Months 12, 1, 2 - Low activity
    SPRING = "spring"       # Months 3, 4, 5 - Resource flush
    SUMMER = "summer"       # Months 6, 7, 8 - Peak aggregation
    FALL = "fall"           # Months 9, 10, 11 - Dispersal, mast harvest


def month_to_season(month: int) -> Season:
    """Convert month to season."""
    if month in [12, 1, 2]:
        return Season.WINTER
    elif month in [3, 4, 5]:
        return Season.SPRING
    elif month in [6, 7, 8]:
        return Season.SUMMER
    else:
        return Season.FALL


class IntegratedSimulation:
    """
    Integrated simulation connecting environment and agent dynamics.

    Annual Cycle:
    1. January: New year begins, annual shocks generated
    2. Spring (Mar-May): Dispersal season, bands forage
    3. Summer (Jun-Aug): Aggregation season at Poverty Point
    4. Fall (Sep-Nov): Dispersal, mast harvest, strategy evaluation
    5. Winter (Dec-Feb): Low activity, mortality, reproduction

    Environmental σ is derived from actual productivity variance rather
    than being an input parameter.
    """

    def __init__(self,
                 params: Optional[SimulationParameters] = None,
                 env_config: Optional[EnvironmentConfig] = None,
                 shortfall_params: Optional[ShortfallParams] = None,
                 seed: int = 42,
                 signal_conditional_partners: bool = False,
                 memory_effect: bool = True):
        """
        Initialize integrated simulation.

        Args:
            params: Simulation parameters (uses defaults if None)
            env_config: Environment configuration (uses defaults if None)
            shortfall_params: Shortfall generation parameters (uses defaults if None)
            seed: Random seed
            signal_conditional_partners: If True, partner formation depends on
                each band's monument and exotic display. If False (default,
                preserves prior behavior), partner formation is signal-blind
                with a uniform 30% probability per band per aggregation.
        """
        self.params = params or default_parameters(seed=seed)
        self.params.seed = seed
        self.signal_conditional_partners = signal_conditional_partners
        self.memory_effect = memory_effect

        # Shortfall parameters
        self.shortfall_params = shortfall_params or ShortfallParams()

        # Override environment config if provided
        if env_config:
            self.env_config = env_config
        else:
            self.env_config = EnvironmentConfig(
                region_size=self.params.environment.region_size,
                n_aquatic_patches=self.params.environment.n_aquatic_patches,
                n_terrestrial_patches=self.params.environment.n_terrestrial_patches,
                n_mast_patches=self.params.environment.n_mast_patches,
                n_ecotone_patches=self.params.environment.n_wetland_patches,
            )

        self.rng = np.random.default_rng(seed)

        # Initialize environment
        self.environment = Environment(self.env_config, seed=seed)

        # Initialize bands (from agents.py pattern)
        self.bands = self._create_bands()
        self.band_by_id: Dict[int, Band] = {b.band_id: b for b in self.bands}
        self.next_band_id = len(self.bands)

        # Random initial obligation-network seeding: each band starts with
        # 0-2 weak reciprocal ties to randomly chosen partners.
        self._seed_initial_obligations()

        # Initialize aggregation site at ecotone location
        self.aggregation_site = self._create_aggregation_site()

        # State tracking
        self.year = 0
        self.month = 1
        self.annual_productivities: List[float] = []
        self.effective_sigma = 0.0

        # Population state sensed by next year's strategy decisions:
        # previous year's realized attendance, and the monument signal
        # stock / lambda the bands observed at the gathering.
        self.prev_n_attending = max(
            5, int(round(0.5 * self.params.population.n_bands))
        )
        self._sensed_M_g = 0.0
        self._sensed_lam = self.params.signaling.lambda_W

        # Shortfall tracking
        self.in_shortfall = False
        self.shortfall_severity = 0.0
        self.shortfall_remaining = 0  # Years remaining in current shortfall

        # Results
        self.results = IntegratedResults(
            seed=seed,
            duration_years=self.params.duration
        )

    def _create_bands(self) -> List[Band]:
        """Create initial band population distributed across region."""
        bands = []
        n_bands = self.params.population.n_bands
        region_size = self.env_config.region_size

        q_min = self.params.signaling.q_min
        q_max = self.params.signaling.q_max

        for i in range(n_bands):
            x = self.rng.uniform(0, region_size)
            y = self.rng.uniform(0, region_size)

            # Initial strategy: Bernoulli(0.5) aggregator/independent
            strategy = (Strategy.AGGREGATOR if self.rng.random() < 0.5
                       else Strategy.INDEPENDENT)

            band = Band(
                band_id=i,
                size=int(self.params.population.initial_band_size
                         + self.rng.integers(-5, 6)),
                home_location=(x, y),
                strategy=strategy,
                # Band productive quality drawn from U[q_min, q_max]
                # (heterogeneous signaling capacity across bands).
                quality=float(self.rng.uniform(q_min, q_max)),
                resources=0.4 + 0.2 * self.rng.random()
            )
            bands.append(band)

        return bands

    def _seed_initial_obligations(self) -> None:
        """Seed each band with 0-2 weak reciprocal obligations."""
        band_ids = [b.band_id for b in self.bands]
        for band in self.bands:
            n_ties = int(self.rng.integers(0, 3))
            if n_ties == 0 or len(band_ids) < 2:
                continue
            partners = self.rng.choice(
                [i for i in band_ids if i != band.band_id],
                size=min(n_ties, len(band_ids) - 1),
                replace=False,
            )
            for partner_id in np.atleast_1d(partners):
                partner_id = int(partner_id)
                band.form_obligation(partner_id, strength=0.1)
                self.band_by_id[partner_id].form_obligation(
                    band.band_id, strength=0.1
                )

    def _create_aggregation_site(self) -> AggregationSite:
        """Create aggregation site at optimal ecotone location."""
        # Find best location using environment model
        best_loc, best_val = self.environment.find_optimal_aggregation_site(
            n_candidates=200,
            access_radius=self.env_config.region_size * 0.1
        )

        # Calculate ecotone advantage (ε) from location value
        # Normalize to [0, 1] based on expected range
        ecotone_advantage = min(1.0, best_val / 3.0)

        return AggregationSite(
            site_id=0,
            name="Poverty Point",
            location=best_loc,
            ecotone_advantage=ecotone_advantage
        )

    def _calculate_effective_sigma(self) -> float:
        """
        Calculate effective environmental uncertainty (sigma).

        Uses the canonical formula from parameters.py:
            sigma = magnitude * sqrt(20 / frequency)

        Calibrated values:
        - Poverty Point (interval=10, magnitude=0.45) -> sigma ~ 0.636
        - High uncertainty (interval=6, magnitude=0.60) -> sigma ~ 0.95 (clipped)
        - Low uncertainty (interval=18, magnitude=0.30) -> sigma ~ 0.316
        """
        magnitude = self.shortfall_params.magnitude_mean
        frequency = self.shortfall_params.mean_interval

        base_sigma = calculate_sigma_from_shortfall(frequency, magnitude)

        # Small adjustment from realized environmental variance
        if len(self.annual_productivities) >= 5:
            recent_prods = self.annual_productivities[-10:]
            mean_prod = np.mean(recent_prods)
            if mean_prod > 0:
                cv = np.std(recent_prods) / mean_prod
                sigma = base_sigma + 0.2 * (cv - 0.15)
            else:
                sigma = base_sigma
        else:
            sigma = base_sigma

        return float(np.clip(sigma, 0.05, 0.95))

    def _evaluate_shortfall(self) -> Tuple[bool, float]:
        """
        Evaluate if current year is a shortfall.

        Uses shortfall_params to determine frequency and magnitude.
        Also considers actual environmental productivity.

        Returns:
            (is_shortfall, severity)
        """
        # Get mean productivity across all zones
        mean_prod = 0.0
        n_zones = 0
        for zone in ResourceZone:
            zone_prod = self.environment.get_zone_productivity(zone)
            if zone_prod > 0:
                mean_prod += zone_prod
                n_zones += 1

        if n_zones > 0:
            mean_prod /= n_zones

        # Record for sigma calculation
        self.annual_productivities.append(float(mean_prod))

        # Check for continuing shortfall
        if self.shortfall_remaining > 0:
            self.shortfall_remaining -= 1
            return True, self.shortfall_severity

        # Determine if new shortfall starts (stochastic)
        # Probability = 1 / mean_interval
        p_shortfall = 1.0 / self.shortfall_params.mean_interval

        if self.rng.random() < p_shortfall:
            # Generate shortfall magnitude
            magnitude = self.shortfall_params.magnitude_mean + \
                       self.rng.normal(0, self.shortfall_params.magnitude_std)
            magnitude = float(np.clip(magnitude, 0.1, 0.9))

            # Duration scales with magnitude
            duration = max(1, int(1 + magnitude * self.shortfall_params.duration_scale))
            self.shortfall_remaining = duration - 1  # This year counts

            return True, magnitude

        return False, 0.0

    def _run_spring_dispersal(self) -> None:
        """
        Spring dispersal: Bands forage independently.
        Resource acquisition based on actual zone productivity.
        """
        for band in self.bands:
            # Get productivity near band's home location
            location_value = self.environment.get_location_value(
                band.home_location,
                access_radius=50.0
            )
            base_harvest = location_value['total'] * 0.3 * self._harvest_factor()

            # Aggregators prepare for travel (reduced foraging)
            if band.strategy == Strategy.AGGREGATOR:
                harvest = base_harvest * (1 - self.params.aggregation.C_opportunity)
            else:
                harvest = base_harvest

            # Update resources
            consumption = band.size * 0.015
            band.resources += harvest - consumption
            band.resources = max(0.0, band.resources)

    # Scale converting (vulnerability x shortfall severity) into per-event
    # mortality. At the PP-scenario severity (m ~ 0.45-0.5) an unbuffered
    # band (alpha ~ 0.985) loses ~9-10% of members per shortfall year;
    # a well-networked aggregator loses proportionally less via alpha(k).
    SHORTFALL_MORTALITY_SCALE = 0.2

    def _harvest_factor(self) -> float:
        """Shortfall propagation into realized productivity.

        In a shortfall year every harvest draw is reduced by the shortfall
        severity, so shortfalls flow through zone productivity into band
        resources rather than acting on mortality alone. Harvests are also
        density-dependent: regional productivity is finite, so the per-band
        share scales inversely with the number of bands drawing on the
        region (normalized to the initial band count).
        """
        shortfall = 1.0 - self.shortfall_severity if self.in_shortfall else 1.0
        density = self.params.population.n_bands / max(1, len(self.bands))
        return shortfall * min(density, 2.0)

    def _run_summer_aggregation(self) -> None:
        """
        Summer aggregation season: bands gather at Poverty Point.

        Runs once per simulated year. Strategy decisions are synchronous:
        every band evaluates the same start-of-year population state
        (previous year's realized attendance, the site's depreciated
        monument signal stock, and the lambda implied by that stock)
        before any band acts. Partner formation runs as a second pass
        over the full attending cohort.
        """
        # Reset aggregation site
        self.aggregation_site.reset_annual_state()

        # Population state sensed by all bands this year.
        expected_n = max(5, self.prev_n_attending)
        M_g_sensed = self.aggregation_site.effective_M_g
        lam_sensed = (
            self.params.signaling.lambda_W
            + compute_lambda_C(M_g_sensed, self.params.conflict)
            + compute_lambda_X(M_g_sensed, self.effective_sigma,
                               self.params.network)
        )
        self._sensed_M_g = M_g_sensed
        self._sensed_lam = lam_sensed

        # Get actual ecotone value at aggregation site
        site_value = self.environment.get_location_value(
            self.aggregation_site.location,
            access_radius=80.0  # Larger radius during aggregation
        )

        total_construction = 0.0
        harvest_factor = self._harvest_factor()

        # Pass 1: synchronous strategy decisions and individual actions.
        for band in self.bands:
            band.strategy = band.decide_strategy(
                expected_n=expected_n,
                sigma=self.effective_sigma,
                epsilon=self.aggregation_site.ecotone_advantage,
                params=self.params,
                rng=self.rng,
                M_g=M_g_sensed,
                lam=lam_sensed,
                site_location=self.aggregation_site.location,
                memory_effect=self.memory_effect,
            )
            band.strategy_history.append(band.strategy)

            if band.strategy == Strategy.AGGREGATOR:
                # Travel to aggregation site (documented cost coefficient,
                # capped at 30% of current resources)
                travel_cost = band.calculate_travel_cost(
                    self.aggregation_site.location,
                    cost_per_km=self.params.aggregation.C_travel_per_km,
                )
                band.resources -= min(travel_cost, band.resources * 0.3)

                # Register attendance
                self.aggregation_site.add_attending_band(band)
                band.aggregation_history.append(True)

                # Benefit from ecotone resources during aggregation
                aggregation_harvest = site_value['total'] * 0.2 * harvest_factor
                band.resources += aggregation_harvest

                # Monument investment at the signaling equilibrium x*(q),
                # under the lambda every band sensed at the start of the
                # gathering (synchronous within the phase).
                if band.resources > 0.3:
                    investment = band.invest_in_monument(
                        lam=lam_sensed,
                        q_min=self.params.signaling.q_min,
                        rng=self.rng,
                    )
                    total_construction += investment

                # Exotic acquisition (at most one material per year)
                band.acquire_exotic(rng=self.rng)
            else:
                # Independent: continue foraging at home
                band.aggregation_history.append(False)
                location_value = self.environment.get_location_value(
                    band.home_location, access_radius=50.0
                )
                harvest = location_value['total'] * 0.25 * harvest_factor
                band.resources += harvest

        # Pass 2: partner formation over the full attending cohort.
        self._form_obligations()

        # Record construction, update each band's realized network state,
        # and remember attendance for next year's decisions.
        self.aggregation_site.record_construction(total_construction)
        self._update_network_state()
        self.prev_n_attending = self.aggregation_site.n_attending

    def _form_obligations(self) -> None:
        """Partner formation among attending bands (one pass per year).

        Signal-conditional mode: tie probability 0.20 + 0.20 * own
        normalized display (display = monument contributions plus
        exotic-goods count, normalized within the attending cohort);
        partner choice weighted 0.5 + partner's normalized display.

        Signal-blind mode (random-partner ablation): the same expected
        number of ties forms (uniform probability equal to the cohort
        mean of the conditional probabilities), but who pairs with whom
        is uniform random.

        Obligations are reciprocal: both bands record the tie.
        """
        attending = self.aggregation_site.attending_bands
        if len(attending) <= 1:
            return

        displays = {}
        for b_id in attending:
            b = self.band_by_id[b_id]
            displays[b_id] = (
                b.monument_contributions + float(b.total_exotic_count)
            )
        d_max = max(displays.values())
        if d_max > 0:
            norm_display = {k: v / d_max for k, v in displays.items()}
        else:
            norm_display = {k: 0.0 for k in displays}

        mean_display = float(np.mean(list(norm_display.values())))
        blind_prob = 0.20 + 0.20 * mean_display

        for b_id in attending:
            band = self.band_by_id[b_id]
            potential_partners = [p for p in attending if p != b_id]
            if not potential_partners:
                continue

            if self.signal_conditional_partners:
                tie_prob = 0.20 + 0.20 * norm_display[b_id]
                if self.rng.random() < tie_prob:
                    # Partner choice weighted by display level. Floor at
                    # 0.5 so low-display bands still get picked; weight up
                    # to 1.5x for max-display partners.
                    weights = np.array([
                        0.5 + norm_display[p_id]
                        for p_id in potential_partners
                    ], dtype=float)
                    weights /= weights.sum()
                    partner_id = int(self.rng.choice(
                        potential_partners, p=weights
                    ))
                    band.form_obligation(partner_id)
                    self.band_by_id[partner_id].form_obligation(b_id)
            else:
                # Signal-blind: equal expected tie count, random pairing.
                if self.rng.random() < blind_prob:
                    partner_id = int(self.rng.choice(potential_partners))
                    band.form_obligation(partner_id)
                    self.band_by_id[partner_id].form_obligation(b_id)

    def _update_network_state(self) -> None:
        """Update each band's realized network degree after aggregation.

        A band's within-aggregation degree is k_0 plus the summed strength
        of its obligations, capped at k_0 + k_max (the saturating ceiling
        of the network-growth function). Aggregators carry the seasonal
        average k_eff into winter vulnerability; independents fall back to
        the baseline kin degree k_0.
        """
        k_0 = self.params.network.k_0
        k_cap = k_0 + self.params.network.k_max
        for band in self.bands:
            k_band = min(k_0 + sum(band.obligations.values()), k_cap)
            band.network_degree_value = k_band
            if band.strategy == Strategy.AGGREGATOR:
                band.seasonal_k = seasonal_effective_degree(
                    k_band, k_0,
                    self.params.aggregation.delta_net,
                    self.params.aggregation.f_agg,
                )
            else:
                band.seasonal_k = k_0

    def _run_fall_dispersal(self) -> None:
        """
        Fall dispersal: Mast harvest, final foraging before winter.
        """
        for band in self.bands:
            # Mast zone productivity peaks in fall
            location_value = self.environment.get_location_value(
                band.home_location,
                access_radius=60.0
            )

            # Extra benefit if mast is accessible
            mast_bonus = location_value.get('mast', 0.0) * 0.5
            harvest = (location_value['total'] * 0.2 + mast_bonus) \
                * self._harvest_factor()

            # Consumption and storage for winter
            consumption = band.size * 0.012
            band.resources += harvest - consumption
            band.resources = max(0.0, band.resources)

    def _run_winter_mortality(self) -> None:
        """
        Winter: Mortality and reproduction based on fitness.
        """
        for band in self.bands:
            # Calculate realized fitness
            if band.aggregation_history and band.aggregation_history[-1]:
                # Network-density coupling to epsilon under signal-conditional
                # mode: an aggregator's effective ecotone parameter is
                # augmented by the fraction of potential obligation ties
                # that have been realized. This implements the framework's
                # prediction that a dense, signal-conditional obligation
                # network at the gathering site reduces sigma_eff for
                # aggregators there beyond ecotone access alone.
                #
                #   epsilon_eff = epsilon + (1 - epsilon) * beta * rho
                #
                # where rho = obligation_count / (n_attending - 1) is the
                # band's realized network density and beta = 0.5 is the
                # coupling strength between network density and the local
                # buffer. Capped at 0.95 to prevent sigma_eff -> 0.
                eps = self.aggregation_site.ecotone_advantage
                if self.signal_conditional_partners:
                    n_attending = max(2, self.aggregation_site.n_attending)
                    rho = len(band.obligations) / float(n_attending - 1)
                    rho = min(1.0, rho)
                    beta_net = 0.5
                    eps = eps + (1.0 - eps) * beta_net * rho
                    eps = min(0.95, eps)
                fitness = W_aggregator(
                    self.effective_sigma,
                    eps,
                    self.aggregation_site.n_attending,
                    self.params,
                    band_quality=band.quality,
                    travel_distance=band.calculate_travel_distance(
                        self.aggregation_site.location
                    ),
                    M_g=self._sensed_M_g,
                    lam=self._sensed_lam,
                )
            else:
                fitness = W_independent(self.effective_sigma, self.params)

            band.fitness_history.append(fitness)

            # Shortfall mortality (vulnerability derived from network degree)
            if self.in_shortfall:
                gamma = self.params.network.gamma
                if band.strategy == Strategy.AGGREGATOR:
                    vuln = vulnerability_coefficient(band.seasonal_k, gamma)
                    # Aggregators can call obligations during shortfall.
                    if band.obligations:
                        if self.signal_conditional_partners:
                            # Tie-strength-weighted help: call obligations in
                            # order of strength (strongest first) until need
                            # is met or obligations exhausted. This closes
                            # the loop with signal-conditional partner
                            # formation: bands that signaled hard, attracted
                            # strong ties, and so receive more reliable help
                            # during shortfalls. The same total need (0.15)
                            # is preserved so blind/conditional modes have
                            # comparable resource budgets.
                            partners_sorted = sorted(
                                band.obligations.items(),
                                key=lambda x: x[1],
                                reverse=True,
                            )
                            remaining = 0.15
                            for partner_id, _strength in partners_sorted:
                                if remaining <= 0.001:
                                    break
                                partner = self.band_by_id.get(partner_id)
                                if partner is None:
                                    # Partner band dissolved; prune the tie.
                                    band.obligations.pop(partner_id, None)
                                    continue
                                # Help is a transfer: bounded by what the
                                # partner can spare (floor 0.05).
                                available = max(0.0, partner.resources - 0.05)
                                if available <= 0.0:
                                    continue
                                help_received = band.call_obligation(
                                    partner_id,
                                    need=min(remaining, available),
                                )
                                partner.resources -= help_received
                                band.resources += help_received
                                remaining -= help_received
                        else:
                            # Signal-blind (prior behavior): one random call.
                            partner_id = int(self.rng.choice(
                                list(band.obligations.keys())
                            ))
                            partner = self.band_by_id.get(partner_id)
                            if partner is None:
                                band.obligations.pop(partner_id, None)
                            else:
                                available = max(0.0, partner.resources - 0.05)
                                help_received = band.call_obligation(
                                    partner_id, need=min(0.15, available),
                                )
                                partner.resources -= help_received
                                band.resources += help_received
                else:
                    vuln = vulnerability_coefficient(self.params.network.k_0, gamma)

                # Mortality is driven by the realized event severity, not
                # the composite sigma index, at the documented scale.
                band.suffer_shortfall(
                    vuln * self.SHORTFALL_MORTALITY_SCALE,
                    self.shortfall_severity,
                    self.rng
                )

            # Reproduction
            band.reproduce(
                fitness=fitness,
                birth_rate=self.params.population.birth_rate,
                death_rate=self.params.population.death_rate,
                rng=self.rng
            )

            # Storage decay on excess resources
            band.apply_storage_decay()

        # Band-size demography (dissolution / fission) is applied once per
        # year in step_year after the winter phase.

    def _apply_fission_and_dissolution(self) -> None:
        """Apply once-per-year band demography.

        Bands below min_band_size dissolve (are removed from the
        population). Bands above max_band_size fission deterministically:
        a daughter band splits off with half the members and resources,
        inheriting the parent's monument-contribution history and
        obligation network at half weight (Band.fission).
        """
        min_size = self.params.population.min_band_size
        max_size = self.params.population.max_band_size

        survivors: List[Band] = []
        daughters: List[Band] = []
        for band in self.bands:
            if band.size < min_size:
                continue  # band dissolves
            if band.size > max_size:
                daughter = band.fission(
                    self.next_band_id, self.rng,
                    q_min=self.params.signaling.q_min,
                    q_max=self.params.signaling.q_max,
                )
                self.next_band_id += 1
                daughters.append(daughter)
            survivors.append(band)

        if not survivors and not daughters:
            # Guard against total dissolution: keep the largest band so
            # downstream statistics remain defined.
            survivors = [max(self.bands, key=lambda b: b.size)]

        self.bands = survivors + daughters
        self.band_by_id = {b.band_id: b for b in self.bands}

    def _record_state(self, annual: bool = False) -> IntegratedState:
        """Record current simulation state."""
        # Count strategies
        n_agg = sum(1 for b in self.bands if b.strategy == Strategy.AGGREGATOR)
        n_ind = len(self.bands) - n_agg
        n_total = len(self.bands)

        dominance = (n_agg - n_ind) / n_total if n_total > 0 else 0.0

        # Productivity by zone
        prod_by_zone = {}
        for zone in ResourceZone:
            prod_by_zone[zone.value] = self.environment.get_zone_productivity(zone)

        # Fitness by strategy
        agg_fitness = [b.fitness_history[-1] for b in self.bands
                       if b.strategy == Strategy.AGGREGATOR and b.fitness_history]
        ind_fitness = [b.fitness_history[-1] for b in self.bands
                       if b.strategy == Strategy.INDEPENDENT and b.fitness_history]

        # Ecotone value
        site_value = self.environment.get_location_value(
            self.aggregation_site.location,
            access_radius=50.0
        )

        # Obligation network metrics
        agg_bands = [b for b in self.bands if b.strategy == Strategy.AGGREGATOR]
        ind_bands = [b for b in self.bands if b.strategy == Strategy.INDEPENDENT]

        agg_obligations = [len(b.obligations) for b in agg_bands] if agg_bands else [0]
        ind_obligations = [len(b.obligations) for b in ind_bands] if ind_bands else [0]

        all_strengths = []
        total_edges = 0
        for b in self.bands:
            total_edges += len(b.obligations)
            all_strengths.extend(b.obligations.values())

        # Exotic counts by material
        exotic_totals: Dict[str, int] = {}
        for b in self.bands:
            for material, count in b.exotic_goods.items():
                exotic_totals[material] = exotic_totals.get(material, 0) + count

        state = IntegratedState(
            year=self.year,
            month=self.month,
            total_population=sum(b.size for b in self.bands),
            n_bands=len(self.bands),
            mean_band_size=np.mean([b.size for b in self.bands]),
            n_aggregators=n_agg,
            n_independents=n_ind,
            strategy_dominance=dominance,
            aggregation_size=self.aggregation_site.n_attending,
            aggregation_population=self.aggregation_site.current_population,
            monument_level=self.aggregation_site.monument_level,
            annual_construction=(
                self.aggregation_site.monument_history[-1] -
                self.aggregation_site.monument_history[-2]
                if len(self.aggregation_site.monument_history) > 1
                else self.aggregation_site.monument_level
            ),
            total_exotics=sum(b.total_exotic_count for b in self.bands),
            mean_productivity=np.mean(list(prod_by_zone.values())),
            productivity_by_zone=prod_by_zone,
            effective_sigma=self.effective_sigma,
            ecotone_value=site_value['total'],
            in_shortfall=self.in_shortfall,
            shortfall_severity=self.shortfall_severity,
            mean_fitness_aggregators=np.mean(agg_fitness) if agg_fitness else 0.0,
            mean_fitness_independents=np.mean(ind_fitness) if ind_fitness else 0.0,
            mean_obligations_per_aggregator=float(np.mean(agg_obligations)),
            mean_obligations_per_independent=float(np.mean(ind_obligations)),
            mean_obligation_strength=float(np.mean(all_strengths)) if all_strengths else 0.0,
            network_edge_count=total_edges,
            exotic_counts_by_material=exotic_totals,
        )

        if annual:
            self.results.yearly_states.append(state)
        else:
            self.results.monthly_states.append(state)

        return state

    def step_year(self) -> IntegratedState:
        """Execute one full year of simulation."""
        # Advance environment to new year
        self.environment.advance_year()

        # Evaluate shortfall from environment
        self.in_shortfall, self.shortfall_severity = self._evaluate_shortfall()

        # Update effective sigma from productivity history
        self.effective_sigma = self._calculate_effective_sigma()

        # Run seasonal cycle: the time step is one year, partitioned into
        # a four-phase annual cycle. Each seasonal handler executes exactly
        # once per year, with the environment set to a representative month
        # for that season.
        for month, handler in ((4, self._run_spring_dispersal),
                               (7, self._run_summer_aggregation),
                               (10, self._run_fall_dispersal),
                               (1, self._run_winter_mortality)):
            self.month = month
            self.environment.month = month
            handler()

        # Monument signal-stock depreciation, once per year:
        # M_g(t+1) = (1 - delta) * M_g(t) + I_g(t). The cumulative
        # monument_level (physical fill) is unaffected; only the signal
        # value depreciates.
        self.aggregation_site.depreciate_monument(self.params.signaling.delta)

        # Band demography: dissolution below the minimum viable size,
        # deterministic fission above the maximum size (daughter bands
        # inherit history and network at half weight).
        self._apply_fission_and_dissolution()

        # Record annual state
        state = self._record_state(annual=True)

        self.year += 1
        return state

    def run(self, verbose: bool = False) -> IntegratedResults:
        """
        Run complete integrated simulation.

        Args:
            verbose: Print progress updates

        Returns:
            IntegratedResults object
        """
        if verbose:
            print(f"Running integrated simulation: {self.params.duration} years")
            print(f"  Aggregation site: {self.aggregation_site.name}")
            print(f"  Location: ({self.aggregation_site.location[0]:.1f}, "
                  f"{self.aggregation_site.location[1]:.1f})")
            print(f"  Ecotone advantage: {self.aggregation_site.ecotone_advantage:.3f}")

        for _ in range(self.params.duration):
            self.step_year()

            if verbose and self.year % 100 == 0:
                state = self.results.yearly_states[-1]
                print(f"  Year {self.year}: Pop={state.total_population}, "
                      f"Dom={state.strategy_dominance:.2f}, "
                      f"σ_eff={state.effective_sigma:.3f}, "
                      f"Monument={state.monument_level:.0f}")

        # Compute summary
        self.results.compute_summary(burn_in=self.params.burn_in)

        if verbose:
            print(f"\nSimulation complete.")
            print(f"  Final dominance: {self.results.final_strategy_dominance:.3f}")
            print(f"  Mean σ_eff: {self.results.mean_effective_sigma:.3f}")
            print(f"  Monument level: {self.results.final_monument_level:.0f}")
            print(f"  Total exotics: {self.results.total_exotics}")

        return self.results


def run_integrated_simulation(duration: int = 600,
                              seed: int = 42,
                              verbose: bool = False) -> IntegratedResults:
    """
    Convenience function to run integrated simulation.

    Args:
        duration: Simulation duration in years
        seed: Random seed
        verbose: Print progress

    Returns:
        IntegratedResults object
    """
    params = default_parameters(seed=seed)
    params.duration = duration

    sim = IntegratedSimulation(params=params, seed=seed)
    return sim.run(verbose=verbose)


if __name__ == "__main__":
    # Test integrated simulation
    results = run_integrated_simulation(
        duration=300,
        seed=42,
        verbose=True
    )

    print(f"\n--- Final Results ---")
    print(f"Strategy dominance: {results.final_strategy_dominance:.3f}")
    print(f"Mean aggregation: {results.mean_aggregation_size:.1f} bands")
    print(f"Monument level: {results.final_monument_level:.0f}")
    print(f"Total exotics: {results.total_exotics}")
    print(f"Mean effective σ: {results.mean_effective_sigma:.3f}")
