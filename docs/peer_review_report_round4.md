# Peer Review Report: Round 4 (Re-Audit)

**Date:** 2026-05-02
**Manuscript:** docs/manuscript_AA/Poverty_Point_AA.md (~22,000 words; six implemented extensions)
**Target journal:** American Antiquity
**Prior reviews:** R1 (2026-03-21), R2 (2026-03-22), R3 (2026-05-01)

---

## Round 3 → Round 4 Trajectory

R4 implemented six of eight priority extensions plus the §S7.5b empirical hydrograph correction. The new headline statistic is Spearman ρ = +0.91 between joint M_g(ε_water-route, n_agg, α-labor-scaling) and observed monument volume across 11 LMV sites.

**Reproducibility:** Substantially improved. R3 had the manuscript-code mismatch (replicate counts, Figure 4 numbers, WB derivation, SD convention) flagged by all three reviewers. R4 resolved all of these per the methods-code-alignment audit (0 critical issues, 9/9 numerical spot-checks pass).

**Empirical content:** All three R4 reviewers identify a deeper concern: the magnitude-prediction defense now rests on stacked extensions, several of which have parameters fit to the same 11-site sample they predict. The Adversarial reviewer states the strongest version: the ρ = +0.91 is dominated by exogenous n_agg, with the framework's ε contributing essentially nothing to magnitude beyond what n_agg alone provides.

**Direct verification:** n_agg alone gives Spearman ρ = +0.87 against ordinal scale (p = 0.001) and ρ = +0.89 against observed volume (p < 0.001). The joint prediction's ρ = +0.91 represents at most a +0.02 to +0.04 marginal contribution from ε plus α-labor-scaling. The Adversarial reviewer's central concern is empirically correct.

---

## Synthesis

### Agreement (raised by 2 or more reviewers)

1. **The ρ = +0.91 result is dominated by exogenous n_agg.** All three reviewers raise this, with varying intensity. n_agg alone gives ρ = +0.87 to +0.89; the framework's ε adds little. The headline cannot be reported as if the framework predicts magnitude when the dominant predictor is supplied externally by Grooms et al. 2023 / Kidder and Grooms 2024.

2. **α = 2.0 was fit to minimize log-overprediction across the same 11 sites.** The supplement §S7.7 extension 2 explicitly says "the absolute calibration is closest at α ≈ 2.0." This is calibration on the test set. The absolute-volume agreement (all sites within ~3× of observed) is a fit, not a prediction.

3. **K = 3 / σ_sd = 0.10 is one cell in a swept hyperparameter table.** The WB closure (5,408 m³ within CI of 7,000 m³) holds at this cell; adjacent cells overshoot or undershoot by 10×. The K = 3 value is justified post-hoc by ethnographic timescales (Wiessner 2002; Kelly 2013) and by the same Saunders et al. 2005 inter-stage-gap evidence that already supports the bistable interpretation. Methods and Adversarial reviewers both flag this.

4. **ξ_X = 0.5 is selected for interpretive content, not derived from data.** The +37% threshold-shift result is invariant in ξ_X. The reframing from "removing one constant" to "genuine signaling-vs-cooperation discrimination" is real but does not constitute new evidence. Methods reviewer is most explicit: "the discrimination remains a within-model property of the equation set."

5. **Internal inconsistency between §5.1 and the abstract / Conclusions.** §5.1 consolidates the position that "the framework predicts threshold-crossing, not magnitude." The abstract leads with "calibrated to the type-site, the model reproduces earthwork volume to within an order of magnitude" and the Conclusions paragraph leads with "ρ = +0.85 to +0.90 between joint M_g(ε, n_agg) and ordinal monument scale." Domain and Adversarial reviewers both flag this.

6. **Sassaman discrimination softened in §5.2 vs §2.1.** §2.1 names the LA-EW transition as a discriminating observable; §5.2 returns to the "complementary frameworks" reading. Domain and Methods reviewers both flag.

7. **22,000 words is too long for AA.** AA articles run 8,000-15,000. Major cut required before submission. Domain reviewer is most specific (target 12,000-13,000), with concrete cuts identified.

8. **Falsification list (§5.6) is growing across rounds.** R3 had three "would not falsify" exclusions. R4 has same three plus the magnitude-conditional-on-n_agg exclusion. A framework whose "would not falsify" list grows is becoming less risky. Adversarial reviewer flags this most explicitly.

9. **No out-of-sample test of the magnitude prediction.** §5.4 names Stallings Island, Green River, Mulberry Creek with conditional placements but does not test. Adversarial and Domain reviewers both want this.

### Disagreements

