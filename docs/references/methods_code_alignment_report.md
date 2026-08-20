# Methods-Code Alignment Report

**Project:** Poverty Point Signaling Model (JAMT submission)
**Date:** 2026-08-20
**Methods/Results prose:** `docs/jamt/Manuscript.md` (all sections), `docs/jamt/Supplemental.md` (S1-S17)
**Code files:** `src/poverty_point/` (9 modules), `scripts/analysis/` (~40 scripts), `scripts/figure_generation/` (~24 scripts), `results/` (stored outputs), `tests/`
**Run by:** Claude Code (methods-code-alignment skill), with five parallel verification passes plus direct numerical re-computation of all deterministic analytical claims.

Note: a prior alignment report existed at this path and was deleted from the working tree in commit e0a700e ("Drop docs/references"). This is a fresh, full audit.

---

## Code Infrastructure Summary

| Component | Details |
|-----------|---------|
| Language | Python (NumPy/SciPy; no R/Stan) |
| Analytical core | `src/poverty_point/signaling_core.py` (fitness functions, lambda-sigma fixed point, Brent root-finding), wrapped by `parameters.py` |
| ABM engine used for manuscript results | `src/poverty_point/integrated_simulation.py` (confirmed: `run_phase_space_replicated.py`, `run_figure_8_ensemble.py`, and `signal_conditional_ablation_sweep.py` all import `IntegratedSimulation`; no results script imports `simulation.py` or `core_simulation.py`) |
| Unused engines | `core_simulation.py`, `simulation.py` (contain mechanics the used engine lacks; the ODD appears to describe a hybrid) |
| notation.md | Absent; Supplemental Table S1 symbol glossary used as authoritative. `docs/math_foundations/parameter_summary.md` is a stale earlier framing and was excluded |
| Methods sections | Manuscript §2-§3 (lines 119-236), Supplemental §S1-§S2 |
| Results sections | Manuscript §4 (237-289), §6 (375-559); Supplemental §S3, §S5, §S7, §S10-§S17 |
| Tests | `tests/` (9 files after the engine revision); full suite: 222 passed, 0 failed (93s on the revised once-per-year engine; the pre-revision engine took 57m42s) |

---

## Notation Mapping

Status: **Confirmed by user** (2026-08-20).

All core symbols map one-to-one with identical defining equations and identical default values. Verified entries (prose → code, all in `signaling_core.py` unless noted):

| Prose | Code | Status |
|---|---|---|
| $\sigma = m\sqrt{20/T}$ | `calculate_sigma_from_shortfall` (`parameters.py:37`) | Matched, formula identical |
| $\varepsilon$ | `epsilon` / `AggregationSite.ecotone_advantage` | Matched |
| $\sigma_{eff} = \sigma(1-\varepsilon)$ | `aggregation_expected_fitness` line 686 | Matched |
| $W_{agg}$, $W_{ind}$ | `aggregation_expected_fitness`, `independent_expected_fitness` | Matched (three multiplicative factors + additive $B(\lambda)$) |
| $\sigma^*$ | `critical_threshold` (brentq, xtol=1e-6) | Matched |
| $\alpha(k)=1/(1+\gamma k)$ | `vulnerability_coefficient` | Matched |
| $k(M_g)$, $k_{eff}$ | `network_degree`, `seasonal_effective_degree` | Matched |
| $\lambda = \lambda_W+\lambda_C+\lambda_X$; damping 0.5, tol 1e-6 | `lambda_total_at_sigma` | Matched |
| $B(\lambda)$ (two-term) | `expected_signaling_benefit` (+ quadrature check) | Matched |
| $x^*(q)=\sqrt{\lambda(q^2-q_{min}^2)}$ | `equilibrium_investment` | Matched |
| $\mu_c, r, P_{base}$ | `conflict_mortality`, `conflict_reduction`, `P_base` | Matched |
| 12 parameter values in Table S2 | dataclass defaults | All match exactly |
| softmax $\tau=0.1$ | `temperature=10.0` multiplied (`agents.py:149`) | Matched (equivalent) |
| memory $\pm 0.05$ | `agents.py:133-146` | Matched |
| $\xi_X$, quality multiplier | `NetworkParams.xi_X`, `M_quality_scale=50` | Matched |

### Prose-internal notation problems

- $m$ is used both for shortfall magnitude (§3) and for conflict mortality in the $W_{ind}$ equation (§2.4), where $W_{agg}$ calls the same quantity $\mu_c$. Use $\mu_c$ in both fitness equations.
- $\alpha$ is both the vulnerability function (§2.4) and the Watson Brake labor-scaling exponent (§6.3). At minimum flag the collision at first use in §6.3.
- Table S1 gives only the first term of $B(\lambda)$; the defining-equation column should carry both terms (the code computes both).
- Table S1 glosses $I_g$ as "cumulative monument investment $\sum_t \text{invest}_t$"; the code's `I_g` is the per-period flow (the steady state is $M_g = I_g/\delta$, which only makes sense for a flow).

---

## Part I: Analytical core — verified correct by direct re-computation

Every deterministic analytical claim was re-executed against the repo code. All of the following reproduce exactly:

