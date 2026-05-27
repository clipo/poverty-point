# Peer Review Report: Round 3 (Re-Audit)

**Date:** 2026-05-01
**Manuscript:** docs/manuscript_AA/Poverty_Point_AA.md (~19,000 words)
**Target journal:** American Antiquity
**Prior reviews:** Round 1 (docs/peer_review_report.md, 2026-03-21); Round 2 (docs/peer_review_report_round2.md, 2026-03-22)

---

## Round 2 → Round 3 Trajectory

| Metric | Round 2 | Round 3 |
|---|---|---|
| Round 2 "Must Fix" items addressed | — | 2 of 3 (f(n) ghost; 42%/34%) |
| Round 2 "Must Fix" items partially addressed | — | 1 of 3 (replicate count: shifted, not resolved) |
| Round 2 "Consider" items addressed | — | 6 of 8 |
| Round 2 "Consider" items not addressed | — | 2 of 8 (PPOs; intermediate-strategy bound) |
| New issues identified in Round 3 | — | 9 critical, multiple supporting |

**Trajectory:** Substantial improvement. The structural problems of Round 1 (calibration circularity, code-text mismatch) and the consistency problems of Round 2 (cost decomposition, ghost terms, ε ambiguity) are largely resolved. The remaining issues are of two kinds: (1) reproducibility-grade internal inconsistencies between the ODD spec, §4.2 results, Supplement §S4, and Figure 4, and (2) a deeper concern flagged most sharply by the Adversarial reviewer that the paper's quantitative apparatus has progressively narrowed to a single screening test plus a paleoclimate-proximity result, with each magnitude-prediction test reinterpreted as confirmation by a different route.

---

## Synthesis

### Agreement (raised by 2 or more reviewers)

1. **Replicate-count inconsistency.** Three versions of the calibrated PP scenario coexist: §3.1 ODD says "100 times for statistical robustness"; §4.2 / Figure 5 use 8 replicates × 200 years; Supplement §S4 reports 10 replicates × 500 years with different numbers. The §4.2 reported numbers correspond to `results/calibration_replicates/replicates_n8_d200.json` (Methods reviewer verified). Domain, Methods, and Adversarial all flag this. **Must Fix.**

2. **Figure 4 vs §4.1 prose number mismatches.** §4.1 narrative reports aggregation "jumps from about 4 to about 19 bands" and monument investment "from ~5,600 to ~30,300"; Figure 4 caption reports "from ~19 bands at low σ_eff to ~40 bands at high σ_eff" and "~8,400 to ~18,100." Strategy-dominance ranges and sign convention also disagree between prose and caption. Both Domain and Methods raise this. **Must Fix.**

3. **Watson Brake 30× overprediction reframing.** Domain reviewer reads the bistable reframing as a strong addition supported by three independent lines of evidence; Adversarial reads it as "the textbook unfalsifiable rescue" deferring miss to two not-yet-implemented extensions. Methods reviewer notes the 30× claim itself is asserted but not derived. The genuine disagreement is about framing: all three agree the calculation should be shown; the disagreement is whether the bistable reading should be presented as a successful prediction modulo extensions or as a hypothesis flagged for future testing.

4. **Magnitude prediction now untestable in the directions the paper presents.** Domain reviewer notes the framework's failure to predict cross-site magnitude is acknowledged in three separate places and should be consolidated. Adversarial reviewer escalates: every magnitude test (qualitative-Shannon ρ = 0.39 NS, phenology ρ = -0.21 NS, EPA L4 ρ = 0.07 NS) is reinterpreted as confirmation through the n_agg-rescue route, which the framework treats as exogenous. **Major reframing required.**

5. **Phenology-ε null result framing.** Methods reviewer praises honest reporting of the negative result; Domain reviewer says the §5.5 framing should be more direct; Adversarial reviewer reads the §S7.6 framing as post-hoc rescue ("if phenology had produced ρ = +0.7, the paper would be reporting it as confirmation; that it produces ρ = -0.21 is reported as confirmation by a different route"). All three agree the framing needs work. **Must Fix.**

6. **Sassaman 2005 engagement insufficient.** Domain reviewer: the "different register" framing leaves the discrimination between signaling and Sanger institutional-containment underdeveloped. Adversarial reviewer: more sharply, the framing converts Sassaman from an opponent into a friendly collaborator, which AA reviewers will not accept. Both want the framing replaced with explicit identification of where the threshold framework and Sassaman's structure-event-process make incompatible predictions.

