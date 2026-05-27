# Parameter Summary: Price Equation Extensions for Cooperative Signaling

Quick reference for all parameters in the unified framework.

---

## Fitness Equations

**Cooperator:**
$$W_C(\sigma, \varepsilon, n) = (1 - C_{\text{total}}) \cdot (1 - \alpha \cdot \sigma(1-\varepsilon)) \cdot f(n) \cdot (1 + B_{\text{recip}}) \cdot (1 - m_0(1-r))$$

**Defector:**
$$W_D(\sigma) = R_{\text{ind}} \cdot (1 - \beta \cdot \sigma) \cdot (1 - m_0)$$

**Critical Threshold:**
$$\sigma^* = \frac{R_{\text{ind}} \cdot \gamma_n - A \cdot \gamma_s}{R_{\text{ind}} \cdot \beta \cdot \gamma_n - A \cdot \alpha_{\text{eff}} \cdot \gamma_s}$$

where $A = (1 - C_{\text{total}}) \cdot f(n) \cdot (1 + B_{\text{recip}})$, $\alpha_{\text{eff}} = \alpha(1-\varepsilon)$, $\gamma_s = 1 - m_0(1-r)$, $\gamma_n = 1 - m_0$

---

## Complete Parameter Table

| Parameter | Symbol | Range | Rapa Nui | Chaco | Poverty Point | Lamoka Lake |
|-----------|--------|-------|----------|-------|---------------|-------------|
| **Environmental** | | | | | | |
| Regional uncertainty | $\sigma$ | 0.0--0.80 | 0.31 | 0.17 | 0.45--0.55 | 0.35--0.45 |
| Ecotone advantage | $\varepsilon$ | 0.0--0.50 | 0.00 | 0.15 | 0.35 | 0.30 |
| **Vulnerability** | | | | | | |
| Cooperator vulnerability | $\alpha$ | 0.10--0.50 | 0.30 | 0.30 | 0.40 | 0.35 |
| Defector vulnerability | $\beta$ | 0.50--0.95 | 0.90 | 0.85 | 0.75 | 0.70 |
| **Costs** | | | | | | |
| Travel cost | $C_{\text{travel}}$ | 0.0--0.20 | 0.00 | 0.00 | 0.12 | 0.08 |
| Signal cost | $C_{\text{signal}}$ | 0.0--0.40 | 0.35 | 0.35 | 0.18 | -- |
| Infrastructure cost | $C_{\text{infra}}$ | 0.0--0.25 | -- | -- | -- | 0.12 |
| Opportunity cost | $C_{\text{opp}}$ | 0.0--0.20 | 0.00 | 0.10 | 0.12 | 0.10 |
| Total cost | $C_{\text{total}}$ | 0.0--1.0 | 0.35 | 0.45 | 0.42 | 0.30 |
| Independent advantage | $R_{\text{ind}}$ | 0.90--1.60 | 1.00 | 1.10 | 1.10 | 1.08 |
| **Cooperation (aggregation only)** | | | | | | |
| Benefit coefficient | $b$ | 0.02--0.15 | -- | -- | 0.08 | 0.10 |
| Optimal group size | $n^*$ | 3--30 | -- | -- | 25 | 12 |
| Crowding coefficient | $c$ | 0.005--0.030 | -- | -- | 0.015 | 0.025 |
| Reciprocal benefit | $B_{\text{recip}}$ | 0.0--0.15 | 0.00 | 0.00 | 0.05 | 0.05 |
| **Conflict (territorial only)** | | | | | | |
| Baseline mortality | $m_0$ | 0.05--0.25 | 0.15 | 0.10 | 0.00 | 0.00 |
| Conflict reduction | $r$ | 0.50--0.90 | 0.75 | 0.75 | 0.00 | 0.00 |
| **Outputs** | | | | | | |
| Critical threshold | $\sigma^*$ | 0.0--1.0 | 0.389 | ~0.15 | 0.534 | 0.305 |

---

## Sensitivity Ranking (at Poverty Point baseline)

| Rank | Parameter | Elasticity | Direction |
|------|-----------|-----------|-----------|
| 1 | $\beta$ (defector vulnerability) | -1.86 | Higher $\beta$ lowers $\sigma^*$ |
| 2 | $C_{\text{total}}$ (total cost) | +1.52 | Higher $C$ raises $\sigma^*$ |
| 3 | $\alpha$ (cooperator vulnerability) | +0.78 | Higher $\alpha$ raises $\sigma^*$ |
| 4 | $\varepsilon$ (ecotone advantage) | -0.61 | Higher $\varepsilon$ lowers $\sigma^*$ |
| 5 | $b$ (cooperation benefit) | -0.54 | Higher $b$ lowers $\sigma^*$ |
| 6 | $R_{\text{ind}}$ (independent advantage) | +0.49 | Higher $R_{\text{ind}}$ raises $\sigma^*$ |
| 7 | $B_{\text{recip}}$ (reciprocal benefit) | -0.12 | Higher $B$ lowers $\sigma^*$ |

---

## Case Study Configurations

### Rapa Nui (Territorial signaling)
- Active terms: $C_{\text{signal}}$, $\alpha/\beta$, $m_0/r$
- Inactive: $\varepsilon$, $f(n)$, $B_{\text{recip}}$, $C_{\text{travel}}$

### Chaco Canyon (Territorial signaling + weak ecotone)
- Active terms: $C_{\text{signal}}$, $\alpha/\beta$, $m_0/r$, $\varepsilon$ (weak)
- Inactive: $f(n)$, $B_{\text{recip}}$

### Poverty Point (Aggregation + costly signaling)
- Active terms: $C_{\text{travel}}$, $C_{\text{signal}}$, $C_{\text{opp}}$, $\alpha/\beta$, $\varepsilon$, $f(n)$, $B_{\text{recip}}$
- Inactive: $m_0/r$

### Lamoka Lake (Aggregation, no signaling)
- Active terms: $C_{\text{travel}}$, $C_{\text{infra}}$, $C_{\text{opp}}$, $\alpha/\beta$, $\varepsilon$, $f(n)$, $B_{\text{recip}}$
- Inactive: $C_{\text{signal}}$, $m_0/r$
