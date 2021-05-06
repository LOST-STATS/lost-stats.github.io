---
title: State Space Models
parent: Time Series
has_children: false
mathjax: true
nav_order: 1
---

# Linear Gaussian State Space Models

The state space model can be used to represent a variety of dynamic processes, including standard ARMA processes.
It has two main components: (1) a hidden/latent $$x_t$$ process referred to as the state process, and (2) an observed process $$y_t$$ that is independent conditional on $$x_t$$.
Let us consider the most basic state space model -- the linear Gaussian model -- in which $$x_t$$ follows a linear autoregressive process and $$y_t$$ is a linear mapping of $x_t$ with added noise.
The linear Gaussian state space model is characterized by the following state equation:

$$ x_{t+1} + F \, x_{t} + u_{t+1} \, ,$$

where $$x_t$$ and $$u_t$$ are both $$p \times 1$$ vectors, such that $$u_t \sim i.i.d. N(0,Q)$$.
It is assumed that the initial state vector $$x_0$$ is drawn from a normal distribution.
The observation equation is expressed as

$$y_t = A_t \, x_t + v_t \, ,$$

where $$y_t$$ is a $q \times 1$ observed vector, $$A_t$$ is a $$q \times p$$ observation matrix, and $$v_t \sim i.i.d. N(0,R)$$ is a $$q \times 1$$ noise vector.

