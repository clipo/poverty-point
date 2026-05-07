# Reproducibility Guide

Step-by-step instructions for regenerating every analysis, simulation, and figure in the manuscripts. All stochastic simulations use deterministic seeds; running the canonical commands below should produce numerically identical outputs to those reported in the manuscript and supplemental.

## 1. Environment

Tested on macOS 25.5 (Darwin) with Python 3.12.2.

```bash
# Option A: pip + venv (pure-Python paths)
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```bash
# Option B: conda (recommended for geospatial stack on macOS / Windows)
conda create -n pp-signaling python=3.12 -c conda-forge \
    numpy=2.4.3 scipy=1.17.1 pandas=3.0.1 matplotlib=3.10.8 \
    seaborn=0.13.2 networkx=3.3 cartopy=0.25.0 geopandas=1.1.0 \
    shapely=2.1.1 pyproj=3.6.1 rasterio=1.4.2 \
    python-docx=1.1.0 pyyaml=6.0.1 tqdm=4.66.5
conda activate pp-signaling
```

`pandoc` (>= 3.0) is required for the manuscript docx build step; install via `brew install pandoc` on macOS or your OS package manager.

## 2. External data

Two external geospatial datasets are referenced by Figure 1 and the GIS-ε analyses. The repo expects them at the paths below; the scripts will fail with informative errors if they are missing.

| Dataset | Repo path | Source |
|---------|-----------|--------|
| Saucier (1994) LMV geomorphology | `data/geology/Saucier_Geomorph_shapefile/Saucier_Geomorph.shp` | USGS ScienceBase 59b7ddd6e4b08b1644df5cf6 (doi:10.5066/F7N878QN) |
| EPA Level IV ecoregions (LA, MS, AR) | `data/ecoregions/{la,ms,ar}_eco_l4/*.shp` | EPA Office of Research and Development; `dmap-prod-oms-edc.s3.us-east-1.amazonaws.com/ORD/Ecoregions/us/us_eco_l4.zip` |

Both datasets are public-domain. Tracked archaeological data, paleoclimate compilations, and processed reference materials are all included in `data/` and `docs/references/`.

## 3. Random-seed strategy

All stochastic simulations are seeded deterministically.

- Core simulation: `src/poverty_point/simulation.py` defines `seed: int = 42` as the model default and constructs `np.random.default_rng(config.seed)` at run time.
- Calibration replicates: `scripts/figure_generation/create_figure_11_calibration.py` uses `seed = 1000 + N_REPLICATES * scenario_index + replicate_index` to give each (scenario, replicate) a unique reproducible seed.
- GIS Monte Carlo perturbations: `scripts/analysis/gis_epsilon.py` and `gis_epsilon_eparegions.py` use `np.random.default_rng(seed=20240501)` for the 1,000-draw zone-weight perturbation (Table 1 §S8.4 supplemental result).

Re-running any of the scripts below should produce numerically identical outputs to those checked into `results/`.

## 4. Reproduce the analyses

The order below mirrors the manuscript's logical flow. Each step is independent: you can regenerate any subset by running the indicated script.

### 4.1 Calibration replicates (Figure 11; manuscript §6.1 summary statistics)

```bash
python scripts/figure_generation/create_figure_11_calibration.py
```

- Run time: ~3 hours on a 2024-class laptop (4 scenarios × 8 replicates × 200 simulated years).
- Outputs: `results/calibration_replicates/replicates_n8_d200.json`; `figures/manuscript/figure_11_calibration.{png,pdf}`.
- Verifies: PP mean 9,731 ± 640 monument units, 21,469 ± 1,405 exotics; calibration scale ≈77 m³/unit.

### 4.2 GIS-ε (geomorphic, Saucier 1994)

```bash
python scripts/analysis/gis_epsilon.py
```

- Outputs: `results/gis/gis_epsilon.json`.
- Verifies: Spearman ρ = 0.70 between qualitative ε and Saucier-geomorphic ε across the 11 LMV sites.

### 4.3 GIS-ε (EPA Level IV ecoregions)

```bash
python scripts/analysis/gis_epsilon_eparegions.py
```

- Outputs: `results/gis/gis_epsilon_eparegions.json`.
- Verifies: Spearman ρ = 0.18 between qualitative ε and EPA-L4 ε; Watson Brake intersects 7 distinct Level IV ecoregions; Jaketown 99% Loess Plains.

### 4.4 Tier-3 sensitivity extensions (manuscript §4.3, §4.5; supplemental §S8.1)

```bash
python scripts/analysis/tier3_extensions.py
```

- Outputs: per-extension JSON in `results/`.
- Verifies: λ_W sweep traces (0.05–0.30); M_half sweep showing λ_C, λ_X stay near zero across {10, 25, 50, 100, 200}; n_agg sweep at WB parameters; stochastic-environment WB pilot at 22.5% aggregator-share.

### 4.5 σ comparison and distance-decay test

```bash
python scripts/analysis/calculate_sigma_comparison.py
python scripts/analysis/distance_decay_test.py
```

- Outputs: paleoclimate σ table; Spearman ρ = 0.95 across four distance-decay materials.

## 5. Regenerate the figures

Each figure script is independent; order does not matter. Manuscript-figure scripts write to `figures/manuscript/`; supplemental-figure scripts write to `figures/supplemental/`. Filenames match the figure numbers in the manuscript and supplemental.

```bash
# Manuscript figures (output: figures/manuscript/figure_NN_*.{png,pdf})
python scripts/figure_generation/create_figure_01_poverty_point_map.py
python scripts/figure_generation/create_figure_02_site_architecture.py
python scripts/figure_generation/create_figure_03_mls_decomposition.py
python scripts/figure_generation/create_figure_04_ecotone_seasonal.py
python scripts/figure_generation/create_figure_05_fitness_crossover.py
python scripts/figure_generation/create_figure_06_model_architecture.py
python scripts/figure_generation/create_integrated_simulation_figures.py  # Figures 7 + 8
python scripts/figure_generation/create_figure_09_regional_chronology.py
python scripts/figure_generation/create_figure_10_paleoclimate.py
python scripts/figure_generation/create_figure_11_calibration.py          # also runs §4.1 above
python scripts/figure_generation/create_figure_12_gis_ecoregions.py
python scripts/figure_generation/create_figure_13_multi_drainage.py
python scripts/figure_generation/create_figure_14_seasonal_phenology.py

# Supplemental figures (output: figures/supplemental/figure_SNN_*.{png,pdf})
python scripts/figure_generation/create_figure_S05_predictions_summary.py
python scripts/figure_generation/create_figures_S06_S07_sigma_sweeps.py
python scripts/figure_generation/create_figure_S08_obligation_network.py
python scripts/figure_generation/create_figure_S09_exotic_distance_decay.py
python scripts/figure_generation/create_figure_S02_joint_mc_diagnostic.py
```

Or use `make figures` to run them all.

## 6. Build the manuscript docx files

The active draft is the merged JAMT manuscript at `docs/jamt/Manuscript.md` and `docs/jamt/Supplemental.md`. Run `make manuscript` from the project root to rebuild both, or invoke pandoc directly:

```bash
# Active draft: merged JAMT main and supplemental
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

# Earlier-draft archives (preserved for history; not required for current submission):
python scripts/build_manuscript_v2.py    # split v2.0 main + supplemental
pandoc docs/manuscript_AA/Poverty_Point_AA.md \
    -o docs/manuscript_AA/Poverty_Point_AA.docx \
    --reference-doc docs/jamt/reference_template.docx \
    --resource-path docs/manuscript_AA \
    --from markdown --to docx
```

The reference template `docs/jamt/reference_template.docx` controls Times New Roman 11pt, italic figure captions, and other manuscript conventions per the project CLAUDE.md. All four targets above are also wrapped in `make manuscript`.

## 7. Verifying reproduction

Each analysis writes a JSON or CSV result file under `results/`. Comparing your re-run output against the committed file in git (`git diff results/...`) should show no numerical changes if your environment matches the pinned versions in `requirements.txt`. Small floating-point differences (last 2-3 decimal places) can occur across BLAS implementations; the qualitative results in the manuscript are robust to this level of variation.

## 8. Outstanding non-reproducible elements

A handful of model extensions are flagged in §5.5 of the AA manuscript as priority follow-up work and are *not* implemented in the current code release:

- Regime-switching ABM (full bistable simulation of Watson Brake)
- Per-event labor scaling (m³-per-investment-unit varies with crew size)
- Regional spatially-explicit ABM with hydrographic routing and across-site selection
- Signal-conditional partner formation (replacing the uniform 20-30% pair probability)
- Restructured network-saturation function

The continuous-equilibrium analyses they would extend are reproducible from this release; the extensions themselves are forward work.
