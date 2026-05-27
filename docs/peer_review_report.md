# Peer Review Report: Poverty Point JAS Manuscript

**Date:** 2026-03-22
**Journal:** Journal of Archaeological Science (JAS)
**Reviewers:** Domain Expert, Methods Expert, Adversarial (simulated)

---

## Reviewer 1: Domain Expert

### Summary Assessment

This manuscript presents an ambitious and formally rigorous application of multilevel selection and costly signaling theory to the Poverty Point archaeological record. The core argument is coherent and well-motivated, and the agent-based model provides a useful formalization. However, the manuscript contains several instances where parameter choices are presented with greater confidence than the underlying evidence warrants, where the model's internal circularity limits its evidentiary force, and where important alternative interpretations are inadequately engaged.

### Strengths

- Formal derivation of the aggregation-signaling threshold (Section 2.4-2.8) is well-executed; the worked example effectively communicates the crossover logic
- Honest signal mechanism for monuments (Section 2.3): the argument that basket-load earth-moving is observable, unfakeable, and inherently cooperative is the strongest part of the framework
- Ecotone advantage formalization (Section 2.6) is a genuine theoretical contribution
- Treatment of PPOs (Section 2.3) demonstrates careful engagement rather than forcing all material culture into the signaling framework
- Paleoclimate proxy validation (Section 4.7) constitutes a genuine out-of-sample test
- Testable predictions (Section 5.8) are specific and falsifiable

### Weaknesses

1. **Circularity in archaeological calibration (Section 4.5):** Scaling factor is derived from the same data it claims to predict. Cross-scenario consistency is tautological. Category (c). Fix: anchor on one quantity, predict a second independently.

2. **Parameter estimation confidence exceeds evidence (Section 2.5):** Mapping from ethnographic ranges to specific parameter values (beta_ind = 0.90 from Kelly 2013 mortality data) is not shown mathematically. Category (b). Fix: show explicit derivation steps, acknowledge plausible ranges.

3. **Fitness functions in manuscript vs. code do not match (Sections 2.4 vs. signaling_core.py):** The manuscript presents exponential survival with f(n) cooperation; the code implements linear survival with network-derived vulnerability, no f(n), and a multi-layer signaling framework. Category (a). Fix: reconcile.

4. **Ecotone advantage parameter inconsistency (Sections 2.6 vs. 3.5):** epsilon = 0.35 in theory, 0.40 in Poverty Point scenario. Fix: standardize.

5. **Insufficient engagement with Kidder and Grooms (2025) revitalization framework.** Single-sentence dismissal is inadequate for the most recent major treatment. Category (b). Fix: expand comparison in Section 5.6.

6. **Cross-cultural validation sample too small and partially non-independent.** Three of five cases share regional paleoclimate. Rapa Nui is a training case. Category (c). Fix: acknowledge non-independence, report out-of-sample subset.

7. **Model omits within-aggregation conflict and disease.** These are central to the aggregation decision, not minor oversights. Category (b). Fix: back-of-envelope calculation for disease cost impact on threshold.

8. **Construction pulse correlation untested (Section 4.6).** Claim that pulses correlate with environmental stress is not tested against chronological data. Category (c). Fix: test or frame as prediction.

9. **Collapse mechanism contradicts model math (Section 5.5).** "Too much uncertainty" mechanism is not in the model, which predicts monotonically increasing aggregation above threshold. Category (a). Fix: add formal upper bound or remove claim.

10. **Occupation span inconsistency:** 600 years, 500 years, and 400 years used in different contexts without reconciliation. Category (a). Fix: standardize.

### Suggestions

1. Expand sensitivity analysis to all key parameters (tornado plot)
2. Present actual model equations from code (or reconcile)
3. Add model verification section
4. Clarify handicap vs. index signals distinction
5. Address absence of storage evidence at Poverty Point
6. Engage Sassaman (2005) "event" framing more substantively
7. Report confidence intervals from replicates
8. Discuss semi-permanent occupation possibility
9. Fix figure numbering inconsistencies (Figure 4 -> Figure_5_model_architecture.png)

---

## Reviewer 2: Methods Expert

### Summary Assessment

The manuscript presents a multilevel selection model that is theoretically motivated and computationally implemented. However, a substantial gap exists between the fitness functions described in the manuscript (Section 2.4) and those actually implemented in the code (signaling_core.py). This discrepancy means the equations the reader encounters are not the equations generating results, undermining reproducibility.

### Strengths

- ABM is appropriate for this problem (emergent dynamics, path dependence, spatial heterogeneity)
- Theoretically grounded fitness functions from Grafen (1990) signaling game theory
- Lambda-sigma feedback loop is a genuine methodological contribution
- Brent's method for threshold identification is mathematically appropriate
- Multi-layer model architecture provides mechanistic depth
- Paleoclimate proxy calibration uses genuinely independent data

