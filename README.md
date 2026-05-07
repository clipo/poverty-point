# Poverty Point Signaling Model

Agent-based model of aggregation-based signaling (group-level index signaling via earthwork construction; band-level index signaling via exotic-goods acquisition) at Poverty Point, Louisiana (ca. 1700-1100 BCE). This project investigates why mobile hunter-gatherers constructed one of the largest earthwork complexes in prehistoric North America while accumulating exotic materials from across the midcontinent.

## Authors

- Carl P. Lipo (Binghamton University, ORCID 0000-0003-4391-3590) — corresponding author
- Diana M. Greenlee (Station Archaeologist, Poverty Point World Heritage Site, University of Louisiana at Monroe)
- Robert J. DiNapoli (Binghamton University, ORCID 0000-0003-2180-2195)

## The Puzzle

Poverty Point encompasses approximately 140 hectares of constructed landscape, including six concentric C-shaped ridges, 36 timber post circles, and Mound A (22 m high, 238,500 cubic meters of fill built in fewer than 90 days). Total earthwork volume is estimated at 750,000 to 1,000,000 cubic meters. Bayesian modeling of 157 radiocarbon dates places the occupation at 164-397 years (3535-3135 cal BP), with active earthwork construction compressed to roughly 75 years (ca. 3300-3225 cal BP). The site also served as a focal point for long-distance exchange networks spanning 1,600+ km (copper, galena, steatite, novaculite). Standard models of hunter-gatherer behavior predict mobility and minimal investment in fixed infrastructure, making this combination of massive collective construction and extensive individual exotic goods acquisition paradoxical.

## The Hypothesis

Poverty Point represents an **adaptive signaling system** operating through seasonal aggregation dynamics. Using multilevel selection theory (Price equation framework), the model shows that when environmental uncertainty exceeds a critical threshold, aggregation with monument construction and exotic-goods acquisition becomes fitness-enhancing:

1. **Environmental uncertainty** creates conditions favoring inter-group cooperation
2. **Seasonal aggregation** at locations with shortfall buffering provides resource stability and cooperation opportunities
3. **Monument construction** functions as a group-level *index* signal of collective cooperative-labor mobilization (the signal is hard to fake because the underlying labor is required to produce it)
4. **Exotic goods** function as band-level *index* signals of long-distance network access (a galena nodule from Potosi cannot be produced by a band that has not directly or indirectly accessed Potosi material)
5. Both signal types solve free-rider, partner-identification, and commitment problems without requiring aggrandizers, religious motivation, or incipient complexity
6. **Multi-drainage shortfall buffering** is the framework's distinctive prediction: aggregation concentrates at sites where multiple resource zones, drawing on independent shortfall drivers, deliver productivity during the periods when surrounding areas are in shortfall. Poverty Point's confluence position integrates four canoe-accessible drainages (Bayou Maçon, Mississippi, Tensas, Yazoo) with non-synchronized hydrographs, the strongest shortfall buffering of any LMV mound-building site

The framework treats convergence dynamics (Grooms et al. 2023; Kidder and Grooms 2024) as the contingent historical fact that supplied attained aggregation size at Poverty Point: multiple groups with independent histories converged on the type-site over a compressed window. Jaketown developed Poverty Point cultural traits 400+ years before the type-site, and exchange networks were distributed rather than radiating from a single center (Ward et al. 2022).

## Key Results

The framework delivers three classes of empirical evaluation: independent tests with stated bounds, calibration anchors, and consistency demonstrations conditional on inputs the framework does not derive. The §6 status table and the §7.4 audit in the manuscript catalog each evaluation explicitly. Headline findings:

- A **sharp phase transition** at $\sigma^* = 0.40$ at PP-scenario parameters ($\varepsilon = 0.35$, $n_{agg} = 25$), validated against the agent-based simulation in §4.1. The §4.2 phase-space diagram across the joint $(\sigma, \varepsilon)$ plane confirms the analytical threshold line accurately separates aggregator-dominated from independent-dominated regimes across the parameter space.
- **Signaling-vs-cooperation ablation (§4.3)**: signal-conditional partner formation does not move the threshold relative to a model in which the same number of cooperative ties form by random pairing ($\sigma_{eff}^*$ shifts by 2.4%, within replicate noise). The framework's discriminating empirical content lies on the spatial-flow dimension (§6.1), not the threshold-location dimension.
- **Paleoclimate threshold-proximity (§6.2, near-tie)**: Bayesian propagation places $P(\sigma_{eff} > \sigma^*) = 0.36$-$0.56$ across plausible $\varepsilon$ priors. Joint propagation including six $\sigma^*$-defining model parameters (each ±50%) gives $P = 0.33$, robust against the conditioning caveat that $\sigma^*$ is calibrated to PP-scenario operation.
- **Type-site calibration (anchor, not test)**: model output scales to ~750,000 m³ of earthwork (~77 m³ per investment unit) over the active interval. The scaling factor is fit to the archaeological target.
- **Distance-decay (acknowledged not to discriminate)**: Spearman ρ = 0.95 across four exotic materials by source distance, $R^2 \approx 0.87$ at the 500 km characteristic length scale. The framework explicitly does not claim this distinguishes signaling from generic transport-cost or down-the-line exchange alternatives.
- **Per-material posterior predictive check (§6.1)**: copper consistent (model 178 vs archaeological 155, predictive interval contains observation); galena overpredicts (~55% recovery loss reconciles); steatite consistent on a vessel basis. Joint Mahalanobis $d^2 = 110$ rejects under no-correction interpretation; cross-material correlations $r = 0.85$-$0.97$ for steatite/galena/novaculite/crystal-quartz mean apparent independence of marginal checks is overstated.
- **Watson Brake (§6.3, consistency demonstration with three free parameters)**: 30× volume overprediction under continuous-equilibrium operation closes to 0.8× under per-event labor scaling at $\alpha = 2.0$ + regime-switching at $K = 3$ + $\sigma_{sd} = 0.10$-$0.125$. Erasmus's (1965) experimental rate of 2.6 m³/person-day implies $\alpha \approx 1$ under additive labor accounting; $\alpha = 2$ requires superadditive scaling beyond what Erasmus supports.
- **Cross-LMV screening (§6.4, sample-selection-bounded)**: under the static-diversity rubric, all nine interior monument-building sites pass the necessity condition (high-$\varepsilon$ band); the coastal Pearl River pair (Claiborne, Cedarland) falls below. The discrimination is interior-vs-coastal, not a magnitude predictor. GIS-derived static $\varepsilon$ correlations are null with both qualitative-rubric $\varepsilon$ ($\rho = 0.22$ for Saucier-geomorphic; $\rho = -0.02$ for EPA Level IV) and observed monument scale ($\rho \approx 0$), confirming that 25-km terrestrial buffer ecological diversity is not the operative quantity (see §6.5 below).
- **Multi-drainage shortfall buffering (§6.5, descriptive)**: modern USGS gauge data identify three substantively independent shortfall regimes at Poverty Point's confluence (Macon Ridge: Bayou Maçon + Tensas at $r = 0.90$ functioning as one; Mississippi mainstem; Yazoo Basin), the strongest multi-regime buffering among LMV mound-building sites. The temporal phenology hierarchy (§6.7, Figure 14) converges on the same conclusion: PP integrates five independent resource-peak windows, more than any other LMV site. Modern-as-proxy concession explicit.
- **Cross-site magnitude (§6.6, not predicted by the framework)**: joint $M_g(\varepsilon, n_{agg})$ correlation across 11 LMV sites returns Spearman ρ = +0.85 to +0.91, but partial-correlation decomposition shows this is essentially the exogenous $n_{agg}$ ranking from the convergence-model literature; $\varepsilon$ contributes ≤ +0.014 marginal correlation. The framework's $\varepsilon$ is a necessity-condition variable, not a magnitude predictor.
- **The visitor-band outflow asymmetry test (§7.4(f))** is identified as the genuinely signaling-discriminating empirical work the framework calls for; not performed in this article.

## Manuscript

The primary submission targets **Journal of Archaeological Method and Theory** (JAMT) and combines the theoretical framework with empirical evaluation against the Lower Mississippi Valley record:

