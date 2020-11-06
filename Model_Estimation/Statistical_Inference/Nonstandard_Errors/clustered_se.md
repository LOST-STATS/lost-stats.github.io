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

- [Cluster Bootstrap Standard Errors]({{ "/Model_Estimation/Statistical_Inference/Nonstandard_Errors/cluster_bootstrap_standard_errors.html" | relative_url }}), which are another way of performing cluster-robust inference that will work even outside of a standard regression context.

# Implementations

**Note:** Clustering of standard errors is especially common in panel models, such as [linear fixed effects]({{ "/Model_Estimation/OLS/fixed_effects_in_linear_regression.html" | relative_url }}). For this reason, software routines for these particular models typically offer built-in support for (multiway) clustering. The implementation pages for these models should be hyperlinked in the relevant places below. Here, we instead concentrate on providing implementation guidelines for clustering in general.

## Julia

For cluster-robust estimation of (high-dimensional) fixed effect models in Julia, see [here]({{ "/Model_Estimation/OLS/fixed_effects_in_linear_regression.html#julia" | relative_url }}).

## R

For cluster-robust estimation of (high-dimensional) fixed effect models in R, see [here]({{ "/Model_Estimation/OLS/fixed_effects_in_linear_regression.html#r" | relative_url }}). Note that these methods can easily be re-purposed to run and cluster standard errors of non-panel models; just omit the fixed-effects in the model call. But for this page we'll focus on some additional methods.

Cluster-robust standard errors for many different kinds of regression objects in R can be obtained using the `vcovCL` or `vcovBS` functions from the **sandwich** package ([link](http://sandwich.r-forge.r-project.org/index.html)). To perform statistical inference, we combine these with the `coeftest` function from the **lmtest** package. This approach allows users to adjust the standard errors for a model "[on-the-fly](https://grantmcdermott.com/better-way-adjust-SEs/)" (i.e. post-estimation) and is thus very flexible. 

```R
# If necessary, install lmtest, sandwich, and estimatr
# install.packages(c('lmtest','sandwich','estimatr'))

# Read in data from the College Scorecard
df <- read.csv('https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Model_Estimation/Data/Fixed_Effects_in_Linear_Regression/Scorecard.csv')

# Create a regression model with normal (iid) errors
my_model <- lm(repay_rate ~ earnings_med + state_abbr, data = df)

# Swap out cluster-robust errors post-estimation with coeftest::lmtest and sandwich::vcovCL 
library(lmtest)
library(sandwich)
coeftest(my_model, vcov = vcovCL(my_model, cluster = ~inst_name))
```

Alternately, users can specify clustered standard errors directly in the model call using the `lm_robust` function from the **estimatr** package ([link](https://github.com/DeclareDesign/estimatr)). This latter approach is very similar to how errors are clustered in Stata, for example.

```R
# Alternately, use estimator::lm_robust to specify clustered SEs in the original model call. 
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
import delimited "https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Model_Estimation/Data/Fixed_Effects_in_Linear_Regression/Scorecard.csv", clear

* The missings are written as "NA", let's turn this numeric
destring earnings_med repay_rate, replace force

* If we want to cluster on a variable or include it as a factor it must not be a string
encode inst_name, g(inst_name_encoded)
encode state_abbr, g(state_encoded)

* Just add vce(cluster) to the options of the regression
* This will give you CR1
regress repay_rate earnings_med i.state_encoded, vce(cluster inst_name_encoded)
```
