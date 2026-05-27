# Modeling Seasonal Aggregation at Lamoka Lake: A Mathematical and Methodological Guide for Dissertation Research

**A companion document to:** *Modeling Seasonal Aggregation at a Late Archaic Ecotone: Predictions for Lamoka Lake, New York*

---

# PART I: THE PUZZLE AND THE FRAMEWORK

---

## 1. Introduction: The Lamoka Lake Puzzle

### 1.1 Why This Site Matters

Lamoka Lake, a 1.2-hectare site at the southern end of Lamoka Lake in Schuyler County, New York, presents one of the most puzzling cases of hunter-gatherer investment in eastern North America. When William Ritchie excavated the site in the 1920s and 1930s, he found over 380 storage pits, numerous hearths and smoking platforms, fish weirs in the lake outlet channel, and approximately 80 burials in midden deposits reaching 150 cm in depth (Ritchie 1932, 1969). Recent AMS redating suggests the most intensive occupation occurred within a remarkably compressed window of roughly 60 years, approximately 2962 to 2902 BCE, though the broader occupation spans approximately 3500 to 1300 BCE.

The puzzle is not that hunter-gatherers lived near a lake. That is entirely expected. The puzzle is *scale*. A storage pit density of 317 per hectare far exceeds what any single band would need. Fish weirs require cooperative labor. Smoking platforms indicate organized food preservation beyond household production. The aggregate estimated storage volume of approximately 50,000 liters could have provisioned several hundred people through a winter season. Everything about the site screams *communal investment*, yet these are mobile foragers who, by all conventional expectations, should have been traveling light and moving on.

### 1.2 Why Model Rather Than Just Describe?

You might reasonably ask: why build a mathematical model when we could simply describe what we see at Lamoka Lake and propose an interpretation? The answer is that description tells us *what* but not *when* or *why*. A descriptive interpretation, for example "Lamoka Lake was a seasonal aggregation site," leaves critical questions unanswered:

- Under what environmental conditions should we expect aggregation to emerge?
- How much environmental variability is "enough" to make aggregation worth the cost?
- What would cause the system to collapse?
- Should we expect similar sites at other locations?
- What specific evidence would *falsify* the interpretation?

A formal model answers all of these questions. It gives us a number, a critical threshold of environmental variability ($\sigma^* \approx 0.306$), that makes a precise, testable prediction: below that level of variability, independent foraging should dominate; above it, aggregation should emerge. It tells us what should happen if the environment stabilizes (the system should collapse, not strengthen). It tells us where to look for similar sites (at ecotone intersections, not random locations). And it tells us exactly what evidence would prove the model wrong.

### 1.3 What a Dissertation Can Contribute

The model published in the JAS manuscript is a *proposal*. It generates seven specific, falsifiable predictions, but those predictions remain untested. A dissertation project can take the model from proposal to evaluated hypothesis by:

1. Compiling and generating the data needed to test each prediction
2. Running the tests and reporting the results honestly, including failures
3. Evaluating alternative hypotheses with the same data
4. Refining the model parameters based on empirical findings

This guide walks you through the mathematics behind the model, explains how each variable maps to measurable archaeological and environmental data, and lays out a concrete research design for testing the model's predictions.

### 1.4 Roadmap

This document is organized in four parts:

- **Part I (Sections 1-3)**: The puzzle and the conceptual framework, in plain language
- **Part II (Sections 4-10)**: Building the mathematical model step by step, with every symbol explained
- **Part III (Sections 11-12)**: The complete model and what simulations add
- **Part IV (Sections 13-17)**: A concrete research design for testing the model

Each section in Part II follows the same template: (1) what we are adding and why, in plain language; (2) the math, with intuitive explanation of every symbol; (3) how to measure or estimate this in the archaeological and environmental record; and (4) what the parameter values are for Lamoka Lake and why.

---

## 2. The Core Idea in Plain Language

### 2.1 The Intuition: Insurance Under Uncertainty

Imagine you are a hunter-gatherer band of 20 people living in the Finger Lakes region around 3000 BCE. Every fall, you face a decision: do you stay in your home range and harvest whatever the local area provides? Or do you travel to a lakeside site where other bands are gathering, invest time and labor in shared infrastructure (storage pits, fish weirs, smoking platforms), and participate in communal food processing?

Staying home is simpler. You avoid travel costs, you do not have to share, and you can focus entirely on your own foraging. But you are also alone. If your local area has a bad year, poor nut harvest, fewer deer, low fish runs, you bear that loss entirely by yourself.

Going to the aggregation site costs you something: the energy to travel, the labor to help build and maintain shared facilities, the foraging opportunities you miss while at the site. But you gain three things in return:

1. **Access to multiple ecological zones.** The aggregation site sits at the intersection of lake, forest, wetland, and upland environments. If the nut crop fails, maybe the fish runs are good. If terrestrial game is scarce, maybe the wetlands are productive. By being at the intersection, you are hedging your bets across multiple resource types.

2. **Communal processing returns.** More hands make lighter work. Fish weirs are more productive per person when more people operate them. Nut processing is faster and more efficient with division of labor. You get more food per unit of effort than you would working alone.

3. **Social insurance.** By aggregating with other bands, you build reciprocal relationships. If your band has a tough winter, you can call on bands you helped last year. These relationships are a safety net.

### 2.2 The Insurance Analogy

Think of aggregation as buying insurance. Insurance costs money (the premium). In good years, you "wasted" that premium, you would have been fine without it. But in bad years, insurance pays off, possibly saving you from ruin.

The key insight is that whether insurance is worth buying depends on *how variable* your situation is:

- If your house will definitely not burn down, fire insurance is a waste of money.
- If your house has a 50% chance of burning down each year, fire insurance is essential.
- Somewhere in between, there is a tipping point where the expected payoff of insurance exactly equals its cost.

That tipping point is what we call $\sigma^*$, the **critical threshold of environmental uncertainty**. Below $\sigma^*$, the environment is stable enough that the "insurance premium" of aggregation (travel costs, shared labor, lost foraging time) is not worth paying. Above $\sigma^*$, the environment is variable enough that the insurance value (ecotone buffering, communal returns, social networks) more than compensates for the costs.

### 2.3 Two Strategies: Aggregate vs. Go It Alone

The model formalizes this intuition as a choice between two strategies:

**Strategy 1: Aggregate.** Travel to the lakeside site in fall. Invest in shared infrastructure. Participate in communal processing. Build reciprocal relationships. Pay costs, but gain insurance and cooperation benefits.

**Strategy 2: Independent.** Stay in your home range year-round. Forage alone. Keep everything you produce. Pay no cooperation costs, but bear all environmental risk yourself.

Neither strategy is always better. Each wins under different conditions. The model's job is to identify the exact conditions under which each strategy dominates.

![Figure 1. Two strategies under uncertainty. Panel A shows a stable environment where both strategies perform similarly. Panel B shows a variable environment where aggregators (blue) have smoother returns while independents (red) suffer frequent shortfall years (triangles).](figures/fig_01_two_strategies.png)

### 2.4 The Threshold Concept

Here is the central result of the model, stated in plain language:

> There exists a specific level of environmental variability, which we call $\sigma^*$, below which independent foraging is the better strategy and above which aggregation is the better strategy.

For Lamoka Lake, $\sigma^* \approx 0.306$. This means that if the Finger Lakes environment during the Late Archaic had a coefficient of variation in annual resource returns greater than about 0.31, aggregation should have been the dominant strategy.

What does a CV of 0.31 feel like in practical terms? It means that if the average band's annual food intake is 1,000 units, the standard deviation is 310 units. In a typical year, returns might range from about 690 to 1,310 (within one standard deviation of the mean). Roughly one year in six, returns would fall below 690, which for a band of 20 people could mean serious hunger. One year in twenty, returns would fall below about 380, which could mean starvation. That is the level of unpredictability at which the insurance value of aggregation starts to outweigh its costs.

The estimated environmental variability for the Finger Lakes during this period is $\sigma \approx 0.35$-$0.45$, well above the threshold. The model predicts aggregation, and that is what we observe.

### 2.5 Why Lamoka Lake?

The model does not just predict *that* aggregation should occur; it predicts *where*. Not every location makes a good aggregation site. What makes Lamoka Lake special is its position at the intersection of five ecological zones:

1. **Lacustrine** (the lake itself): fish, waterfowl, mussels
2. **Upland forest** (ridges between lakes): deer, turkey, small mammals
3. **Mast forest** (nut-bearing trees): hickory, walnut, acorn
4. **Wetland** (stream corridors and margins): fish, turtles, aquatic plants
5. **Montane** (higher elevations): patchy, variable resources

When one zone has a bad year, others often do well, especially zones whose productivity responds to different environmental drivers. Lake productivity and upland forest productivity, for example, tend to be negatively correlated: wet years favor fish but can hinder terrestrial game, and vice versa. This negative covariance creates a natural buffering effect, what we call the **ecotone advantage**.

A band that aggregates at this five-zone intersection experiences lower effective uncertainty than a band stuck in a single zone. That is why aggregation specifically at ecotone locations makes sense, and why the model predicts that aggregation sites should cluster at ecological intersections.

---

## 3. Why Start from the Price Equation?

### 3.1 What the Price Equation Is

The Price equation, developed by George Price in 1970, is the most general mathematical statement about how any trait changes frequency in a population over time. In plain English, it says:

> A trait increases in a population when individuals who carry that trait have higher fitness (more offspring, better survival) than individuals who do not.

That sounds obvious, but the equation captures it in a way that is completely general. It does not assume anything about how traits are inherited (genes, culture, learning), what kind of organisms we are talking about, or how the population is structured. It just says:

$$\Delta\bar{p} = \frac{1}{\bar{w}} \text{Cov}(w_i, p_i)$$

Let us unpack every piece:

- $\Delta\bar{p}$: the change in the average frequency of the trait in the population. If this is positive, the trait is spreading; if negative, it is declining.
- $\bar{w}$: the average fitness across all individuals in the population. This is a scaling factor.
- $\text{Cov}(w_i, p_i)$: the covariance between individual fitness ($w_i$) and individual trait value ($p_i$). In plain language: if individuals with the trait tend to have higher fitness, this covariance is positive, and the trait spreads.

For our purposes, the "trait" is the strategy of aggregating (cooperating) versus foraging independently, and "fitness" is a composite measure of survival and reproductive success.

### 3.2 The Multilevel Version: Groups Within Groups

Price (1972) showed that when individuals are organized into groups, the equation can be split into two parts:

$$\Delta\bar{p} = \underbrace{\frac{1}{\bar{w}} \text{Cov}(w_g, p_g)}_{\text{between-group selection}} + \underbrace{\frac{1}{\bar{w}} E[w_g \cdot \Delta p_g]}_{\text{within-group selection}}$$

The first term captures **between-group selection**: groups with more cooperators have higher average fitness, so the cooperative trait spreads through differential group success.

The second term captures **within-group selection**: within any given group, free-riders (who enjoy cooperation benefits without paying costs) do better than cooperators, so the cooperative trait declines within each group.

This decomposition reveals the fundamental tension in the evolution of cooperation: free-riders prosper within groups, but cooperative groups outperform non-cooperative ones. Cooperation evolves when between-group selection is strong enough to overwhelm within-group selection.

### 3.3 How This Maps to Our Problem

In the Lamoka Lake context:

- **Groups** are bands, small units of 15-30 people that make collective decisions.
- **Cooperators** are bands that aggregate, investing in shared infrastructure and communal processing.
- **Defectors** (free-riders) are bands that forage independently, avoiding cooperation costs.
- **Between-group selection** acts because cooperative groups (aggregators) survive environmental shocks better than non-cooperative groups (independents).
- **Within-group selection** acts because, at any given aggregation event, a band that showed up but contributed nothing to shared infrastructure would do even better than one that contributed fully.

The key question is: when does between-group selection win? The answer, as we will derive formally in Part II, is: when environmental uncertainty ($\sigma$) is high enough that the survival advantage of cooperation overwhelms the free-rider advantage within groups.

### 3.4 Why Not Just Use Game Theory?

You might wonder why we start from the Price equation rather than, say, the prisoner's dilemma or some other game-theoretic framework. Three reasons:

1. **Generality.** The Price equation makes no assumptions about how strategies are transmitted (genetic, cultural, learned). For archaeological populations where we cannot observe transmission directly, this generality is essential.

2. **Multilevel structure.** The Price equation's partition into between-group and within-group selection directly captures the tension at the heart of our problem. Game-theoretic models can capture this too, but it has to be built in explicitly rather than falling out naturally.

3. **Fitness decomposition.** The Price equation lets us write fitness as a product of separate components, survival under environmental stress, cooperation returns, conflict avoidance, each of which can depend on different parameters. This modular structure maps directly onto the ecological mechanisms we want to model.

The rest of Part II takes these insights and progressively adds the ecological and social mechanisms specific to Lamoka Lake, building up the complete model step by step.

### 3.5 An Important Clarification: From Price to Fitness Comparison

Here is something that may seem surprising: the Lamoka Lake model itself does not actually use the full Price equation machinery. Instead, it uses a simpler **individual-level fitness comparison** between two strategies (aggregate vs. independent). No group selection or multilevel selection calculation is required.

So why did we just spend several pages on the Price equation? Because it tells us *why* the simpler fitness comparison works. The Price equation's multilevel decomposition reveals that cooperation can be favored when between-group selection (cooperative groups outsurvive non-cooperative ones) outweighs within-group selection (free-riders outcompete cooperators within groups). For the Lamoka Lake case, environmental uncertainty creates exactly these conditions: the survival advantage of cooperation under high $\sigma$ acts as the "between-group" force, while the cost of cooperation acts as the "within-group" force. The Price equation tells us that a threshold must exist; the fitness comparison approach calculates where it is.

Think of it this way: the Price equation is the *theoretical justification* for why a threshold-based fitness comparison is the right tool. The fitness comparison is the *practical model* we use to calculate $\sigma^*$. You need to understand the theoretical justification to know why the model works, but you need the practical model to generate testable predictions.

In what follows, we build the fitness comparison model step by step. Each section adds a mechanism (environmental uncertainty, vulnerability asymmetry, costs, ecotone buffering, cooperation returns, reciprocal obligations), and we track how each mechanism shifts the threshold $\sigma^*$. The Price equation stays in the background as the theoretical warrant for the whole approach.

---

# PART II: BUILDING THE MODEL STEP BY STEP

---