### Disagreements

- **Overall readiness.** Domain reviewer: "ready for review at AA pending the new issues." Adversarial reviewer: "major revision" required to reframe magnitude/regional/comparative material as motivating questions for follow-up rather than current results. Methods reviewer: closer to Domain reviewer's assessment but flags substantial reproducibility cleanup before submission.
- **Watson Brake test.** Domain reviewer ranks it the "strongest single addition since Round 2." Adversarial reviewer treats it as the framework's central unfalsifiable-rescue example.
- These are not strict contradictions: Domain praises the self-criticism the framework now performs; Adversarial says the self-criticism still doesn't go far enough. Both readings are defensible. The author's call: how much of the magnitude apparatus to keep as "current evidence" vs. reframe as "future tests."

### Must Fix (likely block publication if unaddressed)

1. **Replicate-count inconsistency** across §3.1, §4.2, §S4, Figure 5 caption. Reconcile to a single configuration.
2. **Figure 4 vs §4.1 prose numbers** must match. Define strategy-dominance metric explicitly.
3. **WB 30× calculation** must be shown (model output → 210,000 m³ from ε=0.43, σ=0.56, n_agg=8).
4. **CITE-CHECK flag (line 262, Carleton et al.)** must be resolved; acknowledgments line 316 ("[To be added]") completed.
5. **PPO discussion** in §2.3: either bring PPOs into the index-signal frame or excise the implicit dismissal. PPOs are too central to the LMV record to be silent on.
6. **Bayesian ε-prior sensitivity** (§4.5): the ±0.2 prior centered on the qualitative rubric's 0.49 is informative; rerun with flat ε ∈ [0.10, 0.50] and report whether P(σ_eff > σ*) ≈ 0.25 is robust.
7. **SD reporting consistency** (§4.2 and Figure 5): manuscript reports ±19/82/96 for copper/steatite/galena; recomputation gives ±21/87/103. Reconcile or document the variance convention.

### Consider Addressing (would strengthen but not fatal)

8. **Phenology null result reframing** (§4.5, §5.5, §S7.6). Bracket as null evidence against the magnitude claim, OR state explicitly that the framework predicts magnitude only conditional on n_agg, which the paper does not predict.
9. **Magnitude-prediction position consolidated.** Replace dispersed acknowledgments with one paragraph stating the framework predicts threshold-crossing locations and tempo, not cross-site magnitude.
10. **Sassaman discrimination paragraph** (§5.2 or §2.1). Identify where the threshold framework and structure-event-process make incompatible predictions; the Late Archaic-Early Woodland transition is one candidate observable.
11. **Non-mound comparison sample** for the necessity-condition screening (§4.5). The "all interior monument-building sites pass the high-ε filter" result is sample-selected; either add a contemporaneous non-mound comparison sample or explicitly limit the screening claim.
12. **Four-drainage covariance claim** (§4.5, §5.1). At minimum cite published Mississippi/Yazoo/Tensas/Bayou-Maçon hydrograph evidence; if no source exists, frame as a hypothesis identified by the framework.
13. **Table 1 rubric in main text.** Move 1-2 worked example zone-access scorings from §S2.4 into the main text so AA reviewers can verify on the page.
14. **§5.4 broader-discipline expansion.** Name specific eastern Archaic comparators (Stallings Island, Green River, Mulberry Creek) and predict which the framework places above threshold.
15. **§S3.1 sensitivity tornado-plot table.** Add numerical Δσ* per parameter so readers don't need to consult Figure S1's image.
16. **Random-seed documentation** in Data Availability. Document the explicit seed list for the 8 calibration replicates.
17. **Near-threshold ablation sweep.** Run signal-conditional vs signal-blind across σ values straddling σ*, since the current PP-only comparison (σ - σ* ≈ 0.28) cannot discriminate by construction.

### Revision Plan (priority order)

**Tier 1 (must fix before any submission):**
1. Reconcile replicate counts across §3.1, §4.2, §S4, Figure 5 caption.
2. Reconcile Figure 4 prose vs caption numbers and define the strategy-dominance metric.
3. Show the WB 30× calculation explicitly in §4.5 or §S7.1.
4. Resolve the CITE-CHECK flag (Carleton et al.) and complete acknowledgments.
5. Recompute and report SD's consistently (sample vs. population convention).

