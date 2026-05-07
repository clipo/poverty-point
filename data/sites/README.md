# Late Archaic Site Locations

Canonical site locations used by Figure 1 (regional map) and the GIS-ε analyses
(`scripts/analysis/gis_epsilon*.py`).

## File: `late_archaic_sites.csv`

Columns:

| Column | Description |
|--------|-------------|
| `name` | Site name as referenced in the manuscript |
| `trinomial` | Smithsonian trinomial (state-county-site) |
| `parish_or_county` | Civil division per published site reports |
| `state` | LA or MS |
| `landform` | Geomorphic context per published site descriptions |
| `longitude` | Decimal degrees, WGS84 |
| `latitude` | Decimal degrees, WGS84 |
| `coord_precision_km` | Approximate radius (km) within which the published site location lies |
| `coord_source` | How the lat/lon were derived |
| `site_source` | Primary published references for the site |

## Trinomial corrections from the previous version

Three trinomials in earlier project files were incorrect; they have been
corrected here with the canonical sources cited:

- **Frenchman's Bend**: `16OU269` → `16OU259` (Saunders, Allen, and Saucier
  1994, *Southeastern Archaeology* 13:134-153; Saunders et al. 2005).
- **Insley**: `16FR2` → `16FR3` (Girard and McGimsey 2022, *Louisiana
  Comprehensive Archaeological Plan*).
- **J.W. Copes**: `16TE2` → `16MA47`, parish corrected from Tensas to
  Madison Parish, LA (Jackson 1982a; Jackson 1990; Kidder and Grooms 2024).
  The trinomial `16TE2` belongs to a different site (Osceola, Tensas
  Parish), and the two have been confused in earlier compilations because
  both are Tensas Basin Late Archaic / Poverty Point-period sites.

## Note on Insley vs. Linsley

Two distinct sites are sometimes confused in the literature:

- **Insley** (`16FR3`), Franklin Parish, LA: the Middle Archaic mound
  complex on Macon Ridge attested by Sassaman 2005:340-341.
- **Linsley** (`16OR40`), Orleans Parish, LA: a different site appearing
  in Kidder and Grooms 2024 figures.

Only Insley (`16FR3`) is included in the analyses for this project.

## Coordinate precision

These coordinates are approximate centroids of the published site or its
described landform locale. They place each site (a) within its correct
parish or county per published site reports, and (b) within its correct
landform (Macon Ridge, Pleistocene terrace, Yazoo Basin, etc.). Precise
feature-level coordinates are protected for many of these sites under
archaeological resource protection laws and are not appropriate for
publication. The km-scale precision recorded in `coord_precision_km` is
sufficient for both the regional map (Figure 1) and the EPA Level IV
ecoregion sampling used in the GIS-ε analyses, where ecoregion polygons
span tens of km.
