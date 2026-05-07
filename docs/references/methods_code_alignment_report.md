# Methods-Code Alignment Report (Round 2)

**Project:** Poverty Point Costly Signaling
**Manuscripts:**
- Main: `docs/manuscript_AA/Poverty_Point_AA.md` (~22,000 words; AA Round 3 + extensions)
- Supplemental: `docs/manuscript_v2.0/supplemental/Supplemental_Material.md`

**Code:**
- Core analytical model: `src/poverty_point/signaling_core.py`
- Parameter dataclasses: `src/poverty_point/parameters.py`
- ABM: `src/poverty_point/integrated_simulation.py`
- Recently-added extension scripts: `scripts/analysis/{predicted_scale_ratios,per_event_labor_scaling,regime_switching_simulation,near_threshold_ablation,restructured_saturation_test,bayesian_threshold_posterior,oat_sensitivity_table,hydrograph_covariance,phenology_variance_epsilon}.py`

**Date:** 2026-05-01
**Skill:** methods-code-alignment
**Scope:** Focused audit of the recently-added extensions and their manuscript descriptions, supplementing the 2026-04-30 first-round report. Notation mapping presented below; core mapping unchanged from prior report.

---

## Code Stack Summary

- **Language:** Python 3 (NumPy, SciPy, dataclasses; networkx in ABM)
- **No Bayesian framework** in the modeling sense. Check 5 (Diagnostic Reporting) reframed for fixed-point solver convergence and Monte Carlo sampling.
- **Notation source:** Table S0 in Supplemental Material §S2 serves as the de facto glossary; no separate `notation.md`.

---

## 1. Notation Mapping (manuscript ↔ code)

The mapping below covers symbols used in the recently-added extensions. The full mapping from the 2026-04-30 report remains valid; symbols below are appended.

| Manuscript symbol | Code variable | File:line | Status |
|---|---|---|---|
| σ | `sigma` | `signaling_core.py:597` (function arg) | Same name |
| σ_eff | `sigma_eff = sigma * (1 - epsilon)` | `signaling_core.py:631` | Same name and form |
| σ* | return value of `critical_threshold()` | `signaling_core.py:705-758` | Same role |
| ε | `epsilon` | `signaling_core.py:599` (arg); `parameters.py:188` | Same name |
| n_agg | `n_agg` (function arg); `n_bands` (loop variable) | `signaling_core.py:514, 600` | Same name |
| λ_W | `SignalingParams.lambda_W = 0.15` | `signaling_core.py:42` | Same name and value |
| λ_C | `SignalingParams.lambda_C = 0.10` (initial seed) → endogenous via `compute_lambda_C()` | `signaling_core.py:43, 357-379` | Same name |
| λ_X | `SignalingParams.lambda_X = 0.15` (initial seed) → endogenous via `compute_lambda_X()` | `signaling_core.py:44, 457-501` | Same name |
| ξ_X (extension 5) | `NetworkParams.xi_X = 0.0` (default) | `signaling_core.py:69` | Same name |
| Q(M_g) (quality multiplier, ext. 5) | `Q = M_g / (M_g + M_quality_scale)` | `signaling_core.py:499` | Same role |
| M_quality (extension 5) | `NetworkParams.M_quality_scale = 50.0` | `signaling_core.py:75` | Same role; default value matches manuscript narrative |
| k_eff | `seasonal_effective_degree()` | `signaling_core.py:412-427` | Same role |
| α(k), β(k_0) | `vulnerability_coefficient(k, gamma)` | `signaling_core.py:443-454` | Same role; α and β share the formula 1/(1+γk) |
| M_g | `M_g` (state variable) | `signaling_core.py:537, 566` | Same name |
| B(λ) | `expected_signaling_benefit()` | `signaling_core.py:202-220` | Same role |
| C_total | `C_total = C_travel + C_opportunity + C_signal` | `signaling_core.py:627-628` | Same role and components |
| α (per-event labor scaling, ext. 2) | `alpha` in `per_event_labor_scaling.py` | `scripts/analysis/per_event_labor_scaling.py` | Same role |
| K (band-coordination persistence, ext. 1) | `persist_K` in `regime_switching_simulation.py` | `scripts/analysis/regime_switching_simulation.py` | Same role |
| σ_sd (regime-switch noise sd) | `sigma_sd_input` in regime-switching JSON | `results/sensitivity/regime_switching_wb.json` | Same role |
| m (conflict mortality) | `ConflictParams.conflict_mortality = 0.08` | `signaling_core.py:89` | Same value; different name |
| P_base | `ConflictParams.P_base = 0.008` | `signaling_core.py:88` | Same name and value |
| r (conflict reduction) | `conflict_reduction()` | `signaling_core.py:340-354` | Same role |

