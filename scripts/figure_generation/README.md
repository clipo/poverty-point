# Figure-generation scripts

This folder contains the scripts that produce the figures in the active JAMT manuscript and supplemental.

## Active scripts (referenced by `make figures`)

Each figure has a script named to match the figure number, and writes its output directly to `figures/manuscript/figure_NN_*.{png,pdf}` or `figures/supplemental/figure_SNN_*.{png,pdf}`.

**Manuscript figures (1-15):**

| Figure | Script |
|---|---|
| Figure 1 | `create_figure_01_poverty_point_map.py` |
| Figure 2 | `create_figure_02_site_architecture.py` (formats the externally provided LiDAR base; the labeled manuscript image is shipped as a static asset) |
| Figure 3 | `create_figure_03_mls_decomposition.py` |
| Figure 4 | `create_figure_04_ecotone_seasonal.py` |
| Figure 5 | `create_figure_05_fitness_crossover.py` |
| Figure 6 | `create_figure_06_model_architecture.py` |
| Figure 7 | `create_figure_07_phase_transition.py` (reads `results/ablation/ablation_sweep_engine2.json`) |
| Figure 8 | `create_figure_08_temporal_dynamics_ensemble.py` (reads `results/analysis/figure_8_ensemble_*.json`) |
| Figure 9 | `create_figure_09_phase_space_replicated.py` (reads `results/analysis/phase_space_replicated_*.json`) |
| Figure 10 | `create_figure_10_regional_chronology.py` |
| Figure 11 | `create_figure_11_paleoclimate.py` |
| Figure 12 | `create_figure_12_calibration.py` (reads `results/calibration_replicates/replicates_n8_d200.json`) |
| Figure 13 | `create_figure_13_gis_ecoregions.py` |
| Figure 14 | `create_figure_14_multi_drainage.py` |
| Figure 15 | `create_figure_15_seasonal_phenology.py` |

**Supplemental figures (S1-S11):**

| Figure | Script |
|---|---|
| Figure S1 | `scripts/analysis/oat_sensitivity_table.py` (lives in scripts/analysis/, not here) |
| Figure S2 | `create_figure_S02_joint_mc_diagnostic.py` |
| Figures S3, S4 | static assets in `figures/supplemental/` (conceptual schematics) |
| Figure S5 | `create_figure_S05_predictions_summary.py` |
| Figure S6 | `create_figure_S06_factorial_ablation.py` |
| Figure S7 | `create_figure_S07_price_decomposition.py` |
| Figure S8 | `create_figure_S08_ablation_n20.py` |
| Figures S9 + S10 | `create_figures_S09_S10_sigma_sweeps.py` (multi-output) |
| Figure S11 | `create_figure_S11_obligation_network.py` |

To regenerate every active figure, run `make figures` from the project root.

## Archived scripts (`_archive/`)

The `_archive/` subfolder contains scripts from earlier drafts of this project. They are preserved for reference but are not invoked by `make figures` and do not produce figures referenced by the current JAMT manuscript or supplemental.

If you need to regenerate one of these, invoke it directly with `python scripts/figure_generation/_archive/<script>.py`. Output paths in those scripts may still point to the legacy `figures/final/` or `figures/integrated/` locations.

## Adding a new figure

1. Pick the next available number (or the figure number it replaces).
2. Create `scripts/figure_generation/create_figure_NN_short_name.py` for a manuscript figure or `create_figure_SNN_short_name.py` for a supplemental.
3. The script should write to `figures/manuscript/figure_NN_short_name.{png,pdf}` (or the supplemental equivalent) at 300 dpi.
4. Add the script to the appropriate block in the `figures:` target of the project-root `Makefile`.
5. Update this README and the figures-folder READMEs with the new mapping.
