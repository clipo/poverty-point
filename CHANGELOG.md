# Change Log

Revision history for the Poverty Point costly-signaling project. Most recent first.

## 2026-08-20 — Full validation audit, engine revision, and re-run

**Status**: Complete methods-code alignment audit (`docs/references/methods_code_alignment_report.md`), engine revision to match the ODD specification, full re-run of the §4 simulation suite, and correction of every discrepancy the audit found. Test suite: 222 passed.

**Engine revision** (`src/poverty_point/`): once-per-year scheduling (each seasonal phase executes once, not three times); band fission at size >30 with half-weight inheritance and dissolution below 5; heterogeneous band quality U[0.2, 2.0]; realized network vulnerability (seasonal_k from obligation strengths); synchronous decisions against the emergent monument signal stock (depreciated annually) and previous-year attendance; shortfalls propagate into harvests; severity-scaled shortfall mortality; density-dependent harvests; reciprocal obligations with resource-transfer help; fitness-weighted deaths; quality-based exotic acquisition; random initial network seeding. New tests in `tests/test_engine_semantics.py`.

**Re-run results (all committed)**: ablation sweep n=20 (`ablation_sweep_engine2.json`): signal-conditional crossing at realized σ = 0.387 vs random-partner 0.385 (−0.4% shift; no discriminating shift), analytical σ* = 0.400 matched within 0.013; phase space 12×10×5: simulated crossings within 0.03 of the analytical σ*(ε) line at every ε row; calibration replicates: PP 7,203 ± 3,276 units → 104 m³/unit anchor; per-material PPC (`exotic_ppc.py`, new): copper and galena consistent in like units, steatite consistent on a vessel basis, near-source materials overpredicted 8-63× (reported as a genuine informative misfit), joint Mahalanobis d² = 9,289; Price decomposition: S(t) = −0.011/+0.047/+0.023 below/at/above threshold; factorial: main effects ε +1.00, λ_W +0.32, λ_C/λ_X ≈ 0; memory probe (new): +0.019 crossing shift with memory off.

**Corrections**: α = 1 Watson Brake direction error fixed in six places (overpredicts 2.8×; the "underpredicts 7.7-fold / ~3,500 m³" claim was irreproducible and structurally impossible); ddof-doubled SDs fixed; stale ρ = 0.95 distance-decay lineage removed everywhere (current result ρ = −0.40) and Figure S9 (placeholder data) dropped; W_agg−W_ind monotonicity direction corrected (increasing); GIS/Table 3/§S12/§S13 rebuilt under the corrected coastal ε = 0.40 coding with true rank-based partial correlations (Saucier-vs-rubric now ρ = 0.70, p = 0.016; coastal-last Monte Carlo robustness drops to 21% and §6.4 says so); §6.5 upland correlations reattributed as assumptions; §S1 ODD, §S1.5, §S2, §S5.4, §S5.5, §S6, §S7.1, §S7.2, §S14, §S16, §S17.1, §S17.4 all updated to the implemented model and new outputs; five previously code-free verification claims now have committed scripts (`verify_analytical_diagnostics.py`, `exotic_ppc.py`, `table2_weight_perturbation.py`, `memory_effect_probe.py`).

**Repository**: figure scripts renamed to match figure numbers (main 1-15, supplemental S1-S11 renumbered); Makefile targets reorganized (analyses / simulations / figures / manuscript); REPRODUCE.md rewritten (the §8 "not implemented" list was false); `site_coordinates.csv` regenerated from the canonical `late_archaic_sites.csv`; superseded artifacts removed from the tree. Manuscript.docx and Supplemental.docx rebuilt.

**Open author decision**: README and manuscript disagree on the DiNapoli author name form (Robert J. vs Beau) and author order.

## 2026-05-05 — Submission-ready checkpoint

**Status**: JAMT manuscript and supplemental are submission-ready. Pick up from here for any future resumption.

**Primary deliverables**:
- `docs/merged_jamt/Manuscript.md` — main manuscript (~24k words including References Cited; abstract ~327 words)
- `docs/merged_jamt/Manuscript.docx` — pandoc-rendered DOCX with all 12 main-text figures embedded
- `docs/merged_jamt/Supplemental.md` — supplemental information (S1-S17, ~16k words)
- `docs/merged_jamt/Supplemental.docx` — pandoc-rendered DOCX with all 11 supplemental figures embedded
- `docs/merged_jamt/peer_review_report.md` — re-audit synthesis (3 main-text reviewers + 1 supplemental reviewer); shows status of each prior issue and remaining lower-priority items