**Ghost-variable check.** Every quantity used in §4.5 / §S7.7 / §S7.5b / §S7.6 / §S3.1 prose has a code counterpart. No "ghost variables" identified in the extension narratives. The symbols σ_eff, σ*, ε, n_agg, λ_W, λ_C, λ_X, k_eff, M_g, ξ_X, Q(M_g), and r all map cleanly.

---

## 2. Numerical-Claim Verifications

Each spot-check below records the manuscript claim, the actual JSON / code value, and a pass/fail verdict.

### 2.1 §4.5 / Conclusions: Watson Brake regime-switching prediction (PASS)

**Manuscript claim** (§4.5, repeated in Conclusions):
> "per-event labor scaling combined with stochastic regime-switching brings the prediction to 5,408 m³ (95% CI [2,622, 8,694]) at paleoclimate-central parameters."

**Verification.** `results/sensitivity/regime_switching_wb.json`, cell `sd_0.100_persist_3`:
- `predicted_volume_m3_mean`: 5408.11
- `predicted_volume_m3_ci95`: [2622.12, 8693.95]

Manuscript value 5,408 m³ matches JSON 5408.11. CI [2,622, 8,694] matches JSON [2622, 8694]. **PASS.**

Also, S7.7(1) reports "At $\sigma_{sd} = 0.125$ and $K = 3$, the central prediction is 7,942 m³, near-exactly observed." JSON `sd_0.125_persist_3`: predicted_volume_m3_mean = 7941.73 → manuscript 7,942. **PASS.**

### 2.2 §4.5 / Conclusions: Cross-site magnitude prediction Spearman ρ (PASS, with W1)

**Manuscript claim** (§4.5, S7.7(7), Conclusions):
> "Spearman $\rho = +0.85$ to $+0.89$ between predicted M_g(ε, n_agg) and observed monument scale"

**Verification.** `results/sensitivity/predicted_scale_ratios.json`:
- `pred_static_vs_ordinal.rho` = 0.8478 → rounds to **+0.85**
- `pred_phen_vs_ordinal.rho` = 0.8812 → rounds to **+0.88**
- `pred_static_vs_volume.rho` = 0.8848 → rounds to **+0.88**
- `pred_phen_vs_volume.rho` = 0.8986 → rounds to **+0.90**

Range +0.85 to +0.90. The S7.7(7) text gives more precise breakdown: "ρ = +0.85 (p = 0.001) under static-ε inputs and ρ = +0.88 (p < 0.001) under phenology-ε inputs. Against observed volumes (where reported), ρ = +0.89 (static) and ρ = +0.90 (phenology)" — the +0.89 there is the JSON 0.8848 rounded up; the phenology-against-volume 0.8986 rounds to +0.90, not +0.89. The main-text framing "+0.85 to +0.89" is therefore a slight understatement of the true upper bound (+0.90).

**Verdict: PASS in spirit, minor inconsistency between main-text upper bound and supplemental breakdown.** See Discrepancy W1 below.

### 2.3 §S7.7 ext. 5: Restructured network-saturation values (PASS)

**Manuscript claims** (§4.3, §S7.7(5)):
- λ_X at equilibrium: 0.000 (xi_X=0) to 0.033 (xi_X=0.5), with 0.032 in the signal-blind variant at xi_X=0.5
- threshold shifts: +36.0% / +36.8% / +37.2%

**Verification.** `results/sensitivity/restructured_saturation_test.json`:
- xi_X=0.0: full-apparatus `lambda_X_at_equilibrium` = 1.097e-5 → ~0.000 ✓; signal-blind = 0.001246 (~0.001, not 0.000); `threshold_shift_pct` = **35.95%** → rounds to +36.0% ✓
- xi_X=0.25: full λ_X = 0.01665 ≈ 0.017; signal-blind λ_X = 0.01325 ≈ 0.013; shift_pct = **36.84%** → +36.8% ✓
- xi_X=0.5: full λ_X = 0.03245 ≈ 0.033; signal-blind λ_X = 0.03232 ≈ 0.032; shift_pct = **37.17%** → +37.2% ✓

