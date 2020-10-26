---
title: Heckman Correction Model
parent: Generalised Least Squares
grand_parent: Model Estimation ## Optional for indexing
has_children: false
mathjax: true
nav_order: 1
---

# Heckman Correction Model

The Heckman correction for sample selection is a method designed to be used in cases where the model can only be run on a subsample of the data that is not randomly selected. For example, a regression using $$Wage$$ to predict $$Hours Worked$$ cannot include people who don't work, since we don't observe their wage. The Heckman model views this sample selection process as a form of omitted variable bias. So, it (1) explicitly models the process of selecting into the sample, (2) transforms the predicted probability of being in the sample, and (3) adds a correction term to the model.

For more information, see [Wikipedia: Heckman correction](https://en.wikipedia.org/wiki/Heckman_correction).

## Keep in Mind

- Conceptually, the Heckman model uses the regression covariates to predict selection, transforms the prediction, and then includes that transformation in the model. If there are no variables in the selection model that are excluded from the regression model, then the Heckman model is perfectly collinear, and is only statistically identified because the transformation is nonlinear (you may have heard the phrase "identified by nonlinearity" or "identified by the normality assumption"). That's not ideal! You want to find an exclusion restriction - a variable that predicts selection, but does not belong in the final regression model - to avoid this collinearity.

## Also Consider

- There are many ways to estimate a Heckman model. Maximum likelihood approaches generally have better statistical properties, but two-stage models are computationally simpler. Often you can look in the options of your Heckman estimator command to select an estimation method.
- If your goal is to estimate the effect of a binary treatment by modeling selection into treatment, consider a [Treatment Effect Model]({{ "/Model_Estimation/GLS/treatment_effect_model.html" | relative_url }}), or an [Endogenous Switching Model]({{ "/Model_Estimation/GLS/endogenous_switching_model.html" | relative_url }}) which also allows predictors to work differently in different settings.
- Standard Heckman models rely heavily on assumptions about the normality of error terms. You may want to consider [Nonparametric Sample Selection Models]({{ "/Model_Estimation/GLS/nonparametric_sample_selecion_model.html" | relative_url }}).

# Implementations

## Gretl

See [here](http://www.eco.uc3m.es/~ricmora/MICCUA/materials/S25T44_English_handout.pdf) for a demonstration.

## Python

See [here](https://rlhick.people.wm.edu/stories/econ_407_notes_heckman.html) for a demonstration.

## R

```r

# Install sampleSelection package if necessary
# install.packages('sampleSelection')
library(sampleSelection)

# Get data from Mroz (1987, Econometrica)
# which has Panel Study of Income Dynamics data for married women
data("Mroz87")

# First consider our selection model
# We only observe wages for labor force participants (lfp == 1)
# So we model that as a function of work experience (linear and squared), 
# income from the rest of the family, education, and number of kids 5 or younger.
# lfp ~ exper + I(exper^2) + faminc + educ + kids5

# Then we model the regression of interest. We're interested in modeling
# wage as a function of work experience, education, and whether you're in a city
# Here, we don't include family income or number of kids, under the assumption that they
# do not belong in a wage model. These are our exclusion restrictions
# (note these particular exclusion restrictions might be a little dubious! But hey, this paper's from 1987.)
# wage ~ exper + I(exper^2) + educ + city

# Put them together in a selection() command
heck_model <- selection(lfp ~ exper + I(exper^2) + faminc + educ + kids5,
                        wage ~ exper + I(exper^2) + educ + city,
                        Mroz87)

summary(heck_model)
```

## Stata

```stata
* Get data from Mroz (1987, Econometrica)
* which has Panel Study of Income Dynamics data for married women
* (data via the sampleSelection package in R)
import delimited "https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Estimation/Data/Heckman_Correction_Model/Mroz87.csv", clear

* First, consider the regression of interest. 

* First consider our selection model
* We only observe wages for labor force participants (lfp == 1)
* So we model that as a function of work experience (linear and squared), 
* income from the rest of the family, education, and number of kids 5 or younger.
* select(lfp = c.exper##c.exper faminc educ kids5)

* Then we model the regression of interest. We're interested in modeling
* wage as a function of work experience, education, and whether you're in a city
* Here, we don't include family income or number of kids, under the assumption that they
* do not belong in a wage model. These are our exclusion restrictions
* (note these particular exclusion restrictions might be a little dubious! But hey, 1987.)
* wage c.exper##c.exper educ city

* Now we run our Heckman model!
heckman wage c.exper##c.exper educ city, select(lfp = c.exper##c.exper faminc educ kids5)
```
