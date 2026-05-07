"""
Seasonal phenology of resource peaks in the Lower Mississippi Valley
====================================================================

Figure for §S7.5: visualizes the temporal staggering of resource peaks
across the four canoe-accessible drainages near Poverty Point, and the
extent to which each of the 11 LMV mound-building sites can integrate
those peaks within a 25 km terrestrial + ~1-day canoe catchment.

The argument: the framework's epsilon parameter encodes shortfall buffering
through *negative covariance* between local zone productivity and the
regional shortfall driver. Static Shannon-diversity proxies (qualitative,
geomorphic, EPA L4) measure raw zone count, not temporal staggering. A
site with four ecological zones whose productivity peaks all coincide in
fall has lower negative covariance than a site with three zones whose
peaks span fall, spring, and summer. This figure makes that distinction
visible.

Sources for resource phenology:

- Hardwood mast (hickory, pecan, acorn): peaks Sep-Nov; fall-winter
  population peaks at PP attributed to nut harvest by Thomas and Campbell
  (1978) per Jackson (1986). Webb (1982:18) reports "fall and winter
  provide acorns and other nuts."

- Spring fish spawning runs (drum, gar, buffalo, catfish): peaks Feb-May.
  Webb (1982:18) reports "spring and summer offer ... most varieties of
  fish and crustaceans." PP fauna is fish-dominated (Jackson 1986).

- Summer freshwater mussels and aquatic plants (lotus, cattail): peaks
  May-Aug. Webb (1982) inventories mussel and aquatic plant resources for
  the LMV.

- Falling-water aquatic concentration (oxbow shrinkage, fish trapping in
  cutoff lakes): peaks Aug-Oct. Standard LMV hydrographic phenology
  documented in fish-weir ethnography.

- Migratory waterfowl on the Mississippi Flyway: peaks Sep-Dec (fall
  migration) and Feb-Apr (spring migration). Webb (1982:18) reports
  "millions of migratory waterfowl, ducks, geese, swans, pigeons, filled
  the Mississippi central flyway, cutoff lakes, and the coastal areas."

Site catchment access is coded conservatively from published site
descriptions (Saunders et al. 2005 for Watson Brake and Frenchman's
Bend; Jackson 1981 for J.W. Copes; Sassaman 2005 for Caney and Insley;
Ward et al. 2022 for Jaketown; Webb 1982 for site hierarchy generally).
The five access categories are: hardwood mast (HM), spring fish spawn
(SFS), summer aquatic (SA), falling-water aquatic (FWA), waterfowl
flyway (WF). A site is coded as having access to a peak if its 25 km
terrestrial buffer plus ~1-day canoe radius spans the relevant zone.
The independence count (Panel B) is the number of *independent* peak
windows: peaks driven by different climate mechanisms, so multi-drainage
access is needed for high counts.

Output: figures/manuscript/figure_14_seasonal_phenology.{png,pdf}
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib import gridspec

OUTPUT_DIR = Path('figures/manuscript')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Resource peaks: name, short label, color, peak-month range (Jan=1)
RESOURCE_PEAKS = [
    ('Hardwood mast (hickory, acorn, pecan)',           'HM',  '#b15928', (9, 11)),
    ('Spring fish spawn (drum, gar, buffalo, catfish)', 'SFS', '#1f78b4', (2, 5)),
    ('Summer aquatic (mussels, lotus, cattail)',        'SA',  '#33a02c', (5, 8)),
    ('Falling-water aquatic concentration',             'FWA', '#6a3d9a', (8, 10)),
    ('Migratory waterfowl (fall + spring)',             'WF',  '#e31a1c', (9, 12)),
    ('Migratory waterfowl (spring)',                    'WF',  '#e31a1c', (2, 4)),
]

# Site name, parish, # independent drainages, peak-access flags
# Flags tuple order: (HM, SFS, SA, FWA, WF)
# 1.0 = full access; 0.5 = partial / single-drainage limited; 0.0 = absent
SITES = [
    ('Poverty Point',     'WC',     4, (1.0, 1.0, 1.0, 1.0, 1.0)),  # 4-drainage confluence
    ('Lower Jackson',     'WC',     1, (1.0, 0.5, 0.5, 0.5, 1.0)),  # Macon Ridge, shares PP setting
    ('Watson Brake',      'OU',     1, (1.0, 0.5, 0.5, 0.5, 0.5)),  # Bayou Bartholomew + terrace
    ('Frenchman\'s Bend', 'OU',     1, (1.0, 0.5, 0.5, 0.0, 0.5)),  # Ouachita tributary near Monroe
    ('Caney',             'CT',     1, (1.0, 0.0, 0.5, 0.0, 0.5)),  # Sicily Island Hills, small tributary
    ('Insley',            'FR',     1, (1.0, 0.5, 0.5, 0.0, 0.5)),  # Macon Ridge / Boeuf margin
    ('Cowpen Slough',     'CT',     1, (0.5, 1.0, 1.0, 0.5, 0.5)),  # Boeuf River margin (aquatic-focused)
    ('J.W. Copes',        'MA',     1, (0.5, 1.0, 1.0, 0.5, 0.5)),  # Tensas Basin
    ('Jaketown',          'HU',     1, (1.0, 1.0, 0.5, 0.5, 1.0)),  # Yazoo Basin meander belt + Loess Hills
    ('Claiborne',         'HA',     1, (0.0, 0.5, 0.5, 0.0, 1.0)),  # Pearl River mouth (marine-estuarine)
    ('Cedarland',         'HA',     1, (0.0, 0.5, 0.5, 0.0, 1.0)),  # adjacent to Claiborne
]


def _draw_phenology_strip(ax, peaks, ylabel_size=8):
    """Top panel: month-by-month resource phenology calendar."""
    ax.set_xlim(0.5, 12.5)
    ax.set_ylim(-0.5, len(peaks) - 0.5)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'],
                       fontsize=9)
    ax.set_yticks(range(len(peaks)))
    ax.set_yticklabels([p[1] for p in peaks], fontsize=ylabel_size)
    ax.invert_yaxis()
    for i, (name, label, color, (m_start, m_end)) in enumerate(peaks):
        ax.add_patch(Rectangle((m_start - 0.4, i - 0.35),
                               (m_end - m_start) + 0.8, 0.7,
                               facecolor=color, edgecolor='black',
                               linewidth=0.6, alpha=0.85))
    ax.grid(axis='x', linestyle=':', alpha=0.35)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def _draw_site_matrix(ax, sites, peaks):
    """Middle panel: site x month matrix; cell value is # of accessible peaks."""
    n_sites = len(sites)
    matrix = np.zeros((n_sites, 12))
    # Collapse spring + fall waterfowl into a single category
    peak_indices_by_label = {}
    for k, (_, label, _, _) in enumerate(peaks):
        peak_indices_by_label.setdefault(label, []).append(k)
    n_categories = len(peak_indices_by_label)

    label_order = list(peak_indices_by_label.keys())
    for i, (name, _, _, flags) in enumerate(sites):
        for cat_idx, label in enumerate(label_order):
            access = flags[cat_idx]
            for k in peak_indices_by_label[label]:
                _, _, _, (m_start, m_end) = peaks[k]
                for m in range(m_start, m_end + 1):
                    matrix[i, m - 1] += access
    im = ax.imshow(matrix, aspect='auto', cmap='YlOrBr',
                   vmin=0, vmax=n_categories,
                   extent=(0.5, 12.5, n_sites - 0.5, -0.5))
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'],
                       fontsize=9)
    ax.set_yticks([])
    for i, (name, _, _, _) in enumerate(sites):
        ax.text(0.40, i, name, ha='right', va='center', fontsize=9,
                transform=ax.get_yaxis_transform(which='grid'),
                clip_on=False)
    ax.set_xlim(0.5, 12.5)
    ax.set_ylim(n_sites - 0.5, -0.5)
    return im, matrix


