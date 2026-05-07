"""
Core simulation for Poverty Point aggregation model.

Uses the multilevel signaling framework (signaling_core.py) for fitness
calculations, network dynamics, and monument depreciation.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

from .parameters import (
    SimulationParameters, default_parameters,
    W_aggregator, W_independent, critical_threshold
)
from .agents import Band, AggregationSite, Strategy, create_bands, create_aggregation_site
from .signaling_core import (
    lambda_total_at_sigma,
    vulnerability_coefficient,
    network_degree,
    seasonal_effective_degree,
)


@dataclass
class YearlyState:
    """State snapshot for a single year."""
    year: int

    # Population
    total_population: int
    n_bands: int
    mean_band_size: float

    # Strategy distribution
    n_aggregators: int
    n_independents: int
    strategy_dominance: float  # (n_agg - n_ind) / n_total, in [-1, 1]

    # Aggregation
    aggregation_size: int      # Bands at aggregation
    aggregation_population: int  # Individuals at aggregation

    # Investment
    monument_level: float      # Cumulative
    effective_M_g: float       # Depreciated signal value
    annual_construction: float # This year
    total_exotics: int

    # Environment
    sigma_effective: float
    in_shortfall: bool
    shortfall_magnitude: float

    # MLS framework state
    lambda_total: float        # Equilibrium lambda
    B_lambda: float            # Signaling benefit
    alpha_eff: float           # Derived aggregator vulnerability
    beta_eff: float            # Derived independent vulnerability
    conflict_reduction_r: float  # Derived r
    mean_network_degree_agg: float
    mean_network_degree_ind: float

    # Fitness
    mean_fitness_aggregators: float
    mean_fitness_independents: float


@dataclass
class SimulationResults:
    """Complete results from a simulation run."""
    sigma: float
    epsilon: float
    seed: int

    yearly_states: List[YearlyState] = field(default_factory=list)

    # Summary statistics (computed after simulation)
    final_strategy_dominance: float = 0.0
    mean_aggregation_size: float = 0.0
    final_monument_level: float = 0.0
    total_exotics: int = 0
    mean_population: float = 0.0

    # Theoretical comparison
    sigma_star_theoretical: float = 0.0

    def compute_summary(self, burn_in: int = 100) -> None:
        """Compute summary statistics from time series."""
        analysis_states = [s for s in self.yearly_states if s.year >= burn_in]

        if not analysis_states:
            return

        self.final_strategy_dominance = float(np.mean(
            [s.strategy_dominance for s in analysis_states]
        ))
        self.mean_aggregation_size = float(np.mean(
            [s.aggregation_size for s in analysis_states]
        ))
        self.final_monument_level = analysis_states[-1].monument_level
        self.total_exotics = analysis_states[-1].total_exotics
        self.mean_population = float(np.mean(
            [s.total_population for s in analysis_states]
        ))


class PovertyPointSimulation:
    """
    Main simulation class for Poverty Point aggregation model.

    Uses the multilevel signaling framework for:
    - Strategy decisions (aggregation vs independent)
    - Monument investment (equilibrium signaling)
    - Network dynamics (seasonal formation and decay)
    - Vulnerability (derived from network degree)
    - Monument depreciation (annual stock update)

    Annual cycle:
    1. Shortfall determination
    2. Dispersal season foraging
    3. Compute equilibrium lambda
    4. Strategy decisions
    5. Aggregation season (investment, exotics, obligations)
    6. Network update
    7. Monument depreciation
    8. Shortfall mortality
    9. Reproduction and quality update
    10. State recording
    """

    def __init__(self, params: Optional[SimulationParameters] = None):
        self.params = params or default_parameters()
        self.rng = np.random.default_rng(self.params.seed)

        # Initialize agents with quality
        self.bands = create_bands(
            n_bands=self.params.population.n_bands,
            initial_size=self.params.population.initial_band_size,
            region_size=self.params.environment.region_size,
            rng=self.rng,
            q_min=self.params.signaling.q_min,
            q_max=self.params.signaling.q_max,
        )

        # Initialize aggregation site at center
        center = self.params.environment.region_size / 2
        self.aggregation_site = create_aggregation_site(
            location=(center, center),
            epsilon=self.params.epsilon,
            name="Poverty Point"
        )

        # State tracking
        self.year = 0
        self.in_shortfall = False
        self.shortfall_remaining = 0
        self.shortfall_magnitude = 0.0

        # MLS framework cache (recomputed each year)
        self._eq_cache = {
            'lambda_total': self.params.signaling.lambda_W,
            'M_g': 0.0,
            'alpha_eff': 1.0,
            'beta_eff': 1.0,
            'B_lambda': 0.0,
            'k_eff': self.params.network.k_0,
        }

        # Results
        self.results = SimulationResults(
            sigma=self.params.sigma,
            epsilon=self.params.epsilon,
            seed=self.params.seed
        )

    def _generate_shortfall(self) -> Tuple[bool, float, int]:
        """Generate shortfall event based on sigma."""
        sigma = self.params.sigma
        mean_interval = 20 * (1 - sigma) + 5
        p_shortfall = 1.0 / mean_interval

        if self.rng.random() < p_shortfall:
            magnitude = 0.3 + 0.5 * sigma + self.rng.normal(0, 0.1)
            magnitude = float(np.clip(magnitude, 0.2, 0.9))
            duration = max(1, int(1 + magnitude * 2.5))
            return True, magnitude, duration

        return False, 0.0, 0

    def _compute_equilibrium_lambda(self) -> None:
        """Compute MLS equilibrium lambda at current sigma."""
        n_agg = max(5, self.aggregation_site.n_attending)
        eq = lambda_total_at_sigma(
            self.params.sigma,
            self.params.signaling,
            self.params.network,
            self.params.conflict,
            self.params.aggregation,
            n_bands=n_agg,
        )
        self._eq_cache = eq

    def _run_dispersal_season(self) -> None:
        """Run dispersal season: bands forage independently."""
        for band in self.bands:
            base_harvest = 0.4 + 0.2 * self.rng.random()

            if self.in_shortfall:
                base_harvest *= (1 - self.shortfall_magnitude)

            if band.strategy == Strategy.AGGREGATOR:
                harvest = base_harvest * (1 - self.params.aggregation.C_opportunity)
            else:
                harvest = base_harvest

            consumption = band.size * 0.02
            band.resources += harvest - consumption
            band.resources = max(0.0, band.resources)

    def _run_strategy_decisions(self) -> None:
        """Bands decide strategy using MLS fitness comparison."""
        expected_n = max(5, self.aggregation_site.n_attending)
        M_g = self.aggregation_site.effective_M_g
        lam = self._eq_cache.get('lambda_total', self.params.signaling.lambda_W)

        for band in self.bands:
            band.strategy = band.decide_strategy(
                expected_n=expected_n,
                sigma=self.params.sigma,
                epsilon=self.params.epsilon,
                params=self.params,
                rng=self.rng,
                M_g=M_g,
                lam=lam,
            )
            band.strategy_history.append(band.strategy)

    def _run_aggregation_season(self) -> None:
        """Run aggregation season with equilibrium investment."""
        self.aggregation_site.reset_annual_state()
        total_construction = 0.0
        lam = self._eq_cache.get('lambda_total', self.params.signaling.lambda_W)

        for band in self.bands:
            if band.strategy == Strategy.AGGREGATOR:
                # Travel cost
                travel_cost = band.calculate_travel_cost(
                    self.aggregation_site.location
                )
                band.resources -= min(travel_cost, band.resources * 0.5)

                # Register attendance
                self.aggregation_site.add_attending_band(band)
                band.aggregation_history.append(True)

                # Invest at signaling equilibrium
                investment = band.invest_in_monument(
                    lam=lam,
                    q_min=self.params.signaling.q_min,
                    rng=self.rng,
                )
                total_construction += investment

                # Attempt exotic acquisition
                band.acquire_exotic(rng=self.rng)

                # Form obligations with other attending bands
                if len(self.aggregation_site.attending_bands) > 1:
                    potential_partners = [
                        b_id for b_id in self.aggregation_site.attending_bands
                        if b_id != band.band_id
                    ]
                    if potential_partners and self.rng.random() < 0.3:
                        partner_id = self.rng.choice(potential_partners)
                        band.form_obligation(partner_id)

            else:
                extra_harvest = 0.1 * (
                    1 - self.shortfall_magnitude if self.in_shortfall else 1
                )
                band.resources += extra_harvest
                band.aggregation_history.append(False)

        # Record construction
        self.aggregation_site.record_construction(total_construction)

    def _update_networks(self) -> None:
        """Update band network degrees based on monument stock."""
        M_g = self.aggregation_site.effective_M_g
        net = self.params.network
        agg = self.params.aggregation

        for band in self.bands:
            if band.strategy == Strategy.AGGREGATOR:
                k_agg = network_degree(M_g, net.k_0, net.k_max, net.M_half)
                band.network_degree_value = k_agg
                band.seasonal_k = seasonal_effective_degree(
                    k_agg, net.k_0, agg.delta_net, agg.f_agg
                )
            else:
                band.network_degree_value = net.k_0
                band.seasonal_k = net.k_0

    def _apply_shortfall_mortality(self) -> None:
        """Apply mortality using derived vulnerability from network degree."""
        if not self.in_shortfall:
            return

        gamma = self.params.network.gamma

        for band in self.bands:
            if band.strategy == Strategy.AGGREGATOR:
                sigma_eff = self.params.sigma * (1 - self.params.epsilon)
                vuln = vulnerability_coefficient(band.seasonal_k, gamma)
            else:
                sigma_eff = self.params.sigma
                vuln = vulnerability_coefficient(
                    self.params.network.k_0, gamma
                )

            band.suffer_shortfall(vuln, sigma_eff, self.rng)

            # Aggregators can call obligations for help
            if band.strategy == Strategy.AGGREGATOR and band.obligations:
                partner_id = self.rng.choice(list(band.obligations.keys()))
                help_received = band.call_obligation(partner_id, need=0.2)
                band.resources += help_received

    def _apply_reproduction(self) -> None:
        """Apply reproduction with MLS fitness."""
        M_g = self.aggregation_site.effective_M_g
        lam = self._eq_cache.get('lambda_total', self.params.signaling.lambda_W)

        for band in self.bands:
            if band.aggregation_history and band.aggregation_history[-1]:
                fitness = W_aggregator(
                    self.params.sigma,
                    self.params.epsilon,
                    self.aggregation_site.n_attending,
                    self.params,
                    band_quality=band.quality,
                    M_g=M_g, lam=lam,
                )
            else:
                fitness = W_independent(self.params.sigma, self.params)

            band.fitness_history.append(fitness)

            band.reproduce(
                fitness=fitness,
                birth_rate=self.params.population.birth_rate,
                death_rate=self.params.population.death_rate,
                rng=self.rng
            )

            band.apply_storage_decay()

            # Update quality after demographic changes
            band.update_quality(
                self.params.signaling.q_min,
                self.params.signaling.q_max,
            )

            # Band dissolution/fission
            if band.size < self.params.population.min_band_size:
                band.size = self.params.population.min_band_size
            elif band.size > self.params.population.max_band_size:
                band.size = self.params.population.max_band_size

    def _record_state(self) -> YearlyState:
        """Record current state including MLS framework variables."""
        n_agg = sum(1 for b in self.bands if b.strategy == Strategy.AGGREGATOR)
        n_ind = len(self.bands) - n_agg
        n_total = len(self.bands)

        dominance = (n_agg - n_ind) / n_total if n_total > 0 else 0.0

        agg_fitness = [b.fitness_history[-1] for b in self.bands
                       if b.strategy == Strategy.AGGREGATOR and b.fitness_history]
        ind_fitness = [b.fitness_history[-1] for b in self.bands
                       if b.strategy == Strategy.INDEPENDENT and b.fitness_history]

        agg_k = [b.seasonal_k for b in self.bands
                 if b.strategy == Strategy.AGGREGATOR]
        ind_k = [b.seasonal_k for b in self.bands
                 if b.strategy == Strategy.INDEPENDENT]

        # Conflict reduction from cache
        from .signaling_core import conflict_reduction, expected_signaling_benefit
        M_g = self.aggregation_site.effective_M_g
        r = conflict_reduction(M_g, M_g, self.params.conflict)
        lam = self._eq_cache.get('lambda_total', self.params.signaling.lambda_W)
        B_lam = expected_signaling_benefit(
            lam, self.params.signaling.q_min, self.params.signaling.q_max
        )

        state = YearlyState(
            year=self.year,
            total_population=sum(b.size for b in self.bands),
            n_bands=len(self.bands),
            mean_band_size=float(np.mean([b.size for b in self.bands])),
            n_aggregators=n_agg,
            n_independents=n_ind,
            strategy_dominance=dominance,
            aggregation_size=self.aggregation_site.n_attending,
            aggregation_population=self.aggregation_site.current_population,
            monument_level=self.aggregation_site.monument_level,
            effective_M_g=self.aggregation_site.effective_M_g,
            annual_construction=(
                self.aggregation_site.monument_history[-1]
                - self.aggregation_site.monument_history[-2]
                if len(self.aggregation_site.monument_history) > 1
                else self.aggregation_site.monument_level
            ),
            total_exotics=sum(b.total_exotic_count for b in self.bands),
            sigma_effective=self.params.sigma * (1 - self.params.epsilon),
            in_shortfall=self.in_shortfall,
            shortfall_magnitude=self.shortfall_magnitude,
            lambda_total=lam,
            B_lambda=B_lam,
            alpha_eff=self._eq_cache.get('alpha_eff', 1.0),
            beta_eff=self._eq_cache.get('beta_eff', 1.0),
            conflict_reduction_r=r,
            mean_network_degree_agg=float(np.mean(agg_k)) if agg_k else 0.0,
            mean_network_degree_ind=float(np.mean(ind_k)) if ind_k else self.params.network.k_0,
            mean_fitness_aggregators=float(np.mean(agg_fitness)) if agg_fitness else 0.0,
            mean_fitness_independents=float(np.mean(ind_fitness)) if ind_fitness else 0.0,
        )

        self.results.yearly_states.append(state)
        return state

    def step(self) -> YearlyState:
        """Execute one year of simulation."""
        # 1. Shortfall determination
        if self.shortfall_remaining > 0:
            self.shortfall_remaining -= 1
            if self.shortfall_remaining == 0:
                self.in_shortfall = False
                self.shortfall_magnitude = 0.0
        else:
            new_shortfall, magnitude, duration = self._generate_shortfall()
            if new_shortfall:
                self.in_shortfall = True
                self.shortfall_magnitude = magnitude
                self.shortfall_remaining = duration

        # 2. Dispersal season
        self._run_dispersal_season()

        # 3. Compute equilibrium lambda
        self._compute_equilibrium_lambda()

        # 4. Strategy decisions
        self._run_strategy_decisions()

        # 5. Aggregation season
        self._run_aggregation_season()

        # 6. Update networks
        self._update_networks()

        # 7. Monument depreciation
        self.aggregation_site.depreciate_monument(self.params.signaling.delta)

        # 8. Shortfall mortality
        self._apply_shortfall_mortality()

        # 9. Reproduction and quality update
        self._apply_reproduction()

        # 10. Record state
        state = self._record_state()

        self.year += 1
        return state

    def run(self, verbose: bool = False) -> SimulationResults:
        """Run complete simulation."""
        if verbose:
            print(f"Running simulation: sigma={self.params.sigma:.2f}, "
                  f"epsilon={self.params.epsilon:.2f}")

        for _ in range(self.params.duration):
            self.step()

            if verbose and self.year % 100 == 0:
                state = self.results.yearly_states[-1]
                print(f"  Year {self.year}: Pop={state.total_population}, "
                      f"Dominance={state.strategy_dominance:.2f}, "
                      f"M_g={state.effective_M_g:.1f}, "
                      f"lambda={state.lambda_total:.3f}")

        self.results.compute_summary(burn_in=self.params.burn_in)

        self.results.sigma_star_theoretical = critical_threshold(
            self.params.epsilon,
            n=self.params.population.n_bands,
            params=self.params
        )

        if verbose:
            print(f"Complete. Final dominance: {self.results.final_strategy_dominance:.3f}")
            print(f"Theoretical sigma*: {self.results.sigma_star_theoretical:.3f}")

        return self.results


def run_single_simulation(sigma: float, epsilon: float, seed: int,
                          duration: int = 600, verbose: bool = False
                          ) -> SimulationResults:
    """Convenience function to run a single simulation."""
    params = default_parameters(sigma=sigma, epsilon=epsilon, seed=seed)
    params.duration = duration
    sim = PovertyPointSimulation(params)
    return sim.run(verbose=verbose)
