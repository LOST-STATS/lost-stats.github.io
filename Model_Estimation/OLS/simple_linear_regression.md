---
title: Simple Linear Regression
parent: Ordinary Least Squares
grand_parent: Model Estimation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true
---

# Simple Linear Regression

Ordinary Least Squares (OLS) is a statistical method that produces a best-fit line between some outcome variable $$Y$$ and any number of predictor variables $$X_1, X_2, X_3, ...$$. These predictor variables may also be called independent variables or right-hand-side variables.

For more information about OLS, see [Wikipedia: Ordinary Least Squares](https://en.wikipedia.org/wiki/Ordinary_least_squares).

## Keep in Mind

- OLS assumes that you have specified a true linear relationship.
- OLS results are not guaranteed to have a causal interpretation. Just because OLS estimates a positive relationship between $$X_1$$ and $$Y$$ does not necessarily mean that an increase in $$X_1$$ will cause $$Y$$ to increase.
- OLS does *not* require that your variables follow a normal distribution. 

## Also Consider

- OLS standard errors assume that the model's error term is [IID](https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables), which may not be true. Consider whether your analysis should use [heteroskedasticity-robust standard errors]({{ "/Model_Estimation/Statistical_Inference/Nonstandard_Errors/hc_se.html" | relative_url }}) or [cluster-robust standard errors]({{ "/Model_Estimation/Statistical_Inference/Nonstandard_Errors/clustered_se.html" | relative_url }}).
- If your outcome variable is discrete or bounded, then OLS is by nature incorrectly specified. You may want to use [probit]({{ "/Model_Estimation/GLS/probit_model.html" | relative_url }}) or [logit]({{ "/Model_Estimation/GLS/logit_model.html" | relative_url }}) instead for a binary outcome variable, or [ordered probit]({{ "/Model_Estimation/GLS/ordered_probit.html" | relative_url }}) or [ordered logit]({{ "/Model_Estimation/GLS/ordered_logit.html" | relative_url }}) for an ordinal outcome variable.
- If the goal of your analysis is predicting the outcome variable and you have a very long list of predictor variables, you may want to consider using a method that will select a subset of your predictors. A common way to do this is a [penalized regression method]({{ "/Machine_Learning/penalized_regression.html" | relative_url }}) like LASSO.
- In many contexts, you may want to include [interaction terms or polynomials]({{ "/Model_Estimation/OLS/interaction_terms_and_polynomials.html" | relative_url }}) in your regression equation.

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
# Use 'pip install statsmodels' or 'conda install statsmodels'
# on the command line to install the statsmodels package.

# Import the relevant parts of the package:
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Get the mtcars example dataset
mtcars = sm.datasets.get_rdataset("mtcars").data

# Fit OLS regression model to mtcars
ols = smf.ols(formula='mpg ~ cyl + hp + wt', data=mtcars).fit()

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