- **Domain** reviewer is most positive about overall publication-readiness ("publishable in *AA* on the threshold + screening + paleoclimate-proximity claims"), with the magnitude apparatus needing reframing or trimming.
- **Methods** reviewer is most critical of the cumulative free-parameter problem ("six free parameters and one exogenous predictor against eleven data points"), recommends explicit comparison of with-extensions vs without.
- **Adversarial** reviewer is most critical of the ρ = +0.91 framing ("the framework has converted six identified gaps into six new free parameters, the cumulative effect of which is to recover quantitative confirmation against the same 11-site sample") and recommends out-of-sample testing.

These are not strict contradictions — they reflect different audiences in the AA reviewer pool. A regional-specialist reviewer will read closer to Domain reviewer; a methodological/theoretical reviewer will read closer to Methods or Adversarial reviewer. The revision must satisfy both.

### Must Fix (likely block publication if unaddressed)

1. **Reframe the magnitude-prediction story honestly.** The headline ρ = +0.91 is dominated by exogenous n_agg. Either (a) demote the joint prediction to "consistency check conditional on n_agg from independent sources" and report the partial-correlation analysis showing ε contributes ≤+0.04 marginal Spearman ρ; or (b) drop the joint prediction from the main text entirely and keep it as a §S7.7 sensitivity check. The abstract and Conclusions should not lead with the ρ = +0.91 result.

2. **Acknowledge α = 2.0 is fit, not derived.** State explicitly that the absolute-volume agreement is calibration to the cross-site magnitude data, not prediction. Either drop the absolute-volume claim or pre-register α from a non-LMV source and accept whatever the result is.

3. **Reframe the WB closure as a sensitivity check rather than a passed test.** The K = 3, σ_sd = 0.10 cell is one of seven swept configurations. Either commit to K and σ_sd from independent ethnographic and paleoclimate data and report whatever the prediction is, or report the (K, σ_sd) sensitivity surface and note that the framework is *consistent with* observed WB volume rather than *predicted* it.

4. **Cut the manuscript to 12,000-13,000 words.** AA editors will not work through 22,000 words. The cuts identified by the Domain reviewer (§2.4 fitness exposition to supplement; §4.2 archaeological calibration tightening; §4.3 ablation tightening; §4.5 split into shorter subsections; §5.5 limitations consolidation) absorb the necessary reduction.

5. **Fix the abstract.** Currently says "calibrated to the type-site, the model reproduces earthwork volume to within an order of magnitude." Calibration is the volume anchor, not a prediction. Replace with: "calibrated against the type-site core volume, the model predicts exotic abundance ordering by source distance (ρ = 0.95) and reproduces the pulsed construction tempo." Demote magnitude to a consistency check.

6. **Tighten §5.2 Sassaman paragraph to mirror §2.1.** Name the disagreement, identify the discriminating observable (LA-EW transition), report which way the current evidence cuts.

### Consider Addressing (would strengthen but not fatal)

7. **Add a small supplemental table** documenting per-site n_agg with source citation and the empirical basis (radiocarbon date count, material-class count, footprint-independent estimate). This addresses the circularity concern in extension 7.

8. **Add the "modern hydrograph as first-order proxy for paleo-discharge"** caveat to the abstract and §5.1 consolidated statement. §S7.5b already has it.

9. **Update Figure 7B caption** to lead with the three-independent-regimes claim rather than four canoe-accessible drainages.

10. **State which prior is the principled choice in the Bayesian §4.5.** The flat U[0.10, 0.50] is the natural least-informative prior given the disagreement in operationalizations; under that prior, P = 0.56 (slightly favoring above-threshold). The current presentation of three priors leaves the reader to choose.

11. **Add ξ_X = 0.5 sensitivity sweep to §S7.7** showing the ablation interpretive content as a function of ξ_X, with explicit acknowledgment that the discrimination claim requires ξ_X above some threshold not derived from data.

12. **Run an out-of-sample test** at one or more of the eastern Archaic comparators in §5.4 (Stallings Island, Green River, Mulberry Creek). The framework's predictions there are conditional placements; testing them gives genuine out-of-sample evidence.

13. **Compute partial Spearman ρ** holding n_agg fixed and varying only ε, to isolate the framework's marginal contribution to magnitude prediction.

### Revision Plan (priority order)

