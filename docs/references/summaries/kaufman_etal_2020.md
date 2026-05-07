# Summary: Kaufman et al. 2020

**Full citation**: Kaufman, D. et al. 2020. A global database of Holocene paleotemperature records. *Scientific Data* 7:115.
**PDF filename**: s41597-020-0445-3.pdf
**Date summarized**: 2026-03-21
**Pipeline status**: summary

---

## Relevance to Argument

This paper presents the Temperature 12k database, a global compilation of 1319 quality-controlled, multi-proxy Holocene paleotemperature records from 679 sites. The database is directly relevant to the Poverty Point signaling model because it provides the empirical basis for calibrating environmental variability (sigma) during the Poverty Point period (~3700-3100 BP). All records in the database cover the interval 8500-3500 BP, guaranteeing complete temporal coverage of the Poverty Point occupation. The dominant signal across all proxy types is Neoglacial cooling from peak Holocene warmth (~6500-5000 BP) through the late Holocene, and the Poverty Point occupation falls squarely within this cooling phase. North America has comparatively high site density in the database, and the 30-60 degrees N latitude band that includes Poverty Point is the most data-rich region. The database is available in machine-readable formats (LiPD, R, Python, MATLAB), enabling systematic extraction of records nearest the lower Mississippi Valley for parameterizing the model.

## Key Claims

| Claim | Page | Type | Strength | Notes |
|-------|------|------|----------|-------|
| Database compiles 1319 temperature-sensitive proxy records from 679 sites, covering the past 12,000 years at sub-millennial resolution (median spacing 400 years or finer) | p. 1 | Methodological | Strong | Defines scope; sub-millennial resolution ensures Poverty Point period is represented |
| Records derive from lake sediment (51%), marine sediment (31%), peat (11%), glacier ice (3%), and other archives | p. 1 | Empirical | Strong | Lake and marine sediments dominate (82%); lake sediments are the primary archive for SE North America |
| 51% of sites located within 60-30 degrees N; spatial density comparatively high in North America and Europe | p. 6 | Empirical | Strong | Poverty Point (32.63 degrees N) falls within the most data-rich latitude band |
| All sites include data between 8.5 and 3.5 ka; average record length within the Holocene is 9813 years | p. 6 | Empirical | Strong | Guarantees every record covers the Poverty Point period (~3700-3100 BP) |
| 91% of records extend back at least 6000 years | p. 6 | Empirical | Strong | Captures full climatic context leading into Poverty Point period |
| Median record resolution is 164 years; 15% of records have 50-year or finer resolution, 39% have 51-150 year resolution | p. 6 | Empirical | Strong | ~3-4 data points per record spanning the ~600-year Poverty Point occupation; only high-resolution subset captures centennial variability |
| 74% of sites include annual temperature estimates; 64% have summer, 39% have winter reconstructions | p. 6 | Empirical | Strong | Seasonal records relevant for assessing seasonal resource uncertainty |
| Average chronological control for radiocarbon-dated sequences is 1.0 age per 1000 years | p. 6 | Empirical | Strong | Poverty Point period (~3700-3100 BP) may have at most one independent age control point per record |
| All composites show cooling trend by 6000 years ago across all proxy types | p. 7 | Empirical | Strong | Key finding: Poverty Point occupation occurs during Neoglacial cooling phase |
| In the 30-60 degrees N band, summer, winter, and annual composites all decline from peak values around 6000-5000 BP | pp. 7-8 | Empirical | Strong | Confirms cooling in the latitude band most relevant to Poverty Point |
| Global cooling of approximately 0.5 degrees C from 6500 BP to late Holocene (pre-industrial) | p. 8 | Empirical | Strong | Quantifies the temperature decline during and after Poverty Point; shifts in growing season, species distributions, and resource availability |
| High-resolution composites exhibit greater variability than low-resolution composites | p. 8 | Empirical | Strong | High-resolution records better capture centennial-scale temperature fluctuations relevant to sigma calibration |
| Proxy locations explain 93-100% of temperature variance in latitudinal bands when validated against instrumental data | pp. 8-9 | Empirical | Strong | 30-60 degrees N band: R-squared = 0.98 (HadCRUT4), 0.96 (ERA20C); confirms spatial representativeness |
| Proxy locations explain 94% of variance in mid-Holocene minus preindustrial changes across 12 PMIP3 climate models | p. 9 | Empirical | Strong | Validates database for Holocene temperature trend reconstruction |
| Calibration uncertainties are less important when investigating relative magnitude of temperature changes rather than absolute temperature | p. 11 | Methodological | Strong | The signaling model requires relative variability (sigma), not absolute temperature |
| Only 39% of sites have records with resolution finer than 100 years | p. 13 | Empirical | Strong | Limits the number of records useful for centennial-scale variability assessment near Poverty Point |
| Most North American pollen-based records are from the Marsicek et al. synthesis using the modern analogue technique | p. 5 | Methodological | Strong | Marsicek et al. (2018) is the backbone of North American terrestrial paleotemperature coverage |
| Database available in LiPD, MATLAB, Python, and R formats at DOI 10.25921/4RY2-G808 | p. 17 | Empirical | Strong | Enables direct programmatic extraction of records for model parameterization |

