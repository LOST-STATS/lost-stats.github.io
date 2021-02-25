---
title: Density Discontinuity Tests for Regression Discontinuity
parent: Research Design
grand_parent: Model Estimation
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Density Discontinuity Tests for Regression Discontinuity

The [Regression Discontinuity Design]({{ "/Model_Estimation/Research_Design/regression_discontinuity_design.html" | relative_url }}) can be applied in cases where a running variable (a.k.a. forcing variable) determines treatment, at least partially, and where the treatment assignment changes significantly at a cutoff variable. In sharp designs, there is no treatment if the running variable is to one side of the cutoff, but everyone with a running variable to the other side of the cutoff is treated.

Regression discontinuity in all its forms (sharp, fuzzy, kink, etc.) relies on an assumption that the running variable is not being manipulated around the cutoff value. For example, imagine the running variable is a math test score, the treatment is getting to skip a grade in math, and treatment assignment is that you get to skip a grade if your score is above 90 (cutoff). If someone knows they're about to get an 89 and so works extra hard because they know how close they are to the cutoff, or if a grader observes someone getting an 89, decides they're close enough, and fudges their score to be a 90 so they can skip a grade, then the running variable is being manipulated. You can no longer assume that people just on either side of the cutoff are comparable, and the research design falls apart.

Density discontinuity tests are intended to check for the presence of manipulation at the cutoff. Generally, they examine the density distribution of the running variable, and look for a discontinuity in the density function just to either side of the cutoff. If there is one (in our math score example, perhaps we see hardly anyone with an 88 or 89, but lots of people with 90 or 91), then the running variable is probably manipulated.

There are several ways to perform this test, all of them descending from [McCrary (2008)](https://www.sciencedirect.com/science/article/pii/S0304407607001133). This page will also show the test based on [Cattaneo, Jansson, and Ma (2020)](https://rdpackages.github.io/references/Cattaneo-Jansson-Ma_2020_JASA.pdf), which requires fewer choices of tuning parameters, and takes fuller advantage of local polynomial regression.

## Keep in Mind

- Density discontinuity tests can only detect the presence of manipulation that would change the distribution of the running variable. If manipulation takes the form of the person who *chooses the cutoff* intentionally placing it for their own benefit, or the running variable being manipulated in *both directions* (in our test score example, some strange test grader doesn't just kick a few 88-89 scores up to 90-91, but instead manipulates people both in and out of treatment, also replacing some 90-91 scores with 88-89s), then the density distribution test will not detect this. As with any research design, carefully consider if your assumptions make sense, don't rely only on a statistical test.

## Also Consider

- The page on [Regression Discontinuity Design]({{ "/Model_Estimation/Research_Design/regression_discontinuity_design.html" | relative_url }}) and [Regression Kink Design]({{ "/Model_Estimation/Research_Design/regression_kink_design.html" | relative_url }})

# Implementations

## R

```r
# If necessary
# install.packages(c('rdd','rddensity'))

# Load RDD of house elections from the R package rddtools,
# and originally from Lee (2008) https://www.sciencedirect.com/science/article/abs/pii/S0304407607001121
df <- read.csv("https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Model_Estimation/Data/Regression_Discontinuity_Design/house.csv")

## Run McCrary (2008) version of the test
library(rdd)

# Give it the running variable and the cutpoint
# it will automatically produce a plot and select the number of bins and the bandwidth
# The output will be hte p-value for the presence of a discontinuity
DCdensity(df$x, c = 0)

## Run the Cattaneo, Jansson, and Ma (2020) estimator
library(rddensity)

# Give it the running variable and the cutoff
# It will pick the bandwidth, and has default polynomials, kernel, and bias correction
# It doesn't have bins to pick
denstest <- rddensity(df$x, c = 0)
summary(denstest)

# Not plot the density discontinuity
# It needs the density test object we just made
rdplotdensity(denstest, df$x)
```

## Stata

In Stata, code for the original McCrary (2008) test cannot be installed from the command line like most packages. If you wish to perform the original version of the test, you can find installation instructions and example code at [McCrary's website](https://eml.berkeley.edu/~jmccrary/DCdensity/).

The Cattaneo, Jansson, and Ma (2020) version is easier to install, and code follows:

```stata
* if necessary
* ssc install rddensity

* Load RDD of house elections from the R package rddtools,
* and originally from Lee (2008) https://www.sciencedirect.com/science/article/abs/pii/S0304407607001121
import delimited "https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Model_Estimation/Data/Regression_Discontinuity_Design/house.csv", clear

* We need a running variable and a cutoff, other defaults can be seen in hte help file
* the "plot" option adds a plot while we're at it
rddensity x, c(0) plot
```
