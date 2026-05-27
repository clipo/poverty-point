# Peer Review Report: Round 2 (Re-Audit)

**Date:** 2026-03-22
**Prior review:** 2026-03-22 (docs/peer_review_report.md)

---

## Round 1 vs Round 2 Summary

| Metric | Round 1 | Round 2 |
|--------|---------|---------|
| Prior issues fully addressed | - | 16 of 27 |
| Prior issues partially addressed | - | 9 of 27 |
| Prior issues not addressed | - | 0 of 27 |
| New issues identified | 27 | 11 |

**Overall trajectory: Substantial improvement.** The three most critical Round 1 issues (manuscript-code mismatch, calibration circularity, collapse contradiction) are resolved. The manuscript is now internally consistent where it was previously contradictory.

---

## Remaining Issues (Priority Order)

### Must Fix

1. **f(n) ghost term in Section 4.3.** The manuscript references f(n) = 1 + b*ln(n) as a cooperation-benefit function, but this does not exist in signaling_core.py. The n_agg parameter is accepted but unused in the fitness function. Either add f(n) to the code or remove all references from the manuscript. (Methods reviewer)

2. **42% vs 34% cost inconsistency.** Section 2.4 derives C_total = 34% (4% travel + 18% signal + 12% opportunity at 100km). But Sections 2.8, 4.1, and 5.8 repeatedly cite "42% of resources." Either derive 42% explicitly or fix all references to 34%. (Adversarial reviewer)

3. **100 replicates claim in Section 4.1.** Section 3.6 correctly states 3-5 replicates. Section 4.1 still says "Across 100 replicate simulations." These contradict each other. (Methods + Adversarial reviewers)

4. **epsilon 0.40 in scenario code vs 0.35 in manuscript.** The Poverty Point scenario in environmental_scenarios.py uses expected_epsilon=0.40. All manuscript text uses 0.35. If results were generated at 0.40, the reported numbers correspond to a parameterization the manuscript doesn't describe. (Adversarial reviewer)

### Should Fix

5. **Cross-cultural statistics misleading at point of use.** Section 4.7 reports p=0.03 and Cohen's d=1.76 without caveat about non-independence. The limitations section has the caveat but it's too late. Add parenthetical at point of use. (Domain reviewer)

6. **Layers 2-3 are ornamental for threshold.** Sensitivity analysis shows lambda_C and lambda_X have zero effect on sigma*. The multi-layer architecture doesn't affect the primary prediction. Manuscript should address whether these layers affect other outputs. (Methods reviewer)

7. **Convergence diagnostics still unreported.** Lambda-sigma loop convergence rates, iteration counts, and failure handling are not reported. (Methods reviewer)

8. **Occupation span ambiguity.** Abstract says "500-year," Introduction says "400-year," Section 5.5 says "500-600 years." Need one clear statement relating these three numbers. (Domain reviewer)

### Consider Addressing

9. **PPOs may qualify as index signals.** Section 2.3 dismisses PPOs because of low cost, but the paper elsewhere champions index signals (reliable because of physical constraints, not costliness). PPO geographic patterning makes them informative about group identity regardless of production cost. (Domain reviewer)

10. **Intermediate strategy not analytically bounded.** The bilateral exchange strategy at 10-15% cost is acknowledged but not tested even with a back-of-envelope calculation. (Adversarial reviewer)

11. **Distance-decay test assumes rather than estimates decay constant.** lambda=500 km was assumed, not fitted. A genuine test would estimate lambda from the data. (Adversarial reviewer)

---

## Synthesis

The revised manuscript has resolved the fundamental structural problems identified in Round 1. The equations now match the code. The calibration is honestly framed. The collapse mechanism is consistent with the model math. The parameter values are internally consistent. The epistemological framing is clear and defensible.

The remaining issues are primarily consistency problems (42% vs 34%, 100 vs 3-5 replicates, epsilon 0.40 vs 0.35, f(n) ghost term) rather than structural flaws. These are fixable in a single editing pass. The deeper methodological questions (Layers 2-3 being ornamental, ecotone advantage ungrounded, intermediate strategy untested) are legitimate limitations that are now honestly acknowledged in the manuscript rather than hidden.

The paper is approaching submission readiness. Items 1-4 are blocking; items 5-8 would strengthen the paper; items 9-11 would address sophisticated reviewer concerns but are not essential.
