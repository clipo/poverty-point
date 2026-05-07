#!/usr/bin/env python3
"""
Create Figure 1: Regional Map of Poverty Point and Exchange Network

Shows:
- Main panel: Lower Mississippi Valley with Holocene vs. Wisconsin
  Stage Pleistocene surficial deposits (after Saucier 1981, 1994)
- Inset: Southeastern US context
- Poverty Point and ten other Late Archaic / Middle Archaic
  monument-building sites (the eleven LMV sites in Table 1)
- Arrows for exotic material source directions
- Scale bar and north arrow

Uses Natural Earth shapefiles via cartopy.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Polygon as MplPolygon
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from pathlib import Path

OUTPUT_DIR = Path('/Users/clipo/PycharmProjects/poverty-point-signaling/figures/manuscript')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SAUCIER_SHP = Path(
    '/Users/clipo/PycharmProjects/poverty-point-signaling/data/geology/'
    'Saucier_Geomorph_shapefile/Saucier_Geomorph.shp'
)

# Publication formatting
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 11
plt.rcParams['hatch.linewidth'] = 0.4

# Poverty Point coordinates
PP_LAT = 32.6366
PP_LON = -91.4074


def add_scale_bar(ax, lon, lat, length_km, transform):
    """Add a scale bar to the map."""
    km_per_deg = 111.32 * np.cos(np.radians(lat))
    length_deg = length_km / km_per_deg
    ax.plot([lon, lon + length_deg], [lat, lat], 'k-', linewidth=3, transform=transform)
    ax.plot([lon, lon + length_deg], [lat, lat], 'w-', linewidth=1.5, transform=transform)
    ax.text(lon + length_deg / 2, lat - 0.15, f'{length_km} km',
            ha='center', va='top', fontsize=9, fontweight='bold', transform=transform)


def add_north_arrow(ax, x, y, transform):
    """Add a north arrow."""
    ax.annotate('N', xy=(x, y + 0.5), xytext=(x, y),
                ha='center', va='bottom', fontsize=12, fontweight='bold',
                arrowprops=dict(arrowstyle='->', lw=2, color='black'),
                transform=transform)


def create_regional_map():
    """Create the regional map figure."""
    proj = ccrs.PlateCarree()

    fig = plt.figure(figsize=(10, 12))

    # Main panel: Lower Mississippi Valley
    ax_main = fig.add_axes([0.08, 0.05, 0.84, 0.70], projection=proj)
    main_extent = [-94, -88, 29.5, 35.5]
    ax_main.set_extent(main_extent, crs=proj)

    # Base features
    ax_main.add_feature(cfeature.LAND, facecolor='#f5f0e1', edgecolor='none')
    ax_main.add_feature(cfeature.OCEAN, facecolor='#d4e6f1')
    ax_main.add_feature(cfeature.LAKES, facecolor='#d4e6f1', edgecolor='#6699cc', linewidth=0.5)
    ax_main.add_feature(cfeature.RIVERS, edgecolor='#6699cc', linewidth=0.8)
    ax_main.add_feature(cfeature.STATES, edgecolor='gray', linewidth=0.5, linestyle='--')

    # =====================================================================
    # Surficial geology from USGS digitization of Saucier (1994)
    # ScienceBase item 59b7ddd6e4b08b1644df5cf6 (doi:10.5066/F7N878QN).
    # The Geo_Age field classifies polygons as Holocene (alluvial valley
    # and deltaic-chenier plains) vs. Pleistocene (Wisconsin Stage valley
    # trains, Prairie Complex including Macon Ridge, Deweyville Complex,
    # etc.). The classification is the source's, not ours.
    # =====================================================================
    saucier = gpd.read_file(SAUCIER_SHP).to_crs('EPSG:4326')
    # Clip to map extent for plotting speed
    saucier = saucier.cx[main_extent[0]:main_extent[1],
                         main_extent[2]:main_extent[3]]

    holocene = saucier[saucier['Geo_Age'].str.startswith('Holocene')]
    pleistocene = saucier[saucier['Geo_Age'] == 'Pleistocene']

    # Pleistocene first (zorder 1), then Holocene over it (zorder 2) where
    # they overlap at boundaries.
    pleistocene.plot(
        ax=ax_main, transform=proj,
        facecolor='#e8d6b8', edgecolor='#8c6f3a',
        hatch='....', linewidth=0.4, alpha=0.85, zorder=1,
    )
    holocene.plot(
        ax=ax_main, transform=proj,
        facecolor='#cfe2cf', edgecolor='#5a8a5a',
        hatch='///', linewidth=0.4, alpha=0.85, zorder=2,
    )


    # Zone labels (positioned to avoid overlap with site labels)
    ax_main.text(-89.95, 33.55, 'Yazoo Basin\n(Holocene)',
                 fontsize=9, fontstyle='italic', color='#2f5d2f', ha='center',
                 transform=proj, fontweight='bold', zorder=5,
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, edgecolor='none'))
    ax_main.text(-91.85, 32.95, 'Macon Ridge\n(Pleistocene)',
                 fontsize=9, fontstyle='italic', color='#6f4d1f', ha='center',
                 transform=proj, fontweight='bold', zorder=5,
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, edgecolor='none'))

    # =====================================================================
    # Sites
    # =====================================================================
    # Poverty Point — type site
    ax_main.plot(PP_LON, PP_LAT, marker='*', color='#d62728', markersize=22,
                 markeredgecolor='black', markeredgewidth=1.5, transform=proj, zorder=10)
    ax_main.text(PP_LON + 0.30, PP_LAT + 0.18, 'Poverty Point\n(16WC5)',
                 fontsize=11, fontweight='bold', color='#d62728',
                 transform=proj, zorder=10,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                           alpha=0.9, edgecolor='#d62728'))

    # Other Late Archaic / Middle Archaic monument-building & PP-period sites.
    # Canonical source: data/sites/late_archaic_sites.csv (see
    # data/sites/README.md for trinomial corrections and source notes).
    other_sites = [
        # name, smithsonian, lon, lat, label_dx, label_dy, label_anchor
        # Coordinates derived from data/site utms.xlsx (NAD83, UTM Zone 15N for
        # interior LA/MS sites; Zone 16N for the coastal MS pair). See Table 1.
        ('Jaketown',         '22HU505', -90.4872, 33.2349,  0.22,  0.00, 'left'),
        ('Watson Brake',     '16OU175', -92.1311, 32.3684, -0.18,  0.20, 'right'),
        ("Frenchman's Bend", '16OU259', -92.0437, 32.6357, -0.18, -0.28, 'right'),
        ('Lower Jackson',    '16WC10',  -91.4108, 32.6105,  0.30,  0.05, 'left'),   # stacked between PP label (y=32.81) and J.W. Copes label (y=32.53), all anchored at x ~ -91.11
        ('Insley',           '16FR3',   -91.4791, 32.3893, -0.18,  0.00, 'right'),
        ('Caney',            '16CT5',   -92.0004, 31.4822, -0.18,  0.00, 'right'),
        ('Cowpen Slough',    '16CT147', -91.9346, 31.3293,  0.20,  0.00, 'left'),
        ('J.W. Copes',       '16MA147', -91.3894, 32.5339,  0.22,  0.00, 'left'),   # label to RIGHT, clear of Lower Jackson
        ('Claiborne',        '22HA501', -89.5758, 30.2141,  0.20,  0.20, 'left'),
        ('Cedarland',        '22HA506', -89.5804, 30.2186,  0.20, -0.20, 'left'),
    ]
    for name, smith, lon, lat, dx, dy, anchor in other_sites:
        ax_main.plot(lon, lat, marker='o', color='#ff7f0e', markersize=8,
                     markeredgecolor='black', markeredgewidth=1,
                     transform=proj, zorder=8)
        ax_main.text(lon + dx, lat + dy, f'{name}\n({smith})',
                     fontsize=8, fontstyle='italic', ha=anchor, va='center',
                     transform=proj, zorder=9,
                     bbox=dict(boxstyle='round,pad=0.18', facecolor='white',
                               alpha=0.75, edgecolor='none'))

    # =====================================================================
    # Exotic material source arrows
    # =====================================================================
    # Copper - Great Lakes (~N)
    ax_main.annotate('', xy=(-90.5, 35.3), xytext=(PP_LON, PP_LAT),
                     arrowprops=dict(arrowstyle='->', lw=2.5, color='#d4760a'),
                     transform=proj)
    ax_main.text(-90.3, 35.1, 'Copper\n(Great Lakes,\n~1600 km)',
                 fontsize=8.5, fontweight='bold', color='#d4760a', ha='left',
                 transform=proj,
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85))

    # Steatite - Appalachians (~E)
    ax_main.annotate('', xy=(-88.1, 33.5), xytext=(PP_LON, PP_LAT),
                     arrowprops=dict(arrowstyle='->', lw=2.5, color='#7570b3'),
                     transform=proj)
    ax_main.text(-88.3, 34.05, 'Steatite\n(S. Appalachians,\n~800-900 km)',
                 fontsize=8.5, fontweight='bold', color='#7570b3', ha='center',
                 transform=proj,
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85))

    # Galena - Missouri (~N)
    ax_main.annotate('', xy=(-91.8, 35.3), xytext=(PP_LON, PP_LAT),
                     arrowprops=dict(arrowstyle='->', lw=2.5, color='#636363'),
                     transform=proj)
    ax_main.text(-92.5, 35.10, 'Galena\n(Missouri,\n~800 km)',
                 fontsize=8.5, fontweight='bold', color='#636363', ha='center',
                 transform=proj,
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85))

    # Novaculite - Ouachita Mtns (~W)
    ax_main.annotate('', xy=(-93.8, 33.5), xytext=(PP_LON, PP_LAT),
                     arrowprops=dict(arrowstyle='->', lw=2.5, color='#e7298a'),
                     transform=proj)
    ax_main.text(-93.85, 34.05, 'Novaculite\n(Ouachita,\n~250-300 km)',
                 fontsize=8.5, fontweight='bold', color='#e7298a', ha='center',
                 transform=proj,
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.85))

    # Scale bar and north arrow
    add_scale_bar(ax_main, -93.5, 30.0, 100, proj)
    add_north_arrow(ax_main, -93.5, 34.5, proj)

    # State labels
    state_labels = {
        'LA': (-92.0, 30.8),
        'MS': (-89.7, 32.8),
        'AR': (-92.5, 34.8),
        'TX': (-93.8, 31.5),
    }
    for state, (lon, lat) in state_labels.items():
        ax_main.text(lon, lat, state, fontsize=14, color='gray', alpha=0.5,
                     ha='center', va='center', fontweight='bold', transform=proj)

    # Gridlines
    gl = ax_main.gridlines(draw_labels=True, linewidth=0.5, color='gray',
                           alpha=0.5, linestyle=':')
    gl.top_labels = False
    gl.right_labels = False

    # Legend
    legend_elements = [
        plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='#d62728',
                   markeredgecolor='black', markersize=15, label='Poverty Point (type site)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#ff7f0e',
                   markeredgecolor='black', markersize=8,
                   label='Other Late/Middle Archaic mound sites'),
        mpatches.Patch(facecolor='#cfe2cf', edgecolor='#5a8a5a', hatch='///',
                       label='Holocene Mississippi alluvial valley'),
        mpatches.Patch(facecolor='#e8d6b8', edgecolor='#8c6f3a', hatch='....',
                       label='Wisconsin Stage Pleistocene terraces'),
    ]
    ax_main.legend(handles=legend_elements, loc='lower left', fontsize=8.5,
                   framealpha=0.9, edgecolor='black')

    # ===== Inset: SE US context =====
    ax_inset = fig.add_axes([0.55, 0.72, 0.40, 0.26], projection=proj)
    ax_inset.set_extent([-100, -75, 25, 42], crs=proj)

    ax_inset.add_feature(cfeature.LAND, facecolor='#f5f0e1')
    ax_inset.add_feature(cfeature.OCEAN, facecolor='#d4e6f1')
    ax_inset.add_feature(cfeature.STATES, edgecolor='gray', linewidth=0.3)
    ax_inset.add_feature(cfeature.COASTLINE, linewidth=0.5)

    # Mark Poverty Point on inset
    ax_inset.plot(PP_LON, PP_LAT, marker='*', color='#d62728', markersize=14,
                  markeredgecolor='black', markeredgewidth=1, transform=proj, zorder=10)
    ax_inset.text(PP_LON + 1.5, PP_LAT + 0.5, 'PP', fontsize=10, fontweight='bold',
                  color='#d62728', transform=proj)

    # Draw box showing main panel extent
    from matplotlib.patches import Rectangle
    rect = Rectangle((main_extent[0], main_extent[2]),
                     main_extent[1] - main_extent[0],
                     main_extent[3] - main_extent[2],
                     linewidth=2, edgecolor='red', facecolor='none', transform=proj)
    ax_inset.add_patch(rect)

    # Material source locations on inset
    sources = {
        'Copper': (-87.5, 41.0),
        'Galena': (-90.5, 38.0),
        'Steatite': (-82.5, 35.0),
        'Novaculite': (-93.5, 34.5),
    }
    for name, (lon, lat) in sources.items():
        ax_inset.plot(lon, lat, marker='D', color='#555555', markersize=5,
                      markeredgecolor='black', transform=proj, zorder=8)

    ax_inset.set_title('Regional Context', fontsize=10, fontweight='bold')

    return fig


def main():
    """Generate Figure 1."""
    print("Creating Figure 1: Regional Map")
    print("=" * 60)

    fig = create_regional_map()

    output_png = OUTPUT_DIR / 'figure_01_poverty_point_map.png'
    output_pdf = OUTPUT_DIR / 'figure_01_poverty_point_map.pdf'

    fig.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(output_pdf, bbox_inches='tight', facecolor='white')

    print(f"\nFigure saved to:")
    print(f"  PNG: {output_png}")
    print(f"  PDF: {output_pdf}")

    plt.close(fig)
    return fig


if __name__ == '__main__':
    main()
