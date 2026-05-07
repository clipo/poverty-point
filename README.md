# Poverty Point Signaling Model

Code, data, figures, and manuscript files for:

> Lipo, C.P., Greenlee, D.M., DiNapoli, R.J. (forthcoming). *Signaling under environmental uncertainty: A multilevel-selection threshold model for Poverty Point.* Journal of Archaeological Method and Theory.

This is a reproducibility-focused subset of the project: it contains exactly what is needed to regenerate every analysis, figure, and the JAMT main and supplemental Word documents from the same source code that produced the submitted manuscript. Internal documentation (predecessor drafts, the reference pipeline, working notes, and peer-review artefacts) is not mirrored here; it is kept in the project's working repository.

The manuscript itself is included so that readers can follow the cross-references between the prose, the figures, the analysis outputs, and the model code without having to download anything else:

| | Path |
|---|---|
| Manuscript | `docs/jamt/Manuscript.md`, `docs/jamt/Manuscript.docx` |
| Supplemental | `docs/jamt/Supplemental.md`, `docs/jamt/Supplemental.docx` |
| Pandoc reference template | `docs/jamt/reference_template.docx` |

## Authors

- Carl P. Lipo (Binghamton University, ORCID 0000-0003-4391-3590) — corresponding author
- Diana M. Greenlee (Station Archaeologist, Poverty Point World Heritage Site, University of Louisiana at Monroe)
- Robert J. DiNapoli (Binghamton University, ORCID 0000-0003-2180-2195)

## Quick start

From the project root:

```bash
# 1. Set up the Python environment (Python 3.12.2; see Dependencies below for conda alternative)
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Reproduce
make analyses    # GIS-ε, σ comparison, distance decay, sensitivity, partial correlations
make figures     # Regenerate every figure into figures/manuscript/ and figures/supplemental/
make manuscript  # Rebuild docs/jamt/Manuscript.docx and Supplemental.docx via pandoc
make all         # analyses + figures + manuscript (skips slow calibration)
make calibration # Tier-3 calibration replicates (~3 hours; produces the data behind Figure 11)
```

All stochastic simulations use deterministic seeds, so a clean `make all` should produce numerically identical results to the committed JSON outputs in `results/` and the figures committed in `figures/manuscript/` and `figures/supplemental/`.

`REPRODUCE.md` walks through the same steps script by script and documents the seeding strategy, the external data sources, and the expected outputs of each command.

## What's in this repository

```
poverty-point/
├── src/poverty_point/              # Core simulation package
│   ├── simulation.py               # Main simulation engine
│   ├── core_simulation.py          # Core simulation logic
│   ├── integrated_simulation.py    # Full integrated simulation (signal-conditional toggle)
│   ├── signaling_core.py           # Signaling equilibrium and Brent's-method threshold solver
│   ├── agents.py                   # Band agent behavior and decisions
│   ├── environment.py              # Multi-zone resource dynamics
│   ├── environmental_scenarios.py  # Scenario definitions
│   └── parameters.py               # Model parameters
├── scripts/
│   ├── figure_generation/          # 18 scripts producing Figures 1-14 and S1-S9
│   │   └── README.md               # Figure-to-script mapping
│   ├── analysis/                   # GIS-ε (Saucier, EPA L4, categorical), sigma comparison,
│   │                               # sensitivity, partial correlations, joint Monte Carlo,
│   │                               # distance decay, hydrograph covariance, regional band
│   │                               # allocation, signal-conditional tests
│   └── data_extraction/            # PDF and data extraction tools
├── data/
│   ├── site_coordinates.csv        # Canonical site coordinates (lat/lon and UTM) for the 11 LMV sites
│   ├── site utms.xlsx              # Source UTM coordinates from field survey (NAD83)
│   ├── sites/                      # Late Archaic site catalogue with trinomial corrections
│   ├── calibration/                # Archaeological calibration data
│   ├── paleoclimate/               # Paleoclimate proxy records (Temp12k, Salonen et al. 2025, etc.)
│   ├── geology/                    # USGS Saucier 1994 LMV geomorphology shapefiles
│   └── ecoregions/                 # EPA Level IV ecoregion shapefiles (AR, LA, MS, US)
├── docs/
│   └── jamt/                       # Active JAMT manuscript and supplemental
│       ├── Manuscript.md           # Main-text source (markdown)
│       ├── Manuscript.docx         # Built docx (pandoc + reference_template.docx)
│       ├── Supplemental.md         # Supplemental source
│       ├── Supplemental.docx       # Built docx
│       └── reference_template.docx # Pandoc reference template (Times New Roman 11pt, italic captions)
├── figures/
│   ├── manuscript/                 # 14 manuscript figures, named figure_NN_*.png/.pdf to match figure numbers
│   │   └── README.md               # Figure-to-script mapping
│   └── supplemental/               # 9 supplemental figures, named figure_SNN_*.png/.pdf to match figure numbers
│       └── README.md               # Figure-to-script mapping
├── results/                        # Canonical JSON outputs from each analysis (committed for verification)
│   ├── ablation/                   # Phase-transition sweep, signal-conditional vs random-partner
│   ├── analysis/                   # Sigma sweep, phase space, calibration JSON
│   ├── bayesian/                   # Joint parameter Monte Carlo, threshold posterior
│   ├── calibration_replicates/     # Figure 11 replicate-spread data (Tier-3 calibration)
│   ├── gis/                        # GIS-ε analysis results (Saucier, EPA L4, categorical)
│   └── sensitivity/                # OAT, regional band allocation, partial correlations, coupling form, etc.
├── tests/                          # Test suite for the core simulation package
├── Makefile                        # `make analyses`, `make figures`, `make manuscript`, `make all`, `make calibration`
├── requirements.txt                # Pinned package versions (Python 3.12.2)
├── REPRODUCE.md                    # Step-by-step reproduction guide
└── README.md                       # This file
```