All three threshold shifts match. λ_X values at xi_X=0.5 (0.033 with apparatus, 0.032 without) match manuscript. **PASS.**

The code implementation in `signaling_core.py:457-501` correctly accepts `xi_X` via `NetworkParams` and computes
```
lambda_X = marginal + xi_X * S(k, sigma) * Q(M_g)
```
with `Q(M_g) = M_g / (M_g + M_quality_scale)` and default `M_quality_scale = 50.0`. The functional form matches the manuscript equation in §S7.7(5).

### 2.4 §S7.7 ext. 4: Near-threshold ablation flip zone (PASS, with caveat)

**Manuscript claim** (§4.5, §S7.7(4), §5.6):
> "the apparatus matters specifically in the bistable zone (σ_eff between 0.40 and 0.55 at PP parameters), where it determines whether aggregation is adaptive at all"

**Verification.** `results/sensitivity/near_threshold_ablation.json`:
- All rows show `sigma_star_signal` = 0.3997 and `sigma_star_blind` = 0.5433
- The flip zone is therefore [0.400, 0.543]
- σ values that fall inside: {0.40, 0.425, 0.45, 0.475, 0.50, 0.525} — i.e., 6 sweep points

§S7.7(4) reports: "Six $\sigma$ values in the sweep range $[0.40, 0.525]$ flip regime classification across the ablation". This is correct given the JSON sweep grid (which goes 0.30 → 0.65 in 0.025 increments, capping at 0.525 as the highest sweep point still below σ*_blind = 0.543). The manuscript phrasing "[0.40, 0.55]" in §4.5 / §5.6 is a mild rounding of the actual flip-zone upper bound 0.543, which is consistent with both the data and the supplemental-text bound.

**Caveat (Info-level).** The JSON shows that the equilibrium M_g values are *invariant* across all σ in the sweep (both with and without the apparatus, M_g is the same constant 129.78 / 11.83). The ablation result is therefore *not* a function of σ over this range; it is a one-shot equilibrium comparison repeated at each σ. The substantive content (a regime-classification flip across [0.40, 0.543]) is correct; the sweep is a presentation device, not a sweep over a free parameter. The supplemental text (§S7.7(4)) acknowledges this: "the equilibrium difference is therefore not a function of σ but of whether the apparatus is engaged at all." The main text §4.5 / Conclusions phrasing is internally consistent with this reading. **PASS.**

### 2.5 §4.5 / §S7.5b: Hydrograph covariance claims (PASS)

**Manuscript claims** (§4.5 main text, §S7.5b):
- Bayou Maçon vs Tensas $r = 0.90$, $n = 93$
- Mississippi vs Yazoo $r = 0.11$, $n = 59$
- Mississippi vs Tensas $r = 0.34$, $n = 204$
- Yazoo vs Tensas $r = 0.54$, $n = 231$
- Simultaneous bottom-quartile flow ~10% of months

**Verification.** I re-computed log-monthly-anomaly Pearson correlations from `results/hydrography/usgs_monthly_discharge.csv` (climatology removed by month-of-year, on $\ln(\text{discharge}+1)$):
- Bayou Maçon vs Tensas: n = 93, r = +0.902 → **+0.90** ✓
- Mississippi vs Yazoo: n = 59, r = +0.113 → **+0.11** ✓
- Mississippi vs Tensas: n = 204, r = +0.339 → **+0.34** ✓
- Yazoo vs Tensas: n = 231, r = +0.541 → **+0.54** ✓

`results/hydrography/four_drainage_covariance.json` `low_coincidence_observed[3]` = 0.1017 = 10.17% → manuscript "~10%" ✓.

The four-drainage table in §S7.5b ("Distribution of drainages-in-bottom-quartile per month: 0 = 54.2%, 1 = 25.4%, 2 = 10.2%, 3 = 10.2%") matches JSON `low_coincidence_observed` = {0: 0.5424, 1: 0.2542, 2: 0.1017, 3: 0.1017}. **PASS.**