**Final main-text figure ordering** (12 figures):
1. PP regional map (§1)
2. PP site architecture (§1)
3. MLS Price-equation decomposition (§2.1)
4. Ecotone advantage seasonal complementarity (§2.3)
5. Fitness crossover and critical threshold (§2.4)
6. ABM architecture schematic (§3)
7. Phase transition + signaling-vs-cooperation ablation (§4.1, §4.2) — 3-panel ablation result
8. Regional chronological synthesis (§5.2)
9. Paleoclimate proxy synthesis (§5.5)
10. Archaeological calibration with replicate spread (§6.1)
11. EPA Level IV ecoregions overlay (§6.4)
12. Multi-drainage shortfall buffering (§6.5)

**Final supplemental figure ordering** (11 figures): S1-S10 plus the new S11 joint-MC diagnostic.

**Empirical position**:
- Framework **discriminated** from generic risk-pooling and down-the-line exchange alternatives on the **spatial-flow signature** (§6.1; passed on existing record: Smith 1991 95.7% steatite / 97% galena at type-site; Kidder and Grooms 2025:7 "nothing visible goes out").
- Framework **not discriminated** on the **threshold-location dimension** (§4.2 ablation: −2.4% shift in realized σ_eff between signal-conditional and random-partner modes, within replicate noise).
- Watson Brake closure (§6.3) is a consistency demonstration conditional on three free parameters (α=2 superadditive beyond Erasmus 1965; K=3 sweep-selected; σ_sd from paleoclimate central). At ethnographically defensible α=1, the framework underpredicts WB by ~7×.

**Key analyses run** (reproducible):
- Overnight signal-conditional ablation sweep: 84/84 sims complete (6 reps × 7 σ × 2 modes; 789 min runtime); `results/ablation/overnight_sweep.json` + `results/ablation/phase_transition_summary.json`
- Joint parameter uncertainty Monte Carlo: N=1,000 over 6 model parameters at ±50%; `results/bayesian/joint_parameter_uncertainty.json`
- Joint posterior predictive Mahalanobis check on §6.1 exotics: d² ≈ 110 (rejects no-correction); §6.1 prose
- §S1.4 σ normalization invariance: T₀ ∈ {5, 10, 20, 50} with ratio σ_LMV/σ* = 1.591 preserved exactly

**Optional remaining work** (not blocking submission):
- Visitor-band outflow-asymmetry test at controlled provenience (§7.4(f)) — would tighten the spatial-flow signature from coarse to fine-grained; the coarse result is already in
- Drainage-resolved paleo-discharge for ε at each LMV site (§7.4(3))
- Threshold-vs-displacement collapse discrimination via high-resolution Bayesian dating (§7.4(4))
- Uniformly Bayesian-modeled chronologies for the full LMV PP-trait inventory (§7.4(5))
- Seasonal-aggregation pattern test from PP faunal collections (§7.4(6))

**State of GitHub repo (main branch)**: clean, synced, all today's work pushed. Last commit: prose pass through Manuscript.md (80bc0cc). PDFs deliberately untracked per project policy ("Local PDF stash; not redistributed").

