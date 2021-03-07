
---
title: "State Space Models"
parent: Time Series
has_children: false
nav_order: 1
mathjax: true
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
This may not be necessary, however, unless the data in use has missing observations.
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

## R

Text.

```r



```