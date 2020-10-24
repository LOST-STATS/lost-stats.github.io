---
title: GARCH Model
parent: Time Series
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---
  
# Generalized Autoregressive Conditional Heteroscedasticity (GARCH) model
Generalized AutoRegressive Conditional Heteroskedasticity (GARCH) is a statistical model used in analyzing time-series data where the variance error is believed to be serially autocorrelated. GARCH models assume that the variance of the error term follows an autoregressive moving average process.

GARCH (p, q) model (where p is the order of the GARCH terms $\sigma^{2}$ and q is the order of the ARCH terms $\epsilon^{2}$) is a model which $\epsilon_{t}$, the error terms, can be split into a stochastic piece $z_{t}$ and a time-dependent standard deviation $\sigma_{t}$ characterizing the typical size of the terms so that $\epsilon_{t}=\sigma_{t}z_{t}$.
The random variable $z_{t}$ is a strong white noise process while $\sigma_{t}^{2}$ is an ARMA process, i.e., 
$$\sigma_{t}^{2} = \alpha_{0} + \sum_{i=1}^{q}\alpha_{i}\epsilon_{t-i}^{2} + \sum_{i=1}^{p}\beta_{i}\sigma_{t-i}^{2}$$.


# Keep in Mind
- Data should be properly formatted for estimation as a time-series. See [creating a time series data set]({{ "/Time_Series/creating_time_series_dataset.html" | relative_url }}). If not, you may fail to execute  or receive erroneous output.
- GARCH is appropriate for time series data where the variance of the error term is serially autocorrelated following an autoregressive moving average process. 

# Also Consider
- GARCH can be used to help predict the volatility of returns on financial assets.
- GARCH is useful to assess risk and expected returns for assets that exhibit clustered periods of volatility in returns.
- If an autoregressive(AR) model is assumed for the error variance, the model is an autoregressive conditional heteroskedasticity (ARCH) model. For more information on GARCH models, see [Wikipedia: ARCH](https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity#ARCH(q)_model_specification). For information about estimating an ARCH model, see [LOST: ARCH models]({{ "/Time_Series/ARCH" | relative_url }}-models.html).


# Implementations

## Python

```py
# setup
from random import gauss
from random import seed
from matplotlib import pyplot
from arch import arch_model
import numpy as np
# seed the process
np.random.seed(1)
# Simulating a GARCH(1, 1) process
a0 = 0.2
a1 = 0.5
b1 = 0.3
n = 1000
w = np.random.normal(size=n)
eps = np.zeros_like(w)
sigsq = np.zeros_like(w)
for i in range(1, n):
    sigsq[i] = a0 + a1*(eps[i-1]**2) + b1*sigsq[i-1]
    eps[i] = w[i] * np.sqrt(sigsq[i])
model = arch_model(eps)
model_fit = model.fit()
print(model_fit.summary)
```

## R

```r
# setup
library(fGarch)
# seed pseudorandom number generator
set.seed(1)
# Simulating a GARCH(1,1) process
a0 <- 0.2
a1 <- 0.5
b1 <- 0.3
obs <- 1000
eps <- rep(0, obs)
sigsq <- rep(0,obs)
for (i in 2:obs) {
  sigsq[i] = a0 + a1*(eps[i-1]^2) + b1*sigsq[i-1]
  eps[i] <- rnorm(1)*sqrt(sigsq[i])}

# fit the model
garch.fit <- garchFit(~garch(1,1), data = eps, trace = F)
summary(garch.fit)
```