For additional information about the state-space repsentation, refer to [Wikipedia: State-Space Representation](https://en.wikipedia.org/wiki/State-space_representation#:~:text=In%20control%20engineering%2C%20a%20state,differential%20equations%20or%20difference%20equations.&text=The%20%22state%20space%22%20is%20the,axes%20are%20the%20state%20variables.).

# Keep in Mind

- Expressing a dynamic process in state-space form allows us to apply the Kalman filter and smoother.
- The parameters of a linear Gaussian state space model can be estimated using a maximum likelihood approach.
This is made possible by the fact that the innovation vectors $$u_t$$ and $$v_t$$ are assumed to be multivariate standard normal.
The Kalman filter can be used to construct the likelihood function, which can be transformed into a log-likelihood function and simply optimized with respect to the parameters.
- If the innovations are assumed to be non-Gaussian, then we may still apply the maximum likelihood procedure to yield quasi-maximum likelihood parameter estimates that are consistent and asymptotically normal.
- Unless appropriate restrictions are placed on the parameter matrices, the parameter matrices obtained from the above-mentioned optimization procedure will not be unique.
In other words, in the absence of restrictions, the parameters of the state space model are unidentified.
- The Kalman filter can be used to recursively generate forecasts of the state vector within a sample period given information up to time $$t \in \{t_0,\ldots,T\}$$, where $$t_0$$ and $$T$$ represent the initial and final periods of a sample, respectively.
- The Kalman smoother can be used to generate historical estimates of the state vector throughout the entire sample period given all available information in the sample (information up to time $$T$$).

# Also Consider

- Recall that a stationary ARMA process can be expressed as a state space model.
This may not be necessary, however, unless the given data has missing observations.
If there are no missing data, then one can defer to the standard method of estimating ARMA models described on the [ARMA page]({{ "/Time_Series/ARMA-models.html" | relative_url }}).

# Implementations

First, follow the [instructions]({{ "/Time_Series/creating_time_series_dataset.html" | relative_url }}) for creating and formatting time-series data using your software of choice.
We will again use quarterly US GDP data downloaded from [FRED](https://fred.stlouisfed.org/series/GDPC1) as an example.
We estimate the quarterly log change in GDP using an ARMA(3,1) model in state space form to follow the [ARMA implementation]({{ "/Time_Series/ARMA-models.html" | relative_url }}).

An ARMA($$p,q$$) process

$$ y_t = c + \sum_{i = 1}^{3} \phi_i Y_{t-i} + \sum_{j = 1}^{1} \theta_j \varepsilon_{t-j} + \varepsilon_t $$

may be expressed in state-space form in a variety of ways -- the following is an example of a common parsimonious approach.
The state equation (also referred to as the transition equation) may be expressed as

$$
\begin{bmatrix} y_t \\ y_{t-1} \\ y_{t-2} \\ \varepsilon_t \end{bmatrix}
=
\begin{bmatrix} c \\ 0 \\ 0 \\ 0 \end{bmatrix}
+
\begin{bmatrix} \phi_1 & \phi_2 & \phi_3 & \theta \\ 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{bmatrix}
\, \begin{bmatrix} y_{t-1} \\ y_{t-2} \\ y_{t-3} \\ \varepsilon_{t-1} \end{bmatrix}
+
\begin{bmatrix} \varepsilon_t \\ 0 \\ 0 \\ \varepsilon_t \end{bmatrix} \, ,
$$

while the observation equation (also referred to as the measurement equation) may be expressed as
$$
y_t = \begin{bmatrix} 1&0&0&0 \end{bmatrix} \, \begin{bmatrix} y_t \\ y_{t-1} \\ y_{t-2} \\ \varepsilon_t \end{bmatrix} \, .
$$

The observation matrix $$A_t$$ in our implementation will be time-invariant ($$A_t = A, \forall t$$).

## R

The following R implementation relies on the ``dlm`` package to build an ARMA(3,1) model and express it in state-space form.
The ``dlm`` package is used to work with dynamic linear models (DLMs), which is an alternative name to linear state space models.
To learn more about the package, check out its [CRAN page](https://cran.r-project.org/web/packages/dlm/index.html), as well as [this vignette](https://cran.r-project.org/web/packages/dlm/vignettes/dlm.pdf) written by the author of the package.
First the ``tsibble`` and ``dlm`` packages are installed and loaded.
Then US quarterly GDP data is loaded and log-differentiated in the same exact way as shown on the [ARMA page]({{ "/Time_Series/ARMA-models.html" | relative_url }}).
Then an ARMA(3,1) model is built and implicitly put in state-space form using the ``dlm`` package, after which it is fit to the loaded series using a maximum likelihood approach.
The parameters of the estimated model are stored in ``mod``, and the estimated observation and state error matrices are also stored in ``obs.error.var`` and ``state.error.var``, respectively.
Lastly, both the Kalman filter and smoother are applied to the model, the results of which are stored in the ``filtered`` and ``smoothed`` objects, respectively.

```r

## Install and load time series packages
if (!require("tsibble")) install.packages("tsibble")
library(tsibble)
if (!require("dlm")) install.packages("dlm")
library(dlm)

# Prepare the data

## Load data
gdp <- read.csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv")

## Set our data up as a time-series
gdp$DATE <- as.Date(gdp$DATE)

gdp_ts <- as_tsibble(gdp,
  index = DATE,
  regular = FALSE
) %>%
  index_by(qtr = ~ yearquarter(.))

## Construct our first difference of log gdp variable
gdp_ts$lgdp <- log(gdp_ts$GDPC1)

gdp_ts$ldiffgdp <- difference(gdp_ts$lgdp, lag = 1, difference = 1)

# Estimate ARMA(3,1) using the above data

## Define log-diff gdp as vector y
y <- gdp_ts$ldiffgdp

## Build ARMA(3,1) model
fn <- function(parm) {
  dlmModARMA(
    ar = c(parm[1], parm[2], parm[3]),
    ma = parm[4],
    sigma2 = parm[5]
  )
}

## Fit the model to the data
fit <- dlmMLE(y, c(rep(0, 4), 1), build = fn, hessian = TRUE)
(conv <- fit$convergence)

## Store var-cov stats
mod <- fn(fit$par)
obs.error.var <- V(mod)
state.error.var <- W(mod)

# Apply the Kalman filter
filtered <- dlmFilter(y, mod = mod)

# Apply the Kalman smoother
smoothed <- dlmSmooth(filtered)
```

