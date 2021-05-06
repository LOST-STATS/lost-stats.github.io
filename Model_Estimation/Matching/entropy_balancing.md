---
title: Entropy Balancing
parent: Matching
grand_parent: Model Estimation
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Entropy Balancing

Entropy balancing is a method for matching treatment and control observations that comes from [Hainmueller (2012)](https://www.jstor.org/stable/41403737). It constructs a set of matching weights that, by design, forces certain balance metrics to hold. This means that, like with [Coarsened Exact Matching]({{ "/Model_Estimation/Matching/coarsened_exact_matching.html" | relative_url }}) there is no need to iterate on a matching model by performing the match, checking the balance, and trying different parameters to improve balance. However, unlike coarsened exact matching, entropy balancing does not require enormous data sets or drop large portions of the sample.

Entropy balancing requires a set of balance conditions to be provided. These are often of the form "the mean of matching variable $$A$$ must be the same between treated and control observations," i.e.

$$\sum_{i|D_i=0}w_iA_i = \sum_{i|D_i=1}A_i$$

where $$D_i$$ indicates treatment status and $$w_i$$ are the matching weights, and similarly for other variables for which the mean should match. However, other conditions can also be included, such as matching to equalize the variance of a matching variable, or the skewness, and so on. This is sort of like the [Generalized Method of Moments]({{ "/Model_Estimation/GLS/gmm.html" | relative_url }})

Then, the entropy balancing algorithm searches for a set of matching weights $w_i$ that best satisfies the set of balance conditions. These matching weights can then be used to weight an analysis comparing the treated and control groups to remove measured confounding between them.

## Keep in Mind

- You must specify all the conditions you would like to match on. Adding more and more conditions may improve the amount of balance, but also make it more likely that the match process will fail.

## Also Consider

- [Coarsened Exact Matching]({{ "/Model_Estimation/Matching/coarsened_exact_matching.html" | relative_url }})
- [Propensity Score Matching]({{ "/Model_Estimation/Matching/propensity_score_matching.html" | relative_url }})
- [Nearest-Neighbor Matching]({{ "/Model_Estimation/Matching/propensity_score_matching.html" | relative_url }})

# Implementations

These examples use data from [Broockman (2013)](https://onlinelibrary.wiley.com/doi/full/10.1111/ajps.12018).

## R

Entropy balancing can be implemented in R using the **ebal** package.

```r
# R CODE
library(ebal)
library(tidyverse)

br <- read_csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Model_Estimation/Matching/Data/broockman2013.csv")

# Outcome
Y <- br %>%
  pull(responded)
# Treatment
D <- br %>%
  pull(leg_black)
# Matching variables
X <- br %>%
  select(medianhhincom, blackpercent, leg_democrat) %>%
  # Add square terms to match variances if we like
  mutate(
    incsq = medianhhincom^2,
    bpsq = blackpercent^2
  ) %>%
  as.matrix()

eb <- ebalance(D, X)

# Get weights for usage elsewhere
# Noting that this contains only control weights
br_treat <- br %>%
  filter(leg_black == 1) %>%
  mutate(weights = 1)
br_con <- br %>%
  filter(leg_black == 0) %>%
  mutate(weights = eb$w)
br <- bind_rows(br_treat, br_con)

# Compare outcome (responded) between groups after matching
m <- lm(responded ~ leg_black, data = br, weights = weights)
summary(m)
```

## Stata

Entropy balancing can be implemented in Stata using the **ebalance** package.

```stata
* STATA CODE
* If necessary:
* ssc install ebalance

import delimited "https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Model_Estimation/Matching/Data/broockman2013.csv", clear

* Specify the treatment and matching variables
* And then in targets() specify which moments to match
* 1 for means, 2 for variances, 3 for skew
* Let's do means and variances for our continuous variables
* and just means for our binary matching variable (leg_democrat)
* and store the resulting weights in wt
ebalance leg_black medianhhincom blackpercent leg_democrat, targets(2 2 1) g(wt)

* Use pweight = wt to adjust estimates
reg responded leg_black [pw = wt]
```

