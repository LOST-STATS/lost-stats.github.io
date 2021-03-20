ARIMA Models
================

## Introduction

ARIMA, which stands for **A**uto**r**egressive **I**ntegrated
**M**oving-**A**verage, is a time series model specification which
combines typical Autoregressive
([AR](https://en.wikipedia.org/wiki/Autoregressive_model)) and Moving
Average ([MA](https://en.wikipedia.org/wiki/Moving-average_model)),
while also allowing for multiple unit roots. An ARIMA thus has three
parameters: \(p\), which denotes the AR parameters, \(d\), which is the
number of unit roots, and \(q\), which denotes the MA parameters. A
univariate \(ARIMA(p, 1, q)\) model is specified by
\[y_{t}=\alpha + \delta t +u_{t}\] where \(u_{t}\) is an
\(ARMA(p+1,q)\). Particularly, \[\rho(L)u_{t}=\theta(L)\varepsilon_{t}\]
where \(\varepsilon_{t}\sim WN(0,\sigma^{2})\) and 
(L)&=(1-*{1}L--*{p+1}L<sup>{p+1})\\ (L)&=1+*{1}L++*{q}L</sup>{q}
\\end{align\*} Recall that \(L\) is the lag operator and \(\theta(L)\)
must be invertible.

## Keep in Mind

  - The first difference of an \(ARIMA(p,1,q)\) is an \(ARMA(p,q)\) as
    is the \(d^{th}\)-difference of an \(ARIMA(p,d,q)\).
  - If your model has no unit roots, it may be best to consider an ARMA,
    AR, or MA model
  - You can always test the presence of a unit root afer fitting your
    model using a [unit root
    test](https://en.wikipedia.org/wiki/Unit_root_test), such as the
    [Augmented Dickey-Fuller
    test](https://en.wikipedia.org/wiki/Augmented_Dickey%E2%80%93Fuller_test)

## Also Consider

  - AR Models (\[LOST: AR models\]({{ “/Time\_Series/AR-models.html” |
    relative\_url }}))

  - MA Models (\[LOST: MA models\]({{ “/Time\_Series/MA-Model.html” |
    relative\_url }}))

  - ARMA Models (\[LOST: AR models\]({{ “/Time\_Series/ARMA-models.html”
    | relative\_url }}))

  - Seasonal ARIMA models, if you suspect the time series data you are
    trying to fit with is subject to seasonality

  - If you are working with State-Space models (\[LOST: AR models\]({{
    “/Time\_Series/State\_Space\_Models.html” | relative\_url }})),
    you may be interested in trend-cycle decomposition with ARIMA. This
    involves breaking down the ARIMA into a “trend” component, which
    encapsulates permanent effects (stochastic and deterministic), and a
    “cyclical” effect, which encapsulates transitory, non-permanent
    variation in the model. One extension of this is the Unobserved
    Components ARIMA, or UC-ARIMA

# Implementations

## R

The `stats` package, whic comes standard-loaded on an RStudio workspace,
includes the function `arima`, which allows one

``` r
#load packages
if (!require("pacman")) install.packages("pacman")
```

    ## Loading required package: pacman

``` r
pacman::p_load(tstools)
```

``` r
#load/generate data
gdp = read.csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv")
GDPC1 = ts(gdp[ ,2], frequency = 4, start = c(1947, 01), end = c(2019, 04))
y_level = log(GDPC1)*100
```

``` r
#estimate an ARIMA model
```

For simulating ARIMA models, including seasonal ARIMA models, one should
consider the `simulate.Arima()` function from the `forecast`. This
package also includes the