**Reporting-completeness note (Info-level).** The Bayou Maçon vs Tensas correlation, although central to the §S7.5b claim, is not stored in the saved `four_drainage_covariance.json` (which records only the 3-gauge aligned Mississippi/Yazoo/Tensas matrix). It is computed by the script and printed to stdout but lost on re-load. The script's pairwise-fallback block produces the value, so it is reproducible from the cached CSV — but a reader who reads only the JSON cannot recover the headline 0.90 number. See I1 below.

### 2.6 §4.5: Bayesian ε-prior sensitivity (PASS)

**Manuscript claim** (§4.5, Conclusions, Figure 3 caption):
- P(σ_eff > σ*) = **0.36** (rubric prior), **0.56** (flat prior), **0.48** (GIS-mixture prior)

**Verification.** `results/bayesian/threshold_posterior.json`:
- `rubric.P_above_threshold` = 0.355 → **0.36** ✓ (rounded to 2 decimals)
- `flat.P_above_threshold` = 0.564 → **0.56** ✓
- `gis_mixture.P_above_threshold` = 0.479 → **0.48** ✓

Posterior σ_eff means: 0.324, 0.445, 0.393 → manuscript reports "0.324, 0.445, and 0.393" ✓.
Posterior σ* means: 0.357, 0.422, 0.392 → manuscript reports "0.357, 0.422, and 0.392" ✓.

The Data Availability statement claims "seed = 42" / 43 / 44 for the three priors. Code (`bayesian_threshold_posterior.py:133-135`) confirms `RNG_SEED = 42`, `RNG_SEED + 1 = 43`, `RNG_SEED + 2 = 44`. The JSON only stores the base seed (42), but the seed strategy is correctly documented and reproducible from the script. **PASS.**

### 2.7 §4.2: Calibration replicates (PASS)

**Manuscript claims** (§4.2, §S4 Table):
- Calibrated PP: 9,731 ± 684 monument units, 21,469 ± 1,502 exotics
- Low: 3,006 ± 480, 6,607 ± 996
- Critical: 10,949 ± 330, 24,253 ± 415
- High: 10,833 ± 1,037, 24,324 ± 1,037
- Per-material at PP: copper 178 ± 21, steatite 838 ± 87, galena 1,265 ± 103, novaculite 12,807 ± 889, crystal quartz 6,381 ± 442

**Verification.** Recomputed from `results/calibration_replicates/replicates_n8_d200.json` using ddof = 1 sample SDs (Python implementation of `numpy.std(..., ddof=1)`):

| Scenario | Monuments mean ± sd | Exotics mean ± sd |
|---|---|---|
| low | 3,006.2 ± 480.2 | 6,606.9 ± 996.2 |
| poverty_point | 9,730.9 ± 684.0 | 21,469.2 ± 1,502.0 |
| critical | 10,948.9 ± 329.7 | 24,252.8 ± 415.4 |
| high | 10,832.7 ± 1,037.4 | 24,324.5 ± 1,036.8 |

Per-material at PP:
- copper: 178.1 ± 20.8 → manuscript 178 ± 21 ✓
- steatite: 837.8 ± 87.4 → manuscript 838 ± 87 ✓
- galena: 1,265.2 ± 103.1 → manuscript 1,265 ± 103 ✓
- novaculite: 12,807.2 ± 889.0 → manuscript 12,807 ± 889 ✓
- crystal quartz: 6,380.9 ± 441.8 → manuscript 6,381 ± 442 ✓

Predictive intervals (mean ± 1.96 × SD):
- copper [137.3, 218.9] → manuscript [137, 219] ✓
- galena [1063.1, 1467.3] → manuscript [1063, 1467] ✓
- steatite [666.4, 1009.2] → manuscript [666, 1009] ✓

**PASS.**

### 2.8 §S3.1: OAT tornado-plot table (PASS, with W2)

**Manuscript claims** (§S3.1 table):
- Baseline σ* = 0.3997
- C_signal swing 0.225, ε swing 0.154, C_opportunity swing 0.150, λ_W swing 0.137, C_travel swing 0.050, k_max swing 0.038, γ swing 0.032, δ_net swing 0.016, k_0 swing 0.007, f_agg swing 0.005, n_agg swing 0.003, δ swing 0.001, M_half swing 0.001, λ_C and λ_X swings = 0.000