## Dependencies

Tested with Python 3.12.2 on macOS. See `requirements.txt` for pinned package versions.

```bash
# Option A: pip + venv (pure-Python paths)
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Option B: conda (recommended for the geospatial stack on macOS / Windows)
conda create -n poverty-point python=3.12 -c conda-forge \
    numpy=2.4.3 scipy=1.17.1 pandas=3.0.1 matplotlib=3.10.8 \
    seaborn=0.13.2 networkx=3.3 cartopy=0.25.0 geopandas=1.1.0 \
    shapely=2.1.1 pyproj=3.6.1 rasterio=1.4.2 \
    python-docx=1.1.0 pyyaml=6.0.1 tqdm=4.66.5
conda activate poverty-point
```

Pandoc ≥ 3.0 is required for the `make manuscript` step; install via `brew install pandoc` on macOS or your OS package manager.

## External data sources

Two external geospatial datasets are referenced by Figure 1 and the GIS-ε analyses. Both are public-domain and are committed in this repo at the paths below; the original sources are listed for citation and verification.

| Dataset | Repo path | Source |
|---|---|---|
| LMV site UTM coordinates | `data/site utms.xlsx`, `data/site_coordinates.csv` | Field survey (NAD83, UTM Zone 15N for the nine interior LA/MS sites; Zone 16N for the coastal MS pair) |
| Saucier (1994) LMV geomorphology | `data/geology/Saucier_Geomorph_shapefile/` | USGS ScienceBase 59b7ddd6e4b08b1644df5cf6 (doi:10.5066/F7N878QN) |
| EPA Level IV ecoregions (LA, MS, AR, US) | `data/ecoregions/{la,ms,ar,us}_eco_l4/` | EPA Office of Research and Development |

Paleoclimate proxy data (Temp12k, Salonen et al. 2025, hurricane landfall reconstructions, etc.) used by Figure 10 are committed in `data/paleoclimate/`.

## Verifying reproduction

Each analysis writes a JSON result file under `results/`. After `make analyses`, comparing your re-run output against the committed file (`git diff results/...`) should show no numerical changes if your environment matches the pinned versions in `requirements.txt`. Small floating-point differences in the last 2-3 decimal places can occur across BLAS implementations; the qualitative results in the manuscript are robust to this level of variation. See `REPRODUCE.md` §7 for verification details.

## License and attribution

If you use the model code, the analyses, or the figures in your own work, please cite the manuscript above and the relevant external data sources (USGS, EPA, paleoclimate proxies) as documented in the manuscript references.

## Project working repository

The full project working repository (with predecessor manuscript drafts, reference pipeline, peer-review reports, working notes, and legacy figure scripts) is at `https://github.com/clipo/poverty-point-signaling`. That repository is intended for project members and contains substantial internal documentation that is not necessary for reproducing the published results.
