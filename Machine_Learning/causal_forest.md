---
title: Causal Forest
parent: Machine Learning
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Causal Forest

Causal forests are a causal inference learning method that are an extension of [Random Forests](https://lost-stats.github.io/Machine_Learning/random_forest.html). In random forests, the data is repeatedly split in order to minimize prediction error of an outcome variable. Causal forests are built similarly, except that instead of minimizing prediction error, data is split in order to maximize the difference across splits in the relationship between an outcome variable and a "treatment" variable. This is intended to uncover how treatment effects vary across a sample.

For more information, see [Explicitly Optimizing on Causal Effects via the Causal Forest](https://www.markhw.com/blog/causalforestintro).

## Keep in Mind

- Causal forests simply uncover heterogeneity in a causal effect, they do not by themselves make the effect causal. A standard causal forest must assume that the assignment to treatment is exogenous, as it might be in a randomized controlled trial. Some extensions of causal forest may allow for covariate adjustment or for instrumental variables. See your causal forest package's documentation to see if it has an option for ways of identifying the causal effect when treatment is not exogenous such as conditional adjustment or "instrumental forest".
- If using causal forest to estimate confidence intervals for the effects, in addition to the effects itself, it is recommended that you increase the number of trees generated considerably.

## Also Consider

- Your intuition for how causal forest works can be based on a thorough understanding of [Random Forests](https://lost-stats.github.io/Machine_Learning/random_forest.html), for which materials are much more widely available.

# Implementations

## R

The **grf** package has a `causal_forest` function that can be used to estimate causal forests. Additional functions afterwards can estimate, for example, the `average_treatment_effect()`. See `help(package='grf')` for more options.

```R
# If necessary
# install.packages('grf')
library(grf)

# Get crime data from North Carolina
df <- read.csv('https://vincentarelbundock.github.io/Rdatasets/csv/Ecdat/Crime.csv')

# It's not, but let's pretend that "percentage of young males" pctymle is exogenous
# and see how the effect of it on crmrte varies across the other measured covariates

# Make sure the data has no missing values. Here I'm dropping observations
# with missing values in any variable, but you can limit the data first to just
# variables used in analysis to only drop observations with missing values in those variables
df <- df[complete.cases(df),]

# Let's use training and holdout data
split <- sample(c(FALSE, TRUE), nrow(df), replace = TRUE)
df.train <- df[split,]
df.hold <- df[!split,]

# Isolate the "treatment" as a matrix
pctymle <- as.matrix(df.train$pctymle)

# Isolate the outcome as a matrix
crmrte <- as.matrix(df.train$crmrte)

# Use model.matrix to get our predictor matrix
# We might also consider adding interaction terms
X <- model.matrix(lm(crmrte ~ -1 + factor(year) + prbarr + prbconv + prbpris + 
                       avgsen + polpc + density + taxpc + factor(region) + factor(smsa) + 
                       pctmin + wcon, data = df.train))

# Estimate causal forest
cf <- causal_forest(X,crmrte,pctymle)

# Get predicted causal effects for each observation
effects <- predict(cf)$predictions

# And use holdout X's for prediction
X.hold <- model.matrix(lm(crmrte ~ -1 + factor(year) + prbarr + prbconv + prbpris + 
                       avgsen + polpc + density + taxpc + factor(region) + factor(smsa) + 
                       pctmin + wcon, data = df.hold))
# And get effects
effects.hold <- predict(cf, X.hold)$predictions

# Get standard errors for the holding data predictions - we probably should have set the num.trees
# option in causal_forest higher before doing this, perhaps to 5000.
SEs <- sqrt(predict(cf, X.hold, estimate.variance = TRUE)$variance.estimates)
```