| Component | Path |
|---|---|
| **Main text** | `docs/jamt/Manuscript.{md,docx}` |
| **Supplemental** | `docs/jamt/Supplemental.{md,docx}` |
| **Reference template** (pandoc styling) | `docs/jamt/reference_template.docx` |
| **Outline** | `docs/jamt/Merged_JAMT_Outline.md` |
| **Peer-review report** | `docs/jamt/peer_review_report.md` |
| **Source-check report** | `docs/jamt/source_check_report.md` |
| **Change log** | `CHANGELOG.md` |

The manuscript opens with Poverty Point as the canonical case, develops the multilevel-selection threshold framework, formalizes it in an ABM (motivated by Lewontin's 1974 distinction between dynamic and empirical sufficiency), validates the analytical predictions against agent-based simulation in §4 (phase transition, phase-space structure, signaling-vs-cooperation ablation, sensitivity), and evaluates the framework against the LMV record in §6 (eight evaluations catalogued in the §6 status table as calibration anchors, independent tests with stated bounds, or consistency demonstrations). Engages explicitly with cultural-historical accounts (Sanger 2023/2024 institutional flexibility; Kidder and Grooms 2025 revitalization; Sassaman 2005 structure-event-process; Carballo 2013 collective-action institutions; Peacock and Rafferty 2013 bet-hedging) and with the methodological challenge of evaluating mechanistic models against records assembled under culture-historical paradigms (Perreault 2019).

Supplemental structure:

- **§S1** ODD Protocol (complete model specification with signal-conditional receiver-response apparatus); §S1.4 includes the σ normalization-invariance demonstration
- **§S2** Parameter estimation and justification (Tables S1 symbol glossary; S2 full parameter list)
- **§S3** Sensitivity analyses; §S3.1 includes the joint parameter uncertainty propagation result for §6.2; §S3.6 documents the coupling-form sensitivity (multiplicative vs additive vs hazard composition)
- **§S4** Supplemental theoretical figures
- **§S5** Two unnumbered structural-architecture extensions (near-threshold parameter sweep; restructured network-saturation function)
- **§S6** Zone-access scoring rubric for Table 2
- **§S7-§S9** Detailed scenario results, testable predictions, supplemental empirical figures
- **§S10** Watson Brake bistable analysis
- **§S11-§S14** Magnitude-prediction gaps, GIS ecoregion comparison, Monte Carlo perturbation, per-material exotic decomposition
- **§S15** Modern hydrograph data: empirical test of multi-drainage independence
- **§S16** Seasonal resource phenology
- **§S17** Six numbered model components used in §6 (regime switching, per-event labor scaling, regional band allocation, water-route catchment, per-site $n_{agg}$ scale ratios, seasonally resolved aggregation timing) plus a consolidated list of priority follow-up work

### Predecessor manuscripts (archival)

Older drafts are preserved in `docs/_archive/` for version history but are not part of the active build. See `docs/_archive/README.md` for what each contains and how to rebuild any archived draft if needed:

- `docs/_archive/manuscript_AA/` — single-file *American Antiquity*–format draft
- `docs/_archive/manuscript_v2.0/` — split *JAS v2* draft (separate main and supplemental)
- `docs/_archive/manuscript_old/` — earliest single-file JAS-format drafts and various dated revisions plus method-development notes

These were merged into the current JAMT manuscript on 2026-05-03 to remove the dependency that paper 2 could not be submitted until paper 1 was accepted, and to let JAMT reviewers evaluate theory and application in one pass.

## Project Structure

```
poverty-point-signaling/
├── src/poverty_point/              # Core simulation package
│   ├── simulation.py               # Main simulation engine
│   ├── core_simulation.py          # Core simulation logic
│   ├── integrated_simulation.py    # Full integrated simulation (signal-conditional toggle)
│   ├── signaling_core.py           # Signaling equilibrium calculations
│   ├── agents.py                   # Band agent behavior and decisions
│   ├── environment.py              # Multi-zone resource dynamics
│   ├── environmental_scenarios.py  # Scenario definitions
│   └── parameters.py               # Model parameters
├── scripts/
│   ├── figure_generation/          # Active scripts producing Figures 1-14 + S1-S9
│   │   ├── README.md               # Figure-to-script mapping; "active vs archive" convention
│   │   └── _archive/               # Legacy figure scripts from earlier drafts (16 scripts)
│   ├── analysis/                   # GIS ε, sigma comparison, sensitivity, partial correlations
│   ├── data_extraction/            # PDF and data extraction tools
│   ├── exploration/                # Parameter space exploration
│   └── build_manuscript_v2.py      # Builds the archived v2.0 docx (active build is `make manuscript`)
├── data/
│   ├── site_coordinates.csv        # Canonical site coordinates (lat/lon and UTM) for 11 LMV sites
│   ├── site utms.xlsx              # Source UTM coordinates from field survey
│   ├── calibration/                # Archaeological calibration data
│   ├── paleoclimate/               # Paleoclimate proxy records
│   ├── geology/                    # USGS Saucier 1994 LMV geomorphology
│   ├── ecoregions/                 # EPA Level IV ecoregions (AR, LA, MS)
│   ├── compiled/                   # Compiled datasets
│   └── raw/                        # Raw source data
├── docs/
│   ├── jamt/                       # Active JAMT manuscript (Manuscript.md/.docx, Supplemental.md/.docx, reference template)
│   ├── _archive/                   # Older drafts (manuscript_AA, manuscript_v2.0, manuscript_old) preserved for history
│   ├── references/                 # Reference pipeline (44+ processed sources)
│   │   ├── claims/                 # Claims extractions with page numbers
│   │   ├── summaries/              # Structured source summaries
│   │   ├── INDEX.md                # Master reference index
│   │   ├── crosscheck_log.md       # Verification audit log
│   │   └── methods_code_alignment_report.md
│   ├── paper1_theory/              # Split-paper theoretical draft (legacy)
│   ├── paper2_empirical/           # Split-paper empirical draft (legacy)
│   ├── working/                    # Working notes
│   └── evidence/                   # Evidence documentation
├── figures/
│   ├── manuscript/                 # 14 active manuscript figures, named figure_NN_*.png/.pdf to match figure numbers
│   │   └── README.md               # Figure-to-script mapping
│   ├── supplemental/               # 9 active supplemental figures, named figure_SNN_*.png/.pdf to match figure numbers
│   │   └── README.md               # Figure-to-script mapping
│   ├── final/                      # Legacy outputs from earlier drafts (preserved for backwards compatibility)
│   └── integrated/                 # Legacy outputs from earlier drafts
├── results/
│   ├── analysis/                   # Sigma sweep, phase space, calibration JSON
│   ├── calibration_replicates/     # Figure 11 replicate-spread data
│   ├── gis/                        # GIS-ε analysis results
│   ├── sensitivity/                # OAT, joint Monte Carlo, regional band allocation, etc.
│   └── tier3/                      # Tier-3 sensitivity extensions
├── Makefile                        # `make analyses`, `make figures`, `make manuscript`, `make all`, `make calibration`
├── requirements.txt                # Pinned package versions (Python 3.12.2)
├── REPRODUCE.md                    # Step-by-step reproduction guide
└── tests/                          # Test suite
```

## Model Architecture

The simulation consists of three interacting modules:

**Environment Module**: Four ecological zones (aquatic, terrestrial, mast, ecotone) with seasonal productivity cycles, stochastic shortfalls, and inter-zone negative covariance. Ecotone locations provide variance reduction through portfolio effects, with effective uncertainty $\sigma_{eff} = \sigma(1-\varepsilon)$.

**Agent Module**: Bands (15-30 individuals) choose annually between AGGREGATOR and INDEPENDENT strategies based on expected fitness. Aggregators travel to a central site, invest in monuments, acquire exotic goods, and form reciprocal obligation networks. Under signal-conditional mode (default), tie formation probability scales with each band's normalized monument-and-exotic display level (focal probability 0.20 + 0.20 × normalized own-display, partner-choice weights 0.5× to 1.5×); shortfall help is tie-strength weighted (strongest ties tapped first, multi-call until need is met); and aggregator network density augments local ε via $\varepsilon_{eff} = \varepsilon + (1-\varepsilon) \beta \rho$. Strategy decisions are probabilistic with a small softmax temperature ($\tau = 0.1$).

**Simulation Controller**: Executes a four-phase annual cycle (spring dispersal, summer aggregation, fall harvest, winter reproduction) over 200-500 year runs. Calibration uses 8 stochastic replicates of 200 simulated years per scenario.

The agent-based model serves as a **dynamic-sufficiency test** in Lewontin's (1974) sense: it asks whether the framework's individual-level mechanisms, when implemented as agent-level rules, actually produce the predicted aggregate behavior (sharp phase transition, lock-in dynamics, monument-network feedback) under stochastic, finite-population, spatially explicit conditions. Empirical sufficiency (whether the framework accounts for the LMV record) is a separate question, addressed in §6.

## Theoretical Framework

The model extends the Price equation for multilevel selection:

**Aggregator fitness**: $W_{agg} = (1 - C_{total})(1 - \alpha(k_{eff}) \sigma_{eff})(1 - m(1-r) P_{base}) + B(\lambda)$

**Independent fitness**: $W_{ind} = (1 - \beta(k_0) \sigma)(1 - m P_{base})$

where $C_{total}$ is the aggregation cost (travel + signaling labor + opportunity), $\alpha(k) = 1/(1+\gamma k)$ is the network-mediated vulnerability function, $\sigma_{eff} = \sigma(1-\varepsilon)$ is the locally-buffered uncertainty, $r$ is monument-mediated conflict reduction, and $B(\lambda)$ is the within-group signaling benefit averaged over the band-quality distribution. The framework's $\varepsilon$ encodes shortfall buffering through negative covariance between local zone productivity and the regional shortfall driver, not raw zone count.

The critical threshold $\sigma^*$ where aggregation becomes adaptive is solved numerically with Brent's (1973) method on the lambda-sigma feedback loop. With Poverty Point parameters ($\varepsilon = 0.49$ from Shannon-derived ecotone diversity, $n_{agg} = 25$), $\sigma^* \approx 0.36$.

## Reproducibility

The repository includes pinned dependency versions (`requirements.txt`) and a step-by-step regeneration guide (`REPRODUCE.md`). All stochastic simulations use deterministic seeds; running the canonical commands in REPRODUCE.md produces numerically identical outputs to those reported in the manuscripts and supplemental.

**Quick start.** From the project root:

```bash
make analyses    # rerun all analyses (GIS-ε, σ comparison, distance decay, sensitivity)
make figures     # regenerate every figure into figures/manuscript/ and figures/supplemental/
make manuscript  # rebuild active jamt docx (docs/jamt/Manuscript.docx + Supplemental.docx)
make all         # analyses + figures + manuscript (skips slow calibration; run that explicitly)
make calibration # rerun the Tier-3 calibration replicates (~3 hours; produces Figure 11)
```

Figure-to-script mappings live in `figures/manuscript/README.md`, `figures/supplemental/README.md`, and `scripts/figure_generation/README.md`. Each active figure-generation script is named to match the figure number it produces (e.g., `create_figure_07_phase_transition.py` → Figure 7), and writes its output directly into the corresponding `figures/manuscript/` or `figures/supplemental/` folder with a clean numbered filename. Legacy scripts from earlier drafts are kept in `scripts/figure_generation/_archive/` for reference. See `REPRODUCE.md` for the full step-by-step.

External data dependencies:

| Dataset | Repo path | Source |
|---------|-----------|--------|
| LMV site UTM coordinates | `data/site utms.xlsx`, `data/site_coordinates.csv` | Field survey (NAD83, UTM Zone 15N for nine interior LA/MS sites; Zone 16N for the coastal MS pair) |
| Saucier (1994) LMV geomorphology | `data/geology/Saucier_Geomorph_shapefile/` | USGS ScienceBase 59b7ddd6e4b08b1644df5cf6 (doi:10.5066/F7N878QN) |
| EPA Level IV ecoregions (LA, MS, AR) | `data/ecoregions/{la,ms,ar}_eco_l4/` | EPA Office of Research and Development |

## Reference Pipeline

The project maintains a systematic reference pipeline with 44+ processed sources. Each source has:
- **Claims extraction**: Specific claims with page numbers, typed by evidence category
- **Structured summary**: Relevance assessment, key data, methodological notes, cross-source connections
- **INDEX entry**: Searchable by tags (chronology, construction, environment, signaling, exchange, etc.)

Key recent additions include revised Bayesian chronologies (Kidder and Grooms 2024), the convergence thesis (Grooms et al. 2023), rapid construction evidence (Kidder et al. 2021), ritual space documentation (Clay 2023; Hargrave et al. 2021), flood-driven collapse data (Kidder et al. 2018), and theoretical engagement with bet-hedging (Peacock and Rafferty 2013), institutional flexibility (Sanger 2023), the archaeology of awe (Sanger 2024), revitalization (Kidder and Grooms 2025), the multilevel-selection framework on territorial cases (DiNapoli et al. 2019), and ethnographic grounding for $\lambda_W$ (Hawkes 2000; Hawkes and Bliege Bird 2002; Wiessner 2002). Lewontin (1974) was added to motivate the dynamic-sufficiency framing of the ABM.

## Geology and Ecoregion Data

**Figure 1** uses the USGS digitization of Saucier (1994) Lower Mississippi River Valley geomorphology (ScienceBase item 59b7ddd6e4b08b1644df5cf6, doi:10.5066/F7N878QN, public domain). The figure distinguishes Holocene deposits (Mississippi alluvial valley, deltaic and chenier plains) from Pleistocene deposits (Wisconsin Stage valley trains, Prairie Complex including Macon Ridge, Deweyville Complex). Poverty Point's coordinates (NAD83, UTM Zone 15N: 649390 E / 3612125 N → 32.6366 N, −91.4074 W) fall on the Pleistocene `Pve` formation at the eastern margin of Macon Ridge. Site coordinates for all eleven Table 1 sites are drawn from `data/site_coordinates.csv`, derived from field-surveyed UTMs in `data/site utms.xlsx`.

**Figure 12** (and supplemental GIS analyses) use the EPA Office of Research and Development Level IV ecoregion classification (Omernik and Griffith 2014). Ecoregion shapefiles for Arkansas, Louisiana, and Mississippi are loaded from `data/ecoregions/{ar,la,ms}_eco_l4/`. The figure shows the 11 LMV mound-building sites with their 25 km foraging buffers overlaid on the Level IV polygon background. Watson Brake's buffer crosses the highest count of distinct Level IV polygons (7) of any LMV site, with Caney (6) and Frenchman's Bend (6) close behind; PP integrates 4. The 25-km terrestrial-buffer count does not predict observed monument scale. The framework's ε is operative through the *covariance-based* multi-drainage analysis of §6.5 (Figure 13) and the temporal-staggering analysis of §6.7 (Figure 14), not through static-buffer ecological diversity.

## Dependencies

See `requirements.txt` for pinned versions. Tested with Python 3.12.2 on macOS.

- NumPy 2.4.3, SciPy 1.17.1, Pandas 3.0.1
- Matplotlib 3.10.8, Seaborn 0.13.2, NetworkX 3.3
- GeoPandas 1.1.0, Cartopy 0.25.0, Shapely 2.1.1, PyProj 3.6.1, Rasterio 1.4.2 (geospatial; conda-forge recommended on macOS)
- python-docx 1.1.0, PyYAML 6.0.1, tqdm 4.66.5
- Pandoc ≥ 3.0 (system package; for Markdown to Word conversion)

## Usage

See `REPRODUCE.md` for the complete reproduction runbook. Quick examples (run from project root):

Generate all figures:
```bash
make figures
```

Generate Figure 1 only (regional map with Saucier geology and 11 LMV sites):
```bash
PYTHONPATH=src python scripts/figure_generation/create_figure_01_poverty_point_map.py
```

Generate the calibration replicates (Figure 11; ~3 hours for the underlying simulation):
```bash
make calibration
```

Build the active JAMT manuscript and supplemental Word documents:
```bash
make manuscript
```

Build an archived draft (e.g., AA single-file):
```bash
pandoc docs/_archive/manuscript_AA/Poverty_Point_AA.md \
    -o docs/_archive/manuscript_AA/Poverty_Point_AA.docx \
    --reference-doc docs/jamt/reference_template.docx \
    --resource-path docs/_archive/manuscript_AA \
    --from markdown --to docx
```

## Related Projects

This project applies the multilevel-selection signaling framework developed in parallel studies:
- **Rapa Nui** (Easter Island): Moai and ahu as territorial signals (DiNapoli et al. 2019)
- **Chaco Canyon**: Great houses and exotic goods as dual signaling channels

The theoretical framework (multilevel selection via the Price equation) is shared across all three projects, but model mechanics differ: Rapa Nui and Chaco are agriculturalists with territorial fixity; Poverty Point is a fission-fusion mobile-forager system in which cooperation is re-established with partial strangers each year. The aggregator/independent strategy formalism, the seasonal four-phase annual cycle, and the multi-drainage shortfall-buffering ε formulation are specific to the Poverty Point case.

## Key References

- Bliege Bird, R., Smith, E.A. 2005. Signaling theory, strategic interaction, and symbolic capital. *Current Anthropology* 46:221-248.
- Brent, R.P. 1973. *Algorithms for Minimization without Derivatives*. Prentice-Hall.
- Carballo, D.M. (Ed.) 2013. *Cooperation and Collective Action: Archaeological Perspectives*. University Press of Colorado.
- Clay, R.B. 2023. Two types of ritual space at the Poverty Point Site 16WC5. *American Antiquity* 88:187-206.
- DiNapoli, R.J., et al. 2019. Rapa Nui (Easter Island) monument (ahu) locations explained by freshwater sources. *PLoS ONE* 14:e0210409.
- Gibson, J.L. 2000. *The Ancient Mounds of Poverty Point: Place of Rings*. University Press of Florida.
- Grooms, S.B., Ward, G.M.V., Kidder, T.R. 2023. Convergence at Poverty Point. *Antiquity* 97:1453-1469.
- Hawkes, K., Bliege Bird, R. 2002. Showing off, handicap signaling, and the evolution of men's work. *Evolutionary Anthropology* 11(2):58-67.
- Kidder, T.R., Grooms, S.B. 2024. Chronological hygiene and Bayesian modeling of Poverty Point sites. *American Antiquity* 89:98-118.
- Kidder, T.R., Grooms, S.B. 2025. Performance, ritual, and revitalization at Poverty Point. *Southeastern Archaeology*, in press.
- Kidder, T.R., Henry, E.R., Arco, L.J. 2018. Rapid climate change-induced collapse. *Science China Earth Sciences* 61:178-189.
- Lewontin, R.C. 1974. *The Genetic Basis of Evolutionary Change*. Columbia University Press.
- Omernik, J.M., Griffith, G.E. 2014. Ecoregions of the conterminous United States. *Environmental Management* 54:1249-1266.
- Ortmann, A.L., Kidder, T.R. 2013. Building Mound A at Poverty Point. *Geoarchaeology* 28(1):66-86.
- Peacock, E., Rafferty, J. 2013. The bet-hedging model and Eastern Woodlands earthworks. In Fontijn et al. (eds.), *Beyond Barrows*, pp. 253-279. Sidestone Press.
- Sanger, M.C. 2023. Anarchy, institutional flexibility, and containment of authority at Poverty Point. *World Archaeology* 54:555-571.
- Sanger, M.C. 2024. The archaeology of awe. *Journal of Archaeological Method and Theory* 31:1462-1484.
- Sassaman, K.E. 2005. Poverty Point as structure, event, process. *Journal of Archaeological Method and Theory* 12(4):335-364.
- Saunders, J.W., et al. 2005. Watson Brake, a Middle Archaic mound complex. *American Antiquity* 70:631-668.
- Saucier, R.T. 1994. *Geomorphology and Quaternary Geologic History of the Lower Mississippi Valley*. U.S. Army Corps of Engineers, Vicksburg.
- Ward, G.M.V., et al. 2022. The view from Jaketown. *American Antiquity* 87:758-775.
- Wiessner, P. 2002. Hunting, healing, and Hxaro exchange. *Evolutionary Anthropology* 11(2):63-65.
