#!/usr/bin/env python3
"""GIS-based measurement of ecotone diversity for LMV mound sites.

Addresses the §5.4 limitation flagging GIS-implemented epsilon as a
priority empirical refinement. Uses the USGS digitization of Saucier
(1994) (data/geology/Saucier_Geomorph_shapefile/) to compute, for
each of the 11 sites in Table 1:

1. Areal coverage of each geomorphic age class (Holocene Alluvial
   Valley, Holocene Deltaic/Chenier, Pleistocene) within a 25 km
   foraging buffer
2. Shannon diversity over those measured area fractions
3. Predicted epsilon under the Shannon mapping
4. Comparison to the qualitative-weight epsilon used in Table 1

This is a partial implementation: it uses geomorphology only and does
not include vegetation cover (which would distinguish forested from
prairie zones). Even so, it provides an independent empirical check
on the qualitative weights.

Output: results/gis/gis_epsilon_results.json plus a plain-text table
suitable for inclusion in the manuscript.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import geopandas as gpd
from shapely.geometry import Point


SAUCIER_SHP = Path(
    '/Users/clipo/PycharmProjects/poverty-point-signaling/'
    'data/geology/Saucier_Geomorph_shapefile/Saucier_Geomorph.shp'
)

# Sites and coordinates (lon, lat). Canonical source:
# data/sites/late_archaic_sites.csv (see data/sites/README.md for sources
# and trinomial corrections).
SITES = [
    ('Poverty Point',     '16WC5',   -91.4074, 32.6366),  # West Carroll Parish, LA
    ('Lower Jackson',     '16WC10',  -91.4108, 32.6105),  # West Carroll Parish; ~2 km S of PP
    ('Watson Brake',      '16OU175', -92.1311, 32.3684),  # Ouachita Parish, LA
    ('Caney',             '16CT5',   -92.0004, 31.4822),  # Catahoula Parish; Sicily Island Hills
    ("Frenchman's Bend",  '16OU259', -92.0437, 32.6357),  # Ouachita Parish; Bayou Desiard
    ('Insley',            '16FR3',   -91.4791, 32.3893),  # Franklin Parish, LA
    ('J.W. Copes',        '16MA147',  -91.3894, 32.5339),  # Madison Parish, LA (Tensas Basin)
    ('Cowpen Slough',     '16CT147', -91.9346, 31.3293),  # Catahoula Parish; Boeuf River margin
    ('Jaketown',          '22HU505', -90.4872, 33.2349),  # Humphreys County, MS; near Belzoni
    ('Claiborne',         '22HA501', -89.5758, 30.2141),  # Hancock County, MS; Pearl River mouth
    ('Cedarland',         '22HA506', -89.5804, 30.2186),  # Hancock County, MS; adjacent to Claiborne
]

# Foraging buffer radius (km). 25 km is a typical ethnographic
# day-trip radius for mobile foragers (Kelly 2013).
BUFFER_KM = 25.0


def shannon(area_dict):
    total = sum(area_dict.values())
    if total <= 0:
        return 0.0
    p = np.array([v / total for v in area_dict.values() if v > 0])
    return float(-(p * np.log(p)).sum())


def main():
    print(f"Loading Saucier shapefile...")
    gdf = gpd.read_file(SAUCIER_SHP)
    # Keep in projected CRS (Albers Equal Area) for accurate areas
    gdf_albers = gdf.to_crs('EPSG:5070')  # NAD83 Conus Albers
    print(f"  {len(gdf_albers)} polygons; CRS: {gdf_albers.crs.name}")

    rows = []
    for name, smithsonian, lon, lat in SITES:
        # Project site coord to Albers
        pt_wgs = gpd.GeoSeries([Point(lon, lat)], crs='EPSG:4326')
        pt_albers = pt_wgs.to_crs('EPSG:5070').iloc[0]

        # 25 km buffer in meters (Albers is in meters)
        buffer_m = BUFFER_KM * 1000.0
        buf = pt_albers.buffer(buffer_m)

        # Intersect each polygon with the buffer; aggregate areas by Geo_Age
        areas_by_age = {}
        for _, row in gdf_albers.iterrows():
            geom = row.geometry
            geo_age = row['Geo_Age']
            if geom is None or geo_age is None:
                continue
            inter = geom.intersection(buf)
            if inter.is_empty:
                continue
            a = inter.area  # m^2
            if a > 0:
                areas_by_age[geo_age] = areas_by_age.get(geo_age, 0.0) + a

        # Add the 'Outside Saucier mapped extent' bucket (i.e., upland
        # outside the alluvial valley, e.g., the western Pleistocene
        # uplands not specifically mapped). Compute as buffer area minus
        # mapped intersection.
        total_mapped = sum(areas_by_age.values())
        buffer_total_area = buf.area
        outside = max(0.0, buffer_total_area - total_mapped)
        if outside > 0:
            areas_by_age['Outside (upland/non-LMV)'] = outside

        # Convert to km^2 for reporting
        areas_km2 = {k: v / 1e6 for k, v in areas_by_age.items()}
        H = shannon(areas_km2)
        # Maximum possible H given the number of distinct classes
        n_classes = len(areas_km2)
        H_max = np.log(max(n_classes, 1)) if n_classes > 0 else 1.0
        # Map onto epsilon range [0, 0.5] using same convention as
        # qualitative rubric, but normalize by ln(5) for comparability
        H_max_5 = np.log(5)
        eps_gis = 0.5 * H / H_max_5
        # Cap epsilon at 0.5
        eps_gis = min(eps_gis, 0.5)

        rows.append({
            'name': name,
            'smithsonian': smithsonian,
            'H': H,
            'epsilon_gis': eps_gis,
            'n_classes': n_classes,
            'areas_km2': {k: round(v, 1) for k, v in areas_km2.items()},
        })

    # Print table
    print()
    print(f"{'Site':<22} {'#cls':>5} {'H':>5} {'eps_gis':>8}")
    print("-" * 50)
    for r in rows:
        print(f"{r['name']:<22} {r['n_classes']:>5} {r['H']:>5.2f} "
              f"{r['epsilon_gis']:>8.3f}")

    # Compare to qualitative epsilon from Table 1
    qual_eps = {
        'Poverty Point': 0.49, 'Lower Jackson': 0.48,
        'Watson Brake': 0.43, 'Caney': 0.43,
        "Frenchman's Bend": 0.43, 'Insley': 0.43,
        'J.W. Copes': 0.42, 'Cowpen Slough': 0.42,
        'Jaketown': 0.40,
        'Claiborne': 0.30, 'Cedarland': 0.30,
    }
    print()
    print(f"{'Site':<22} {'eps_qual':>9} {'eps_gis':>8} {'diff':>7}")
    print("-" * 50)
    for r in rows:
        q = qual_eps.get(r['name'])
        d = r['epsilon_gis'] - q if q is not None else None
        print(f"{r['name']:<22} {q:>9.2f} {r['epsilon_gis']:>8.3f} "
              f"{d:>+7.3f}")

    # Spearman correlation between qualitative and GIS epsilons
    from scipy.stats import spearmanr
    qual_vals = [qual_eps[r['name']] for r in rows]
    gis_vals = [r['epsilon_gis'] for r in rows]
    rho, p = spearmanr(qual_vals, gis_vals)
    print(f"\nQualitative-vs-GIS Spearman: rho={rho:.3f}, p={p:.3f} (n={len(rows)})")

    # Persist
    out_dir = Path(__file__).resolve().parent.parent.parent / 'results' / 'gis'
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / 'gis_epsilon_results.json', 'w') as f:
        json.dump({
            'sites': rows,
            'qualitative_epsilon': qual_eps,
            'spearman_rho': float(rho),
            'spearman_p': float(p),
            'buffer_km': BUFFER_KM,
        }, f, indent=2)
    print(f"\nWrote {out_dir / 'gis_epsilon_results.json'}")


if __name__ == '__main__':
    main()
