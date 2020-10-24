---
title: AR Models
parent: Time Series
has_children: false
mathjax: true
nav_order: 1
---

# Autoregressive (AR) Models

Autoregressive (AR) models are fundamental to time series analysis. They are estimated via regressing a variable on one or more of its lagged values. That is, AR models take the form: $$Y_t = c + \sum_{i = 1}^{p} \beta_i Y_{t-i} + \epsilon_t $$ Where we say p is the *order* of our auto regression. Their estimation in statistical software packages is generally straightforward.

For additional information, see [Wikipedia: Autoregressive model](https://en.wikipedia.org/wiki/Autoregressive_model).

## Keep In Mind

- An AR model can be univariate (scalar) or multivariate (vector). This may be important to implementing an AR model in your statisical package of choice.  
- Data should be properly formatted before estimation. If not, non-time series objects (e.g., a date column) may be interpereted by software as a time series variable, leading to erroneous output. 

# Implementations

Following the [instructions]({{ "/Time_Series/creating_time_series_dataset.html" | relative_url }}) for creating and formatting Time Series Data, we will use quaterly GDP data downloaded from [FRED](https://fred.stlouisfed.org/series/GDPC1) as an example.

## Python

In Python, the
[**statsmodels**](https://www.statsmodels.org/stable/index.html) package
provides a range of tools to fit models using maximum likelihood
estimation. In the example below, we will use the `AutoReg` function. This
can fit models of the form:

$$

y_t = \delta_0 + \delta_1 t + \phi_1 y_{t-1} + \ldots + \phi_p y_{t-p} + \sum_{i=1}^{s-1} \gamma_i d_i + \sum_{j=1}^{m} \kappa_j x_{t,j} + \epsilon_t.

$$

where $$d_i$$ are seasonal dummies, $$x_{t,j}$$ are exogenous regressors, and the $$\phi_p$$ are the coefficients of the auto-regressive components of the model.

Using GDP data, let’s fit an auto-regressive model of order 1, an AR(1), with `AutoReg`:

```python
# Install pandas and statsmodels using 'pip install' or 'conda install' on the command line
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg, ar_select_order

gdp = pd.read_csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv",
                    index_col=0)
ar1_model = AutoReg(gdp, 1)
results = ar1_model.fit()
print(results.summary())
```

    ##                             AutoReg Model Results                             
    ## ==============================================================================
    ## Dep. Variable:                  GDPC1   No. Observations:                  292
    ## Model:                     AutoReg(1)   Log Likelihood               -1625.980
    ## Method:               Conditional MLE   S.D. of innovations             64.626
    ## Date:                0000000000000000   AIC                              8.358
    ## Time:                        00:00:00   BIC                              8.396
    ## Sample:                    04-01-1947   HQIC                             8.373
    ##                          - 10-01-2019                                         
    ## ==============================================================================
    ##                  coef    std err          z      P>|z|      [0.025      0.975]
    ## ------------------------------------------------------------------------------
    ## intercept     21.8083      7.439      2.931      0.003       7.227      36.389
    ## GDPC1.L1       1.0043      0.001   1356.492      0.000       1.003       1.006
    ##                                     Roots                                    
    ## =============================================================================
    ##                   Real          Imaginary           Modulus         Frequency
    ## -----------------------------------------------------------------------------
    ## AR.1            0.9957           +0.0000j            0.9957            0.0000
    ## -----------------------------------------------------------------------------

Now let’s use the automatic option to choose how many lags to include (this uses the BIC criterion to choose, though over criteria are available):

```python
select_model = ar_select_order(gdp, maxlag=10)
print(select_model.ar_lags)
```
    ## [1 2 3]

This tells us to include lags up to 3. We can pass the list of lags right back to the
`Auto_Reg` function:

```python
arp_model = AutoReg(gdp, select_model.ar_lags)
results_p = arp_model.fit()
print(results_p.summary())
```

    ##                             AutoReg Model Results                             
    ## ==============================================================================
    ## Dep. Variable:                  GDPC1   No. Observations:                  292
    ## Model:                     AutoReg(3)   Log Likelihood               -1593.285
    ## Method:               Conditional MLE   S.D. of innovations             59.989
    ## Date:                0000000000000000   AIC                              8.223
    ## Time:                        00:00:00   BIC                              8.286
    ## Sample:                    10-01-1947   HQIC                             8.248
    ##                          - 10-01-2019                                         
    ## ==============================================================================
    ##                  coef    std err          z      P>|z|      [0.025      0.975]
    ## ------------------------------------------------------------------------------
    ## intercept     13.3707      7.098      1.884      0.060      -0.541      27.282
    ## GDPC1.L1       1.2921      0.058     22.273      0.000       1.178       1.406
    ## GDPC1.L2      -0.1253      0.095     -1.315      0.189      -0.312       0.062
    ## GDPC1.L3      -0.1646      0.058     -2.826      0.005      -0.279      -0.050
    ##                                     Roots                                    
    ## =============================================================================
    ##                   Real          Imaginary           Modulus         Frequency
    ## -----------------------------------------------------------------------------
    ## AR.1            0.9960           +0.0000j            0.9960            0.0000
    ## AR.2            1.7430           +0.0000j            1.7430            0.0000
    ## AR.3           -3.5005           +0.0000j            3.5005            0.5000
    ## -----------------------------------------------------------------------------


## R

```r
#load data
gdp = read.csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv")

#estimation via ols: pay attention to the selection of the 'GDPC1' column. 
#if the column is not specified, the function call also interprets the date column as a time series variable!
ar_gdp = ar.ols(gdp$GDPC1)
ar_gdp

#lag order is automatically selected by minimizing AIC 
#disable this feature with the optional command 'aic = F'. Note: you will also likely wish to specify the argument 'order.max'.
#ar.ols() defaults to demeaning the data automatically. Also consider taking logs and first differencing for statistically meaningful results.
```

## STATA

```stata
*load data
import delimited "https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv", clear

*Generate the new date variable
*To generalize to a different set of data, replace '1947q1' with your own series' start date.
generate date_index = tq(1947q1) + _n-1

*Index the new variable format as quarter
format date_index %tq

*Convert a variable into time-series data
tsset date_index

*Specifiy and Run AR regression: this STATA method will not automatically select a lag order.
*The 'L.' operator indicates the lagged value of a variable in STATA, 'L2.' its second lag, and so on.
reg gdpc1 L.gdpc1 L2.gdpc1
*variables are not demeaned automatically by STATA. Also consider taking logs and first differencing for statistically meaningful results.
```
