---
title: Heteroskedasticity-consistent standard errors
parent: Nonstandard Errors
grand_parent: Statistical Inference ## Optional for indexing
nav_order: 1
---

# Heteroskedasticity-consistent (HC) standard errors

Heteroskedasticity is when the variance of a model's error term is related to the predictors in that model. For more information, see [Wikipedia: Heteroscedasticity](https://en.m.wikipedia.org/wiki/Heteroscedasticity).

Many regression models assume homoskedasticity (i.e. constant variance of the error term), especially when calculating standard errors. So in the presence of heteroskedasticity, standard errors will be incorrect. _Heteroskedasticity-consistent_ (HC) standard errors &mdash; also called "heteroskedasticity-robust", or sometimes just "robust" standard errors &mdash; are calculated without assuming such homoskedasticity. For more information, see [Wikipedia: Heteroscedasticity-consistent standard errors](https://en.wikipedia.org/wiki/Heteroscedasticity-consistent_standard_errors).

## Keep in Mind

- Robust standard errors are a common way of dealing with heteroskedasticity. However, they make certain assumptions about the form of that heteroskedasticity which may not be true. You may instead want to use [GMM]({{ "/Model_Estimation/generalized_method_of_moments.html" | relative_url }}) instead.
- For nonlinear models like [Logit]({{ "/Model_Estimation/logit_model.html" | relative_url }}), heteroskedasticity can bias estimates in addition to messing up standard errors. Simply using a robust covariance matrix will not eliminate this bias. Check the documentation of your nonlinear regression command to see whether its robust-error options also adjust for this bias. If not, consider other ways of dealing with heteroskedasticity besides robust errors.
- There are multiple kinds of robust standard errors, for example HC1, HC2, and HC3. Check in to the kind available to you in the commands you're using.

## Also Consider

- [Generalized Method of Moments]({{ "/Model_Estimation/generalized_method_of_moments.html" | relative_url }})
- [Cluster-Robust Standard Errors]({{ "/Model_Estimation/cluster_robust_standard_errors.html" | relative_url }})
- [Bootstrap Standard Errors]({{ "/Model_Estimation/bootstrap_standard_errors.html" | relative_url }})
- [Jackknife Standard Errors]({{ "/Model_Estimation/jackknife_standard_errors.html" | relative_url }})

# Implementations

## R

The easiest way to obtain robust standard errors in R is with the **estimatr** package ([link](https://declaredesign.org/r/estimatr/)) and its family of `lm_robust` functions. These will default to "HC2" errors, but users can specify a variety of other options. 

```R
# If necessary, install estimatr
# install.packages(c('estimatr'))
library(estimatr)

# Get mtcars data
# data(mtcars) ## Optional: Will load automatically anyway

# Default is "HC2". Here we'll specify "HC3" just to illustrate.
m1 <- lm_robust(mpg ~ cyl + disp + hp, data = mtcars, se_type = "HC3")
summary(m1)
```

Alternately, users may consider the `vcovHC` function from the **sandwich** package ([link](https://cran.r-project.org/web/packages/sandwich/index.html)), which is very flexible and supports a wide variety of generic regression objects. For inference (t-tests, etc.), use in conjunction with the `coeftest` function from the **lmtest** package ([link](https://cran.r-project.org/web/packages/lmtest/index.html)).

```R
# If necessary, install lmtest and sandwich
# install.packages(c('lmtest','sandwich'))
library(sandwich)
library(lmtest)

# Create a normal regression model (i.e. without robust standard errors)
m2 <- lm(mpg ~ cyl + disp + hp, data = mtcars)

# Get the robust VCOV matrix using sandwich::vcovHC(). We can pick the kind of robust errors 
# with the "type" argument. Note that, unlike estimatr::lm_robust(), the default this time  
# is "HC3". I'll specify it here anyway just to illustrate.
vcovHC(m2, type = "HC3")
sqrt(diag(vcovHC(m2))) ## HAC SEs

# For statistical inference, use together with lmtest::coeftest().
coeftest(m2, vcov = vcovHC(m2))
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
