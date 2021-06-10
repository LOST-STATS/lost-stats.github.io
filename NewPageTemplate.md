---
title: Serial Correlation
parent: Time Series
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Serial Correlation/Autocorrelation  

Serial correlation, also known as autocorrelation, is the relationship between a variable and lagged versions of itself. Error terms from different time periods of a time series variable being correlated is what we call "serial correlation". Time series data that exhibits autocorrelation is easier to predict and forecast than data that does not.

## Keep in Mind

- Remember that the data must be in time series format in order to be run through the autocorrelation functions, otherwise you will yield an error. 

## Also Consider

[Creating Time Series Data]({{https://lost-stats.github.io/Time_Series/creating_time_series_dataset.html}})

# Implementations

## R
```{r}
#load necessary packages
library(pacman)
p_load(tidyverse, tseries)
```
```{r}
#load in data, pick a variable, and make sure it is in time series format

gov <- read_csv("Government Revenue and Expenditures.csv")

ts_def<- ts(gov$def, start=c(1959), end=c(2019), frequency = 1)
```

```{r}
#now run the time series data through the autocorrelation function

#"acf()" works just fine for this next step

acf_def <- acf(ts_def, plot=TRUE, main="Defense Expenditures and Investment, Autocorrelation")

#to plot the estimated values given in the plot, set "plot=FALSE"

acf_def <- acf(ts_def, plot=FALSE, main="Defense Expenditures and Investment, Autocorrelation")
```

```

# References 
(Further reading on serial correlation)[https://www3.nd.edu/~rwilliam/stats2/l26.pdf]

