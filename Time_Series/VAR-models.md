---
title: VAR Models
parent: Time Series
has_children: false
mathjax: true
nav_order: 1
---

# Vector Autoregression (VAR) Models

A vector autoregression (VAR) of order $$p$$, often abbreviated as VAR($$p$$), is the following data-generating process (DGP):

$$y_t = \upsilon + A_1 y_{t-1} + \ldots + A_p y_{t-p} + u_t \, ,$$

for t = 0, 1, 2, \ldots, where $$y_t = (y_{1t}, \ldots, y_{Kt})'$$ is a ($$K \times 1$$) random vector of observed data, the $$A_i$$ are fixed ($$K \times K$$) coefficient matrices, $$\upsilon = (\upsilon_1 , \ldots , \upsilon_K)'$$ is a fixed ($$K \times 1$$) vector of intercept terms, and $$u_t = (u_{1t} , \ldots , u_{Kt})'$$ is a $$K$$-dimensional innovation process with $$E(u_t) = 0$$, $$E(u_t u_t') = \Sigma_u$$, and $$E(u_t u_s') = 0$$ for $$s \neq t$$. 
Simply put, a VAR($$p$$) is a model of the DGP underlying some random data vector $$y_t$$ for all $$t$$ as a function of $$1, \ldots , p$$ of its own lags, along with identically and independently distributed (iid) innovations.

Any given VAR($$p$$) process has an equivalent VAR(1) representation:

$$Y_t = \boldsymbol{\upsilon} + \boldsymbol{A} Y_{t-1} + U_t \, ,$$

where 

$$ Y_t \ident \begin{bmatrix} y_t \\ y_{t-1} \\ \vdots \\ y_{t-p+1} \end{bmatrix} \, , $$

$$ \boldsymbol{\upsilon} \ident \begin{bmatrix} \upsilon \\ 0 \\ \vdots \\ 0 \end{bmatrix}  \, ,$$

$$ A \ident \begin{bmatrix}  A_1 & A_2 & \ldots & A_{p-1} & A_p \\ I_K & 0 & \ldots & 0 & 0 \\ 0 & I_K & & 0 & 0 \\ \vdots & & \ddots & \vdots & \vdots \\ 0 & 0 & \ldots & I_K & 0 \end{bmatrix} \, , $$

and 

$$ U_t \ident \begin{bmatrix} u_t \\ 0 \\ vdots \\ 0 \end{bmatrix} \, .$$

By the above ubiquitous formulation, any given VAR($$p$$) is stable if $$\text{det}(I_{Kp} - \boldsymbol{A}z) \neq 0 $$ for $$\abs{z} \leq 1$$. 
In other words, if all eigenvalues of $$\boldsymbol{A}$$ live within the complex unit circle, we may express the VAR(1) model as 

$$ Y_t = \boldsymbol{\mu} + \sum_{i=0}^\infty \boldsymbol{A}^i U_{t-i} \, , $$

where $$\boldsymbol{\mu} \ident E(Y_t) = (I_{Kp} - \boldsymbol{A})^{-1} \boldsymbol{\upsilon}$$, $$\Gamma_Y(h) = \sum_{i=0}^\infty \boldsymbol{A}^{h+i} \Sigma_U (\boldsymbol{A}^i)'$$, and $$\frac{\partial Y_t}{U_{t-i}} = \boldsymbol{A}^i \rightarrow 0$$ as $i \rightarrow \infty$.
Intuitively, this means that the impulse response of $$Y_t$$ to innovations converges to zero over time.
Furthermore, a stable VAR($$p$$) process is stationary -- its first and second moments are time invariant. 

VAR($$p$$) models may be estimated using a variety of statistical methods, with one of the most popular approaches being multivariate least squares estimation.
Suppose we observe a sample time series $$y_1, \ldots, y_T$$, along with $$p$$ presample values for each variable (effectively a combined sample size of $$T+p$$).
Define

$$Y \ident (y_1, \ldots, y_T) \, ,$$

$$B \ident (\upsilon, A_1, \ldots, A_p) \, ,$$

$$Z_t \ident \begin{bmatrix} 1 \\ y_t \\ \vdots \\ y_{t-p+1} \end{bmatrix} \, ,$$

$$Z \ident (Z_0 , \ldots, Z_{T-1}) \, , $$

$$U \ident (u_1, \ldots, u_T) \, ,$$

$$\boldsymbol{y} = \vec(Y) \, $$

$$\boldsymbol{\beta} = \vec(B) \, $$

$$\boldsymbol{b} = \vec(B') \, , $$

$$\boldsymbol{u} = \vec(U) \, .$$

Using the above notvation, we may express any given VAR($$p$$) model as 

$$Y = BZ + U \, ,$$

or equivalently as 

$$\vec(Y) = \vec(B Z) + \vec(U) = (Z' \kron I_K) \vec(B) + \vec(U) \, ,$$

or

$$\boldsymbol{y} = (Z' \kron I_K) \boldsymbol{\beta} + \boldsymbol{u} \, ,$$

with the covariance matrix of $$\boldsymbol{u}$$ being $$\Sigma_{\boldsymbol{u}} = I_t \kron \Sigma_u$$.

It can be shown that the least-squares (LS) estimator for the given model is 

$$\widehat{\boldsymbol{b}} = \vec(\widehat{B}') = (I_K \kron (Z Z')^{-1} Z) \vec(Y') \, ,$$

which is equivalent to separately estimating each of the $$K$$ equations in the standard formulation of a VAR($$p$$) model using OLS.

It can also be shown that if $$y_t$$ is stable with standard white noise disturbances, we can ues the $$t$$-ratios provided by common regression programs in setting up confidence intervals and tests for individual coefficients. 
These $$t$$-statistics can be obtained by dividing the elements of $$\widehat{B}$$ by square roots of the corresponding diagonal elements of $$(Z Z')^{-1} \kron \widehat{\Sigma}_u$$.

# Keep in Mind 

- VARs are often used for impulse response analysis, which is plagued with a multitude of identification limitations that you can read about in Lütkepohl's (2005) and Kilian and Lütkepohl's (2017) textbooks. VARs are reduced-form models -- it is necessary to impose structural restrictions to identify the relevant innovations and impulse responses.
 
# Implementations 

## R

Begin by loading relevant packages.
`dplyr` provides us with data manipulation capabilities, `lubridate` allows us to generate and work with date data, and `vars` contains VAR-related tools.
```r
if (!require("pacman")) install.packages("pacman")
library(pacman)
p_load(dplyr, lubridate, vars)
```

Then we create an arbitrary dataset containing two different time series.
The actual relationship between these time series is irrelevant for this demonstration -- the focus is on estimating VARs.
```r
gdp   <- read.csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/GDPC1.csv")
fdefx <- read.csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Time_Series/Data/FDEFX.csv")
data  <- inner_join(gdp, fdefx) %>% # Join the two data sources into a single data frame
          mutate(DATE = as.Date(DATE), 
                 GDPC1 = log(GDPC1), # log GDPC1
                 FDEFX = log(FDEFX)) # log FDEFX
```

We may use the `vars::VARselect` function to obtain optimal lag orders under a variety of information criteria.
Notice that we are excluding the date vector when inputting the data into `VARselect`.
```r
lagorders <- VARselect(data[,c("GDPC1","FDEFX")])$selection
lagorders
```

Now we estimate the VAR by defaulting to the Akaike Information Criterium (AIC) optimal lag order.
We include an intercept in the model by passing the `type = "const"` argument inside of `VAR`. 
```r
lagorder <- lagorders[1]
estim <- VAR(data[,c("GDPC1","FDEFX")], p = lagorder, type = "const")
```

Print the estimated VAR roots -- we must make sure that the VAR is stable (all roots lie within the unit circle).
```r
summary(estim)$roots
```

Regardless of stability issues, we are able to generate the non-cumulative impulse response function of FDEFX responding to an orthogonal shock to GDPC1. 
```r
irf <- irf(estim, impulse = "FDEFX", response = "GDPC1")
plot(irf)
```

Lastly, we may also generate forecast error variance decompositions.
```r
fevd <- fevd(estim)
plot(fevd)
```
