---
title: Heteroskedasticity-Robust Standard Errors
parent: Model Estimation
has_children: false
nav_order: 1
---

# Heteroskedasticity-Robust Standard Errors

Heteroskedasticity is when the variance of a model's error term is related to the predictors in that model. For more information, see [Wikipedia: Heteroscedasticity](https://en.m.wikipedia.org/wiki/Heteroscedasticity).

Many regression models assume homoskedasticity (the variance of the error term is constant), especially when calculating standard errors. So in the presence of heteroskedasticity, standard errors will be incorrect. Heteroskedasticity-robust standard errors calculate standard errors without assuming homoskedasticity.

## Keep in Mind

- Robust standard errors are a common way of dealing with heteroskedasticity. However, they make certain assumptions about the form of that heteroskedasticity which may not be true. You may instead want to use [GMM](https://lost-stats.github.io/Model_Estimation/generalized_method_of_moments.html) instead.
- For nonlinear models like [Logit](https://lost-stats.github.io/Model_Estimation/logit_model.html), heteroskedasticity can bias estimates in addition to messing up standard errors. Simply using a robust covariance matrix will not eliminate this bias. Check the documentation of your nonlinear regression command to see whether its robust-error options also adjust for this bias. If not, consider other ways of dealing with heteroskedasticity besides robust errors.
- There are multiple kinds of robust standard errors, for example HC1, HC2, and HC3. Check in to the kind available to you in the commands you're using.

## Also Consider

- [Generalized Method of Moments](https://lost-stats.github.io/Model_Estimation/generalized_method_of_moments.html)
- [Cluster-Robust Standard Errors](https://lost-stats.github.io/Model_Estimation/cluster_robust_standard_errors.html)
- [Bootstrap Standard Errors](https://lost-stats.github.io/Model_Estimation/bootstrap_standard_errors.html)
- [Jackknife Standard Errors](https://lost-stats.github.io/Model_Estimation/jackknife_standard_errors.html)

# Implementations

## R

Robust standard errors for many different kinds of regression objects in R can be obtained using the `coeftest` function in the `lmtest` package combined with the `vcovHC` function in the `sandwich` package. Alternately, while it does not handle as many types of regressions, the `lm_robust` function in `estimatr` can provide robust standard errors much more easily.

```R
# If necessary, install lmtest, sandwich, and estimatr
# install.packages(c('lmtest','sandwich','estimatr'))

# Get mtcars data
data(mtcars)

# Get robust errors using vcovHC and lmtest
library(lmtest)
library(sandwich)

# Create regression model without robust standard errors
m1 <- lm(mpg ~ cyl + disp + hp, data = mtcars)

# Put the model into vcovHC() to get a robust covariance matrix
# and then put that in lmtest() to get the regression results with robust errors
# Pick the kind of robust errors with "type" 
# HC3 is the default but I've specified it here anyway
coeftest(m1, vcov = vcovHC(m1, type = "HC3"))

# Alternately, just use lm_robust. Here, HC2 is the default
library(estimatr)
m2 <- lm_robust(mpg ~ cyl + disp + hp, data = mtcars, se_type = "HC3")
summary(m2)
```

## Stata

Stata has robust standard errors built into most regression commands, and they generally work the same way for all commands.

```stata
* Load in auto data
sysuse auto.dta, clear

* Just add robust to the options of the regression
* This will give you HC1
regress price mpg gear_ratio foreign, robust

* For other kinds of robust standard errors use vce()
regress price mpg gear_ratio foreign, vce(hc3)
```
