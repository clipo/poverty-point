"""
One-at-a-time (OAT) sensitivity analysis for Poverty Point signaling model.

Sweeps each key parameter while holding others at defaults, records sigma*
for each combination, and produces a tornado plot and markdown results table.
"""

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from poverty_point.signaling_core import (
    critical_threshold,
    SignalingParams,
    NetworkParams,
    ConflictParams,
    AggregationParams,
)

# ---------------------------------------------------------------
# Fixed context for all sweeps
# ---------------------------------------------------------------
EPSILON = 0.35
N_AGG = 25
TRAVEL_DISTANCE = 100.0

# Default parameter objects
DEFAULT_SIG = SignalingParams()
DEFAULT_NET = NetworkParams()
DEFAULT_CONF = ConflictParams()
DEFAULT_AGG = AggregationParams()


def compute_sigma_star(sig_params=None, net_params=None,
                       conf_params=None, agg_params=None):
    """Run critical_threshold with given params, return sigma* or None."""
    sig_params = sig_params or DEFAULT_SIG
    net_params = net_params or DEFAULT_NET
    conf_params = conf_params or DEFAULT_CONF
    agg_params = agg_params or DEFAULT_AGG

    try:
        result = critical_threshold(
            epsilon=EPSILON,
            n_agg=N_AGG,
            travel_distance=TRAVEL_DISTANCE,
            sig_params=sig_params,
            net_params=net_params,
            conf_params=conf_params,
            agg_params=agg_params,
        )
        ss = result['sigma_star']
        # sigma_star of 0.0 or 1.0 are boundary cases
        return ss
    except Exception as e:
        print(f"  Error: {e}")
        return None


# ---------------------------------------------------------------
# Parameter sweep definitions
# ---------------------------------------------------------------
# Each entry: (display_name, param_class, field_name, values_array, default_value)
sweeps = [
    ("gamma", "net", "gamma",
     np.arange(0.01, 0.16, 0.02), DEFAULT_NET.gamma),
    ("delta", "sig", "delta",
     np.arange(0.02, 0.16, 0.01), DEFAULT_SIG.delta),
    ("C_signal", "agg", "C_signal",
     np.arange(0.08, 0.29, 0.02), DEFAULT_AGG.C_signal),
    ("C_opportunity", "agg", "C_opportunity",
     np.arange(0.05, 0.21, 0.02), DEFAULT_AGG.C_opportunity),
    ("C_travel_per_km\n(at 100 km)", "agg", "C_travel_per_km",
     np.arange(0.0001, 0.00085, 0.0001), DEFAULT_AGG.C_travel_per_km),
    ("P_base", "conf", "P_base",
     np.arange(0.002, 0.016, 0.002), DEFAULT_CONF.P_base),
    ("lambda_W", "sig", "lambda_W",
     np.arange(0.05, 0.31, 0.03), DEFAULT_SIG.lambda_W),
    ("lambda_C", "sig", "lambda_C",
     np.arange(0.02, 0.21, 0.02), DEFAULT_SIG.lambda_C),
    ("lambda_X", "sig", "lambda_X",
     np.arange(0.05, 0.31, 0.05), DEFAULT_SIG.lambda_X),
    ("k_max", "net", "k_max",
     np.arange(2.0, 11.0, 1.0), DEFAULT_NET.k_max),
    ("M_half", "net", "M_half",
     np.arange(1.0, 5.5, 0.5), DEFAULT_NET.M_half),
    ("q_min", "sig", "q_min",
     np.arange(0.1, 0.51, 0.05), DEFAULT_SIG.q_min),
    ("q_max", "sig", "q_max",
     np.arange(1.0, 3.25, 0.25), DEFAULT_SIG.q_max),
]


