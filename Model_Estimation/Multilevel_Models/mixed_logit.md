---
title: Mixed Logit Model
parent: Multilevel Models
grand_parent: Model Estimation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: TRUE
---

A mixed logit model (sometimes referred to as a random parameters logit model) estimates distributional parameters that allow for individual-level heterogeneity in tastes that are not compatible with a traditional logit framework.  Mixed logit models can also provide for additional flexibility as it pertains to correlated random parameters and can be used with panel data.

For more information about mixed logit models, see [Wikipedia: Mixed Logit.](https://en.wikipedia.org/wiki/Mixed_logit)

## Keep in Mind

- The mixed logit model estimates a distribution.  Parameters are then generated from that distribution via a simulation with a specified number of draws.
- The estimates from a mixed logit model cannot simply be interpreted as marginal effects, as they are maximum likelihood estimations.  Further, the variation at the individual level means estimated effects are relative to the individual.
- The estimation of mixed logit models is very difficult and there are quite a few details and different approaches. So you can't really assume that one package will produce the same results as another. Read the documentation of the command you're using so you at least know what paper produced the estimation method!

# Implementations

## R

To estimate a mixed logit model in R, we will first transform the data using the [dfidx](https://cran.r-project.org/web/packages/dfidx/index.html) package.  Then we will use the [mlogit](https://cran.r-project.org/web/packages/mlogit/) package to carry out the estimation.


```r
# Install mlogit which also includes the Electricity dataset for the example.
# The package dfidx will be used to transform our data
# install.packages("mlogit", "dfidx")
library(mlogit)
library(dfidx)

# Load the Electricity dataset
data("Electricity", package = "mlogit")

# First, we need to coerce the data to a dfidx object
# This allows for a panel with multiple indices
# For further documentation, see dfidx.

Electricity$index <- 1:nrow(Electricity)
elec = dfidx(Electricity, idx = list(c("index", "id")),
                choice = "choice", varying = 3:26, sep = "")

# We then estimate individual choice over electricity providers for
# different cost and contract structures with a suppressed intercept

my_mixed_logit = mlogit(data = elec, 
       formula = choice ~ 0 + pf + cl + loc + wk + tod + seas,
       # Specify distributions for random parameter estimates
       # "n" indicates we have specified a normal distribution
       # note pf is omitted from rpar, so it will not be estimated as random
       rpar = c(cl = "n", loc = "u", wk = "n", tod = "n", seas = "n"), 
       # R is the number of simulation draws
       R = 100, 
       # For simplicity, we won't include correlated parameter estimates
       correlation = FALSE, 
       # This data is from a panel
       panel = TRUE)

# Results
summary(my_mixed_logit)

# Note that this output will include the simulated coefficient estimates, 
# simulated standard error estimates, and distributional details for the
# random coefficients (all, in this case)
# Note also that pf is given as a point estimate, and mlogit does not generate
# a distribution for it as it does the others

# You can extract and summarize coefficient estimates using the rpar function

marg_loc = rpar(my_mixed_logit, "loc")
summary(marg_loc)

# You can also normalize coefficients and distributions by, say, price

cl_by_pf = rpar(my_mixed_logit, "cl", norm = "pf")
summary(cl_by_pf)
```

For further examples, visit the CRAN vignette [here.](https://cran.r-project.org/web/packages/mlogit/vignettes/c5.mxl.html)

For a very detailed example using the Electricity dataset, see [here.](https://cran.r-project.org/web/packages/mlogit/vignettes/e3mxlogit.html)

## Stata

As of Stata 17, there is the base-Stata `xtmlogit` command which is probably preferable to `mixlogit`. However, many people do not have Stata 17, so this example uses `mixlogit`, which requires installation from `ssc install mixlogit`. For more information on `xtmlogit`, see [this page](https://www.stata.com/new-in-stata/panel-data-multinomial-logit/).

`mixlogit` requires data of the form (although not necessarily with the variable names):

choice | X | group | id
-|--|-|-
1 | 10 | 1 | 1
0 | 12 | 1 | 1
0 | 11 | 2 | 1
1 | 14 | 2 | 1
1 | 9 | 3 | 2
0 | 11 | 3 | 2

where `choice` is the dependent variable and is binary, indicating which of the options was chosen. `X` is (one of) the predictors, `group` is an identifying variable for the different choice occasions, and `id` is a vector of individual-decision-maker identifiers, if this is panel data where the same decision-making makes multiple decisions.

```stata
* If necessary:
* ssc install mixlogit

import delimited "https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Model_Estimation/Multilevel_Models/Data/Electricity.csv", clear

* Reshape data into "long" format like we need for mixlogit
g decision_id = _n
reshape long pf cl loc wk tod seas, i(choice id decision_id) j(option)

* Remember, the dependent variable should be binary, indicating that this option
* was chosen
g chosen = choice == option

* Let's fix the parameters on all the predictors
* except for pf, which we'll allow to vary
* (this is for speed in the example)
mixlogit chose cl loc wk tod seas, ///
	group(decision_id) /// each individual choice is identified by decision_id
	id(id) /// each person is identified by id
	rand(pf)

* Options to consider:
* corr allows multiple parameter distributions to be correlated
* ln() allows some of the parameter distributions to be log-normal

* We can get individual parameter estimates with mixlbeta, which will
* save the estimates to file
mixlbeta pf, saving(pf_coefs.dta)
```
