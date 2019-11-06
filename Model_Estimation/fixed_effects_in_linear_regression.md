---
title: Fixed Effects in Linear Regression
parent: Model Estimation
has_children: false
mathjax: true
nav_order: 1
---

# Fixed Effects in Linear Regression

Fixed effects is a statistical regression model in which the intercept of the regression model is allowed to vary freely across individuals or groups. It is often applied to panel data in order to control for any individual-specific attributes that do not vary across time.

For more information, see [Wikipedia: Fixed Effects Model](https://en.wikipedia.org/wiki/Fixed_effects_model).

## Keep in Mind

- To use individual-level fixed effects, you must observe the same person multiple times (panel data).
- In a linear regression context, fixed effects regression is relatively straightforward, and can be thought of as effectively adding a binary control variable for each individual, or subtracting the within-individual mean of each variable (the "within" estimator). However, you may want to apply fixed effects to other models like logit or probit. This is usually possible (depending on the model), but if you just add a set of binary controls or subtract within-individual means, it won't work very well. Instead, look for a command specifically designed to implement fixed effects for that model.
- If you are using fixed effects to estimate the causal effect of a variable $$X$$, individuals with more variance in $$X$$ will be weighted more heavily (Gibbons, Serrano, & Urbancic 2019, ungated copy [here](http://gibbons.bio/docs/bfe.pdf). You may want to consider weighting your regression by the inverse within-individual variance of $$X$$.

## Also Consider

- [Random effects](https://lost-stats.github.io/Model_Estimation/random_effects.html)
- You may want to consider [clustering your standard errors](https://lost-stats.github.io/Model_Estimation/cluster_robust_standard_errors.html) at the same level as your fixed effects.

# Implementations

## R

We will demonstrate fixed effects using `felm` from the `lfe` package. You may also want to consider `lm_robust` from the `estimatr` package. The syntax for the latter is easier, but it is less efficient.

`felm` uses the Method of Alternating Projections to "sweep out" the fixed effects and avoid estimating them directly.

```r
# If necessary, install lfe
# install.packages('lfe')
library(lfe)

# Read in data from the College Scorecard
df <- read.csv('https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Estimation/Data/Fixed_Effects_in_Linear_Regression/Scorecard.csv')
# Calculate proportion of graduates working
df$prop_working <- df$count_working/(df$count_working + df$count_not_working)

# A felm formula is constructed as:
# outcome ~
# covariates |
# fixed effects |
# instrumental variables specification | 
# cluster variables for standard errors

# Here let's regress earnings_med on prop_working
# with institution name and year as our fixed effects
# And clusters for institution name
fe_model <- felm(earnings_med ~ prop_working | inst_name + year | 0 | inst_name, data = df)

# Look at our results
summary(fe_model)
```

## Stata

We will estimate fixed effects in two ways: using the built in `xtreg`, and `reghdfe`, which is more efficient and better handles multiple levels of fixed effects, but must be downloaded.

```stata
* Install regdhfe if necessary
* ssc install reghdfe

* Load in College Scorecard data
import delimited "https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Estimation/Data/Fixed_Effects_in_Linear_Regression/Scorecard.csv", clear

* The missings are written as "NA", let's turn this numeric
destring count_not_working count_working earnings_med, replace force
* Calculate the proportion working
g prop_working = count_working/(count_working + count_not_working)

* xtset requires that the individual identifier be a numeric variable
encode inst_name, g(name_number)

* Set the data as panel data with xtset
xtset name_number

* Use xtreg with the "fe" option to run fixed effects
* Regressing earnings_med on prop_working
* with fixed effects for name_number (implied by fe)
* and also year (which we'll add manually with i.year)
* and standard errors clustered by name_number
xtreg earnings_med prop_working i.year, fe vce(cluster name_number)

* For reghdfe we don't need to xtset the data. Let's undo that
xtset, clear

* We specify both sets of fixed effects in absorb()
reghdfe earnings_med prop_working, absorb(name_number year) vce(cluster inst_name)
```
