---
title: Bootstrap Standard Errors
parent: Nonstandard Errors
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Bootstrap Standard Errors

Boostrapping is a statistical method that uses random sampling with replacement to determine the sampling variation of an estimate. If you have a data set of size $$N$$, then (in its simplest form) a "bootstrap sample" is a data set that randomly selects $$N$$ rows from the original data, perhaps taking the same row multiple times. For more information, see [Wikipedia](https://en.wikipedia.org/wiki/Bootstrapping_%28statistics%29).

Bootstrap is commonly used to calculate standard errors. If you produce many bootstrap samples and calculate a statistic in each of them, then under certain conditions, the distribution of that statistic across the bootstrap samples is the sampling distribution of that statistic. So the standard deviation of the statistic across bootstrap samples can be used as an estimate of standard error. This approach is generally used in cases where calculating the standard error of a statistic parametrically would be too difficult or impossible.

## Keep in Mind

- Although it feels entirely data-driven, bootstrap standard errors rely on assumptions just like everything else. It assumes your original model is correctly specified, for example. Basic bootstrapping assumes no heteroskedasticity, and otherwise independent error terms.
- Bootstrapping can also be used to calculate other features of the parameter's sample distribution, like the percentile, not just the standard error.

## Also Consider

- This page will consider the simplest approach to bootstrapping (the basic resampling of rows), but there are many others, such as cluster (strata) bootstrap, Bayesian bootstrap, and Wild bootstrap. For more information, see [Wikipedia](https://en.wikipedia.org/wiki/Bootstrapping_%28statistics%29). Check the help files of the bootstrap package you're using to see if they support these approaches.
- Bootstrap is relatively straightforward to program yourself: resample, calculate, repeat, and then look at the distribution. If your reason for doing bootstrap is because you want your standard errors to reflect an unusual sampling or data manipulation procedure, for example, you may be best off programming your own routine.
- This page contains a general approach to bootstrap, but for some statistical procedures, bootstrap standard errors are common enough that the command itself has an option to produce bootstrap standard errors. If this option is available, it is likely superior.

# Implementations

## R

The standard approach to bootstrapping standard errors in R is to use the **boot** package.

```r
# If necessary
# install.packages('boot','broom','stargazer')

# Load boot library
library(boot)

# Use mtcars data
data(mtcars)

# Create function that takes
# A dataset and indices as input, and then
# performs analysis and returns a parameter of interest
regboot <- function(data, indices) {
  m1 <- lm(hp~mpg + cyl, data = data[indices,])
  
  return(coefficients(m1))
}

# Call boot() function using the function we just made with 200 bootstrap samples
# Note the option for stratified resampling with "strata", in addition to other options
# in help(boot)
boot_results <- boot(mtcars, regboot, R = 200)

# See results
boot_results
plot(boot_results)
# There are lots of diagnostics you can look at at this point,
# see https://statweb.stanford.edu/~tibs/sta305files/FoxOnBootingRegInR.pdf

# Optional: print regression table with the bootstrap SEs
# This uses stargazer, but the method is similar
# with other table-making packages,
# see https://lost-stats.github.io/Presentation/export_a_formatted_regression_table.html
library(broom)
tidy_results <- tidy(boot_results)

library(stargazer)
m1 <- lm(hp~mpg + cyl, data = mtcars)
stargazer(m1, se = list(tidy_results$std.error), type = 'text')
```

## Stata

Many commands in Stata come with a `vce(bootstrap)` option, which will implement bootstrap standard errors.

```stata
* Load auto data
sysuse auto.dta, clear

* Run a regression with bootstrap SEs
reg mpg weight length, vce(bootstrap)

* see help bootstrap to adjust options like number of samples
* or strata
reg mpg weight length, vce(bootstrap, reps(200))
```