---
title: Penalized Regression
parent: Machine Learning
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Penalized Regression

When running a regression, especially one with many predictors, the results have a tendency to overfit the data, reducing out-of-sample predictive properties. 

Penalized regression eases this problem by forcing the regression estimator to shrink its coefficients towards 0 in order to avoid the "penalty" term imposed on the coefficients. This process is closely related to the idea of Bayesian shrinkage, and indeed standard penalized regression results are equivalent to regression performed using [certain Bayesian priors](https://amstat.tandfonline.com/doi/abs/10.1198/016214508000000337?casa_token=DE6O93Bz7uUAAAAA:Ff_MiPXvPH32NA2hnGtZtqb8grXEiEqF0fdO3B0p_a6wOaqRciCZ4ASwxn69gdOb93Lbt-HSyK1o4As).

Regular OLS selects coefficients $$\hat{\beta}$$ to minimize the sum of squared errors:

$$
\min\sum_i(y_i - X_i\hat{\beta})^2
$$

Non-OLS regressions similarly select coefficients to minimize a similar objective function. Penalized regression adds a penalty term $$\lambda\lVert\beta\rVert_p$$ to that objective function, where $$\lambda$$ is a tuning parameter that determines how harshly to penalize coefficients, and $$\lVert\beta\rVert_p$$ is the $$p$$-norm of the coefficients, or $$\sum_j\lvert\beta\rvert^p$$.

$$
\min\left(\sum_i(y_i - X_i\hat{\beta})^2 + \lambda\left\lVert\beta\right\rVert_p \right)
$$

Typically $$p$$ is set to 1 for LASSO regression (least absolute shrinkage and selection operator), which has the effect of tending to set coefficients to 0, i.e. model selection, or to 2 for Ridge Regression. Elastic net regression provides a weighted mix of LASSO and Ridge penalties, commonly referring to the weight as $$\alpha$$. 

## Keep in Mind

- To avoid being penalized for a constant term, or by differences in scale between variables, it is a very good idea to standardize each variable (subtract the mean and divide by the standard deviation) before running a penalized regression.
- Penalized regression can be run for logit and other kinds of regression, not just linear regression. Using penalties with general linear models like logit is common.
- Penalized regression coefficients are designed to improve out-of-sample prediction, but they are biased. If the goal is estimation of a parameter, rather than prediction, this should be kept in mind. A common procedure is to use LASSO to select variables, and then run regular regression models with the variables that LASSO has selected.
- The $$\lambda$$ parameter is often chosen using cross-validation. Many penalized regression commands include an option to select $$\lambda$$ by cross-validation automatically.
- LASSO models commonly include variables along with polynomial transformation of those variables and interactions, allowing LASSO to determine which transformations are worth keeping.

## Also Consider

- If it is not important to estimate coefficients but the goal is simply to predict an outcome, then there are many other [machine learning]({{ "/Machine_Learning/Machine_Learning.html" | relative_url }}) methods that do so, and in some cases can handle higher dimensionality or work with smaller samples.

# Implementations

## R

We will use the **glmnet** package.

```r
# Install glmnet and tidyverse if necessary
# install.packages('glmnet', 'tidyverse')

# Load glmnet
library(glmnet)

# Load iris data
data(iris)

# Create a matrix with all variables other than our dependent vairable, Sepal.Length
# and interactions. 
# -1 to omit the intercept
M <- model.matrix(lm(Sepal.Length ~ (.)^2 - 1, data = iris))
# Add squared terms of numeric variables
numeric.var.names <- names(iris)[2:4]
M <- cbind(M,as.matrix(iris[,numeric.var.names]^2))
colnames(M)[16:18] <- paste(numeric.var.names,'squared')

# Create a matrix for our dependent variable too
Y <- as.matrix(iris$Sepal.Length)

# Standardize all variables
M <- scale(M)
Y <- scale(Y)


# Use glmnet to estimate penalized regression
# We pick family = "gaussian" for linear regression;
# other families work for other kinds of data, like binomial for binary data
# In each case, we use cv.glmnet to pick our lambda value using cross-validation
# using nfolds folds for cross-validation
# Note that alpha = 1 picks LASSO
cv.lasso <- cv.glmnet(M, Y, family = "gaussian", nfolds = 20, alpha = 1)
# We might want to see how the choice of lambda relates to out-of-sample error with a plot
plot(cv.lasso)
# After doing CV, we commonly pick the lambda.min for lambda, 
# which is the lambda that minimizes out-of-sample error
# or lambda.1se, which is one standard error above lambda.min,
# which penalizes more harshly. The choice depends on context.
lasso.model <- glmnet(M, Y, family = "gaussian", alpha = 1, lambda = cv.lasso$lambda.min)
# coefficients are shown in the beta element. . means LASSO dropped it
lasso.model$beta

# Running Ridge, or mixing the two with elastic net, simply means picking
# alpha = 0 (Ridge), or 0 < alpha < 1 (Elastic Net)
cv.ridge <- cv.glmnet(M, Y, family = "gaussian", nfolds = 20, alpha = 0)
ridge.model <- glmnet(M, Y, family = "gaussian", alpha = 0, lambda = cv.ridge$lambda.min)

cv.elasticnet <- cv.glmnet(M, Y, family = "gaussian", nfolds = 20, alpha = .5)
elasticnet.model <- glmnet(M, Y, family = "gaussian", alpha = .5, lambda = cv.elasticnet$lambda.min)
```

## Stata

Penalized regression is one of the few machine learning algorithms that Stata does natively. This requires Stata 16. If you do not have Stata 16, you can alternately perform some forms of penalized regression by installing the **lars** package using **ssc install lars**.

```stata
* Use NLSY-W data
sysuse nlsw88.dta, clear

* Construct all squared and interaction terms by loop so we don't have to specify them all
* by hand in the regression function
local numeric_vars = "age grade hours ttl_exp tenure"
local factor_vars = "race married never_married collgrad south smsa c_city industry occupation union"

* Add all squares
foreach x in `numeric_vars' {
	g sq_`x' = `x'^2
}

* Turn all factors into dummies so we can standardize them
local faccount = 1
local dummy_vars = ""
foreach x in `factor_vars' {
	xi i.`x', pre(f`count'_)
	local count = `count' + 1
}

* Add all numeric-numeric interactions; these are easy
* factor interactions would need a more thorough loop
forvalues i = 1(1)5 {
	local next_i = `i'+1
	forvalues j = `next_i'(1)5 {
		local namei = word("`numeric_vars'",`i')
		local namej = word("`numeric_vars'",`j')
		g interact_`i'_`j' = `namei'*`namej'
	}
}

* Standardize everything
foreach var of varlist `numeric_vars' f*_* interact_* {
	qui summ `var'
	qui replace `var' = (`var' - r(mean))/r(sd)
}

* Use the lasso command to run LASSO
* using sel(cv) to select lambda using cross-validation
* we specify a linear model here, but logit/probit/poisson would work
lasso linear wage `numeric_vars' f*_* interact_*, sel(cv)
* get list of included coefficients
lassocoef

* We can use elasticnet to run Elastic Net
* By default, alpha will be selected by cross-validation as well
elasticnet linear wage `numeric_vars' f*_* interact_*, sel(cv)
```