def make_params(param_class, field_name, value):
    """Create a modified parameter dataclass with one field changed."""
    if param_class == "sig":
        d = {f.name: getattr(DEFAULT_SIG, f.name)
             for f in DEFAULT_SIG.__dataclass_fields__.values()}
        d[field_name] = float(value)
        return {"sig_params": SignalingParams(**d)}
    elif param_class == "net":
        d = {f.name: getattr(DEFAULT_NET, f.name)
             for f in DEFAULT_NET.__dataclass_fields__.values()}
        d[field_name] = float(value)
        return {"net_params": NetworkParams(**d)}
    elif param_class == "conf":
        d = {f.name: getattr(DEFAULT_CONF, f.name)
             for f in DEFAULT_CONF.__dataclass_fields__.values()}
        d[field_name] = float(value)
        return {"conf_params": ConflictParams(**d)}
    elif param_class == "agg":
        d = {f.name: getattr(DEFAULT_AGG, f.name)
             for f in DEFAULT_AGG.__dataclass_fields__.values()}
        d[field_name] = float(value)
        return {"agg_params": AggregationParams(**d)}
    else:
        raise ValueError(f"Unknown param class: {param_class}")


# ---------------------------------------------------------------
# Run all sweeps
# ---------------------------------------------------------------
print("Computing default sigma*...")
default_result = compute_sigma_star()
default_sigma_star = default_result
print(f"  Default sigma* = {default_sigma_star}")

all_results = []  # list of dicts
tornado_data = []  # (name, default_val, min_sigma, max_sigma, default_sigma_star)

for name, pclass, field, values, default_val in sweeps:
    clean_name = name.replace('\n', ' ')
    print(f"\nSweeping {clean_name} ({len(values)} values)...")
    sigmas = []
    for v in values:
        kwargs = make_params(pclass, field, v)
        ss = compute_sigma_star(**kwargs)
        sigmas.append(ss)
        status = f"{ss:.4f}" if ss is not None else "no threshold"
        all_results.append({
            'parameter': clean_name,
            'default': default_val,
            'tested': float(v),
            'sigma_star': ss,
        })
        print(f"  {clean_name}={v:.5f} -> sigma*={status}")

    valid = [s for s in sigmas if s is not None]
    if valid:
        tornado_data.append({
            'name': clean_name,
            'default': default_val,
            'min_sigma': min(valid),
            'max_sigma': max(valid),
            'range': max(valid) - min(valid),
        })
    else:
        tornado_data.append({
            'name': clean_name,
            'default': default_val,
            'min_sigma': None,
            'max_sigma': None,
            'range': 0.0,
        })

# Sort tornado data by range (descending)
tornado_data.sort(key=lambda x: x['range'], reverse=True)

print("\n\n=== TORNADO SUMMARY (sorted by sensitivity) ===")
for td in tornado_data:
    if td['min_sigma'] is not None:
        print(f"  {td['name']:30s}  range={td['range']:.4f}  "
              f"[{td['min_sigma']:.4f}, {td['max_sigma']:.4f}]")
    else:
        print(f"  {td['name']:30s}  no valid thresholds")


# ---------------------------------------------------------------
# Tornado plot
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 6))

n_params = len(tornado_data)
y_pos = np.arange(n_params)

# Plot bars
for i, td in enumerate(tornado_data):
    if td['min_sigma'] is not None and td['max_sigma'] is not None:
        left = td['min_sigma']
        width = td['max_sigma'] - td['min_sigma']
        bar = ax.barh(n_params - 1 - i, width, left=left, height=0.6,
                      color='#4C72B0', alpha=0.85, edgecolor='white', linewidth=0.5)
    else:
        # No valid data; skip bar
        pass

# Vertical dashed line at default sigma*
if default_sigma_star is not None:
    ax.axvline(x=default_sigma_star, color='#C44E52', linestyle='--',
               linewidth=1.5, label=f'Default $\\sigma^*$ = {default_sigma_star:.3f}')