**Verification.** `results/sensitivity/oat_sigma_star.json`:
- baseline = 0.3997 ✓
- C_signal swing = 0.2250 → 0.225 ✓
- ε swing = 0.1537 → 0.154 ✓
- C_opportunity swing = 0.1495 → 0.150 ✓ (rounds up at half)
- λ_W swing = 0.1368 → 0.137 ✓
- C_travel swing = 0.04973 → 0.050 ✓
- k_max swing = 0.03807 → 0.038 ✓
- γ swing = 0.03162 → 0.032 ✓
- δ_net swing = 0.01608 → 0.016 ✓
- **k_0 swing = 0.00646 → manuscript reports 0.007.** Standard rounding to three decimals is 0.006 (the value 0.00646 is below the 0.0065 half-rounding boundary). Minor rounding direction inconsistency (W2).
- f_agg swing = 0.00535 → 0.005 ✓
- n_agg swing = 0.00299 → 0.003 ✓
- δ swing = 0.00075 → manuscript reports 0.001 (round-half-up) ✓
- M_half swing = 0.00070 → manuscript reports 0.001. Strictly 0.001 by round-half-up ✓.
- λ_C swing = 1.7e-7 → 0.000 ✓
- λ_X swing = 4.3e-8 → 0.000 ✓

**PASS** with one minor rounding flag on k_0 (W2).

### 2.9 §S7.6: Phenology Test A and variance-based ε (PASS)

**Manuscript claims** (§S7.6):
- Test A: ρ_static = +0.39 (p = 0.24), ρ_phen = -0.21 (p = 0.54)
- Variance-based: ρ = -0.02 (p = 0.95), with PP ε_var = 0.168 etc.

**Verification.**
- `results/phenology/phenology_epsilon_test.json`:
  - `eps_static_vs_scale.rho` = 0.388, p = 0.239 → manuscript +0.39, p = 0.24 ✓
  - `eps_phen_vs_scale.rho` = -0.207, p = 0.542 → manuscript -0.21, p = 0.54 ✓
- `results/phenology/phenology_variance_epsilon.json`:
  - `eps_var_vs_scale.rho` = -0.0215, p = 0.950 → manuscript -0.02, p = 0.95 ✓
  - PP ε_var = 0.168 ✓; Jaketown 0.165 ✓; LJ 0.164 ✓; WB 0.162 ✓; Cowpen 0.159 ✓; JWC 0.159 ✓; Frenchman 0.147 ✓; Insley 0.147 ✓; Claiborne 0.127 ✓; Cedarland 0.127 ✓; Caney 0.122 ✓

All values match. **PASS.**

---

## 3. Model-Specification Check (§2.4 fitness equation)

**Manuscript equation (§2.4):**
$$W_{agg} = (1 - C_{total})(1 - \alpha(k_{eff})\sigma_{eff})(1 - m(1-r)P_{base}) + B(\lambda)$$
$$W_{ind} = (1 - \beta(k_0)\sigma)(1 - mP_{base})$$

**Code implementation** (`signaling_core.py:597-654`):
```python
sigma_eff = sigma * (1.0 - epsilon)
k_agg = network_degree(M_g, ...)
k_eff = seasonal_effective_degree(k_agg, k_0, delta_net, f_agg)
alpha_eff = vulnerability_coefficient(k_eff, gamma)   # 1/(1 + γ·k_eff)
r = conflict_reduction(M_g, M_g, conf_params)
B_lam = expected_signaling_benefit(lam, q_min, q_max)
reproduction = 1.0 - C_total
survival = 1.0 - alpha_eff * sigma_eff
conflict_effect = 1.0 - conflict_mortality * (1.0 - r) * P_base
W = reproduction * survival * conflict_effect + B_lam
```

**Verdict:** Code matches manuscript equation exactly, with `m → conflict_mortality = 0.08`. Where the manuscript writes α(k_eff), the code's `alpha_eff = vulnerability_coefficient(k_eff, gamma)` evaluates 1/(1 + γ·k_eff). Where the manuscript writes β(k_0), the code's `beta_eff = vulnerability_coefficient(k_0, gamma)` evaluates 1/(1 + γ·k_0). Both functions share the implementation, which is consistent with the manuscript's footnote explaining that α and β are the same function applied to different k arguments. **PASS.**

---

## 4. Diagnostic-Convergence Check

**Manuscript claim (§2.4):**
> "Across a 30-point sweep of σ from 0.10 to 0.95, all 30 runs converge to within tolerance, and the iteration count is uniform: mean, median, and maximum are all 18."

