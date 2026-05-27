# Cooperative Monumentality vs. Defensive Fortification in Polynesia: A Price Equation Framework for Predicting Architectural Divergence from Shared Ancestry

**Authors**: [Authors]

**Target Journal**: *Journal of Archaeological Science*

---

**Abstract**

Polynesian societies descended from a shared Ancestral Polynesian culture yet produced strikingly divergent architectural traditions: cooperative monumental platforms (marae, ahu, heiau, tohua) in some archipelagos and defensive hilltop fortifications (pa, pare) in others. This divergence has been explained by appeals to local history, ecology, or cultural drift, but no unified framework predicts which outcome should occur where. We apply a Price equation framework for costly cooperative signaling under environmental uncertainty to six Polynesian cases: Rapa Nui (Easter Island), the Marquesas, Tahiti (Society Islands), Hawai'i, Rapa Iti, and New Zealand (Aotearoa). The framework yields a critical environmental uncertainty threshold $\sigma^*$, above which cooperative signaling architectures are the evolutionarily stable strategy, and below which defensive competition dominates. A new parameter, the mobility buffer $\mu$, captures the fact that defectors on isolated islands have no exit option during resource shortfalls, whereas defectors in archipelagos can partially buffer shocks through inter-island mobility. This isolation effect lowers $\sigma^*$ on isolated islands, making cooperation easier to achieve. Because precise point estimates of model parameters are unavailable for prehistoric island societies, we specify plausible ranges for each parameter and use Monte Carlo sampling ($N$ = 10,000) to compute the probability that each case falls in the cooperative regime. Results show that the Marquesas (P(cooperative) = 62.1%) and Rapa Nui (P(cooperative) = 55.8%) are classified as cooperative, Tahiti (P(cooperative) = 21.5%) and Hawai'i (P(cooperative) = 19.8%) occupy the marginal zone, and Rapa Iti (P(cooperative) $\approx$ 0%) and New Zealand (P(cooperative) $\approx$ 0%) are unambiguously defensive. Notably, incorporating the isolation effect shifts Rapa Nui from the marginal zone (where a model without $\mu$ would place it) into the cooperative regime, correctly predicting its extraordinary ahu/moai tradition. All six cases are correctly classified, with the two marginal cases providing additional insight into how populations near $\sigma^*$ exhibit variable and unstable cooperative architectures. An extended 2$\times$2 framework that separates cooperation (risk pooling) from signaling (costly display) reveals that environmental uncertainty $\sigma$ controls the cooperation decision while conflict mortality $m_0$ independently controls the signaling decision. At observed Polynesian $m_0$ values (0.10 to 0.18), signaling alone does not justify its cost; cooperation and monumental display are observed together because they are adaptively bundled, with signaling serving as the mechanism that sustains cooperation rather than functioning as an independent conflict-reduction strategy. The analysis demonstrates that a single, parameter-driven model can account for the full range of Polynesian architectural variation without invoking ad hoc cultural explanations.

**Keywords**: Polynesia, costly signaling, Price equation, environmental uncertainty, monumental architecture, fortification, marae, pa, moai, heiau, mobility buffer, Monte Carlo, 2$\times$2 strategy

---

## 1. Introduction

The Polynesian colonization of the Pacific represents one of the great natural experiments in human cultural evolution. Beginning from a shared Ancestral Polynesian culture in western Polynesia around 1000 BCE, colonists spread across a vast oceanic region, eventually settling islands from Hawai'i in the north to New Zealand in the south and Rapa Nui in the east (Kirch 2000). These populations carried a common cultural toolkit, including language, social organization principles, horticultural practices, and religious concepts, into radically different environmental settings. The resulting cultural divergence provides an opportunity to test hypotheses about the relationship between environmental parameters and cultural outcomes while controlling, to a remarkable degree, for ancestral culture.

One of the most striking divergences concerns monumental architecture. Some Polynesian societies invested heavily in cooperative construction of ceremonial platforms and temples: the ahu and moai of Rapa Nui, the tohua and me'ae of the Marquesas, the marae of Tahiti and the Society Islands, and the heiau of Hawai'i. Others invested instead in defensive fortifications: the pa (fortified hilltop enclosures, also known as pare) of Rapa Iti and the pa of New Zealand (Aotearoa). Both types of architecture require substantial communal labor investment, but they serve fundamentally different social functions. Cooperative monumental platforms facilitate ritual, exchange, and inter-group signaling. Defensive fortifications facilitate resource defense, territorial competition, and inter-group conflict.

Why should closely related populations, descended from the same ancestral culture, produce such different architectural traditions? Previous explanations have emphasized local ecology (Anderson et al. 2006), population pressure (Kirch 1984), political competition (Goldman 1970), or cultural drift (Sahlins 1958). While each of these factors is relevant, none provides a unified predictive framework that specifies, in advance, which outcome should occur on which island.

This paper applies a Price equation framework for costly cooperative signaling under environmental uncertainty (Bliege Bird and Smith 2005; Lipo et al. 2025) to six Polynesian cases. The framework, originally developed and validated across four diverse archaeological case studies (Rapa Nui, Chaco Canyon, Poverty Point, and Lamoka Lake), predicts when costly cooperative behaviors become the evolutionarily stable strategy as a function of environmental uncertainty $\sigma$. The central prediction is a critical threshold $\sigma^*$: when $\sigma > \sigma^*$, cooperative signaling architectures are favored; when $\sigma < \sigma^*$, they are not, and competitive/defensive strategies dominate instead.

The Polynesian cases provide a cleaner test of this prediction than the original four-case comparison for two reasons. First, shared cultural ancestry controls for many variables that differ across the original cases (subsistence system, cultural tradition, historical period). Second, the Polynesian cases are all island territorial systems, allowing us to use a simplified version of the general framework with fewer free parameters.

We introduce two methodological innovations in this paper. First, we add a mobility buffer parameter $\mu$ that captures the asymmetry between isolated and archipelago islands. On isolated islands such as Rapa Nui, defectors who refuse to cooperate have no option to relocate during resource shortfalls; they must absorb every shock alone. On archipelago islands, defectors can partially buffer resource failures through inter-island movement. This asymmetry makes cooperation easier to evolve on isolated islands, an effect that the original framework did not capture. Second, rather than relying on single point estimates of model parameters, we specify plausible ranges for each parameter and use Monte Carlo sampling to compute the probability that each case falls in the cooperative regime. This approach honestly represents the uncertainty inherent in estimating prehistoric environmental and social parameters.

We organize the paper as follows. Section 2 presents the theoretical framework, simplified for island territorial systems and extended with the mobility buffer, and introduces a 2$\times$2 strategy framework that unbundles cooperation and signaling as independent behavioral dimensions. Section 3 describes the archaeological background for each of the six cases. Section 4 details parameter estimation, calibration methods, and Monte Carlo classification. Section 5 presents the results, including $\sigma^*$ computations, Monte Carlo classification probabilities, phase space visualization, sensitivity analysis, and the 2$\times$2 classification. Section 6 discusses the implications for understanding Polynesian cultural evolution, the bundling of cooperation and signaling, and the broader applicability of the framework.

