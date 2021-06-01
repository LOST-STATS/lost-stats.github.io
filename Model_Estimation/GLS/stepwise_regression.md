---
title: Stepwise Regression
parent: Generalised Least Squares
has_children: false
nav_order: 1
mathjax: true 
---

# Stepwise Regression

When we use multiple explanatory variables to perform regression analysis on a dependent variable, there is a great possibility that the problem of multicollinearity will occur. However, multiple linear regression requires that the correlation between the independent variables is not too high, so we need a method to eliminate multicollinearity and select the "optimal" regression equation. That is stepwise regression. It can automatically help us retain the most important explanatory variables and remove relatively unimportant variables from the model. 


The idea of stepwise regression is to introduce independent variables one by one, and after each independent variable is introduced, the selected variables are tested one by one. If the originally introduced variable is no longer significant due to the introduction of subsequent variables, then delete it. Repeat this process until the regression equation does not introduce insignificant independent variables and does not remove significant independent variables, then the optimal regression equation can be obtained.

## Keep in Mind


- The purpose of stepwise regression is to find which combination of variables can explain more changes in dependent variables.

- Stepwise regression is to observe statistical values, such as R-square, t-stats, and AIC indicators to identify important variables. 

- There are three methods of stepwise regression: Forward Selection, Backward Elimination and Stepwise Selection.

- Forward selection starts from the most important independent variable in the model, and then increases the variable in each step. 

- Backward elimination starts with all the independent variables of the model, and then removes the least significant variable at each step.

- The standard stepwise selection combines the above two methods, adding or removing independent variables in each step.

## Also Consider

- When our model has an overfitting problem, penalized regression is a good model-selection method. 

- The idea is penalizing the model for coefficients as they move away from zero, so so we can force the regression estimator to shrink its coefficient to 0.

- The optimal penalty will balance reduced model's variance with increased bias.


# Implementations

## R

We will use the build-in mtcars dataset, and the step() function in package "stats" can help us to do the stepwise regression. 

### Set up

```r
# Load package

library(stats)
library(broom)

# Load data and take a look at this dataset
data(mtcars)
head(mtcars)

#                    mpg cyl disp  hp drat    wt  qsec vs am gear carb
# Mazda RX4         21.0   6  160 110 3.90 2.620 16.46  0  1    4    4
# Mazda RX4 Wag     21.0   6  160 110 3.90 2.875 17.02  0  1    4    4
# Datsun 710        22.8   4  108  93 3.85 2.320 18.61  1  1    4    1
# Hornet 4 Drive    21.4   6  258 110 3.08 3.215 19.44  1  0    3    1
# Hornet Sportabout 18.7   8  360 175 3.15 3.440 17.02  0  0    3    2
# Valiant           18.1   6  225 105 2.76 3.460 20.22  1  0    3    1

# Define a regression model mpg ~ all other independent variables.
reg_mpg <- lm(mpg ~ ., data=mtcars)

# Define intercept model
intercept <- lm(mpg ~ 1, data=mtcars)
```

### Stepwise Selection
```r
# Stepwise selection

stepwise <- step(intercept, direction = c("both"), scope=formula(reg_mpg))

# Start:  AIC=115.94
# mpg ~ 1

#        Df Sum of Sq     RSS     AIC
# + wt    1    847.73  278.32  73.217
# + cyl   1    817.71  308.33  76.494
# + disp  1    808.89  317.16  77.397
# + hp    1    678.37  447.67  88.427
# + drat  1    522.48  603.57  97.988
# + vs    1    496.53  629.52  99.335
# + am    1    405.15  720.90 103.672
# + carb  1    341.78  784.27 106.369
# + gear  1    259.75  866.30 109.552
# + qsec  1    197.39  928.66 111.776
# <none>              1126.05 115.943

# Omit the filter in the middle...

# Step:  AIC=62.66
# mpg ~ wt + cyl + hp

#        Df Sum of Sq    RSS    AIC
# <none>              176.62 62.665
# - hp    1    14.551 191.17 63.198
# + am    1     6.623 170.00 63.442
# + disp  1     6.176 170.44 63.526
# - cyl   1    18.427 195.05 63.840
# + carb  1     2.519 174.10 64.205
# + drat  1     2.245 174.38 64.255
# + qsec  1     1.401 175.22 64.410
# + gear  1     0.856 175.76 64.509
# + vs    1     0.060 176.56 64.654
# - wt    1   115.354 291.98 76.750

```
```r
# Result
tidy(stepwise)

#   A tibble: 4 x 5
#   term        estimate std.error statistic  p.value
#   <chr>          <dbl>     <dbl>     <dbl>    <dbl>
# 1 (Intercept)  38.8       1.79       21.7  4.80e-19
# 2 wt           -3.17      0.741      -4.28 1.99e- 4
# 3 cyl          -0.942     0.551      -1.71 9.85e- 2
# 4 hp           -0.0180    0.0119     -1.52 1.40e- 1


```

The optimal equation we get from stepwise selection is 
$$mpg = 38.752 - 3.167*wt - 0.942*cyl - 0.018*hyp
$$


### Forward Selection And Backward Selection

The standard function for step is step(object, direction, scope, trace..). To use forward selection or backward selection, we just need to switch the object (regression) and choose the direction (forward or backward). 