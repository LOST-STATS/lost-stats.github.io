---
title: Random/Mixed Effects in Linear Regression
parent: Multilevel Models
grand_parent: Model Estimation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Random/Mixed Effects in Linear Regression

In panel data, we often have to deal with unobserved heterogeneity among the units of observation that are observed over time. If we assume that the unobserved heterogeneity is uncorrelated with the independent variables, we can use random effects model. Otherwise, we may consider [fixed effects]({{ "/Model_Estimation/OLS/fixed_effects_in_linear_regression.html" | relative_url }}). In practice, random effects and fixed effects are often combined to implement a mixed effects model. Mixed refers to the fact that these models contain both fixed, and random effects.

For more information, see [Wikipedia: Random Effects Model](https://en.wikipedia.org/wiki/Random_effects_model)

## Keep in Mind

  - To use random effects model, you must observe the same person multiple times (panel data).
  - If unobserved heterogeneity is correlated with independent variables, the random effects estimator is biased and inconsistent.
  - However, even if unobserved heterogeneity is expected to be correlated with independent variables, the fixed effects model may have high standard errors if the number of observation per unit of observation is very small. Random effects maybe considered in such cases.
  - Additionally, modeling the correlation between the indepdendent variables and the random effect by using variables in predicting the random effect can account for this problem

## Also Consider

  - Consider [Fixed effects]({{ "/Model_Estimation/OLS/fixed_effects_in_linear_regression.html" | relative_url }})
    if unobserved heterogeneity and independent variables are correlated or if only within-variation is desired.
  - [Hauman Tests](https://en.wikipedia.org/wiki/Durbin%E2%80%93Wu%E2%80%93Hausman_test) are often used to inform us about the appropiateness of fixed effects models vs. random effects models in which only the intercept is random.
  - [Clustering your error]({{ "Model_Estimation/Statistical_Inference/Nonstandard_Errors/clustered_se.html" | relative_url }})

# Implementations

We continue from our the example in [Fixed effects]({{ "/Model_Estimation/OLS/fixed_effects_in_linear_regression.html" | relative_url }}). In that example we estimated a fixed effect model of the form:

$$ earnings_{it} = \beta_0 + \beta_1 prop\_ working_{it} + \delta_t + \delta_i + \epsilon_{it} $$

That is, average earnings of graduates of an institution depends on proportion employed, after controlling for time and institution fixed effects. But, some institutions have one observation, and the average number of observations is 5.1. We may be worried about the precision of our estimates. So, we may choose to use random effects for intercepts by institution to estimate the model even if we think $$corr(prop\_ working_{it}, \delta_{i}) \ne 0$$. That is, we choose possiblity of bias over variance.

## R

Several packages can be used to implement a random effects model in R - such as [**lme4**](https://cran.r-project.org/web/packages/lme4/index.html) and [**nlme**](https://cran.r-project.org/web/packages/nlme/nlme.pdf). **lme4** is more widely used. The example that follows uses the **lme4** package.

``` r
# If necessary, install lme4
if(!require(lme4)){install.packages("lme4")}
library(lme4)

# Read in data from the College Scorecard
df <- read.csv('https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Model_Estimation/Data/Fixed_Effects_in_Linear_Regression/Scorecard.csv')

# Calculate proportion of graduates working
df$prop_working <- df$count_working/(df$count_working + df$count_not_working)

# We write the mixed effect formula for estimation in lme4 as:
# dependent_var ~ 
# covariates (that can include fixed effects) + 
# random effects - we need to specify if our model is random effects in intercepts or in slopes. In our example, we suspect random effects in intercepts at institutions. So we write "...+(1 | inst_name), ...." If we wanted to specify a model where the coefficient on prop_working was also varying by institution - we would use (1 + open | inst_name).

# Here we regress average earnings graduates in an institution on prop_working, year fixed effects and random effects in intercepts for institutions.

relm_model <- lmer(earnings_med ~ prop_working + factor(df$year) + (1 | inst_name), data = df)

# Display results
summary(relm_model)

# We note that comparing with the fixed effects model, our estimates are more precise. But, the correlation between X`s and errors suggest bias in our mixed effect model, and we do see a large increase in estimated beta.
```

## Stata

We will estimate a mixed effects model using Stata using the built in `xtreg` command.

```stata

* Obtain same data from Fixed Effect tutorial
 
import delimited "https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Model_Estimation/Data/Fix
ed_Effects_in_Linear_Regression/Scorecard.csv", clear

* Data cleaning

* We are turning missings are written as "NA" into numeric
destring count_not_working count_working earnings_med, replace force

* Calculate the proportion working
g prop_working = count_working/(count_working + count_not_working)

* xtset requires that the individual identifier be a numeric variable

encode inst_name, g(name_number)

* Set the data as panel data with xtset
xtset name_number

* Use xtreg with the "re" option to run random effects on institution intercepts 
* Regressing earnings_med on prop_working
* with random effects for name_number (implied by re)
* and also year fixed effects (which we'll add manually with i.year)

xtreg earnings_med prop_working i.year, re

* We note that comparing with the fixed effects model, our estimates are more precise. But, correlation between X`s and errors suggest bias in our random effect model, and we do see a large increase in estimated beta.
```
