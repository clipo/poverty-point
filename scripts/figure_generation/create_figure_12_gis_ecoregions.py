#!/usr/bin/env python3
"""Supplemental Figure: LMV sites overlaid on EPA Level IV ecoregions.

Visual support for §S8.3 (EPA Level IV ecoregion analysis). Shows the
11 LMV mound-building sites in Table 1 with their 25-km foraging buffer
circles overlaid on the EPA Level IV ecoregion polygon background,
making the cross-site differences in ecological catchment heterogeneity
visible at a glance.

Data: EPA Office of Research and Development, Level IV ecoregions
(loaded from data/ecoregions/{ar,la,ms}_eco_l4/) and site coordinates
matching scripts/analysis/gis_epsilon_eparegions.py.

Output: figures/manuscript/figure_12_gis_ecoregions.{png,pdf}
"""
from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely.geometry import Point

DATA_DIR = Path(
    '/Users/clipo/PycharmProjects/poverty-point-signaling/data/ecoregions'
)
OUTPUT_DIR = Path(
    '/Users/clipo/PycharmProjects/poverty-point-signaling/figures/manuscript'
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STATES = ['ar', 'la', 'ms']

# Canonical source: data/sites/late_archaic_sites.csv (see
# data/sites/README.md for trinomial corrections and source notes).
SITES = [
    # (display name, smithsonian, lon, lat, dx, dy)
    # dx, dy are the label-offset in degrees from the marker position.
    # Offsets are tuned so labels do not overlap and each label sits on
    # the side of its marker away from neighbouring markers. Geographic
    # order matters: Frenchman's Bend (32.64 N) is *north* of Watson
    # Brake (32.37 N), so FB's label goes ABOVE its marker and WB's goes
    # BELOW its marker (they would otherwise visually swap).
    ('Poverty Point',     '16WC5',   -91.4074, 32.6366,  0.30,  0.22),
    ('Lower Jackson',     '16WC10',  -91.4108, 32.6105, -0.32, -0.08),
    ('Watson Brake',      '16OU175', -92.1311, 32.3684, -0.22, -0.22),
    ("Frenchman's Bend",  '16OU259', -92.0437, 32.6357, -0.22,  0.22),
    ('Caney',             '16CT5',   -92.0004, 31.4822, -0.22,  0.00),
    ('Insley',            '16FR3',   -91.4791, 32.3893,  0.32, -0.10),
    ('J.W. Copes',        '16MA147', -91.3894, 32.5339,  0.32,  0.10),
    ('Cowpen Slough',     '16CT147', -91.9346, 31.3293,  0.22,  0.00),
    ('Jaketown',          '22HU505', -90.4872, 33.2349,  0.22,  0.00),
    ('Claiborne',         '22HA501', -89.5758, 30.2141,  0.22,  0.22),
    ('Cedarland',         '22HA506', -89.5804, 30.2186,  0.22, -0.22),
]

BUFFER_KM = 25.0


def load_ecoregions():
    """Load and concat the three state ecoregion shapefiles."""
    parts = []
    for st in STATES:
        p = DATA_DIR / f'{st}_eco_l4'
        gdf = gpd.read_file(p)
        parts.append(gdf)
    combined = pd.concat(parts, ignore_index=True)
    return gpd.GeoDataFrame(combined, crs=parts[0].crs)


def main():
    print('Loading EPA Level IV ecoregions for AR, LA, MS...')
    eco = load_ecoregions()
    print(f'  Loaded {len(eco)} polygons; CRS = {eco.crs}')

    # Project to a planar CRS for accurate buffers (USA Contiguous Albers)
    albers = 'EPSG:5070'
    eco_a = eco.to_crs(albers)

    # Build site-buffer GeoDataFrame in same CRS
    sites_records = []
    for name, smith, lon, lat, dx, dy in SITES:
        pt = gpd.GeoSeries([Point(lon, lat)], crs='EPSG:4326').to_crs(albers).iloc[0]
        sites_records.append({
            'name': name, 'smithsonian': smith,
            'geometry': pt, 'buffer': pt.buffer(BUFFER_KM * 1000.0),
            'lon': lon, 'lat': lat, 'dx': dx, 'dy': dy,
        })
    sites_df = gpd.GeoDataFrame(sites_records, crs=albers)

    # Bounding box covers all site buffers + a bit of context
    bufs = list(sites_df['buffer'])
    union = bufs[0]
    for b in bufs[1:]:
        union = union.union(b)
    minx, miny, maxx, maxy = union.bounds
    pad = 60_000  # 60 km padding
    bbox = (minx - pad, miny - pad, maxx + pad, maxy + pad)

    # Clip ecoregions to bbox to reduce rendering load
    eco_clip = eco_a.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]
    print(f'  After clip: {len(eco_clip)} polygons in bbox')

    # Color assignment per Level IV class within the clipped area
    # Use a discrete categorical colormap
    classes = sorted(eco_clip['US_L4CODE'].dropna().unique())
    n_classes = len(classes)
    print(f'  Distinct Level IV classes in bbox: {n_classes}')
    cmap = plt.colormaps['tab20']
    colors = {cls: cmap((i % 20) / 20.0) for i, cls in enumerate(classes)}

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 9
    fig, ax = plt.subplots(figsize=(11, 8))

    # Plot ecoregions colored by L4 class
    for cls in classes:
        sub = eco_clip[eco_clip['US_L4CODE'] == cls]
        sub.plot(ax=ax, color=colors[cls], edgecolor='gray',
                 linewidth=0.2, alpha=0.55)

    # Plot 25-km buffer circles for each site
    for _, row in sites_df.iterrows():
        is_pp = row['name'] == 'Poverty Point'
        edge_color = '#d62728' if is_pp else '#ff7f0e'
        gpd.GeoSeries([row['buffer']], crs=albers).plot(
            ax=ax, facecolor='none', edgecolor=edge_color,
            linewidth=2.2 if is_pp else 1.5, linestyle='-' if is_pp else '--',
            alpha=0.9,
        )

    # Plot site markers
    for _, row in sites_df.iterrows():
        is_pp = row['name'] == 'Poverty Point'
        marker = '*' if is_pp else 'o'
        size = 350 if is_pp else 90
        ax.scatter([row['geometry'].x], [row['geometry'].y],
                   marker=marker, s=size,
                   color='#d62728' if is_pp else '#ff7f0e',
                   edgecolor='black', linewidth=1.2, zorder=10)

    # Site labels (project the offset back from EPSG:4326 dx/dy degrees).
    # Draws a thin leader line from the marker to the label so the
    # attribution stays clear even after offsetting labels to avoid overlap.
    for _, row in sites_df.iterrows():
        # Offset in degrees, convert to Albers
        offset_pt = gpd.GeoSeries(
            [Point(row['lon'] + row['dx'], row['lat'] + row['dy'])],
            crs='EPSG:4326'
        ).to_crs(albers).iloc[0]
        marker_x, marker_y = row['geometry'].x, row['geometry'].y
        is_pp = row['name'] == 'Poverty Point'
        weight = 'bold' if is_pp else 'normal'
        size_ = 11 if is_pp else 8
        color_ = '#d62728' if is_pp else 'black'
        ax.annotate(
            f"{row['name']}\n({row['smithsonian']})",
            xy=(marker_x, marker_y),
            xytext=(offset_pt.x, offset_pt.y),
            ha='left' if row['dx'] > 0 else 'right',
            va='center', fontsize=size_, fontweight=weight, color=color_,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.92,
                      edgecolor='gray', linewidth=0.5),
            arrowprops=dict(arrowstyle='-', color='#555555', lw=0.6,
                            alpha=0.8, shrinkA=0, shrinkB=4),
            zorder=11,
        )

    ax.set_xlim(bbox[0], bbox[2])
    ax.set_ylim(bbox[1], bbox[3])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

    # Scale bar (100 km in Albers meters)
    sb_x = bbox[0] + 50_000
    sb_y = bbox[1] + 30_000
    sb_len = 100_000
    ax.plot([sb_x, sb_x + sb_len], [sb_y, sb_y], 'k-', linewidth=3)
    ax.text(sb_x + sb_len / 2, sb_y - 12_000, '100 km',
            ha='center', va='top', fontsize=9, fontweight='bold')

    # No embedded title (per project CLAUDE.md figure-style convention:
    # descriptive information goes in the caption, not on the figure).

    # Legend explanation (sites + buffer)
    legend_handles = [
        plt.Line2D([0], [0], marker='*', color='w',
                   markerfacecolor='#d62728', markeredgecolor='black',
                   markersize=15, label='Poverty Point (16WC5)'),
        plt.Line2D([0], [0], marker='o', color='w',
                   markerfacecolor='#ff7f0e', markeredgecolor='black',
                   markersize=10, label='Other LMV mound sites'),
        plt.Line2D([0], [0], color='#d62728', linewidth=2.2,
                   label='25 km foraging buffer (PP)'),
        plt.Line2D([0], [0], color='#ff7f0e', linewidth=1.5, linestyle='--',
                   label='25 km foraging buffer (other sites)'),
        mpatches.Patch(facecolor='lightgray', edgecolor='gray', alpha=0.55,
                       label=f'EPA Level IV ecoregion polygons\n'
                             f'({n_classes} distinct classes shown)'),
    ]
    ax.legend(handles=legend_handles, loc='upper right', fontsize=8,
              framealpha=0.92, title='Legend')

    plt.tight_layout()

    # Output filenames match the current Figure 13 numbering (filename of
    # the generator script is retained for backward compatibility).
    out_png = OUTPUT_DIR / 'figure_13_gis_ecoregions.png'
    out_pdf = OUTPUT_DIR / 'figure_13_gis_ecoregions.pdf'
    fig.savefig(out_png, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(out_pdf, bbox_inches='tight', facecolor='white')
    print(f'\nSaved:\n  {out_png}\n  {out_pdf}')


if __name__ == '__main__':
    main()
