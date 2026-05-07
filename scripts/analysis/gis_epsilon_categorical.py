#!/usr/bin/env python3
"""Category-level GIS-epsilon: weight ecoregion distinctness by ecological group.

The fine-grained EPA Level IV ecoregion analysis (gis_epsilon_eparegions.py)
treats every L4 class as equally distinct. But ecologically, "upland" vs
"lowland" are fundamentally different (different species, different shortfall
drivers, different productivity timing) while different lowland subtypes
(Holocene Meander Belt vs Backswamp) are more similar.

This script maps each L4 class to a broad ecological category (alluvial
active, backswamp, pleistocene terrace, loess uplands, tertiary uplands,
coastal marsh, coastal plain uplands, prairies, mountains/hills), then
computes Shannon entropy at the CATEGORY level rather than the fine-grained
L4 level. A site with 7 L4 classes all in alluvial-active gives less actual
ecological diversity than a site with 4 L4 classes spanning upland +
lowland + backswamp.

For each of the 11 sites in Table 1:
1. 25 km foraging buffer
2. Intersect with EPA L4 polygons
3. Map each L4 class to broad category (mapping below)
4. Compute Shannon entropy over area-weighted CATEGORY fractions
5. Compute epsilon = 0.5 * H / ln(N_max_categories)
6. Compare to fine-grained L4 epsilon and qualitative epsilon

Output: results/gis/gis_epsilon_categorical.json
"""
from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point


