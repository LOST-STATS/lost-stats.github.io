---
title: Cluster-Robust Standard Errors
parent: Nonstandard Errors
grand_parent: Statistical Inference ## Optional for indexing
nav_order: 1
---

# Cluster-Robust Standard Errors (a.k.a. Clustered Standard Errors)

Data is considered to be clustered when there are subsamples within the data that are related to each other. For example, if you had data on test scores in a school, those scores might be correlated within classroom because classrooms share the same teacher. When *error terms* are correlated within clusters but independent across clusters, then regular standard errors, which assume independence between all observations, will be incorrect. Cluster-robust standard errors are designed to allow for correlation between observations within cluster. For more information, see [A Practitioner's Guide to Cluster-Robust Inference](http://cameron.econ.ucdavis.edu/research/Cameron_Miller_JHR_2015_February.pdf).

## Keep in Mind

- Just because there are likely to be clusters in your data is not necessarily a good justification for using cluster-robust inference. Generally, clustering is advised only if either sampling or treatment assignment is performed at the level of the clusters. See [Abadie, Athey, Imbens, & Wooldridge (2017)](https://arxiv.org/abs/1710.02926), or [this simple summary](https://blogs.worldbank.org/impactevaluations/when-should-you-cluster-standard-errors-new-wisdom-econometrics-oracle) of the paper.
- There are multiple kinds of cluster-robust standard errors, for example CR0, CR1, and CR2. Check in to the kind available to you in the commands you're using.

## Also Consider

- [Cluster Bootstrap Standard Errors](https://lost-stats.github.io/Model_Estimation/cluster_bootstrap_standard_errors.html), which are another way of performing cluster-robust inference that will work even outside of a standard regression context.

# Implementations

**Note:** Clustering of standard errors is especially common in panel models, such as [linear fixed effects](https://lost-stats.github.io/Model_Estimation/fixed_effects_in_linear_regression.html). For this reason, software routines for these particular models typically offer built-in support for (multiway) clustering. The implementation pages for these models should be hyperlinked in the relevant places below. Here, we instead concentrate on providing implementation guidelines for clustering in general.

## Julia

For cluster-robust estimation of (high-dimensional) fixed effect models in Julia, see [here](https://lost-stats.github.io/Model_Estimation/fixed_effects_in_linear_regression.html#julia).

## R

For cluster-robust estimation of (high-dimensional) fixed effect models in R, see [here](https://lost-stats.github.io/Model_Estimation/fixed_effects_in_linear_regression.html#r).

Cluster-robust standard errors for many different kinds of regression objects in R can be obtained using the `coeftest` function in the **lmtest** package combined with the `vcovCL` function in the **sandwich** package. Alternately, while it does not handle as many types of regressions, the `lm_robust` function in **estimatr** can provide cluster-robust standard errors much more easily.

```R
# If necessary, install lmtest, sandwich, and estimatr
# install.packages(c('lmtest','sandwich','estimatr'))

# Read in data from the College Scorecard
df <- read.csv('https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Estimation/Data/Fixed_Effects_in_Linear_Regression/Scorecard.csv')

# Get robust errors using vcovCL and lmtest
library(lmtest)
library(sandwich)

# Create a regression model without cluster-robust standard errors
my_model <- lm(repay_rate ~ earnings_med + state_abbr, data = df)

# Put the model into vcovCL() to get a robust covariance matrix
# and then put that in lmtest() to get the regression results with robust errors
# Pick the kind of robust errors with "type" 
# It refers to the heteroskedasticity-consistent error types.
# HC1 is the default but I've specified it here anyway
coeftest(my_model, vcov = vcovCL(my_model, 
                                 cluster = df$inst_name,
                                 type = "HC1"))

# Alternately, just use lm_robust. 
# Standard error types are referred to as CR0, CR1 ("stata"), CR2 here.
# Here, CR2 is the default
library(estimatr)
my_model2 <- lm_robust(repay_rate ~ earnings_med + state_abbr, data = df,
						clusters = inst_name,
                       se_type = "stata")
summary(my_model2)
```

## Stata

Stata has clustered standard errors built into most regression commands, and they generally work the same way for all commands.

```stata
* Load in College Scorecard data
import delimited "https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Model_Estimation/Data/Fixed_Effects_in_Linear_Regression/Scorecard.csv", clear

* The missings are written as "NA", let's turn this numeric
destring earnings_med repay_rate, replace force

* If we want to cluster on a variable or include it as a factor it must not be a string
encode inst_name, g(inst_name_encoded)
encode state_abbr, g(state_encoded)

* Just add vce(cluster) to the options of the regression
* This will give you CR1
regress repay_rate earnings_med i.state_encoded, vce(cluster inst_name_encoded)
```