**Tier 2 (must fix before AA-quality submission):**
6. Add PPO discussion paragraph in §2.3.
7. Run Bayesian ε-prior sensitivity (flat over [0.10, 0.50]) and report whether the ~25% above-threshold posterior is robust; soften the §4.5 inference if it drops.
8. Reframe phenology null result either as null evidence against magnitude OR as a refinement that establishes the framework's empirical commitment to threshold-crossing only, not magnitude.
9. Consolidate the magnitude-prediction position into a single paragraph.
10. Replace "different register" framing of Sassaman with explicit discrimination paragraph.

**Tier 3 (would strengthen the contribution):**
11. Add non-mound comparison sample for screening test (or explicitly bracket the claim).
12. Cite hydrograph evidence for the four-drainage covariance claim.
13. Move 1-2 worked rubric examples to main text.
14. Expand §5.4 with named eastern Archaic comparators.
15. Add sensitivity tornado-plot numerical table to §S3.1.
16. Document seed list in Data Availability or replicate JSON metadata.
17. Run near-threshold ablation sweep.

---

## Domain Review (Round 3)

### Summary Assessment

The manuscript argues that Poverty Point's monuments and exotic-goods accumulation are consistent with an aggregation-based costly-signaling system operating above a critical environmental-uncertainty threshold modulated by multi-drainage shortfall buffering (ε). The central contribution is a structural complement to the Sanger / Kidder & Grooms / Sassaman cultural-historical accounts: a quantitative threshold framework that predicts where, when, and at what tempo monument construction should appear under specified ecological conditions, and that integrates the Watson Brake-to-Poverty-Point trajectory as bistable-vs-above-threshold cases of the same model. The trajectory across three rounds is genuinely strong: Round 1's structural problems are resolved; Round 2's consistency problems are now substantially cleaned up; the Round 3 manuscript is internally coherent, honest about its limits, and reads as ready for review at AA pending the new issues below.

### Round 2 Issue Tracking (selected items; full text available)

