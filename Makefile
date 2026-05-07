# Poverty Point Costly Signaling — reproducibility targets.
#
# See REPRODUCE.md for full step-by-step documentation of each analysis,
# random-seed strategy, and expected outputs.
#
# Standard targets:
#   make figures      regenerate every figure in figures/final/ and figures/integrated/
#   make calibration  rerun the Tier-3 calibration replicates (~3 hours; produces Figure 5)
#   make analyses     rerun all analyses below the calibration tier (GIS-eps, sigma, etc.)
#   make manuscript   build the AA and v2.0 docx manuscripts
#   make all          analyses + figures + manuscript (skips slow calibration; run that explicitly)
#   make clean        remove generated docx files (keeps figures and JSON results)

PYTHON ?= python
SCRIPTS_FIG := scripts/figure_generation
SCRIPTS_ANA := scripts/analysis

.PHONY: all figures calibration analyses manuscript clean help

help:
	@echo "Poverty Point Costly Signaling reproducibility targets:"
	@echo "  make figures      regenerate every figure"
	@echo "  make calibration  rerun calibration replicates (~3 hours; Figure 5)"
	@echo "  make analyses     rerun GIS-eps, sigma comparison, distance decay, tier-3 sweeps"
	@echo "  make manuscript   build AA and v2.0 docx files"
	@echo "  make all          analyses + figures + manuscript (skips slow calibration)"
	@echo "  make clean        remove generated docx files"

all: analyses figures manuscript

# --- Figures ---------------------------------------------------------------

figures:
	# Manuscript figures (output: figures/manuscript/figure_NN_*.{png,pdf})
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_01_poverty_point_map.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_02_site_architecture.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_03_mls_decomposition.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_04_ecotone_seasonal.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_05_fitness_crossover.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_06_model_architecture.py
	$(PYTHON) $(SCRIPTS_FIG)/create_integrated_simulation_figures.py  # Figures 7 + 8 (and S6/S7 indirectly via the sigma-sweeps script below)
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_09_regional_chronology.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_10_paleoclimate.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_12_gis_ecoregions.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_13_multi_drainage.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_14_seasonal_phenology.py
	# Supplemental figures (output: figures/supplemental/figure_SNN_*.{png,pdf})
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_S05_predictions_summary.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figures_S06_S07_sigma_sweeps.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_S08_obligation_network.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_S09_exotic_distance_decay.py
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_S02_joint_mc_diagnostic.py

# --- Calibration (slow; ~3 hours) -----------------------------------------
# Figure 11 (calibration anchor) regenerates the Tier-3 replicates and emits
# the figure. Slow target; not invoked by `make figures`.

calibration:
	$(PYTHON) $(SCRIPTS_FIG)/create_figure_11_calibration.py

# --- Analyses --------------------------------------------------------------

analyses:
	$(PYTHON) $(SCRIPTS_ANA)/gis_epsilon.py
	$(PYTHON) $(SCRIPTS_ANA)/gis_epsilon_eparegions.py
	$(PYTHON) $(SCRIPTS_ANA)/gis_epsilon_categorical.py
	$(PYTHON) $(SCRIPTS_ANA)/calculate_sigma_comparison.py
	$(PYTHON) $(SCRIPTS_ANA)/distance_decay_test.py
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
