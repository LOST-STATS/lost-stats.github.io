---
title: Quantile Regression
parent: Ordinary Least Squares
grand_parent: Model Estimation ## Optional for indexing
has_children: false
nav_order: 4
mathjax: true
---

# Quantile Regression
  
Quantile Regression is an extension of linear regression analysis. Quantile Regression differs from OLS in how it estimates the response variable. OLS estimates the conditional mean of the $$Y$$ across the predictor variables ($$X_1, X_2, X_3...$$), whereas quantile regression estimates the conditional median (or quantiles) of the $$Y$$ across the predictor variables ($$X_1, X_2, X_3...$$). It is useful in situations where OLS assumptions are not met (heteroskedasticity, bi-modal or skewed distribution). To specify the desired quantile, select a $$\tau$$ value between 0 to 1 (.5 gives median).
  
For more information on Quantile Regression, see [Wikipedia: Quantile Regression](https://en.wikipedia.org/wiki/Quantile_regression)
  
## Keep in Mind
  
- This method allows for the dependent variable to have any distributional form, however it cannot be a dummy variable and must be continuous.
- This method is robust to outliers, so there is no need to remove outlier observations.
- Either the intercept term or at least one predictor is required to run an analysis.
- [LASSO](https://en.wikipedia.org/wiki/Lasso_(statistics)) regression cannot be used for feature selection in this framework due to it requiring OLS assumptions to be satisfied.
- This method does not restrict the use of polynomial or interaction terms, a unique functional form can be specified.
  
## Also Consider
  
- While Quantile Regression can be useful in applications where OLS assumptions are not met, it can actually be used to detect heteroskedasticity. This makes is a useful tool to ensure this assumption is met for OLS.
- Several different standard error calculations can be used with this method, however [bootstrapped standard errors](https://en.wikipedia.org/wiki/Bootstrapping_(statistics)) are generally the best for complex modeling situations. [Clustered standard errors](https://en.wikipedia.org/wiki/Clustered_standard_errors) are also possible by estimating a quantile regression with pooled OLS clustered errors.
- Quantile regression works with baysnian methods as well.
  
# Implementations
  
## R
The main package to implement Quantile Regression in R is through the `quantreg` package. The main function in this package is `qr()`, which fits a Quantile Regression model with a default $$\tau$$ value of .5 but can be changed.

```r
# Load package
library(quantreg)

# Load data
data(mtcars)

# Run quantile regression with mpg as outcome variable
# and cyl, hp, and wt as predictors
# Using a tau value of .2 for quantiles
quantreg_model = rq(mpg ~ cyl + hp + wt, data = mtcars, tau = .2)

# Look at results
summary(quantreg_model)
```