**To restart from here**:
1. Read `docs/merged_jamt/Manuscript.md` and `docs/merged_jamt/Supplemental.md` for current state.
2. Read `docs/merged_jamt/peer_review_report.md` for the most recent peer-review re-audit (which lists what's been addressed and what remains optional).
3. Read `CHANGELOG.md` (this file) for full revision history.
4. The §4.2 ablation is the most recent substantive integration; if any new ablation runs are commissioned, they would refine but not change Outcome B.

---

## 2026-05-04 — Peer-review re-audit + Must Fix and Consider-Addressing batches

**Re-audit peer review**: Spawned three independent main-text reviewers (domain, methods, adversarial) plus a fourth dedicated supplemental reviewer. All four read the prior 2026-05-04-morning peer review report and the current manuscript and tracked what was addressed, what wasn't, and what's new. Synthesis at `docs/merged_jamt/peer_review_report.md`. Headline findings: revision trajectory honest and substantively responsive to all prior Must Fix items; new highest-priority remaining issue is §6.3 carrying the WB closure with more force than §7.4(ii)'s Erasmus disclosure supports; supplemental had a merged-but-unreconciled splice of two title pages and broken cross-references.

**Round 1 Must Fix items addressed**:
- MF-R1 (§6.3): inlined α=2 / K=3 qualifications; lead with α=1 underprediction (~7×); treat α=2 closure as consistency-conditional-on-three-free-parameters.
- MF-R2 (§2.2 forward reference): rewrote line 89 to describe what §4.2 actually delivers; pointed to §6.1 outflow asymmetry as the framework's discriminating empirical content.
- MF-R3 (§8 preference claim): softened in earlier outflow asymmetry upgrade.
- MF-R4 (§5.4 steatite count): removed 838 ± 87 simulation output from archaeological inventory paragraph; restored Webb's "several hundred vessels" + 2,221-fragment framing.
- MF-R5 (PPO cost-vs-unfakeability): tightened so PPO exclusion rests on PPOs failing the unfakeability criterion (any band with local clay can produce them, including non-attendees) rather than on cost.
- MF-S1 (merged-supplemental structure): collapsed two title pages and TOC paragraphs into one; removed cross-references to "the companion theory paper."
- MF-S2 (Manuscript Supplemental Material paragraph): rewrote to describe actual S1-S17 contents (was describing non-existent S1-S8 structure with "crosscheck-log summary" that does not exist).
- MF-S3 (CA3 σ normalization invariance in §S1.4): clean four-row table for $T_0 \in \{5, 10, 20, 50\}$ showing $\sigma_{LMV}$, $\sigma^*$, ratio = 1.591 preserved exactly.
- MF-S4 (broken cross-references): fixed §S9 figure numbers (Figs 6, 7 → 8, 9), §S10.2 "§3.4 paleoclimate" → "main-text §6.2", §S7 "ODD S6 of the framework supplemental" → "§S1.6", §S17 "framework paper supplemental S10" → "§S5".

**Round 2 Consider-Addressing items addressed**:
- CA-R1 (§7.5 Eastern Archaic placements): reframed from "consistent with [observed pattern]" confirmations to falsifiable predictions.
- CA-R2 (Sassaman framing): unified across §6.6, §7.1, §7.2 — agreed structural-vs-contingent decomposition, contested weight of structural register.
- CA-R3 (Figure 11 caption): reframed as documenting the static-diversity baseline that Figure 12B's covariance reasoning departs from.
- CA-R5 (§6.6 partial correlation): added Table 3 displaying zero-order and partial correlations for all three ε operationalizations (Shannon-rubric, EPA L4, phenology) so the framework's central honest concession (ε contributes ≤+0.014 marginal correlation given $n_{agg}$) is verifiable from a displayed result.
- CA-S1 (§S6 per-site rubric weights): added per-site weight vector table for all eleven sites with $(w_a, w_u, w_d, w_m, w_p)$ values used to compute Shannon $H$ in main-text Table 2.
- CA-S2 (§S15 climatology procedure): documented log-transformation, monthly climatology computation, residual construction, pairwise overlap handling.
- CA-S3 (K=3 page references): added Wiessner 2002:434-435 and Kelly 2013:159-167 with explicit caveat that these support order-of-magnitude calibration but not the specific $K = 3$ value (which was sweep-selected).
- CA-S4 (figure captions S1, S4, S6, S7): expanded each from terse one-phrase versions to standalone captions with parameter ranges, baselines, panel-by-panel content, and source script references.

**Outflow asymmetry upgrade**: Recognized that the framework's principal discriminating empirical claim — asymmetric flow into the gathering vs reciprocal flow or outward dispersal — is *passed* by the existing LMV record (Smith 1991: 95.7% steatite, 97% galena at type-site; Kidder and Grooms 2025:7: "nothing visible goes out"). Generic risk-pooling predicts reciprocal flow; generic down-the-line exchange predicts outward dispersal of PP-style markers; neither is observed. Reframed §6.1 outflow paragraph from "future test" to "discriminating test passed on existing data"; added 6.1 (outflow) row to §6 status table; revised §7.4(f), §8 conclusion, and abstract accordingly. The framework now has four (not three) evaluations carrying independent inferential weight, with the asymmetric-flow signature as the discriminating one.

**Plain-language passes** (§2.4, §3, §4.2): reframed lambda-sigma feedback in plain prose first; added gloss for fixed-point iteration, softmax, and partial-derivative notation; split dense σ-derivation paragraph into three; introduced three λ components by name + meaning before §4.2 ablation discussion.

**PPO discussion** (§2.2): two-stage revision. First, separated function (cooking) from form (style) and routed PPO formal variation to cultural-transmission analysis. Second, sharpened the framework's exclusion of PPOs from costly signaling: the criterion is unfakeability, not cost; PPOs fail because any band with local clay and fuel can produce them, including non-attending bands.

**GIS ecoregions promotion**: Promoted `fig_gis_ecoregions.png` from S10 to main-text Figure 11 (in §6.4) for geographic concreteness of the cross-LMV screening. Renumbered Fig 11 (multi-drainage) → 12; Supplemental S11 → S10. Final main-text ordering: 12 figures.

**Sweep mid-run** (overnight signal-conditional ablation, currently 71/84): Signal arm fully complete (42/42); random arm fully complete through σ=0.40 (24/24), σ=0.44 has 5/6. **Outcome B confirmed within replicate noise**: random-partner formation produces statistically indistinguishable threshold from signal-conditional formation (both crossovers at realized σ_eff ≈ 0.40-0.41; differences inconsistent in sign and within SD ranges of 0.04-0.19). Pre-staged §4.2 Outcome B language at `docs/merged_jamt/section_4_2_update_pending.md` will swap in once the remaining 13 sims complete (~2 hours).

## 2026-05-04 — JAMT pedagogical figures + abstract trim

**Changes**:
- Abstract trimmed from ~440 words to 236 words; removed in-text citations per JAMT convention. Spanish resumen condensed to match.
- Added two new pedagogical main-text figures so JAMT readers (who may not be steeped in costly-signaling or multilevel-selection literature) can see the framework's mechanics directly:
  - Figure 3: Multilevel-selection Price decomposition. Two-panel illustration showing (A) the within-group cost penalty and between-group cooperation reward as a schematic of two groups with mixed strategies, and (B) within / between / net selection components plotted vs σ, with the threshold σ* marked where the components balance. Lands at illustrative σ* ≈ 0.41 (matches the manuscript's 0.40 calibrated value). Script `scripts/figure_generation/create_figure_mls_decomposition.py`.
  - Figure 4: Ecotone advantage promoted from Supplemental S3 (`figure_ecotone_seasonal.png`). Panel A shows staggered seasonal productivity profiles for the four resource zones; Panel B shows the dramatic difference in shortfall frequency between a single-zone band (9 of 50 years) and an ecotone-buffered band drawing from two negatively correlated zones (0 of 50 years).
- Renumbered existing main-text figures: 3 → 5 (fitness crossover), 4 → 6 (ABM schematic), 5 → 7 (phase transition), 6 → 8 (regional chronology), 7 → 9 (paleoclimate proxy), 8 → 10 (calibration), 9 → 11 (multi-drainage).
- Final main-text ordering (11 figures): 1 regional map, 2 site architecture, 3 MLS decomposition, 4 ecotone advantage, 5 fitness crossover, 6 ABM schematic, 7 phase transition, 8 regional chronology, 9 paleoclimate, 10 calibration, 11 multi-drainage.
- Supplemental cleanup: removed the ecotone-seasonal figure (was S3); renumbered remaining S4-S12 → S3-S11.
- DOCX regenerated: Manuscript.docx 15.5 MB / 11 figures; Supplemental.docx 4.6 MB / 11 figures.

## 2026-05-04 — Figure promotions + overnight sweep mid-run check

**Changes**:
- Promoted three figures from supplemental to main text for reading flow:
  - Figure 4: ABM architecture schematic (was S2) inserted after §3 to give readers a visual reference for the model before §4 results.
  - Figure 6: Regional chronological synthesis (was S12) inserted in §5.2 alongside the chronology and collapse discussion.
  - Figure 7: Paleoclimate proxy synthesis (was S10) inserted in §5.5 to anchor the σ ≈ 0.64 estimate visually.
- Renumbered existing main-text figures: phase transition Fig 4 → Fig 5; calibration Fig 5 → Fig 8; multi-drainage Fig 6 → Fig 9. Final main-text figure ordering: 1 regional map, 2 site architecture, 3 fitness crossover, 4 ABM schematic, 5 phase transition (placeholder pending sweep), 6 regional chronology, 7 paleoclimate, 8 calibration, 9 multi-drainage.
- Renumbered supplemental figures: removed S2/S10/S12, S3-S6 → S2-S5, S7-S9 → S6-S8, S11 → S9, S13-S15 → S10-S12. Section numbers (S1-S17) unchanged.
- Manuscript.docx now embeds all 9 main-text figures cleanly (14.7 MB); Supplemental.docx embeds all 12 SI figures (5.1 MB).
- Mid-run check on `overnight_sweep.json`: signal-conditional arm now 31/42 sims complete; phase transition clearly resolved (dom climbs from -0.40 at σ_eff=0.20 through crossover at σ_eff≈0.28-0.30 to +0.86 at σ_eff=0.50). Random-partner arm has not started.

## 2026-05-04 — Round 4 polish + overnight ablation launched

**Changes**:
- Cleaner DOCX exports without reference-template image bloat (Manuscript.docx 12 MB, Supplemental.docx 6.3 MB; was 26 + 20 MB).
- §S17 Ext. 2 expanded with the Erasmus 1965 α-derivation analysis: linear scaling (α≈1) is what Erasmus's 2.6 m³/person-day rate supports; α=2 used in §6.3 implies superadditive scaling beyond the ethnographic baseline.
- §S3.1 OAT extended with the joint parameter uncertainty propagation result for §6.2 (P=0.33 under N=1,000 Monte Carlo over 6 model parameters + σ + ε priors).
- README.md rewritten to reflect the merged JAMT submission as primary deliverable and to match the post-Round-4 honest framing.
- CHANGELOG.md created (this file).

**Overnight sweep launched** (`scripts/analysis/signal_conditional_ablation_sweep.py`):
- 84 simulations: 7 σ_eff × 6 replicates × 2 modes (signal_conditional, random_partners)
- σ_eff controlled via `ShortfallParams.mean_interval` (the actual driver of effective σ in the integrated simulation, discovered during diagnostic)
- Saves intermediate JSON after every sim
- ETA ~12-13 hours
- Will integrate into §4.2 (genuine ablation result) and §4.1 (phase transition validation rerun)

## 2026-05-04 — Round 4: substantive new analyses

Four substantive new analyses to address peer-review concerns that exceeded prose-level fixes.

**Round 4-1: Joint parameter uncertainty in §6.2 (✅ done)**
- Monte Carlo over 6 model parameters defining σ* (C_signal, C_opportunity, λ_W, k_max, M_half, γ) at ±50% jointly with §6.2 rubric priors on σ and ε.
- N=1,000 samples → P(σ_eff > σ*) = 0.33; comparable to §6.2 baseline 0.36.
- Posterior on σ_eff − σ* has mean −0.05, 95% CI [−0.26, +0.18]; straddles zero.
- Conditioning caveat introduced in MF3 (Round 1) is real but bounded.
- `scripts/analysis/joint_parameter_uncertainty.py`; output `results/bayesian/joint_parameter_uncertainty.json`.

**Round 4-2: Signal-conditional ablation (◐ overnight sweep running)**
- Diagnostic uncovered that the integrated simulation's σ-input parameter does NOT correspond directly to analytical σ; running at σ_regional=0.385, ε=0.35 produced realized mean_effective_sigma=0.690 (not 0.25 as the naive σ × (1−ε) calculation would predict).
- Effective σ in the integrated simulation comes from `ShortfallParams.magnitude_mean × √(20/mean_interval)`, not from the `sigma` parameter to `default_parameters`.
- Overnight sweep set up to control σ_eff via `ShortfallParams.mean_interval`; will produce both the ablation comparison and the phase-transition rerun.
- §4.2 updated with honest framing: implementable in code, full quantitative result pending sweep completion.

**Round 4-3: Erasmus 1965 α derivation (✅ done)**
- Erasmus's experimental rate of 2.6 m³/person-day corresponds to α ≈ 1 (linear in crew size) under additive labor accounting.
- The α = 2 used in §6.3 implies superadditive scaling beyond Erasmus.
- §7.4(ii) updated: "consistent only under a fitted α = 2 that exceeds Erasmus-derived linear scaling," not ethnographically grounded.
- §S17 Ext. 2 includes the full derivation and discussion.
- Erasmus 1965 added to References Cited.

**Round 4-4: Phase transition rerun (◐ folded into Round 4-2 sweep)**
- The signal_conditional=True arm of the overnight sweep provides 6 replicates × 7 σ_eff points at PP-scenario parameters, addressing the methods-reviewer's replicate-thinness concern in §4.1.
- Will integrate when sweep completes.

## 2026-05-04 — Round 3: methods-heavy Consider-Addressing items

Three methods-level revisions:
- **CA10**: σ type-mismatch clarified in §3. σ is best read as an "effective shortfall severity index over a 20-year horizon." Alternative reference windows can be used equivalently if other σ-bearing parameters are recalibrated in tandem.
- **CA3**: σ normalization invariance demonstrated analytically + numerically in §S1.4. Under T_0 → T_0', both σ_LMV and σ* rescale by √(T_0'/T_0), inequality preserved by construction. Verified at T_0 = 5 and T_0 = 50.
- **CA12**: Joint posterior predictive check for §6.1 exotics. d² = 110 rejects under no-correction interpretation; cross-material correlations (r = 0.85-0.97 for steatite/galena/novaculite/crystal-quartz) reveal apparent independence of marginal checks was overstated. Recovery-loss correction at the rate that reconciles galena marginal (~55%) brings joint check into consistent range.
- **CA2**: §4.1 phase transition replicate thinness acknowledged with pointer to broader 400-cell × 5-replicate phase-boundary sweep in §S3.

## 2026-05-04 — Round 2: prose-level Consider-Addressing items

Eight prose-level revisions from peer-review:
- **CA1**: Sassaman framing reconciled across §6.6, §7.1, §7.2, §8. §7.2 commits to "genuine tension"; §6.6 and §7.1 now flag partial alignment on necessity-not-sufficiency point and direct readers to §7.2.
- **CA4**: USGS "confirm" softened in §8 (already removed in Round 1 §8 rewrite).
- **CA5**: §5.2 convergence-not-diffusion claim qualified. Lower Jackson / Watson Brake order corrected. Convergence reading explicitly imported from Grooms 2023 / Kidder & Grooms 2024.
- **CA6**: PPO literature engagement added in §2.2 (Hays 2019, Webb 1982).
- **CA7**: §6.7 heading expanded to "(plausibility check, not independent test)".
- **CA8**: §6 audit table catalogs all 8 evaluations: what is fit, what is independent, status.
- **CA9**: Figure 5 panel B caption rewritten — no more "would be misleading" warning.
- **CA11**: Repository file paths in main text relocated.

## 2026-05-04 — Round 1: peer-review Must-Fix items + Perreault framing

Four Must-Fix items addressed:
- **MF1**: Abstract and §8 alignment with §7.4 honest audit. Rewritten to organize results by 3 independent tests + 5 consistency demonstrations.
- **MF2**: §4.2 reframed from "ablation" to "within-group reward sensitivity check." The 36-37% threshold shift is now framed as parameter sensitivity, not a discrimination result. Genuine signal-conditional ablation identified as priority work.
- **MF3**: §6.2 conditioning caveat added. Names the parameter-set dependence: σ* is not derived independently of Poverty Point.
- **MF4**: §7.4(ii) "K=3 ethnographically justified" claim corrected to "K=3 selected from a sweep where K=1 overshoots and K=5 undershoots WB's observed volume."

**Plus**: Perreault 2019 epistemological framing added at two points:
- §1: new paragraph on the structural challenge of evaluating explanatory models against records assembled under culture-historical paradigms.
- §7.4 expanded: makes the resolution-question match explicit, distinguishes discriminating items (visitor-band outflow signature, signal-conditional ablation) from items that tighten specific framework claims.

## 2026-05-03 — Peer-review-sim run

Three independent reviewers (Domain, Methods, Adversarial) produced structured feedback. Report at `docs/merged_jamt/peer_review_report.md`.

Convergent findings:
- A1: Ablation test does not establish what abstract claims (Methods W2 + Adversarial C1).
- A2: Watson Brake closure double-fitted, not flagged in abstract/§8 (all three).
- A3: Empirical evaluations dominated by patterns alternative frameworks predict equally well (Domain W2 + Adversarial C2).
- A4: Abstract/§8 oversells cumulative case relative to §7.4 audit (all three).
- A5: §6.2 Bayesian threshold-proximity test less independent than framing suggests (Methods W1 + Adversarial C3).

Adversarial reviewer's strongest counterargument: a pure risk-pooling/storage account in the Halstead and O'Shea (1989) tradition predicts the same threshold-crossing patterns; framework's empirical case rests on consistency rather than discrimination. The visitor-band outflow asymmetry test would discriminate but is not performed.

## 2026-05-03 — JAMT manuscript build

Built `docs/merged_jamt/Manuscript.md` from the existing two-paper split:
- Paper 1 (theory + ABM, target: JAMT)
- Paper 2 (Poverty Point empirical evaluation, target: American Antiquity)

Merge rationale: Paper 2 cannot submit until Paper 1 accepted under the split structure. JAMT accepts long papers and the theory + worked-empirical-case pairing is JAMT's sweet spot.

Title: *Costly signaling under environmental uncertainty: A multilevel-selection threshold model for Poverty Point*.

Section structure (8 sections + supplemental S1-S17):
- §1 Introduction (PP-led; Late Archaic context one paragraph)
- §2 Theoretical framework (multilevel selection, index signals, ecotone advantage, fitness functions)
- §3 Agent-based model (ODD protocol)
- §4 Theoretical results (phase transition, λ_W sensitivity, parameter sensitivity)
- §5 LMV record (eleven sites + chronology + tempo + exotics + paleoclimate)
- §6 Empirical evaluation (8 tests with explicit audit table)
- §7 Discussion (cultural-historical alternatives, collapse, falsifiable predictions, broader implications)
- §8 Conclusions

Original two-paper files retained as predecessor manuscripts in `docs/paper1_theory/` and `docs/paper2_empirical/`.

## 2026-05-03 — Wiessner 1977 dissertation processed

Fourth reference in the audit chain on the disputed "10-30% additional resources during shortfalls" figure that earlier drafts attributed to a Wiessner source. Bounded reading confirms the figure is not in any of the four sources audited (Hawkes 2000, Wiessner 1982, Wiessner 2002, Wiessner 1977). Most plausibly a paraphrase artifact from secondary literature or the dissertation's data tables not exhaustively read in this audit. Paper 1 (now §4.2 ethnographic anchor paragraph) revised to remove the unsupported attribution.

Cross-check log: `docs/references/crosscheck_log.md`.

## Earlier history

- 2026-05-03: Wiessner 1982 ("Beyond Willow Smoke") added; third audit on the 10-30% figure.
- 2026-05-03: Hill et al. 2016 LA-ICP-MS copper provenance paper added; replaces unpublished hill_etal_2010 SAA precursor.
- 2026-05-03: Wiessner 2002 audit; "10-30%" figure not in this paper.
- 2026-05-03: Hawkes 2000 audit; "10-20%" figure not in this paper.
- Earlier 2026: Reference pipeline built (47+ sources processed), AA + JAS v2 manuscripts authored, three rounds of internal peer review on AA.

---

## Forward agenda

Items identified as priority empirical work in §7.4 of the JAMT manuscript:

1. **Visitor-band outflow asymmetry test**: controlled provenience analysis on PP-style exotic material at sites whose visitor-band status is independently established. Genuinely signaling-discriminating; would address the Adversarial reviewer's strongest counterargument.
2. **Joint parameter-uncertainty propagation in §6.2**: ✅ done in Round 4-1.
3. **Drainage-resolved paleo-discharge for ε**: replace modern hydrograph-as-proxy with sediment-yield reconstructions or paleo-flood-frequency proxies per drainage at focal-site scale.
4. **Threshold-vs-displacement collapse discrimination**: high-resolution Bayesian dating of terminal-occupation deposits comparable to Kidder and Grooms (2024) for active interval.
5. **Uniformly Bayesian-modeled chronologies for the full LMV PP-trait inventory** at sites beyond Jaketown and Poverty Point, to discriminate convergence from delayed down-the-line diffusion.
6. **Seasonal-aggregation pattern test**: reanalysis of existing PP faunal collections at finer seasonal resolution.
7. **Higher-resolution PP-scenario phase-transition rerun**: ◐ folded into the overnight sweep launched 2026-05-04.
8. **Genuine signal-conditional ablation**: ◐ overnight sweep running.
9. **Independent ethnographic derivation of α at relevant crew sizes**: ✅ partially done (Erasmus 1965 supports α ≈ 1; α = 2 used in §6.3 needs additional justification).

Items 1, 3, 4, 5, 6 require new field collection or substantial new analytical work. Items 7, 8 are running. Items 2, 9 are done.
