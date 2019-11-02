---
title: Ordinary least squares
parent: Estimation
has_children: true
nav_order: 1
---

# Ordinary Least Squares (Linear Regression)

Ordinary Least Squares (OLS) is a statistical method that produces a best-fit line between some outcome variable **Y** and any number of predictor variables **X1, X2, X3, ...**. These predictor variables may also be called independent variables or right-hand-side variables.

For more information about OLS, see [Wikipedia: Ordinary Least Squares](https://en.wikipedia.org/wiki/Ordinary_least_squares).

## Keep in Mind

- OLS assumes that you have specified a true linear relationship.
- OLS results are not guaranteed to have a causal interpretation. Just because OLS estimates a positive relationship between **X1** and **Y** does not necessarily mean that an increase in **X1** will cause **Y** to increase.
- OLS does *not* require that your variables follow a normal distribution.

## Also Consider

- OLS standard errors assume that the model's error term is [independently and identically distributed (IID)](https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables), which may not be true. Consider whether your analysis should use [heteroskedasticity-robust standard errors](non-ses.html) or cluster-robust standard errors.
- If your outcome variable is discrete or bounded, then OLS is by nature incorrectly specified. You may want to use probit or logit instead for a binary outcome variable, or ordered probit or ordered logit for an ordinal outcome variable.
- If the goal of your analysis is predicting the outcome variable and you have a very long list of predictor variables, you may want to consider using a method that will select a subset of your predictors. A common way to do this is a penalized regression method like Lasso.

# Implementations

## Python

```python
'''Load R Datasets'''
mtcars = sm.datasets.get_rdataset("mtcars").data
# Fit OLS regression model to mtcars
ols = smf.ols(formula= 'mpg ~ cyl + hp + wt', data= mtcars).fit()
# Look at the OLS results
print(ols.summary())
```

## R

```r
# Load Data
data(mtcars)

# Run OLS using the mtcars data, with mpg as the outcome variable
# and cyl, hp, and wt as predictors
olsmodel <- lm(mpg ~ cyl + hp + wt, data = mtcars)

# Look at the results
summary(olsmodel)
```

## SAS

```sas
/* Load Data */
proc import datafile="C:mtcars.dbf"
   out=fromr dbms=dbf;
run;
/* OLS regression */
proc reg;
   model mpg = cyl hp wt;
run;
```

## Stata

```stata
* Load auto data
sysuse auto.dta

* Run OLS using the auto data, with mpg as the outcome variable
* and headroom, trunk, and weight as predictors
regress mpg headroom trunk weight
```

## Gretl

```gretl
# Load auto data
open auto.gdt

# Run OLS using the auto data, with mpg as the outcome variable
# and headroom, trunk, and weight as predictors
ols mpg const headroom trunk weight
```

## Matlab

```matlab
% Load auto data
load('auto.mat')

% Run OLS using the auto data, with mpg as the outcome variable
% and headroom, trunk, and weight as predictors

intercept = ones(length(headroom), 1);
X = [intercept headroom trunk weight];
[b, bint, r, rint, stats] = regress(mpg, X);
```