**Verification.** Direct empirical run of `lambda_total_at_sigma()` on `np.linspace(0.10, 0.95, 30)` at default parameters (n_bands=25):
- All 30 runs converged: True
- Iteration counts: min = 18, max = 18, mean = 18.00, median = 18.0

**PASS.** The tight uniformity reflects the deterministic damped-fixed-point structure (damping = 0.5, tol = 1e-6, max_iter = 100): every starting point reaches tolerance in exactly 18 steps under default parameters. This is consistent with a contraction-mapping interpretation but is a stronger empirical statement than the manuscript phrasing implies (the implicit minimum is also 18, which the manuscript does not state).

---

## 5. Reporting-Completeness Checks

### 5.1 §3.1 run-configuration table

**Manuscript claim (§3.1):** Three run configurations are used in the article:
- (i) Phase-transition sweep (§4.1): 5 σ_eff values × 2 reps × 400 yrs
- (ii) Calibration scenarios (§4.2): 4 settings × 8 reps × 200 yrs
- (iii) §S3 sensitivity: 1 perturbation each × 10 reps × 100 yrs

**Verification.**
- (ii) **PASS.** `scripts/figure_generation/create_fig_calibration.py` confirms `N_REPLICATES = 8`, `DURATION = 200`, four scenarios. JSON `replicates_n8_d200.json` confirms 4 scenarios × 8 replicates each.
- (i) Not separately verified against a JSON output here, but the figure caption (§4.1) and S-curve plot are consistent with two replicates per σ_eff.
- (iii) **FAIL (Critical).** The §S3.1 OAT tornado-plot table is **purely analytical** — `scripts/analysis/oat_sensitivity_table.py` calls `critical_threshold()` (a deterministic Brent root-finder), with no replicates and no simulated years. The manuscript's "ten replicates per perturbation, 100 simulated years per replicate" description does not match the code that produced the §S3.1 table values (verified above in §2.8). The §S3.1 table is reproducible from the deterministic OAT script alone. See Discrepancy C1.

### 5.2 Random-seed documentation

**Manuscript claim (Data Availability):**
- §4.2 calibration: seeds 1000-1031 via formula `1000 + N_REPLICATES * scenario_index + replicate_index`. ✓ Verified: `create_fig_calibration.py:108` uses `seed = 1000 + N_REPLICATES * SCENARIOS.index(scen) + r`.
- §S3 sensitivity: "seed = 42 as the analytical model default and parameter-perturbation seeds documented in `scripts/sensitivity_analysis.py`." ✗ **The script `scripts/sensitivity_analysis.py` contains no seed value or list. The OAT sensitivity in §S3.1 is deterministic and needs no seed. The Data Availability claim is technically vacuous.** See Discrepancy W3.
- §S7.6 phenology Test A: "seed = 42 (no stochastic component)." ✓ Test A is deterministic, so seed is unused; consistent.
- §4.5 Bayesian: seeds 42 (rubric), 43 (flat), 44 (GIS-mixture). ✓ Verified at `bayesian_threshold_posterior.py:133-135`.
- §S7.4 GIS Monte Carlo: seed = 20240501. Not separately verified in this audit.
- §S7.6 variance-based phenology: not stated in Data Availability, but JSON shows `rng_seed = 42`. Worth adding to Data Availability for completeness.

### 5.3 Restructured-saturation default behavior

**Manuscript §4.3 / §S7.7(5)** states: "We retain $\xi_X = 0.0$ as the default in the main results to preserve comparability with the analyses presented above; the restructured-form sensitivity is documented in §S7.7 extension #5".

**Verification.** `signaling_core.py:69` confirms `xi_X: float = 0.0` as the `NetworkParams` default. `compute_lambda_X()` at lines 494-496 short-circuits to the original marginal-only form when `xi_X <= 0.0`. The xi_X = 0.0 case at the test JSON shows `M_g = 129.78` and `lambda_X = 1.1e-5` (effectively zero) — matching the manuscript's claim that under the original parameterization "$\lambda_C$ and $\lambda_X$ collapse to near-zero at equilibrium." **PASS.**

---

## 6. Discrepancies (Severity-Tagged)

### Critical

