---
title: ARCH Model
parent: Time Series
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Autoregressive Conditional Heteroscedasticity (ARCH) model

The autoregressive conditional heteroscedasticity (ARCH) model is a statistical model for time series data that models the variance of the current error as a function of the actual sizes of the previous time periods' errors. The ARCH model is appropriate when the error variance in a time series follows an autoregressive (AR) model.

An ARCH(q) process can be written as $y_{t} = a_{0} + \sum_{i=1}^{q}y_{t-q}+\epislon_{t}$ where $\epsilon_{t}$ denote the error terms. These $\epsilon_{t}$ are split into a stochastic piece $z_{t}$ and a time-dependent standard deviation $\sigma_{t}$ characterizing the typical size of the terms so that $\epsilon_{t}=\sigma_{t}z_{t}$.
The random variable $z_{t}$ is a strong white noise process. The series $\sigma_{t}^{2}$ is modeled by
$$\sigma_{t}^{2} = \alpha_{0} + \alpha_{1}\epsilon_{t-1}^{2} + \dots + \alpha_{q}\epsilon_{t-1}^{2} = \alpha_{0} + \sum_{i=1}^{q}\alpha_{i}\epsilon_{t-i}^{2}$$ where $\alpha_{0} > 0$ and $\alpha_{i} \ geq 0$, $i > 0$.

An ARCH(q) model can be estimated using ordinary least squares. This procedure is as follows:

1. Estimate the best fitting autoregressive model AR(q) $$y_{t}=a_{0}+a_{1}y_{t-1}+\dots +a_{q}y_{t-q}+\epsilon_{t} =a_{0}+\sum_{i=1}^{q}a_{i}y_{t-i}+\epsilon_{t}$$.

2. Obtain the squares of the error $\hat{\epsilon}^{2}$ and regress them on a constant and q lagged values:
$$\hat{\epsilon}^{2}=\hat {\alpha}_{0}+\sum_{i=1}^{q}\hat{\alpha}_{i}\hat{\epsilon}_{t-i}^{2}$$
where q is the length of ARCH lags.

3. Null Hypothesis: $\alpha_{i}=0$ for all $i=1,\dots ,q$. Alternative hypothesis : At least one of the estimated $\alpha_{i}$ coefficients must be significant. Under the null hypothesis of no ARCH errors, the test statistic $T'R²$ follows $\chi^{2}$ distribution with q degrees of freedom, where $T'$ is the number of equations in the model which fits the residuals vs the lags (i.e. $T'=T-q$). If $T'R²$ is greater than the Chi-square table value, we reject the null hypothesis and conclude there is an ARCH effect, otherwise we do not reject the null hypothesis.

For additional information, see [Wikipedia: Autoregressive conditional heteroskedasticity](https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity#ARCH(q)_model_specification).

## Keep in Mind

- Data should be properly formatted for estimation as a time-series. See [creating a time series data set]({{ "/Time_Series/creating_time_series_dataset.html" | relative_url }}). If not, you may fail to execute  or receive erroneous output.
- ARCH can be used to model time-varying conditional variance.

## Also Consider

- ARCH models can be univariate (scalar) or multivariate (vector). 
- ARCH models are commonly employed in modeling financial time series that exhibit time-varying volatility and volatility clustering, i.e. periods of swings interspersed with periods of relative calm.
- If an autoregressive moving average (ARMA) model is assumed for the error variance, the model is a generalized autoregressive conditional heteroskedasticity (GARCH) model. For more information on GARCH models, see [Wikipedia: GARCH](https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity#GARCH). For information about estimating an GARCH models, see [LOST: GARCH models]({{ "/Time_Series/GARCH" | relative_url }}-models.html).

# Implementations

## Python

```py
from random import gauss
from random import seed
from matplotlib import pyplot
from arch import arch_model
import numpy as np
# seed the process
np.random.seed(1)
# Simulating a ARCH(1) process
a0 = 1
a1 = .5
w = np.random.normal(size=1000)
e = np.random.normal(size=1000)
Y = np.empty_like(w)
for t in range(1, len(w)):
    Y[t] = w[t] * np.sqrt((a0 + a1*Y[t-1]**2))
# fit model
model = arch_model(Y, vol = "ARCH", rescale = "FALSE")
model_fit = model.fit()
print(model_fit.summary)
```

## R

```r
# setup
library(fGarch)
# seed pseudorandom number generator
set.seed(1)
# Simulating a ARCH(1) process
e <- NULL
obs <- 1000
e[1] <- rnorm(1)
for (i in 2:obs) {e[i] <- rnorm(1)*(1+0.5*(e[i-1])^2)^0.5}
# fit the model
arch.fit <- garchFit(~garch(1,0), data = e, trace = F)
summary(arch.fit)
```

## Stata

```stata
* seed pseudorandom number generator
set seed 1
* Simulating a ARCH(1) process
set obs 1000
gen time=_n
tsset time
gen e=.
replace e=rnormal() if time==1
replace e=rnormal()*(1 + .5*(e[_n-1])^2)^.5 if time>=2 & time<=2000
* Estimate arch parameters.. 
arch e, arch(1)
```
