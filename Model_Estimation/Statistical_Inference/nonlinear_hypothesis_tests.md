---
title: Nonlinear Hypothesis Tests
parent: Statistical Inference
grand_parent: Model Estimation
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Joint Significance Tests

Most regression output, or output from other methods that produce multiple coefficients, will include the results of frequentist hypothesis tests comparing each coefficient to 0. However, in many cases, you may be interested in a hypothesis test of a null restriction that involves a nonlinear combination of the coefficients, or producing an estimate and sampling distriubtion for that nonlinear combination. For example, in the model

$$ Y = \beta_0 + \beta_1X + \beta_2Z + \varepsilon $$

You may be interested in the ratio of the two effects, $\beta_1/\beta_2$, and would want an estimate of that combination, along with a standard error, and a hypothesis test comparing that estimate to 0 or some other value.

Estimates and tests of nonlinear combinations of coefficients are different than for linear combinations, because they imply restrictions on estimation that cannot be expressed in the form of a matrix of linear restrictions. The most common approach to producing a sampling distribution for a nonlinear combination of coefficients is the [delta method](https://en.wikipedia.org/wiki/Delta_method) and that is what all the commands on this page use.

## Keep in Mind

- Depending on your goal, you may be able to avoid doing a test of nonlinear combinations of coefficients by converting the combination into a linear one. For example, if you do not want to estimate $\beta_1/\beta_2$ itself, but instead are only interested in testing the null hypothesis $\beta_1/\beta_2 = 1$, this null hypothesis can be manipulated to instead be $\beta_1 = \beta_2$ or $\beta_1 - \beta_2 = 0$, either of which can be evaluated as a hypothesis test on a linear combination of coefficients.

## Also Consider

- [Linear Hypothesis Tests]({{ "Model_Estimation/Statistical_Inference/linear_hypothesis_tests.html" | relative_url }}).

# Implementations

## R

In R, the **marginaleffects** package contains a number of useful functions for postestimation, including nonlinear combinations of coefficients via the `deltamethod()` function. It is used here with `lm()`, but is also compatible with regression output from many other packages and functions.

```r
library(marginaleffects)

data(mtcars)

# Run the model
m = lm(mpg ~ hp + wt, data = mtcars)

# Specify the combination of coefficients in the form of a null-hypothesis equation
deltamethod(m, 'hp/wt = 1')

# This produces an estimate, standard error, p-value, and confidence interval
```


## Stata

Stata has the `nlcom` postestimation command for producing estimates and standard errors for nonlinear tests of coefficients. It will also produce the results of hypothesis tests comparing the combination to 0, so to compare to other values, subtract the desired value from the combination.


```stata
* Load auto data
sysuse https://github.com/LOST-STATS/lost-stats.github.io/blob/master/Data/auto.dta

regress mpg trunk weight

nlcom _b[trunk]/_b[weight] - 1
```