**A note on "fitness" before we begin.** Throughout Part II, we talk about the "fitness" of each strategy. For our purposes, fitness is simply a number that captures how well a strategy performs, combining survival probability, reproductive success, and resource acquisition into a single score. A strategy with fitness 0.80 does better than one with fitness 0.60. We are not measuring fitness directly in the archaeological record; instead, we are comparing fitness *functions* (equations) for the two strategies and finding the conditions under which one exceeds the other. Think of fitness as a scorecard: we want to know when the aggregation scorecard beats the independence scorecard.

---

## 4. Environmental Uncertainty ($\sigma$)

### 4.1 What We Are Adding and Why

The standard fitness comparison treats fitness as a fixed property of individuals: cooperators always have fitness $w_C$, defectors always have fitness $w_D$. But the fitness consequences of cooperation depend on context. In a stable environment where resources are predictable, cooperation imposes costs with minimal benefit. Why share when there is enough for everyone? In a variable environment where resources fluctuate unpredictably, cooperation provides insurance, information sharing, and risk pooling that can be the difference between surviving and not.

To capture this context-dependence, we need to make fitness a function of how variable the environment is. That is what $\sigma$ does.

### 4.2 The Math

We define $\sigma$ as the **coefficient of variation** in annual resource returns:

$$\sigma = \frac{\text{Standard deviation of annual resource returns}}{\text{Mean annual resource returns}}$$

$\sigma$ ranges from 0 to 1. At $\sigma = 0$, resources are perfectly predictable, the same every year. At $\sigma = 1$, the standard deviation equals the mean, meaning resources fluctuate so wildly that some years produce nothing. In practice, $\sigma > 0.80$ represents environments too variable for sustained human occupation.

What does this look like concretely? Imagine a region where the average annual nut harvest is 1,000 kg. If the standard deviation is 350 kg (some years you get 650 kg, other years 1,350 kg), then $\sigma = 0.35$. That is the lower end of what we estimate for the Finger Lakes during the Late Archaic.

$\sigma$ integrates three components of environmental risk:

$$\sigma \propto \frac{\text{magnitude} \times \text{duration}}{\text{return period}}$$

- **Magnitude**: how severe is a shortfall when it happens? (0 to 1 scale, where 1 means complete failure)
- **Duration**: how many years does a shortfall last?
- **Return period**: on average, how many years between shortfall events?

An environment where shortfalls are severe (magnitude 0.6), prolonged (duration 3 years), and frequent (return period 5 years) has much higher $\sigma$ than one where shortfalls are mild (magnitude 0.2), brief (duration 1 year), and rare (return period 20 years).

![Figure 2. What sigma feels like. Three resource distributions centered at mean = 1.0 with different levels of variability. The shaded regions below the shortfall threshold (0.6) show how increasing sigma dramatically increases the probability of a bad year.](figures/fig_02_sigma_distributions.png)

### 4.3 How to Estimate $\sigma$ from the Record

This is where things get practical. You cannot directly measure $\sigma$ for the Late Archaic Finger Lakes, but you can estimate it from multiple proxy sources:

**Pollen cores from Finger Lakes sediments.** Pollen data from lake sediment cores record changes in vegetation composition over time. High variability in pollen percentages (especially for mast-producing trees like *Carya* and *Quercus*) indicates variable growing conditions. Look for existing cores from Lamoka Lake, Waneta Lake, Seneca Lake, and other nearby water bodies.

**Lake sediment cores (varved sediments).** Some Finger Lakes have annually laminated (varved) sediments. Layer thickness variations reflect changes in sediment input, which correlate with precipitation variability. Higher variance in layer thickness implies higher $\sigma$.

**Speleothem (cave formation) records.** Oxygen isotope ratios ($\delta^{18}$O) in speleothem calcite record precipitation and temperature variability. Regional caves in Pennsylvania and West Virginia provide records extending into the Late Archaic. The variance in $\delta^{18}$O values during the period of interest provides a precipitation variability proxy.

**Tree-ring records (limited for this period).** Where preserved wood of sufficient age exists, tree-ring width variability directly measures growing-season conditions. For the Late Archaic, preserved wood is rare, but any available records from the broader Northeast would be informative.

**Modern ecological data on mast production variability.** Long-term monitoring data on nut production in modern temperate forests provides an analog for past variability. Hickory and oak mast crops are notoriously variable: Koenig and Knops (2000) documented coefficients of variation of 0.35-0.50 for acorn production in eastern deciduous forests, with multi-year cycles of boom and bust driven by the complex interaction of weather, pollination success, and insect herbivory. Silvertown (1980) showed that mast-fruiting species exhibit substantially higher inter-annual variability than species with more regular reproduction. These data give us a lower bound on the resource variability component.

**Table 4.1. Sources for estimating $\sigma$ in the Finger Lakes Late Archaic.**

| Proxy source | What it measures | Temporal resolution | Key datasets to seek | Limitation |
|--------------|-----------------|---------------------|---------------------|------------|
| Pollen cores | Vegetation variability | Decades to centuries | NY State Museum collections; published Finger Lakes pollen diagrams | Low temporal resolution |
| Lake varves | Hydrological variability | Annual (if varved) | Cornell Geological Sciences; USGS sediment data | Not all lakes are varved |
| Speleothems | Precipitation variability | Sub-annual to decadal | Published PA/WV cave records | Distant from Finger Lakes |
| Tree rings | Growing season variability | Annual | ITRDB; Mohonk Preserve long chronology | Rare for Late Archaic period |
| Modern mast data | Nut crop variability | Annual | USDA Forest Service mast surveys | Modern analog assumption |

### 4.4 What Lamoka Lake's $\sigma$ Is and Why

We estimate $\sigma \approx 0.35$-$0.45$ for the Finger Lakes during the Late Archaic. This reflects:

- The continental climate of interior New York, which produces greater interannual variation than coastal or oceanic environments
- The high inherent variability of mast crops (CV of 0.35-0.50 in modern data), which were a critical fall resource
- Lake-effect moderation from the Finger Lakes themselves, which buffers temperature extremes and reduces $\sigma$ somewhat
- Late Holocene paleoclimate conditions, which were generally stable but with notable episodes of increased variability

The estimated range $\sigma \approx 0.35$-$0.45$ places the Finger Lakes well above the model's predicted threshold of $\sigma^* \approx 0.306$, which is consistent with the observation that aggregation did occur at Lamoka Lake.

**Table 4.2. Environmental uncertainty ranges across four case studies.**

| Case study | Region | $\sigma$ estimate | Calibration basis |
|-----------|--------|-------------------|-------------------|
| Rapa Nui | SE Pacific | ~0.31 | ENSO-driven drought frequency |
| Chaco Canyon | SW North America | ~0.17 | Tree-ring records |
| Poverty Point | SE North America | 0.45-0.55 | Gulf Coast paleoclimate |
| **Lamoka Lake** | **NE North America** | **0.35-0.45** | **Lake sediments, mast variability** |

---

## 5. Who Gets Hurt More? Vulnerability Parameters ($\alpha$ and $\beta$)

### 5.1 What We Are Adding and Why

Making fitness depend on environmental variability ($\sigma$) is necessary but not sufficient. If both aggregators and independents were equally hurt by bad years, there would be no reason to prefer one strategy over the other regardless of $\sigma$. The crucial insight is that *different strategies experience environmental uncertainty differently*.

Aggregators pool risk. They access multiple ecological zones. They share information about resource conditions. They have stored surplus to fall back on. When a bad year hits, they are buffered.

Independents bear the full variance of their local environment. A solitary band dependent on whatever their home range provides is exposed to every fluctuation, good and bad.

This difference in exposure is captured by two parameters: $\alpha$ (how much a bad year hurts aggregators) and $\beta$ (how much a bad year hurts independents).

### 5.2 The Math

The survival component of fitness for each strategy is:

$$S_{\text{aggregator}}(\sigma) = 1 - \alpha \cdot \sigma_{\text{eff}}$$

$$S_{\text{independent}}(\sigma) = 1 - \beta \cdot \sigma$$

Let us unpack each piece:

- **$S$**: Survival probability. At $S = 1$, everyone survives. At $S = 0$, no one does.
- **$\alpha$**: Aggregator vulnerability. How sensitive are cooperators to each unit of environmental uncertainty? Range: 0.10-0.50. Lower values mean better buffering.
- **$\beta$**: Independent vulnerability. How sensitive are independents to each unit of environmental uncertainty? Range: 0.50-0.95. Higher values mean more exposure.
- **$\sigma_{\text{eff}}$**: Effective uncertainty at the aggregation site (we will define this precisely in Section 8; for now, think of it as $\sigma$ reduced by the ecotone advantage).

![Figure 3. Vulnerability: why aggregators weather bad years better. Aggregator survival (blue) declines more slowly with increasing sigma than independent survival (red), because ecotone buffering reduces effective exposure. At sigma = 0.45, aggregators retain 89% of baseline survival while independents retain only 69%.](figures/fig_03_vulnerability.png)

The critical constraint is $\alpha < \beta$. This says that aggregators are less vulnerable than independents to environmental shocks. This is the mechanism by which aggregation provides a fitness advantage. Without this asymmetry ($\alpha = \beta$), there would be no survival benefit to aggregation, and the strategy would never be selected because its costs would never be offset.

The ratio $\beta / \alpha$ captures the **strength of the buffering effect**. At $\beta / \alpha = 2$, aggregation halves your vulnerability. At $\beta / \alpha = 3$, it cuts vulnerability by two-thirds. The higher the ratio, the stronger the advantage of cooperation.

### 5.3 Why $\alpha < \beta$: Four Concrete Mechanisms

The asymmetry $\alpha < \beta$ is not an arbitrary assumption. It reflects specific, documentable mechanisms:

**Risk pooling.** If 12 bands each forage in different patches and pool some of their production, the unpredictability of any individual band's food supply drops substantially. Here is the intuition: if one band has a bad year, the other 11 probably did not all have bad years too (assuming their foraging areas are somewhat independent). By sharing, the risk is spread across the group. Statistically, when $N$ bands pool independently varying resources, the variance of the average per-band consumption drops by a factor of $1/N$. With 12 bands, the pooled average is only 1/12th as variable as any individual band's returns. In practice, bands do not pool everything, but even partial sharing (contributing 20% to a communal store) meaningfully reduces the chance that any one band faces catastrophic shortfall (Winterhalder 1986).

**Information sharing.** Aggregating bands exchange knowledge about resource conditions: where the fish are running, which groves have good mast this year, where game trails are active. This information reduces the effective uncertainty each band faces because it allows more efficient patch choice.

**Ecotone access.** As discussed in Section 2.5, aggregation at an ecotone location provides access to multiple resource zones with different variability profiles. This is formalized as the ecotone advantage $\varepsilon$ in Section 8, but the effect here is that it lowers the uncertainty aggregators actually experience.

**Stored surplus.** Aggregating bands accumulate processed food (smoked fish, dried nuts) that provides a buffer against winter shortfalls. This stored surplus directly reduces the mortality risk from bad years.

### 5.4 How to Estimate $\alpha$ and $\beta$

