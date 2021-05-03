---
title: Interaction Terms and Polynomials
parent: Ordinary Least Squares
grand_parent: Model Estimation ## Optional for indexing
has_children: false
nav_order: 2
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Interaction Terms and Polynomials

Regression models generally assume that the outcome variable is a function of an *index*, which is a linear function of the independent variables, for example in [ordinary least squares]({{ "/Model_Estimation/OLS/simple_linear_regression.html" | relative_url }}):

$$
Y = \beta_0+\beta_1X_1+\beta_2X_2
$$

However, if the independent variables have a nonlinear effect on the outcome, the model will be incorrectly specified. This is fine as long as that nonlinearity is modeled by including those nonlinear terms in the index. 

The two most common ways this occurs is by including interactions or polynomial terms. With an interaction, the effect of one variable varies according to the value of another:

$$
Y = \beta_0+\beta_1X_1+\beta_2X_2 + \beta_3X_1X_2
$$

and with polynomial terms, the effect of one variable one the outcome is allowed to take a non-linear shape:

$$
Y = \beta_0+\beta_1X_1+\beta_2X_2 + \beta_3X_2^2 + \beta_4X_2^3
$$

## Keep in Mind

- When you have interaction terms or polynomials, the effect of a variable can no longer be described with a single coefficient, and in some senses the individual coefficients lose meaning without the others. You can understand the effect of a single variable by taking the derivative of the index with respect to that variable. For example, in $$Y = \beta_0+\beta_1X_1+\beta_2X_2 + \beta_3X_1X_2$$, the effect of $$X_2$$ on $$Y$$ is $$\partial Y/\partial X_2 = \beta_2 + \beta_3X_1$$. You must plug in the value of $$X_1$$ to get the effect of $$X_2$$. Or in $$Y = \beta_0+\beta_1X_1+\beta_2X_2 + \beta_3X_2^2 + \beta_4X_2^3$$, the effect of $$X_2$$ is $$\partial Y/\partial X_2 = \beta_2 + 2\beta_3X_2 + 3\beta_4X_2^2$$. You must plug in a value of $$X_2$$ to get the marginal effect of $$X_2$$ at that value.
- In almost all cases, if you are including an interaction term, you should also include each of the interacted variables on their own. Otherwise, the coefficients become very difficult to interpret.
- In almost all cases, if you are including a polynomial, you should include all terms of the polynomial. In other words, include the linear and squared term, not just the squared term.

## Also Consider

- Interaction terms tend to have low statistical power. Consider performing a [power analysis of interaction terms]({{ "/Other/power_analysis_for_interactions.html" | relative_url }}) before running your analysis.
- Polynomials are not the only way to model a nonlinear relationship. You could, for example, run one of many kinds of [nonparametric regression]({{ "/Model_Estimation/nonparametric_regression.html" | relative_url }}).
- You may want to get the [average marginal effects]({{ "/Model_Estimation/average_marginal_effects.html" | relative_url }}) or the [marginal effects at the mean]({{ "/Model_Estimation/GLS/marginal_effects_at_the_mean.html" | relative_url }}) of your variables after running your model.
- One common way to display the effects of a model with interactions is to graph them. See [marginal effects plots for interactions with continuous variables]({{ "/Presentation/Figures/marginal_effects_plots_for_interactions_with_continuous_variables.html" | relative_url }}) and [Marginal effects plots for interactions with continuous variables]({{ "/Presentation/Figures/marginal_effects_plots_for_interactions_with_categorical_variables.html" | relative_url }})

# Implementations

## Python

Using the [**statsmodels**](https://www.statsmodels.org/stable/index.html) package, we can use a similar formulation as the `R` example below.

```python
# Standard imports
import numpy as np
import pandas as pd
import statsmodels.formula.api as sms
from matplotlib import pyplot as plt

# Load the R mtcars dataset from a URL
df = pd.read_csv('https://raw.githubusercontent.com/LOST-STATS/lost-stats.github.io/source/Data/mtcars.csv')

# Include a linear, squared, and cubic term using the I() function.
# N.B. Python uses ** for exponentiation (^ means bitwise xor)
model1 = sms.ols('mpg ~ hp + I(hp**2) + I(hp**3) + cyl', data=df)
print(model1.fit().summary())

# Include an interaction term and the variables by themselves using *
# The interaction term is represented by hp:cyl
model2 = sms.ols('mpg ~ hp * cyl', data=df)
print(model2.fit().summary())

# Equivalently, you can request "all quadratic interaction terms" by doing
model3 = sms.ols('mpg ~ (hp + cyl) ** 2', data=df)
print(model3.fit().summary())

# Include only the interaction term and not the variables themselves with :
# Hard to interpret! Occasionally useful though.
model4 = sms.ols('mpg ~ hp : cyl', data=df)
print(model4.fit().summary())
```

## R

```r
# Load mtcars data
data(mtcars)

# Include a linear, squared, and cubic term using the I() function
model1 <- lm(mpg ~ hp + I(hp^2) + I(hp^3) + cyl, data = mtcars)

# Include a linear, squared, and cubic term using the poly() function
# The raw = TRUE option will give the exact same result as model1
# Omitting this will give you orthogonal polynomial terms,
# which are not correlated with each other but are more difficult to interpret
model2 <- lm(mpg ~ poly(hp, 3, raw = TRUE) + cyl, data = mtcars)

# Include an interaction term and the variables by themselves using *
model3 <- lm(mpg ~ hp*cyl, data = mtcars)

# Include only the interaction term and not the variables themselves with :
# Hard to interpret! Occasionally useful though.
model4 <- lm(mpg ~ hp:cyl, data = mtcars)
```

## Stata

Stata allows interaction and polynomial terms using hashtags ## to join together variables to make interactions, or joining a variable with itself to get a polynomial. You must also specify whether each variable is continuous (prefix the variable with c.) or a factor (prefix with i.).

```stata
* Load auto data
sysuse auto.dta, clear

* Use ## to interact variables together and also include the variables individually
* foreign is a factor variable so we prefix it with i.
* weight is continuous so we prefix it with c.
reg mpg c.weight##i.foreign

* Use # to include just the interaction term and not the variables themselves
* If one is a factor, this will include the effect of the continuous variable
* For each level of the factor
reg mpg c.weight#i.foreign

* Interact a variable with itself to create a polynomial term
reg mpg c.weight##c.weight##c.weight foreign
```

