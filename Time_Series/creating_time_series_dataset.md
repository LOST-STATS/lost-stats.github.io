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

# Implementations

## Python

**pandas** supports time series data. Here is an example which downloads quarterly data, casts the date column (read in as an `object` series) as a `datetime` series, and creates a year-quarter column.

```python
import pandas as pd

# Read in data
gdp = pd.read_csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv")

# Convert date column to be of data type datetime64
gdp['DATE'] = pd.to_datetime(gdp['DATE'])

# Create a column with quarter-year combinations
gdp['yr-qtr'] = gdp['DATE'].apply(lambda x: str(x.year) + '-' + str(x.quarter))
```

## R

There are many different kinds of time series data set objects in R. Instead of R-based time series objects such as `ts`, `zoo` and `xts`, here we will use **tsibble**, will preserves time indices as the essential data column and makes heterogeneous data structures possible.

The **tsibble** package extends the **tidyverse** to temporal data and built on top of the `tibble`, and so is a data- and model-oriented object.

For more detail information for using **tsibble** such as _key_ and _index_, check the [tsibble page](https://tsibble.tidyverts.org) and the [Introduction to tsibble](https://tsibble.tidyverts.org/articles/intro-tsibble.html). 

STEP 1) Load necessary packages

```r
# If necessary
# install.packages(c('here','tsibble','tidyverse'))
library(here)
library(tsibble)
library(tidyverse)
```

STEP 2) Import data into R. 

```r
gdp <- read.csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv")

# read.csv() has read in our date variable as a factor. We need a date!
gdp$DATE <- as.Date(gdp$DATE)
# If it were a little less well-behaved than this, we could use the lubridate package to fix it.
```

STEP 3) Convert a date variable formats to quarter

```r
gdp_ts <- as_tsibble(gdp,
                     index = DATE,
                     regular = FALSE) %>% 
    index_by(qtr = ~ yearquarter(.))
```

By applying `yearmonth()` to the index variable (referred to as `.`), it creates new variable named `qtr` with a quarter interval which corresponds to the year-quarter for the original variable `DATE`.
  
Since the `tsibble` handles regularly-spaced temporal data whereas our data (`GDPC1`) has an irregular time interval (since it's not the exact same number of days between quarters every time), we set the option `regular = FALSE`.

Now, we have a quarterly time-series dataset with the new variable `date`.

References for more information: 

1. If you want to learn how to build various types of time-series forecasting models, [**Forecasting: Principles and Practice**](https://otexts.com/fpp3/index.html) provides very useful information to deal with time-series data in R.
2. If you need more detail information on **tssible**, visit the [tsibble page](https://tsibble.tidyverts.org/) or [tsibble on RDRR.io](https://rdrr.io/cran/tsibble/man/tsibble.html).
3. The **fable** packages provides a collection of commonly used univariate and multivariate time-series forecasting models. For more information, visit [fable](https://fable.tidyverts.org/).


## Stata

STEP 1) Import Data to Stata

```stata
import delimited "https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv", clear
```

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
