#!/usr/bin/env python3
"""
Create Figure: Regional Chronological Synthesis

Shows the revised chronological framework from Kidder & Grooms 2024,
Grooms et al. 2023, Kidder Henry & Arco 2018, and Saunders et al. 2005.

Two panels:
A. Regional timeline showing Watson Brake, Jaketown, and Poverty Point
   occupation spans with construction events, exchange networks, and
   the flood/collapse event.
B. Expanded view of the construction window (3500-3000 BP) showing
   convergence of construction events and the flood termination.

Formatting follows CLAUDE.md requirements:
- Sans-serif font
- Colorblind-safe palette (Okabe-Ito derived)
- 300 DPI, 7 inch width
- No titles on figures

Author: Generated for Poverty Point JAS manuscript
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyArrowPatch, Rectangle, Patch
from matplotlib.gridspec import GridSpec
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'figures', 'final')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Publication formatting
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['legend.fontsize'] = 8
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9

# Colorblind-safe palette
CB = {
    'blue': '#0173B2',
    'orange': '#DE8F05',
    'green': '#029E73',
    'red': '#D55E00',
    'purple': '#CC78BC',
    'brown': '#CA9161',
    'gray': '#949494',
    'yellow': '#ECE133',
    'light_blue': '#56B4E9',
    'dark_gray': '#555555',
}

# ============================================================
# Data from processed papers (all dates in cal BP)
# ============================================================

# Watson Brake (Saunders et al. 2005)
wb_occupation = (5500, 4800)  # approximate occupation span
wb_construction = [(5500, 5300), (5100, 4900)]  # episodic, with 200+ yr hiatuses
wb_label = 'Watson Brake'

# Jaketown (Grooms et al. 2023; Ward et al. 2022)
jt_phase1 = (4570, 3820)   # initial occupation with PPOs and imports
jt_phase2 = (3585, 3395)   # intensive occupation, Appalachian soapstone
jt_phase3 = (3425, 3365)   # earthwork construction
jt_phase4 = (3245, 2455)   # post-flood reoccupation
jt_feasting = 3430          # fall feasting episode before mound construction
jt_flood = 3310             # crevasse splay (Kidder Henry Arco 2018)
jt_label = 'Jaketown'

# Poverty Point (Kidder & Grooms 2024)
pp_occupation = (3535, 3135)    # 95.4% hpd from Model 4
pp_construction = (3300, 3225)  # active construction window (micromorphology)
pp_moundA = 3261                # mean date for Mound A (Ortmann & Kidder 2013)
pp_rw3 = 3280                   # approximate Ridge West 3 (Kidder et al. 2021)
pp_label = 'Poverty Point'

# Key events
gap_wb_pp = (4800, 3535)  # 1300-year gap between Watson Brake and PP
flood_event = 3310
abandonment_end = 2780

# ============================================================
# Figure
# ============================================================

fig = plt.figure(figsize=(7, 6))
gs = GridSpec(2, 1, height_ratios=[1, 1.2], hspace=0.35)

# ------ Panel A: Full regional timeline ------
ax1 = fig.add_subplot(gs[0])

y_positions = {'Watson Brake': 2.5, 'Jaketown': 1.5, 'Poverty Point': 0.5}
bar_height = 0.6

# Watson Brake
ax1.barh(y_positions[wb_label], wb_occupation[0] - wb_occupation[1],
         left=wb_occupation[1], height=bar_height, color=CB['brown'],
         alpha=0.4, edgecolor=CB['brown'], linewidth=0.8)
for cs, ce in wb_construction:
    ax1.barh(y_positions[wb_label], cs - ce, left=ce, height=bar_height,
             color=CB['brown'], alpha=0.8, edgecolor='black', linewidth=0.5)

# Jaketown phases
# Phase 1: light fill
ax1.barh(y_positions[jt_label], jt_phase1[0] - jt_phase1[1],
         left=jt_phase1[1], height=bar_height, color=CB['blue'],
         alpha=0.25, edgecolor=CB['blue'], linewidth=0.8)
# Phase 2: medium fill
ax1.barh(y_positions[jt_label], jt_phase2[0] - jt_phase2[1],
         left=jt_phase2[1], height=bar_height, color=CB['blue'],
         alpha=0.5, edgecolor=CB['blue'], linewidth=0.8)
# Phase 3: construction (dark fill)
ax1.barh(y_positions[jt_label], jt_phase3[0] - jt_phase3[1],
         left=jt_phase3[1], height=bar_height, color=CB['blue'],
         alpha=0.85, edgecolor='black', linewidth=0.8)
# Phase 4: post-flood
ax1.barh(y_positions[jt_label], jt_phase4[0] - jt_phase4[1],
         left=jt_phase4[1], height=bar_height, color=CB['blue'],
         alpha=0.15, edgecolor=CB['blue'], linewidth=0.5, linestyle='--')

# Poverty Point
ax1.barh(y_positions[pp_label], pp_occupation[0] - pp_occupation[1],
         left=pp_occupation[1], height=bar_height, color=CB['orange'],
         alpha=0.4, edgecolor=CB['orange'], linewidth=0.8)
ax1.barh(y_positions[pp_label], pp_construction[0] - pp_construction[1],
         left=pp_construction[1], height=bar_height, color=CB['orange'],
         alpha=0.85, edgecolor='black', linewidth=0.8)

# Flood event line
ax1.axvline(x=flood_event, color=CB['red'], linewidth=2, linestyle='-',
            alpha=0.8, zorder=5)
ax1.text(flood_event - 30, 3.05, 'Flood\n3310 BP', fontsize=7,
         color=CB['red'], ha='right', va='bottom', fontweight='bold')

# 1300-year gap annotation
gap_mid = (gap_wb_pp[0] + gap_wb_pp[1]) / 2
ax1.annotate('', xy=(gap_wb_pp[1], 1.85), xytext=(gap_wb_pp[0], 1.85),
             arrowprops=dict(arrowstyle='<->', color=CB['gray'],
                             lw=1.0, ls='--'))
ax1.text(gap_mid, 1.95, '~1,300 yr gap', fontsize=7, ha='center',
         color=CB['gray'], style='italic')

# Labels
ax1.set_yticks([0.5, 1.5, 2.5])
ax1.set_yticklabels(['Poverty Point', 'Jaketown', 'Watson Brake'])
ax1.set_xlabel('Calendar years BP')
ax1.set_xlim(5800, 2200)
ax1.invert_xaxis()
ax1.set_ylim(-0.1, 3.4)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Legend for Panel A
legend_elements = [
    Patch(facecolor=CB['gray'], alpha=0.25, edgecolor='gray',
          label='Occupation'),
    Patch(facecolor=CB['gray'], alpha=0.85, edgecolor='black',
          label='Earthwork construction'),
    Patch(facecolor=CB['gray'], alpha=0.15, edgecolor='gray',
          linestyle='--', label='Post-flood reoccupation'),
    plt.Line2D([0], [0], color=CB['red'], linewidth=2,
               label='Crevasse splay (3310 BP)'),
]
ax1.legend(handles=legend_elements, loc='upper right', framealpha=0.9,
           fontsize=7, ncol=2)

ax1.text(0.02, 0.95, 'A', transform=ax1.transAxes, fontsize=14,
         fontweight='bold', va='top')

# ------ Panel B: Expanded construction window ------
ax2 = fig.add_subplot(gs[1])

# Shaded background zones
ax2.axvspan(3535, 3135, color=CB['orange'], alpha=0.08,
            label='PP occupation (95.4% hpd)')

# Jaketown phases in detail
ax2.barh(3, jt_phase2[0] - jt_phase2[1], left=jt_phase2[1], height=0.5,
         color=CB['blue'], alpha=0.4, edgecolor=CB['blue'])
ax2.barh(3, jt_phase3[0] - jt_phase3[1], left=jt_phase3[1], height=0.5,
         color=CB['blue'], alpha=0.85, edgecolor='black', linewidth=0.8)

# Jaketown feasting event
ax2.plot(jt_feasting, 3, marker='v', color=CB['green'], markersize=10,
         zorder=5)
ax2.text(jt_feasting - 15, 2.55, 'Fall feasting', fontsize=7,
         color=CB['green'], ha='right', va='top')

# Poverty Point occupation
ax2.barh(2, pp_occupation[0] - pp_occupation[1], left=pp_occupation[1],
         height=0.5, color=CB['orange'], alpha=0.3, edgecolor=CB['orange'])

# PP construction window
ax2.barh(2, pp_construction[0] - pp_construction[1],
         left=pp_construction[1], height=0.5, color=CB['orange'],
         alpha=0.85, edgecolor='black', linewidth=0.8)

# Individual construction events
ax2.plot(pp_moundA, 1, marker='s', color=CB['orange'], markersize=10,
         zorder=5, markeredgecolor='black', markeredgewidth=0.5)
ax2.text(pp_moundA + 15, 1.05, 'Mound A\n(3261 BP, <90 days)',
         fontsize=7, color=CB['dark_gray'], ha='left', va='center')

ax2.plot(pp_rw3, 0.5, marker='D', color=CB['orange'], markersize=8,
         zorder=5, markeredgecolor='black', markeredgewidth=0.5)
ax2.text(pp_rw3 + 15, 0.5, 'Ridge West 3\n(days to weeks)',
         fontsize=7, color=CB['dark_gray'], ha='left', va='center')

# Flood event
ax2.axvline(x=flood_event, color=CB['red'], linewidth=2.5, alpha=0.8,
            zorder=5)

# Abandonment zone
ax2.axvspan(flood_event, abandonment_end, color=CB['red'], alpha=0.08)
ax2.text((flood_event + abandonment_end) / 2, 3.7,
         '530-year abandonment', fontsize=8, ha='center',
         color=CB['red'], style='italic')

# Arrow showing convergence
ax2.annotate('', xy=(3300, 3.9), xytext=(3425, 3.9),
             arrowprops=dict(arrowstyle='->', color=CB['purple'],
                             lw=1.5))
ax2.annotate('', xy=(3300, 3.65), xytext=(3535, 3.65),
             arrowprops=dict(arrowstyle='->', color=CB['purple'],
                             lw=1.5))
ax2.text(3620, 3.77, 'Convergence', fontsize=8, color=CB['purple'],
         fontweight='bold', ha='left')

# Exchange network annotations
ax2.annotate('Soapstone exchange begins', xy=(3585, 2.7),
             fontsize=7, color=CB['blue'], ha='center',
             style='italic')

# Post-flood annotation
ax2.text(2900, 0.2,
         'Post-flood: no monuments,\nno exchange, no lapidary art',
         fontsize=7, color=CB['red'], ha='center', va='center',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                   edgecolor=CB['red'], alpha=0.8))

# Labels
ax2.set_yticks([0.5, 1, 2, 3])
ax2.set_yticklabels(['Ridge West 3', 'Mound A', 'Poverty Point\n(occupation)',
                     'Jaketown'])
ax2.set_xlabel('Calendar years BP')
ax2.set_xlim(3700, 2700)
ax2.invert_xaxis()
ax2.set_ylim(-0.2, 4.2)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

ax2.text(0.02, 0.95, 'B', transform=ax2.transAxes, fontsize=14,
         fontweight='bold', va='top')

# Save
plt.savefig(os.path.join(OUTPUT_DIR, 'figure_09_regional_chronology.png'),
            dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(os.path.join(OUTPUT_DIR, 'figure_09_regional_chronology.pdf'),
            bbox_inches='tight', facecolor='white')
plt.close()

print("Figure saved to figures/manuscript/figure_09_regional_chronology.png")
print("Figure saved to figures/manuscript/figure_09_regional_chronology.pdf")
