# Figure-generation scripts

This folder contains the scripts that produce the figures in the active JAMT manuscript and supplemental.

## Active scripts (referenced by `make figures`)

Each manuscript figure has a script named to match the figure number, and writes its output directly to `figures/manuscript/figure_NN_*.{png,pdf}` or `figures/supplemental/figure_SNN_*.{png,pdf}`.

**Manuscript figures (1–14):**

| Figure | Script |
|---|---|
| Figure 1 | `create_figure_01_poverty_point_map.py` |
| Figure 2 | `create_figure_02_site_architecture.py` |
| Figure 3 | `create_figure_03_mls_decomposition.py` |
| Figure 4 | `create_figure_04_ecotone_seasonal.py` |
| Figure 5 | `create_figure_05_fitness_crossover.py` |
| Figure 6 | `create_figure_06_model_architecture.py` |
| Figures 7 + 8 | `create_integrated_simulation_figures.py` (multi-output) |
| Figure 9 | `create_figure_09_regional_chronology.py` |
| Figure 10 | `create_figure_10_paleoclimate.py` |
| Figure 11 | `create_figure_11_calibration.py` (slow; ~3 hr to regenerate the underlying calibration replicates) |
| Figure 12 | `create_figure_12_gis_ecoregions.py` |
| Figure 13 | `create_figure_13_multi_drainage.py` |
| Figure 14 | `create_figure_14_seasonal_phenology.py` |

**Supplemental figures (S1–S9):**

| Figure | Script |
|---|---|
| Figure S1 | `scripts/analysis/oat_sensitivity.py` (lives in scripts/analysis/, not here) |
| Figure S2 | `create_figure_S02_joint_mc_diagnostic.py` |
| Figure S3, S4 | (source scripts not currently identified; figures preserved as static assets in `figures/supplemental/`) |
| Figure S5 | `create_figure_S05_predictions_summary.py` |
| Figures S6 + S7 | `create_figures_S06_S07_sigma_sweeps.py` (multi-output) |
| Figure S8 | `create_figure_S08_obligation_network.py` |
| Figure S9 | `create_figure_S09_exotic_distance_decay.py` |

To regenerate every active figure, run `make figures` from the project root.

## Archived scripts (`_archive/`)

The `_archive/` subfolder contains 16 scripts from earlier drafts of this project. They are preserved for reference but are not invoked by `make figures` and do not produce figures referenced by the current JAMT manuscript or supplemental. Examples:

- `abm_validation.py` — validation figures from an earlier ABM iteration
- `dissertation_guide_figures.py` — figures used in a dissertation chapter version
- `pacific_comparison_figures.py` — pacific-rim comparison figures from an earlier theoretical scope
- `population_dynamics.py`, `monument_trajectories.py`, `theoretical_phase_space.py`, `price_equation_figures.py`, etc. — single-purpose visualizations from prior drafts

If you need to regenerate one of these, invoke it directly with `python scripts/figure_generation/_archive/<script>.py`. Output paths in those scripts may still point to the legacy `figures/final/` or `figures/integrated/` locations.

## Adding a new figure

1. Pick the next available number (or the figure number it replaces).
2. Create `scripts/figure_generation/create_figure_NN_short_name.py` for a manuscript figure or `create_figure_SNN_short_name.py` for a supplemental.
3. The script should write to `figures/manuscript/figure_NN_short_name.{png,pdf}` (or the supplemental equivalent) at 300 dpi.
4. Add the script to the appropriate block in the `figures:` target of the project-root `Makefile`.
5. Update this README and the figures-folder READMEs (`figures/manuscript/README.md` and `figures/supplemental/README.md`) with the new mapping.
