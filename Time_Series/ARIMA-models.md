ARIMA Models
================

## Introduction

ARIMA, which stands for **A**uto**r**egressive **I**ntegrated
**M**oving-**A**verage, is a time series model specification which
combines typical Autoregressive
([AR](https://en.wikipedia.org/wiki/Autoregressive_model)) and Moving
Average ([MA](https://en.wikipedia.org/wiki/Moving-average_model)),
while also allowing for unit roots. An ARIMA thus has three parameters:
\(p\), which denotes the AR parameters, \(q\), which denotes the MA
parameters, and \(d\), which represents the number of times an ARIMA
model must be differenced in order to get an ARMA model. A univariate
\(ARIMA(p, 1, q)\) model can be specified by
\[y_{t}=\alpha + \delta t +u_{t}\] where \(u_{t}\) is an
\(ARMA(p+1,q)\). Particularly, \[\rho(L)u_{t}=\theta(L)\varepsilon_{t}\]
where \(\varepsilon_{t}\sim WN(0,\sigma^{2})\) and 
(L)&=(1-*{1}L--*{p+1}L<sup>{p+1})\\ (L)&=1+*{1}L++*{q}L</sup>{q}
\\end{align\*} Recall that \(L\) is the lag operator and \(\theta(L)\)
must be invertible. If we factor
\(\rho(L)=(1-\lambda_{1}L)\cdots(1-\lambda_{p+1}L)\), where
\(\{\lambda\}\) are the eigenvalues of the \(F\) matrix (see \[LOST:
State-Space Models\]({{ “/Time\_Series/State\_Space\_Models.html” |
relative\_url }})), then define
\(\phi(L)=(1-\lambda_{1}L)\cdots(1-\lambda_{p}L)\). It follows that 
Since \(\Delta u_{t}\) is now a stationary \(ARMA(p,q)\), it has a Wold
form \(\Delta u_{t}=\phi^{-1}(L)\theta(L)\varepsilon_{t}\), and so we
can write  In the general case of an \(ARIMA(p,d,q)\), a unit root of
multiplicity \(d\) leads to
\[\phi(L)(1-L)^{d}u_{t}=\theta(L)\varepsilon_{t}\] which leads to
\(\Delta^{d} u_{t}\) being an \(ARMA(p,q)\) process.

## Keep in Mind

  - Error terms are generally assumed to be either \(WN(0,\sigma^{2})\)
    or i.i.d. \(N(0,\sigma^{2})\)
  - A non-zero intercept or mean in \(\Delta y_{t}\) is reffered to as
    *drift*, and can be speciied in functions below
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

  - ARMA Models (\[LOST: ARMA models\]({{
    “/Time\_Series/ARMA-models.html” | relative\_url }}))

  - Seasonal ARIMA models, if you suspect the time series data you are
    trying to fit with is subject to seasonality

  - If you are working with \[State-Space models\]({{
    “/Time\_Series/State\_Space\_Models.html” | relative\_url }}), you
    may be interested in trend-cycle decomposition with ARIMA. This
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
#load/generate data
gdp = read.csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv")
GDPC1 = ts(gdp[ ,2], frequency = 4, start = c(1947, 01), end = c(2019, 04))
y_level = log(GDPC1)*100
```

``` r
#estimate an ARIMA model
gdp_arima <- arima(y_level, c(1,1,1))
```

For simulating ARIMA models, including seasonal ARIMA models, one should
consider the `simulate.Arima()` function from the `forecast`. This
package also includes the ability to *auto-select* ARIMA models. This is
of particular use when one would like to automate the selection of
\(p,q\), and \(d\), without writing their own function. According to
[David
Childers](https://donskerclass.github.io/Forecasting/ARIMA.html#:~:text=Condition%20for%20stationarity%20or%20an%20ARMA%20model%20is,roots%2C%20differencing%20%5C%28y_t%5C%29%20d%20times%20can%20restore%20stationarity),
`forecast::auto.arima()` takes the following steps: - Use the
[KPSS](https://en.wikipedia.org/wiki/KPSS_test) to test for unit roots,
differencing the series unit stationary - Create likelihood functions at
various orders of \(p,q\) - Use AIC to choose \(p,q\), then estimate via
Maxmium Likelihood to select \(p,q\) If one knows the value of \(d\), it
can be passed to the function. Maximum and starting values for \(p,q,\)
and \(d\) can be specified in the seasonal- and non-seasonal cases.

``` r
pacman::p_load(forecast)
```
