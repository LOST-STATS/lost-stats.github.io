---
title: Autocorrelation Function
parent: Time Series
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Autocorrelation Function

Serial correlation, also known as autocorrelation, is the relationship between a variable and lagged versions of itself. Error terms from different time periods of a time series variable being correlated is what we call "serial correlation". Time series data that exhibits autocorrelation is easier to predict and forecast than data that does not.

The process for detecting the presence of serial correlation is fairly straightforward. In effect, you simply check whether a variable is correlated with lagged versions of itself. There are details in that process, but that's the main idea. The "autocorrelation" function checks the correlation between a variable and different lags of itself, typically presented as a graph. It is common to then look at the correlations (or a plot of them) and see which lag lengths have nonzero correlations. There is also the "partial autocorrelation" function, which in the context of a single varaible looks at the correlation between $$Y_t$$ and $$Y_{t-j}$$ while controlling for each of the intermediate lags $$Y_{t-1}, ..., Y_{t-j+1}$$.

## Keep in Mind

- In most languages, there is a dedicated data format for time series data that must be used with time series commands. See [Creating a Time Series Dataset]({{ "/Time_Series/creating_time_series_dataset.html" | relative_url }}). 

## Also Consider

- The number of nonzero autocorrelations you find can help inform your choice of time-series model, for example how many autoregressive terms to include in an [AR Model]({{ "/Time_Series/AR-models.html" | relative_url }}).
- For further reading on serial correlation, [see here](https://www3.nd.edu/~rwilliam/stats2/l26.pdf)

# Implementations

The data we use comes from the Federal Reserve's Economic Database, using the series on [U.S. national defense expenditures and gross investment](https://fred.stlouisfed.org/series/FDEFX). 

## Python

```python
import pandas as pd
import statsmodels.api as sm

d = pd.read_csv('https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/FDEFX.csv')

# Plot the ACF
sm.graphics.tsa.plot_acf(d['FDEFX'])

# Plot the PACF
sm.graphics.tsa.plot_pacf(d['FDEFX'])


# The PACF shows that, while defense expenditures are correlated with defense expenditures
# many periods ago (as shown in the ACF), all of that is explained by a one-period lag.
# The rest of the effect is *through* that one-period lag.
```

## R

Base-R has a well-rounded set of time series functions, including `acf()` and `pacf()`.

```r
# load in data, pick a variable, and make sure it is in time series format
gov <- read.csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/FDEFX.csv")

ts_def <- ts(gov$FDEFX, start=c(1959), end=c(2020), frequency = 1)

# now run the time series data through the autocorrelation function acf()
# which will also produce a plot
acf(ts_def, plot=TRUE, main="Defense Expenditures and Investment, Autocorrelation")
acf(ts_def, plot=FALSE, main="Defense Expenditures and Investment, Autocorrelation")

# or pacf() for a partial autocorrelation
pacf(ts_def, plot=TRUE, main="Defense Expenditures and Investment, Autocorrelation")

# The PACF shows that, while defense expenditures are correlated with defense expenditures
# many periods ago (as shown in the ACF), all of that is explained by a one-period lag.
#  The rest of the effect is *through* that one-period lag.
```

## Stata

```stata
import delimited "https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/FDEFX.csv", clear

* Set the date variable to be quarterly date data
* with qofd picking the quarter from the actual date
g quarter = qofd(date(date, "YMD"))

* tell Stata this is time series data
* Specifically, quarterly data
tsset quarter, quarterly

* Get both the autocorrelation and partial autocorrelation
* (with a text-based graph)
corrgram fdefx

* The PACF shows that, while defense expenditures are correlated with defense expenditures
* many periods ago (as shown in the ACF), all of that is explained by a one-period lag.
* The rest of the effect is *through* that one-period lag.
```