### Weaknesses

1. **Manuscript fitness functions do not match code (category: wrong).** Manuscript: exponential survival with f(n) cooperation. Code: linear survival, no f(n), network-derived vulnerability, conflict mortality term, signaling benefit B(lambda). These have qualitatively different behavior. Fix: reconcile and re-verify all numerical results.

2. **Vulnerability parameters are endogenous in code, fixed in manuscript (category: wrong).** Code derives alpha(k) = 1/(1 + gamma*k); manuscript presents alpha = 0.40 as ethnographically justified constant. Fix: describe network derivation in methods.

3. **Simulation duration mismatch (category: wrong).** Manuscript says 500 years; code defaults to 600 years with 100-year burn-in. Fix: state explicitly.

4. **Shortfall generation differs between engines (category: wrong).** core_simulation.py makes frequency sigma-dependent; integrated_simulation.py uses fixed scenarios. Fix: clarify which engine produced results.

5. **Cross-cultural validation statistical issues (category: unsupported).** Rapa Nui is a training case; null hypothesis unspecified; 5 cases provide minimal power. Fix: acknowledge, reframe as "consistent with."

6. **Replication protocol overstated (category: unsupported).** Manuscript claims 100 replicates; analysis scripts use 3-5. Fix: report actual numbers.

7. **Sensitivity analysis incomplete (category: plausible but not demonstrated).** Two-parameter OAT analysis across 15+ free parameters. Fix: Morris screening or systematic OAT of all parameters.

8. **Calibration is unit conversion, not validation (category: plausible but not demonstrated).** Fix: reframe; test parameter-free derived quantities (e.g., exotic/monument ratio).

9. **Ecotone advantage lacks independent estimation (category: unsupported).** Fix: compute GIS-based diversity index or clearly present as free parameter with sensitivity.

10. **No convergence diagnostics for lambda-sigma loop (category: plausible but not demonstrated).** Fix: report iteration counts, convergence rates, failure handling.

### Suggestions

1. Reconcile manuscript equations and code (highest priority)
2. Add analytical benchmark comparison
3. Report ODD protocol or equivalent
4. Provide code versioning (Zenodo DOI, requirements file)
5. Consolidate simulation engines
6. Add cross-correlation test for construction pulses vs. shortfalls
7. Justify or sensitivity-test monument depreciation rate (delta = 0.08)

---

## Reviewer 3: Adversarial (Devil's Advocate)

### Summary Assessment

The paper attempts something genuinely ambitious. It is most convincing when demonstrating that Late Archaic environmental conditions fall within the predicted parameter space and when showing that co-occurring monuments and exotics follow from signaling theory. It is least convincing in its claims of archaeological calibration, where apparent quantitative rigor obscures fundamental circularity, and in the relationship between the analytical model (Section 2) and the ABM (Section 3), which appear to be different models wearing the same notation.

### Critical Concerns

1. **Calibration is circular by construction.** Dividing target by output to derive a scaling factor, then presenting the match as evidence, is algebraic identity. The exotic goods comparison misses by a factor of 1.6x under the calibrated scenario. Fix: execute at least one prediction not derived from calibration data (distance-decay ratios are the strongest candidate).

2. **Analytical model and ABM are not the same model.** The multi-layer framework in signaling_core.py bears little resemblance to the Section 2 equations. Fix: demonstrate formal reduction or present ABM as an extension with ablation tests.

3. **Ecotone advantage is asserted, not demonstrated.** No quantitative evidence that Poverty Point's resource streams exhibit negative covariance, that variance reduction is 35-40%, or that Poverty Point is unusual in ecotone access. If epsilon = 0.20 instead of 0.35, the model predicts no aggregation. Fix: GIS analysis or acknowledge as hypothesis.

4. **Vulnerability ratio does the heavy lifting without independent justification.** beta_ind/alpha_agg = 2.25 determines the threshold; it was set with knowledge of the target. Fix: derive from network dynamics or conduct full sensitivity analysis.

5. **Cross-cultural validation conflates sample selection with prediction.** Rapa Nui is a training case; 3 of 5 sites share regional paleoclimate. 100% accuracy on 5 non-independent cases is not meaningful. Fix: acknowledge limitations, provide sigma derivations for all cases.

6. **Collapse mechanism is underspecified and potentially contradictory.** The model predicts monotonically increasing aggregation above threshold; "too much uncertainty" collapse is not in the math. Fix: add formal upper bound or restrict to sigma-decline mechanism.

