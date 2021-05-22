---
title: "Rolling Regression"
parent: Time Series
nav_order: 1
mathjax: no
has_children: no
---

# Rolling Regression

Rolling regressions are one of the best and simplest models to to analyze changing relationships among variables overtime. It utilize the linear regression but allows certain parts of the data set used to constantly change. In most linear regression models parameters are assumed to be time-invariant and thus should not change overtime. Rolling regression can test this by finding a models parameters using a fixed window of time over the entire data set. A larger sample size, or window, used will result in less less parameter estimates but utilize more observations. For more information, see [Base on Rolling](https://factorpad.com/fin/glossary/rolling-regression.html#:~:text=Rolling%20Regression%20is%20an%20analysis,generated%20from%20a%20linear%20regression.&text=For%20context%2C%20recall%20that%20measures,in%20Finance%20change%20over%20time.)

## Keep in Mind
- When setting the width of your rolling regression you are also creating the starting position of your analysis given that it needs the a window sized amount of data begin.

## Also Consider
- An expanding window can be used where instead of a constantly changing fixed window, the regression starts with a predetermined time and then continually adds in other observations until the entire data set is used.


# Implementation

## R

In R the **rollRegres** (one s, not two) package has a fast and efficient way to compute rolling regressions while being able to specify the linear regression, window size, whether you want a rolling or expanding window, the minimum number of observations required in a window and others.

```r?example=roll_regress
#Load in the packages
library(pacman)
p_load(rollRegres,tidyr,dplyr)
```

The data will be manually created where x can be interpreted as any independent variable over a fixed time period, and y is an outcome variable.
```r?example=roll_regress
#Simulate data
set.seed(29132867)
n <- 200
p <- 2
X <- cbind(1, matrix(rnorm(p * n), ncol = p))
y <- drop(X %*% c(1, -1, 1)) + rnorm(n)
df_1 <- data.frame(y, X[, -1])

#Run the rolling regression (Rolling window)
roll_rolling <- roll_regres(y ~ X1, df_1, width = 25L,do_downdates = TRUE)

#Check the first 10 coefficients
roll_rolling$coefs %>% tail(25)
```


To demonstrate the note about a starting position for your analysis, these are all blank because there aren't enough lags in the data for them to be included.

```?example=roll_regress
#Check the first 25 coefficients
roll_rolling$coefs %>% head(25)
```

Finally, we can show the different results when using an expanding window

```?example=roll_regress
#Run the rolling regression (Rolling window)
roll_expanding <- roll_regres(y ~ X1, df_1, width = 25L,do_downdates = FALSE)

#Check the last 10 coefficients
roll_expanding$coefs %>% tail(10)
```