## Data Presented

The database contains 1319 paleotemperature time series from 679 globally distributed sites. Records span 470 terrestrial and 209 marine sites, with 715 records from lake sediments, 359 from marine sediments, and 245 from other terrestrial archives. No primary data are generated in this paper; the contribution is the compilation, quality control, and standardization of previously published proxy records into a unified, machine-readable database. Composite temperature curves (z-score standardized, 500-year bins) are presented globally, by proxy type, by latitude band, by season, by archive type, and by resolution class. Validation is provided against instrumental temperature data (HadCRUT4, ERA20C) and mid-Holocene climate model output (PMIP3 ensemble).

## Methodological Notes

Selection criteria include peer-reviewed publication, demonstrated temperature sensitivity, minimum 4000-year record length, sub-millennial resolution (median spacing 400 years or finer), and at least one age control point every 3000 years. Quality screening criteria were relaxed in data-sparse regions. Compositing involved z-score standardization (mean zero, variance 1 SD over entire record length) and 500-year binning, which smooths centennial-scale variability. The 500-year binning means that the ~600-year Poverty Point occupation is represented by at most one or two composite bins (~3500-3000 BP and ~4000-3500 BP). For finer-scale sigma calibration, individual high-resolution records from the database would need to be extracted and analyzed at their native resolution rather than relying on the composites.

Three categories of uncertainty are identified by the authors: (1) calibration and proxy biases, which affect the magnitude of reconstructed temperature changes; (2) chronological uncertainty, which affects the timing of inferred changes; and (3) spatiotemporal coverage, which affects how well the database represents any specific region. All three are relevant when applying this database to the lower Mississippi Valley.

## Connections to Other Sources

- **Marsicek et al. 2018** (*Nature* 554:92): Primary source for North American pollen-based paleotemperature records in the database. Demonstrated millennial-scale cooling after ~5500 BP, consistent with the composites presented here.
- **PAGES 2k Consortium**: The global composite is calibrated by aligning the 500-1500 CE mean with the PAGES 2k global temperature reconstruction.
- **PMIP3 climate models**: Used for spatial validation of the proxy network's representativeness for mid-Holocene temperature patterns.
- Paleoclimate context established here supports the environmental uncertainty argument developed in the Poverty Point signaling model: Neoglacial cooling would have increased resource unpredictability, potentially creating conditions favoring aggregation-based costly signaling.
- Regional paleoclimate studies (speleothem, pollen) from the Gulf Coast and Mississippi Valley can be cross-referenced against this global compilation to assess whether local trends match the zonal composites.

## Verification Notes

Claims were extracted from the published PDF (Scientific Data 7:115). All quantitative values (record counts, resolution statistics, validation R-squared values, temperature magnitudes) are drawn directly from the text and figures of the paper. The database itself (version 1.0.0) is publicly available at NOAA/NCEI (www.ncdc.noaa.gov/paleo/study/27330) and can be independently verified. No discrepancies were identified between the claims file and the published paper. The full author list for the citation includes 93 co-authors; the citation is abbreviated as "Kaufman, D. et al." following the claims file convention, but should be expanded in any final manuscript citation to meet journal requirements.
