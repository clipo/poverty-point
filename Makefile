# Poverty Point Costly Signaling — reproducibility targets.
#
# See REPRODUCE.md for full step-by-step documentation of each analysis,
# random-seed strategy, and expected outputs.
#
# Standard targets:
#   make figures      regenerate every figure in figures/manuscript/ and figures/supplemental/
#   make simulations  rerun the stochastic simulation suite (ablation sweep, phase space,
#                     ensemble, Price decomposition, calibration replicates; ~2-3 hours)
#   make analyses     rerun the deterministic analyses (GIS-eps, sigma, correlations,
#                     diagnostics, PPC; minutes)
#   make manuscript   build the JAMT Manuscript and Supplemental docx files
#   make all          analyses + figures + manuscript (skips slow simulations; run explicitly)
#   make clean        remove generated docx files (keeps figures and JSON results)

PYTHON ?= python
SCRIPTS_FIG := scripts/figure_generation
SCRIPTS_ANA := scripts/analysis

.PHONY: all figures simulations analyses manuscript clean help

help:
	@echo "Poverty Point Costly Signaling reproducibility targets:"
	@echo "  make figures      regenerate every figure"
	@echo "  make simulations  rerun stochastic simulation suite (~2-3 hours)"
	@echo "  make analyses     rerun deterministic analyses (minutes)"
	@echo "  make manuscript   build JAMT docx files"
	@echo "  make all          analyses + figures + manuscript (skips slow simulations)"
	@echo "  make clean        remove generated docx files"

all: analyses figures manuscript

# --- Figures ---------------------------------------------------------------
# Each script is named for the manuscript/supplemental figure it produces.

figures:
	# Manuscript figures (output: figures/manuscript/figure_NN_*.{png,pdf})
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_01_poverty_point_map.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_02_site_architecture.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_03_mls_decomposition.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_04_ecotone_seasonal.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_05_fitness_crossover.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_06_model_architecture.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_07_phase_transition.py       # depends on results/ablation/ablation_sweep_engine2.json (make simulations)
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_08_temporal_dynamics_ensemble.py  # depends on results/analysis/figure_8_ensemble_*.json
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_09_phase_space_replicated.py # depends on results/analysis/phase_space_replicated_*.json
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_10_regional_chronology.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_11_paleoclimate.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_12_calibration.py            # depends on results/calibration_replicates/replicates_n8_d200.json
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_13_gis_ecoregions.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_14_multi_drainage.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_15_seasonal_phenology.py
	# Supplemental figures (output: figures/supplemental/figure_SNN_*.{png,pdf})
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_S02_joint_mc_diagnostic.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_S05_predictions_summary.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_S06_factorial_ablation.py    # depends on results/ablation/factorial_channel_ablation_*.json
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_S07_price_decomposition.py   # depends on results/analysis/price_decomposition_*.json
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_S08_ablation_n20.py          # depends on results/ablation/ablation_sweep_engine2.json
	$(PYTHON) $(SCRIPTS_FIG)/create_figures_S09_S10_sigma_sweeps.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_S11_obligation_network.py

# --- Stochastic simulation suite (slow; ~2-3 hours total) -------------------

simulations:
	$(PYTHON) $(SCRIPTS_ANA)/run_calibration_replicates.py
	$(PYTHON) $(SCRIPTS_ANA)/run_figure_8_ensemble.py
	$(PYTHON) $(SCRIPTS_ANA)/run_price_decomposition.py
	$(PYTHON) $(SCRIPTS_ANA)/signal_conditional_ablation_sweep.py
	$(PYTHON) $(SCRIPTS_ANA)/run_phase_space_replicated.py
	$(PYTHON) $(SCRIPTS_ANA)/run_factorial_channel_ablation.py
	$(PYTHON) $(SCRIPTS_ANA)/run_morris_sa.py

# --- Deterministic analyses (minutes) ---------------------------------------

analyses:
	$(PYTHON) $(SCRIPTS_ANA)/verify_analytical_diagnostics.py
	$(PYTHON) $(SCRIPTS_ANA)/oat_sensitivity_table.py
	$(PYTHON) $(SCRIPTS_ANA)/gis_epsilon.py
	$(PYTHON) $(SCRIPTS_ANA)/gis_epsilon_eparegions.py
	$(PYTHON) $(SCRIPTS_ANA)/gis_epsilon_categorical.py
	$(PYTHON) $(SCRIPTS_ANA)/calculate_sigma_comparison.py
	$(PYTHON) $(SCRIPTS_ANA)/water_route_catchment_epsilon.py
	$(PYTHON) $(SCRIPTS_ANA)/partial_correlation_eps_nagg.py
	$(PYTHON) $(SCRIPTS_ANA)/predicted_scale_ratios.py
	$(PYTHON) $(SCRIPTS_ANA)/per_event_labor_scaling.py
	$(PYTHON) $(SCRIPTS_ANA)/phenology_variance_epsilon.py
	$(PYTHON) $(SCRIPTS_ANA)/phenology_epsilon_test.py
	$(PYTHON) $(SCRIPTS_ANA)/table2_weight_perturbation.py
	$(PYTHON) $(SCRIPTS_ANA)/exotic_ppc.py                # depends on calibration replicates
	$(PYTHON) $(SCRIPTS_ANA)/hydrograph_covariance.py
	$(PYTHON) $(SCRIPTS_ANA)/renovation_ratio.py
	$(PYTHON) $(SCRIPTS_ANA)/tier3_extensions.py

# --- Manuscript ------------------------------------------------------------

manuscript:
	# Active JAMT draft: Manuscript and Supplemental (in docs/jamt/)
	pandoc docs/jamt/Manuscript.md \
	    -o docs/jamt/Manuscript.docx \
	    --reference-doc docs/jamt/reference_template.docx \
	    --resource-path docs/jamt \
	    --from markdown --to docx
	pandoc docs/jamt/Supplemental.md \
	    -o docs/jamt/Supplemental.docx \
	    --reference-doc docs/jamt/reference_template.docx \
	    --resource-path docs/jamt \
	    --from markdown --to docx
	# Older drafts in docs/_archive/ are not rebuilt by default. See docs/_archive/README.md
	# for the build commands if regeneration is needed.

clean:
	rm -f docs/jamt/Manuscript.docx
	rm -f docs/jamt/Supplemental.docx
