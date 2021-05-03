---
title: Instrumental Variables
parent: Research Design
grand_parent: Model Estimation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Instrumental Variables

In the regression model

$$ Y = \beta_0 + \beta_1 X + \epsilon $$

where $$\epsilon$$ is an error term, the estimated $$\hat{\beta}_1$$ will not give the causal effect of $$X$$ on $$Y$$ if $$X$$ is *endogenous* - that is, if $$X$$ is related to $$\epsilon$$ and so determined by forces *within the model* (endogenous). 

One way to recover the causal effect of $$X$$ on $$Y$$ is to use instrumental variables. If there exists a variable $$Z$$ that is related to $$X$$ but is completely unrelated to $$\epsilon$$ (perhaps after adding some controls), then you can use instrumental variables estimation to isolate only the part of the variation in $$X$$ that is explained by $$Z$$. Naturally, then, this part of the variation is unrelated to $$\epsilon$$ because $$Z$$ is unrelated to $$\epsilon$$, and you can get the causal effect of that part of $$X$$.

For more information, see [Wikipedia: Instrumental variables estimation](https://en.wikipedia.org/wiki/Instrumental_variables_estimation).

## Keep in Mind

- Technically, all the variables in the model except for the dependent variable and the endogenous variables are "instruments", including controls. However, it is also common to refer to only the *excluded* instruments (i.e., variables that are only used to predict the endogenous variable, not the dependent variable) as instruments. This page will follow that convention.
- For instrumental variables to work, it must be the case that the instrument is **only** related to the outcome variable **through** other variables already included in the model like the endogenous variables or the controls. This is called the "validity" assumption and it cannot be verified in the data, only theoretically. Give serious consideration as to whether validity applies to your instrument before using instrumental variables.
- You can check for the *relevance* of your instrument, which is how strongly related it is to your endogenous variable. A rule of thumb is that an [joint F-test]({{ "/Model_Estimation/Statistical_Inference/linear_hypothesis_tests.html" | relative_url }}) of the instruments should be at least 10, but this is only a rule of thumb, and imprecise (see [Stock and Yogo 2005](https://books.google.com/books?hl=en&lr=&id=sLXakrLDloEC&oi=fnd&pg=PA80&ots=5hTdefAIvc&sig=-rhr7Z7dK758nLn2wFzLlf1WxhU#v=onepage&q&f=false) for a more precise version of this test). In general, if the instruments are not very strong predictors of the endogenous variables, you should consider whether your analysis fits the assumptions necessary to run a weak-instrument-robust estimation method. See [Hahn & Hausman 2003](https://www.aeaweb.org/articles?id=10.1257/000282803321946912) for an overview.
- Instrumental variables estimates a *local average treatment effect* - in other words, a weighted average of each individual observation's treatment effect, where the weights are based on the strength of the effect of the instrument on the endogenous variable. Note both that this is not the same thing as an *average treatment effect*, which is an average of each individual's treatment effect, which is usually what is desired, and also that if the instrumental variable has effects of different signs for different people (non-monotonicity), then the estimate isn't really anything of interest. Be sure that monotonicity makes sense in your context before using instrumental variables.
- Instrumental variables is a consistent estimator of a causal effect, but it is biased in finite samples. Be wary of using instrumental variables in small samples.

## Also Consider

- Instrumental variables methods generally rely on linearity assumptions, and if your dependent or endogenous variables are not continuous, their assumptions may not hold. Consider methods specially designed for [nonlinear instrumental variables estimation]({{ "/Model_Estimation/nonlinear_instrumental_variables_estimation.html" | relative_url }}).
- There are many ways to estimate instrumental variables, not just two stage least squares. Different estimators such as GMM or k-class limited-information maximum likelihood estimators perform better or worse depending on heterogeneous treatment effects, heteroskedasticity, and sample size. Many instrumental variables estimation commands allow for multiple different estimation methods, described below. Note that in the just-identified case (where the number of instruments is the same as the number of endogenous variables), several common estimators produce identical results.


# Implementations

## Python

The easiest way to run instrument variables regressions in Python is probably the [**linearmodels**](https://bashtage.github.io/linearmodels/index.html) package, although there are other packages available.

```python
# Conda install linearmodels, pandas, and numpy, if you don't have them already
from linearmodels.iv import IV2SLS
import pandas as pd
import numpy as np

df = pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/AER/CigarettesSW.csv',
                 index_col=0)

# We will use cigarette taxes as an instrument for cigarette prices
# to evaluate the effect of cigarette price on log number of packs smoked
# With income per capita as a control

# Adjust everything for inflation
df['rprice'] = df['price']/df['cpi']
df['rincome'] = df['income']/df['population']/df['cpi']
df['tdiff'] = (df['taxs'] - df['tax'])/df['cpi']

# Specify formula in format of 'y ~ exog + [endog ~ instruments]'.
# The '1' on the right-hand side of the formula adds a constant.
formula = 'np.log(packs) ~ 1 + np.log(rincome) + [np.log(rprice) ~ tdiff]'

# Specify model and data
mod = IV2SLS.from_formula(formula, df)

# Fit model
res = mod.fit()

# Show model summary
res.summary

```

## R

There are several ways to run instrumental variables in R. Here we will cover two - `AER::ivreg()`, which is probably the most common, and `lfe::felm()`, which is more flexible and powerful. You may also want to consider looking at `estimatr::iv_robust`, which combines much of the flexibility of `lfe::felm()` with the simple syntax of `AER::ivreg()`, although it is not as powerful.

```r
# If necessary, install both packages.
# install.packages(c('AER','lfe'))
# Load AER
library(AER)

# Load the Cigarettes data from ivreg, following the example
data(CigarettesSW)
# We will be using cigarette taxes as an instrument for cigarette prices
# to evaluate the effect of cigarette price on log number of packs smoked
# With income per capita as a control

# Adjust everything for inflation
CigarettesSW$rprice <- CigarettesSW$price/CigarettesSW$cpi
CigarettesSW$rincome <- CigarettesSW$income/CigarettesSW$population/CigarettesSW$cpi
CigarettesSW$tdiff <- (CigarettesSW$taxs - CigarettesSW$tax)/CigarettesSW$cpi

# The regression formula takes the format
# dependent.variable ~ endogenous.variables + controls | instrumental.variables + controls
ivmodel <- ivreg(log(packs) ~ log(rprice) + log(rincome) | tdiff + log(rincome),
                 data = CigarettesSW)
summary(ivmodel)


# Now we will run the same model with lfe::felm
library(lfe)

# The regression formula takes the format
# dependent vairable ~ 
#    controls |
#    fixed.effects | 
#    (endogenous.variables ~ instruments) |
#    clusters.for.standard.errors
# So if need be it is straightforward to adjust this example to account for
# fixed effects and clustering.
# Note the 0 indicating no fixed effects
ivmodel2 <- felm(log(packs) ~ log(rincome) | 0 | (log(rprice) ~ tdiff),
                     data = CigarettesSW)
summary(ivmodel2)

# felm can also use several k-class estimation methods; see help(felm) for the full list.
# Let's run it with a limited-information maximum likelihood estimator with 
# the fuller adjustment set to minimize squared error (4).
ivmodel3 <- felm(log(packs) ~ log(rincome) | 0 | (log(rprice) ~ tdiff),
                 data = CigarettesSW, kclass = 'liml', fuller = 4)
summary(ivmodel3)
```

## Stata

Instrumental variables estimation in Stata typically uses the built-in `ivregress` command. This command can be used to implement linear instrumental variables regression using two-stage least squares, GMM, or LIML

```stata
* Get Stock and Watson Cigarette data
import delimited "https://vincentarelbundock.github.io/Rdatasets/csv/Zelig/CigarettesSW.csv", clear

* Adjust everything for inflation
g rprice = price/cpi
g rincome = (income/population)/cpi
g tdiff = (taxs - tax)/cpi

* And take logs
g lpacks = ln(packs)
g lrincome = ln(rincome)
g lrprice = ln(rprice)

* The syntax for the regression is
* name_of_estimator dependent_variable controls (endogenous_variable = instruments)
* where name_of_estimator can be two stage least squares (2sls), 
* limited information maximum likelihood (liml, note that ivregress doesn't support k-class estimators), 
* or generalized method of moments (gmm)
* Here we can run two stage least squares
ivregress 2sls lpacks rincome (lrprice = tdiff)

* Or gmm. 
ivregress gmm lpacks rincome (lrprice = tdiff)
```
