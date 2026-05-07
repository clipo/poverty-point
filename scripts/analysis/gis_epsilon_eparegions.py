#!/usr/bin/env python3
"""GIS-based epsilon using EPA Level IV ecoregions (improved version).

Replaces the geomorphology-only analysis (gis_epsilon.py) with the
richer EPA Level IV ecoregion classification, which captures both
geomorphology AND vegetation/wetland zones. The EPA L4 categories
distinguish, for example, Macon Ridge (73j), Northern Holocene
Meander Belts (73a), Northern Backswamps (73d), Pleistocene Fluvial
Terraces (35c), Tertiary Uplands (35a), Gulf Coast Flatwoods (75a),
and Coastal Marshes (73o). This is much closer to the ecological
heterogeneity the model's epsilon parameter represents.

Data: EPA Office of Research and Development, ecoregions of the
continental United States, Level IV. State shapefiles loaded
from data/ecoregions/{ar,la,ms}_eco_l4/.

For each of the 11 sites in Table 1:
1. Compute 25-km foraging buffer
2. Intersect with EPA L4 polygons
3. Compute Shannon entropy over area-weighted L4 class fractions
4. Compute epsilon = 0.5 * H / ln(5)
5. Compare to qualitative epsilon

Output: results/gis/gis_epsilon_eparegions.json
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


DATA_DIR = Path(
    '/Users/clipo/PycharmProjects/poverty-point-signaling/data/ecoregions'
)
STATES = ['ar', 'la', 'ms']  # Arkansas, Louisiana, Mississippi

# Sites and coordinates (lon, lat). Canonical source:
# data/sites/late_archaic_sites.csv (see data/sites/README.md for sources
# and trinomial corrections).
SITES = [
    ('Poverty Point',     '16WC5',   -91.4074, 32.6366),
    ('Lower Jackson',     '16WC10',  -91.4108, 32.6105),
    ('Watson Brake',      '16OU175', -92.1311, 32.3684),
    ('Caney',             '16CT5',   -92.0004, 31.4822),
    ("Frenchman's Bend",  '16OU259', -92.0437, 32.6357),
    ('Insley',            '16FR3',   -91.4791, 32.3893),
    ('J.W. Copes',        '16MA147',  -91.3894, 32.5339),
    ('Cowpen Slough',     '16CT147', -91.9346, 31.3293),
    ('Jaketown',          '22HU505', -90.4872, 33.2349),
    ('Claiborne',         '22HA501', -89.5758, 30.2141),
    ('Cedarland',         '22HA506', -89.5804, 30.2186),
]

BUFFER_KM = 25.0

# Qualitative epsilon from Table 1 for comparison
QUAL_EPSILON = {
    'Poverty Point': 0.49, 'Lower Jackson': 0.48,
    'Watson Brake': 0.43, 'Caney': 0.43,
    "Frenchman's Bend": 0.43, 'Insley': 0.43,
    'J.W. Copes': 0.42, 'Cowpen Slough': 0.42,
    'Jaketown': 0.40,
    'Claiborne': 0.30, 'Cedarland': 0.30,
}


def load_ecoregions():
    """Load and concat the three state ecoregion shapefiles."""
    parts = []
    for st in STATES:
        p = DATA_DIR / f'{st}_eco_l4'
        gdf = gpd.read_file(p)
        parts.append(gdf)
    combined = pd.concat(parts, ignore_index=True)
    return gpd.GeoDataFrame(combined, crs=parts[0].crs)


def shannon(area_dict):
    total = sum(area_dict.values())
    if total <= 0:
        return 0.0
    p = np.array([v / total for v in area_dict.values() if v > 0])
    return float(-(p * np.log(p)).sum())


def main():
    print('Loading EPA L4 ecoregions for AR + LA + MS...')
    eco = load_ecoregions()
    print(f'  {len(eco)} polygons in CRS {eco.crs.name}')
    print(f'  L4 classes: {eco["US_L4CODE"].nunique()} unique')

    H_max_5 = np.log(5)  # for epsilon mapping

    rows = []
    for name, smithsonian, lon, lat in SITES:
        # Project site to the same CRS as the ecoregions
        pt_wgs = gpd.GeoSeries([Point(lon, lat)], crs='EPSG:4326')
        pt_albers = pt_wgs.to_crs(eco.crs).iloc[0]
        buf = pt_albers.buffer(BUFFER_KM * 1000.0)

        # Compute area of each L4 class within buffer
        areas = {}
        for _, row in eco.iterrows():
            geom = row.geometry
            if geom is None:
                continue
            inter = geom.intersection(buf)
            if inter.is_empty:
                continue
            a = inter.area
            if a > 0:
                key = f"{row['US_L4CODE']}: {row['US_L4NAME']}"
                areas[key] = areas.get(key, 0.0) + a

        # Convert to km^2
        areas_km2 = {k: v / 1e6 for k, v in areas.items()}
        H = shannon(areas_km2)
        n_classes = len(areas_km2)
        # Map to epsilon range [0, 0.5] using ln(5) normalization for
        # consistency with the qualitative rubric
        eps_gis = min(0.5, 0.5 * H / H_max_5)

        rows.append({
            'name': name,
            'smithsonian': smithsonian,
            'H': H,
            'n_l4_classes': n_classes,
            'epsilon_gis_l4': eps_gis,
            'top_classes': sorted(areas_km2.items(),
                                  key=lambda x: -x[1])[:5],
        })

    print()
    print(f"{'Site':<22} {'#L4':>4} {'H':>5} {'eps_gis_l4':>10} {'eps_qual':>9} {'diff':>6}")
    print('-' * 70)
    for r in rows:
        q = QUAL_EPSILON[r['name']]
        d = r['epsilon_gis_l4'] - q
        print(f"{r['name']:<22} {r['n_l4_classes']:>4} {r['H']:>5.2f} "
              f"{r['epsilon_gis_l4']:>10.3f} {q:>9.2f} {d:>+6.2f}")

    print()
    print('Top L4 classes per site (with km^2):')
    for r in rows:
        print(f"\n  {r['name']}:")
        for cls, a in r['top_classes']:
            print(f"    {a:>7.1f} km^2  {cls}")

    # Spearman correlations
    from scipy.stats import spearmanr
    qual_vals = [QUAL_EPSILON[r['name']] for r in rows]
    gis_vals = [r['epsilon_gis_l4'] for r in rows]
    rho_qual_gis, p_qual_gis = spearmanr(qual_vals, gis_vals)
    print(f"\nQualitative epsilon vs GIS-L4 epsilon: rho={rho_qual_gis:.3f}, "
          f"p={p_qual_gis:.3f} (n={len(rows)})")

    # Persist
    out_dir = Path(__file__).resolve().parent.parent.parent / 'results' / 'gis'
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / 'gis_epsilon_eparegions.json', 'w') as f:
        json.dump({
            'sites': [
                {k: v for k, v in r.items() if k != 'top_classes'}
                for r in rows
            ],
            'top_classes_per_site': {
                r['name']: r['top_classes'] for r in rows
            },
            'qualitative_epsilon': QUAL_EPSILON,
            'spearman_qual_vs_gis_l4': {
                'rho': float(rho_qual_gis),
                'p': float(p_qual_gis),
                'n': len(rows),
            },
            'buffer_km': BUFFER_KM,
            'data_source': 'EPA Office of Research and Development, '
                           'Ecoregions of the United States, Level IV',
        }, f, indent=2)
    print(f"\nWrote {out_dir / 'gis_epsilon_eparegions.json'}")


if __name__ == '__main__':
    main()