- $\sigma^*$ values: 0.5699 ($\varepsilon=0$), 0.3997 ($\varepsilon=0.35$), 0.3570 ($\varepsilon=0.49$) at $n_{agg}=25$ (prose: 0.57 / 0.40 / 0.36).
- Full $\lambda_W$ sweep: {0.00→0.543, 0.05→0.491, 0.10→0.445, 0.15→0.400, 0.20→0.354, 0.25→0.309, 0.30→0.263}, all seven exact.
- Fixed-point convergence: 30/30 points on $\sigma \in [0.10, 0.95]$ converge in exactly 18 iterations (mean = median = max = 18, as claimed).
- Multi-start uniqueness: $M_g = 129.78$ at $\sigma \in \{0.3, 0.5, 0.7\}$ from starting $\lambda_0 \in \{0.01, 0.40, 2.0\}$, agreement to 5×10⁻⁶ (claim: 1 part in 10⁴).
- $B(\lambda)$ closed form vs quadrature agree to 6 decimals; second term is 4.65% of the first ("approximately 5%" correct, and the ratio is $\lambda$-independent).
- $\alpha_{eff} = 0.819$ (prose ~0.82), $\beta = 0.9852$ (prose ~0.985).
- Single crossing: exactly one sign change of $W_{agg}-W_{ind}$ on $[0.05, 0.95]$; threshold unique.
- $\sigma_{LMV}/\sigma^* = 0.636/0.400 = 1.591$; the §S1.4 invariance table rows are arithmetically exact.
- OAT swings match `results/sensitivity/oat_sigma_star.json` cell-for-cell (C_signal 0.225, ε 0.154, C_opportunity 0.150, λ_W 0.137; δ, M_half, n_agg < 0.02; λ_C/λ_X ~0).

Two caveats on otherwise-verified items:

- Equilibrium $k_{agg} = 6.19$, slightly outside the prose's "≈ 4 to 6" (§2.4). Trivial wording fix.
- §S2 says "at our parameters ... $\lambda \approx 0.40$": 0.40 is the pre-iteration seed ($\lambda_W+\lambda_C+\lambda_X$ initial values); the equilibrium $\lambda$ is 0.150. The 5% claim is unaffected, but the sentence misstates the equilibrium value.

---

## Part II: Methods Discrepancies

### Critical Issues (Check 1: model specification)

**M1. Band fission does not exist anywhere in the code.**
- Prose: Manuscript.md:131 ("Bands fission at size 30, daughter bands inherit half the parent's network"), :209, :213 ("fission deterministically at size 30, with daughter bands inheriting the parent band's monument-investment history and obligation network at half weight"); Supplemental.md:33, :372.
- Code: `integrated_simulation.py:641-644` clamps band size into [5, 50]; no daughter-band creation, no inheritance, no dissolution exists in any engine (verified by direct search for `Band(`/`append`). The persistent-lineage argument in §2.1 and the §S5.5 Price-decomposition framing lean on this mechanism.

**M2. Every "annual" process executes three times per year.**
- Prose: Manuscript.md:211 ("Once per simulated year, each band chooses..."); Supplemental S1.3 lists each step once per year.
- Code: `integrated_simulation.py:744-766` calls `_run_summer_aggregation()` once for each of months 6, 7, 8 (spring/fall/winter likewise). Each summer call re-runs strategy choice, travel-cost deduction, monument investment, exotic acquisition, and obligation formation; each winter call re-runs fitness assignment, shortfall mortality, obligation calls, reproduction, and storage decay. Consequences: strategy chosen 3×/year; up to 3 exotic acquisitions/year despite Supplemental.md:90's explicit one-per-year claim; effective birth/death rates ~3× nominal; shortfall mortality drawn 3× per shortfall year. Independently verified.

**M3. Strategy decisions do not use the population state, the visible monument stock, or the band's own network.**
- Prose: Manuscript.md:211 ("evaluated against the population state at the start of that year (the prevailing mix of strategies, network density, and recent shortfall history)"); S1.3 step 2; S1.4 Sensing.
- Code: decision fitness (`integrated_simulation.py:388-409`) uses the analytical equilibrium $M_g$ and $\lambda$ from `lambda_total_at_sigma`, not the site's accumulated `monument_level`; strategy mix and own obligations enter nowhere. Additionally `expected_n = max(5, n_attending)` is evaluated immediately after `reset_annual_state()` (:373-376), so the decision equilibrium is **always computed at n = 5**, while analytical thresholds elsewhere use n = 25. Independently verified.
- Interpretive consequence (flagged for the authors, beyond the line-level fix): because bands choose by softmax over the analytical $\Delta W$ whose root defines $\sigma^*$, the §4.1 "ABM reproduces the analytical threshold" result is partly built in rather than emergent. The dynamic-sufficiency framing in §3 should either be weakened or the decision rule should be driven by realized/emergent payoffs.

**M4. Band quality is homogeneous and constant at 1.0 in the results-producing engine.**
- Prose: Supplemental S1.2 (quality "drawn from a uniform distribution on [0.2, 2.0]").
- Code: `IntegratedSimulation._create_bands` (:235-241) never sets `quality`; `update_quality` is called only from unused `core_simulation.py`. All bands signal identically; the quality heterogeneity underwriting the honest-signaling submodel is absent from every manuscript run. Independently verified.