- **f(n) ghost term:** Addressed.
- **42%/34% inconsistency:** Addressed.
- **100 replicates claim:** Partially addressed (new inconsistency; see new weakness #1).
- **ε = 0.40 vs 0.35:** Addressed.
- **Cross-cultural statistics caveat:** Addressed (cross-cultural validation removed from AA version).
- **Layers 2-3 ornamental:** Partially addressed (now openly acknowledged but residual structural concern remains).
- **Convergence diagnostics:** Addressed.
- **Occupation span ambiguity:** Addressed.
- **PPOs as index signals:** Not addressed.
- **Intermediate strategy bound:** Partially addressed (limitation flagged, no quantitative bound).
- **Distance-decay constant fitted vs. assumed:** Partially addressed.

### New Strengths (R3)

- **Watson Brake test (§4.5)** is the strongest single addition; reframing as near-threshold bistable is supported by three independent lines of evidence.
- **Index vs. handicap distinction** made operative in §2.3.
- **Signal half-life argument (§2.3)** is a genuine theoretical contribution.
- **Honest framing of magnitude predictions** (§4.5, "What the framework actually predicts about magnitude").
- **Threshold-vs-displacement collapse discrimination (§5.3)** offers a sharp empirical test for future Bayesian dating.
- **Convergence-vs-diffusion discrimination (§5.2)** correctly calibrated; not overclaiming Grooms et al. 2023.

### New Weaknesses (R3)

1. **Replicate-count inconsistency between methods and results (§3.1 vs §4.2).**
2. **Inconsistency between Figure 4 and §4.1 narrative.**
3. **Strategy-dominance sign convention is unclear (§4.1, Figure 4).**
4. **Table 1 zone-weighting rubric is not visible in main text.**
5. **The "four canoe-accessible drainages" claim is asserted but not measured.**
6. **The phenology refinement undermines its own role (§5.5).**
7. **Section 5.4 hunter-gatherer-archaeology framing is thin.**
8. **Sanger 2023, 2024 engagement is fair but underdeveloped.**
9. **Acknowledgments and reference completeness** (CITE-CHECK flag, "[To be added]").

---

## Methods Review (Round 3)

### Summary Assessment

The methods are now well-aligned with the code in their most critical respect: the f(n) ghost term flagged in Round 2 has been removed from the AA fitness equation, the three coupled signaling rules are implemented in `integrated_simulation.py` exactly as §S1.6 specifies, and convergence diagnostics are now reported. What remains are reproducibility-style internal inconsistencies (replicate counts, simulation duration, three different versions of the "calibrated PP scenario") and a handful of small numerical mismatches between figure captions and the prose. None is fatal individually, but cumulatively they erode a reader's trust that the paper knows which run produced which number.

### Round 2 Issue Tracking

- **f(n) ghost term:** Addressed (verified against signaling_core.py:567-612).
- **42% vs 34%:** Addressed.
- **100 replicates claim:** Partially addressed; ODD spec still says 500 years × 100 replicates while §4.2 uses 8 × 200 and Supplement §S4 uses 10 × 500.
- **ε = 0.40 vs 0.35:** Resolved as methodological choice.
- **Cross-cultural statistics:** Addressed.
- **Layers 2-3 ornamental:** Addressed (honestly framed).
- **Convergence diagnostics:** Addressed.
- **Occupation span:** Mostly addressed.
- **PPOs as index signals:** Not visibly addressed.
- **Intermediate strategy bound:** Not addressed.
- **Distance-decay length scale:** Partially addressed.

### New Strengths (R3)

- **§S7.6 phenology test reports null result honestly** (verified ρ = -0.21 vs +0.39 in JSON).
- **Bayesian §4.5 framing internally consistent.**
- **Three signal-conditional rules implemented in code** (verified in integrated_simulation.py).
- **GIS-ε results match JSON outputs.**
- **Per-material exotic counts match the JSON output.**

### New Weaknesses (R3)

1. **Three different versions of the calibrated PP scenario coexist.**
2. **Figure 4 caption reports different ranges than text §4.1 prose.**
3. **The 30× WB volume overprediction claim is asserted, not derived.**
4. **Bayesian ε prior is informative without justification** (centered on 0.49 with ±0.2; would benefit from flat-prior sensitivity check).
5. **Sensitivity-analysis tornado plot referenced but not characterized numerically.**
6. **Random-seed strategy claim in Data Availability is imprecise.**
7. **§4.1 prose vs Figure 4 numerical discrepancy (96% independent claim).**
8. **Standard-deviation reporting inconsistent with stored data by ~10%** (sample vs. population convention).

### Suggestions

1. Run Bayesian §4.5 propagation with less informative ε prior; report robustness.
2. Reconcile the three replicate-count specifications.
3. Show WB 30× calculation explicitly.
4. Add tornado-plot numerical table to §S3.1.
5. Document seed list.
6. Reconcile Figure 4 prose-vs-caption.
7. Run signal-conditional vs signal-blind ablation at near-threshold parameters.
8. Provide 2-3 example replicate trajectories in supplementary material.

---

## Adversarial Review (Round 3)

### Summary Assessment

The manuscript is genuinely improved across rounds: the egregious calibration circularity, equation-code mismatch, and unsupported collapse mechanism of Round 1 are gone, and Round 2's parameter consistency issues are resolved. What remains, however, is a deeper problem the consistency editing has actually made more visible: the framework's *quantitative* claims have been progressively narrowed to a single screening test (PP vs. coastal pair) and a posterior-predictive copper count, while every other quantitative test now resolves to "consistent with the framework once X extension is added" or "null result, but the framework predicts that anyway." The paper is now most convincing where it derives a phase transition and uses paleoclimate independently of archaeology, and least convincing where it explains why six different operationalizations of the magnitude prediction all fail to track observed monument scale.

### Round 2 Issue Tracking

- **R2 #1 (f(n)):** Addressed.
- **R2 #2 (42%/34%):** Addressed.
- **R2 #3 (100 replicates):** Partially.
- **R2 #4 (ε 0.40 vs 0.35):** Addressed.
- **R2 #5 (cross-cultural):** N/A (removed; trajectory of contracting predictive scope).
- **R2 #6 (Layers 2-3):** Partially (honestly conceded; concession does not so much resolve as confirm).
- **R2 #7 (convergence diagnostics):** Addressed.
- **R2 #8 (occupation span):** Partially.
- **R2 #9 (PPOs):** Not.
- **R2 #10 (intermediate strategy):** Not.
- **R2 #11 (distance-decay constant):** Partially.

### Critical Concerns (R3)

1. **The framework's magnitude prediction is now untestable in any version where it is allowed to be wrong.** Three magnitude tests, all null, each interpreted as confirmation through n_agg rescue. The framework's positive content reduces to "above-threshold ε is necessary, and PP achieved larger n_agg for reasons the framework does not specify."

2. **The Watson Brake bistable reframing is the textbook unfalsifiable rescue.** 30× miss → reframe as near-threshold bistable → defer to two not-yet-implemented extensions. §5.6 explicitly says magnitude mismatch at a single LMV site need not falsify, which is preemptive concession of a falsification opportunity.

3. **The "all interior monument-building sites pass the high-ε filter" screening claim is endogenous to sample selection.** Sample is mound-building sites; non-mound contemporaneous LMV occupations are silently excluded. If they also pass the filter, the screening is uninformative.

4. **Coordinate corrections weakened the GIS results.** Under L4, PP is not the most ecologically diverse interior site. The paper's defense (PP's distinguishing feature is confluence position, requiring an unimplemented water-route operationalization) is the third claim deferred to priority extensions.

