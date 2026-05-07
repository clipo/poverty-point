"""
Test the four-drainage independence claim with modern USGS gauge data.

The framework's core LMV claim (§4.5, §5.1) is that PP integrates four
canoe-accessible drainages (Mississippi, Yazoo, Tensas, Bayou Maçon)
with non-synchronized hydrographs, and that this multi-drainage access
is what differentiates PP from single-drainage sites in the high-ε
band. The claim is asserted but not measured in the manuscript.

This script pulls modern USGS gauge records from the four drainages
near or upstream of the Poverty Point catchment and computes:

  - Pearson and Spearman correlations across the four monthly mean
    discharge series.
  - Year-to-year correlation of low-flow events (defined as months
    with discharge below the 25th percentile of the long-term record).
  - Independent-shortfall index: fraction of years in which at most
    one drainage is in the bottom-quartile, vs. all four simultaneously.

The expected pattern under the four-drainage independence hypothesis:
the four drainages should have moderate cross-correlations (large
shared regional precipitation signal) but enough independent variance
that low-flow years rarely coincide across all four.

USGS gauges selected (representative downstream stations):
  - Mississippi River at Vicksburg, MS         (USGS 07289000)
  - Yazoo River at Greenwood, MS                (USGS 07287150)
  - Tensas River at Tendal, LA                  (USGS 07368000)
  - Bayou Maçon near Delhi, LA                  (USGS 07370240)

Output: results/hydrography/four_drainage_covariance.json
"""
from pathlib import Path
import json
import sys
from io import StringIO

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

try:
    import urllib.request as urlreq
except ImportError:
    import urllib2 as urlreq  # type: ignore


# USGS gauge ID → human label
# Corrected to use the Tensas at Tendal (07369500) and Bayou Maçon at Delhi (07370000);
# the earlier 07368000 was the Boeuf River (a parallel drainage in the same basin), and
# the earlier 07370240 was an inactive station with no discharge record.
GAUGES = {
    '07289000': 'Mississippi River at Vicksburg, MS',
    '07287150': 'Yazoo River at Greenwood, MS',
    '07369500': 'Tensas River at Tendal, LA',
    '07370000': 'Bayou Macon near Delhi, LA',
}

# Date range for analysis (use long enough record to capture ENSO-scale
# variability)
START_DATE = '1985-01-01'
END_DATE = '2024-12-31'


def fetch_usgs_monthly(gauge_id: str, start: str, end: str) -> pd.Series:
    """Fetch USGS daily discharge and return monthly mean (cubic ft/sec)."""
    url = (
        f'https://waterservices.usgs.gov/nwis/dv/?format=rdb'
        f'&sites={gauge_id}'
        f'&startDT={start}&endDT={end}'
        f'&statCd=00003'  # daily mean
        f'&parameterCd=00060'  # discharge cfs
    )
    print(f'  Fetching {gauge_id}...')
    try:
        req = urlreq.Request(url, headers={'User-Agent': 'pp-signaling-research/1.0'})
        with urlreq.urlopen(req, timeout=60) as resp:
            text = resp.read().decode('utf-8')
    except Exception as exc:
        print(f'  ERROR fetching {gauge_id}: {exc}')
        return pd.Series(dtype=float)

    # Parse RDB (tab-separated with comment lines starting with '#')
    rows = []
    header_seen = False
    cols = []
    for line in text.splitlines():
        if line.startswith('#') or not line.strip():
            continue
        parts = line.split('\t')
        if not header_seen:
            cols = parts
            header_seen = True
            continue
        if parts[0] == '5s':  # column type row
            continue
        if len(parts) < 4:
            continue
        rows.append(parts)
    if not rows:
        return pd.Series(dtype=float)

    df = pd.DataFrame(rows, columns=cols)
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    # Discharge column header varies; find it
    discharge_col = None
    for c in df.columns:
        if c.endswith('_00060_00003'):
            discharge_col = c
            break
    if discharge_col is None:
        print(f'  WARN: no discharge column for {gauge_id}')
        return pd.Series(dtype=float)
    df['discharge'] = pd.to_numeric(df[discharge_col], errors='coerce')
    df = df.dropna(subset=['datetime', 'discharge'])
    df = df.set_index('datetime')

    # Monthly mean
    monthly = df['discharge'].resample('MS').mean()
    return monthly