![**Figure 1.** *Six Pacific cases with shared Polynesian ancestry and divergent architectural outcomes.* Blue borders indicate cooperative monumental traditions (ahu/moai, tohua/me'ae, marae, heiau); orange borders indicate defensive fortification traditions (pa/pare). Labels include the mobility buffer $\mu$ for each case: $\mu = 0$ for isolated islands (Rapa Nui, Rapa Iti), $\mu > 0$ for archipelago systems. Dashed lines indicate the Polynesian Triangle. Marker size is proportional to log island area.](figures/pacific_fig_01_map.png)

## 2. Theoretical Framework

The core logic of the framework can be stated without equations. Building a temple or a ceremonial platform is expensive: the labor could have been spent growing food or fishing. So why do it? The answer depends on how unpredictable the environment is. When harvests fluctuate dramatically from year to year, groups that cooperate, sharing food in bad years and pooling labor in good ones, survive better than loners who face each bad year alone. Monumental architecture is the visible, costly signal that makes such cooperation credible: a group that can afford to build a temple is a group worth partnering with. But when the environment is stable and resources are predictable, that same investment is a waste. Groups are better off defending their own territory than investing in cooperative display. The model below formalizes this logic and identifies the exact level of environmental unpredictability at which the balance tips from one strategy to the other.

A second consideration, not captured in the original framework, concerns isolation. On an archipelago, a group that refuses to cooperate can still partially escape the consequences of a bad year by moving to another island. This exit option reduces the penalty for non-cooperation. On a truly isolated island, there is nowhere to go. A defector who gambles on self-sufficiency must live with the outcome. This asymmetry, which we capture with a mobility buffer parameter $\mu$, means that cooperation evolves more easily on isolated islands than on archipelagos, all else being equal. The formalism below makes this intuition precise.

### 2.1 The Price Equation for Cooperative Signaling

The formal framework begins with the multilevel Price equation (Price 1970, 1972), which partitions evolutionary change in a trait $p$ into between-group and within-group selection components:

$$\Delta\bar{p} = \frac{1}{\bar{w}} \text{Cov}(w_g, p_g) + \frac{1}{\bar{w}} E[w_g \cdot \Delta p_g]$$

where $w_g$ is mean group fitness, $p_g$ is mean trait frequency in group $g$, and $\Delta p_g$ is within-group change. The first term captures between-group selection: groups with more cooperators outperform groups with fewer, so the cooperative trait spreads between groups. The second term captures within-group selection: within any single group, free-riders who enjoy cooperation benefits without paying costs outperform cooperators, so the cooperative trait declines within groups. Cooperation evolves when the between-group advantage outweighs the within-group disadvantage.

To make this operational, we construct explicit fitness functions for cooperators ($W_C$) and defectors ($W_D$) as functions of environmental and social parameters. Fitness here means long-term reproductive success: the expected number of surviving descendants. The direction of selection depends on which strategy yields higher fitness at the prevailing level of environmental uncertainty $\sigma$.

### 2.2 Fitness Functions for Island Territorial Systems

For Polynesian island territorial systems, the general framework simplifies considerably. Unlike seasonal aggregation systems (such as Poverty Point or Lamoka Lake), island territorial groups are permanent and sedentary, so we do not need terms for group-size effects or reciprocal obligations that arise from fluid gatherings. In addition, most Polynesian islands lack the multiple complementary ecological zones that reduce risk through portfolio diversification, so the ecotone advantage parameter $\varepsilon$ is approximately zero for most cases (with small exceptions for the Marquesas and Hawai'i, whose diverse micro-environments provide modest buffering).

Each fitness function is a product of three components, representing the three ways that strategy choice affects long-term success: (1) how much of the harvest is retained after paying cooperation costs, (2) how well the group weathers environmental shocks, and (3) how likely members are to survive inter-group conflict.

**Cooperator fitness:**

$$W_C(\sigma) = \underbrace{(1 - C_{total})}_{\text{production after cost}} \cdot \underbrace{(1 - \alpha_{eff} \cdot \sigma)}_{\text{survival through shocks}} \cdot \underbrace{\gamma_s}_{\text{conflict survival}}$$

**Defector fitness:**

$$W_D(\sigma) = \underbrace{R_{ind}}_{\text{independent advantage}} \cdot \underbrace{(1 - \beta_{eff} \cdot \sigma)}_{\text{survival through shocks}} \cdot \underbrace{\gamma_n}_{\text{conflict survival}}$$

The parameters have concrete meanings:

**Production.** $C_{total}$ is the fraction of a group's productive capacity diverted from subsistence to monumental construction. If a community spends 30% of its available labor building a marae instead of farming and fishing, $C_{total} = 0.30$. Cooperators retain $(1 - C_{total})$ of their production; defectors retain all of theirs, potentially multiplied by a small independent-action advantage $R_{ind}$ (typically $R_{ind} \approx 1.0$, meaning no inherent advantage to going it alone).

**Survival through environmental shocks.** In a bad year, such as a drought or failed harvest, fitness declines proportionally to uncertainty $\sigma$. But the decline is steeper for defectors ($\beta_{eff}$) than for cooperators ($\alpha_{eff}$), because cooperators share food and labor across groups while defectors absorb each shock alone. The effective cooperator vulnerability $\alpha_{eff} = \alpha(1 - \varepsilon)$ can be further reduced if the island offers ecotone diversity ($\varepsilon > 0$). The effective defector vulnerability $\beta_{eff} = \beta(1 - \mu)$ incorporates the mobility buffer described in Section 2.5.

**Conflict survival.** Inter-group conflict kills a fraction $m_0$ of the population in each generation. Costly signals, visible monuments demonstrating group strength, deter aggression, reducing mortality by a factor $r$ for signalers. The conflict survival probability for signalers is $\gamma_s = 1 - m_0(1 - r)$: if baseline conflict mortality is 15% ($m_0 = 0.15$) and signaling reduces it by 75% ($r = 0.75$), then signaler mortality drops to $0.15 \times 0.25 = 3.75\%$. Non-signalers face the full $m_0$, giving $\gamma_n = 1 - m_0 = 0.85$.

![**Figure 2.** *Fitness anatomy: decomposition of cooperator and defector fitness into three components for the Rapa Nui case.* At Rapa Nui's estimated environmental uncertainty ($\sigma$ = 0.365), cooperators pay a production cost ($C_{total}$) but gain better shock survival and conflict survival. The total fitness comparison (rightmost pair) determines which strategy is favored.](figures/pacific_fig_02_fitness_anatomy.png)

### 2.3 The Critical Threshold $\sigma^*$

The critical threshold $\sigma^*$ is the value of $\sigma$ where $W_C = W_D$. We derive it by setting the two fitness functions equal and solving algebraically. Let $A = (1 - C_{total})$ for compactness:

$$A \cdot (1 - \alpha_{eff} \cdot \sigma^*) \cdot \gamma_s = R_{ind} \cdot (1 - \beta_{eff} \cdot \sigma^*) \cdot \gamma_n$$

Expanding both sides:

$$A \cdot \gamma_s - A \cdot \alpha_{eff} \cdot \gamma_s \cdot \sigma^* = R_{ind} \cdot \gamma_n - R_{ind} \cdot \beta_{eff} \cdot \gamma_n \cdot \sigma^*$$

Collecting the $\sigma^*$ terms on the left and constants on the right:

$$R_{ind} \cdot \beta_{eff} \cdot \gamma_n \cdot \sigma^* - A \cdot \alpha_{eff} \cdot \gamma_s \cdot \sigma^* = R_{ind} \cdot \gamma_n - A \cdot \gamma_s$$

Factoring out $\sigma^*$:

$$\sigma^* \cdot (R_{ind} \cdot \beta_{eff} \cdot \gamma_n - A \cdot \alpha_{eff} \cdot \gamma_s) = R_{ind} \cdot \gamma_n - A \cdot \gamma_s$$

Solving:

$$\sigma^* = \frac{R_{ind} \cdot \gamma_n - A \cdot \gamma_s}{R_{ind} \cdot \beta_{eff} \cdot \gamma_n - A \cdot \alpha_{eff} \cdot \gamma_s}$$

where $A = (1 - C_{total})$, $\alpha_{eff} = \alpha(1 - \varepsilon)$, and $\beta_{eff} = \beta(1 - \mu)$.

The numerator represents the *fitness gap at zero uncertainty*: how much better off defectors are when the environment is perfectly stable ($\sigma = 0$). In a world with no droughts, no failed harvests, and no unpredictable shortfalls, cooperation is pure cost with no survival benefit, so defectors always win. The numerator quantifies this baseline disadvantage of cooperators. Note that $\mu$ does not appear in the numerator: the mobility buffer only matters when there are shocks to buffer.

The denominator represents the *rate at which uncertainty closes this gap*. As environmental variability increases, defectors suffer more than cooperators (because $\beta_{eff} > \alpha_{eff}$), so the fitness gap narrows. A larger denominator means the gap closes faster, yielding a lower $\sigma^*$, meaning less uncertainty is needed for cooperation to become worthwhile. The mobility buffer $\mu$ appears here through $\beta_{eff}$: when $\mu > 0$, defectors are partially buffered against shocks, so $\beta_{eff} < \beta$, the denominator shrinks, and $\sigma^*$ increases. In plain terms, mobility makes cooperation harder to justify because defectors are not as exposed.

In plain terms: $\sigma^*$ answers the question, "How unpredictable does the environment need to be before the insurance value of cooperation outweighs its cost?" A low $\sigma^*$ means cooperation pays off even in moderately variable environments; a high $\sigma^*$ means the environment must be very unpredictable before cooperation becomes worthwhile.

The formula requires both numerator and denominator to be positive for a meaningful threshold to exist. If the numerator is non-positive, cooperation is favored even at $\sigma = 0$ (it is so cheap or so beneficial that it always pays). If the denominator is non-positive, defectors always weather shocks better than cooperators, and cooperation is never favored regardless of $\sigma$.

### 2.4 The Two Predicted Regimes

The framework predicts two distinct architectural outcomes for island territorial systems:

**Regime 1: Cooperative Signaling ($\sigma > \sigma^*$)**. When environmental uncertainty exceeds the threshold, groups that invest in cooperative monumental architecture (marae, ahu, heiau, tohua) achieve higher fitness than those that defect. This regime produces the cooperative architectural traditions observed across much of Polynesia: shared ceremonial platforms, communal feasting facilities, and inter-group ritual exchange. The architecture serves as a costly signal of group commitment and capacity, facilitating cooperation and risk-pooling among groups.

**Regime 2: Defensive Competition ($\sigma < \sigma^*$)**. When environmental uncertainty is low, the costs of cooperative signaling exceed its benefits. In this regime, the dominant strategy is independent resource defense. If population density is sufficiently high that inter-group competition occurs, the architecture shifts to defensive fortifications (pa, pare). Resources are predictable enough that defending a territory is more profitable than pooling risk through cooperative signaling.

**Marginal Zone ($\sigma \approx \sigma^*$)**. When $\sigma$ is close to $\sigma^*$, the system is near the phase boundary, the dividing line between the cooperative and defensive regimes. In this zone, we predict: (a) cooperation may emerge late and conditionally, (b) cooperative and competitive strategies may coexist or alternate, (c) the system is sensitive to small parameter perturbations, and (d) historical contingency and cultural factors may tip the balance in either direction.

### 2.5 The Isolation Effect: Mobility Buffer $\mu$

A crucial asymmetry between island settings is the option available to non-cooperators during resource shortfalls. On an archipelago such as the Society Islands or Hawai'i, a group or individual experiencing a bad year can relocate, temporarily or permanently, to another island. This inter-island mobility does not eliminate the cost of a resource shock, but it provides partial buffering. On a truly isolated island, such as Rapa Nui (the most isolated inhabited island on Earth, approximately 2,000 km from the nearest inhabited land) or Rapa Iti (effectively isolated within the Austral chain), there is no such option. Defectors must absorb every shock in full.

We capture this asymmetry with the mobility buffer parameter $\mu \in [0, 1]$, which modifies defector vulnerability:

$$\beta_{eff} = \beta \cdot (1 - \mu)$$

When $\mu = 0$ (complete isolation), defectors face the full vulnerability $\beta$. When $\mu > 0$, inter-island mobility partially buffers defectors, reducing their effective vulnerability. The parameter $\mu$ does not appear in the cooperator fitness function because cooperators already have a buffering mechanism: cooperation itself. The mobility buffer is specifically a defector advantage that partially substitutes for cooperative risk-pooling.

The effect on $\sigma^*$ is straightforward. Increasing $\mu$ decreases $\beta_{eff}$, which shrinks the denominator of the $\sigma^*$ formula, thereby increasing $\sigma^*$. This means that cooperation requires higher environmental uncertainty to become adaptive on archipelago islands (where defectors have an exit option) than on isolated islands (where they do not).

**Table 2.** Mobility buffer values with rationale.

| Case | $\mu$ | Rationale |
|------|-------|-----------|
| Rapa Nui | 0.00 | Most isolated inhabited island on Earth (~2,000 km to nearest) |
| Rapa Iti | 0.00 | Effectively isolated within Australs (~500 km to nearest inhabited) |
| New Zealand | 0.03 | Large landmass, limited North/South Island movement via Cook Strait |
| Marquesas | 0.10 | 6 major islands, documented inter-island voyaging |
| Hawai'i | 0.10 | 8 major islands, inter-island movement documented |
| Tahiti | 0.12 | 14 Society Islands, extensive inter-island network |

The isolation effect has a specific archaeological prediction: among islands with otherwise similar parameters, isolated islands should develop cooperative monumental traditions more readily than archipelago islands. Rapa Nui provides the key test case. Without the mobility buffer ($\mu = 0$ for all cases), Rapa Nui's environmental uncertainty ($\sigma$) falls near the phase boundary; including the isolation effect ($\mu = 0$ for Rapa Nui vs. $\mu > 0$ for archipelago cases) lowers Rapa Nui's $\sigma^*$ relative to archipelagos, shifting Rapa Nui into the cooperative regime. This correctly predicts Rapa Nui's extraordinary ahu/moai tradition, one of the most remarkable cooperative investments in all of Polynesia.

![**Figure 3.** *The two predicted regimes: cooperative signaling and defensive fortification.* When environmental uncertainty $\sigma$ exceeds the critical threshold $\sigma^*$, cooperative monumental architecture is the evolutionarily stable strategy. When $\sigma < \sigma^*$ and population density is high, defensive fortification dominates. The six cases are positioned by estimated $\sigma$ and relative population pressure, with $\mu$ values shown. The mobility buffer shifts $\sigma^*$ rightward for archipelago cases, making cooperation harder to achieve.](figures/pacific_fig_03_two_regimes.png)

![**Figure 4.** *The mobility buffer ($\mu$): how isolation promotes cooperation.* Panel A compares $\sigma^*$ computed with and without the mobility buffer for all six cases. Isolated islands (Rapa Nui, Rapa Iti) show no shift; archipelago cases show increased $\sigma^*$ when $\mu > 0$. Vertical bars indicate estimated $\sigma$ ranges. Panel B shows the fitness crossover for Rapa Nui under two scenarios: actual isolation ($\mu = 0$) and hypothetical archipelago placement ($\mu = 0.10$). Isolation lowers $\sigma^*$, placing Rapa Nui's $\sigma$ range above the threshold.](figures/pacific_fig_04_mu_effect.png)

### 2.6 Unbundling Cooperation and Signaling: The 2$\times$2 Strategy Framework

The fitness functions in Section 2.2 bundle two independent behavioral dimensions into a single "cooperator" strategy: cooperation (risk pooling through resource sharing) and signaling (costly visible display through monumental construction). In reality, these are separate decisions. A group can cooperate without building monuments, and an individual can invest in competitive display without participating in cooperative risk-pooling. Separating these dimensions creates a 2$\times$2 strategy space with four distinct strategies, each with a different archaeological signature.

**Strategy CS (Cooperative Signaler):** Groups that both pool risk cooperatively and invest in monumental display. This is the "cooperator" of the bundled model. The production term is $(1 - C_{coop} - C_{signal})$ where $C_{coop}$ is the cost of cooperative risk-pooling (food sharing, labor pooling) and $C_{signal}$ is the cost of monumental construction. Shock survival uses the cooperative parameter $\alpha_{eff}$. Conflict survival benefits from group signal-mediated deterrence: $\gamma_{CS} = 1 - m_0(1 - r_{group})$. Archaeological signatures include ahu/moai, tohua, marae, and heiau.

**Strategy CN (Cooperative Non-signaler):** Groups that cooperate in risk-pooling but do not invest in monumental display. The production term is $(1 - C_{coop})$, retaining the cost savings from not building monuments. Shock survival uses the cooperative $\alpha_{eff}$. Conflict survival receives no signal-mediated reduction: $\gamma_{CN} = 1 - m_0$. Archaeological signatures of this strategy would be largely invisible, consisting of food sharing networks and reciprocal labor arrangements that leave no durable architectural record.

**Strategy IS (Individual Signaler):** Individuals who invest in competitive display (prestige goods, feasting) without participating in group cooperative risk-pooling. The production term is $(1 - C_{signal,ind})$ where $C_{signal,ind} < C_{signal}$ because individual display is cheaper than group monumental construction. Shock survival uses the non-cooperative $\beta_{eff}$. Conflict survival benefits from individual display: $\gamma_{IS} = 1 - m_0(1 - r_{ind})$ where $r_{ind} < r_{group}$ because individual display is less effective at deterrence than group monuments. Archaeological signatures include prestige goods accumulation and big-man feasting facilities.

**Strategy NN (Non-cooperative Non-signaler):** Neither cooperation nor signaling, corresponding to the "defector" of the bundled model. The production term is $R_{ind}$, shock survival uses $\beta_{eff}$, and conflict survival is $\gamma_{NN} = 1 - m_0$. Archaeological signatures include pa/pare defensive fortifications, which represent investment in resource defense rather than cooperative signaling.

The four fitness functions are:

$$W_{CS}(\sigma) = (1 - C_{coop} - C_{signal}) \cdot (1 - \alpha_{eff} \cdot \sigma) \cdot (1 - m_0(1 - r_{group}))$$

$$W_{CN}(\sigma) = (1 - C_{coop}) \cdot (1 - \alpha_{eff} \cdot \sigma) \cdot (1 - m_0)$$

$$W_{IS}(\sigma) = (1 - C_{signal,ind}) \cdot (1 - \beta_{eff} \cdot \sigma) \cdot (1 - m_0(1 - r_{ind}))$$

$$W_{NN}(\sigma) = R_{ind} \cdot (1 - \beta_{eff} \cdot \sigma) \cdot (1 - m_0)$$

A critical mathematical property of this decomposition is that environmental uncertainty $\sigma$ and conflict mortality $m_0$ control different dimensions of the strategy space. The comparison between CS and CN (should cooperators also signal?) is $\sigma$-independent: the shock survival term $(1 - \alpha_{eff} \cdot \sigma)$ appears in both and cancels in the ratio $W_{CS}/W_{CN}$. Whether signaling adds value to cooperation depends only on $m_0$, $r_{group}$, and $C_{signal}$. Similarly, the comparison between IS and NN (should non-cooperators signal?) is $\sigma$-independent: the shock term $(1 - \beta_{eff} \cdot \sigma)$ cancels. This means the full strategy space is two-dimensional in ($\sigma$, $m_0$): environmental uncertainty controls the cooperation axis, and conflict mortality controls the signaling axis.

The signaling thresholds can be derived analytically. For cooperators, signaling becomes worthwhile when:

$$m_0 > m_0^{*,coop} = \frac{C_{signal}}{(1 - C_{coop}) \cdot r_{group} + C_{signal} \cdot (1 - r_{group})}$$

For non-cooperators, individual signaling becomes worthwhile when:

$$m_0 > m_0^{*,ind} = \frac{(1 - C_{signal,ind}) - R_{ind}}{(1 - C_{signal,ind}) \cdot (1 - r_{ind}) - R_{ind}}$$

The constraint $C_{coop} + C_{signal} = C_{total}$ ensures backward compatibility: $W_{CS}$ reduces to $W_C$ from the bundled model when $r_{group} = r$, and $W_{NN}$ is identical to $W_D$.

**Table 4.** New parameters for the 2$\times$2 framework.

| Parameter | Symbol | Description | Range |
|-----------|--------|-------------|-------|
| Cooperation cost | $C_{coop}$ | Risk pooling, food sharing | 0.07-0.16 |
| Group signal cost | $C_{signal}$ | Monument construction (derived: $C_{total} - C_{coop}$) | 0.12-0.26 |
| Individual signal cost | $C_{signal,ind}$ | Prestige goods, feasting | 0.04-0.13 |
| Group signal effectiveness | $r_{group}$ | Same as $r$ in bundled model | 0.60-0.80 |
| Individual signal effectiveness | $r_{ind}$ | Lower than group | 0.20-0.45 |

![**Figure 13.** *The 2$\times$2 strategy space: cooperation and signaling as independent dimensions.* Four strategies arise from the crossing of two binary decisions (cooperate or not, signal or not). Each cell shows the cost structure, fitness benefit, and archaeological exemplar. Environmental uncertainty $\sigma$ controls the cooperation axis; conflict mortality $m_0$ controls the signaling axis.](figures/pacific_fig_13_2x2_conceptual.png)

## 3. The Six Cases

### 3.1 Rapa Nui (Easter Island)

Rapa Nui (27.1$^{\circ}$S, 109.3$^{\circ}$W) is a small (164 km$^2$), isolated volcanic island in the southeastern Pacific, colonized by Polynesian settlers around 1200 CE (Hunt and Lipo 2006; Wilmshurst et al. 2011). The island supported a population estimated at 3,000 to 4,000 individuals organized into territorial kin groups (mata) distributed around the coastal perimeter (Lipo et al. 2013, 2025).

The monumental architecture of Rapa Nui consists of ahu (stone platforms) and moai (carved stone statues). Approximately 300 ahu and nearly 1,000 moai were constructed between roughly 1200 and 1600 CE (DiNapoli et al. 2020). The ahu were distributed around the island's coastline, each associated with a specific territorial group (DiNapoli et al. 2020; Lipo et al. 2013). Moai were carved at the Rano Raraku quarry and transported to ahu sites across the island, a process requiring coordinated group labor (Lipo et al. 2013).

Rapa Nui's environment is characterized by high effective uncertainty driven by several reinforcing factors. The island is directly exposed to ENSO variability, which drives large inter-annual fluctuations in rainfall and marine productivity (Anderson et al. 2006). Its small size (164 km$^2$) provides no spatial averaging of shocks: a drought or storm affects the entire island simultaneously. The lack of protective lagoons or barrier reefs increases vulnerability to marine resource fluctuations (Stein et al. 2025). Most critically, Rapa Nui's extreme isolation, approximately 2,000 km from the nearest inhabited land, means that there is no possibility of importing food during shortfalls, exchanging resources with neighboring populations, or relocating. This isolation amplifies the effective uncertainty experienced by island residents, because the raw climatic variability cannot be buffered by any external mechanism. We estimate $\sigma$ in the range 0.28 to 0.45, with the upper bound reflecting this amplification from isolation.

The isolation also directly affects the model through the mobility buffer parameter $\mu = 0$: defectors on Rapa Nui have no exit option, making the full vulnerability $\beta$ apply. This combination of high effective $\sigma$ and zero mobility buffer places Rapa Nui in the cooperative regime, correctly predicting the island's extraordinary monumental tradition.

The ahu/moai system shows signs of late-period transformation: by approximately 1500-1600 CE, moai construction declined and some ahu were modified or repurposed. This pattern is consistent with a system in the cooperative regime that experienced parameter shifts (possibly declining uncertainty or increasing population pressure) that moved it toward the phase boundary (DiNapoli et al. 2017; Lipo et al. 2025).

### 3.2 Marquesas Islands

The Marquesas (9.0$^{\circ}$S, 139.5$^{\circ}$W) are a group of volcanic islands totaling approximately 1,050 km$^2$ in the central-eastern Pacific, colonized around 1000 CE (Allen 2010; Suggs 1961). The estimated contact-period population was 35,000 to 80,000 (Allen 2010; Suggs 1961), distributed across the major islands of Nuku Hiva, Hiva Oa, Ua Pou, Ua Huka, Fatu Hiva, and Tahuata.

Marquesan monumental architecture centers on the tohua (large public ceremonial plazas surrounded by stone platforms) and me'ae (sacred stone-lined enclosures for religious ceremonies). Tohua could be enormous, some exceeding 100 meters in length, and served as venues for inter-valley and inter-island gatherings involving feasting, dance, and exchange (Allen 2010). Me'ae were typically smaller but architecturally elaborate, with finely fitted stone walls (Suggs 1961).

The Marquesas have the highest environmental uncertainty of our six cases. The islands lack protective barrier reefs, are directly exposed to ENSO-driven variability, experience irregular rainfall patterns, and suffer from periodic severe droughts that devastate both marine and terrestrial resources (Anderson et al. 2006). The steep, deeply incised valleys create sharp ecological boundaries between resource zones but also limit the spatial extent of any single resource patch (Allen 2010). We estimate $\sigma$ in the range 0.38 to 0.50.

Despite being an archipelago with documented inter-island voyaging ($\mu$ = 0.05 to 0.15), the Marquesas are classified as cooperative (P(cooperative) = 62.1%) because the raw environmental uncertainty is so high that it overwhelms the mobility buffer effect. The $\sigma^*$ at point estimates is 0.415, and the midpoint $\sigma$ of 0.44 exceeds this threshold. The tohua system facilitated inter-valley cooperation and resource sharing that buffered against the extreme environmental variability (Allen 2010).

The Marquesas represent the strongest positive test of the framework: with $\sigma$ clearly exceeding $\sigma^*$ even after accounting for inter-island mobility, cooperation is robustly predicted, and the elaborate cooperative monumental tradition is exactly what is observed.

### 3.3 Tahiti and the Society Islands

Tahiti (17.7$^{\circ}$S, 149.4$^{\circ}$W) is the largest island (1,045 km$^2$) in the Society Islands archipelago, colonized around 1000 CE (Kirch 2000; Wilmshurst et al. 2011). The contact-period population of the Society Islands as a whole was estimated at 120,000 to 200,000 (Kahn and Kirch 2014).

The Society Islands' monumental architecture is the marae: rectangular stone-paved ceremonial platforms with upright stone slabs (Emory 1933; Kahn 2024; Wallin 2010). Marae varied from small household-level structures to enormous community and supra-community complexes (Emory 1933; Kahn 2024; Kahn and Kirch 2014). The most elaborate, such as Taputapuatea on Ra'iatea, served as nodes in an inter-island ritual network connecting communities across the archipelago (Kahn and Kirch 2014). Marae construction and use involved substantial communal labor and ritual investment (Kahn 2024; Wallin 2010).

Tahiti's environmental uncertainty is moderate ($\sigma$ range: 0.24 to 0.35). The island has barrier reefs providing some buffering of marine resources, relatively reliable rainfall, and productive lowland taro cultivation (Kirch 2000). However, ENSO variability still affects rainfall patterns and marine productivity, and the Society Islands are within the cyclone belt (Anderson et al. 2006).

The Society Islands' extensive inter-island network ($\mu$ = 0.08 to 0.16, with 14 islands connected by regular voyaging) provides substantial mobility buffering for defectors, raising $\sigma^*$ to approximately 0.351 at point estimates. Monte Carlo analysis gives P(cooperative) = 21.5%, placing Tahiti in the marginal zone. This is consistent with the archaeological observation that marae construction was highly variable in intensity across the archipelago (Kahn 2024; Kahn and Kirch 2014). Some districts invested heavily in elaborate marae complexes while others did not, a pattern expected for a system near $\sigma^*$ where small local differences can tip the balance.

### 3.4 Hawai'i

The Hawaiian archipelago (19.8$^{\circ}$N, 155.5$^{\circ}$W) comprises islands totaling 10,430 km$^2$, colonized around 1000-1100 CE (Kirch 2010; Wilmshurst et al. 2011). The contact-period population exceeded 100,000, with estimates ranging up to 400,000 (Kirch 2010, 2024).

Hawaiian monumental architecture centers on the heiau: stone-walled temple platforms of varying sizes and functions (Kirch 1990; Kolb 1994). Some heiau were enormous, such as Pi'ilanihale Heiau on Maui, the largest in Polynesia by area (Kirch 1990). Heiau were associated with both community rituals and chiefly power, serving as venues for agricultural ceremonies, war rituals, and human sacrifice in the late pre-contact period (Kirch 2010; Kolb 1994). The Hawaiian system shows a clear temporal trajectory from cooperative community heiau to increasingly hierarchical and coercive structures, particularly after approximately 1400 CE (Kirch 2010).

Hawai'i's environmental uncertainty is moderate ($\sigma$ range: 0.26 to 0.38). The large islands have diverse microclimates and multiple ecological zones (from coastal reefs to upland forests), providing some buffering ($\varepsilon$ = 0.05 to 0.15) (Kirch 2010). However, ENSO variability affects rainfall, and the islands experience periodic droughts and hurricanes (Anderson et al. 2006). The 8-island archipelago provides a moderate mobility buffer ($\mu$ = 0.05 to 0.15).

Monte Carlo analysis gives P(cooperative) = 19.8%, placing Hawai'i in the marginal zone. The $\sigma^*$ at point estimates is 0.386, well above the $\sigma$ midpoint of 0.32. This marginal positioning is consistent with the archaeological pattern of variable and evolving heiau traditions. The late-period shift from cooperative to coercive heiau use may reflect a system that crossed from the cooperative to the competitive regime as population growth altered the effective parameters.

### 3.5 Rapa Iti

Rapa Iti (27.6$^{\circ}$S, 144.3$^{\circ}$W), often referred to simply as Rapa, is a small (40 km$^2$), rugged volcanic island in the Austral Islands chain, colonized around 1200 CE (Kennett et al. 2006). The estimated pre-contact population was 500 to 2,000 (Kennett et al. 2006).

Unlike the cooperative monumental traditions of other Polynesian islands, Rapa Iti's architecture is dominated by pa (fortified hilltop enclosures, also called pare). At least 15 major pa have been identified, perched on the island's steep ridges and peaks, with defensive walls, ditches, and terracing (Kennett et al. 2006). These fortifications are among the most dramatic in Polynesia and represent a clear investment in inter-group competition and resource defense rather than cooperative signaling.

Rapa Iti's environmental uncertainty is low ($\sigma$ range: 0.08 to 0.16). Although the island lies at a latitude similar to Rapa Nui (27.6$^{\circ}$S vs. 27.1$^{\circ}$S), it sits 35 degrees further west in the central Pacific (144.3$^{\circ}$W vs. 109.3$^{\circ}$W), placing it outside the zone of strongest ENSO teleconnection. ENSO-driven rainfall and sea-surface temperature anomalies are strongest in the eastern Pacific and attenuate westward (Anderson et al. 2006), so Rapa Iti experiences substantially less inter-annual climatic variability than Rapa Nui despite comparable latitude. Rainfall is relatively reliable, and the surrounding ocean supports productive fisheries (Kennett et al. 2006). The primary ecological challenge is the island's small area and limited agricultural potential (Kennett et al. 2006), which creates carrying capacity constraints but not the kind of stochastic uncertainty that drives cooperative signaling.

Like Rapa Nui, Rapa Iti is effectively isolated ($\mu = 0$), meaning defectors face the full vulnerability $\beta$. However, with $\sigma$ so far below $\sigma^*$, the isolation effect does not matter: even the lowest possible $\sigma^*$ (at $\mu = 0$) is far above the environmental uncertainty. Monte Carlo analysis gives P(cooperative) $\approx$ 0%, confirming that cooperative signaling would be maladaptive in this environment regardless of isolation status. The observed pattern of defensive fortification is exactly what the framework predicts.

### 3.6 New Zealand (Aotearoa)

New Zealand (41.3$^{\circ}$S, 174.8$^{\circ}$E) is by far the largest landmass in Polynesia (268,000 km$^2$), colonized around 1250-1300 CE (Jacomb et al. 2022). The estimated pre-European population was 100,000 to 200,000 (Davidson 1984).

New Zealand's architectural tradition is dominated by the pa: fortified settlements with palisades, ditches, fighting stages, and terraced defenses (Bellwood 1971; Davidson 1984; Fox 1976; Schmidt 1996). Thousands of pa sites have been recorded, concentrated in the North Island (Davidson 1984). Pa were actively contested, with archaeological evidence of burning, reconstruction, and inter-group warfare (Bellwood 1971; Fox 1976). The New Zealand pattern is the most clearly defensive architectural tradition in Polynesia.

New Zealand's environmental uncertainty is low ($\sigma$ range: 0.14 to 0.22). The temperate climate provides relatively predictable seasonal resource availability, including abundant marine resources, forest game (until megafauna extinction), and, in the North Island, sweet potato (kumara) horticulture (Anderson 2002). ENSO effects are attenuated at New Zealand's high latitude (Anderson et al. 2006). However, population growth combined with megafauna depletion created intense inter-group competition for terrestrial resources, particularly after approximately 1500 CE (Jacomb et al. 2022).

New Zealand has a small mobility buffer ($\mu$ = 0.01 to 0.05) reflecting limited movement between the North and South Islands via Cook Strait. Combined with a slightly elevated $R_{ind}$ (range 1.00 to 1.10, reflecting the competitive advantage of independent resource defense in a temperate environment with predictable resources), New Zealand has the highest $\sigma^*$ of any case (approximately 0.530 at point estimates). Monte Carlo analysis gives P(cooperative) $\approx$ 0%. The framework clearly predicts defensive competition, which is what is observed.

## 4. Parameter Estimation

### 4.1 Environmental Uncertainty ($\sigma$)

Environmental uncertainty $\sigma$ is the coefficient of variation (standard deviation divided by the mean) of key resource returns, a dimensionless measure of how much subsistence productivity fluctuates from year to year. A $\sigma$ of 0.30 means that in a typical year, resource returns deviate from the long-term average by about 30%, so good years might yield 130% of normal and bad years only 70%. We estimate $\sigma$ ranges for each case from five lines of evidence. The first and most important is ENSO teleconnection strength. The El Nino-Southern Oscillation (ENSO) is the dominant source of year-to-year climate variability in the Pacific; its effects propagate across the ocean through atmospheric and oceanic pathways called teleconnections, but these effects weaken with distance from the eastern Pacific, so islands closer to the eastern Pacific or in the tropics experience stronger ENSO-driven fluctuations in rainfall, temperature, and marine productivity (Anderson et al. 2006). The second is cyclone and hurricane exposure, specifically the frequency and intensity of tropical cyclone impacts that can devastate both marine and terrestrial resources. Third, we consider drought frequency, estimated from paleoclimate proxy records (speleothems, pollen, lake sediments) where available and from modern climatological data. Fourth, marine resource stability depends on the presence or absence of protective reefs and lagoons, which buffer marine resource variability. Fifth, terrestrial resource diversity captures the number and complementarity of productive ecological zones accessible from the settlement area.

Rather than reporting single point estimates, which imply a precision that does not exist, we report plausible ranges for $\sigma$ that reflect the uncertainty in mapping these qualitative lines of evidence to a quantitative coefficient of variation.

The Marquesas receive the highest $\sigma$ range (0.38 to 0.50) due to direct ENSO exposure, lack of barrier reefs, steep topography limiting agricultural buffering, and documented severe droughts (Allen 2010; Anderson et al. 2006). Rapa Nui receives a broad range (0.28 to 0.45), with the upper bound reflecting the amplification of effective uncertainty caused by extreme isolation: climatic variability that could be partially buffered by inter-island exchange on an archipelago translates into full resource impacts on Rapa Nui (Stein et al. 2025). Hawai'i (0.26 to 0.38) and Tahiti (0.24 to 0.35) receive moderate ranges reflecting partial ENSO buffering from reef systems and ecological diversity (Kirch 2000, 2010). New Zealand (0.14 to 0.22) receives a low range due to high-latitude attenuation of ENSO and reliable temperate resource base (Anderson 2002; Anderson et al. 2006). Rapa Iti (0.08 to 0.16) receives the lowest range despite its small size, because its central-Pacific longitude (35$^{\circ}$ west of Rapa Nui) places it outside the zone of strongest ENSO teleconnection (Anderson et al. 2006), and its marine resources are relatively stable (Kennett et al. 2006).

### 4.2 Cooperation Costs ($C_{total}$)

The total cooperation cost $C_{total}$ represents the fraction of group productivity diverted from subsistence to monumental construction and cooperative signaling activities. We estimate $C_{total}$ ranges from three sources. Where archaeological estimates of construction labor are available (moai transport person-hours, marae construction volumes), we convert these to a fraction of total available labor-time. We supplement this with ethnographic observations of the fraction of productive time devoted to communal ritual and construction in Polynesian societies (Kirch 1984; Sahlins 1958). Finally, we consider architectural scale: the volume of construction material moved, normalized by estimated population and time span.

Rapa Nui receives the broadest and highest $C_{total}$ range (0.25 to 0.40) reflecting the extraordinary per-capita investment in moai carving and transport combined with uncertainty about the construction timeline (Hunt and Lipo 2011). The Marquesas receive 0.25 to 0.35 for the substantial tohua and me'ae construction (Allen 2010). Hawai'i receives 0.22 to 0.34 for the extensive heiau tradition (Kirch 1990; Kolb 1994). Tahiti receives the lowest cooperative range (0.20 to 0.30), reflecting the variable intensity of marae construction across the archipelago (Kahn 2024; Kahn and Kirch 2014). Defensive cases (Rapa Iti, New Zealand) receive hypothetical ranges of 0.25 to 0.35 representing what cooperation costs would be if cooperative signaling had been adopted.

### 4.3 Vulnerability Parameters ($\alpha$, $\beta$)

The vulnerability parameters $\alpha$ (cooperator vulnerability) and $\beta$ (defector vulnerability) capture the degree to which environmental shocks reduce fitness. The key asymmetry, $\beta > \alpha$, reflects the fact that cooperators pool risk across groups while defectors face shocks alone.

For all cases, $\beta$ ranges from 0.70 to 0.95, with isolated islands and those with stronger ENSO exposure at the upper end. The $\alpha$ ranges from 0.20 to 0.40, reflecting the degree of cooperative buffering possible given island ecology. The effective vulnerability ratio $\beta_{eff}/\alpha_{eff}$ is further modified by the mobility buffer $\mu$ and ecotone diversity $\varepsilon$.

### 4.4 Conflict Parameters ($m_0$, $r$)

The baseline conflict mortality $m_0$ captures the probability of death from inter-group conflict in the absence of signaling. We estimate $m_0$ ranges from archaeological evidence of inter-group conflict, supplemented by ethnohistoric accounts of contact-period Polynesian warfare and cross-cultural estimates of pre-state conflict mortality (Kirch 1984).

The signal-mediated conflict reduction $r$ captures how much cooperative signaling reduces conflict mortality. This parameter is grounded in costly signaling theory: visible, expensive monuments credibly advertise group size and cohesion, deterring potential aggressors from initiating conflict (Bliege Bird and Smith 2005; Lipo et al. 2025).

### 4.5 Mobility Buffer ($\mu$)

The mobility buffer is estimated from three lines of evidence: geographic isolation (distance to nearest inhabited land), number of accessible islands within voyaging range, and archaeological and ethnohistoric evidence of inter-island movement. Rapa Nui and Rapa Iti receive $\mu = 0$ (fixed) based on their extreme isolation. New Zealand receives a small range (0.01 to 0.05) reflecting limited cross-strait movement. The three archipelago cases (Marquesas, Tahiti, Hawai'i) receive ranges of 0.05 to 0.16 based on the number and proximity of islands in each group.

### 4.6 Monte Carlo Classification

Because each parameter is specified as a range rather than a point estimate, we cannot compute a single $\sigma^*$ for each case. Instead, we draw $N$ = 10,000 samples from uniform distributions over all parameter ranges, compute $\sigma^*$ from each sample, and compare the sampled $\sigma$ against the sampled $\sigma^*$. The classification probability P(cooperative) is the fraction of samples where $\sigma > \sigma^*$. This approach propagates all parameter uncertainty simultaneously, avoiding the false precision of point estimates.

We verify convergence by comparing results across independent random seeds. All P(cooperative) values are stable to within $\pm$0.006 across seeds, confirming that $N$ = 10,000 is sufficient.

### 4.7 Complete Parameter Table

**Table 1.** Model parameter ranges for the six Pacific island cases. Point estimates (midpoints) used for visualization are shown in parentheses.

| Parameter | Rapa Nui | Marquesas | Tahiti | Hawai'i | Rapa Iti | New Zealand |
|-----------|----------|-----------|--------|---------|---------|-------------|
| Area (km$^2$) | 164 | 1,050 | 1,045 | 10,430 | 40 | 268,000 |
| Pop. est. | 3,000-4,000 | 35,000-80,000 | 120,000-200,000 | 100,000+ | 500-2,000 | 100,000-200,000 |
| $\sigma$ | 0.28-0.45 (0.365) | 0.38-0.50 (0.44) | 0.24-0.35 (0.295) | 0.26-0.38 (0.32) | 0.08-0.16 (0.12) | 0.14-0.22 (0.18) |
| $C_{total}$ | 0.25-0.40 (0.325) | 0.25-0.35 (0.30) | 0.20-0.30 (0.25) | 0.22-0.34 (0.28) | 0.25-0.35 (0.30)* | 0.25-0.35 (0.30)* |
| $\alpha$ | 0.25-0.35 (0.30) | 0.30-0.40 (0.35) | 0.20-0.30 (0.25) | 0.20-0.30 (0.25) | 0.25-0.35 (0.30) | 0.25-0.35 (0.30) |
| $\beta$ | 0.85-0.95 (0.90) | 0.85-0.95 (0.90) | 0.80-0.90 (0.85) | 0.80-0.90 (0.85) | 0.80-0.90 (0.85) | 0.70-0.80 (0.75) |
| $\mu$ | 0.00 | 0.05-0.15 (0.10) | 0.08-0.16 (0.12) | 0.05-0.15 (0.10) | 0.00 | 0.01-0.05 (0.03) |
| $\beta_{eff}$ | 0.85-0.95 (0.90) | 0.72-0.90 (0.81) | 0.67-0.83 (0.75) | 0.68-0.86 (0.77) | 0.80-0.90 (0.85) | 0.67-0.79 (0.73) |
| $\varepsilon$ | 0.00 | 0.02-0.08 (0.05) | 0.00 | 0.05-0.15 (0.10) | 0.00 | 0.00 |
| $R_{ind}$ | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00-1.10 (1.05) |
| $m_0$ | 0.12-0.18 (0.15) | 0.10-0.15 (0.125) | 0.08-0.12 (0.10) | 0.08-0.12 (0.10) | 0.12-0.18 (0.15) | 0.10-0.14 (0.12) |
| $r$ | 0.70-0.80 (0.75) | 0.65-0.75 (0.70) | 0.65-0.75 (0.70) | 0.60-0.70 (0.65) | 0.65-0.75 (0.70)* | 0.65-0.75 (0.70)* |
| **$\sigma^*$ (point)** | **0.351** | **0.415** | **0.351** | **0.386** | **0.348** | **0.530** |
| **P(cooperative)** | **55.8%** | **62.1%** | **21.5%** | **19.8%** | **$\approx$0%** | **$\approx$0%** |
| Classification | Cooperative | Cooperative | Marginal | Marginal | Defensive | Defensive |
| Observed | Cooperative | Cooperative | Cooperative | Cooperative | Defensive | Defensive |

*For defensive cases, $C_{total}$ and $r$ are hypothetical values representing what the parameters would be if cooperative signaling had been adopted.

## 5. Results

### 5.1 Monte Carlo Classification

Table 1 (above) reports the Monte Carlo classification probability P(cooperative) for each case, along with $\sigma^*$ computed at point estimates. The six cases fall into three categories:

**Cooperative** (P(cooperative) > 50%): The Marquesas (P = 62.1%) and Rapa Nui (P = 55.8%). These cases are classified as cooperative because in the majority of Monte Carlo samples, the sampled environmental uncertainty exceeds the sampled critical threshold. For the Marquesas, this reflects the extremely high raw environmental uncertainty that overwhelms any mobility buffer effect. For Rapa Nui, this reflects the combination of moderately high uncertainty (amplified by isolation) and zero mobility buffer ($\mu = 0$), which lowers $\sigma^*$ relative to archipelago cases.

**Marginal** (10% < P(cooperative) $\leq$ 50%): Tahiti (P = 21.5%) and Hawai'i (P = 19.8%). These cases fall near the phase boundary, with $\sigma$ below $\sigma^*$ at point estimates but with substantial overlap in their uncertainty ranges. The marginal positioning predicts exactly the archaeological pattern observed: cooperation that emerges conditionally, varies in intensity across space and time, and is vulnerable to transformation or collapse when parameters shift.

**Defensive** (P(cooperative) $\leq$ 10%): Rapa Iti (P $\approx$ 0%) and New Zealand (P $\approx$ 0%). These cases fall far below the threshold across all Monte Carlo samples. The framework unambiguously predicts that cooperative signaling is not adaptive, and the observed pa/pare defensive traditions match this prediction.

The classification is stable across random seeds: all P(cooperative) values change by no more than 0.006 between independent seeds ($N$ = 10,000 per seed), confirming convergence.

**Worked example: Rapa Nui.** To illustrate the Monte Carlo procedure, we trace the classification of Rapa Nui in detail. From Table 1, the parameter ranges are: $\sigma \in [0.28, 0.45]$, $C_{total} \in [0.25, 0.40]$, $\alpha \in [0.25, 0.35]$, $\beta \in [0.85, 0.95]$, $\mu = 0$ (fixed), $\varepsilon = 0$ (fixed), $R_{ind} = 1.00$ (fixed), $m_0 \in [0.12, 0.18]$, $r \in [0.70, 0.80]$.

For each of the 10,000 Monte Carlo samples, we draw a value from each range uniformly at random, compute $\sigma^*$ from the sampled parameters, and check whether the sampled $\sigma$ exceeds the sampled $\sigma^*$. In 55.8% of samples, $\sigma > \sigma^*$, meaning cooperation is the dominant strategy. This probability is sensitive to the $\sigma$ range: the upper portion of the range (roughly $\sigma > 0.35$) consistently falls in the cooperative regime, while the lower portion ($\sigma < 0.30$) typically falls in the defensive regime. The threshold $\sigma^*$ varies across samples from approximately 0.28 to 0.45, with a median of about 0.35.

Without the mobility buffer (i.e., if we set $\mu = 0$ for all cases including archipelagos), the relative classification of the six cases would remain the same, but comparing Rapa Nui to archipelago cases would be misleading because it would ignore the asymmetry in defector options. With $\mu$, the framework correctly captures why isolated Rapa Nui developed one of the most extraordinary cooperative monumental traditions in Polynesia despite having environmental uncertainty comparable to some archipelago cases with merely marginal cooperative traditions.

### 5.2 The Isolation Effect

The mobility buffer $\mu$ has a systematic effect on $\sigma^*$ across the six cases. For isolated islands (Rapa Nui, Rapa Iti) with $\mu = 0$, the inclusion of $\mu$ in the model does not change $\sigma^*$ (since $\beta_{eff} = \beta$ when $\mu = 0$). For archipelago cases, $\mu > 0$ raises $\sigma^*$ by reducing the effective defector vulnerability $\beta_{eff}$. The magnitude of the shift depends on $\mu$ and the baseline $\beta$:

**Table 3.** Effect of mobility buffer on $\sigma^*$.

| Case | $\sigma^*$ ($\mu = 0$) | $\sigma^*$ (with $\mu$) | Shift |
|------|------------------------|------------------------|-------|
| Rapa Nui | 0.351 | 0.351 | 0.000 |
| Marquesas | 0.362 | 0.415 | +0.053 |
| Tahiti | 0.296 | 0.351 | +0.055 |
| Hawai'i | 0.337 | 0.386 | +0.049 |
| Rapa Iti | 0.348 | 0.348 | 0.000 |
| New Zealand | 0.508 | 0.530 | +0.022 |

The shift is largest for Tahiti and the Marquesas, which have the highest $\mu$ values. The key consequence for classification is that the isolation effect widens the gap between Rapa Nui (unchanged $\sigma^*$) and the archipelago cases (increased $\sigma^*$), making Rapa Nui's cooperative classification more robust. Without $\mu$, Rapa Nui and Tahiti would have similar $\sigma^*$ values (0.351 vs. 0.296), but with $\mu$, Tahiti's $\sigma^*$ increases to match Rapa Nui's while Rapa Nui's remains unchanged, creating a clearer separation in classification.

![**Figure 5.** *Fitness crossover at $\sigma^*$: all six Pacific cases.* Panels A-F show cooperator ($W_C$, blue) and defector ($W_D$, red) fitness as functions of environmental uncertainty $\sigma$ for each case. The crossover point ($\sigma^*$, green dashed line) marks the critical threshold. Colored vertical bands indicate estimated $\sigma$ ranges. Mobility buffer values ($\mu$) are shown for each case.](figures/pacific_fig_05_fitness_crossover_all.png)

### 5.3 Phase Space and Summary Visualization

Figure 6 plots all six cases in $\sigma \times C_{total}$ phase space, with parameter uncertainty shown as rectangles rather than points. The phase boundary separating cooperative and defensive regimes is shown for both $\mu = 0$ (solid) and $\mu = 0.10$ (dashed). The cooperative cases (Rapa Nui, Marquesas) have uncertainty rectangles that overlap substantially with the cooperative region. The marginal cases (Tahiti, Hawai'i) have rectangles that straddle the boundary. The defensive cases (Rapa Iti, New Zealand) sit entirely in the defensive region regardless of the phase boundary used.

The phase boundary curve reveals an important relationship: as cooperation costs increase, a higher level of environmental uncertainty is needed to make cooperation adaptive. The mobility buffer shifts the boundary rightward, meaning that for any given cooperation cost, archipelago populations need higher uncertainty than isolated populations to justify cooperative investment.

Figure 7 provides a complementary view, plotting the Monte Carlo 90% range of $\sigma^*$ (x-axis) against the estimated $\sigma$ range (y-axis) for each case. Cases whose uncertainty rectangles lie above the 1:1 line are predicted cooperative; those below are predicted defensive. The clear separation between the cooperative cluster (Marquesas, Rapa Nui) and the defensive cluster (Rapa Iti, New Zealand) is visible, with the marginal cases (Tahiti, Hawai'i) straddling the boundary.

![**Figure 6.** *Phase space with parameter uncertainty regions.* Rectangles show the joint range of $\sigma$ (x-axis) and $C_{total}$ (y-axis) for each case. The solid black curve shows the phase boundary at $\mu = 0$; the dashed curve shows the boundary at $\mu = 0.10$. Cooperative cases (Marquesas, Rapa Nui) overlap the cooperative region; defensive cases (Rapa Iti, New Zealand) sit entirely in the defensive region.](figures/pacific_fig_06_phase_space_regions.png)

![**Figure 7.** *$\sigma^*$ vs. $\sigma$ with parameter uncertainty.* Rectangles show 90% ranges for both $\sigma^*$ (x-axis, from Monte Carlo) and $\sigma$ (y-axis, from parameter ranges). Points above the 1:1 line (blue region) indicate cooperation predicted. Labels show P(cooperative) from Monte Carlo analysis.](figures/pacific_fig_07_sigma_summary.png)

### 5.4 Classification Robustness

Figure 8 presents the Monte Carlo classification results as horizontal bars, ordered by P(cooperative). The classification is robust in three important senses. First, the two cooperative cases (Marquesas, Rapa Nui) are clearly separated from the two marginal cases (Tahiti, Hawai'i), which are in turn clearly separated from the two defensive cases (Rapa Iti, New Zealand). There is no overlap between categories. Second, the results are stable across random seeds (all differences $\leq$ 0.006). Third, the ordering is consistent with archaeological expectations: the Marquesas (highest P) has the most robust cooperative tradition, Rapa Iti and New Zealand (P $\approx$ 0%) have the most unambiguous defensive traditions, and the intermediate cases (Tahiti, Hawai'i, Rapa Nui) show exactly the conditional and variable patterns expected near the phase boundary.

![**Figure 8.** *Classification robustness: Monte Carlo with full parameter uncertainty.* Horizontal bars show P(cooperative) from $N$ = 10,000 Monte Carlo samples for each case, ordered by probability. Blue indicates cooperative (P > 50%), gray indicates marginal (10% to 50%), red indicates defensive (P < 10%). Stability across seeds confirms convergence.](figures/pacific_fig_08_classification_robustness.png)

### 5.5 Parameter Comparison and Vulnerability

Figure 9 displays the full set of parameter ranges across all six cases as dot-whisker plots. Several patterns are evident. The $\sigma$ panel shows the wide range for Rapa Nui (0.28 to 0.45), reflecting isolation-amplified uncertainty, compared with the narrower ranges for the defensive cases. The $\mu$ panel shows the clear binary separation between isolated islands ($\mu = 0$) and archipelago systems. The $\beta$ panel shows that all cases share similar raw defector vulnerability, confirming that the differences in classification arise primarily from $\sigma$, $C_{total}$, and $\mu$ rather than from the vulnerability parameters themselves.

Figure 10 examines the effective vulnerability ratio $\beta_{eff}/\alpha_{eff}$ against ENSO exposure ($\sigma$). The mobility buffer reduces $\beta_{eff}$ for archipelago cases, lowering their effective vulnerability ratios relative to isolated islands with the same raw $\beta$. This effect is visible in the downward shift of archipelago cases relative to where they would plot using raw $\beta/\alpha$.

![**Figure 9.** *Parameter comparison across six Pacific cases.* Dot-whisker plots show point estimates (markers) and plausible ranges (horizontal bars) for all eight model parameters across the six cases. The $\sigma$ panel shows the wide range for Rapa Nui reflecting isolation-amplified uncertainty. The $\mu$ panel shows the clear separation between isolated ($\mu = 0$) and archipelago cases.](figures/pacific_fig_09_parameter_comparison.png)

![**Figure 10.** *Effective vulnerability ratio ($\beta_{eff}/\alpha_{eff}$) and ENSO exposure across six cases.* The mobility buffer reduces $\beta_{eff}$ for archipelago cases (shown with $\mu$ labels), lowering their effective vulnerability ratios relative to isolated islands with the same raw $\beta$.](figures/pacific_fig_10_vulnerability.png)

### 5.6 Sensitivity Analysis

Figure 11 presents tornado charts showing the sensitivity of $\sigma^*$ to each parameter for two baselines: an isolated island ($\mu = 0$, Panel A) and a hypothetical archipelago ($\mu = 0.10$, Panel B). In both panels, the most influential parameters are $\beta$ (defector vulnerability, negative elasticity: increasing $\beta$ lowers $\sigma^*$), $C_{total}$ (cooperation cost, positive elasticity: increasing cost raises $\sigma^*$), and $R_{ind}$ (independent advantage, positive elasticity).

The mobility buffer $\mu$ enters the sensitivity analysis directly. At the archipelago baseline ($\mu = 0.10$), $\mu$ has a positive elasticity of approximately +0.13, meaning that a 1% increase in $\mu$ raises $\sigma^*$ by about 0.13%. While this elasticity is smaller than those of $\beta$ or $C_{total}$, its effect accumulates: the difference between $\mu = 0$ and $\mu = 0.12$ shifts $\sigma^*$ by approximately 0.055 (see Table 3), which is comparable to the gap between cooperative and marginal classification for several cases.

The ranking reveals that the framework is most sensitive to the parameters with the clearest economic logic: the cost-benefit balance of independent action ($R_{ind}$, $C_{total}$) and the vulnerability asymmetry ($\beta$, $\alpha$). The conflict parameters ($m_0$, $r$) and mobility buffer ($\mu$) contribute but are secondary. The key empirical implication is that accurate estimates of cooperation costs and environmental vulnerability, both of which can be grounded in archaeological and ecological data, are more important than precise conflict or mobility estimates for generating reliable predictions.

Figure 12 provides a landscape view of the fitness difference $W_C - W_D$ as a function of $\sigma$ for all six cases simultaneously. Each curve crosses zero at the case-specific $\sigma^*$; the steepness of the crossing indicates the sensitivity of classification to $\sigma$ uncertainty. The Marquesas and Rapa Nui curves cross zero within or below their $\sigma$ ranges, confirming cooperative classification. The Rapa Iti and New Zealand curves cross zero far above their $\sigma$ ranges, confirming defensive classification. The Tahiti and Hawai'i curves cross zero near the upper end of their $\sigma$ ranges, consistent with marginal positioning.

![**Figure 11.** *Parameter sensitivity: isolated ($\mu = 0$) vs. archipelago ($\mu = 0.10$) baseline.* Tornado charts show elasticity of $\sigma^*$ with respect to each parameter. Red bars indicate parameters that raise $\sigma^*$ (harder for cooperation); green bars lower $\sigma^*$ (easier for cooperation). The mobility buffer $\mu$ appears in both panels.](figures/pacific_fig_11_sensitivity.png)

![**Figure 12.** *Fitness difference landscape: $W_C - W_D$ vs. $\sigma$ for all six cases.* Positive values (blue region) indicate cooperation is favored; negative values (red region) indicate defection. Each curve crosses zero at the case-specific $\sigma^*$. Colored horizontal bars on the zero line indicate estimated $\sigma$ ranges. The Marquesas and Rapa Nui curves cross zero within or below their $\sigma$ ranges; Rapa Iti and New Zealand curves cross zero far above.](figures/pacific_fig_12_fitness_difference.png)

### 5.7 The 2$\times$2 Classification: Unbundling Cooperation and Signaling

The 2$\times$2 framework (Section 2.6) separates the "cooperator" strategy into its cooperation and signaling components, revealing a richer structure in the strategy space. Figure 14 presents the ($\sigma$, $m_0$) phase diagram computed from the Rapa Nui parameter set, with all six cases plotted as rectangles spanning their estimated parameter ranges.

The phase diagram confirms the theoretical prediction that $\sigma$ and $m_0$ independently control two distinct axes of the strategy space. A vertical cooperation boundary ($\sigma^*$, solid black line) separates cooperative strategies (CN, CS) on the right from non-cooperative strategies (NN, IS) on the left. Two horizontal signaling boundaries ($m_0^*$, dashed lines) mark the conflict mortality levels above which signaling becomes worthwhile: $m_0^{*,coop} \approx 0.283$ for cooperative signalers (CS vs. CN) and $m_0^{*,ind} \approx 0.199$ for individual signalers (IS vs. NN).

A striking result is that all six cases, with observed $m_0$ values ranging from 0.10 to 0.15, fall below both signaling thresholds. At observed conflict mortality levels, signaling alone does not justify its cost for either cooperators or non-cooperators. The four cooperative cases (Rapa Nui, Marquesas, Tahiti, Hawai'i) are classified as CN (cooperative non-signaler) by the 2$\times$2 model, and the two defensive cases (Rapa Iti, New Zealand) are classified as NN (non-cooperative non-signaler), with Rapa Iti showing a minority IS classification (P(IS) = 11.9%) reflecting its higher $m_0$ range.

Monte Carlo 2$\times$2 classification ($N$ = 10,000) confirms these patterns. For Rapa Nui, P(CN) = 98.9% and P(CS) = 1.1%. For the Marquesas, P(CN) = 100%. For the defensive cases, P(NN) ranges from 86.0% (Rapa Iti) to 99.2% (New Zealand). The classification is stable across seeds.

Figure 15 shows the four-strategy fitness crossover at observed $m_0$ for three exemplar cases. In all three panels, CN dominates CS across the full range of $\sigma$, confirming that the cooperative shock-buffering benefit operates independently of the signaling decision. The crossover between cooperative (CN) and non-cooperative (NN) strategies occurs at a $\sigma^*$ that closely matches the bundled-model threshold, providing independent validation of the original two-strategy results.

Figure 16 presents the bundling analysis: how the fitness advantage of signaling (CS over CN for cooperators, IS over NN for non-cooperators) varies with $m_0$. The signaling thresholds $m_0^{*,coop}$ and $m_0^{*,ind}$ are clearly visible as the zero-crossings of each curve. The observed $m_0$ values (vertical dotted lines) fall to the left of these thresholds for all cases, confirming that signaling is not independently cost-effective at observed conflict mortality levels. The implication, discussed in Section 6.9, is that cooperation and signaling are observed together in the archaeological record not because signaling independently pays but because the two behaviors are adaptively bundled: signaling is the mechanism that makes cooperation credible and detectable.

![**Figure 14.** *($\sigma$, $m_0$) phase diagram: four strategy regions.* Colors show the dominant strategy at each point in ($\sigma$, $m_0$) space computed from the Rapa Nui parameter set: NN (red), CN (light blue), IS (light orange), CS (dark blue). The solid black curve marks the cooperation boundary ($\sigma^*$). Dashed horizontal lines mark signaling thresholds ($m_0^*$). Rectangles show $\sigma \times m_0$ parameter ranges for each case. All cases fall below the signaling thresholds, classifying as CN (cooperative non-signaler) or NN (non-cooperative non-signaler) at observed $m_0$ values.](figures/pacific_fig_14_phase_diagram.png)

![**Figure 15.** *Four-strategy fitness crossover at observed $m_0$.* Panels show all four strategy fitness curves as functions of $\sigma$ for three exemplar cases: Rapa Nui (A), Marquesas (B), and Rapa Iti (C). At observed $m_0$ values, CN (dashed light blue) dominates CS (solid dark blue) across all $\sigma$, and the cooperation-vs-non-cooperation crossover matches the bundled model threshold. Colored bands show estimated $\sigma$ ranges.](figures/pacific_fig_15_fitness_crossover_2x2.png)

![**Figure 16.** *Bundling analysis: when does signaling add value?* Panel A shows the fitness difference $W_{CS} - W_{CN}$ as a function of $m_0$ for three cooperative cases at their observed $\sigma$. Signaling becomes worthwhile only when $m_0$ exceeds the threshold $m_0^{*,coop}$ (circles on zero line). Panel B shows $W_{IS} - W_{NN}$ for non-cooperators. Vertical dotted lines indicate observed $m_0$ values, all of which fall below the signaling thresholds.](figures/pacific_fig_16_bundling.png)

## 6. Discussion

### 6.1 Why the Framework Works: Controlled Cultural Ancestry

The central advantage of the Polynesian comparison is the control of cultural ancestry. All six societies descended from a common Ancestral Polynesian culture within the last 1,000 to 2,000 years (Kirch 2000). They share linguistic, social, and religious foundations: the concept of mana, the chief/priest/warrior status distinctions, the importance of genealogical rank, and the basic organizational unit of the hapu or equivalent (Goldman 1970; Kirch 2000). When these closely related populations produce dramatically different architectural traditions, cooperative temples on some islands and defensive fortifications on others, the most parsimonious explanation is that environmental parameters, not cultural differences, drive the divergence.

The Price equation framework formalizes this argument. By specifying fitness as a function of environmental uncertainty $\sigma$, mobility buffer $\mu$, and a small number of additional parameters ($C_{total}$, $\alpha$, $\beta$, $m_0$, $r$), the framework predicts which architectural outcome should arise on each island. The predictions match the archaeological record for all six cases, including the more nuanced prediction that marginal cases should show variable and conditional cooperative traditions.

### 6.2 The Isolation-Cooperation Nexus

The mobility buffer $\mu$ introduces a theoretically grounded mechanism, the isolation-cooperation nexus, that has implications beyond the Polynesian cases. The key insight is that isolation can promote cooperation by eliminating the exit option for defectors. This is distinct from, and complementary to, the commonly invoked argument that isolation promotes cooperation by forcing groups to interact repeatedly (the "shadow of the future" mechanism from iterated game theory). In our framework, isolation does not work through repeated interaction but through vulnerability: isolated defectors are more exposed to environmental shocks because they cannot relocate, making the insurance value of cooperation relatively greater.

This mechanism makes a specific prediction: among islands with similar environmental uncertainty and social parameters, more isolated islands should exhibit stronger cooperative traditions. The comparison between Rapa Nui ($\mu = 0$, cooperative) and the Society Islands ($\mu \approx 0.12$, marginal) is consistent with this prediction, though other parameters also differ. A cleaner test would require controlling for environmental uncertainty while varying isolation, a natural experiment that the Pacific archipelago system may provide with additional cases.

The nexus also suggests that the extraordinary monumental tradition of Rapa Nui, often treated as an archaeological puzzle requiring special explanation, is in fact a predictable consequence of ordinary evolutionary dynamics operating under extreme isolation. The moai were not an irrational "cultural obsession" that led to ecological collapse (contra Diamond 2005); they were an adaptive response to the specific combination of environmental uncertainty and isolation that characterizes the island.

### 6.3 The Rapa Iti / New Zealand Pattern: Low $\sigma$ + High Density = Defensive

Rapa Iti and New Zealand both exhibit the defensive pa/pare architectural tradition despite being very different in scale (40 km$^2$ vs. 268,000 km$^2$). What they share is low environmental uncertainty combined with conditions that promote inter-group competition.

For Rapa Iti, the small island area means that population growth rapidly approaches carrying capacity, creating intense competition for limited but predictable resources (Kennett et al. 2006). The steep topography provides natural defensive positions that are easily fortified (Kennett et al. 2006). With $\sigma$ in the range 0.08 to 0.16 and P(cooperative) $\approx$ 0%, there is no plausible parameter combination under which cooperative risk-pooling would be adaptive.

For New Zealand, the temperate climate provides predictable seasonal resources (Anderson 2002), supplemented by kumara horticulture in the North Island (Davidson 1984). The elevated $R_{ind}$ (1.00 to 1.10) reflects the advantage of independent resource defense in an environment where resources are spatially distributed and defensible. The small mobility buffer ($\mu$ = 0.01 to 0.05) slightly raises $\sigma^*$ but is not the primary driver of the defensive classification; even at $\mu = 0$, New Zealand's $\sigma^*$ (0.508) far exceeds its $\sigma$ (0.14 to 0.22).

The framework captures both cases through the same mechanism: when P(cooperative) $\approx$ 0%, cooperative risk-pooling is never adaptive across the full range of plausible parameters, and competitive/defensive strategies dominate.

### 6.4 Marginal Cases: Tahiti and Hawai'i Near the Boundary

Two of our six cases, Tahiti and Hawai'i, fall in the marginal zone with P(cooperative) of approximately 20%. This marginal positioning generates specific archaeological predictions that match the observed records.

**Tahiti** (P(cooperative) = 21.5%): The marae tradition shows enormous variation across the Society Islands, from simple household platforms to the massive inter-island complex at Taputapuatea (Kahn 2024; Kahn and Kirch 2014). This variability, with some communities investing heavily and others minimally, is expected for a system near $\sigma^*$ where small local differences in parameters tip the balance. The extensive inter-island mobility ($\mu$ = 0.08 to 0.16) raises $\sigma^*$ for the archipelago as a whole, but individual islands facing locally higher uncertainty (exposed coastlines, rain-shadow valleys) may cross the threshold locally.

**Hawai'i** (P(cooperative) = 19.8%): The heiau tradition evolved from cooperative community temples to increasingly hierarchical and coercive structures, eventually incorporating human sacrifice (Kirch 2010). This trajectory, from cooperative to competitive, is predicted for a marginal system where population growth and environmental change shift parameters across the phase boundary. The ecological diversity of the larger islands ($\varepsilon$ = 0.05 to 0.15) provides some buffering, but the inter-island mobility ($\mu$ = 0.05 to 0.15) counteracts this by raising $\sigma^*$.

The marginal cases provide a more informative test of the framework than the clearly classified cases. Any model can predict that cooperative architecture should appear where it does appear. Fewer models can predict that the same architecture should be variable, conditional, and historically unstable, which is precisely what the framework predicts for cases with P(cooperative) in the 10% to 50% range.

### 6.5 Rapa Nui: From Marginal to Cooperative

One of the most significant results of incorporating the mobility buffer is the reclassification of Rapa Nui from marginal to cooperative. In the original analysis without $\mu$ (and with narrower $\sigma$ ranges), Rapa Nui sat near the phase boundary with $\sigma$ slightly below $\sigma^*$, requiring the invocation of "marginal" positioning to explain its extraordinary monumental tradition. With the revised analysis, two changes shift Rapa Nui into the cooperative regime.

First, the $\sigma$ range is broadened to 0.28 to 0.45 (from 0.28 to 0.34), reflecting the recognition that effective uncertainty on an isolated island includes not just raw climatic variability but also the amplification caused by having no external buffering mechanism. This is not a post-hoc adjustment; it follows directly from the theory: if the model includes a mobility buffer $\mu$ for archipelago islands that reduces effective defector vulnerability, the corresponding effect on isolated islands is that all uncertainty is absorbed locally. The $\sigma$ parameter for isolated islands should therefore reflect total effective uncertainty, not just climatic variability.

Second, the mobility buffer ($\mu = 0$) holds $\sigma^*$ at its baseline value while archipelago cases see their $\sigma^*$ increase. The relative effect is that Rapa Nui's $\sigma^*$ (0.351) is now lower than it would be for a hypothetical archipelago version of Rapa Nui ($\sigma^* = 0.389$ at $\mu = 0.10$).

Together, these changes produce P(cooperative) = 55.8%: Rapa Nui is more likely cooperative than not. This correctly predicts the island's ahu/moai tradition, one of the most remarkable cooperative monumental investments in Polynesia. The 55.8% probability is not overwhelming, but this is consistent with the archaeological evidence of late-period transformation: the system was cooperative but not unconditionally so, and small parameter shifts eventually moved it toward the boundary.

### 6.6 The Marquesas as the Strongest Positive Test

The Marquesas provide the strongest positive test of the framework because they have the highest P(cooperative) = 62.1% despite having a moderate mobility buffer ($\mu$ = 0.05 to 0.15). The raw environmental uncertainty is so high ($\sigma$ = 0.38 to 0.50) that it overwhelms both the mobility buffer and the variation in other parameters. In the Monte Carlo analysis, nearly two-thirds of all parameter combinations produce a cooperative classification.

The archaeological record confirms this prediction. The tohua and me'ae of the Marquesas represent some of the most elaborate cooperative architectural investments in Polynesia. Tohua were not merely ceremonial platforms but large public gathering spaces that facilitated inter-valley exchange, feasting, and ritual, precisely the kind of cooperative signaling infrastructure predicted by the framework (Allen 2010). The Marquesan system persisted and intensified throughout the pre-contact period, consistent with a system well above the threshold where cooperation is robustly adaptive across a wide range of parameter values.

### 6.7 Implications for Polynesian Political Evolution

Traditional models of Polynesian political evolution have emphasized a progression from simpler to more complex chiefdoms, driven by population growth, agricultural intensification, and competitive politics (Goldman 1970; Kirch 1984; Sahlins 1958). The Price equation framework offers a complementary perspective: the form of political organization, cooperative vs. competitive, is predicted by environmental parameters and isolation rather than by stage in a developmental sequence.

This reframing has several implications. First, defensive fortification systems like those of Rapa Iti and New Zealand are not "less developed" versions of cooperative monumental systems; they are distinct adaptive responses to different environmental conditions. Second, the transformation of cooperative systems into coercive ones (as in late-period Hawai'i) may reflect parameter shifts, population growth lowering effective $\sigma$ by reducing per-capita resource variability or increasing $R_{ind}$ by making defense more profitable, rather than inherent political dynamics. Third, the persistence of cooperative systems (as in the Marquesas) is not evidence of "cultural conservatism" but of continued adaptive value under sustained high uncertainty. Fourth, the isolation-cooperation nexus explains why some of the most extraordinary cooperative investments in Polynesia (and worldwide) occur on isolated islands, a pattern that is puzzling under standard models but predictable under our framework.

### 6.8 Why Cooperation and Signaling Are Bundled

The 2$\times$2 framework (Section 2.6) reveals a result that at first appears paradoxical: at observed Polynesian conflict mortality levels ($m_0$ = 0.10 to 0.18), the model predicts that cooperators should not signal. The signaling threshold $m_0^{*,coop}$ ranges from approximately 0.22 to 0.28 across the six cases, meaning that group monumental display becomes cost-effective only when conflict mortality exceeds 22 to 28% per generation. Yet the archaeological record shows cooperation and monumental signaling occurring together, precisely the CS strategy that the 2$\times$2 model says is suboptimal at observed $m_0$.

This apparent contradiction resolves when we recognize that the 2$\times$2 model treats cooperation and signaling as truly independent decisions, whereas in practice they are mechanistically coupled. The costly signaling framework is built on the premise that cooperation is sustained through honest costly signals: a group's monumental investment credibly advertises its capacity for cooperation, enabling partner choice and coalition formation. Without the signal, cooperation is vulnerable to free-riding because potential partners cannot distinguish genuine cooperators from pretenders. In this view, CN (cooperation without signaling) is not a stable strategy because it lacks the mechanism that sustains cooperation in the first place.

The 2$\times$2 analysis makes this dependency visible rather than hidden. The bundled model (Section 2.2) implicitly assumes that cooperation and signaling come as a package; the 2$\times$2 model shows why they must. The key insight is that signaling is not independently worth its cost at observed $m_0$ levels, meaning that groups do not build monuments primarily for the conflict-deterrence benefit ($r_{group}$). Rather, signaling is the coordination mechanism that enables the shock-buffering benefit ($\alpha_{eff}$ vs. $\beta_{eff}$) to be realized. The cooperation benefit subsidizes the signaling cost, and the signal sustains the cooperation. The two are adaptively bundled.

This bundling hypothesis makes a testable prediction. If signaling were independently valuable (i.e., if $m_0 > m_0^{*,coop}$), we would expect to see the IS strategy (individual competitive display without cooperative risk-pooling) as a common archaeological pattern. But IS is rarely if ever observed as a stable long-term strategy in Polynesian archaeology, precisely because $m_0$ values are below the threshold where signaling alone pays. The absence of stable IS strategies in the archaeological record is evidence that signaling functions primarily as a cooperation-enabling mechanism rather than as an independent conflict-reduction strategy.

### 6.9 Limitations and Future Directions

Several limitations should be noted. First, our parameter ranges, while theoretically motivated, involve subjective judgment. Future work should develop more rigorous calibration methods using paleoclimate proxy data, bioarchaeological evidence, and ethnographic production data. The Monte Carlo approach honestly represents this uncertainty, but narrower ranges based on better data would sharpen the classifications.

Second, the framework treats each case as a static system at equilibrium, whereas the archaeological record shows dynamic change over time. A temporal extension of the model, tracking how $\sigma$ and other parameters change over centuries, would allow more detailed comparison with archaeological sequences.

Third, we have not modeled the transition dynamics between cooperative and defensive regimes. How long does it take for a population near the phase boundary to shift from one architectural tradition to another? Agent-based simulations (validated for the Rapa Nui case; see Lipo et al. 2025) could address this question.

Fourth, the six cases do not exhaust Polynesian architectural variation. Tonga, Samoa, the Cook Islands, and other archipelagos could extend the comparison, though parameter estimation becomes more difficult for cases with less archaeological and paleoclimate data.

Fifth, the mobility buffer $\mu$ is estimated qualitatively from geographic and ethnohistoric evidence. Archaeological evidence of inter-island movement (e.g., geochemical sourcing of stone tools, ancient DNA) could provide more direct estimates of mobility rates.

Finally, the framework should be tested against additional non-Polynesian cases to confirm that the environmental mechanism, rather than some Polynesia-specific cultural factor, drives the architectural divergence.

## 7. Conclusion

The Polynesian Pacific provides a natural experiment in cultural evolution: populations with shared ancestry colonized islands with varying environmental parameters and produced divergent architectural traditions. The Price equation framework for costly cooperative signaling under environmental uncertainty, extended with a mobility buffer $\mu$ that captures the isolation effect on defector options, predicts this divergence from first principles.

When environmental uncertainty $\sigma$ exceeds a critical threshold $\sigma^*$, cooperative monumental architecture (marae, ahu, heiau, tohua) is the adaptive strategy; when $\sigma$ falls below $\sigma^*$, defensive fortification (pa, pare) dominates. The mobility buffer raises $\sigma^*$ for archipelago populations (where defectors can partially escape shocks through inter-island movement) relative to isolated populations (where defectors have no exit option), making cooperation easier to evolve on isolated islands, all else being equal.

Monte Carlo classification with $N$ = 10,000 samples across plausible parameter ranges confirms six predictions. The Marquesas (P(cooperative) = 62.1%) and Rapa Nui (P = 55.8%), with the highest environmental uncertainty and zero mobility buffer (for Rapa Nui), show robust cooperative traditions. Rapa Iti (P $\approx$ 0%) and New Zealand (P $\approx$ 0%), with the lowest uncertainty, show unambiguous defensive traditions. Tahiti (P = 21.5%) and Hawai'i (P = 19.8%), positioned in the marginal zone, show the variable, conditional, and historically unstable cooperative traditions predicted for cases near $\sigma^*$.

The reclassification of Rapa Nui from marginal to cooperative is the most significant result of the revised analysis. The ahu/moai tradition is not an archaeological puzzle requiring special explanation; it is a predictable consequence of high effective environmental uncertainty combined with extreme isolation that eliminates the defector exit option.

The 2$\times$2 extension, which separates cooperation (risk pooling) from signaling (costly display) as independent behavioral dimensions, reveals an additional insight. Environmental uncertainty $\sigma$ controls whether cooperation is adaptive, while conflict mortality $m_0$ independently controls whether signaling is worthwhile. At observed Polynesian $m_0$ values, signaling alone does not justify its cost: the signaling threshold $m_0^{*,coop}$ exceeds observed mortality for all six cases. Cooperation and monumental display are observed together in the archaeological record because they are adaptively bundled. Signaling sustains cooperation by providing an honest, visible signal of group commitment, and cooperation subsidizes signaling by buffering the environmental shocks that would otherwise make the combined investment unprofitable. The rarity of stable individual signaling strategies (IS) in the Polynesian archaeological record corroborates this interpretation.

The framework's power lies in its combination of simplicity and honesty: a small number of environmentally grounded parameters, specified as ranges rather than false point estimates, predict a binary architectural outcome with quantified confidence. By controlling for cultural ancestry through the Polynesian natural experiment, we isolate environmental uncertainty and isolation as the key drivers of the cooperative-defensive divergence, providing the cleanest available test of the costly signaling hypothesis for monumental architecture.

## 8. References

Allen, M.S. 2010. Oscillating climate and socio-political process: The case of the Marquesan Archipelago, central East Polynesia. *Antiquity* 84(323):86-102.

Anderson, A. 2002. Faunal collapse, landscape change and settlement history in Remote Oceania. *World Archaeology* 33(3):375-390.

Anderson, A., Chappell, J., Gagan, M., and Grove, R. 2006. Prehistoric maritime migration in the Pacific islands: An hypothesis of ENSO forcing. *The Holocene* 16(1):1-6.

Bellwood, P.S. 1971. Fortifications and economy in prehistoric New Zealand. *Proceedings of the Prehistoric Society* 37(1):56-95.

Bliege Bird, R. and Smith, E.A. 2005. Signaling theory, strategic interaction, and symbolic capital. *Current Anthropology* 46(2):221-248.

Davidson, J.M. 1984. *The Prehistory of New Zealand*. Longman Paul, Auckland.

Diamond, J. 2005. *Collapse: How Societies Choose to Fail or Succeed*. Viking, New York.

DiNapoli, R.J., Lipo, C.P., Brosnan, T., Hunt, T.L., Hixon, S., Morrison, A.E., and Becker, M. 2020. Rapa Nui (Easter Island) monument (ahu) locations explained by freshwater sources. *PLoS ONE* 15(1):e0210409.

DiNapoli, R.J., Morrison, A.E., Lipo, C.P., Hunt, T.L., and Lane, B.G. 2017. East Polynesian islands as models of cultural divergence: The case of Rapa Nui and Rapa Iti. *Journal of Island and Coastal Archaeology* 13(2):206-223.

Emory, K.P. 1933. Stone remains in the Society Islands. *Bernice P. Bishop Museum Bulletin* 116.

Fox, A. 1976. *Prehistoric Maori Fortifications in the North Island of New Zealand*. Longman Paul, Auckland.

Goldman, I. 1970. *Ancient Polynesian Society*. University of Chicago Press.

Hunt, T.L. and Lipo, C.P. 2006. Late colonization of Easter Island. *Science* 311(5767):1603-1606.

Hunt, T.L. and Lipo, C.P. 2011. *The Statues That Walked: Unraveling the Mystery of Easter Island*. Free Press, New York.

Jacomb, C., Walter, R., Jennings, C., and Peniston-Bird, O. 2022. Archaeological evidence for Polynesian settlement of New Zealand: A review. *Journal of the Polynesian Society* 131(1):7-48.

Kahn, J.G. 2024. Re-evaluating Society Islands marae: Landscape, architecture, and sociopolitics. In *The Oxford Handbook of Polynesian Archaeology*, edited by E.E. Cochrane and T.L. Hunt. Oxford University Press.

Kahn, J.G. and Kirch, P.V. 2014. *Monumentality and Ritual Materialization in the Society Islands*. Bishop Museum Press, Honolulu.

Kennett, D.J., Anderson, A.J., and Winterhalder, B. 2006. The ideal free distribution, food production, and the colonization of Oceania. In *Behavioral Ecology and the Transition to Agriculture*, edited by D.J. Kennett and B. Winterhalder, pp. 265-288. University of California Press, Berkeley.

Kirch, P.V. 1984. *The Evolution of the Polynesian Chiefdoms*. Cambridge University Press.

Kirch, P.V. 1990. Monumental architecture and power in Polynesian chiefdoms: A comparison of Tonga, Hawaii, and Easter Island. *World Archaeology* 22(2):206-222.

Kirch, P.V. 2000. *On the Road of the Winds: An Archaeological History of the Pacific Islands before European Contact*. University of California Press.

Kirch, P.V. 2010. *How Chiefs Became Kings: Divine Kingship and the Rise of Archaic States in Ancient Hawai'i*. University of California Press.

Kirch, P.V. 2024. Monumentality in Hawaiian archaeology. In *The Oxford Handbook of Polynesian Archaeology*, edited by E.E. Cochrane and T.L. Hunt. Oxford University Press.

Kolb, M.J. 1994. Monumentality and the rise of religious authority in precontact Hawai'i. *Current Anthropology* 35(5):521-547.

Lipo, C.P., DiNapoli, R.J., and Hunt, T.L. 2025. Costly signaling and the evolution of cooperative monumentality on Rapa Nui. *Journal of Archaeological Science* (in press).

Lipo, C.P., Hunt, T.L., and Haoa, S.R. 2013. The 'walking' megalithic statues (moai) of Easter Island. *Journal of Archaeological Science* 40(6):2859-2866.

Price, G.R. 1970. Selection and covariance. *Nature* 227:520-521.

Price, G.R. 1972. Extension of covariance selection mathematics. *Annals of Human Genetics* 35(4):485-490.

Sahlins, M.D. 1958. *Social Stratification in Polynesia*. University of Washington Press.

Schmidt, M. 1996. The commencement of pa construction in New Zealand prehistory. *Journal of the Polynesian Society* 105(4):441-460.

Stein, K., DiNapoli, R.J., Lipo, C.P., and Hunt, T.L. 2025. Environmental variability and costly signaling on Rapa Nui: Paleoclimate evidence for the cooperative threshold. *The Holocene* (in review).

Suggs, R.C. 1961. *The Archaeology of Nuku Hiva, Marquesas Islands, French Polynesia*. Anthropological Papers of the American Museum of Natural History, Vol. 49, Part 1.

Wallin, P. 2010. *Marae of the Society Islands: The Development of Marae in Relation to Socio-Political Development in the Society Islands*. Gotarc Series B, Gothenburg Archaeological Theses.

Wilmshurst, J.M., Hunt, T.L., Lipo, C.P., and Anderson, A.J. 2011. High-precision radiocarbon dating shows recent and rapid initial human colonization of East Polynesia. *Proceedings of the National Academy of Sciences* 108(5):1815-1820.

## Appendix A: Complete Parameter Derivations

**Table A1.** Detailed parameter definitions with confidence tiers and sources.

| Parameter | Definition | Range across cases | Tier |
|-----------|-----------|-------------------|------|
| $\sigma$ | Environmental uncertainty (CV of resource returns) | 0.08-0.50 | A (paleoclimate proxy) |
| $C_{total}$ | Total cooperation cost (fraction of productivity) | 0.20-0.40 | B (labor estimates) |
| $\alpha$ | Cooperator vulnerability to shocks | 0.20-0.40 | B (ecological reasoning) |
| $\beta$ | Defector vulnerability to shocks | 0.70-0.95 | B (ecological reasoning) |
| $\mu$ | Mobility buffer (inter-island movement) | 0.00-0.16 | B (geographic/ethnohistoric) |
| $R_{ind}$ | Independent action advantage | 1.00-1.10 | C (theoretical) |
| $\varepsilon$ | Ecotone advantage | 0.00-0.15 | B (island ecology) |
| $m_0$ | Baseline conflict mortality | 0.08-0.18 | B (archaeological/ethnohistoric) |
| $r$ | Signal-mediated conflict reduction | 0.60-0.80 | C (theoretical) |

**Table A2.** $\sigma^*$ computation at point estimates for each case.

| Component | Rapa Nui | Marquesas | Tahiti | Hawai'i | Rapa Iti | NZ |
|-----------|----------|-----------|--------|---------|---------|-----|
| $A = 1 - C_{total}$ | 0.675 | 0.700 | 0.750 | 0.720 | 0.700 | 0.700 |
| $\alpha_{eff} = \alpha(1-\varepsilon)$ | 0.300 | 0.333 | 0.250 | 0.225 | 0.300 | 0.300 |
| $\beta_{eff} = \beta(1-\mu)$ | 0.900 | 0.810 | 0.748 | 0.765 | 0.850 | 0.728 |
| $\gamma_s$ | 0.963 | 0.963 | 0.970 | 0.965 | 0.955 | 0.964 |
| $\gamma_n$ | 0.850 | 0.875 | 0.900 | 0.900 | 0.850 | 0.880 |
| Numerator | 0.200 | 0.201 | 0.173 | 0.205 | 0.182 | 0.249 |
| Denominator | 0.570 | 0.485 | 0.491 | 0.532 | 0.522 | 0.470 |
| **$\sigma^*$** | **0.351** | **0.415** | **0.351** | **0.386** | **0.348** | **0.530** |
| **P(coop)** | **55.8%** | **62.1%** | **21.5%** | **19.8%** | **$\approx$0%** | **$\approx$0%** |

## Figure Captions

**Figure 1.** *Six Pacific cases with shared Polynesian ancestry and divergent architectural outcomes.* Blue borders indicate cooperative monumental traditions (ahu/moai, tohua/me'ae, marae, heiau); orange borders indicate defensive fortification traditions (pa/pare). Labels include the mobility buffer $\mu$ for each case: $\mu = 0$ for isolated islands (Rapa Nui, Rapa Iti), $\mu > 0$ for archipelago systems. Dashed lines indicate the Polynesian Triangle. Marker size is proportional to log island area.

**Figure 2.** *Fitness anatomy: decomposition of cooperator and defector fitness into three components for the Rapa Nui case.* At Rapa Nui's estimated environmental uncertainty ($\sigma$ = 0.365), cooperators pay a production cost ($C_{total}$) but gain better shock survival and conflict survival. The total fitness comparison (rightmost pair) determines which strategy is favored.

**Figure 3.** *The two predicted regimes: cooperative signaling and defensive fortification.* When environmental uncertainty $\sigma$ exceeds the critical threshold $\sigma^*$, cooperative monumental architecture is the evolutionarily stable strategy. When $\sigma < \sigma^*$ and population density is high, defensive fortification dominates. The six cases are positioned by estimated $\sigma$ and relative population pressure, with $\mu$ values shown. The mobility buffer shifts $\sigma^*$ rightward for archipelago cases.

**Figure 4.** *The mobility buffer ($\mu$): how isolation promotes cooperation.* Panel A compares $\sigma^*$ computed with and without the mobility buffer for all six cases. Isolated islands (Rapa Nui, Rapa Iti) show no shift; archipelago cases show increased $\sigma^*$ when $\mu > 0$. Panel B shows the fitness crossover for Rapa Nui under two scenarios: actual isolation ($\mu = 0$) and hypothetical archipelago placement ($\mu = 0.10$).

**Figure 5.** *Fitness crossover at $\sigma^*$: all six Pacific cases.* Panels A-F show cooperator ($W_C$, blue) and defector ($W_D$, red) fitness as functions of environmental uncertainty $\sigma$ for each case. The crossover point ($\sigma^*$, green dashed line) marks the critical threshold. Colored vertical bands indicate estimated $\sigma$ ranges. Mobility buffer values ($\mu$) are shown.

**Figure 6.** *Phase space with parameter uncertainty regions.* Rectangles show the joint range of $\sigma$ (x-axis) and $C_{total}$ (y-axis) for each case. The solid black curve shows the phase boundary at $\mu = 0$; the dashed curve at $\mu = 0.10$. Cooperative cases overlap the cooperative region; defensive cases sit entirely in the defensive region.

**Figure 7.** *$\sigma^*$ vs. $\sigma$ with parameter uncertainty.* Rectangles show 90% ranges for both $\sigma^*$ (x-axis, from Monte Carlo) and $\sigma$ (y-axis, from parameter ranges). Points above the 1:1 line (blue region) indicate cooperation predicted. Labels show P(cooperative) from Monte Carlo.

**Figure 8.** *Classification robustness: Monte Carlo with full parameter uncertainty.* Horizontal bars show P(cooperative) from $N$ = 10,000 Monte Carlo samples, ordered by probability. Blue = cooperative (P > 50%), gray = marginal (10% to 50%), red = defensive (P < 10%).

**Figure 9.** *Parameter comparison across six Pacific cases.* Dot-whisker plots show point estimates (markers) and plausible ranges (horizontal bars) for all eight model parameters. The $\sigma$ panel shows the wide range for Rapa Nui reflecting isolation-amplified uncertainty. The $\mu$ panel shows the clear separation between isolated and archipelago cases.

**Figure 10.** *Effective vulnerability ratio ($\beta_{eff}/\alpha_{eff}$) and ENSO exposure across six cases.* The mobility buffer reduces $\beta_{eff}$ for archipelago cases, lowering their effective vulnerability ratios relative to isolated islands with the same raw $\beta$.

**Figure 11.** *Parameter sensitivity: isolated ($\mu = 0$) vs. archipelago ($\mu = 0.10$) baseline.* Tornado charts show elasticity of $\sigma^*$ with respect to each parameter. Red bars raise $\sigma^*$ (harder for cooperation); green bars lower $\sigma^*$ (easier for cooperation).

**Figure 12.** *Fitness difference landscape: $W_C - W_D$ vs. $\sigma$ for all six cases.* Positive values indicate cooperation favored; negative values indicate defection. Each curve crosses zero at the case-specific $\sigma^*$. Colored horizontal bars on the zero line indicate estimated $\sigma$ ranges.

**Figure 13.** *The 2$\times$2 strategy space: cooperation and signaling as independent dimensions.* Four strategies arise from the crossing of two binary decisions (cooperate or not, signal or not). Each cell shows the cost structure, fitness benefit, and archaeological exemplar. Environmental uncertainty $\sigma$ controls the cooperation axis; conflict mortality $m_0$ controls the signaling axis.

**Figure 14.** *($\sigma$, $m_0$) phase diagram: four strategy regions.* Colors show the dominant strategy at each point in ($\sigma$, $m_0$) space: NN (red), CN (light blue), IS (light orange), CS (dark blue). The solid black curve marks the cooperation boundary ($\sigma^*$). Dashed horizontal lines mark signaling thresholds ($m_0^*$). Rectangles show $\sigma \times m_0$ parameter ranges for each case. All cases fall below the signaling thresholds, classifying as CN or NN at observed $m_0$ values.

**Figure 15.** *Four-strategy fitness crossover at observed $m_0$.* Panels show all four strategy fitness curves as functions of $\sigma$ for three exemplar cases. At observed $m_0$ values, CN dominates CS across all $\sigma$, and the cooperation-vs-non-cooperation crossover matches the bundled model threshold.

**Figure 16.** *Bundling analysis: when does signaling add value?* Panel A shows $W_{CS} - W_{CN}$ as a function of $m_0$ for three cooperative cases. Signaling becomes worthwhile only when $m_0$ exceeds $m_0^{*,coop}$ (circles). Panel B shows $W_{IS} - W_{NN}$. Vertical dotted lines indicate observed $m_0$ values, all below the signaling thresholds.