**Ethnographic analogs.** Studies of modern and historically documented foraging societies provide data on mortality rates during resource shortfalls. Societies with extensive sharing networks and diversified subsistence bases show lower shortfall mortality than those dependent on narrow resource bases. Wiessner (2002) documents how !Kung (Ju/'hoansi) exchange networks ($hxaro$) buffer individual shortfalls, reducing mortality by an estimated 30-50% compared to unnetworked individuals.

**Faunal assemblage diversity as a proxy for $\alpha$.** A highly diverse faunal assemblage (many species, multiple ecological zones represented) at an aggregation site indicates broad dietary buffering, supporting lower $\alpha$ values. If Lamoka Lake's faunal assemblage shows high diversity (deer, fish, squirrel, waterfowl, turtle, multiple plant species), this is consistent with effective risk buffering.

**Storage capacity as a proxy for $\alpha$.** The estimated 50,000 liters of storage capacity at Lamoka Lake represents substantial buffering potential. If this volume could provision 200-300 people for 2-3 months, the stored surplus reduces winter shortfall vulnerability significantly, supporting $\alpha = 0.35$.

**Modern ecological data on zone-specific failure rates for $\beta$.** How often does a single ecological zone fail? Modern monitoring data on fish populations, deer densities, and mast crops show that individual zones can fail severely (>50% below average) in any given year. A band dependent on a single zone would be fully exposed to these failures, supporting $\beta = 0.70$.

### 5.5 Lamoka Lake Values

For Lamoka Lake, we use $\alpha = 0.35$ and $\beta = 0.70$, giving a ratio of $\beta / \alpha = 2.00$.

**Why $\alpha = 0.35$?** Aggregators at Lamoka Lake benefit from five-zone ecotone access, stored surplus (50,000 liters capacity), communal processing that generates additional food, and reciprocal sharing networks. These multiple buffering mechanisms justify a vulnerability about one-third as large as the maximum possible.

**Why $\beta = 0.70$?** Independents in the Finger Lakes are not maximally vulnerable (northeastern winters are harsh but not as extreme as, say, subarctic conditions), and even lone bands have some resilience through mobility and local knowledge. But single-zone dependence means that a bad year for your primary resource hits hard. A value of 0.70 reflects substantial but not catastrophic exposure.

**Table 5.1. Vulnerability parameters across four case studies.**

| Parameter | Rapa Nui | Chaco Canyon | Poverty Point | **Lamoka Lake** |
|-----------|----------|--------------|---------------|-----------------|
| $\alpha$ | 0.30 | 0.30 | 0.40 | **0.35** |
| $\beta$ | 0.90 | 0.85 | 0.75 | **0.70** |
| $\beta / \alpha$ | 3.00 | 2.83 | 1.88 | **2.00** |

Note the pattern: island and arid environments (Rapa Nui, Chaco) show higher $\beta$ (independents are more exposed, fewer fallback options) and higher $\beta / \alpha$ ratios. Continental settings with more fallback options (Poverty Point, Lamoka Lake) show lower $\beta$ and moderate ratios.

---

## 6. The Cost of Cooperating ($C_{\text{total}}$)

### 6.1 What We Are Adding and Why

If cooperation were free, everyone would do it, and the "signal" would carry no useful information. The defining feature of the model is that aggregation imposes real costs on participating bands, costs that are only justified when the insurance benefits are large enough. We need to specify what those costs are, how large they are, and how to estimate them from the archaeological record.

### 6.2 The Math

The total cost of aggregation is decomposed into three components:

$$C_{\text{total}} = C_{\text{travel}} + C_{\text{infrastructure}} + C_{\text{opportunity}}$$

Each component represents a fraction of baseline fitness (between 0 and 1) that aggregators sacrifice:

- **$C_{\text{travel}}$**: The cost of traveling to the aggregation site. Energy and time spent in transit instead of foraging.
- **$C_{\text{infrastructure}}$**: The cost of building and maintaining shared facilities, storage pits, fish weirs, smoking platforms.
- **$C_{\text{opportunity}}$**: The foregone foraging that occurs because bands spend time at the aggregation site rather than in their home ranges.

These costs enter the aggregator fitness function as a multiplicative penalty:

$$W_{\text{aggregator}} = (1 - C_{\text{total}}) \times (\text{survival term}) \times (\text{cooperation benefits})$$

The $(1 - C_{\text{total}})$ term means that if $C_{\text{total}} = 0.30$, aggregators retain 70% of their baseline productive capacity after paying all aggregation costs.

We also need a parameter for the baseline advantage of the independent strategy:

$$R_{\text{ind}} = \text{independent reproductive advantage when } \sigma = 0$$

This captures the fact that, in a perfectly stable environment, independents can invest all their time and energy in foraging and reproduction, whereas aggregators divert some to cooperation. $R_{\text{ind}} > 1$ means independents have a head start; cooperation has to overcome this advantage through its insurance and cooperation benefits.

### 6.3 How to Estimate Each Cost Component

**$C_{\text{travel}} = 0.08$ (travel cost)**

How to estimate:
- **Catchment analysis**: Define the probable catchment area for Lamoka Lake. Based on the site's scale and the regional settlement pattern, a radius of approximately 75 km (150 km diameter) is reasonable. The average band would travel roughly 40-75 km to reach the site.
- **Travel cost per km**: Ethnographic and experimental data suggest that travel through temperate forest costs approximately 0.1-0.2% of annual caloric budget per km of one-way travel (accounting for travel time, portage, and foregone foraging en route). Kelly (2013:Table 4.1) compiles travel distances and mobility costs for foraging societies across diverse environments; Binford (2001:Table 5.01) provides residential move distances for temperate woodland foragers averaging 40-80 km, consistent with the Finger Lakes catchment estimate.
- **Calculation**: At 60 km average one-way distance and 0.13% per km, $C_{\text{travel}} \approx 0.08$.

Why Lamoka Lake's travel cost is low: The Finger Lakes catchment (~150 km) is much smaller than Poverty Point's (~500 km), so bands travel shorter distances. Travel follows lake valleys and stream corridors, which are relatively easy terrain. Fall timing means bands are traveling when they would otherwise be transitioning to winter ranges anyway.

**$C_{\text{infrastructure}} = 0.12$ (infrastructure cost)**

How to estimate:
- **Pit construction labor**: A typical storage pit (60 cm diameter, 60 cm deep) requires approximately 2-4 person-hours to excavate, line, and prepare. Experimental archaeology on prehistoric pit construction in comparable soils (DeBoer 1988; Wandsnider 1997) yields estimates of 1-3 person-hours for excavation alone, with additional time for lining and preparation. With 380 pits over 60 core years, that is roughly 6-7 pits per year, representing approximately 15-25 person-hours of digging labor per year.
- **Fish weir maintenance**: Wooden stake weirs require annual repair. Estimated 50-100 person-hours per season.
- **Smoking platform operation**: Construction and fuel gathering, estimated 30-60 person-hours per season.
- **Total labor**: Approximately 100-200 person-hours per season, divided among 200-300 aggregating individuals. As a fraction of total annual productive time (~2,000 hours per person), this is roughly 0.10-0.15.

Why this cost is moderate: Unlike Poverty Point, where monumental mound construction (238,000 cubic meters for Mound A alone) represented enormous labor investment with no direct caloric return, Lamoka Lake's infrastructure is utilitarian. Storage pits store food. Fish weirs catch fish. The infrastructure generates direct returns, partially offsetting its labor cost. The *net* cost ($C_{\text{infrastructure}} = 0.12$) already accounts for some of this offset.

**$C_{\text{opportunity}} = 0.10$ (opportunity cost)**

How to estimate:
- **Seasonal timing**: Fall aggregation coincides with the peak availability of the resources being processed (mast, fish, deer). This means bands are not missing prime foraging in their home ranges; they are foraging at the aggregation site instead. The opportunity cost is the *difference* between what they would have harvested at home versus what they harvest at the aggregation site (before accounting for communal processing benefits).
- **Duration**: If aggregation lasts 4-6 weeks out of a 26-week productive season (April-October), bands spend roughly 15-23% of their productive season at the site. But because they are actively foraging and processing during aggregation, the true opportunity cost is only the marginal difference.

### 6.4 The Independent Advantage ($R_{\text{ind}}$)

$R_{\text{ind}} = 1.08$ for Lamoka Lake. This means that in a perfectly stable environment ($\sigma = 0$), independents would have an 8% fitness advantage over aggregators. This advantage comes from:

- No travel costs (save time and energy)
- No infrastructure investment (devote all labor to direct foraging)
- Full flexibility in foraging decisions (no obligation to be at a specific place at a specific time)

An important subtlety: $R_{\text{ind}}$ captures the advantage of independence *only in a hypothetical world with zero environmental variability*. It does not include winter hardship or resource shortfalls, those effects are captured separately by $\beta$ and $\sigma$. $R_{\text{ind}}$ purely reflects the structural efficiency of not paying cooperation costs.

Why $R_{\text{ind}} = 1.08$ and not higher? The Finger Lakes region has relatively short growing seasons and cold winters that limit the total annual caloric budget available to any band, whether cooperating or not. In this context, the 30% cooperation cost ($C_{\text{total}}$) represents a substantial fraction of the annual budget, but the *marginal* advantage of avoiding that cost is limited because even independent bands must invest heavily in winter preparation (building shelters, caching food individually). The 8% advantage reflects the fact that independent bands save on cooperation costs but must substitute their own individual preparation efforts. Compare to Poverty Point ($R_{\text{ind}} = 1.10$), where the longer growing season and milder winters in the Lower Mississippi Valley provide independents with a slightly larger margin of advantage from avoiding cooperation costs (Kelly 2013).

### 6.5 Summary: Lamoka Lake Costs

**Table 6.1. Cost decomposition across four case studies.**

| Component | Rapa Nui | Chaco Canyon | Poverty Point | **Lamoka Lake** |
|-----------|----------|--------------|---------------|-----------------|
| $C_{\text{travel}}$ | 0.00 | 0.00 | 0.12 | **0.08** |
| $C_{\text{signal}}$ | 0.35 | 0.35 | 0.18 | -- |
| $C_{\text{infrastructure}}$ | -- | -- | -- | **0.12** |
| $C_{\text{opportunity}}$ | 0.00 | 0.10 | 0.12 | **0.10** |
| **$C_{\text{total}}$** | **0.35** | **0.45** | **0.42** | **0.30** |
| $R_{\text{ind}}$ | 1.00 | 1.10 | 1.10 | **1.08** |

Note the key distinction: at Lamoka Lake, there is no signal cost ($C_{\text{signal}}$) because the infrastructure is utilitarian. It is replaced by the lower infrastructure cost ($C_{\text{infrastructure}} = 0.12$). This makes Lamoka Lake's total cost (0.30) the lowest of all four case studies, which is one reason its threshold ($\sigma^*$) is also the lowest.

---

## 7. The Tipping Point: Deriving $\sigma^*$

### 7.1 What We Are Adding and Why

We now have all the pieces needed to calculate the tipping point. We have:

- Aggregator fitness that depends on costs ($C_{\text{total}}$) and vulnerability ($\alpha$)
- Independent fitness that depends on reproductive advantage ($R_{\text{ind}}$) and vulnerability ($\beta$)
- Both fitness functions depending on environmental uncertainty ($\sigma$)

The tipping point $\sigma^*$ is the value of $\sigma$ where both strategies yield exactly equal fitness. Below $\sigma^*$, independents do better. Above $\sigma^*$, aggregators do better.

### 7.2 The Algebra, Step by Step

We will work through this slowly. Each step does one thing.

**Step 1: Write the two fitness functions.**

For now, we use the simplified versions (without ecotone advantage, cooperation returns, or reciprocal benefits, which we will add in Sections 8-10). The core fitness functions are:

$$W_{\text{agg}} = (1 - C_{\text{total}}) \cdot (1 - \alpha \cdot \sigma)$$

$$W_{\text{ind}} = R_{\text{ind}} \cdot (1 - \beta \cdot \sigma)$$

$W_{\text{agg}}$ says: aggregator fitness equals baseline productivity after paying costs, times the probability of surviving environmental stress.

$W_{\text{ind}}$ says: independent fitness equals the reproductive advantage of independence, times the probability of surviving environmental stress (at higher vulnerability).

**Step 2: Set them equal at the tipping point.**

At $\sigma = \sigma^*$, both strategies yield the same fitness:

$$W_{\text{agg}}(\sigma^*) = W_{\text{ind}}(\sigma^*)$$

$$(1 - C_{\text{total}})(1 - \alpha \cdot \sigma^*) = R_{\text{ind}} \cdot (1 - \beta \cdot \sigma^*)$$

**Step 3: Expand both sides.**

Multiply out the left side:

$$(1 - C_{\text{total}}) - (1 - C_{\text{total}}) \cdot \alpha \cdot \sigma^*$$

Multiply out the right side:

$$R_{\text{ind}} - R_{\text{ind}} \cdot \beta \cdot \sigma^*$$

So:

$$(1 - C_{\text{total}}) - (1 - C_{\text{total}})\alpha\sigma^* = R_{\text{ind}} - R_{\text{ind}}\beta\sigma^*$$

**Step 4: Collect all terms with $\sigma^*$ on one side.**

Move all $\sigma^*$ terms to the left and all constants to the right:

$$R_{\text{ind}}\beta\sigma^* - (1 - C_{\text{total}})\alpha\sigma^* = R_{\text{ind}} - (1 - C_{\text{total}})$$

**Step 5: Factor out $\sigma^*$.**

$$\sigma^* \cdot [R_{\text{ind}}\beta - (1 - C_{\text{total}})\alpha] = R_{\text{ind}} - (1 - C_{\text{total}})$$

**Step 6: Divide both sides to isolate $\sigma^*$.**

$$\boxed{\sigma^* = \frac{R_{\text{ind}} - (1 - C_{\text{total}})}{R_{\text{ind}} \cdot \beta - (1 - C_{\text{total}}) \cdot \alpha}}$$

That is the critical threshold equation. Every quantity in it has a concrete interpretation:

- **Numerator** $R_{\text{ind}} - (1 - C_{\text{total}})$: the fitness gap between strategies in a perfectly stable environment ($\sigma = 0$). Since $R_{\text{ind}} > (1 - C_{\text{total}})$ when cooperation is costly, the numerator is positive. This is the "handicap" that aggregation starts with.
- **Denominator** $R_{\text{ind}} \cdot \beta - (1 - C_{\text{total}}) \cdot \alpha$: the rate at which increasing uncertainty closes the gap. Since $\beta > \alpha$, the independent strategy loses fitness *faster* as uncertainty increases. The denominator is how quickly that faster loss catches up.

In words: $\sigma^*$ is the ratio of "how much worse aggregation starts out" to "how much faster independence declines with increasing uncertainty."

### 7.3 Plugging in Lamoka Lake Numbers (Simplified)

Using just the basic parameters (before adding ecotone, cooperation returns, etc.):

- $C_{\text{total}} = 0.30$, so $(1 - C_{\text{total}}) = 0.70$
- $R_{\text{ind}} = 1.08$
- $\alpha = 0.35$
- $\beta = 0.70$

$$\sigma^* = \frac{1.08 - 0.70}{1.08 \times 0.70 - 0.70 \times 0.35} = \frac{0.38}{0.756 - 0.245} = \frac{0.38}{0.511} \approx 0.744$$

This simplified threshold is $\sigma^* \approx 0.74$, which is unrealistically high. At this threshold, aggregation would almost never be observed because the required environmental variability approaches the upper limit of what humans can tolerate. This tells us something important: *the basic model is not enough for aggregation systems*. We need the ecotone advantage, cooperation returns, and reciprocal benefits (Sections 8-10) to bring the threshold down to the observed range.

### 7.4 What This Means and How Sensitive It Is

The threshold equation tells us how $\sigma^*$ responds to changes in each parameter:

| If this increases... | Then $\sigma^*$... | Because... |
|---------------------|---------------------|------------|
| $C_{\text{total}}$ (cost) | Goes **up** | Costlier cooperation needs more uncertainty to justify it |
| $\beta$ (independent vulnerability) | Goes **down** | More vulnerable independents make cooperation relatively better |
| $\alpha$ (aggregator vulnerability) | Goes **up** | Less effective cooperation needs more uncertainty to justify it |
| $R_{\text{ind}}$ (independent advantage) | Goes **up** | Stronger baseline advantage of going solo raises the bar |

The most influential parameters are $\beta$ (elasticity -1.86) and $C_{\text{total}}$ (elasticity +1.52). This means: if you are testing the model and can only measure a few things well, prioritize getting good estimates of independent vulnerability and cooperation costs.

![Figure 8. Sensitivity analysis: what matters most. Tornado diagram showing how sigma* changes when each parameter is varied plus or minus 20% from baseline. Green bars indicate changes that lower the threshold (helping aggregation); red bars indicate changes that raise it. Independent vulnerability (beta) and total cost are the most influential parameters.](figures/fig_08_sensitivity_tornado.png)

![Figure 4. The fitness crossover: the core prediction. Aggregator fitness (blue) and independent fitness (red) as functions of environmental uncertainty. The crossover at sigma* = 0.306 is the critical threshold. The yellow band marks the estimated Finger Lakes sigma range (0.35-0.45), which falls in the aggregation zone.](figures/fig_04_fitness_crossover.png)

**Summary: What to take away from this section.** If the algebra felt dense, here is the bottom line. The threshold $\sigma^*$ is the ratio of two quantities: (1) how much better independents do in a stable world (the numerator), divided by (2) how much faster independents lose ground as the world becomes more variable (the denominator). Everything that makes cooperation cheaper, better buffered, or more productive shrinks the numerator and grows the denominator, making $\sigma^*$ smaller and aggregation easier to sustain. The simplified model gives an unrealistically high threshold (0.74), which tells us that the additional mechanisms we introduce in Sections 8-10 are not optional extras; they are essential for explaining why aggregation is observed.

---

## 8. The Ecotone Advantage ($\varepsilon$): Portfolio Theory

### 8.1 What We Are Adding and Why

Section 7 showed that the basic model predicts an unrealistically high threshold ($\sigma^* \approx 0.74$) for Lamoka Lake. The first mechanism that brings this down is the **ecotone advantage**: the fact that the aggregation site sits at the intersection of multiple ecological zones whose productivities do not all move in lockstep.

This is directly analogous to portfolio diversification in finance. A financial advisor tells you: do not put all your money in one stock. Spread it across different sectors (technology, healthcare, energy) whose returns are not perfectly correlated. If technology crashes, maybe healthcare holds steady. The diversified portfolio has the same average return but lower variance, lower risk.

For hunter-gatherers, the "stocks" are ecological zones. The "portfolio" is the set of zones accessible from the aggregation site. And the "diversification benefit" is the reduction in effective environmental uncertainty that comes from accessing multiple zones with imperfectly correlated (and ideally negatively correlated) productivities.

### 8.2 The Math

Consider an aggregation site with access to $K$ ecological zones. Each zone $k$ has annual productivity $X_k$ with variance $\sigma_k^2$. The zones have pairwise correlations $\rho_{jk}$.

If a population divides its foraging effort equally across zones (weight $1/K$ per zone), and all zones have similar variance ($\sigma_k = \sigma_0$), the variance of the "portfolio" is:

$$\text{Var}(X_{\text{portfolio}}) = \sigma_0^2 \cdot \frac{1 + (K-1)\bar{\rho}}{K}$$

where $\bar{\rho}$ is the mean pairwise correlation across all zone pairs.

The ecotone advantage is the proportional reduction in effective uncertainty:

$$\varepsilon = 1 - \sqrt{\frac{1 + (K-1)\bar{\rho}}{K}}$$

Let us unpack each piece:

- **$K$**: the number of ecological zones. More zones = more diversification potential. Lamoka Lake has $K = 5$.
- **$\bar{\rho}$**: the average correlation between zone productivities. Negative $\bar{\rho}$ means zones tend to compensate each other (good for buffering). Positive $\bar{\rho}$ means zones tend to fail together (bad for buffering). $\bar{\rho} = 0$ means zones are independent.

**Key insight: why negative correlations matter.** When $\bar{\rho} < 0$, the expression under the square root shrinks, and $\varepsilon$ gets larger. In ecological terms, negative correlations arise when zones respond differently to the same environmental driver. For example:

- **Wet years** favor aquatic resources (fish, waterfowl) but may flood terrestrial hunting grounds and reduce nut production (late spring frosts associated with wet patterns).
- **Dry years** favor upland game (concentrated at fewer water sources) but reduce fish populations.

This complementary response creates natural buffering: when one zone fails, another tends to succeed.

### 8.3 How It Modifies the Fitness Function

The ecotone advantage reduces the effective uncertainty experienced by aggregators:

$$\sigma_{\text{eff}} = \sigma \cdot (1 - \varepsilon)$$

The aggregator fitness function becomes:

$$W_{\text{agg}} = (1 - C_{\text{total}}) \cdot (1 - \alpha \cdot \sigma \cdot (1 - \varepsilon))$$

Crucially, independents do not get this benefit. They forage in single zones and experience the full regional uncertainty $\sigma$:

$$W_{\text{ind}} = R_{\text{ind}} \cdot (1 - \beta \cdot \sigma)$$

This asymmetry, aggregators get ecotone buffering, independents do not, is what makes the ecotone advantage powerful. It widens the fitness gap between strategies under high uncertainty.

### 8.4 How to Estimate $\varepsilon$

To estimate $\varepsilon$, you need to know (1) how many zones are accessible from the site, and (2) how their productivities covary.

**Zone identification.** Use GIS analysis to map ecological zones within the foraging radius (~25 km) of Lamoka Lake. The five zones identified in the JAS manuscript are:

| Zone | Key resources | Base productivity | Inter-annual variability |
|------|--------------|-------------------|--------------------------|
| Lacustrine | Fish, waterfowl, mussels | 0.65 | 0.12 |
| Upland forest | Deer, turkey, small mammals | 0.60 | 0.10 |
| Mast | Hickory, walnut, acorn | 0.55 | 0.35 |
| Wetland | Fish, turtles, aquatic plants | 0.60 | 0.15 |
| Montane | Patchy, variable | 0.40 | 0.18 |

**Covariance estimation.** The zone covariances used in the model are *educated estimates based on ecological reasoning*, not measured values. These are among the parameters most in need of empirical refinement, and generating better estimates from modern monitoring data would be a significant dissertation contribution. The estimated covariances are:

| Zone pair | Correlation ($\rho$) | Buffering? |
|-----------|---------------------|------------|
| Lacustrine - Upland forest | -0.25 | Good: wet favors fish, dry favors game |
| Lacustrine - Mast | +0.10 | Slight positive: both moisture-dependent |
| Lacustrine - Wetland | +0.35 | Positive: both water-dependent |
| Lacustrine - Montane | -0.15 | Some buffering |
| Upland forest - Mast | +0.30 | Positive: both forest-dependent |
| Upland forest - Wetland | -0.20 | Some buffering |
| Upland forest - Montane | +0.25 | Positive: both terrestrial |
| Mast - Wetland | +0.05 | Nearly independent |
| Mast - Montane | +0.15 | Some positive |
| Wetland - Montane | -0.10 | Slight buffering |

Mean $\bar{\rho} \approx +0.05$. With $K = 5$:

$$\varepsilon = 1 - \sqrt{\frac{1 + 4 \times 0.05}{5}} = 1 - \sqrt{\frac{1.20}{5}} = 1 - \sqrt{0.24} = 1 - 0.49 \approx 0.51$$

The theoretical maximum is $\varepsilon \approx 0.51$, but the model uses a conservative $\varepsilon = 0.30$ because:
- Not all zones are equally accessible
- Foraging effort is not perfectly divided across zones
- Some zones (montane) contribute less to the diet

![Figure 5. The ecotone portfolio effect. Panel A shows five hypothetical resource zone time series with negative covariances; the bold black line is the weighted portfolio average, which is much smoother. Panel B shows how increasing ecotone advantage lowers the critical threshold, with Lamoka Lake's epsilon = 0.30 marked.](figures/fig_05_ecotone_portfolio.png)

**How to generate better estimates for a dissertation:**

1. **Modern ecological monitoring data**: Contact the USDA Forest Service and NYS DEC for long-term monitoring data on mast production, fish populations, and deer harvest within the Finger Lakes region. Calculate actual covariances from time-series data.

2. **GIS zone mapping**: Map the five zones within the foraging radius of Lamoka Lake using soils, elevation, and hydrology data. Calculate the proportion of each zone accessible from the site.

3. **Paleoenvironmental reconstruction**: Use pollen cores and sediment records to reconstruct past zone productivity and its variability.

### 8.5 How $\varepsilon$ Modifies the Threshold

With the ecotone advantage, the threshold equation becomes:

$$\sigma^* = \frac{R_{\text{ind}} - (1 - C_{\text{total}})}{R_{\text{ind}} \cdot \beta - (1 - C_{\text{total}}) \cdot \alpha_{\text{eff}}}$$

where $\alpha_{\text{eff}} = \alpha \cdot (1 - \varepsilon) = 0.35 \times 0.70 = 0.245$.

Notice that the numerator ($R_{\text{ind}} - (1 - C_{\text{total}})$) has not changed. The ecotone advantage does not affect the fitness gap at $\sigma = 0$ because when there is no uncertainty, ecotone buffering has nothing to buffer. What changes is the denominator: $\alpha_{\text{eff}} < \alpha$, so the denominator is *larger*, which makes $\sigma^*$ *smaller*. The ecotone advantage lowers the threshold by making cooperators *even more protected* against environmental shocks than the basic model assumed.

Plugging in Lamoka Lake values (still without cooperation returns):

$$\sigma^* = \frac{1.08 - 0.70}{1.08 \times 0.70 - 0.70 \times 0.245} = \frac{0.38}{0.756 - 0.172} = \frac{0.38}{0.585} \approx 0.650$$

The ecotone advantage has reduced the threshold from 0.744 to 0.650, but it is still too high. We need the remaining mechanisms (Sections 9-10) to bring it the rest of the way down.

---

## 9. Strength in Numbers: Returns to Scale ($f(n)$)

### 9.1 What We Are Adding and Why

In aggregation systems like Lamoka Lake, cooperation is not merely about risk pooling; it generates positive returns to group size. More people at the site means:

- **More productive fish weirs**: A weir operated by 10 people catches more fish per person than one operated by 3.
- **More efficient nut processing**: Division of labor, harvesting, cracking, leaching, drying, increases throughput.
- **Better game smoking**: More smoking platforms operated simultaneously means less spoilage.
- **Faster pit construction**: Digging goes faster with more hands.

These are *increasing returns to scale*, at least up to a point. Eventually, too many people deplete local resources, create sanitation problems, and generate social friction. The returns follow a hump-shaped curve: rising with group size initially, then declining after the site reaches capacity.

### 9.2 The Math

The cooperation benefit function is:

$$f(n) = 1 + b \cdot \ln(n) - c \cdot (n - n^*)^2 \cdot \mathbb{1}_{n > n^*}$$

Let us unpack each piece:

- **$f(n)$**: The cooperation benefit multiplier. At $f = 1$, there is no cooperation benefit (a single band). At $f = 1.25$, cooperation boosts productivity by 25%.
- **$n$**: The number of bands at the aggregation site. More bands = more cooperation potential.
- **$b$**: The benefit coefficient. How much does each additional band contribute? Range: 0.02-0.15.
- **$\ln(n)$**: The natural logarithm of $n$. This captures **diminishing marginal returns**: the second band adds a lot (doubling labor force), but the twelfth band adds only a little. The logarithm is the mathematically natural way to express this.
- **$n^*$**: The optimal group size. Below this, more bands always helps. Above this, crowding costs kick in.
- **$c$**: The crowding coefficient. How quickly do costs mount when the site is overcrowded?
- **$\mathbb{1}_{n > n^*}$**: An indicator function that equals 1 when $n > n^*$ and 0 otherwise. Crowding costs only apply above the optimal size.

**Why logarithmic?** Imagine the fish weir. With 1 band (20 people), you can build a small weir. With 2 bands (40 people), you can build a weir twice as wide and operate it in shifts, more than doubling your catch per person. With 4 bands, you have enough people for a large weir plus processing stations. But with 12 bands, the weir is already operating at capacity; the additional labor goes into diminishing-return activities. The logarithm captures this decreasing marginal benefit naturally.

### 9.3 Lamoka Lake Values

- $b = 0.10$: Strong per-capita returns from communal processing
- $n^* = 12$ bands: Site capacity of ~1.2 hectares limits optimal aggregation
- $c = 0.025$: Higher crowding coefficient than Poverty Point because the site is small

At the optimal aggregation size ($n = 12$):

$$f(12) = 1 + 0.10 \times \ln(12) = 1 + 0.10 \times 2.485 = 1.249$$

This means a 24.9% productivity boost from cooperation, roughly matching Poverty Point's 25.7% at its optimal size of 25 bands.

### 9.4 How to Estimate $b$ and $n^*$

**Ethnographic data on communal processing returns.** Documented cases of communal fishing show returns per person increasing substantially with group size. Suttles (1968) documented communal reef-net fishing among Straits Salish groups where cooperative crews of 6-15 achieved 2-3 times the per-capita catch of individual fishers. Cleland (1982) described communal fish weir operations in the Great Lakes region where cooperative labor forces of 20-50 people produced returns 50-200% above individual effort. Winterhalder (1986) modeled these returns to scale effects and showed they follow a diminishing-returns pattern consistent with logarithmic benefits. This supports $b$ in the range 0.05-0.15.

**Site area as constraint on $n^*$.** At 1.2 hectares, Lamoka Lake can physically accommodate approximately 200-300 people during a seasonal gathering. Whitelaw (1991) compiled ethnographic data on camp floor area requirements, finding that short-duration aggregation camps require approximately 40-60 m$^2$ per person (compared to 100+ m$^2$ for long-term residential camps). At 1.2 hectares (12,000 m$^2$) and 40-60 m$^2$ per person, the site accommodates 200-300 people. At 20 people per band, this is 10-15 bands, centered on 12.

**Faunal and botanical evidence for scale of processing.** The number and size of smoking platforms, fish weir extent, and storage pit volume provide evidence for the scale of communal activities. If the fish weir in the outlet channel required 8+ bands to operate effectively (based on similar ethnographic weir operations), this constrains the minimum aggregation size for full communal processing.

![Figure 6. Returns to scale: the cooperation benefit f(n). The logarithmic benefit curve shows increasing returns up to n* = 12 bands, then crowding costs. Green dots mark minimum worker thresholds for communal activities. At n = 12, f(n) = 1.249, a 24.9% productivity boost.](figures/fig_06_returns_to_scale.png)

### 9.5 How $f(n)$ Modifies the Threshold

With cooperation benefits included, the aggregator fitness becomes:

$$W_{\text{agg}} = (1 - C_{\text{total}}) \cdot (1 - \alpha_{\text{eff}} \cdot \sigma) \cdot f(n)$$

The threshold equation uses a composite term $A$:

$$A = (1 - C_{\text{total}}) \cdot f(n)$$

Since $f(n) > 1$ (when there are cooperation benefits), $A > (1 - C_{\text{total}})$, which means the numerator of the threshold equation decreases and $\sigma^*$ drops. Returns to scale lower the threshold, making aggregation viable in less variable environments.

---

## 10. Social Insurance: Reciprocal Obligations ($B_{\text{recip}}$)

### 10.1 What We Are Adding and Why

Aggregation is not a one-shot interaction. Bands that repeatedly co-aggregate form social bonds, debts of mutual aid that can be called upon in future shortfalls. If your band had a bad winter, you can call on bands you helped process fish last fall. These reciprocal obligations provide insurance value beyond the immediate returns of communal processing.

### 10.2 The Math

Reciprocal obligations enter the fitness function as a multiplier:

$$W_{\text{agg}} = (1 - C_{\text{total}}) \cdot (1 - \alpha_{\text{eff}} \cdot \sigma) \cdot f(n) \cdot (1 + B_{\text{recip}})$$

where $B_{\text{recip}}$ represents the proportional fitness boost from having a network of reciprocal obligations:

$$B_{\text{recip}} = \sum_{j} p_{\text{call}}(j) \times V_{\text{help}}(j) \times d_{\text{trust}}(j)$$

- **$p_{\text{call}}(j)$**: Probability of needing to invoke obligation $j$ in a given year (proportional to $\sigma$; more variable environments mean more frequent calls for help)
- **$V_{\text{help}}(j)$**: Value of received help relative to baseline fitness (food sharing, labor assistance, information)
- **$d_{\text{trust}}(j)$**: Reliability discount, the probability that the obligated partner will actually honor the commitment

### 10.3 Why the Upper Bound Is Low

For Lamoka Lake, $B_{\text{recip}} = 0.05$, meaning reciprocal obligations provide a 5% fitness boost. This is deliberately conservative. If reciprocal obligations provided very large benefits (say, 20% or more), a "fake cooperator" strategy, attending aggregation just long enough to establish obligations, then defecting, would become viable. The honesty of the reciprocal system requires that obligations build gradually through repeated interaction and that the benefits, while real, are modest enough not to invite exploitation.

Ethnographic data from !Kung $hxaro$ exchange networks suggest that social network insurance typically provides a 5-10% buffer against individual shortfalls (Wiessner 2002).

### 10.4 How to Estimate $B_{\text{recip}}$

**Exchange goods as proxy.** The presence and frequency of non-local materials (beveled adzes, Genesee Valley cherts) at Lamoka Lake indicate exchange relationships between bands. Higher frequencies of exchange goods suggest stronger reciprocal networks.

**Burial patterns.** If individuals from different bands are buried at the aggregation site, this indicates enduring social connections across band boundaries, consistent with strong reciprocal obligation networks.

**Ethnographic analogs.** Data from documented foraging societies with seasonal aggregation patterns (California acorn harvest gatherings, Australian corroboree systems) provide calibration for the magnitude of reciprocal benefits.

**Tracking the threshold: how each mechanism brought $\sigma^*$ down.**

Before we assemble the complete model, it is worth seeing how each extension contributed. Starting from the basic cost-vulnerability framework and adding one mechanism at a time:

| After adding... | $\sigma^*$ | Change | Why it helps |
|----------------|-----------|--------|-------------|
| Basic model (Sections 4-7) | 0.744 | -- | Costs vs. vulnerability alone |
| + Ecotone advantage $\varepsilon = 0.30$ (Section 8) | 0.650 | -0.094 | Reduces effective $\alpha$ by 30% |
| + Cooperation returns $f(12) = 1.249$ (Section 9) | 0.380 | -0.270 | Boosts aggregator productivity 25% |
| + Reciprocal benefits $B_{\text{recip}} = 0.05$ (Section 10) | 0.306 | -0.075 | Adds 5% insurance value |

![Figure 7. Building the threshold: how each mechanism lowers sigma*. The waterfall chart shows how the threshold drops from 0.744 (basic model) to 0.306 (full model) as each mechanism is added. Cooperation returns contribute the largest single reduction. The yellow band shows the Finger Lakes sigma range.](figures/fig_07_waterfall_threshold.png)

The biggest single contribution comes from cooperation returns ($f(n)$), which reflects the direct caloric benefit of communal processing. The ecotone advantage provides substantial additional reduction. Reciprocal benefits contribute modestly. Together, these three mechanisms cut the threshold from an impractical 0.74 to an empirically relevant 0.31.

---

# PART III: PUTTING IT ALL TOGETHER

---

## 11. The Complete Model for Lamoka Lake

### 11.1 Full Fitness Equations

Combining all the mechanisms from Sections 4-10, the complete fitness equations are:

**Aggregator fitness:**

$$W_{\text{agg}}(\sigma, \varepsilon, n) = (1 - C_{\text{total}}) \cdot (1 - \alpha \cdot \sigma(1-\varepsilon)) \cdot f(n) \cdot (1 + B_{\text{recip}})$$

This has four multiplicative components:

| Component | Expression | Lamoka value | What it captures |
|-----------|-----------|--------------|-----------------|
| Cost penalty | $(1 - C_{\text{total}})$ | $1 - 0.30 = 0.70$ | Costs of travel, infrastructure, opportunity |
| Environmental survival | $(1 - \alpha \cdot \sigma_{\text{eff}})$ | Depends on $\sigma$ | Survival under environmental stress, buffered by ecotone |
| Cooperation returns | $f(n)$ | $f(12) = 1.249$ | Returns to scale from communal processing |
| Reciprocal insurance | $(1 + B_{\text{recip}})$ | $1.05$ | Insurance value of social network |

**Independent fitness:**

$$W_{\text{ind}}(\sigma) = R_{\text{ind}} \cdot (1 - \beta \cdot \sigma)$$

This has two components:

| Component | Expression | Lamoka value | What it captures |
|-----------|-----------|--------------|-----------------|
| Reproductive advantage | $R_{\text{ind}}$ | $1.08$ | Advantage from avoiding cooperation costs |
| Environmental survival | $(1 - \beta \cdot \sigma)$ | Depends on $\sigma$ | Survival under environmental stress, fully exposed |

### 11.2 Worked Numerical Example: Calculating $\sigma^*$

Now we walk through the complete $\sigma^*$ calculation for Lamoka Lake, step by step, with actual numbers.

**Step 1: Calculate the composite cooperation term $A$.**

$$A = (1 - C_{\text{total}}) \cdot f(n) \cdot (1 + B_{\text{recip}})$$

$$A = (1 - 0.30) \times 1.249 \times (1 + 0.05)$$

$$A = 0.70 \times 1.249 \times 1.05$$

$$A = 0.70 \times 1.311 = 0.918$$

**Step 2: Calculate the effective cooperator vulnerability $\alpha_{\text{eff}}$.**

$$\alpha_{\text{eff}} = \alpha \times (1 - \varepsilon) = 0.35 \times (1 - 0.30) = 0.35 \times 0.70 = 0.245$$

**Step 3: Calculate the numerator of the threshold equation.**

$$\text{Numerator} = R_{\text{ind}} - A = 1.08 - 0.918 = 0.162$$

This is the fitness gap between strategies at $\sigma = 0$: independents start with a 0.162 advantage.

**Step 4: Calculate the denominator.**

$$\text{Denominator} = R_{\text{ind}} \cdot \beta - A \cdot \alpha_{\text{eff}}$$

$$= 1.08 \times 0.70 - 0.918 \times 0.245$$

$$= 0.756 - 0.225 = 0.531$$

This is the rate at which increasing uncertainty closes the gap between strategies.

**Step 5: Divide to get $\sigma^*$.**

$$\sigma^* = \frac{0.162}{0.531} = 0.305$$

**Result: $\sigma^* \approx 0.306$ for Lamoka Lake.**

This means: if the Finger Lakes Late Archaic environment had a coefficient of variation in annual resource returns exceeding approximately 0.31, aggregation at the Lamoka Lake ecotone should have been the dominant strategy. Given the estimated $\sigma \approx 0.35$-$0.45$, the model predicts aggregation, consistent with what we observe.

### 11.3 Comparing Lamoka Lake to Other Case Studies

**Table 11.1. Threshold comparison across four case studies.**

| Case | $\sigma^*$ | Estimated $\sigma$ | $\sigma > \sigma^*$? | Observed? | Duration |
|------|-----------|--------------------|-----------------------|-----------|----------|
| Lamoka Lake | 0.305 | 0.35-0.45 | Yes | Yes | ~1,600 years |
| Rapa Nui | 0.389 | ~0.31 | Marginal | Conditional | ~400 years |
| Poverty Point | 0.534 | 0.45-0.55 | Marginal | Yes | ~600 years |
| Chaco Canyon | ~0.15 | 0.17 | Yes | Yes | ~300 years |

![Figure 9. Four case studies compared. Each row shows a case study's critical threshold (diamond) and estimated sigma range (horizontal bar). Green bars indicate cases where sigma clearly exceeds sigma* (aggregation predicted and observed). Yellow bars indicate marginal cases where sigma is near sigma*. Duration of occupation is annotated.](figures/fig_09_case_comparison.png)

Three important patterns emerge:

1. **Lamoka Lake has the lowest threshold.** This is because its costs are lowest (utilitarian infrastructure, small catchment) and its cooperation benefits are strong (communal processing generates direct caloric returns). The lower threshold means aggregation becomes viable under milder environmental conditions.

2. **Lamoka Lake has the longest duration.** The ~1,600-year broad occupation window is the longest of all four cases. This is consistent with the model: a lower threshold means the system is more robust, it takes a larger decrease in environmental variability to push the system below threshold and cause collapse.

3. **Near-threshold systems are unstable.** Rapa Nui and Poverty Point, where estimated $\sigma$ is close to $\sigma^*$, both eventually collapsed. Lamoka Lake and Chaco, where $\sigma$ is more comfortably above $\sigma^*$, operated for longer periods.

### 11.4 Why Lamoka Has the Lowest Threshold

The Lamoka Lake model differs from the other three cases in two key ways that drive the low threshold:

**Lower costs.** $C_{\text{total}} = 0.30$ versus 0.35-0.45 for the other cases. The main reason: Lamoka Lake's infrastructure is utilitarian (storage pits, fish weirs) rather than monumental (22-meter mounds at Poverty Point, moai on Rapa Nui). Utilitarian infrastructure partially pays for itself through direct caloric returns, lowering the net cost.

**Stronger cooperation returns.** $b = 0.10$ versus 0.08 at Poverty Point. Communal processing at Lamoka Lake (fish weirs, nut processing, game smoking) generates direct food returns with clear increasing returns to labor. At Poverty Point, much of the cooperation investment goes into monumental earthworks with no direct caloric return.

These two differences, lower costs and stronger direct returns, compound multiplicatively. The result is a system that becomes viable at lower environmental variability and is more robust once established.

---

## 12. What the Simulation Tells Us Beyond the Math

### 12.1 Why We Need Simulation

The analytical model (Sections 4-11) makes several simplifying assumptions:

- Fitness depends linearly on $\sigma$ (in reality, the relationship may be nonlinear)
- Group size $n$ is fixed (in reality, it fluctuates year to year)
- Strategy decisions are deterministic (in reality, they are probabilistic)
- The population is well-mixed (in reality, bands are distributed across space)
- There is no memory or path dependence (in reality, past experience influences decisions)

The agent-based model (ABM) relaxes all of these assumptions. It simulates 25 bands over 1,600 years with stochastic resource returns, spatial structure, probabilistic decision-making, memory effects, and dynamic demographics.

### 12.2 Key Simulation Results

**Phase transition confirmed.** The ABM reproduces the phase transition predicted by the analytical model. At low $\sigma$ (0.05-0.28), most bands forage independently. As $\sigma$ approaches and exceeds the threshold, bands increasingly aggregate. The simulated transition zone ($\sigma \approx 0.40$-$0.45$) is somewhat above the analytical prediction ($\sigma^* = 0.306$).

Why the gap? The analytical model assumes optimal, instantaneous decision-making: bands immediately choose whichever strategy has higher fitness. The ABM is more realistic. Bands learn from experience, take time to switch strategies, make occasional mistakes, and face stochastic resource draws that add noise to the signal. Just as a real insurance market does not snap into equilibrium the instant risk crosses a threshold, the simulated population needs $\sigma$ somewhat above $\sigma^*$ before the aggregation advantage is strong enough to emerge reliably through the noise. The analytical threshold is the *minimum* level of uncertainty at which aggregation can theoretically pay off; the simulated threshold is the *practical* level at which it actually takes hold. Both are useful: the analytical value tells us where the fundamental tipping point is, and the simulated value tells us what we should expect in a messy, realistic world.

**Null models confirm mechanism.** Six null models each remove one component of the model. None produces aggregation, confirming that the full mechanism (uncertainty + ecotone + vulnerability differential + cooperation returns + processing) is required. No single mechanism is sufficient.

**Robustness test.** Even with extreme processing returns (fish weir returns doubled, nut storage fraction increased to 95%), the sigma barrier cannot be overcome. If environmental variability is too low ($\sigma < \sigma^*$), no amount of processing productivity makes aggregation adaptive. The barrier is structural, not quantitative.

![Figure 10. Phase space: where aggregation emerges. The two-dimensional parameter space of environmental uncertainty (sigma) and ecotone advantage (epsilon). Blue regions indicate where aggregation dominates; red regions where independence dominates. The black contour is the phase boundary. All four case studies are marked, showing their positions relative to the boundary.](figures/fig_10_phase_space.png)

### 12.3 Where Analytical Approximations Break Down

The ABM reveals several dynamics that the analytical model misses:

1. **Gradual transition.** The analytical model predicts a sharp phase transition at $\sigma^*$. The ABM shows a gradual transition over a range of $\sigma$ values ($\pm 0.03$-$0.05$ around $\sigma^*$), reflecting the time needed for strategy frequencies to equilibrate.

2. **Hysteresis.** Once cooperation is established, it persists slightly below $\sigma^*$ due to cultural inertia (memory effects, established reciprocal networks). Once lost, it requires $\sigma$ slightly above $\sigma^*$ to re-emerge. This hysteresis is important for interpreting the archaeological record: the system may show "stickiness" near the threshold.

3. **Stochastic clustering.** In some simulation runs, shortfall events cluster randomly, creating periods of intense aggregation followed by periods of reduced activity. This mirrors the kind of punctuated pattern we might expect in the archaeological record: bursts of intensive site use separated by quieter intervals.

4. **Dynamic group size.** The analytical model assumes $n = 12$ (the optimal), but in the ABM, aggregation size fluctuates from 2-4 bands (just below threshold) to 13-20 bands (well above). This means the cooperation benefit $f(n)$ varies over time, creating dynamic feedback between group size and threshold.

---

# PART IV: TESTING THE MODEL — A DISSERTATION RESEARCH DESIGN

---

## 13. Seven Testable Predictions

The model generates seven specific predictions, labeled H1 through H7. For each, we describe: (1) what the model predicts and why, (2) what evidence would confirm it, (3) what evidence would falsify it, (4) what data are required, and (5) what methods to use.

### 13.1 H1: Fall Aggregation Seasonality

**Prediction.** Aggregation at Lamoka Lake occurred primarily during fall (September-November), timed to coincide with mast harvest, fall fish runs, and deer during the rut. The model predicts fall timing because the processing module specifies that communal nut processing, fish weir operation, and game smoking all reach peak returns when these resources are maximally available. Additionally, fall-processed food has the highest preservation potential for winter consumption.

**Confirming evidence:**
- Deer mandibles showing fall-season kill patterns (dental eruption stages, antler growth)
- Fish otoliths with growth rings indicating fall capture
- High densities of hickory and walnut shell fragments in association with storage features
- Migratory waterfowl remains concentrated in fall-indicative contexts
- Minimal evidence for warm-season (spring-summer) residential occupation

**Falsifying evidence:**
- Seasonality indicators showing primarily spring or summer occupation
- Deer mandibles predominantly from winter or spring kills
- Absence of fall-harvest plant remains in storage contexts
- Evidence for year-round residential occupation at the same intensity

**Required data:**
- Faunal seasonality analysis (mandibles, otoliths, antler fragments)
- Botanical analysis of storage pit contents
- Migratory species occurrence by stratigraphic context

**Methods:**
- Cementum annuli analysis of deer teeth for season-of-death determination
- Fish otolith thin-section analysis
- Flotation and botanical identification of storage pit fill
- Taxonomic identification of avian remains with seasonal availability assessment

### 13.2 H2: Storage Infrastructure Scaling

**Prediction.** Storage pit accumulation scales with the product of aggregation size, aggregation frequency, and occupation duration. With 12 bands aggregating for approximately 60 core years, the model predicts total storage infrastructure consistent with ~380 pits. Pit construction should be concentrated during the core occupation period (~2962-2902 BCE) with lower rates before and after.

**Confirming evidence:**
- Pit construction dates clustering within the core occupation window
- Overlapping pits indicating sequential construction episodes
- Pit density correlating with indicators of aggregation intensity (faunal density, exotic goods)
- Construction rate accelerating during the core period and declining afterward

**Falsifying evidence:**
- Pits constructed uniformly throughout the full occupation span
- No temporal clustering of construction
- Pit density uncorrelated with aggregation indicators
- Pits constructed primarily during periods of low aggregation

**Required data:**
- AMS dates on short-lived organics from pit fill (charcoal, nutshell, bone)
- Stratigraphic analysis of pit-cutting relationships
- Pit morphology and size data through the sequence

**Methods:**
- Targeted AMS dating of 20-30 pits spanning the occupation sequence
- Harris matrix construction from pit superposition relationships
- Statistical analysis of construction rate over time (kernel density estimation on dates)

### 13.3 H3: Ecotone-Driven Site Selection

**Prediction.** Aggregation sites with dense storage infrastructure should cluster at ecotone intersections where multiple ecological zones are accessible within a single foraging radius ($\varepsilon > 0$). Sites in single-zone locations should lack aggregation-scale infrastructure. The model predicts this because ecotone buffering is necessary for the threshold to be low enough for aggregation to emerge.

**Confirming evidence:**
- Positive correlation between ecological zone diversity (within foraging radius) and storage infrastructure density across Late Archaic sites in the Finger Lakes
- Lamoka Lake having the highest zone diversity score among sites with dense storage features
- Sites in single-zone interiors (deep forest, high montane) lacking storage pit concentrations

**Falsifying evidence:**
- Dense storage sites in single-zone locations with low ecotone diversity
- No correlation between zone diversity and infrastructure density
- Multiple sites with Lamoka-like infrastructure in non-ecotone locations

**Required data:**
- Regional site database with storage feature counts
- GIS-based ecological zone mapping for the Finger Lakes region
- Zone diversity index calculated for each known site location

**Methods:**
- GIS analysis mapping five ecological zones within 25 km radius of each Late Archaic site
- Calculation of ecotone diversity index (number of zones, area proportions)
- Regression analysis: storage density vs. ecotone diversity
- This is the cheapest hypothesis to test because it uses existing site data and GIS

### 13.4 H4: Environmental Variability Correlation

**Prediction.** Periods of higher environmental variability should correspond to more intensive aggregation, greater storage investment, and larger aggregation sizes. Periods of lower variability should correspond to reduced aggregation. This follows directly from the threshold mechanism: the fitness advantage of aggregation grows with $\sigma$.

**Confirming evidence:**
- Positive correlation between paleoclimate variability proxies and indicators of aggregation intensity at Lamoka Lake
- Periods of high climate variability coinciding with peak storage pit construction
- Periods of low variability coinciding with reduced site use

**Falsifying evidence:**
- No correlation between climate variability and aggregation intensity
- Aggregation intensifying during stable periods
- Aggregation declining during variable periods

**Required data:**
- High-resolution paleoclimate proxy record for the Finger Lakes (3500-1300 BCE)
- Archaeological indicators of aggregation intensity through the occupation sequence

**Methods:**
- Obtain or generate pollen, varve, or speleothem records covering the occupation period
- Calculate rolling variability measures (e.g., 50-year moving window standard deviation)
- Correlate with archaeological intensity indicators (AMS date density, pit construction rate, faunal density)

### 13.5 H5: Regional Site Hierarchy

**Prediction.** The regional site distribution should be strongly skewed, with one dominant aggregation site (Lamoka Lake) and numerous smaller camps lacking aggregation-scale infrastructure. This derives from the cooperation benefit function $f(n)$, which produces increasing returns: bands benefit from joining the largest aggregation rather than starting a competing one.

**Confirming evidence:**
- Right-skewed distribution of storage pit densities across Finger Lakes Late Archaic sites
- Lamoka Lake as an extreme outlier in pit density (317/hectare)
- Most other sites showing densities consistent with single-band occupation (<20 pits/hectare)
- Possibly 1-2 secondary aggregation sites with intermediate densities

**Falsifying evidence:**
- Multiple sites with Lamoka-like storage densities (suggesting competing aggregation sites)
- Uniform distribution of storage infrastructure across the region
- No outlier pattern (graduated hierarchy rather than extreme skew)

**Required data:**
- Systematic inventory of storage features at Late Archaic sites across the Finger Lakes
- Site area and feature density calculations

**Methods:**
- Database compilation from published excavation reports, site files (NYS OPRHP CRIS database)
- Statistical analysis of site-size distribution (Gini coefficient, rank-size analysis)
- Comparison to expectations from different settlement models

### 13.6 H6: Exchange Goods Concentration

**Prediction.** Non-local artifacts, particularly beveled adzes and Genesee Valley cherts (~80 km distant), should be concentrated at the aggregation site relative to smaller camps. Exchange goods are acquired during aggregation events when many bands interact, so they accumulate preferentially at the aggregation site.

**Confirming evidence:**
- Higher frequencies of non-local materials at Lamoka Lake than at contemporary camps
- Non-local materials associated with high-investment features (storage pits, hearths, burials)
- Exchange goods increasing during periods of intensive aggregation

**Falsifying evidence:**
- Uniform distribution of exchange goods across all site types
- Higher concentrations at small camps than at the aggregation site
- Exchange goods unrelated to aggregation features

**Required data:**
- Lithic sourcing data from Lamoka Lake and comparative sites
- Artifact provenance by feature context at Lamoka Lake

**Methods:**
- XRF or other sourcing analysis on beveled adzes and Genesee-type cherts
- Comparison of non-local artifact proportions across site types
- Spatial analysis of exchange goods within the Lamoka Lake site

### 13.7 H7: Abandonment Under Environmental Stabilization

**Prediction.** The Lamoka Lake aggregation system should cease when environmental variability drops below $\sigma^*$. The model predicts that abandonment correlates with environmental *stabilization* (reduced variability), not necessarily deterioration (persistent drought or cooling). When variability is too low to generate the survival differential that makes aggregation economically advantageous, bands should revert to independent foraging.

This is the most counterintuitive and diagnostic prediction. Most alternative models predict that environmental improvement strengthens existing institutions. The aggregation economics model predicts the opposite: stable good times should cause collapse because the insurance value of aggregation drops below its cost.

**Confirming evidence:**
- Terminal occupation at Lamoka Lake correlating with decreased variability in paleoclimate proxies
- Abandonment occurring during a period of environmental stability, not deterioration
- Post-abandonment regional settlement showing dispersed pattern without aggregation-scale sites

**Falsifying evidence:**
- Abandonment during a period of increasing environmental variability
- Abandonment caused by environmental deterioration (drought, cooling)
- Abandonment during a period of documented social disruption unrelated to climate

**Required data:**
- High-resolution paleoclimate record spanning the abandonment period
- Precise chronology of the terminal occupation

**Methods:**
- AMS dating of terminal occupation features
- Paleoclimate variability analysis spanning the abandonment period
- Comparison of pre-abandonment and post-abandonment variability levels

---

## 14. Required Data Classes

### 14.1 Chronological Data

**What exists:**
- Ritchie's original excavation notes and publications (1932, 1969)
- Limited original radiocarbon dates
- Recent AMS dates constraining the core occupation (~2962-2902 BCE)

**What is needed:**
- Additional AMS dates (20-30) targeting specific features (storage pits, hearths, burials) to establish construction chronology
- Bayesian modeling of the radiocarbon chronology to refine occupation phases

**Where to get it:**
- Curated collections at the Rochester Museum and Science Center (RMSC)
- New York State Museum (NYSM), Albany
- AMS laboratory (e.g., UCIAMS, Beta Analytic, or university facility)
- Budget: ~$300-500 per date, $6,000-15,000 total

### 14.2 Seasonality Data

**What exists:**
- Ritchie's original faunal identifications (species-level only)
- General characterizations of resource availability

**What is needed:**
- Detailed faunal seasonality analysis (cementum annuli, otolith analysis)
- Migratory species occurrence data
- Botanical seasonality indicators from storage pit contents

**Where to get it:**
- Curated faunal collections (RMSC, NYSM)
- Zooarchaeological specialist for cementum annuli analysis
- Paleoethnobotanist for flotation and identification
- Budget: ~$5,000-10,000 for specialist analyses

### 14.3 Paleoenvironmental Data

**What exists:**
- General Late Holocene climate reconstructions for the Northeast
- Some pollen diagrams from Finger Lakes region (published in various journals)
- Modern ecological monitoring data from NYS DEC

**What is needed:**
- High-resolution pollen core from Lamoka Lake or adjacent water body
- Sediment analysis for hydrological variability proxies
- Regional speleothem or other proxy data for the 3500-1300 BCE window
- Modern covariance data for the five ecological zones

**Where to get it:**
- Cornell Department of Earth and Atmospheric Sciences (existing cores?)
- Lamont-Doherty Earth Observatory (regional paleoclimate expertise)
- NYS DEC and USDA Forest Service (modern monitoring data)
- Budget: new core extraction and analysis ~$15,000-25,000; compilation of existing data ~$2,000-5,000

### 14.4 Spatial Data

**What exists:**
- Ritchie's site plan (published 1932)
- General USGS topographic and hydrological mapping
- NYS OPRHP CRIS archaeological site database

**What is needed:**
- GIS database of Late Archaic sites in the Finger Lakes region with feature data
- Ecological zone mapping within foraging radii
- Digital elevation model analysis for catchment and travel cost modeling

**Where to get it:**
- NYS OPRHP CRIS database (requires research application)
- USGS National Map data (freely available)
- USDA NRCS soils data (freely available)
- Budget: GIS analysis is largely software and labor cost, ~$2,000-5,000

### 14.5 Exchange Data

**What exists:**
- Ritchie's artifact descriptions and illustrations
- General characterizations of beveled adzes and Genesee points as "exotic"

**What is needed:**
- Formal lithic sourcing analysis (XRF or LA-ICP-MS)
- Comparative sourcing data from other Finger Lakes sites
- Quantitative comparison of non-local artifact frequencies across site types

**Where to get it:**
- Curated lithic collections (RMSC, NYSM)
- Archaeometry laboratory for sourcing analysis
- Budget: ~$50-100 per sample, ~$5,000-10,000 for a comprehensive analysis

### 14.6 Storage Data

**What exists:**
- Ritchie's pit counts, dimensions, and general descriptions
- Some information on pit contents and lining materials

**What is needed:**
- Systematic re-analysis of pit morphology, capacity, and construction sequence
- Comparative data on storage features from other Finger Lakes sites
- Detailed analysis of pit fill contents (botanical, faunal, sediment)

**Where to get it:**
- Original excavation records and notes (RMSC, Ritchie papers)
- Published and unpublished site reports from regional CRM and academic projects
- Budget: primarily research time; ~$3,000-5,000 for collections access and analysis

### 14.7 Faunal and Botanical Data

**What exists:**
- Ritchie's species lists and general descriptions
- Some published faunal and botanical analyses

**What is needed:**
- Comprehensive faunal reanalysis with modern methods (NISP, MNI, skeletal element representation)
- Diet breadth analysis to assess resource diversification
- Stable isotope analysis of human bone for dietary reconstruction

**Where to get it:**
- Curated collections (RMSC, NYSM)
- Zooarchaeological specialist
- Stable isotope laboratory
- Budget: ~$8,000-15,000 for comprehensive reanalysis

---

## 15. Alternative Hypotheses

A rigorous dissertation must consider alternative explanations. The model's predictions are most convincing when they can distinguish between the aggregation economics hypothesis and plausible alternatives. Here we lay out six alternative hypotheses, describe their predictions, and identify where they overlap with and diverge from the aggregation economics model.

### 15.1 Alternative 1: Trade Center Model

**Claim.** Lamoka Lake served as a central place in a regional exchange network. Bands congregated to trade goods, and the infrastructure resulted from trade-related activities.

**Predictions:**
- Exchange goods should be abundant and central to site activities
- Infrastructure should relate to trade facilitation, not food processing
- Site location should optimize network centrality, not ecological diversity
- Site importance should track trade network intensity, not environmental variability

**Overlap with aggregation economics:** Both predict exchange goods concentration at the site (H6) and regional site hierarchy (H5).

**Distinguishing tests:**
- Trade center predicts exchange goods drive infrastructure; economics predicts infrastructure drives exchange. Test: do exchange goods precede or follow storage pit construction?
- Trade center predicts no relationship between environmental variability and site intensity (H4 distinguishes).
- Trade center does not predict ecotone-driven site selection (H3 distinguishes).

### 15.2 Alternative 2: Ritual/Ceremonial Center

**Claim.** Lamoka Lake served as a ritual or ceremonial center. The burials, the density of features, and the aggregation pattern reflect ceremonial rather than economic motivations.

**Predictions:**
- Ritual objects and features should be prominent
- Burials should show evidence of elaborate ceremonial treatment
- Infrastructure investment should exceed economic necessity
- Site location may reflect cosmological significance rather than ecological factors

**Overlap with aggregation economics:** Both predict fall seasonality (if ceremonies were harvest-timed) and site primacy.

**Distinguishing tests:**
- Ceremonial model does not predict storage scaling with aggregation size (H2 distinguishes).
- Ceremonial model does not predict environmental variability correlation (H4 distinguishes).
- Ceremonial model does not predict abandonment under stabilization (H7 distinguishes).
- If burials show simple interment without grave goods or elaborate preparation, the ceremonial interpretation is weakened.

### 15.3 Alternative 3: Aggrandizer ("Big Man") Model

**Claim.** Ambitious individuals organized communal labor to enhance their own status. Storage infrastructure reflects competitive display and accumulation by emerging elites, not cooperative risk management.

**Predictions:**
- Storage and exchange goods should be unequally distributed (concentrated with "Big Men")
- Infrastructure investment should scale with individual status markers, not aggregation size
- Burials should show inequality in grave goods and treatment
- Site should show evidence of centralized control (differential access to storage features)

**Overlap with aggregation economics:** Both predict site primacy and aggregation-scale infrastructure.

**Distinguishing tests:**
- Aggrandizer model predicts unequal distribution of storage and goods; economics predicts relatively even distribution.
- Aggrandizer model does not predict environmental threshold for emergence (H4, H7 distinguish).
- If storage pits are distributed evenly across the site without evidence of differential access, the aggrandizer interpretation is weakened.

### 15.4 Alternative 4: Resource Abundance Model

**Claim.** Lamoka Lake was simply a very rich location. High resource abundance attracted people and sustained large populations, and the infrastructure naturally followed from long-term occupation.

**Predictions:**
- Site should be located at the point of maximum resource abundance
- Infrastructure should scale with total resource availability, not environmental variability
- Site use should intensify during periods of high resource availability
- No specific relationship between variability and aggregation intensity

**Overlap with aggregation economics:** Both recognize the ecological importance of the site location.

**Distinguishing tests:**
- Abundance model predicts site use intensifies during good times; economics predicts intensification during variable times (H4 distinguishes).
- Abundance model predicts gradual infrastructure accumulation proportional to occupation duration; economics predicts pulse construction during high-variability periods (H2 distinguishes).
- Abundance model does not predict abandonment under stabilization (H7 distinguishes).
- Abundance model predicts sites at points of maximum productivity, not maximum diversity. If other locations in the Finger Lakes have higher absolute productivity but lack aggregation infrastructure, the abundance model is weakened (H3 distinguishes).

### 15.5 Alternative 5: Costly Signaling Model

**Claim.** The infrastructure at Lamoka Lake functioned as a costly signal, a display of group capacity designed to advertise quality to potential partners or rivals, similar to the framework used for Rapa Nui and Poverty Point.

**Predictions:**
- Infrastructure should exceed utilitarian need (over-investment as display)
- Construction should be visible and impressive rather than purely functional
- Signal costs should be wasteful (honest signaling requires genuine sacrifice)
- Infrastructure should correlate with group quality indicators

**Overlap with aggregation economics:** Both predict aggregation and cooperative investment.

**Distinguishing tests:**
- Costly signaling predicts over-investment beyond practical need; economics predicts investment proportional to practical returns. Test: do storage pit volumes match estimated food storage needs, or exceed them substantially?
- Costly signaling predicts investment in visible features even without practical return; economics predicts all investment is utilitarian.
- If storage capacity approximately matches estimated food storage needs (~50,000 liters for ~300 people for ~3 months), the utilitarian interpretation is supported. If capacity vastly exceeds need, the costly signaling interpretation gains strength.

### 15.6 Alternative 6: Population Pressure Model

**Claim.** Growing population forced people together and compelled cooperative infrastructure investment. Aggregation was not a strategic choice but a demographic necessity.

**Predictions:**
- Population growth should precede aggregation intensification
- Infrastructure investment should correlate with population size, not environmental variability
- Abandonment should correlate with population decline
- Aggregation should be involuntary (no strategic choice component)

**Overlap with aggregation economics:** Both recognize that aggregation involves multiple bands.

**Distinguishing tests:**
- Population pressure predicts infrastructure scaling with population; economics predicts scaling with aggregation frequency x size x duration (H2 distinguishes).
- Population pressure does not predict environmental variability correlation (H4 distinguishes).
- Population pressure predicts abandonment from population decline; economics predicts abandonment from environmental stabilization (H7 distinguishes).
- Regional population estimates for the Late Archaic Finger Lakes (~500 people in ~25 bands) suggest densities well below carrying capacity, weakening the population pressure argument.

---

## 16. A Discrimination Protocol

### 16.1 Which Predictions Are Shared vs. Unique?

**Table 16.1. Prediction overlap across hypotheses.**

| Prediction | Agg. Econ. | Trade | Ritual | Aggrandizer | Abundance | Signal | Pop. Pressure |
|-----------|:----------:|:-----:|:------:|:-----------:|:---------:|:------:|:-------------:|
| H1: Fall seasonality | X | ? | ? | ? | X | X | X |
| H2: Storage scaling | X | | | | | | |
| H3: Ecotone site selection | X | | | | | | |
| H4: Env. variability correlation | X | | | | | | |
| H5: Regional hierarchy | X | X | X | X | ? | X | ? |
| H6: Exchange concentration | X | X | ? | X | | X | |
| H7: Abandonment under stabilization | X | | | | | | |

**X** = predicted; **?** = partially or conditionally predicted; blank = not predicted.

### 16.2 Strongest Discriminators

**H7 (abandonment under stabilization)** is the single strongest discriminator. It is predicted only by the aggregation economics model and is actively contradicted by most alternatives (which predict abandonment from deterioration, not stabilization). If you can demonstrate that Lamoka Lake's terminal occupation coincided with decreased climate variability, this provides strong support for the economic model and falsifies the abundance, population pressure, and simple deterioration explanations.

**H4 (environmental variability correlation)** is the second strongest. Only the aggregation economics model predicts that site use intensity should track environmental *variability* rather than mean conditions. The abundance model predicts tracking with mean conditions; the trade and ceremonial models predict no environmental relationship.

**H3 (ecotone site selection)** is the third strongest. Only the aggregation economics model generates a spatial prediction linking site selection to ecological diversity. This is also the cheapest to test (GIS analysis with existing site data).

### 16.3 Recommended Test Sequence

Start with the cheapest and most discriminating tests:

**Round 1 (lowest cost, highest discrimination):**

1. **H3: Ecotone site selection.** GIS analysis of site locations vs. ecological diversity. Cost: labor + software (~$2,000-5,000). If ecotone diversity does NOT correlate with storage density, the model is in trouble.

2. **H5: Regional site hierarchy.** Compile storage feature data from published site reports. Cost: labor (~$2,000-3,000). If the distribution is NOT skewed, the model's prediction of site primacy is wrong.

3. **H6: Exchange concentration.** Compare non-local artifact frequencies across site types using existing collection data. Cost: labor + collections access (~$3,000-5,000). If exchange goods are NOT concentrated at Lamoka Lake, the aggregation interpretation is weakened.

**Round 2 (moderate cost, moderate discrimination):**

4. **H1: Fall seasonality.** Faunal seasonality analysis from curated collections. Cost: ~$5,000-10,000. If the site was NOT primarily a fall occupation, the timing predictions fail.

5. **H2: Storage scaling.** AMS dating of storage pit construction sequence. Cost: ~$6,000-15,000. If pit construction does NOT cluster in the core occupation period, the scaling prediction fails.

**Round 3 (highest cost, strongest discrimination):**

6. **H4: Environmental variability.** Paleoclimate proxy analysis. Cost: ~$15,000-25,000 for new cores; less if existing data can be compiled. If aggregation intensity does NOT correlate with climate variability, the threshold mechanism is not supported.

7. **H7: Abandonment conditions.** Requires both precise terminal chronology and high-resolution paleoclimate record. Cost: combined with H4 work. If abandonment correlates with *increased* variability rather than stabilization, the model is falsified.

### 16.4 Decision Tree for Interpreting Results

```
                    Does H3 hold?
                   (ecotone correlation)
                   /              \
                 Yes               No
                  |                 |
           Does H4 hold?     Model likely wrong.
        (variability correlation)  Consider abundance
               /       \          or trade models.
             Yes        No
              |          |
        Does H7 hold?   Partial support only.
     (abandon under     Threshold mechanism
      stabilization)    questionable.
           /    \       Consider modified
         Yes     No     model or alternatives.
          |       |
     STRONG      MODERATE
     SUPPORT     SUPPORT
     for model   (H7 is hardest
                  to test; partial
                  support still
                  meaningful)
```

---

## 17. Practical Dissertation Roadmap

### 17.1 Year 1: Compile Existing Data, Run Preliminary Tests

**Semester 1 (Fall)**
- Literature review: Lamoka Lake, Finger Lakes Late Archaic, aggregation theory
- Compile existing site database from NYS OPRHP CRIS and published reports
- Begin GIS analysis for H3 (ecotone site selection)
- Access curated collections at RMSC and NYSM
- Identify available paleoclimate data for the Finger Lakes region

**Semester 2 (Spring)**
- Complete H3 test (GIS ecotone analysis)
- Complete H5 test (regional site hierarchy from existing data)
- Begin H6 test (exchange goods comparison from existing collection data)
- Draft literature review and methods chapters
- Prepare grant applications for Year 2 fieldwork and analysis

**Key deliverable:** Preliminary results from H3, H5, H6 (the cheapest tests). These results determine whether the model survives initial screening. If H3 fails decisively (no ecotone correlation), you may need to revise the model or pivot to an alternative framework.

### 17.2 Year 2: Generate New Data

**Semester 3 (Fall)**
- Submit samples for AMS dating (H2: storage scaling chronology)
- Begin faunal reanalysis from curated collections (H1: seasonality)
- If feasible: arrange paleoclimate core extraction from Lamoka Lake or adjacent water body (H4, H7)
- Begin lithic sourcing analysis (H6: exchange goods)

**Semester 4 (Spring)**
- Receive and analyze AMS dates (H2)
- Complete faunal seasonality analysis (H1)
- Process and analyze paleoclimate core (H4, H7) or compile existing proxy data
- Complete lithic sourcing analysis (H6)
- Begin data integration and model parameter refinement

**Key deliverable:** New data for H1, H2, and H6. Paleoclimate data for H4 and H7 (may extend into Year 3 depending on core processing time).

### 17.3 Year 3: Test Remaining Hypotheses, Write Up

**Semester 5 (Fall)**
- Complete H4 test (environmental variability correlation)
- Complete H7 test (abandonment conditions) if paleoclimate data are available
- Run updated simulations with refined parameter estimates
- Begin writing results and discussion chapters

**Semester 6 (Spring)**
- Complete dissertation writing
- Address alternative hypotheses (Section 15) in discussion
- Present results at SAA or ESAF conference
- Defend

### 17.4 Collaborations Needed

| Expertise | Why needed | Potential contacts |
|-----------|-----------|-------------------|
| Paleoecologist | Pollen/sediment core analysis | Cornell, Syracuse, or Binghamton Earth Sciences |
| Zooarchaeologist | Faunal seasonality analysis | Specialist in eastern North America fauna |
| Paleoethnobotanist | Storage pit contents analysis | Northeast specialist |
| GIS specialist | Ecological zone mapping | Geography department |
| Archaeometry | Lithic sourcing (XRF/LA-ICP-MS) | University archaeometry lab |
| Statistician | Bayesian radiocarbon modeling | Specialist in OxCal or similar |

### 17.5 Budget Considerations

**Table 17.1. Estimated costs by data class.**

| Item | Estimated cost | Priority |
|------|---------------|----------|
| GIS analysis (H3, H5) | $2,000-5,000 | Year 1, high priority |
| Collections access and travel | $3,000-5,000 | Years 1-2 |
| AMS dating (20-30 dates) | $6,000-15,000 | Year 2, high priority |
| Faunal reanalysis (H1) | $5,000-10,000 | Year 2, moderate priority |
| Paleoclimate core (H4, H7) | $15,000-25,000 | Year 2, high priority |
| Lithic sourcing (H6) | $5,000-10,000 | Year 2, moderate priority |
| Botanical analysis | $3,000-5,000 | Year 2, moderate priority |
| **Total estimated** | **$39,000-75,000** | |

**Funding sources to consider:**
- NSF Doctoral Dissertation Research Improvement (DDRI) grant (~$20,000-25,000)
- Wenner-Gren Dissertation Fieldwork Grant (~$25,000)
- SAA Student Research Award
- University dissertation research funds
- State humanities council grants (NY Council on the Humanities)

---

## 18. Conclusion

This guide has walked through the complete mathematical framework behind the Lamoka Lake aggregation economics model, from the Price equation foundations through the critical threshold derivation to the seven testable predictions and a practical research design.

The core insight is simple: seasonal aggregation at a productive ecotone becomes adaptive when environmental variability is high enough that the insurance value of cooperation, ecotone buffering, stored surplus, and reciprocal obligations exceeds the costs of travel, infrastructure investment, and foregone foraging. The math formalizes this intuition into a single number, $\sigma^* \approx 0.306$, that makes a precise, testable prediction.

What makes this framework valuable for a dissertation is that it generates specific, falsifiable predictions that can be evaluated with archaeological and environmental data. The seven hypotheses (H1-H7) are not vague directional claims ("aggregation should relate to environment") but precise statements about what patterns should exist in the record *if* the model is correct and *should not* exist if it is wrong. The strongest discriminators, H7 (abandonment under stabilization), H4 (variability correlation), and H3 (ecotone selection), collectively test the core mechanism of the model and distinguish it from five alternative hypotheses.

A successful dissertation would not merely confirm or reject the model. It would:

1. Provide independent estimates of model parameters ($\sigma$, $\varepsilon$, covariance structure) from empirical data
2. Test each prediction against evidence, honestly reporting both confirmations and failures
3. Evaluate alternative hypotheses with the same data
4. Refine the model based on findings, potentially revising parameter values or identifying mechanisms that the current model misses
5. Identify which aspects of the Lamoka Lake record are well-explained by the economic model and which require additional or alternative explanation

The model is a tool for structuring inquiry, not a final answer. Its value lies not in being "right" but in being specific enough to be tested, refined, or rejected based on evidence. That is what formal models offer that verbal interpretations cannot: precision sufficient for empirical engagement.

A final word of practical advice: a dissertation committee will value intellectual honesty over confirmation. If your data falsify one or more predictions, that is a contribution, not a failure. Models are most useful when they are wrong in informative ways, because the pattern of failure tells us which assumptions need revision. The strongest possible dissertation outcome is not "the model was right about everything" but rather "here is what the model got right, here is what it got wrong, and here is what the failures tell us about the actual processes at work at Lamoka Lake."

---

## References

Binford, L.R. 1980. Willow smoke and dogs' tails: Hunter-gatherer settlement systems and archaeological site formation. *American Antiquity* 45(1):4-20.

Binford, L.R. 2001. *Constructing Frames of Reference: An Analytical Method for Archaeological Theory Building Using Ethnographic and Environmental Data Sets*. University of California Press.

Bliege Bird, R. and Smith, E.A. 2005. Signaling theory, strategic interaction, and symbolic capital. *Current Anthropology* 46(2):221-248.

Cleland, C.E. 1982. The inland shore fishery of the northern Great Lakes: Its development and importance in prehistory. *American Antiquity* 47(4):761-784.

Conkey, M.W. 1980. The identification of prehistoric hunter-gatherer aggregation sites: The case of Altamira. *Current Anthropology* 21(5):609-630.

DeBoer, W.R. 1988. Subterranean storage and the organization of surplus: The view from eastern North America. *Southeastern Archaeology* 7(1):1-20.

Funk, R.E. 1988. The Laurentian concept: A review. *Archaeology of Eastern North America* 16:1-42.

Gibson, J.L. 2000. *The Ancient Mounds of Poverty Point: Place of Rings*. University Press of Florida.

Grafen, A. 1990. Biological signals as handicaps. *Journal of Theoretical Biology* 144(4):517-546.

Hunt, T.L. and Lipo, C.P. 2011. *The Statues that Walked: Unraveling the Mystery of Easter Island*. Free Press.

Kelly, R.L. 2013. *The Lifeways of Hunter-Gatherers: The Foraging Spectrum*. Cambridge University Press.

Koenig, W.D. and Knops, J.M.H. 2000. Patterns of annual seed production by northern hemisphere trees: A global perspective. *American Naturalist* 155(1):59-69.

Kidder, T.R., Ortmann, A.L. and Arco, L.J. 2008. Poverty Point and the archaeology of singularity. *SAA Archaeological Record* 8(5):9-12.

Price, G.R. 1970. Selection and covariance. *Nature* 227:520-521.

Price, G.R. 1972. Extension of covariance selection mathematics. *Annals of Human Genetics* 35(4):485-490.

Ritchie, W.A. 1932. The Lamoka Lake site: The type station of the Archaic Algonkin period in New York. *Researches and Transactions of the New York State Archaeological Association* 7(4):79-134.

Ritchie, W.A. 1969. *The Archaeology of New York State*. Natural History Press, Garden City, New York.

Sassaman, K.E. 2005. Poverty Point as structure, event, process. *Journal of Archaeological Method and Theory* 12(4):335-364.

Silvertown, J.W. 1980. The evolutionary ecology of mast seeding in trees. *Biological Journal of the Linnean Society* 14(2):235-250.

Suttles, W. 1968. Coping with abundance: Subsistence on the Northwest Coast. In Lee, R.B. and DeVore, I. (eds.), *Man the Hunter*, pp. 56-68. Aldine, Chicago.

Wandsnider, L. 1997. The roasted and the boiled: Food composition and heat treatment with special emphasis on pit-hearth cooking. *Journal of Anthropological Archaeology* 16(1):1-48.

Whitelaw, T. 1991. Some dimensions of variability in the social organization of community space among foragers. In Gamble, C.S. and Boismier, W.A. (eds.), *Ethnoarchaeological Approaches to Mobile Campsites*, pp. 139-188. International Monographs in Prehistory, Ann Arbor.

Wiessner, P. 2002. Hunting, healing, and hxaro exchange: A long-term perspective on !Kung (Ju/'hoansi) large-game hunting. *Evolution and Human Behavior* 23(6):407-436.

Winterhalder, B. 1986. Diet choice, risk, and food sharing in a stochastic environment. *Journal of Anthropological Archaeology* 5(4):369-392.

Zahavi, A. 1975. Mate selection: A selection for a handicap. *Journal of Theoretical Biology* 53(1):205-214.

---

## Appendix A: Step-by-Step Algebra for the $\sigma^*$ Derivation

This appendix presents the complete derivation of the critical threshold $\sigma^*$ in maximum detail, showing every algebraic step.

### A.1 Starting Point: The Full Fitness Equations

**Aggregator fitness:**

$$W_{\text{agg}} = (1 - C_{\text{total}}) \cdot (1 - \alpha_{\text{eff}} \cdot \sigma) \cdot f(n) \cdot (1 + B_{\text{recip}})$$

**Independent fitness:**

$$W_{\text{ind}} = R_{\text{ind}} \cdot (1 - \beta \cdot \sigma)$$

### A.2 Define the Composite Cooperation Term

To simplify notation, define:

$$A = (1 - C_{\text{total}}) \cdot f(n) \cdot (1 + B_{\text{recip}})$$

This term bundles together all the "static" (non-$\sigma$-dependent) advantages and disadvantages of cooperation:
- $(1 - C_{\text{total}})$: fitness remaining after paying costs
- $f(n)$: cooperation returns from group size
- $(1 + B_{\text{recip}})$: reciprocal obligation benefits

With this substitution, the aggregator fitness simplifies to:

$$W_{\text{agg}} = A \cdot (1 - \alpha_{\text{eff}} \cdot \sigma)$$

### A.3 Set Equal at the Threshold

At $\sigma = \sigma^*$, both strategies yield equal fitness:

$$A \cdot (1 - \alpha_{\text{eff}} \cdot \sigma^*) = R_{\text{ind}} \cdot (1 - \beta \cdot \sigma^*)$$

### A.4 Expand Both Sides

Left side:
$$A - A \cdot \alpha_{\text{eff}} \cdot \sigma^*$$

Right side:
$$R_{\text{ind}} - R_{\text{ind}} \cdot \beta \cdot \sigma^*$$

Full equation:
$$A - A \cdot \alpha_{\text{eff}} \cdot \sigma^* = R_{\text{ind}} - R_{\text{ind}} \cdot \beta \cdot \sigma^*$$

### A.5 Move All $\sigma^*$ Terms to One Side

Add $R_{\text{ind}} \cdot \beta \cdot \sigma^*$ to both sides:
$$A - A \cdot \alpha_{\text{eff}} \cdot \sigma^* + R_{\text{ind}} \cdot \beta \cdot \sigma^* = R_{\text{ind}}$$

Subtract $A$ from both sides:
$$R_{\text{ind}} \cdot \beta \cdot \sigma^* - A \cdot \alpha_{\text{eff}} \cdot \sigma^* = R_{\text{ind}} - A$$

### A.6 Factor Out $\sigma^*$

$$\sigma^* \cdot (R_{\text{ind}} \cdot \beta - A \cdot \alpha_{\text{eff}}) = R_{\text{ind}} - A$$

### A.7 Solve for $\sigma^*$

$$\sigma^* = \frac{R_{\text{ind}} - A}{R_{\text{ind}} \cdot \beta - A \cdot \alpha_{\text{eff}}}$$

### A.8 Substitute Back the Definition of $A$

$$\sigma^* = \frac{R_{\text{ind}} - (1 - C_{\text{total}}) \cdot f(n) \cdot (1 + B_{\text{recip}})}{R_{\text{ind}} \cdot \beta - (1 - C_{\text{total}}) \cdot f(n) \cdot (1 + B_{\text{recip}}) \cdot \alpha \cdot (1 - \varepsilon)}$$

### A.9 Worked Example: Lamoka Lake

**Given values:**
- $C_{\text{total}} = 0.30$
- $f(12) = 1 + 0.10 \times \ln(12) = 1 + 0.10 \times 2.485 = 1.249$
- $B_{\text{recip}} = 0.05$
- $R_{\text{ind}} = 1.08$
- $\alpha = 0.35$
- $\beta = 0.70$
- $\varepsilon = 0.30$

**Step 1:** Calculate $A$:
$$A = (1 - 0.30) \times 1.249 \times (1 + 0.05) = 0.70 \times 1.249 \times 1.05 = 0.918$$

**Step 2:** Calculate $\alpha_{\text{eff}}$:
$$\alpha_{\text{eff}} = 0.35 \times (1 - 0.30) = 0.35 \times 0.70 = 0.245$$

**Step 3:** Calculate numerator:
$$R_{\text{ind}} - A = 1.08 - 0.918 = 0.162$$

**Step 4:** Calculate denominator:
$$R_{\text{ind}} \cdot \beta - A \cdot \alpha_{\text{eff}} = 1.08 \times 0.70 - 0.918 \times 0.245 = 0.756 - 0.225 = 0.531$$

**Step 5:** Calculate $\sigma^*$:
$$\sigma^* = \frac{0.162}{0.531} = 0.305$$

**Result:** $\sigma^* \approx 0.305$ for Lamoka Lake.

### A.10 Verification Against Code

The `parameters.py` implementation in the Lamoka Lake codebase calculates:

```python
def critical_threshold(epsilon, n, params):
    C_total = params.costs.C_total          # 0.30
    f_n = cooperation_benefit(n, params.cooperation)  # 1.249
    recip = 1.0 + params.cooperation.B_recip          # 1.05
    R_ind = params.cooperation.R_ind                    # 1.08
    A = (1.0 - C_total) * f_n * recip                  # 0.918
    alpha_eff = params.vulnerability.alpha_agg * (1.0 - epsilon)  # 0.245
    denom = R_ind * params.vulnerability.beta_ind - A * alpha_eff # 0.531
    numerator = R_ind - A                               # 0.162
    sigma_star = numerator / denom                      # 0.305
    return sigma_star
```

The analytical derivation reproduces the code output exactly.

---

## Appendix B: Complete Parameter Table with Estimation Methods

**Table B.1. Complete parameters for Lamoka Lake with estimation methods.**

| Parameter | Symbol | Value | Range | Estimation method | Data source |
|-----------|--------|-------|-------|-------------------|-------------|
| **Environmental** | | | | | |
| Regional uncertainty | $\sigma$ | 0.45 | 0.35-0.45 | CV of annual resource returns | Pollen cores, lake sediments, mast variability data |
| Ecotone advantage | $\varepsilon$ | 0.30 | 0.20-0.35 | Portfolio theory from zone covariances | GIS zone mapping + modern/paleo covariance data |
| **Vulnerability** | | | | | |
| Aggregator vulnerability | $\alpha$ | 0.35 | 0.10-0.50 | Mortality rate under shortfall with buffering | Faunal diversity, storage capacity, ethnographic analogs |
| Independent vulnerability | $\beta$ | 0.70 | 0.50-0.95 | Mortality rate under shortfall without buffering | Single-zone failure rates, modern ecological data |
| **Costs** | | | | | |
| Travel cost | $C_{\text{travel}}$ | 0.08 | 0.00-0.20 | Distance/caloric cost ratio | Catchment analysis, lithic sourcing distances |
| Infrastructure cost | $C_{\text{infrastructure}}$ | 0.12 | 0.00-0.25 | Labor hours / total productive hours | Pit volume x construction time, weir maintenance |
| Opportunity cost | $C_{\text{opportunity}}$ | 0.10 | 0.00-0.20 | Foregone foraging value | Seasonal resource comparison, home range vs. site |
| Total cost | $C_{\text{total}}$ | 0.30 | 0.00-1.00 | Sum of components | Sum of above |
| Independent advantage | $R_{\text{ind}}$ | 1.08 | 0.90-1.60 | Baseline fitness advantage from avoiding cooperation costs at $\sigma = 0$ | Ethnographic comparison of time allocation with/without cooperation obligations |
| **Cooperation** | | | | | |
| Benefit coefficient | $b$ | 0.10 | 0.02-0.15 | Returns to scale in communal processing | Ethnographic communal fishing/processing data |
| Optimal group size | $n^*$ | 12 | 3-30 | Site capacity | Site area, ethnographic floor area requirements |
| Crowding coefficient | $c$ | 0.025 | 0.005-0.030 | Resource depletion rate above optimal | Central-place foraging models |
| Reciprocal benefit | $B_{\text{recip}}$ | 0.05 | 0.00-0.15 | Insurance value of social networks | Exchange goods frequency, burial patterns |
| **Conflict** | | | | | |
| Baseline mortality | $m_0$ | 0.00 | 0.05-0.25 | Not applicable (aggregation system) | -- |
| Conflict reduction | $r$ | 0.00 | 0.50-0.90 | Not applicable (aggregation system) | -- |
| **Output** | | | | | |
| Critical threshold | $\sigma^*$ | 0.305 | -- | Derived from above | -- |

---

## Appendix C: Summary of Alternative Hypothesis Predictions

**Table C.1. Predictions by hypothesis.**

| Prediction | Aggregation Economics | Trade Center | Ritual | Aggrandizer | Abundance | Costly Signaling | Population Pressure |
|-----------|:--------------------:|:------------:|:------:|:-----------:|:---------:|:----------------:|:-------------------:|
| **H1**: Fall seasonality | Yes | Maybe | Maybe | Maybe | Yes | Yes | Yes |
| **H2**: Storage scales with agg. size x frequency x duration | Yes | No | No | No | No | No | No |
| **H3**: Ecotone-driven site selection | Yes | No | No | No | No | No | No |
| **H4**: Env. variability correlates with agg. intensity | Yes | No | No | No | No (predicts mean, not variance) | No | No |
| **H5**: Strongly skewed regional hierarchy | Yes | Yes | Yes | Yes | Maybe | Yes | Maybe |
| **H6**: Exchange goods concentrated at agg. site | Yes | Yes | Maybe | Yes | No | Yes | No |
| **H7**: Abandonment under environmental stabilization | Yes | No | No | No | No (predicts opposite) | No | No |

**Unique predictions of the aggregation economics model:**
- H2 (storage scaling): Only the economics model predicts the specific relationship between aggregation parameters and infrastructure accumulation.
- H3 (ecotone selection): Only the economics model generates a spatial prediction linking site location to ecological diversity.
- H4 (variability correlation): Only the economics model predicts that site use intensity tracks environmental *variability* rather than mean conditions.
- H7 (abandonment under stabilization): Only the economics model predicts the counterintuitive result that environmental improvement causes system collapse.

**Most discriminating single test:** H7. If abandonment correlates with stabilization rather than deterioration, this simultaneously confirms the economics model and falsifies the abundance, population pressure, and simple deterioration explanations.

**Most cost-effective initial test:** H3. GIS analysis of existing site data against ecological zone diversity can be done with minimal cost and provides strong discrimination between the economics model and most alternatives.