**C1. §3.1 / §S3 run-configuration mismatch.**
The manuscript §3.1 "(iii) The §S3 sensitivity analyses run one-at-a-time parameter perturbations, ten replicates per perturbation, 100 simulated years per replicate" describes a stochastic ABM-based sensitivity that does not exist for the §S3.1 OAT table. The actual §S3.1 numerical table is produced by the deterministic `oat_sensitivity_table.py` analytical script. There is no replication or simulated time underlying those numbers.
- **Manuscript location:** §3.1, run-config bullet (iii); also referenced in Data Availability under "§S3 sensitivity sweeps."
- **Code location:** `scripts/analysis/oat_sensitivity_table.py` (deterministic); `scripts/sensitivity_analysis.py` (also deterministic; uses `critical_threshold` directly).
- **Suggested edit:** See E1 below.

### Warning

**W1. Cross-site Spearman ρ upper bound understated.**
Main text §4.5 / Conclusions report "Spearman ρ = +0.85 to +0.89" but the actual upper bound is +0.90 (`pred_phen_vs_volume.rho` = 0.8986). The supplemental §S7.7(7) gives the breakdown that includes ρ = +0.90 (rounded from 0.8986).
- **Manuscript locations:** §4.5 Watson Brake paragraph; Conclusions ("$\rho = +0.85$ to $+0.89$ ($p < 0.01$)"); also in §5.6 ("Eight extensions are flagged ... Spearman ρ = +0.85 to +0.89").
- **JSON location:** `results/sensitivity/predicted_scale_ratios.json` — `pred_phen_vs_volume.rho = 0.8986`.
- **Suggested edit:** See E2 below.

**W2. k_0 swing rounding direction in §S3.1 table.**
Manuscript reports k_0 swing = 0.007. JSON value is 0.00646, which conventionally rounds to 0.006 at three decimals (0.00646 < 0.0065 half-boundary). The other table values are correctly rounded.
- **Manuscript location:** §S3.1 OAT table, k_0 row.
- **JSON location:** `results/sensitivity/oat_sigma_star.json`, k_0 entry, swing = 0.0065 (low_sigma 0.39642, high 0.40288, abs diff 0.00646).
- **Suggested edit:** See E3 below.

**W3. §S3 sensitivity seed-documentation claim is vacuous.**
Data Availability claims "parameter-perturbation seeds documented in `scripts/sensitivity_analysis.py`." That script contains no seed list or seed value because the OAT sensitivity is purely analytical (no stochastic component). The claim is non-load-bearing but as written points readers at a non-existent artifact.
- **Manuscript location:** Data Availability §, second-to-last paragraph.
- **Code location:** `scripts/sensitivity_analysis.py` — no seed references.
- **Suggested edit:** See E4 below.

### Info

**I1. Bayou Maçon vs Tensas correlation absent from JSON.**
The headline §S7.5b claim ($r = 0.90$, $n = 93$) is computed by `hydrograph_covariance.py` in the pairwise-fallback block but is not stored in `results/hydrography/four_drainage_covariance.json`, which records only the 3-gauge aligned (Mississippi/Yazoo/Tensas) matrix. The value is reproducible from the cached CSV but not directly readable from the JSON, which a reviewer auditing the artifacts may not realize.
- **Manuscript location:** §4.5; §S7.5b table.
- **Code/JSON location:** `scripts/analysis/hydrograph_covariance.py` script computes pairwise correlations to stdout; `results/hydrography/four_drainage_covariance.json` stores only the 3-gauge matrix.
- **Suggested fix:** Modify `hydrograph_covariance.py` to also write the pairwise overlaps (with their n-counts and r-values) into the JSON output. This is a code change rather than a manuscript change. See E5 below.

**I2. Near-threshold ablation invariance.**
The `near_threshold_ablation.json` shows that M_g and σ* are invariant across the σ sweep — every row has identical values. The "sweep" is a presentation device labeling 15 σ-points each with the same equilibrium answer. The §S7.7(4) text correctly explains this ("the equilibrium difference is therefore not a function of σ but of whether the apparatus is engaged at all"). The main-text framing is internally consistent. No edit required, but readers checking the JSON may be surprised that the rows are uniformly identical.

**I3. Internal consistency of σ*_blind across files.**
`restructured_saturation_test.json` (xi_X=0.0) and `near_threshold_ablation.json` both report sigma_star_blind = 0.5433. The manuscript reports 0.543 → "+36% upward shift" (§4.3). All three sources match.

---

## 7. Suggested Manuscript Edits

