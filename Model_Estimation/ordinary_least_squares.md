---
title: Ordinary Least Squares (Linear Regression)
parent: Model Estimation
has_children: false
nav_order: 1
mathjax: true
---

# Ordinary Least Squares (Linear Regression)

Ordinary Least Squares (OLS) is a statistical method that produces a best-fit line between some outcome variable $$Y$$ and any number of predictor variables $$X_1, X_2, X_3, ...$$. These predictor variables may also be called independent variables or right-hand-side variables.

For more information about OLS, see [Wikipedia: Ordinary Least Squares](https://en.wikipedia.org/wiki/Ordinary_least_squares).

## Keep in Mind

- OLS assumes that you have specified a true linear relationship.
- OLS results are not guaranteed to have a causal interpretation. Just because OLS estimates a positive relationship between $$X_1$$ and $$Y$$ does not necessarily mean that an increase in $$X_1$$ will cause $$Y$$ to increase.
- OLS does *not* require that your variables follow a normal distribution. 

## Also Consider

- OLS standard errors assume that the model's error term is [IID](https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables), which may not be true. Consider whether your analysis should use [heteroskedasticity-robust standard errors](https://lost-stats.github.io/Model_Estimation/Nonstandard_Errors/hc_se.html) or [cluster-robust standard errors](https://lost-stats.github.io/Model_Estimation/Nonstandard_Errors/clustered_se.html).
- If your outcome variable is discrete or bounded, then OLS is by nature incorrectly specified. You may want to use [probit](https://lost-stats.github.io/Model_Estimation/probit_model.html) or [logit](https://lost-stats.github.io/Model_Estimation/logit_model.html) instead for a binary outcome variable, or [ordered probit](https://lost-stats.github.io/Model_Estimation/ordered_probit.html) or [ordered logit](https://lost-stats.github.io/Model_Estimation/ordered_logit.html) for an ordinal outcome variable.
- If the goal of your analysis is predicting the outcome variable and you have a very long list of predictor variables, you may want to consider using a method that will select a subset of your predictors. A common way to do this is a [penalized regression method](https://lost-stats.github.io/Machine_Learning/penalized_regression.html) like LASSO.
- In many contexts, you may want to include [interaction terms or polynomials](https://lost-stats.github.io/Model_Estimation/interaction_terms_and_polynomials.html) in your regression equation.

# Implementations


## Gretl

```gretl
# Load auto data
open https://github.com/LOST-STATS/lost-stats.github.io/blob/master/Data/auto.gdt

# Run OLS using the auto data, with mpg as the outcome variable
# and headroom, trunk, and weight as predictors
ols mpg const headroom trunk weight
```

## Matlab

```matlab
% Load auto data
load('https://github.com/LOST-STATS/lost-stats.github.io/blob/master/Data/auto.mat')

% Run OLS using the auto data, with mpg as the outcome variable
% and headroom, trunk, and weight as predictors

intercept = ones(length(headroom),1);
X = [intercept headroom trunk weight];
[b,bint,r,rint,stats] = regress(mpg,X);
```

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
# data(mtcars) ## Optional: automatically loaded anyway

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
sysuse https://github.com/LOST-STATS/lost-stats.github.io/blob/master/Data/auto.dta

* Run OLS using the auto data, with mpg as the outcome variable
* and headroom, trunk, and weight as predictors
regress mpg headroom trunk weight
```