DATA_DIR = Path(
    '/Users/clipo/PycharmProjects/poverty-point-signaling/data/ecoregions'
)
OUTPUT_DIR = Path(
    '/Users/clipo/PycharmProjects/poverty-point-signaling/results/gis'
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
STATES = ['ar', 'la', 'mexico_la' if False else 'ms']

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

# L4 -> broad ecological category mapping. Categories are defined by
# fundamental ecological distinctness for hunter-gatherer subsistence:
# different shortfall drivers, different species assemblages, different
# productivity timing. Within-category L4 differences are subtle subtypes
# of the same fundamental ecology.
L4_TO_CATEGORY = {
    # Alluvial Active Valley: frequently flooded, river-dominated; fish
    # runs, oxbow waterfowl, riverine mussel beds; flood-pulse driven
    '73a': 'Alluvial Active', '73f': 'Alluvial Active',
    '73h': 'Alluvial Active', '73k': 'Alluvial Active',
    '73g': 'Alluvial Active', '35g': 'Alluvial Active',
    '37b': 'Alluvial Active', '65p': 'Alluvial Active',
    '34c': 'Alluvial Active', '35b': 'Alluvial Active',
    '75i': 'Alluvial Active',
    # Backswamp / Wetland: slow water, seasonal flooding, distinct from
    # active alluvial; cypress-tupelo, slow waterfowl, distinct fishery
    '73d': 'Backswamp', '73i': 'Backswamp', '73m': 'Backswamp',
    '73n': 'Backswamp', '73c': 'Backswamp',
    # Pleistocene Terraces: older, elevated, stable substrate; mast oak
    # forests, terrestrial game; not flood-dominated
    '73b': 'Pleistocene Terrace', '73l': 'Pleistocene Terrace',
    '73j': 'Pleistocene Terrace',  # Macon Ridge (PP's home)
    '35c': 'Pleistocene Terrace', '74d': 'Pleistocene Terrace',
    # Loess Uplands: wind-deposited soils, distinctive vegetation,
    # different from terrace and from active alluvium
    '74a': 'Loess Upland', '74b': 'Loess Upland',  # Jaketown's home
    '74c': 'Loess Upland', '34j': 'Loess Upland',
    # Tertiary Uplands: older bedrock, mixed forest, slow-flowing
    # streams; distinct from Pleistocene terraces
    '35a': 'Tertiary Upland', '35d': 'Tertiary Upland',
    '35e': 'Tertiary Upland', '65d': 'Tertiary Upland',
    '65e': 'Tertiary Upland', '65i': 'Tertiary Upland',
    '65j': 'Tertiary Upland', '65q': 'Tertiary Upland',
    # Coastal Marsh / Estuary: saline, tidal, fundamentally different
    # subsistence (oysters, marine fish, salt-marsh waterfowl)
    '73o': 'Coastal Marsh', '34g': 'Coastal Marsh',
    '75k': 'Coastal Marsh',
    # Coastal Plain Uplands: sandy soils, pine forest, fire-maintained
    '35f': 'Coastal Plain Upland', '65f': 'Coastal Plain Upland',
    '75a': 'Coastal Plain Upland',
    # Prairies: grasslands, bison range historically, distinct flora
    '73e': 'Prairie', '65a': 'Prairie', '35h': 'Prairie',
    '34a': 'Prairie', '65r': 'Prairie', '65b': 'Prairie',
    # Mountains / Hills: igneous/metamorphic substrate, very distinct
    '36a': 'Mountain Hills', '36b': 'Mountain Hills',
    '36c': 'Mountain Hills', '36d': 'Mountain Hills',
    '36e': 'Mountain Hills', '37a': 'Mountain Hills',
    '37c': 'Mountain Hills', '37d': 'Mountain Hills',
    '38a': 'Mountain Hills', '38b': 'Mountain Hills',
    '39a': 'Mountain Hills', '39b': 'Mountain Hills',
    '39c': 'Mountain Hills', '39d': 'Mountain Hills',
}

# Total number of categories (used for Shannon normalization)
N_CATEGORIES = len(set(L4_TO_CATEGORY.values()))

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
    parts = []
    for st in STATES:
        gdf = gpd.read_file(DATA_DIR / f'{st}_eco_l4')
        parts.append(gdf)
    return gpd.GeoDataFrame(pd.concat(parts, ignore_index=True), crs=parts[0].crs)


def shannon(counts: dict) -> float:
    total = sum(counts.values())
    if total <= 0:
        return 0.0
    H = 0.0
    for v in counts.values():
        p = v / total
        if p > 0:
            H -= p * np.log(p)
    return H


def main():
    print('Loading EPA Level IV ecoregions...')
    eco = load_ecoregions()
    eco_a = eco.to_crs('EPSG:5070')
    print(f'  Loaded {len(eco_a)} polygons')
    print(f'  Mapped {len(L4_TO_CATEGORY)} L4 classes to {N_CATEGORIES} categories')

    rows = []
    for name, smith, lon, lat in SITES:
        pt = gpd.GeoSeries([Point(lon, lat)], crs='EPSG:4326').to_crs('EPSG:5070').iloc[0]
        buf = pt.buffer(BUFFER_KM * 1000.0)

        # Intersect ecoregion polygons with buffer
        eco_clip = eco_a[eco_a.intersects(buf)].copy()
        eco_clip['inter_geom'] = eco_clip.geometry.intersection(buf)
        eco_clip['inter_area'] = eco_clip['inter_geom'].area

        # Aggregate by L4 class
        l4_areas = eco_clip.groupby('US_L4CODE')['inter_area'].sum().to_dict()

        # Aggregate by broad category
        cat_areas = {}
        unmapped_area = 0.0
        for l4, area in l4_areas.items():
            cat = L4_TO_CATEGORY.get(l4)
            if cat is None:
                unmapped_area += area
                continue
            cat_areas[cat] = cat_areas.get(cat, 0.0) + area

        # Compute Shannon at L4 and category levels
        l4_areas_km2 = {k: v / 1e6 for k, v in l4_areas.items()}
        cat_areas_km2 = {k: v / 1e6 for k, v in cat_areas.items()}
        H_l4 = shannon(l4_areas_km2)
        H_cat = shannon(cat_areas_km2)
        H_l4_max = np.log(max(2, len(l4_areas_km2)))
        H_cat_max = np.log(max(2, N_CATEGORIES))

        eps_l4 = 0.5 * H_l4 / H_l4_max
        eps_cat = 0.5 * H_cat / H_cat_max

        rows.append({
            'site': name,
            'smithsonian': smith,
            'qual_epsilon': QUAL_EPSILON.get(name),
            'l4_n_classes': len(l4_areas_km2),
            'l4_H': round(H_l4, 4),
            'l4_epsilon': round(eps_l4, 4),
            'category_n': len(cat_areas_km2),
            'category_H': round(H_cat, 4),
            'category_epsilon': round(eps_cat, 4),
            'category_areas_km2': {k: round(v, 1) for k, v in cat_areas_km2.items()},
            'unmapped_area_km2': round(unmapped_area / 1e6, 1),
        })

    print()
    print(f"{'Site':<22} {'qual':>6} {'L4_n':>6} {'L4_eps':>8} {'cat_n':>6} {'cat_eps':>8}")
    print('-' * 60)
    for r in rows:
        print(f"{r['site']:<22} {r['qual_epsilon']:>6.2f} "
              f"{r['l4_n_classes']:>6d} {r['l4_epsilon']:>8.3f} "
              f"{r['category_n']:>6d} {r['category_epsilon']:>8.3f}")
        if r['category_n'] <= 4:
            cats = ', '.join(sorted(r['category_areas_km2'].keys()))
            print(f"  categories: {cats}")
        else:
            cats = sorted(r['category_areas_km2'].items(), key=lambda x: -x[1])
            top = ', '.join(f"{c}: {a:.0f} km²" for c, a in cats[:3])
            print(f"  top categories: {top}")

    # Spearman correlations
    from scipy.stats import spearmanr
    qual = [r['qual_epsilon'] for r in rows]
    l4 = [r['l4_epsilon'] for r in rows]
    cat = [r['category_epsilon'] for r in rows]
    print()
    rho_ql, p_ql = spearmanr(qual, l4)
    rho_qc, p_qc = spearmanr(qual, cat)
    rho_lc, p_lc = spearmanr(l4, cat)
    print(f'Spearman rho (qualitative vs L4): {rho_ql:.3f}, p = {p_ql:.3f}')
    print(f'Spearman rho (qualitative vs category): {rho_qc:.3f}, p = {p_qc:.3f}')
    print(f'Spearman rho (L4 vs category): {rho_lc:.3f}, p = {p_lc:.3f}')

    out = OUTPUT_DIR / 'gis_epsilon_categorical.json'
    with open(out, 'w') as f:
        json.dump({
            'methodology': {
                'buffer_km': BUFFER_KM,
                'n_categories': N_CATEGORIES,
                'l4_to_category': L4_TO_CATEGORY,
                'category_list': sorted(set(L4_TO_CATEGORY.values())),
            },
            'sites': rows,
            'correlations': {
                'qualitative_vs_l4': {'rho': rho_ql, 'p': p_ql},
                'qualitative_vs_category': {'rho': rho_qc, 'p': p_qc},
                'l4_vs_category': {'rho': rho_lc, 'p': p_lc},
            },
        }, f, indent=2)
    print(f'\nSaved: {out}')


if __name__ == '__main__':
    main()
