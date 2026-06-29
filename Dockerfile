# syntax=docker/dockerfile:1
#
# Reproducibility container for the Poverty Point costly-signaling project.
# Bundles Python 3.12.2, the pinned dependencies (requirements.txt), pandoc, and
# Arial/Times New Roman fonts so that every figure, analysis, and the manuscript
# docx can be regenerated on any platform with only a container runtime.
#
#   docker build -t poverty-point .
#   docker run --rm -v "$PWD/figures:/opt/poverty-point/figures" poverty-point make figures
#
# See REPRODUCE.md, section "Reproducing in a container", for full usage.
FROM python:3.12.2-slim-bookworm

# --- System tools -----------------------------------------------------------
#   pandoc            : manuscript docx build (`make manuscript`)
#   make, git         : build driver and provenance
#   fonts-liberation  : metric-compatible Arial/Times substitutes (always available)
#   ttf-mscorefonts   : exact Arial/Times New Roman (best-effort; needs network + EULA)
RUN set -eux; \
    if [ -f /etc/apt/sources.list.d/debian.sources ]; then \
        sed -i 's/^Components: main$/Components: main contrib non-free non-free-firmware/' \
            /etc/apt/sources.list.d/debian.sources; \
    else \
        echo "deb http://deb.debian.org/debian bookworm contrib non-free non-free-firmware" \
            >> /etc/apt/sources.list; \
    fi; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        pandoc git make ca-certificates curl fontconfig fonts-liberation; \
    echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" \
        | debconf-set-selections; \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends ttf-mscorefonts-installer \
        || echo "WARNING: Times New Roman (mscorefonts) unavailable at build time; figures will use the metric-compatible Liberation fonts."; \
    fc-cache -f; \
    rm -rf /var/lib/apt/lists/*

# --- Python dependencies ----------------------------------------------------
# Pinned in requirements.txt. The geospatial wheels (shapely, pyproj, rasterio,
# fiona, cartopy) bundle GEOS/PROJ/GDAL, so no system GIS libraries are needed.
WORKDIR /opt/poverty-point
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Project files ----------------------------------------------------------
COPY . /opt/poverty-point

# Compatibility shim: several scripts still reference the author's absolute path.
# Symlink it onto the canonical /opt project root so they resolve unchanged.
# (create_figure_13 is already path-relative; making the rest relative is a
# tracked follow-up. Removing this line once that is done is harmless.)
RUN mkdir -p /Users/clipo/PycharmProjects && \
    ln -sfn /opt/poverty-point /Users/clipo/PycharmProjects/poverty-point

ENV MPLBACKEND=Agg \
    PYTHONUNBUFFERED=1

# Default to a shell. Reproduce with, e.g., `make figures`, `make analyses`, `make all`.
CMD ["bash"]