7. **Seasonal aggregation is assumed, not explained.** The model compares aggregation against independence but omits intermediate strategies (bilateral exchange partnerships at 10-15% cost). If such strategies exist, aggregation's 42% cost may not dominate. Fix: add third strategy or argue why intermediate is not viable.

### Strongest Counterargument

The model's quantitative predictions are not independent of the data they claim to explain, and the qualitative predictions are not unique to the costly signaling framework. Every competing explanation also predicts monumentality, exotics, site hierarchy, and abandonment. The formal derivation depends on parameters selected with knowledge of the target. Strip away the mathematics and the argument reduces to: "if uncertainty is high enough and ecotone access is good enough, cooperation pays off and costly signals stabilize it." This is plausible but not distinguishable from "if resources are concentrated enough, aggregation occurs and social mechanisms stabilize it."

The paper can survive this objection only by shifting emphasis from post-hoc calibration to the genuinely distinguishing predictions already identified (distance-decay, ecotone-hierarchy, construction-paleoclimate correlation). Executing one or two of these would convert the framework from plausible narrative into empirically tested model.

---

## Synthesis

### Agreement (raised by 2+ reviewers, highest priority)

1. **Manuscript equations ≠ code equations** (all 3 reviewers). The most critical issue. The exponential-survival, f(n)-cooperation model in Section 2 is not what the code runs. This must be reconciled before anything else.

2. **Calibration circularity** (all 3 reviewers). Monument volume calibration is unit conversion, not validation. The exotic goods prediction misses by 1.6x. At least one genuinely independent prediction must be executed.

3. **Ecotone advantage lacks empirical grounding** (all 3 reviewers). epsilon = 0.35-0.40 is asserted without quantitative evidence. The entire argument is sensitive to this parameter.

4. **Cross-cultural validation is weak** (all 3 reviewers). Too few cases, non-independent, Rapa Nui is a training case. Must be reframed.

5. **Collapse mechanism contradicts model math** (domain + adversarial). "Too much uncertainty" is not predicted by the model. Must be formalized or removed.

6. **Parameter estimation overconfident** (domain + adversarial). Vulnerability ratio, cooperation parameters presented with false precision. Sensitivity analysis needed.

### Disagreements

- None of substance. All three reviewers converge on the same core issues from different angles.

### "Must Fix" (would likely block publication)

1. Reconcile manuscript equations with code implementation
2. Fix calibration framing (reframe as unit conversion + execute one independent prediction)
3. Resolve collapse mechanism contradiction
4. Fix internal inconsistencies (epsilon, simulation duration, occupation span)
5. Report actual replication counts, not claimed ones

### "Consider Addressing" (would strengthen but not fatal)

1. GIS-based ecotone diversity index for Poverty Point vs. comparanda
2. Expanded sensitivity analysis (all key parameters)
3. Third strategy (low-cost bilateral cooperation) to test aggregation dominance
4. Substantive engagement with Kidder & Grooms 2025 revitalization framework
5. ODD protocol or equivalent for ABM description
6. Disease/conflict costs in aggregation fitness
7. Construction pulse correlation test
8. Code versioning with Zenodo DOI

### Revision Plan (priority order)

1. **Reconcile equations and code.** Either update manuscript to describe the actual multi-layer model, or simplify the code to match the manuscript equations and re-run. This is prerequisite for all other fixes.

2. **Execute one independent quantitative test.** The distance-decay prediction (exotic material ratios from Webb 1968 inventory vs. exp(-d/500)) is the strongest candidate. Report R-squared, fitted decay constant, and whether 500 km was assumed or estimated.

3. **Formalize or remove collapse mechanism.** Either add an upper sigma bound where aggregation fails (e.g., travel becomes impossible) or restrict collapse to sigma-decline and acknowledge the Kidder 2006 landscape instability evidence is inconsistent.

4. **Fix internal inconsistencies.** Standardize epsilon (0.35 or 0.40), simulation duration (600 years with 100-year burn-in), and occupation span across all sections.

5. **Expand sensitivity analysis.** At minimum: gamma, delta, all cost parameters, vulnerability ratio. Tornado plot showing threshold sensitivity to each.

6. **Reframe calibration and cross-cultural validation.** Calibration is unit conversion. Cross-cultural test is illustrative, not statistically rigorous. Rapa Nui is a training case.

7. **Engage Kidder & Grooms 2025 substantively.** Dedicated comparison paragraph in Section 5.6 specifying where frameworks agree and disagree empirically.

8. **Compute ecotone diversity index.** GIS analysis of zone count/heterogeneity at Poverty Point vs. 2-3 comparison sites would convert epsilon from assertion to estimate.
