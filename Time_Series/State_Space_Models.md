
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

- The parameters of a linear Gaussian state space model can be estimated using a maximum likelihood approach.
This is made possible by the fact that the innovation vectors $$u_t$$ and $$v_t$$ are assumed to be multivariate standard normal.
The Kalman filter can be used to construct the likelihood function, which can be transformed into a log-likelihood function and simply optimized with respect to the parameters. 
- If the innovations are assumed to be non-Gaussian, then we may still apply the maximum likelihood procedure to yield quasi-maximum likelihood parameter estimates that are consistent and asymptotically normal.
- Unless appropriate restrictions are placed on the parameter matrices, the parameter matrices obtained from the above-mentioned optimization procedure will not be unique. 
In other words, in the absence of restrictions, the parameters of the state space model are unidentified. 
- The Kalman filter can be used to recursively generate forecasts of the state vector within a sample period given information up to time $$t \in \{t_0,\ldots,T\}$$, where $$t_0$$ and $$T$$ represent the initial and final periods of a sample, respectively.
- The Kalman smoother can be used to generate historical estimates of the state vector throughout the entire sample period given all available information in the sample (information up to time $$T$$).

# Also Consider 

-

# Implementations

## R

Text.

```r



```