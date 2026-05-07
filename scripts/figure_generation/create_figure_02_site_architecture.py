#!/usr/bin/env python3
"""
Create Figure 2: Poverty Point Site Architecture

Loads the existing LiDAR image of Poverty Point mounds and formats it
for publication with title bar and consistent styling.

Source image: figures/PovertyPoint-Mounds.png
Output: figures/manuscript/figure_02_site_architecture.png
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path

PROJECT_ROOT = Path('/Users/clipo/PycharmProjects/poverty-point-signaling')
INPUT_IMAGE = PROJECT_ROOT / 'figures' / 'PovertyPoint-Mounds.png'
OUTPUT_DIR = PROJECT_ROOT / 'figures' / 'final'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Publication formatting
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 11


def create_site_architecture_figure():
    """Create the site architecture figure from LiDAR image."""
    if not INPUT_IMAGE.exists():
        raise FileNotFoundError(f"LiDAR image not found: {INPUT_IMAGE}")

    img = mpimg.imread(str(INPUT_IMAGE))

    # Get image aspect ratio
    h, w = img.shape[:2]
    aspect = w / h

    fig_width = 10
    fig_height = fig_width / aspect + 0.8  # extra space for title

    fig = plt.figure(figsize=(fig_width, fig_height))

    # Image axis
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.88])
    ax.imshow(img)
    ax.axis('off')

    # Title
    fig.suptitle('Figure 2. Poverty Point Site Architecture (LiDAR)',
                 fontsize=13, fontweight='bold', y=0.97)

    # Caption below title
    fig.text(0.5, 0.92,
             'LiDAR imagery showing concentric C-shaped ridges, Mound A (Bird Mound, 22 m), '
             'Mound B, plaza, and Bayou Macon.',
             ha='center', va='top', fontsize=10, fontstyle='italic',
             wrap=True)

    return fig


def main():
    """Generate Figure 2."""
    print("Creating Figure 2: Site Architecture")
    print("=" * 60)

    fig = create_site_architecture_figure()

    output_png = OUTPUT_DIR / 'figure_02_site_architecture.png'
    output_pdf = OUTPUT_DIR / 'figure_02_site_architecture.pdf'

    fig.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
    fig.savefig(output_pdf, bbox_inches='tight', facecolor='white')

    print(f"\nFigure saved to:")
    print(f"  PNG: {output_png}")
    print(f"  PDF: {output_pdf}")

    plt.close(fig)
    return fig


if __name__ == '__main__':
    main()