def _draw_independence_bars(ax, sites):
    """Right panel: independent peak count per site (full access only).

    The y-axis is shared with the site x month matrix; the matrix uses
    imshow extent to put row 0 at the top, so we must NOT call
    invert_yaxis here (that would double-invert the shared axis).
    """
    counts = []
    for _, _, _, flags in sites:
        counts.append(sum(1 for f in flags if f >= 0.75))
    bars = ax.barh(range(len(sites)), counts, color='#888888', edgecolor='black')
    for i, count in enumerate(counts):
        ax.text(count + 0.1, i, str(count), va='center', fontsize=9)
    pp_idx = next(i for i, s in enumerate(sites) if s[0] == 'Poverty Point')
    bars[pp_idx].set_color('#d62728')
    ax.set_yticks([])
    ax.set_xlim(0, 5.8)
    ax.set_xticks(range(0, 6))
    ax.set_xlabel('Independent peak\nwindows (full access)', fontsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='x', linestyle=':', alpha=0.35)
    ax.set_axisbelow(True)


def main():
    fig = plt.figure(figsize=(11.0, 7.5))
    gs = gridspec.GridSpec(
        nrows=2, ncols=2,
        height_ratios=[1.1, 3.4],
        width_ratios=[3.2, 1.0],
        hspace=0.35, wspace=0.10,
    )

    ax_phen = fig.add_subplot(gs[0, 0])
    ax_mat = fig.add_subplot(gs[1, 0])
    ax_bar = fig.add_subplot(gs[1, 1], sharey=ax_mat)
    ax_phen.set_title('(A) LMV resource peak windows', fontsize=11, loc='left',
                      pad=6)
    _draw_phenology_strip(ax_phen, RESOURCE_PEAKS)

    ax_mat.set_title('(B) Site x month resource access (warmer = more peaks accessible)',
                     fontsize=11, loc='left', pad=6)
    im, _ = _draw_site_matrix(ax_mat, SITES, RESOURCE_PEAKS)
    cbar = plt.colorbar(im, ax=ax_mat, orientation='vertical',
                        fraction=0.025, pad=0.04, aspect=20)
    cbar.set_label('# resource peaks active', fontsize=9)

    ax_bar.set_title('(C)', fontsize=11, loc='left', pad=6)
    _draw_independence_bars(ax_bar, SITES)

    fig.suptitle('', y=0.99)

    out_png = OUTPUT_DIR / 'figure_14_seasonal_phenology.png'
    out_pdf = OUTPUT_DIR / 'figure_14_seasonal_phenology.pdf'
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    fig.savefig(out_pdf, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved: {out_png}')
    print(f'Saved: {out_pdf}')


if __name__ == '__main__':
    main()
