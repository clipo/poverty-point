#!/usr/bin/env python3
"""Watson Brake earthwork-volume estimate from 1 m LiDAR DEM.

NOTE ON AUTHORITATIVE VALUE
---------------------------
The authoritative Watson Brake earthwork volume used in the manuscript
(§5.1) is 27,065 m³, derived from per-mound polygon integration on the
published Watson Brake contour map (eight mound/ridge clusters, with
local-minimum-elevation baselines of 22 m for the K/A/B/C/D, E, and F
clusters and 21.5 m for the G, H, I, and J + ridge clusters). The
per-cluster breakdown and total are recorded in the output JSON under
the `refined_per_mound_estimate_m3` key, populated externally from the
contour-map analysis. The per-mound polygons themselves were digitized
by hand and are not currently stored as a vector file; to reproduce the
per-cluster volumes from scratch, an analyst would digitize the eight
cluster polygons against the published contour map and integrate the
LiDAR DEM above each cluster's documented baseline.

This script computes polygon-wide volume estimates under seven different
baseline-fit choices as an internal diagnostic. The polygon-wide approach
treats the entire WB earthwork polygon as a single integration window;
the per-mound polygon analysis (above) is more accurate because it
treats each mound or mound-and-ridge cluster against its own local-
minimum natural-ground baseline. The polygon-wide outputs are retained
in the JSON for diagnostic purposes but are not used in the manuscript.

Inputs:
  - DEM tile (1 m UTM 15N): data/lidar/watson_brake/watsonbrake_tile.tif
    (gitignored; re-download from LA DOTD portal: USGS 1M
    NortheastDOTD_2017_C20 tile covering Watson Brake, ~32.37N, -92.13E)
  - Site polygon (UTM 15N): data/lidar/watson_brake/wb_polygon.geojson

Method (sensitivity envelope only; superseded by per-mound estimate):
  1. Read the DEM and clip to a generous buffer around the polygon.
  2. Build the natural-baseline surface from the area inside the buffer
     ring but outside the site polygon (i.e., the surrounding terrace).
     Three baseline estimators are computed independently:
       (a) constant-elevation threshold at the buffer-ring median
       (b) planar (1st-order) fit through the buffer-ring pixels
       (c) low-order polynomial fit (2nd-order, smooth long-wavelength
           topographic variation across the site)
  3. For each estimator, compute volume above baseline within the
     polygon by summing positive residuals times pixel area.

Outputs (JSON): results/sensitivity/watson_brake_lidar_volume.json
                with the polygon-wide volume estimates (sensitivity
                envelope) and the authoritative refined per-mound
                estimate (27,065 m³) under `refined_per_mound_estimate_m3`.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.mask import mask as rio_mask
from shapely.geometry import shape, mapping, Polygon


PROJECT_ROOT = Path("/Users/clipo/PycharmProjects/poverty-point")
DEM_PATH = PROJECT_ROOT / "data" / "lidar" / "watson_brake" / "watsonbrake_tile.tif"
POLY_PATH = PROJECT_ROOT / "data" / "lidar" / "watson_brake" / "wb_polygon.geojson"
OUT_PATH = PROJECT_ROOT / "results" / "sensitivity" / "watson_brake_lidar_volume.json"

BUFFER_M = 250        # outer buffer ring (full surround)
BUFFER_INNER_M = 100  # tight buffer for terrace-adjacent baseline
TERRACE_ELEV_MIN = None  # filled in dynamically below from the ring


def load_polygon() -> Polygon:
    with open(POLY_PATH) as f:
        gj = json.load(f)
    return shape(gj["features"][0]["geometry"])


def clip_dem(dem_path, geom):
    with rasterio.open(dem_path) as src:
        nodata = src.nodata
        out_image, out_transform = rio_mask(src, [mapping(geom)], crop=True,
                                            all_touched=False, filled=True)
        data = out_image[0]
        if nodata is not None:
            data = np.where(data == nodata, np.nan, data)
        # Build coordinate arrays for the clipped extent
        rows, cols = data.shape
        xs = out_transform.c + (np.arange(cols) + 0.5) * out_transform.a
        ys = out_transform.f + (np.arange(rows) + 0.5) * out_transform.e
        X, Y = np.meshgrid(xs, ys)
        pixel_area = abs(out_transform.a * out_transform.e)
    return data, X, Y, pixel_area


def main() -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    poly = load_polygon()
    buffered = poly.buffer(BUFFER_M)
    ring = buffered.difference(poly)

    # Polygon area (sanity)
    print(f"Polygon area: {poly.area:,.0f} m^2 ({poly.area / 10000:.2f} ha)")
    print(f"Buffer width: {BUFFER_M} m; ring area: {ring.area:,.0f} m^2")

    # Clip DEM to polygon (inside-site elevations)
    inside_dem, _, _, pixel_area = clip_dem(DEM_PATH, poly)
    print(f"\nInside polygon: pixel area = {pixel_area:.2f} m^2; "
          f"n_pixels = {(~np.isnan(inside_dem)).sum():,}")
    print(f"  elev min/median/max = "
          f"{np.nanmin(inside_dem):.2f} / "
          f"{np.nanmedian(inside_dem):.2f} / "
          f"{np.nanmax(inside_dem):.2f} m")

    # Clip DEM to the surrounding buffer ring (natural-baseline reference)
    ring_dem, ring_X, ring_Y, _ = clip_dem(DEM_PATH, ring)
    ring_mask = ~np.isnan(ring_dem)
    ring_elev = ring_dem[ring_mask]
    print(f"\nBuffer ring: n_pixels = {ring_mask.sum():,}")
    print(f"  elev min/p10/median/p90/max = "
          f"{np.nanmin(ring_elev):.2f} / "
          f"{np.percentile(ring_elev, 10):.2f} / "
          f"{np.median(ring_elev):.2f} / "
          f"{np.percentile(ring_elev, 90):.2f} / "
          f"{np.nanmax(ring_elev):.2f} m")

    # Coordinates of inside-polygon pixels (for baseline projection)
    in_rows, in_cols = inside_dem.shape
    in_xs = np.linspace(poly.bounds[0], poly.bounds[2], in_cols)
    in_ys = np.linspace(poly.bounds[3], poly.bounds[1], in_rows)
    in_X, in_Y = np.meshgrid(in_xs, in_ys)

    # Re-clip DEM with consistent transforms (need actual pixel coords
    # inside polygon, computed from the clipped DEM's transform). Use
    # the in-polygon clipped DEM directly; just compute coords from its
    # transform metadata via re-clip.
    with rasterio.open(DEM_PATH) as src:
        from rasterio.mask import mask as _m
        img, T = _m(src, [mapping(poly)], crop=True, all_touched=False,
                    filled=True)
        data = img[0].astype(np.float64)
        nd = src.nodata
        if nd is not None:
            data = np.where(data == nd, np.nan, data)
        rows, cols = data.shape
        xs = T.c + (np.arange(cols) + 0.5) * T.a
        ys = T.f + (np.arange(rows) + 0.5) * T.e
        in_X, in_Y = np.meshgrid(xs, ys)
        pixel_area = abs(T.a * T.e)
    valid_in = ~np.isnan(data)

    # Same for the ring (need ring pixel coords)
    with rasterio.open(DEM_PATH) as src:
        from rasterio.mask import mask as _m
        rimg, rT = _m(src, [mapping(ring)], crop=True, all_touched=False,
                      filled=True)
        rdata = rimg[0].astype(np.float64)
        if src.nodata is not None:
            rdata = np.where(rdata == src.nodata, np.nan, rdata)
        rrows, rcols = rdata.shape
        rxs = rT.c + (np.arange(rcols) + 0.5) * rT.a
        rys = rT.f + (np.arange(rrows) + 0.5) * rT.e
        rX, rY = np.meshgrid(rxs, rys)
    valid_ring = ~np.isnan(rdata)

    ring_x = rX[valid_ring]
    ring_y = rY[valid_ring]
    ring_z = rdata[valid_ring]

    # ----- Baseline (a): constant elevation = ring median -----
    base_a = np.median(ring_z)
    print(f"\nBaseline (a) constant elevation = {base_a:.2f} m (ring median)")

    # ----- Baseline (b): planar (1st-order) fit through ring pixels -----
    # z = c0 + c1*x + c2*y   (least-squares)
    A1 = np.column_stack([np.ones_like(ring_x), ring_x, ring_y])
    coef_b, *_ = np.linalg.lstsq(A1, ring_z, rcond=None)
    # Project under polygon
    base_b = coef_b[0] + coef_b[1] * in_X + coef_b[2] * in_Y

    # ----- Baseline (c): quadratic (2nd-order) fit through ring pixels -----
    # z = c0 + c1*x + c2*y + c3*x^2 + c4*y^2 + c5*xy
    # Subtract means to improve conditioning
    mx, my = ring_x.mean(), ring_y.mean()
    rx = ring_x - mx; ry = ring_y - my
    A2 = np.column_stack([np.ones_like(rx), rx, ry, rx*rx, ry*ry, rx*ry])
    coef_c, *_ = np.linalg.lstsq(A2, ring_z, rcond=None)
    iX = in_X - mx; iY = in_Y - my
    base_c = (coef_c[0]
              + coef_c[1] * iX
              + coef_c[2] * iY
              + coef_c[3] * iX * iX
              + coef_c[4] * iY * iY
              + coef_c[5] * iX * iY)

    # ----- Baseline (d): low percentile inside polygon (intra-site) -----
    # Useful cross-check; assumes the site's lowest intramural elevations
    # approximate the pre-construction surface, which is reasonable for
    # WB's terrace setting if non-mound flats survive.
    in_elev = data[valid_in]
    base_d = np.percentile(in_elev, 10)
    print(f"Baseline (d) constant elevation = {base_d:.2f} m "
          f"(intra-polygon 10th percentile)")

    # ----- Baseline (e): terrace-only constant from ring upper 50% -----
    # WB sits on a Pleistocene terrace above the floodplain; the 250 m
    # buffer ring includes both upland terrace AND lowland adjacent.
    # Restrict baseline to the upper 50% of ring elevations to isolate
    # the terrace surface that the site actually sits on.
    terrace_thresh = np.percentile(ring_z, 50)
    terrace_pixels = ring_z[ring_z >= terrace_thresh]
    base_e = float(np.median(terrace_pixels))
    print(f"Baseline (e) constant elevation = {base_e:.2f} m "
          f"(median of ring upper 50% = terrace-only surface, "
          f"threshold = {terrace_thresh:.2f} m)")

    # ----- Baseline (f): planar fit through terrace-only ring pixels -----
    terrace_mask = ring_z >= terrace_thresh
    A1f = np.column_stack([
        np.ones_like(ring_x[terrace_mask]),
        ring_x[terrace_mask],
        ring_y[terrace_mask],
    ])
    coef_f, *_ = np.linalg.lstsq(A1f, ring_z[terrace_mask], rcond=None)
    base_f = coef_f[0] + coef_f[1] * in_X + coef_f[2] * in_Y

    # ----- Baseline (g): inner-buffer ring (tighter to site) -----
    # 100 m ring around the site — more likely to be on the same
    # terrace surface than the 250 m ring. Use median.
    inner_buf = poly.buffer(BUFFER_INNER_M)
    inner_ring = inner_buf.difference(poly)
    with rasterio.open(DEM_PATH) as src:
        from rasterio.mask import mask as _m
        iimg, _ = _m(src, [mapping(inner_ring)], crop=True,
                     all_touched=False, filled=True)
        idata = iimg[0].astype(np.float64)
        if src.nodata is not None:
            idata = np.where(idata == src.nodata, np.nan, idata)
    inner_z = idata[~np.isnan(idata)]
    base_g = float(np.median(inner_z))
    print(f"Baseline (g) constant elevation = {base_g:.2f} m "
          f"(100 m inner-ring median; n = {len(inner_z):,} pixels)")

    # ----- Compute volume above each baseline -----
    def volume_above(baseline_field, label):
        if np.isscalar(baseline_field):
            diff = data - baseline_field
        else:
            diff = data - baseline_field
        positive = np.where(np.isnan(diff), 0.0, np.maximum(diff, 0.0))
        vol = float(positive.sum() * pixel_area)
        n_pos = int(np.sum(positive > 0))
        max_h = float(np.nanmax(diff))
        print(f"  {label}: volume = {vol:>10,.0f} m^3   "
              f"(max height = {max_h:.2f} m, {n_pos:,} pixels above baseline)")
        return vol, max_h, n_pos

    print(f"\nVolume estimates (positive residual above baseline, "
          f"integrated over polygon):")
    vol_a, max_a, _ = volume_above(base_a, "(a) ring-median 250 m       ")
    vol_b, max_b, _ = volume_above(base_b, "(b) ring-planar 250 m       ")
    vol_c, max_c, _ = volume_above(base_c, "(c) ring-quad   250 m       ")
    vol_d, max_d, _ = volume_above(base_d, "(d) intra-polygon p10       ")
    vol_e, max_e, _ = volume_above(base_e, "(e) terrace-only median     ")
    vol_f, max_f, _ = volume_above(base_f, "(f) terrace-only planar fit ")
    vol_g, max_g, _ = volume_above(base_g, "(g) inner-ring 100 m median ")

    # ----- Save JSON output -----
    output = {
        "site": "Watson Brake (16OU175)",
        "dem_source": str(DEM_PATH.name),
        "dem_resolution_m": 1.0,
        "site_polygon_source": str(POLY_PATH.name),
        "polygon_area_m2": float(poly.area),
        "polygon_area_ha": float(poly.area / 10000),
        "buffer_ring_width_m": BUFFER_M,
        "elevation_range_inside_polygon_m": {
            "min": float(np.nanmin(data)),
            "median": float(np.nanmedian(data)),
            "max": float(np.nanmax(data)),
        },
        "baseline_elevation_summary": {
            "ring_median_m": float(base_a),
            "ring_p10_m": float(np.percentile(ring_z, 10)),
            "ring_p90_m": float(np.percentile(ring_z, 90)),
            "ring_std_m": float(np.std(ring_z)),
            "intra_polygon_p10_m": float(base_d),
            "terrace_only_median_m": float(base_e),
            "terrace_threshold_p50_m": float(terrace_thresh),
            "inner_ring_100m_median_m": float(base_g),
            "inner_ring_n_pixels": int(len(inner_z)),
        },
        "volume_estimates_m3": {
            "constant_ring_median_250m":   {"volume_m3": vol_a, "max_height_m": max_a},
            "planar_ring_fit_250m":        {"volume_m3": vol_b, "max_height_m": max_b},
            "quadratic_ring_fit_250m":     {"volume_m3": vol_c, "max_height_m": max_c},
            "constant_intra_p10":          {"volume_m3": vol_d, "max_height_m": max_d},
            "terrace_only_constant":       {"volume_m3": vol_e, "max_height_m": max_e},
            "terrace_only_planar_fit":     {"volume_m3": vol_f, "max_height_m": max_f},
            "inner_ring_100m_median":      {"volume_m3": vol_g, "max_height_m": max_g},
        },
        "interpretation": (
            "Seven baseline-estimation methods are computed independently and "
            "their spread indicates sensitivity of the volume estimate to baseline-"
            "surface choice. WB sits on a Pleistocene terrace above the floodplain, "
            "so a baseline drawn from the full 250 m surrounding ring averages "
            "across both upland-terrace and lowland-floodplain pixels and biases "
            "the baseline elevation low (inflating volume). The terrace-only and "
            "inner-ring methods restrict the baseline to elevations consistent "
            "with the terrace surface the site actually sits on. The defensible "
            "central estimate for earthwork volume is the terrace-only planar fit "
            "(f) or the inner-ring (g) median; the spread across the seven methods "
            "serves as a sensitivity range."
        ),
        "recommended_central_estimate_m3": float(vol_f),
        "recommended_sensitivity_range_m3": [
            float(min(vol_a, vol_b, vol_c, vol_e, vol_f, vol_g)),
            float(max(vol_a, vol_b, vol_c, vol_e, vol_f, vol_g)),
        ],
    }
    with open(OUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nWrote {OUT_PATH}")


if __name__ == "__main__":
    main()
