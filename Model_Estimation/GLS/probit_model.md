---
title: Probit Model
parent: Generalised Least Squares
grand_parent: Model Estimation ## Optional for indexing
has_children: false
mathjax: true
nav_order: 1
---

# Probit Regressions

A Probit regression is a statistical method for a best-fit line between a binary [0/1] outcome variable $$Y$$ and any number of independent variables. Probit regressions follow a [standard normal probability distribution](https://en.wikipedia.org/wiki/Normal_distribution) and the predicted values are bounded between 0 and 1. 

For more information about Probit, see [Wikipedia: Probit](https://en.wikipedia.org/wiki/Probit_model).

## Keep in Mind
- The beta coefficients from a probit model are maximum likelihood estimations. They are not the marginal effect, as you would see in an OLS estimation. So you cannot interpret the beta coefficient as a marginal effect of $$X$$ on $$Y$$.
- To obtain the marginal effect, you need to perform a post-estimation command to discover the marginal effect. In general, you can 'eye-ball' the marginal effect by dividing the probit beta coefficient by 2.5.

# Implementations

## Gretl

```gretl
# Load auto data
open auto.gdt

# Run probit using the auto data, with mpg as the outcome variable
# and headroom, trunk, and weight as predictors
probit mpg const headroom trunk weight
```

## Python

The [**statsmodels**](https://www.statsmodels.org/stable/index.html) package has methods that can perform probit regressions.

```python
# Use pip or conda to install pandas and statsmodels
import pandas as pd
import statsmodels.formula.api as smf

# Read in the data
df = pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/datasets/mtcars.csv',
                 index_col=0)

# Specify the model
mod = smf.probit('vs ~ mpg + cyl', data=df)

# Fit the model
res = mod.fit()

# Look at the results
res.summary()

# Compute marginal effects
marge_effect = res.get_margeff(at='mean', method='dydx')

# Show marginal effects
marge_effect.summary()
```

## R
R can run a probit regression using the `glm()` function. However, to get marginal effects you will need to calculate them by hand or use a package. We will use the **mfx** package, although the **margins** package is another good option, which produces tidy model output.

```r
# If necessary, install the mfx package
# install.packages('mfx')
# mfx is only needed for the marginal effect, not the regression itself
library(mfx)

# Load mtcars data
data(mtcars)

# Use the glm() function to run probit
# Here we are predicting engine type using 
# miles per gallon and number of cylinders as predictors
my_probit <- glm(vs ~ mpg + cyl, data = mtcars,
                family = binomial(link = 'probit'))
# The family argument says we are working with binary data
# and using a probit link function (rather than, say, logit)

# The results
summary(my_probit)

# Marginal effects
probitmfx(vs ~ mpg + cyl, data = mtcars)
```

## Stata

```stata
* Load auto data
sysuse auto.dta

* Probi Estimation
probit foreign mpg weight headroom trunk

* Recover the Marginal Effects (Beta Coefficient in OLS)
margins, dydx(*)
```
