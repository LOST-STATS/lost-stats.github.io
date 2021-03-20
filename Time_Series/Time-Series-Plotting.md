Time Series Plotting
================

## Introduction

Plotting is important to almost any statistical practice, but arguably
most important in time series analysis. In some circumstances, a basic
plot may be all that is needed. Other times, many bells and whistles are
desired, and standard plotting packages may be to general for time
series data. The purpose of this page is to highlight time series
plotting techniques that are specialized and require more overhead than
a standard plotting package.

## Keep in Mind

  - Some time series packages may be formatted specially, so you may run
    into issues using your normal plotting package
  - If the graph output is very simple, it probably best to restrict
    yourself to working with normal graphing packages
  - To use the following techniques, you have to have time series data
  - These techniques are best utilized following a time series analysis
    with time series data
      - E.g., you did a Bevridge-Nelson Decomposition (see [Stack
        Exchange: Explaining the beveridge nelson
        decomposition](https://stats.stackexchange.com/questions/80548/explaining-the-beveridge-nelson-decomposition))
        after estimating an ARIMA model (see \[LOST: ARIMA models\]({{
        “/Time\_Series/ARIMA-models.html” | relative\_url }}))
  - Many time series packages format data differently. Using plotting
    methods from one time series package on another may cause problems

## Also Consider

  - If your plots need not be turned into time series objects (e.g., if
    you have downloaded GDP data over time), a basic plotter can be used
      - With that being said, these techniques will work for these types
        of plots as well
      - Some plotting packages may be perfectly fine handling time
        series objects
  - You can try to convert your objects back into an object type that is
    more suitable for other plotting

# Implementations

## R

Turning objects into time series objects is best done via the `ts()`
function from the `stats` package, which is loaded by default in an R
Studio terminal. Graphing `ts` objects can be done efficiently using
`tsplot` from the package `tstools`. If one does not need to turn their
data into a time series object, `base::plot()` or `ggplot2::ggplot()`
are good alternatives.

``` r
if (!require("pacman")) install.packages("pacman")
```

    ## Loading required package: pacman

``` r
pacman::p_load(tstools)
```

For a complete description of `tsplot`, see `vignette("tstools")`. To
keep things simple and focus on the details of this package, I will use

``` r
gdp = read.csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv")

GDPC1 = ts(gdp[ ,2], frequency = 4, start = c(1947, 01), end = c(2019, 04))
y_level = log(GDPC1)*100
dy = diff(y_level)
T = length(dy)
```
