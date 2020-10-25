---
title: ARMA Models
parent: Time Series
has_children: false
mathjax: true
nav_order: 1
---

# Autoregressive Moving-Average (ARMA) Models

Auto regressive moving average (ARMA) models are a combination of two commonly used time series processes, the [autoregressive (AR)]({{ "/Time_Series/AR-models.html" | relative_url }}) process and the [moving-average (MA)]({{ "/Time_Series/MA-models.html" | relative_url }}) process. As such, ARMA models have the form

$$Y_t = c + \sum_{i = 1}^{p} \beta_i Y_{t-i} + \sum_{j = 1}^{q} \theta_j \varepsilon_{t-j} + \varepsilon_t $$

If an ARMA model has an AR component of order $$p$$ and an MA component of order $$q$$, then the model is commonly refered to as an $$ARMA(p,q)$$

For additional information, see [Wikipedia: Autoregressive Moving-Average model](https://en.wikipedia.org/wiki/Autoregressive%E2%80%93moving-average_model).

# Keep In Mind

- Data must be properly formatted for estimation as a time-series. See [creating a time series data set]({{ "/Time_Series/creating_time_series_dataset.html" | relative_url }}). If this is not done, then depending on your statistical package of choice, either your estimation will fail to execute or you will receive erroneous output.
- ARMA models include some number of lagged error terms from the MA component, which are inherently unobservable. Consequently these models cannot be estimated using OLS alone, unlike AR models.
- ARMA models are most commonly estimated using maximum likelihood estimation (MLE). One consequence of this is that, given some time series and some specified order $$(p,q)$$, the estimates obtained from the estimated $$ARMA(p,q)$$ model will vary depending on the type of MLE estimation used.
- As is the case in many situations where one is trying to estimate a time-series process, model selection is important. For ARMA models, model selection meaning chosing the number of AR and MA parameters, the $$p$$ and $$q$$, for which a coefficient will be estimated. In practice, it is common to estimate several different potential models, then use some criterion to determine which model best fits the time-series. Common criteria used to evaluate ARMA models are the Akaike Information Criterion (AIC) and the Bayesian Information Criterion (BIC), also referred to as the Schwarz Information Criterion (SIC). For more information on these and other model selection criteria, see [Wikipedia: Model Selection](https://en.wikipedia.org/wiki/Model_selection#Criteria).
- Estimating a time series using an ARMA model relies on two assumptions. The first is the standard assumption that we have selected the correct functional form for the time series. In this case, that means assuming that we have selected the correct $$p$$ and $$q$$. Second, we also have to assume that our time series is stationary. For a discussion of the stationarity assumption and what constraints this assumption imposes on our model, again see [Wikipedia: Autoregressive Moving-Average model](https://en.wikipedia.org/wiki/Autoregressive%E2%80%93moving-average_model).

# Also Consider

- ARMA models can only be estimated for univariate time series. If you are interested in estimating a time series process using multiple time series on the right hand side of your model, consider using a [vector AR (VAR)]({{ "/Time_Series/VAR-models.html" | relative_url }}) model or a [VARMA]({{ "/Time_Series/VARMA-models.html" | relative_url }}) model.
- Before estimating an ARMA model, it is standard practice to try to determine whether or not the time series appears to be stationary. See [LOST: Stationarity and Weak Dependence]({{ "/Time_Series/Stationarity-and-weak-dependence.html" | relative_url }}) for more details.
- If the time series you are trying to estimate does not appear to be stationary, then using an ARMA model to estimate the series is innappropriate. For simpler forms of nonstationarity, an ARIMA model may be useful. An $$ARIMA(p,d,q)$$ model is a more general model for a time-series than an $$ARMA(p,q)$$. In these models, $$p$$ still signifies an $$AR(p)$$ component, and $$q$$ an $$MA(q)$$ component. For more information on ARIMA models, see [Wikipedia: ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average). For information about estimating an ARIMA model, see [LOST: ARIMA models]({{ "/Time_Series/ARIMA-models.html" | relative_url }})


# Implementations

First, follow the [instructions]({{ "/Time_Series/creating_time_series_dataset.html" | relative_url }}) for creating and formatting time-series data using your software of choice. We will again use quarterly US GDP data downloaded from [FRED](https://fred.stlouisfed.org/series/GDPC1) as an example. This time, though, we will try to estimate the quarterly log change in GDP with an $$ARMA(3,1)$$ process. Note that an $$ARMA(3,1)$$ model is almost certainly not the best way to estimate this time series, and is used here solely as an example.

## Python

The [**statsmodels**](https://www.statsmodels.org/stable/index.html) library offers a way to fit ARIMA(p, d, q) models, with its `ARIMA` function. To get an ARMA model, just set $$d$$ to zero.

In the example below, we'll take the first difference of the log of the data, then fit a model with $$p=3$$ auto-regressive terms and $$q=1$$ moving average terms.


```python
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

gdp = pd.read_csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv",
                    index_col=0)

# Take 1st diff of log of gdp
d_ln_gdp = np.log(gdp).diff()

print(d_ln_gdp.head())
```

                   GDPC1
    DATE                
    1947-01-01       NaN
    1947-04-01 -0.002670
    1947-07-01 -0.002067
    1947-10-01  0.015521
    1948-01-01  0.014931


You can see that the first value is NaN. That's because, for the first value, there is no previous value to do the differencing with.

Let's fit the model:


```python
p = 3
d = 0
q = 1

mod = ARIMA(d_ln_gdp, order=(p, d, q))
res = mod.fit()
print(res.summary())
```

                                   SARIMAX Results                                
    ==============================================================================
    Dep. Variable:                  GDPC1   No. Observations:                  292
    Model:                 ARIMA(3, 0, 1)   Log Likelihood                 972.763
    Date:                        00:00:00   AIC                          -1933.526
    Time:                        00:00:00   BIC                          -1911.466
    Sample:                    01-01-1947   HQIC                         -1924.690
                             - 10-01-2019                                         
    Covariance Type:                  opg                                         
    ==============================================================================
                     coef    std err          z      P>|z|      [0.025      0.975]
    ------------------------------------------------------------------------------
    const          0.0077      0.001      9.163      0.000       0.006       0.009
    ar.L1          0.1918      0.417      0.461      0.645      -0.625       1.008
    ar.L2          0.1980      0.145      1.368      0.171      -0.086       0.482
    ar.L3         -0.0961      0.072     -1.332      0.183      -0.237       0.045
    ma.L1          0.1403      0.410      0.342      0.732      -0.663       0.944
    sigma2      7.301e-05   4.29e-06     17.006      0.000    6.46e-05    8.14e-05
    ===================================================================================
    Ljung-Box (L1) (Q):                   0.02   Jarque-Bera (JB):                59.78
    Prob(Q):                              0.90   Prob(JB):                         0.00
    Heteroskedasticity (H):               0.26   Skew:                             0.15
    Prob(H) (two-sided):                  0.00   Kurtosis:                         5.20
    ===================================================================================
    
    Warnings:
    [1] Covariance matrix calculated using the outer product of gradients (complex-step).



## R

There are numerous packages to estimate ARMA models in R. For this tutorial, we will use the `arima()` function, which comes preloaded into R from the **stats** package. For our purposes, it is sufficient to note that estimating an $$ARIMA(p,0,q)$$ model is largely equivalent to estimating an $$ARMA(p,q)$$. For more information about estimating a true ARIMA process (where $$d>0$$), see the *Also Consider* section above. Additionally, the **tsibble** package can also be used to easily construct our quarterly log change in GDP variable.

The `arima()` function does require that we specify the order of the model (ie, pick the values of $$p$$ and $$q$$). For an alternative function that will evaluate multiple models and select the best performing, see the `auto.arima` function available through the [**forecast** package](https://www.rdocumentation.org/packages/forecast/versions/8.11/topics/auto.arima).

```r
## Load and install time series packages
if (!require("tsibble")) install.packages("tsibble")
library(tsibble)


#load data
gdp = read.csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv")

#set our data up as a time-series
gdp$DATE <- as.Date(gdp$DATE)

gdp_ts <- as_tsibble(gdp,
                     index = DATE,
                     regular = FALSE) %>%
    index_by(qtr = ~ yearquarter(.))

#construct our first difference of log gdp variable
gdp_ts$lgdp=log(gdp_ts$GDPC1)

gdp_ts$ldiffgdp=difference(gdp_ts$lgdp, lag=1, difference=1)


#Estimate our ARMA(3,1)
##Note that because we are modeling for the first difference of log GDP, we cannot use our first observation of
##log GDP to estimate our model.
arma_gdp = arima(gdp_ts$lgdp[2:292], order=c(3,0,1))
arma_gdp
```

## Stata
In Stata we will again estimate an $$ARMA(p,q)$$ by estimating an $$ARIMA(p,0,q)$$ using the Stata command `arima`. This command works similarly to Stata's `reg` command. For information about the specific estimation procedure used by this function, optional arguments, etc, see [Stata: ARIMA manual](https://www.stata.com/manuals13/tsarima.pdf)

```stata
*load data

import delimited "https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv"

*Generate the new date variable

generate date_index = tq(1947q1) + _n-1

*Index the date variable as quarterly

format date_index %tq

*Convert a variable into time-series data
tsset date_index

*construct our first difference of log gdp variable

gen lgdp = ln(gdpc1)
gen dlgdp = D.lgdp

*Specify the ARMA model using the arima command
*Stata will automatically drop the first entry, since we do not have a value for the first difference of GDP
*for this entry.

arima dlgdp, arima(3,0,1)

```