### E1. Fix §3.1 run-configuration (iii) [Critical]

**Current text (§3.1):**
> (iii) The §S3 sensitivity analyses run one-at-a-time parameter perturbations, ten replicates per perturbation, 100 simulated years per replicate, used to characterize the local sensitivity of $\sigma^*$ to each parameter.

**Replacement:**
> (iii) The §S3.1 OAT sensitivity table is produced by the deterministic `oat_sensitivity_table.py` analytical script: each parameter is perturbed by ±50% (or absolute, for $\varepsilon$ and $n_{agg}$) and $\sigma^*$ is recomputed via Brent's-method root-finding applied to the lambda-sigma fixed-point equilibrium. There are no stochastic replicates because $\sigma^*$ at fixed parameters is deterministic; the OAT table reports the analytical $\sigma^*$ swings directly.

This also requires editing the parallel statement in Data Availability under §S3.

### E2. Tighten cross-site Spearman bound [Warning]

**Current text (§4.5 Watson Brake paragraph; Conclusions; §5.6):**
> Spearman $\rho = +0.85$ to $+0.89$

**Replacement:**
> Spearman $\rho = +0.85$ to $+0.90$ (across the four pred-vs-observed combinations: static-ε vs ordinal scale = +0.85; phenology-ε vs ordinal = +0.88; static-ε vs volume = +0.88; phenology-ε vs volume = +0.90).

Or, retain the abbreviated form but use "+0.85 to +0.90" rather than "+0.85 to +0.89".

### E3. Correct k_0 swing rounding in §S3.1 table [Warning]

**Current text (§S3.1 table, k_0 row):**
> | $k_0$ (baseline degree) | $-50\%$ | 0.396 | $+50\%$ | 0.403 | $-0.003$ | $+0.003$ | 0.007 |

**Replacement:**
> | $k_0$ (baseline degree) | $-50\%$ | 0.396 | $+50\%$ | 0.403 | $-0.003$ | $+0.003$ | 0.006 |

(JSON value 0.00646 rounds to 0.006 at three decimals.)

### E4. Reword §S3 seed claim in Data Availability [Warning]

**Current text (Data Availability):**
> The §S3 sensitivity sweeps use `seed = 42` as the analytical model default and parameter-perturbation seeds documented in `scripts/sensitivity_analysis.py`.

**Replacement:**
> The §S3.1 OAT sensitivity table is fully deterministic (analytical $\sigma^*$ via `scripts/analysis/oat_sensitivity_table.py`) and requires no seeds. Stochastic figures elsewhere in §S3 use `seed = 42` as the default.

### E5. Code-side fix for hydrograph JSON (not a manuscript edit) [Info]

In `scripts/analysis/hydrograph_covariance.py`, augment the JSON output to record the pairwise correlations (including Bayou Maçon vs Tensas) with their n-counts. The current JSON only stores the 3-gauge aligned matrix; the 6 pairwise overlaps from the fallback block are computed but discarded. Adding them to the JSON would make the §S7.5b $r = 0.90$ headline value directly verifiable from results files alone.

---

## 8. Summary

| Severity | Count | Items |
|---|---|---|
| Critical | 1 | C1 (run-config (iii) mismatch) |
| Warning | 3 | W1 (Spearman upper bound), W2 (k_0 swing rounding), W3 (vacuous seed claim) |
| Info | 3 | I1 (BM-Tensas r in JSON), I2 (ablation invariance), I3 (σ*_blind consistency confirmed) |

All 9 spot-checks pass on numerical content. The fitness equation in §2.4 matches the code exactly. The convergence claim of 18 iterations is verified empirically. The recently-added extension scripts produce JSON outputs that match every numerical claim made about them in the manuscript, modulo a single rounding direction error (W2) and a slight understatement of the upper bound on cross-site Spearman ρ (W1). The single Critical issue (C1) is a description-of-method mismatch in the §3.1 run-configuration table that requires fixing the §3.1 prose and the parallel Data Availability statement.

The audit finds no scientific or computational errors in the recent extensions. All numerical claims in §4.5, §S7.7, §S7.5b, §S7.6, and §S3.1 are reproducible from the listed scripts and JSON files. The notation mapping is complete; there are no ghost variables. The model specification matches the code. The framework's threshold-prediction, regime-switching prediction, restructured-saturation prediction, and Bayesian-prior sensitivity all check out.
