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

  - LIST OF OTHER TECHNIQUES THAT WILL COMMONLY BE USED ALONGSIDE THIS
    PAGE’S TECHNIQUE
  - Consider using standard plotting packages if your plots are just
    downloaded data (e.g., if you have downloaded GDP data over time, a
    basic plotter can be used)
      - With that being said, these techniques will work for these types
        of plots as well
  - You can try to convert your objects back into an object type that is
    more suitable for other plotting

# Implementations

## R

Turning objects into time series objects is best done via the `ts()`
function from the `stats` package, which is loaded by default in an R
Studio terminal. Graphing `ts` objects can be done efficiently using
`tsplot` from the package `tstools`.

``` r
if (!require("pacman")) install.packages("pacman")
```

    ## Loading required package: pacman

``` r
pacman::p_load(tstools)
```

For a complete description of `tsplot`, see `vignette("tstools")`. We
will start with a short example.