**Tier 1 (must fix before any submission):**
1. Compute and report partial-correlation analysis (ε vs n_agg contribution to ρ).
2. Reframe abstract and Conclusions to demote magnitude to consistency check.
3. Acknowledge α = 2.0 fit and rework §S7.7 extension 2 framing.
4. Reframe WB closure as sensitivity check.
5. Tighten §5.2 Sassaman to mirror §2.1.
6. Cut to 12,000-13,000 words.
7. Fix abstract phrase about reproducing earthwork volume.
8. Update §5.6 falsification list (don't grow further; tighten what would falsify).

**Tier 2 (recommended):**
9. Add hydrograph paleo caveat.
10. Update Figure 7B caption to three-regimes.
11. Name principled Bayesian prior.
12. ξ_X sensitivity sweep in §S7.7.
13. Per-site n_agg supplemental table.

**Tier 3 (would substantially strengthen, but heavier work):**
14. Out-of-sample test at Stallings Island, Green River, or Mulberry Creek.
15. Replace per-site n_agg with footprint-independent estimates.
16. Replace water-route access weights with DEM-derived routing.

---

## Domain Review (Round 4)

[Full review embedded; key findings:]

- Trajectory is upward across four rounds; current readiness is "publishable on the threshold + screening + paleoclimate-proximity claims"; magnitude apparatus needs reframing.
- New strengths: §S7.5b USGS gauge analysis (most important addition); extension 5 ξ_X restructuring; §5.4 conditional placements; PPO paragraph; §5.6 explicit list.
- Critical new weaknesses: compounding-extensions problem; tension between §5.1 and abstract/Conclusions; K = 3 selection undermines WB falsification structure; §5.2 retreats from §2.1 Sassaman discrimination; abstract is misleading on what framework predicts; modern-hydrograph caveat needed in abstract; extension 7 circularity concern; Figure 7B duplicates abandoned framing; 22,000 words too long.
- Length recommendation: 12,000-13,000 main-text words.

## Methods Review (Round 4)

[Full review embedded; key findings:]

- All R3 reproducibility issues addressed; equations match code; convergence claim verified.
- Critical new weaknesses: α = 2.0 is fit to minimize |mean log10(pred/obs)|; ρ = +0.91 driven by analyst-assigned n_agg (the "consistent with footprint scale" defaults are explicit fits to the dependent variable); ξ_X = 0.5 is selected for interpretive content; K = 3 yr persistence is not theoretically motivated; water-route access weights are author-specified; six free parameters and one exogenous predictor against 11 data points.
- Cumulative-extensions concern: extensions 1, 4, 6 are defensible operationalization; extensions 2, 5, 7 are calibration-fitting wearing the clothes of operationalization.
- Suggestions: report the framework's predictions without extensions alongside with-extensions; replace n_agg with footprint-independent estimates; tighten K and σ_sd from independent evidence.

## Adversarial Review (Round 4)

[Full review embedded; key findings:]

- The framework has converted six identified gaps into six new free parameters; the cumulative effect is to recover quantitative confirmation against the same 11-site sample.
- Critical new concerns: ρ = +0.91 is dominated by exogenous n_agg (verified empirically: n_agg alone gives ρ = +0.87 to +0.89); α = 2.0 is fit to monument scale; WB closure is one cell in a (σ_sd, K) sweep; ξ_X = 0.5 moves unfalsifiability one parameter to the right; water-route access weights are author-specified; six free parameters against 11 data points; "would not falsify" list growing across rounds.
- Strongest counterargument: "the framework has converted six identified gaps into six new free parameters, the cumulative effect of which is to recover quantitative confirmation against the same 11-site sample."
- Survival path: report the joint magnitude prediction as a *consistency demonstration* rather than a *test*.
- What would now falsify: above-threshold non-mound site at the same regional σ; monumental site at low ε_wr; out-of-sample magnitude failure at Stallings Island, Green River, or Mulberry Creek; threshold-vs-displacement collapse discrimination failure; paleo-discharge correlation matrix differing substantively from modern.

---

## Notes for the next revision

The R4 result is paradoxical: reproducibility is excellent, but the framework's quantitative claims have moved away from independent risk and toward extension-stacked confirmation. The honest version of this manuscript is the one that:

1. Leads with what the framework genuinely predicts: above-threshold ε is necessary for sustained aggregation; the binary screening discrimination of interior-vs-coastal sites passes; paleoclimate σ at PP is at-or-near threshold (P = 0.36-0.56 across plausible priors).

2. Demotes the magnitude apparatus to a consistency demonstration that requires (a) per-site n_agg from independent sources, (b) α from independent ethnographic data, (c) K and σ_sd from independent paleoclimate evidence, and acknowledges that under the current parameterization, the joint ρ ≈ +0.91 is dominated by n_agg variation that the framework does not predict from first principles.

3. Pre-registers an out-of-sample test (Stallings Island volume range, or Green River monument scale) that would carry independent evidential weight if it succeeds, and accept that failure would require revising the framework rather than awaiting Extension 3 or 8.

This honest version is shorter, less confident in places, and more compelling overall. It is also the version the R3 Adversarial reviewer recommended; R4 has clarified that recommendation rather than answered it.