# Labels
labels = []
for td in tornado_data:
    if td['name'] == "C_travel_per_km (at 100 km)":
        labels.append(f"$C_{{travel}}$ (at 100 km)\n[def={td['default']:.4f}]")
    elif td['name'] == "C_signal":
        labels.append(f"$C_{{signal}}$\n[def={td['default']:.2f}]")
    elif td['name'] == "C_opportunity":
        labels.append(f"$C_{{opportunity}}$\n[def={td['default']:.2f}]")
    elif td['name'] == "P_base":
        labels.append(f"$P_{{base}}$\n[def={td['default']:.3f}]")
    elif td['name'] == "lambda_W":
        labels.append(f"$\\lambda_W$\n[def={td['default']:.2f}]")
    elif td['name'] == "lambda_C":
        labels.append(f"$\\lambda_C$\n[def={td['default']:.2f}]")
    elif td['name'] == "lambda_X":
        labels.append(f"$\\lambda_X$\n[def={td['default']:.2f}]")
    elif td['name'] == "k_max":
        labels.append(f"$k_{{max}}$\n[def={td['default']:.1f}]")
    elif td['name'] == "M_half":
        labels.append(f"$M_{{half}}$\n[def={td['default']:.1f}]")
    elif td['name'] == "q_min":
        labels.append(f"$q_{{min}}$\n[def={td['default']:.2f}]")
    elif td['name'] == "q_max":
        labels.append(f"$q_{{max}}$\n[def={td['default']:.2f}]")
    elif td['name'] == "gamma":
        labels.append(f"$\\gamma$\n[def={td['default']:.2f}]")
    elif td['name'] == "delta":
        labels.append(f"$\\delta$\n[def={td['default']:.2f}]")
    else:
        labels.append(f"{td['name']}\n[def={td['default']:.3f}]")

labels.reverse()  # because we plotted bottom-to-top
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=8, fontfamily='sans-serif')
ax.set_xlabel('Critical threshold $\\sigma^*$', fontsize=11, fontfamily='sans-serif')

# Add range annotations on right side
for i, td in enumerate(reversed(tornado_data)):
    if td['min_sigma'] is not None and td['range'] > 0:
        ax.annotate(f'{td["range"]:.3f}',
                    xy=(td['max_sigma'] + 0.005, i),
                    va='center', ha='left', fontsize=7,
                    fontfamily='sans-serif', color='#333333')

ax.legend(fontsize=9, loc='lower right', framealpha=0.9)
ax.set_xlim(0, 1.0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()

outpath_png = os.path.join(os.path.dirname(__file__), '..', 'figures', 'final',
                           'figure_sensitivity_tornado.png')
outpath_png = os.path.abspath(outpath_png)
fig.savefig(outpath_png, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\nTornado plot saved to: {outpath_png}")

# Also save PDF
outpath_pdf = outpath_png.replace('.png', '.pdf')
fig.savefig(outpath_pdf, bbox_inches='tight', facecolor='white')
print(f"PDF saved to: {outpath_pdf}")

plt.close(fig)

# ---------------------------------------------------------------
# Markdown results table
# ---------------------------------------------------------------
md_path = os.path.join(os.path.dirname(__file__), '..', 'docs', 'manuscript',
                       'sensitivity_results.md')
md_path = os.path.abspath(md_path)

with open(md_path, 'w') as f:
    f.write("# Sensitivity Analysis Results\n\n")
    f.write(f"**Fixed context**: epsilon={EPSILON}, n_agg={N_AGG}, "
            f"travel_distance={TRAVEL_DISTANCE} km\n\n")
    f.write(f"**Default sigma* = {default_sigma_star:.4f}**\n\n")

    # Summary tornado table
    f.write("## Tornado Summary (sorted by sensitivity)\n\n")
    f.write("| Parameter | Default | Min sigma* | Max sigma* | Range |\n")
    f.write("|-----------|---------|-----------|-----------|-------|\n")
    for td in tornado_data:
        if td['min_sigma'] is not None:
            f.write(f"| {td['name']} | {td['default']:.4f} | "
                    f"{td['min_sigma']:.4f} | {td['max_sigma']:.4f} | "
                    f"{td['range']:.4f} |\n")
        else:
            f.write(f"| {td['name']} | {td['default']:.4f} | "
                    f"no threshold | no threshold | N/A |\n")

    f.write("\n\n## Full OAT Sweep Results\n\n")
    f.write("| Parameter | Default | Tested Value | sigma* |\n")
    f.write("|-----------|---------|-------------|--------|\n")
    for r in all_results:
        ss_str = f"{r['sigma_star']:.4f}" if r['sigma_star'] is not None else "no threshold"
        f.write(f"| {r['parameter']} | {r['default']:.4f} | "
                f"{r['tested']:.5f} | {ss_str} |\n")

print(f"Results table saved to: {md_path}")
print("\nDone.")