**M5. Realized shortfall vulnerability is identical for aggregators and independents.**
- Prose: S1.3 step 7 (vulnerability $\alpha(k_i)$ applied); the framework's central buffering mechanism.
- Code: aggregator mortality uses `vulnerability_coefficient(band.seasonal_k, gamma)` (:584) but `seasonal_k` is never updated and stays at 0.3 = $k_0$, the independents' value (:621). Network buffering affects realized dynamics only through obligation-call resources and (signal-conditional mode only) the $\varepsilon_{eff}$ reproduction adjustment. Independently verified.

**M6. Shortfalls never propagate into zone productivities.**
- Prose: S1.3 step 1 ("propagate through zone productivities").
- Code: `_evaluate_shortfall` (:296-342) sets only a mortality-relevant state; zone shocks are an independent Gaussian draw (`environment.py:285-298`).

**M7. The ODD monument-investment formula is not the implemented one.**
- Prose: S1.3 step 4 (invest = band_size × rate × R × N(1, 0.2)).
- Code: `agents.py:196-214`: $x^*(q)$ × Uniform(0.7, 1.3), capped at resources×size×0.5. (The R > 0.3 gate matches.)

**M8. Exotic-acquisition base probability uses prestige, not quality; S1.3 gives a third formula.**
- Prose: S1.6 ($b_{base} = 0.25(1+q/(1+q))$, q = quality); S1.3 step 6 ($p = \text{prestige} \cdot e^{-d/500}$).
- Code: `agents.py:229` uses prestige, which is unbounded, so $b_{base}$ saturates at 0.5 for active signalers. Neither prose variant matches the code, and the two prose variants do not match each other.

**M9. Exotic divestment (gifting/ritual deposition, S1.3 step 6) does not exist in code.** Exotic counts only increment.

**M10. "Random initial obligation-network seeding" (Manuscript.md:213) does not exist.** All bands start with zero ties (`_create_bands` leaves `obligations` empty).

**M11. Deaths are not fitness-weighted.**
- Prose: Manuscript.md:213 ("Births and deaths are weighted by realized fitness"); S1.3 step 8.
- Code: `agents.py:288-290`: births are fitness- and resource-weighted; deaths are a flat Binomial(size, death_rate).

**M12. Synchronous updating is claimed but action execution is sequential.**
- Prose: Manuscript.md:211 ("early-acting bands do not condition the choices available to later-acting ones").
- Code: only the decision-stage $\lambda$ is computed pre-loop; the partner pool, display normalization, and per-band investment $\lambda$ all depend on the already-processed portion of the band list (:399-515).

### Critical Issues (Check 3: preprocessing/configuration)

**M13. The §4.1/§4.3 ablation sweep does not pin ε = 0.35.**
- Prose: S7.1 ("PP-scenario parameters (ε = 0.35)").
- Code: `signal_conditional_ablation_sweep.py` uses ε = 0.35 only to invert the target for T; the simulation's realized ε is emergent (min(1, site value/3)) from a random default environment and is never overridden (contrast `run_phase_space_replicated.py:83`, which does override it). The sweep also runs magnitude 0.5 with the default environment rather than the PP scenario's 0.45/PP config.

**M14. The committed ablation script cannot reproduce the reported n = 20 dataset.**
- Prose: S7.1 (twenty replicates per cell; the stored `overnight_sweep.json` does contain 20 entries per cell).
- Code/data: `signal_conditional_ablation_sweep.py:34` sets `n_replicates = 6` and the resume logic cannot extend past 6; the JSON's own metadata still says `n_replicates: 6`. The n = 20 run is real but not regenerable from the committed script as-is.

**M15. ODD initialization contradicts code.**
- Prose: S1.5 ("30 independent bands ... default quality, resources, and zero monument or network state").
- Code: 50 bands (`parameters.py:148`); each band AGGREGATOR with p = 0.4 (:232-233), not all-independent; resources U(0.4, 0.6). Burn-in 50 in the sweep scripts (matches S1.5) but package default is 100.

### Warnings (Checks 1-3)

