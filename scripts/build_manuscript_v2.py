#!/usr/bin/env python3
"""Build v2.0 docx files (main paper and supplemental)."""
import subprocess
from pathlib import Path

V2_DIR = Path('/Users/clipo/PycharmProjects/poverty-point-signaling/docs/manuscript_v2.0')
TEMPLATE = Path('/Users/clipo/PycharmProjects/poverty-point-signaling/docs/jamt/reference_template.docx')


def build(md_path: Path, docx_path: Path, resource_dir: Path):
    cmd = [
        'pandoc',
        str(md_path),
        '-o', str(docx_path),
        '--reference-doc', str(TEMPLATE),
        '--resource-path', str(resource_dir),
        '--from', 'markdown',
        '--to', 'docx',
    ]
    print(' '.join(cmd))
    subprocess.run(cmd, check=True)
    print(f'  -> {docx_path} ({docx_path.stat().st_size:,} bytes)')


def main():
    main_md = V2_DIR / 'Poverty_Point_JAS_v2.md'
    main_docx = V2_DIR / 'Poverty_Point_JAS_v2.docx'
    build(main_md, main_docx, V2_DIR)

    supp_md = V2_DIR / 'supplemental' / 'Supplemental_Material.md'
    supp_docx = V2_DIR / 'supplemental' / 'Supplemental_Material.docx'
    # Supplemental references figures via ../figures/
    build(supp_md, supp_docx, V2_DIR / 'supplemental')


if __name__ == '__main__':
    main()
