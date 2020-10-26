---
title: Linear Mixed-Effects Regression
parent: Multilevel Models
grand_parent: Model Estimation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Linear Mixed-Effects Regression

Mixed-effects regression goes by many names, including hierarchical linear model, random coefficient model, and random parameter models. In a mixed-effects regression, some of the parameters are "random effects" which are allowed to vary over the sample. Others are "fixed effects", which are not. Note that this use of the term "fixed effects" is not the same as in [fixed effects regression]({{ "/Model_Estimation/OLS/fixed_effects_in_linear_regression.html" | relative_url }}).

For example, consider the model

$$
y_{ij} = \beta_{0j} + \beta_{1j}X_{1ij} + \beta_{2}X_{2ij} + e_{ij}
$$

The intercept $$\beta_{0j}$$ has a $j$ subscript and is allowed to vary over the sample at the $$j$$ level, where $$j$$ may indicate individual or group, depending on context. The slope on $$X_{1ij}$$, $$\beta_{1j}$$, is similarly allowed to vary over the sample. These are random effects. $$\beta_{2}$$ is not allowed to vary over the sample and so is fixed.

The random parameters have their own "level-two" equations, which may or may not include level-two covariates. 

$$
\beta_{0j} = \gamma_{00} + \gamma_{01}W_j + u_{0j}
$$

$$
\beta_{1j} = \gamma_{10} + u_{1j}
$$

For more information see [Wikipedia](https://en.wikipedia.org/wiki/Multilevel_model).

## Keep in Mind

- The assumptions necessary to use a mixed-effects model in general are the same as for most linear models. However, in addition, mixed-effects models assume that the error terms at different levels are unrelated.
- At the second level, statistical power depends on the number of different $$j$$ values there are. Mixed-effects models may perform poorly if the coefficient is allowed to vary over only a few groups.
- There's no need to stop at two levels - the second-level coefficients can also be allowed to vary at a higher level.

## Also Consider

- There are many variations of mixed-effects models for working with non-linear data, see [nonlinear mixed-effects models]({{ "/Model_Estimation/Multilevel_Models/nonlinear_mixed_effects_models.html" | relative_url }}).
- If the goal is making predictions within subgroups, you may want to consider [multi-level regression with poststratification]({{ "/Model_Estimation/Multilevel_Models/multilevel_regression_with_poststratification.html" | relative_url }}).

# Implementations

## R

One common way to fit mixed-effects models in R is with the `lmer` function in the **lme4** package. To fit fully Bayesian models you may want to consider instead using STAN with the **rstan** package. See the [multi-level regression with poststratification]({{ "/Model_Estimation/multilevel_regression_with_poststratification.html" | relative_url }}) page for more information.

```r
# Install lme4 if necessary
# install.packages('lme4')

# Load up lme4
library(lme4)

# Load up university instructor evaluations data from lme4
data(InstEval)

# We'll be treating lecture age as a numeric variable
InstEval$lectage <- as.numeric(InstEval$lectage)

# Let's look at the relationship between lecture ratings andhow long ago the lecture took place
# with a control for whether the lecture was a service lecture
ols <- lm(y ~ lectage + service, data = InstEval)
summary(ols)

# Now we will use lmer to allow the intercept to vary at the department level
me1 <- lmer(y ~ lectage + service + (1 | dept), data = InstEval)
summary(me1)

# Now we will allow the slope on lectage to vary at the department level
me2 <- lmer(y ~ lectage + service + (-1 + lectage | dept), data = InstEval)
summary(me2)

# Now both the intercept and lectage slope will vary at the department level
me3 <- lmer(y ~ lectage + service + (lectage | dept), data = InstEval)
summary(me3)
```

## Stata

Stata has a family of functions based around the `mixed` command that can estimate mixed-effects models.

```stata
* Load NLS-W data
sysuse nlsw88.dta, clear

* We are going to estimate the relationship between hourly wage and job tenure
* with a contorl for marital status
* Without mixed effects
reg wage tenure married

* Now we will allow the intercept to vary with occupation
mixed wage tenure married || occupation: 

* Next we will allow the slope on tenure to vary with occupation
mixed wage tenure married || occupation: tenure, nocons

* Now, both!
mixed wage tenure married || occupation: tenure

* Finally we will allow the intercept and tenure slope to vary over both occupation
* and age
mixed wage tenure married || occupation: tenure || age: tenure
```