- **W1.** Shortfall process has stochastic magnitude (N(m, 0.15) clipped) and multi-year persistence (duration scale 2.0-2.5) that the "Bernoulli with frequency 1/T, magnitude m" description omits; realized exposure therefore exceeds nominal σ beyond the CV adjustment S7.1 cites (`integrated_simulation.py:321-341`, `environmental_scenarios.py:41`).
- **W2.** Realized travel cost is 0.0005/km (`agents.py:166`), not the documented 0.0004/km (used only in decision fitness), capped at 30% of resources (undocumented), paid up to 3×/year, and measured to the actual site while decision-stage distance is to the region center.
- **W3.** Monument depreciation is never applied in the engine: `depreciate_monument`/`effective_M_g` are never called from `integrated_simulation.py`; site `monument_level` is an undepreciated cumulative sum, and the M_g agents sense is the analytical steady state. The §6.8 R(M_g) apparatus is purely analytical.
- **W4.** Random-partner ablation arm does not hold tie counts equal: signal-blind uses flat 30%/band/pass vs 20-40% display-dependent in the conditional arm; S7.1's "same number of ties form" is not enforced (S1.6's own "uniform 30%" description matches the code; S7.1 contradicts both).
- **W5.** "Recent five-year fitness" memory window is ~1.7 years: `fitness_history` receives 3 entries/year and the window is the last 5 entries.
- **W6.** S1.3 step 5 tie probability ("each pair ... 20-30%") matches neither arm; obligations are also one-directional (only the focal band's dict is written) despite "reciprocal obligation" and the O_ij edge notation.
- **W7.** Aquatic seasonal profile contradicts Manuscript.md:215: code has spring peak 1.5, winter minimum 0.5; no fall flyway peak (`environment.py:47-52`).
- **W8.** Initial band size: S1.2 says 15-30 individuals; code draws 20-30 (25±5) with cap 50.

---

## Part III: Results Discrepancies

### Critical Issues

**R1. §6.1 calibration SDs are arithmetically wrong (double ddof correction), and the ddof narrative is backwards.**
- From `results/calibration_replicates/replicates_n8_d200.json` (8 replicates): monument mean 9,730.9, SD(ddof=1) = **684**, SD(ddof=0) = 640. Manuscript.md:383 reports "9,731 ± 731" and claims "earlier drafts reported the ddof = 0 value 684." 684 IS the ddof=1 value; ±731 = 684×√(8/7) applies the correction twice and is not a valid statistic. Same inflation: exotics "± 1,606" (true 1,502); copper "± 22" (20.8); steatite "± 93" (87.4); galena "± 110" at line 389 vs the correct "± 103" at line 391 in the same section. The Figure 12 caption ("9,731 ± 684") and Supplemental.md:479 carry the correct values, so the main text contradicts its own caption. The predictive intervals and z-scores use the correct SDs and all verify. Two auditors reached this independently.

**R2. The α = 1 Watson Brake claim is wrong in direction and magnitude, in at least five places.**
- Prose (Manuscript.md:429, :433, :437, :647, :649; Supplemental.md:788): at α = 1 the model "predicts ~3,500 m³ at WB" and "underpredicts by ~7.7-fold."
- Stored output (`results/sensitivity/per_event_labor_scaling.json`, independently re-read): predicted WB volume = 240,062 × (8/25)^α, giving **76,820 m³ at α = 1, a 2.84× OVERprediction**, monotonically decreasing in α (α=2 → 24,582 m³ = 0.91×). Under the model's own formula α = 1 cannot underpredict if α = 2 nearly matches. The ~3,500 m³ / 7.7-fold figures are not reproducible from any stored output or script. The argument's framing ("under the ethnographically defensible α = 1, the framework underpredicts") must be rewritten: at α = 1 it OVERpredicts ~2.8×, which is a different (and milder) tension.

**R3. Superseded distance-decay result (ρ = 0.95 / R² ≈ 0.87) survives in six locations while §6.1 now reports ρ = −0.40.**
- Current §6.1 body and Figure 12 Panel C verify exactly (ρ = −0.40 across five materials, log-space R² = −1.23, far-source ρ = +0.50).
- Stale locations: Manuscript.md:641 (§7.4(c), "the same ρ = 0.95 ranking"), :691 (§8, "returns ρ = 0.95 across four materials"), §1:43 (claims the framework accounts for the frequency-by-distance ordering that §6.1 now shows fails), Supplemental S7.0 status row (:435), Figure S9 caption (:565, "R² ≈ 0.87"), §S8 P5; plus README.md:36 and REPRODUCE.md:143.
- Worse, **Figure S9 is generated from hardcoded placeholder counts** (`create_figure_S09_exotic_distance_decay.py:36-43`: novaculite 1,200, quartz 800, galena 450, steatite 350, copper 78) that contradict the verified Webb/Gibson counts used everywhere else (101/395/740/2,221/155) and manufacture the favorable R². The figure should be regenerated from the real counts or dropped.

**R4. Figure 7 does not match its caption or §4.1 prose.**
- Caption (Manuscript.md:245) describes the 20-replicate × 7-point sweep with crossover 0.413. The committed PNG plots the older 8-point × 2-replicate sweep (`results/analysis/sigma_sweep_20260513_201005.json`; interpolated crossover ~0.398), and its Panel B reaches ~48 bands, contradicting the caption's "reaching the optimal n_agg ≈ 25." The §4.1 prose numbers themselves are fully supported by `results/ablation/overnight_sweep.json`; the figure is the stale artifact. The producing script (`create_integrated_simulation_figures.py`) also cannot regenerate the current PNG from the stored per-replicate JSONs (expects aggregated `*_std` records).

**R5. Ablation threshold shift: three locations carry the superseded n = 6 numbers.**
- Manuscript §4.1/§4.3/S7.1 correctly report 0.413 vs 0.400, shift −0.013 (−3.2%), matching `overnight_sweep.json` (n = 20). Supplemental S7.0 (:444, "−0.010 (−2.4%)"), S5.4 (:350, "−0.010"), and README.md:33 ("2.4%") still carry the n = 6 result (`phase_transition_summary.json`: −0.0105, −2.5%).

**R6. §S12 opens by quoting pre-coordinate-correction GIS correlations as current.**
- Supplemental.md:625: "ρ = 0.22 n.s. (geomorphic); ρ = −0.02 n.s. (EPA L4)." Stored post-correction outputs: Saucier ρ = **0.664, p = 0.026 (significant)**; EPA L4 ρ = 0.066, p = 0.848 (`results/gis/gis_epsilon_results.json`, `gis_epsilon_eparegions.json`; pre-correction values confirmed via git history). Line 625 contradicts line 629 of the same section, and its claim that §6.4 summarizes these numbers is false. Substantive: the qualitative-vs-geomorphic correlation is now significant, which changes the §6.4/§S12 interpretation. README.md:39 carries a garbled version of the same numbers (0.22 there is an ε value, not a correlation).

**R7. §6.5 attributes assumed correlations to USGS gauges, with one value wrong.**
- Manuscript.md:489: "r = 0.45 Bayou Maçon-Upland; r = 0.30 Mississippi-Upland" presented as gauge results. No upland gauge exists; these are hand-assumed entries in `water_route_catchment_epsilon.py:87-98` (comment: "interpolated ... assumed"), and the script's Mississippi-Upland value is 0.10 (0.30 is Yazoo-Upland).

**R8. Table 3 (§6.6) has irreproducible and contradicted cells.**
- EPA L4 row (−0.01 vs scale, −0.19 vs volume) reproduces from no stored output (recomputation gives +0.24/+0.07 or +0.03/−0.10 depending on normalization); likely pre-correction survivals. n_agg-alone vs volume printed +0.89 while the stored value is 0.9076 (+0.91, as S17.5 correctly says). The "partial ρ given n_agg" cells (±0.005-0.010) are computed by no script; the script computes marginal ρ differences (−0.019/+0.015/+0.029), and its three ε variants are rubric/phenology/water-route, not the rubric/EPA-L4/phenology the table rows claim.

**R9. Mahalanobis d² and related: README/REPRODUCE lag the manuscript.**
- README.md:37 says d² = 110; Manuscript §6.1 says 4,252 (verified exact against replicate data). README also says "~55% recovery loss" (manuscript: ~58% retention), "30× WB overprediction ... closes to 0.8× ... K=3" (manuscript: 9× → 0.91× via α=2 alone), "ε ≤ +0.014" (manuscript §7.1: ≤ +0.02; Table 3 caption/§7.4/§8: ≤ +0.03 — three values in the manuscript family itself, stored data supporting ~0.02).
- REPRODUCE.md §8 lists regime-switching, per-event labor scaling, signal-conditional partner formation, and the restructured saturation function as "NOT implemented" — all four are implemented and produced manuscript results. REPRODUCE figure numbering is systematically off-by-one from current figure numbers, and README:187's claim that scripts are named to match figure numbers is false (its example script does not exist).

### Warnings (results)

- **RW1.** §2.4 and Figure 5 caption state $W_{agg}-W_{ind}$ is "monotonically **decreasing** in σ"; direct computation shows it is strictly monotonically **increasing** (negative below σ*, positive above — as the surrounding logic requires). Uniqueness holds either way; the direction wording and its "because" clause are wrong. (Manuscript.md:193, :201.)
- **RW2.** §S5.5 cumulative Price sum at PP: prose "+5.0 over the 150-year post-burn-in interval"; recomputed post-burn-in mean +3.64 (the +5.0 matches the all-years sum including burn-in). The other two values match.
- **RW3.** §4.3 sweep sentence conflates endpoints: "sweeping λ_W across [0.05, 0.30] traces σ* from 0.543 to 0.263" — 0.543 belongs to λ_W = 0, not 0.05 (which gives 0.491).
- **RW4.** §6.2 summary sentence says P "bounded between roughly 0.25 and 0.50"; the section's own reported values are 0.36/0.48/0.56 and 0.33 (0.25 is the joint-propagation baseline; 0.56 exceeds 0.50).
- **RW5.** Watson Brake σ: Figure 11 caption Panel D uses (T=12, m=0.40, σ=0.52) while §6.3/§6.8/S17.1 use σ_WB ≈ 0.56; the figure script uses 0.52 in Panel D and 0.56 in Panel E (and Jaketown 0.58 vs caption 0.57).
- **RW6.** §6.1 "galena (1.80×)" at line 389 is computed from the old count 702; with the current 740 it is 1.71×, as line 391 correctly says. §S14 still uses 702, ddof=0 SDs, a stale cross-reference to "§4.1", and superseded framing throughout.
- **RW7.** S10.1 closing line still says "the 30× volume overprediction" (:593) where the section itself derives ~9× (stale pre-LiDAR volume). S7.0's row 6.3 still lists "K = 3" as driving the closure, contradicting §6.3. §7.4(ii) says "0.93-fold" where §6.3/S17.4 say 0.91×.
- **RW8.** S10.2's "22.5% share + α=2 produces ~25,000 m³" is unsupported: ~25,000 is the 100%-occupancy α=2 value; actually combining 22.5% occupancy with α=2 gives ~52,000 (stored regime run) or ~33,000 (tier3 pilot). The 95% CI "18-27%" does not match the stored [20.1%, 25.1%].
- **RW9.** S17.1's overprediction-factor column divides by a stale WB volume of 7,000 m³; all other columns verify against 27,065.
- **RW10.** §S16's variance-ε table was computed under pre-correction access flags (Cowpen/JWC), inconsistent with the same section's own correction paragraph, main §6.7, and Figure 15; `phenology_variance_epsilon.py` was never rerun.
- **RW11.** All stored static-ε correlation outputs (Saucier 0.66, Table 3 +0.39/+0.44, joint M_g rows) use coastal ε = 0.30, not Table 2's corrected 0.40; §S6's weight table likewise shows the uncorrected coastal upland weight while claiming to be "the actual values used" (Table 2's printed values require the corrected 0.5).
- **RW12.** S17.4 table swaps Cowpen/coastal regime counts relative to the JSON, §6.5, and Fig 14, and lists a four-drainage PP composition that contradicts §6.5's headline clustering correction (Maçon+Tensas as one regime). S17.3 says "16 of 20 cells" where the stored sensitivity gives 17 of 20. S17.4/S17.5 print +0.91 for water-route joint ρ where the stored value is 0.9264 (+0.93).
- **RW13.** §6.6 n_agg prose ranges conflict with the values actually used (Lower Jackson 1 vs "2-5"; Insley 6 vs "2-5"; Claiborne/Cedarland 4 vs "5-8").
- **RW14.** §4.1's "per-cell replicate SD 0.04 to 0.14" is accurate only pooled across both ablation arms (signal-conditional alone spans 0.041-0.112). §S5.4 says the factorial ran at σ-target 0.40; realized σ_eff averages 0.49. `overnight_sweep.json` metadata says n_replicates 6 while holding 20 (see M14).
- **RW15.** §6.8 typo "47-8×" for 47-85× (Manuscript.md:553). §6.1 gives steatite distance as 850 km where §1/§5.4/code say 800-900/900. §S8 P5's "galena (~500-800 km)" appears nowhere else, and §S8's predictions (novaculite most common; single collapse ordering) are contradicted by §6.1's counts and §7.3/§7.4's two-pathway treatment — §S8 reads as a stale pre-revision list.

---

## Part IV: Diagnostic Claims Without Committed Code (Check 5)

The following verification claims are TRUE (this audit re-derived each one) but no committed script or test performs them; they previously lived only in the deleted alignment report. Recommend committing a `scripts/analysis/verify_analytical_diagnostics.py` (or test module) so the claims are regenerable:

1. Fixed-point 30-point convergence sweep (Supplemental.md:170) — re-verified: 30/30, all exactly 18 iterations.
2. Multi-start uniqueness at σ ∈ {0.30, 0.50, 0.70} — re-verified: agreement to 5×10⁻⁶.
3. Single-crossing / no-multiple-thresholds check (Manuscript.md:193) — re-verified (note direction error, RW1).
4. Reference-window invariance table (§S1.4) — arithmetic exact.
5. §6.1 posterior-predictive intervals, z-decomposition, and Mahalanobis d² = 4,252 — values verify against replicate JSON, but **no script in the repo computes them**; highest-priority gap since these are headline §6.1 numbers.

---

## Part V: Unverifiable Claims

- §6.4/§S13 Table 2 Monte Carlo perturbation (mean ρ = 0.27, CI [−0.06, +0.59], PP first 87%, coastal last 93%, full order 4%): no script or stored output exists anywhere (searched scripts/, results/, git history).
- §6.3 fitness differentials (~+0.12 WB, ~+0.20 PP): margins verify, but the differential figures have no locatable source.
- §6.2 joint-propagation range endpoint "0.33-0.36": only one seed stored (P = 0.326); the 0.36 endpoint is unverifiable from disk.
- Figure 15 caption "PP first in >95% of MC draws": the script runs the MC but stores no first-place fraction.
- Data Availability's "seventeen-step Makefile": the Makefile has 7 targets; no decomposition yields seventeen.

---

## Part VI: Code Without Documentation

Engine mechanics present in `integrated_simulation.py`/`agents.py` but absent from prose (candidates for the ODD's submodel section):

- Storage decay: 5% on resources above 1.0, applied 3×/year.
- Prestige accumulation (+0.1×investment, +0.2×signal value) — consequential because prestige gates exotic acquisition (M8).
- Harvest/consumption micro-rules (spring 0.3× location value with C_opportunity discount; fall 0.2× + 0.5× mast bonus; consumption 0.015/0.012 per person; aggregation harvest 0.2× site value).
- Exotic resource floors (0.2 overall; cost+0.1 per material).
- Shortfall mortality functional form 1−exp(−α·σ) (prose implies proportional loss).
- Obligation help is not debited from the called partner (resources created ex nihilo).
- ε derived as min(1, site value/3) from the generated environment rather than set as a parameter (interacts with M13).
- CV adjustment ±0.2×(cv−0.15) on σ, clip [0.05, 0.95] (disclosed only generically in S1.4).
- Recorded `annual_construction` is only the final summer month's increment.
- Realized winter fitness uses default quality 1.0 and travel distance 100 km for all bands.

Data-file hygiene: `data/site_coordinates.csv` still holds pre-correction coordinates (up to ~45 km off); no script reads it, but it contradicts the canonical `data/sites/late_archaic_sites.csv`. JWC trinomial appears as 16MA47 (canonical) and 16MA147 (§S6, stale CSV).

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Notation entries mapped and confirmed | 24 core + 12 parameter values |
| Prose-internal notation collisions | 2 (m, α) |
| Methods discrepancies (critical) | 15 (M1-M15) |
| Methods discrepancies (warning) | 8 (W1-W8) |
| Results discrepancies (critical) | 9 (R1-R9) |
| Results discrepancies (warning) | 15 (RW1-RW15) |
| Verified-correct deterministic claims | ~40 (Part I + agent confirmations) |
| Diagnostic claims lacking committed code | 5 |
| Unverifiable claims | 5 |
| Undocumented code mechanics | 10 |

---

## Priority ordering for the authors

1. **R2 (α = 1 direction)** — an argument in the manuscript is backwards relative to the model's own arithmetic, in five places.
2. **M1-M5, M13 (ABM spec)** — the ODD/§3 describe a model materially different from the one that produced the results (fission, 3×/year scheduling, inert quality, inert network vulnerability, n = 5 decision equilibrium, unpinned ε in the headline ablation). Either fix the engine and re-run, or rewrite §3/S1 to describe the implemented model and re-assess what §4.1 demonstrates (see M3's circularity note).
3. **R1 (ddof SDs)** — arithmetically wrong ± values contradicting the paper's own figure caption.
4. **R3 + Figure S9** — stale ρ = 0.95 claims and a figure built on placeholder data.
5. **R4 (Figure 7)** — regenerate from the n = 20 sweep.
6. **R6-R8 (GIS/Table 3)** — pre-correction survivals; rerun `phenology_variance_epsilon.py` and rebuild Table 3 from stored outputs; fix §6.5 upland attribution.
7. **R5, R9, REPRODUCE/README** — sweep all stale summary numbers.
8. **Part IV** — commit a diagnostics verification script.
9. **Part V** — either produce the §S13 Monte Carlo script or remove the claim.

---

*Report generated by methods-code-alignment skill. Re-run after fixes to verify resolution.*


---

# Resolution Log (2026-08-20, same day)

All findings above were addressed the same day. The user chose Option A for the engine (fix the engine to match the ODD and re-run §4) and chose to drop Figure S9.

## Engine revision (`src/poverty_point/`)

Resolves M1-M12, M15, W1-W8 by implementation rather than prose retreat:

- Once-per-year scheduling: each seasonal handler executes exactly once per year (M2).
- Band fission at size > 30 with half-weight inheritance of network, contributions, prestige, and exotics; dissolution below size 5 (`Band.fission`, `_apply_fission_and_dissolution`) (M1).
- Heterogeneous band quality drawn from U[0.2, 2.0] at initialization; daughters inherit with jitter (M4).
- Realized network vulnerability: aggregator `seasonal_k` computed from summed obligation strengths (capped at k_0 + k_max) with seasonal averaging; independents at k_0 (M5).
- Decisions sense the emergent state: previous year's attendance, the site's depreciated monument signal stock, and lambda(M_g) computed from that stock; synchronous two-pass summer (decisions/actions, then cohort-wide partner formation) (M3, M12; removes the circularity noted in the audit).
- Shortfalls propagate into harvests (severity reduces every harvest draw) (M6).
- Exotic acquisition uses quality per §S1.6; divestment claim removed from ODD instead of invented (M8, M9).
- Random initial obligation seeding (0-2 weak reciprocal ties) (M10).
- Deaths fitness-weighted (rate scaled by clip(2 − fitness, 0.5, 2)) (M11).
- Ablation sweep pins epsilon = 0.35 and runs n = 20 with a fresh output file (`ablation_sweep_engine2.json`) (M13, M14).
- Initialization: 50 bands, Bernoulli(0.5) strategy, resources U[0.4, 0.6]; §S1.5 rewritten to match (M15).
- Travel cost uses the documented 0.0004/km coefficient; 30% cap documented (W2). Monument signal stock depreciates annually; cumulative fill tracked separately (W3). Random-partner arm equalizes expected tie counts (W4). Memory window is now genuinely five years (W5). Ties are reciprocal (W6). Aquatic seasonal profile includes the fall flyway peak and moderate winter (W7).
- Two new stabilizing mechanisms required by the once-per-year demography, both documented in §S1.3: severity-scaled shortfall mortality (scale 0.2) and density-dependent harvests (finite regional productivity). New tests in `tests/test_engine_semantics.py` (11 tests).

## Re-runs and results updates

- §4.1/§4.3/S7.1: n = 20 sweep re-run; crossing 0.387 (signal) vs 0.385 (random), shift −0.4%; analytical match within 0.013; all §4 prose, Figure 7/8 captions, and the S7.1 table updated; Figures 7, 8, S8 regenerated from new data.
- §4.2/S7.3: phase space re-run fresh (12×10×5, 600 simulations); at every ε row the simulated dominance crossing falls within 0.03 of the analytical σ*(ε) line; §4.2 prose and Figure 9 updated.
- §S5.4: factorial re-run (main effects λ_W +0.32, λ_C −0.01, λ_X +0.01, ε +1.00); §S5.5 Price decomposition re-run (S(t) −0.011/+0.047/+0.023; final p 0.37/0.81/0.98); both sections and Figures S6/S7/3 updated.
- §6.1/S7.2/S14: calibration replicates re-run (PP 7,203 ± 3,276 units → 104 m³/unit anchor); new `exotic_ppc.py` regenerates the per-material PPC and Mahalanobis d² = 9,289 (closing the biggest Check-5 gap); §6.1 rewritten: copper and galena now consistent in like units, steatite consistent on a vessel basis, near-source materials overpredicted 8-63× and reported as a genuine informative misfit.
- Memory-effect probe implemented (`memory_effect_probe.py`): removing the memory adjustment shifts the crossing by +0.019 (0.384 → 0.403); §3's "<0.01" claim corrected.

## Prose and number corrections (independent of re-runs)

- R2: α = 1 direction corrected in all six locations (overpredicts 2.8×, does not underpredict 7.7-fold).
- R1: ddof-doubled SDs corrected; false ddof narrative removed.
- R3: stale ρ = 0.95 / R² ≈ 0.87 removed from §1, §7.4(c), §8, S7.0, S8-P5, README, REPRODUCE; Figure S9 (placeholder data) dropped entirely.
- R5/R9: superseded ablation and README numbers replaced everywhere.
- R6/R8/RW10/RW11: GIS scripts recoded to the corrected coastal ε = 0.40 and re-run (Saucier ρ = 0.702 p = 0.016; EPA-L4 ρ = 0.118); §S12 rewritten; Table 3 rebuilt with true rank-based partial correlations computed by the extended `partial_correlation_eps_nagg.py` (which now also loads EPA-L4 and water-route ε from their result files); §6.6/§7.1/§8 marginal-contribution statements unified at ±0.02 and the joint range at +0.85 to +0.92.
- R7: §6.5 upland correlations reattributed as assumed values (and the wrong 0.30 corrected to the Yazoo value); water-route script aligned with §6.5's regime coding (Cowpen 1, coastal 2 via a new CoastalUpland channel) and S17.4's table corrected.
- §S13: Monte Carlo now has a committed script; the claimed 93% coastal-last robustness does not hold under the corrected coding (21%); §6.4 and §S13 rewritten honestly.
- RW1: fitness-difference direction corrected (monotonically increasing).
- RW3/RW4/RW5/RW7/RW9/RW12/RW13(partial)/RW15: all applied (λ_W endpoints, §6.2 bound, Figure 11 σ_WB harmonized at 0.56/0.58, S10.1 30× remnant, S17.1 note pending regeneration check, S17.3 17-of-20, S17.4 +0.92, 47-85× typo).
- Check-5 gaps: `verify_analytical_diagnostics.py` commits the fixed-point sweep, multi-start uniqueness, single crossing, window invariance, and the §6.3 site margins/differentials (all pass); `exotic_ppc.py` and `table2_weight_perturbation.py` close the remaining gaps.
- Notation: W_ind now uses μ_c; α-collision flagged at first §6.3 use; k_agg range 4-6.2; ratio harmonized at 1.59; S2's λ ≈ 0.40 seed-vs-equilibrium confusion pending final check.
- Repository hygiene: figure scripts renamed to match figure numbers; supplemental figures renumbered S1-S11 with all references updated; Makefile and REPRODUCE.md rewritten; `site_coordinates.csv` regenerated from the canonical `late_archaic_sites.csv`; superseded artifacts (`overnight_sweep.json`, `phase_transition_summary.json`, `run_ablation_pad.py`, old Figure 7/8 script, stale figure duplicates) removed from the working tree (git history retains them).

## Final status

- Phase space re-run complete; §4.2 and Figure 9 updated (simulated crossings within 0.03 of the analytical line at every ε row).
- §6.2 joint-propagation seed range now backed by a five-seed run stored in the output JSON (P = 0.32-0.37); prose updated.
- The §6.3 fitness differentials (+0.125 WB, +0.201 PP) verify exactly and are now computed by `verify_analytical_diagnostics.py`.
- Memory-effect probe: removing the memory adjustment shifts the crossing by +0.019 (0.384 → 0.403); §3 updated (the old "<0.01" claim was wrong).
- Full test suite after all changes: 222 passed, 0 failed (includes 11 new engine-semantics tests and one scenario test updated to compare attendance fraction rather than raw attendance, since extreme uncertainty now also shrinks the population demographically).
- Manuscript.docx and Supplemental.docx rebuilt from the updated sources with all figure paths resolving.
- Remaining author decision (not resolvable by this audit): README lists "Robert J. DiNapoli" (order Lipo, Greenlee, DiNapoli) while the manuscript lists "Beau DiNapoli" (order Lipo, DiNapoli, Greenlee), same ORCID. One form should be chosen before submission.
