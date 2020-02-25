---
title: Creating Time Series Dataset
parent: Time Series
has_children: false
nav_order: 1
---

# Introduction

Time-series estimators are, by definition, a function of the temporal ordering of the observations in the estimation sample. So a number of programmed time-series econometric routines can only be used if the software is instructed ahead of time that it is working with a time-series dataset. 


## Keep in Mind

- Date data can be notoriously difficult to work with. Be sure before declaring your data set as a time series that your date variable has been imported properly.

- As an example, we will use data on U.S. **quarterly** real Gross Domestic Product (GDP). To get an Excel spreadsheet holding the GDP data, go to the Saint Louis Federal Reserve Bank [FRED](https://fred.stlouisfed.org) website.


#### Stata

- Stata’s time-series commands require the data to be sorted and indexed by time, using the tsset command, before they can be used.

- The `tsset` is simply a way for you to tell Stata which variable in your dataset represents time. [^1]

[^1]: [STATA TIME-SERIES REFERENCE MANUAL](https://www.stata.com/manuals13/ts.pdf)

- By default, Stata interprets 0 as the first date a date variable can take in 1960, 1 as the second date in 1960, and vice versa (negative integers refer to dates prior to 1960).

# Implementations

## R

There are many different kinds of time series data set objects in R. Instead of R-based time series objects such as `ts`, `zoo` and `xts`, here we will use **tsibble**, will preserves time indices as the essential data column and makes heterogeneous data structures possible.

The **tsibble** package extends the **tidyverse** to temporal data and built on top of the `tibble`, and so is a data- and model-oriented object.

For more detail information for using **tsibble** such as _key_ and _index_, check the [tsibble page](https://tsibble.tidyverts.org) and the [Introduction to tsibble](https://tsibble.tidyverts.org/articles/intro-tsibble.html). 

STEP 1) Install necessary packages using **pacman** and `pacman::p_load()`

```r
if (!require("pacman")) install.packages("pacman")
pacman::p_load(here, readxl, tssible, tidyverse)
```

STEP 2) Import data into R. 

```r
gdp <- read_excel("https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Estimation/Time_Series/Data/GDPC1.xls",
                  range = cell_rows(11:301), col_names = TRUE)
```

The option `range = cell_rows(11:301), col_names = TRUE` is to select only necessary observations. 

STEP 3) Convert a date variable formats to quarter

```r
gdp_ts <- as_tsibble(gdp,
                     index = observation_date,
                     regular = FALSE) %>% 
  index_by(date = ~ yearquarter(.))
```

By applying `yearmonth()` to the index variable (referred to as `.`), it creates new variable named `'date'` with a quarter interval which corresponds to the year-quarter for the original variable `'observation_date'`.
  
Since the `tsibble` handles regularly-spaced temporal data whereas our data (`GDPC1`) has an irregular time interval, we set the option `regular = FALSE`.

Now, we have a quarterly time-series dataset with the new variable `date`.

References for more information: 

1. If you want to learn how to build various types of time-series forecasting models, [**Forecasting: Principles and Practice**](https://otexts.com/fpp3/index.html) provides very useful information to deal with time-series data in R.
2. If you need more detail information on **tssible**, visit the [tsibble page](https://tsibble.tidyverts.org/) or [tsibble on RDRR.io](https://rdrr.io/cran/tsibble/man/tsibble.html).
3. The **fable** packages provides a collection of commonly used univariate and multivariate time-series forecasting models. For more information, visit [fable](https://fable.tidyverts.org/).


## Stata

STEP 1) Import Data to Stata

```stata
import excel "https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Estimation/Time_Series/Data/GDPC1.xls", sheet("FRED Graph") cellrange(A11:B301) clear firstrow
```
The option `sheet("FRED GRAPH") cellrange(A11:B301)` is to select only necessary observations.

STEP 2) Generate the new date variable

```stata
generate date_index = tq(1947q1) + _n-1
```

The function `tq()` converts a date variable for each of the above formats to an integer value (starting point of our data is `1947q1`). 

`_n` is a Stata command gives the index number of the current row.

STEP 3) Index the new variable format as quarter

```stata
format date_index %tq
```

This command will format `date_index` as a vector of quarterly dates which corresponds to our original date variable `observation date`.

STEP 4) Convert a variable into time-series data

```stata
tsset date_index
```

Now, we have a quarterly Stata time-series dataset. Any data you add to this file in the future will be interpreted as time-series data.