5. **Phenology-ε null result is not "graceful" — it is a refinement that contradicts what the framework promised.** Phenology was introduced to show better alignment; instead it shows worse. The §4.5 framing ("confirms scale not determined by ε alone") is post-hoc.

6. **The Sassaman-aligned reviewer's objection has not been engaged.** The "different register" framing converts Sassaman from an opponent into a collaborator. AA reviewers will not accept this.

7. **The "one-directional flow" signature is the only genuinely discriminating prediction, and the paper concedes it cannot test it with current data.**

### Strongest Counterargument

A hostile AA reviewer would write: *"The authors have produced a highly elaborated agent-based formalization providing one positive result (paleoclimate σ at or above threshold with ~25% joint-posterior support) and one screening discrimination (interior vs. coastal). Every other quantitative test resolves to a null result reframed as confirmation: distance-decay matches but cannot discriminate signaling; cross-LMV magnitude prediction fails under three operationalizations and is rescued by exogenous n_agg; Watson Brake overshoots by 30× and is rescued by two not-yet-implemented extensions; signaling-vs-cooperation ablation reduces to 'removing one asserted constant.' The contribution is a theoretical apparatus and a paleoclimate cross-check, dressed in the rhetoric of a quantitatively validated regional model. AA's LMV readership will not accept this framing: Sassaman (2005) argues directly against the explanatory adequacy of structural conditions, and the paper's response — that Sassaman operates on 'a different register' — does not engage the actual claim. I recommend major revision in which the magnitude-prediction material, the cross-LMV regional hierarchy claim, and the Watson Brake test are reframed as motivating questions for follow-up rather than as current results."*

**Can the paper survive this objection?** Partially. The phase transition derivation, the index-signal interpretation (especially the signal half-life argument), and the paleoclimate-threshold proximity result are real and survive. The framework's qualitative reading is defensible if the paper restricts its claims to those pillars plus a screening comparison with an honest non-mound-building sample. What the paper cannot survive in its current form is the rhetorical gap between the elaborate quantitative apparatus and the actual evidentiary content.

---

## Notes for the next revision

1. The trajectory across three rounds is genuinely upward: Round 1 had structural circularities, Round 2 had consistency issues, Round 3 has reproducibility cleanup and a framing question. The framing question (how much regional/magnitude apparatus to keep as "current evidence" vs. reframe as "future tests") is the central editorial choice for the next revision.

2. Domain reviewer's "ready for review" assessment and Adversarial reviewer's "major revision" assessment are not strictly contradictory: they reflect different audiences in the AA reviewer pool. A regional-LMV reviewer focused on the case study will read closer to Domain reviewer; a theoretical/methodological reviewer with cross-disciplinary perspective will read closer to Adversarial reviewer. Both readings are likely from AA's actual reviewer pool. The revision should aim to satisfy both: tighten reproducibility for the regional reviewer (Tier 1 fixes), bracket the magnitude apparatus for the methodological reviewer (Tier 2 reframings).

3. The Watson Brake test and the phenology refinement are the two most ambivalent items. Both are genuine intellectual additions; both can be read as either confirming or disconfirming the framework. The honest revision identifies under what conditions each would discriminate the framework from alternatives, and brackets the current results accordingly.