def main():
    out_dir = Path('results/hydrography')
    out_dir.mkdir(parents=True, exist_ok=True)

    cache_path = out_dir / 'usgs_monthly_discharge.csv'
    if cache_path.exists():
        print(f'Loading cached monthly discharge from {cache_path}')
        full = pd.read_csv(cache_path, index_col=0, parse_dates=True)
    else:
        series = {}
        print('Fetching USGS monthly discharge for four drainages...')
        for gid, label in GAUGES.items():
            s = fetch_usgs_monthly(gid, START_DATE, END_DATE)
            if not s.empty:
                series[label] = s
            else:
                print(f'  Skipping {label}: no data')
        if not series:
            print('No gauge data retrieved; aborting.')
            return
        full = pd.DataFrame(series)
        full.to_csv(cache_path)
        print(f'Cached {cache_path}')

    print()
    print('Long-term monthly discharge availability:')
    for col in full.columns:
        n = full[col].notna().sum()
        print(f'  {col:50s} n={n} months')

    # Drop rows where any drainage is missing for cross-correlation
    aligned = full.dropna()
    pairwise_overlaps = []  # collected for JSON output
    if len(aligned) == 0:
        print('\nNo all-four-gauge overlap; falling back to all available pairs.')
        # Fall back: compute pairwise correlations using each pair's overlap
        print('\nPairwise overlaps:')
        for ci in full.columns:
            for cj in full.columns:
                if ci >= cj:
                    continue
                pair = full[[ci, cj]].dropna()
                if len(pair) >= 24:
                    log_pair = np.log(pair + 1)
                    log_anom_pair = log_pair.copy()
                    for c in pair.columns:
                        clim = log_pair[c].groupby(log_pair.index.month).transform('mean')
                        log_anom_pair[c] = log_pair[c] - clim
                    r_p, p_p = pearsonr(log_anom_pair[ci], log_anom_pair[cj])
                    r_s, p_s = spearmanr(log_anom_pair[ci], log_anom_pair[cj])
                    print(f'  {ci[:35]:35s} vs {cj[:35]:35s}: '
                          f'n={len(pair)}, r={r_p:+.3f} (p={p_p:.3f}), rho={r_s:+.3f}')
                    pairwise_overlaps.append({
                        'a': ci, 'b': cj, 'n': int(len(pair)),
                        'pearson_r': float(r_p), 'pearson_p': float(p_p),
                        'spearman_rho': float(r_s), 'spearman_p': float(p_s),
                    })
        # Use the largest 3-gauge overlap for the main analysis
        # (excluding Bayou Macon, which has the shortest record)
        bm_col = next((c for c in full.columns if 'Maçon' in c or 'Macon' in c), None)
        if bm_col:
            three_cols = [c for c in full.columns if c != bm_col]
            aligned = full[three_cols].dropna()
            print(f'\nProceeding with three-drainage analysis '
                  f'({len(aligned)} aligned months, '
                  f'{aligned.index[0].strftime("%Y-%m")} to '
                  f'{aligned.index[-1].strftime("%Y-%m")}).')
        else:
            print('No fallback available; aborting main analysis.')
            return
    else:
        print(f'\nAligned record: {len(aligned)} months '
              f'({aligned.index[0].strftime("%Y-%m")} to '
              f'{aligned.index[-1].strftime("%Y-%m")})')

    if len(aligned) < 60:
        print('WARN: aligned record too short for robust correlations.')

    # Compute monthly anomalies: subtract long-term monthly climatology
    anom = aligned.copy()
    for col in aligned.columns:
        clim = aligned[col].groupby(aligned.index.month).transform('mean')
        anom[col] = aligned[col] - clim

    # Compute log-transformed anomalies to handle wide range of discharges
    log_disc = np.log(aligned + 1.0)
    log_anom = log_disc.copy()
    for col in log_disc.columns:
        clim = log_disc[col].groupby(log_disc.index.month).transform('mean')
        log_anom[col] = log_disc[col] - clim

    print()
    print('Cross-correlations (Pearson on log-transformed monthly anomalies):')
    cols = list(anom.columns)
    pearson_matrix = np.zeros((len(cols), len(cols)))
    spearman_matrix = np.zeros((len(cols), len(cols)))
    for i, ci in enumerate(cols):
        for j, cj in enumerate(cols):
            if i == j:
                pearson_matrix[i, j] = 1.0
                spearman_matrix[i, j] = 1.0
                continue
            r_p, _ = pearsonr(log_anom[ci], log_anom[cj])
            r_s, _ = spearmanr(log_anom[ci], log_anom[cj])
            pearson_matrix[i, j] = r_p
            spearman_matrix[i, j] = r_s

    print(f'{"":50s} ' + ' '.join(f'{c[:18]:>18s}' for c in cols))
    for i, ci in enumerate(cols):
        row_vals = ' '.join(f'{pearson_matrix[i, j]:18.3f}' for j in range(len(cols)))
        print(f'{ci:50s} {row_vals}')

    # Off-diagonal mean
    off_diag_pearson = []
    off_diag_spearman = []
    for i in range(len(cols)):
        for j in range(i+1, len(cols)):
            off_diag_pearson.append(pearson_matrix[i, j])
            off_diag_spearman.append(spearman_matrix[i, j])
    print()
    print(f'Mean off-diagonal Pearson:  {np.mean(off_diag_pearson):.3f}')
    print(f'Mean off-diagonal Spearman: {np.mean(off_diag_spearman):.3f}')

    # Low-flow co-incidence: in any given month, how often are 0/1/2/3/4
    # drainages in the bottom-quartile?
    lows = pd.DataFrame(index=aligned.index)
    for col in cols:
        q25 = aligned[col].quantile(0.25)
        lows[col] = aligned[col] < q25
    n_low_per_month = lows.sum(axis=1)
    coincidence_dist = n_low_per_month.value_counts().sort_index()
    print()
    print('Distribution of "drainages-in-bottom-quartile" per month:')
    for n_low, count in coincidence_dist.items():
        pct = count / len(lows) * 100
        print(f'  {int(n_low)} drainages low: {int(count)} months ({pct:.1f}%)')

    # Independence prediction: under independent drainages with q=0.25 each,
    # P(0 low) = 0.75^4 = 0.316; P(all 4 low) = 0.25^4 = 0.0039.
    # Compare with observed.
    n_total = len(lows)
    p_observed = coincidence_dist / n_total
    p_indep = pd.Series({
        0: 0.75**4,
        1: 4 * 0.25 * 0.75**3,
        2: 6 * 0.25**2 * 0.75**2,
        3: 4 * 0.25**3 * 0.75,
        4: 0.25**4,
    })
    print()
    print('Observed vs independent-drainage prediction:')
    print(f'  {"n_low":>6s} {"observed":>10s} {"independent":>14s} {"ratio":>8s}')
    for k in range(5):
        obs = float(p_observed.get(k, 0))
        ind = float(p_indep[k])
        ratio = obs / ind if ind > 0 else float('inf')
        print(f'  {k:6d} {obs:10.3f} {ind:14.3f} {ratio:8.2f}')

    out_path = out_dir / 'four_drainage_covariance.json'
    with open(out_path, 'w') as f:
        json.dump({
            'gauge_ids': list(GAUGES.keys()),
            'gauge_labels': list(GAUGES.values()),
            'date_range': [START_DATE, END_DATE],
            'aligned_n_months': int(len(aligned)),
            'pearson_matrix': pearson_matrix.tolist(),
            'spearman_matrix': spearman_matrix.tolist(),
            'mean_offdiag_pearson': float(np.mean(off_diag_pearson)),
            'mean_offdiag_spearman': float(np.mean(off_diag_spearman)),
            'low_coincidence_observed': {int(k): float(v) for k, v in p_observed.items()},
            'low_coincidence_independent': {int(k): float(p_indep[k]) for k in range(5)},
            'pairwise_overlaps': pairwise_overlaps,
        }, f, indent=2)
    print(f'\nWrote {out_path}')


if __name__ == '__main__':
    main()
