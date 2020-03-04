---
title: Auto Regressive Models
parent: Time Series
has_children: false
mathjax: true
nav_order: 1
---

# Auto Regressive Models

Auto Regressive models are fundamental to time series analysis. They are estimated via regressing a variable on one or more of its lagged values. That is, AR models take the form: $$Y_t = c + \sum_{i = 1}^{p} \beta_i Y_{t-i} + \epsilon_t $$ Where we say p is the *order* of our auto regression. Their estimation in statistical software packages is generally straightforward.

For additional information, see [Wikipedia: Autoregressive model](https://en.wikipedia.org/wiki/Autoregressive_model).

## Keep In Mind

- An AR model can be univariate (scalar) or multivariate (vector). This may be important to implementing an AR model in your statisical package of choice.  
- Data should be properly formatted before estimation. If not, non-time series objects (e.g., a date column) may be interpereted by software as a time series variable, leading to erroneous output. 

# Implementations

Following the [instructions](https://lost-stats.github.io/Time_Series/creating_time_series_dataset.html) for creating and formatting Time Series Data, we will use quaterly GDP data downloaded from [FRED](https://fred.stlouisfed.org/series/GDPC1) as an example.

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
#load data
import delimited "https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv", clear

#Generate the new date variable
#To generalize to a different set of data, replace '1947q1' with your own series' start date.
generate date_index = tq(1947q1) + _n-1

#Index the new variable format as quarter
format date_index %tq

#Convert a variable into time-series data
tsset date_index

#Specifiy and Run AR regression: this STATA method will not automatically select a lag order.
#The 'L.' operator indicates the lagged value of a variable in STATA, 'L2.' its second lag, and so on.
reg gdpc1 L.gdpc1 L2.gdpc1
#variables are not demeaned automatically by STATA. Also consider taking logs and first differencing for statistically meaningful results.
```