---
title: Linear Hypothesis Tests
parent: Statistical Inference
grand_parent: Model Estimation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Linear Hypothesis Tests

Most regression output will include the results of frequentist hypothesis tests comparing each coefficient to 0. However, in many cases, you may be interested in whether a linear sum of the coefficients is 0. For example, in the regression

$$
Outcome = \beta_0 + \beta_1\times GoodThing + \beta_2\times BadThing
$$

You may be interested to see if $$GoodThing$$ and $$BadThing$$ (both binary variables) cancel each other out. So you would want to do a test of $$\beta_1 - \beta_2 = 0$$.

Alternately, you may want to do a joint significance test of multiple linear hypotheses. For example, you may be interested in whether $$\beta_1$$ *or* $$\beta_2$$ are nonzero and so would want to jointly test the hypotheses $$\beta_1 = 0$$ *and* $$\beta_2=0$$ rather than doing them one at a time. Note the *and* here, since if either one *or* the other is rejected, we reject the null.

## Keep in Mind

- Be sure to carefully interpret the result. If you are doing a joint test, rejection means that *at least one* of your hypotheses can be rejected, not each of them. And you don't necessarily know which ones can be rejected!
- Generally, linear hypothesis tests are performed using F-statistics. However, there are alternate approaches such as likelihood tests or chi-squared tests. Be sure you know which on you're getting.
- Conceptually, what is going on with linear hypothesis tests is that they compare the model you've estimated against a more restrictive one that requires your restrictions (hypotheses) to be true. If the test you have in mind is too complex for the software to figure out on its own, you might be able to do it on your own by taking the sum of squared residuals in your original unrestricted model ($$SSR_{UR}$$), estimate the alternate model with the restriction in place ($$SSR_R$$) and then calculate the F-statistic for the joint test using $$F_{q,n-k-1} = ((SSR_R - SSR_{UR})/q)/(SSR_{UR}/(n-k-1))$$.

## Also Consider

- The process for testing a nonlinear combination of your coefficients, for example testing if $$\beta_1\times\beta_2 = 1$$ or $$\sqrt{\beta_1} = .5$$, is generally different. See [Nonlinear hypothesis tests]({{ "/Model_Estimation/nonlinear_hypothesis_tests.html" | relative_url }}).

# Implementations

## R

Linear hypothesis test in R can be performed for most regression models using the `linearHypothesis()` function in the **car** package. See [this guide](https://www.econometrics-with-r.org/7-3-joint-hypothesis-testing-using-the-f-statistic.html) for more information.

```R
# If necessary
# install.packages('car')
library(car)

data(mtcars)

# Run our model
m1 <- lm(mpg ~ hp + disp + am + wt, data = mtcars)

# Test a linear combination of coefficients
linearHypothesis(m1, c('hp + disp = 0'))

# Test joint significance of multiple coefficients
linearHypothesis(m1, c('hp = 0','disp = 0'))

# Test joint significance of multiple linear combinations
linearHypothesis(m1, c('hp + disp = 0','am + wt = 0'))
```

## Stata

Tests of coefficients in Stata can generally be performed using the built-in `test` command.

```stata
* Load data
sysuse auto.dta

reg mpg headroom trunk prince rep78

* Make sure to run tests while the previous regression is still in memory

* Test joint significance of multiple coefficients
test headroom trunk
* testparm does the same thing but allows wildcards to select coefficients
* this will test the joint significance of every variable with an e in it
testparm *e*

* Test a linear combination of the coefficients
test headroom + trunk = 0

* Test multiple linear combinations by accumulating them one at a time
test headroom + trunk = 0
test price + rep78 = 0, accumulate
```
