---
title: Creating Time Series Dataset
parent: Time Sereis
has_children: false
nav_order: 1
---

# Introduction

- Time-series estimators are, by definition, a function of the temporal ordering of the observations in the estimation sample. So a number of programmed time-series econometric routines can only be used if Stata or R knows it is working with a time-series dataset. 


## Keep in Mind

- As an example, we will use data on U.S. **quarterly** real Gross Domestic Product (GDP). To get an Excel spreadsheet holding the GDP data, go to the Saint Louis Federal Reserve Bank [FRED](https://fred.stlouisfed.org) website.

- Within code chunk, any description after ## (R) and ** (Stata) is to explain the command line above in detail.


#### Stata

- Stata’s time-series commands require the data to be sorted and indexed by time, using the tsset command, before they can be used.

- The `tsset` is simply a way for you to tell Stata which variable in your dataset represents time. [^1]

[^1]: [STATA TIME-SERIES REFERENCE MANUAL](https://www.stata.com/manuals13/ts.pdf)

- By default, Stata interprets 0 as the first date a date variable can take in 1960, 1 as the second date in 1960, and vice versa (negative integers refer to dates prior to 1960).


#### R [^2] 

[^2]: [tsibble](https://tsibble.tidyverts.org) and [Introduction to tsibble](https://tsibble.tidyverts.org/articles/intro-tsibble.html)

- Instead of R-based time series objects such as `ts`, `zoo` and `xts`, here the **`tsibble`** will be introduced which preserves time indices as the essential data column and makes heterogeneous data structures possible.

- The tssible package extends the tidyverse to temporal data and built on top of the tibble, it is a data- and model-oriendted object. 

- For more detail information for using tsibble such as _key_ and _index_, check [tsibble](https://tsibble.tidyverts.org). 


# Implementations

## R

```r

# 1) Install necessary packages using pacman and pacman::p_load()

if (!require("pacman")) install.packages("pacman")
pacman::p_load(here, readxl, tssible, tidyverse)


# 2) Import data to R. 

gdp <- read_excel("YOUR_WORKING_DIRECTORY_PATH/GDPC1.xls",
                  range = cell_rows(11:301), col_names = TRUE)

## cf) The option "range = cell_rows(11:301), col_names = TRUE" is to select only necessary observations. 
          

# 3) Convert a date variable formats to quarter

gdp_ts <- as_tsibble(gdp,
                     index = observation_date,
                     regular = FALSE) %>% 
  index_by(date = ~ yearquarter(.))

## By applying "yearmonth()" to the index variable (referred to as .), it creates new variable named 'date' with quarter interval which corresponds to the year-quarter for the original variable 'observation_date'.
  
## cf) Since the "tsibble"" handles regularly-spaced temporal data whereas our data (GDPC1) has irregular time interval, we set option "regular = FALSE".
```

- Now, we have a quarterly time-series dataset with the new variable *date*.



## Stata

```stata

* 1) Import Data to Stata

import excel "YOUR_WORKING_DIRECTORY_PATH\GDPC1.xls", sheet("FRED Graph") cellrange(A12:B301)

** The option "sheet("FRED GRAPH") cellrange(A12:B301)" is to select only necessary observations.


* 2) Generate the new date variable

generate date_index = tq(1947q1) + _n-1

** The functions "tq()" converts a date variable for each of the above formats to an integer value (starting point of our data is 1947q1). 

** "_n" is a Stata command giving an index of the observations running from one to the number of data points.


* 3) Indexing the new variable format as quarter

format date_index %tq

** The command will format 'date_index' as a vector of quarterly dates which corresponds to our original date variable ("observation date").


* 4) Conversing a variable into time-series data

tsset date_index

** Finally, you need to tell Stata that the data is time-series data with the variable 'date_index' indicating the date of each observation.

```

- Now, we have a quarterly Stata time-series dataset. Any data you add to this file in the future will be interpreted as time-series data.



## Also Consider

- If you want to learn how to build various types of time-series forecasting model, [**Forecasting: Principles and Practice**](https://otexts.com/fpp3/index.html) provides very useful information to deal with time-series data in R.

- If you need more detail information on tssible, visit [tssible1](https://tsibble.tidyverts.org/) or [tissble2](https://rdrr.io/cran/tsibble/man/tsibble.html).

- The fable packages provides a collection of commonly used univariate and nultivariate time-series forecasting models. For more information, visit [fable](https://fable.tidyverts.org/).
