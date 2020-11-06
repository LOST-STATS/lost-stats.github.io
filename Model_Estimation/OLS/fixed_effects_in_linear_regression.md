---
title: Fixed Effects in Linear Regression
parent: Ordinary Least Squares
grand_parent: Model Estimation ## Optional for indexing
has_children: false
mathjax: true
nav_order: 3
---

# Fixed Effects in Linear Regression

Fixed effects is a statistical regression model in which the intercept of the regression model is allowed to vary freely across individuals or groups. It is often applied to panel data in order to control for any individual-specific attributes that do not vary across time.

For more information, see [Wikipedia: Fixed Effects Model](https://en.wikipedia.org/wiki/Fixed_effects_model).

## Keep in Mind

- To use individual-level fixed effects, you must observe the same person multiple times (panel data).
- In a linear regression context, fixed effects regression is relatively straightforward, and can be thought of as effectively adding a binary control variable for each individual, or subtracting the within-individual mean of each variable (the "within" estimator). However, you may want to apply fixed effects to other models like logit or probit. This is usually possible (depending on the model), but if you just add a set of binary controls or subtract within-individual means, it won't work very well. Instead, look for a command specifically designed to implement fixed effects for that model.
- If you are using fixed effects to estimate the causal effect of a variable $$X$$, individuals with more variance in $$X$$ will be weighted more heavily (Gibbons, Serrano, & Urbancic 2019, ungated copy [here](http://gibbons.bio/docs/bfe.pdf)). You may want to consider weighting your regression by the inverse within-individual variance of $$X$$.

## Also Consider

- Instead of fixed effects you may want to use random effects, which requires additional assumptions but is statistically more efficient and also allows the individual effect to be modeled using covariates. See [Linear Mixed-Effects Regression]({{ "/Model_Estimation/Multilevel_Models/linear_mixed_effects_regression.html" | relative_url }})
- You may want to consider [clustering your standard errors]({{ "/Statistical_Inference/Statistical_Inference/Nonstandard_Errors/clustered_se.html" | relative_url }}) at the same level as (some or more of) your fixed effects.

# Implementations

## Julia

Julia provides support for estimating high-dimensional fixed effect models through the **FixedEffectModels.jl** package ([link](https://github.com/matthieugomez/FixedEffectModels.jl)). Similarly to **felm** (R) and **reghdfe** (Stata), the package uses the method of alternating projections to sweep out fixed effects. However, the Julia implementation is typically quite a bit faster than these other two methods. It also offers further performance gains via GPU computation for users with a working CUDA installation (up to an order of magnitude faster for complicated problems).

```julia
# If necessary, install JuliaFixedEffects.jl and some ancilliary packages for reading in the data
# ] add JuliaFixedEffects, CSVFiles, DataFrames

# Read in the example CSV and convert to a data frame
using CSVFiles, DataFrames
df = DataFrame(load("https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Model_Estimation/Data/Fixed_Effects_in_Linear_Regression/Scorecard.csv"))
# Calculate proportion of graduates working
df[!, :prop_working] = df[!, :count_working] ./ (df[!, :count_working ] .+ df[!, :count_not_working])

using JuliaFixedEffects

# Regress median earnings on the proportion of working graduates.
# We'll control for institution name and year as our fixed effects.
# We'll also cluster our standard errors by institution name.
reg(df, @formula(earnings_med ~ prop_working + fe(inst_name) + fe(year)), Vcov.cluster(:inst_name))

# Multithread example
Threads.nthreads() ## See: https://docs.julialang.org/en/v1.2/manual/parallel-computing/#man-multithreading-1
reg(df, @formula(earnings_med ~ prop_working + fe(inst_name) + fe(year)), Vcov.cluster(:inst_name), method = :lsmr_threads)

# GPU example (requires working CUDA installation)
reg(df, @formula(earnings_med ~ prop_working + fe(inst_name) + fe(year)), Vcov.cluster(:inst_name), method = :lsmr_gpu)
```

## R

There are numerous packages for estimating fixed effect models in R. We will limit our examples here to the two fastest implementations &mdash; `lfe::felm` and `fixest::feols` &mdash; both of which support high-dimensional fixed effects and standard error correction (multiway clustering, etc.).

We first demonstrate fixed effects in R using `felm` from the **lfe** package ([link](https://cran.r-project.org/web/packages/lfe/index.html)). `lfe::felm` uses the Method of Alternating Projections to "sweep out" the fixed effects and avoid estimating them directly. By default, this is automatically done in parallel, using all available cores on a user's machine to maximize performance. (It is also possible to change this behaviour.)

```r
# If necessary, install lfe
# install.packages('lfe')
library(lfe)

# Read in data from the College Scorecard
df <- read.csv('https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Model_Estimation/Data/Fixed_Effects_in_Linear_Regression/Scorecard.csv')
# Calculate proportion of graduates working
df$prop_working <- df$count_working/(df$count_working + df$count_not_working)

# A felm formula is constructed as:
# outcome ~
#   covariates |
#   fixed effects |
#   instrumental variables specification | 
#   cluster variables for standard errors

# Here let's regress earnings_med on prop_working
# with institution name and year as our fixed effects
# And clusters for institution name
felm_model <- felm(earnings_med ~ prop_working | inst_name + year | 0 | inst_name, data = df)

# Look at our results
summary(felm_model)
```

Next, we consider `feols` from the **fixest** package ([link](https://github.com/lrberge/fixest/wiki)). The syntax is very similar to  `lfe::felm` and again the estimation will be done in parallel by default. However, rather than the method of alternating projections, `fixest::feols` uses a concentrated maximum likelihood method to efficiently estimate models with an arbitrary number of fixed effects. Current [benchmarks](https://github.com/lrberge/fixest/wiki#benchmarking) suggest that this can yield significant speed gains, especially for large problems. For the below example, we'll continue with the same College Scorecard dataset already loaded into memory. 

```r
# If necessary, install fixest
# install.packages('fixest')
library(fixest)

# Run the same regression as before
feols_model <- feols(earnings_med ~ prop_working | inst_name + year, data = df)

# Look at our results
# Standard errors are automatically clustered at the inst_name level
summary(feols_model)
# It is also possible to specify additional or different clustering of errors
summary(feols_model, se = "twoway")
summary(feols_model, cluster = c("inst_name", "year")) ## same as the above
```

As noted above, there are numerous other ways to implement fixed effect models in R. Users may also wish to look at the **plm**, **lme4**, and **estimatr** packages among others. For example, the latter's `estimatr::lm_robust` function provides syntax that may be more familar syntax to new R users who are coming over from Stata. Note, however, that it will be less efficient for complicated models.

## Stata

We will estimate fixed effects using Stata in two ways. First, using the built in `xtreg` command. Second, using the **reghdfe** package ([link](http://scorreia.com/software/reghdfe/)), which is more efficient and better handles multiple levels of fixed effects (as well as multiway clustering), but must be downloaded from SSC first.

```stata
* Load in College Scorecard data
import delimited "https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Model_Estimation/Data/Fixed_Effects_in_Linear_Regression/Scorecard.csv", clear

* The missings are written as "NA", let's turn this numeric
destring count_not_working count_working earnings_med, replace force
* Calculate the proportion working
g prop_working = count_working/(count_working + count_not_working)

* xtset requires that the individual identifier be a numeric variable
encode inst_name, g(name_number)

* Set the data as panel data with xtset
xtset name_number

* Use xtreg with the "fe" option to run fixed effects
* Regressing earnings_med on prop_working
* with fixed effects for name_number (implied by fe)
* and also year (which we'll add manually with i.year)
* and standard errors clustered by name_number
xtreg earnings_med prop_working i.year, fe vce(cluster name_number)

* Now, let's demonstrate the same regression with reghdfe.
* Install the package first if necessary.
* ssc install reghdfe

* For reghdfe we don't need to xtset the data. Let's undo that
xtset, clear

* We specify both sets of fixed effects in absorb()
reghdfe earnings_med prop_working, absorb(name_number year) vce(cluster inst_name)
```
