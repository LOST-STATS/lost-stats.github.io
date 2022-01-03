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
In other words, if all eigenvalues of $$\boldsymbol{A}$$ liw within the complex unit circle, we may express the VAR(1) model as 

$$ Y_t = \boldsymbol{\mu} + \sum_{i=0}^\infty \boldsymbol{A}^i U_{t-i} \, , $$

where $$\boldsymbol{\mu} \ident E(Y_t) = (I_{Kp} - \boldsymbol{A})^{-1} \boldsymbol{\upsilon}$$, $$\Gamma_Y(h) = \sum_{i=0}^\infty \boldsymbol{A}^{h+i} \Sigma_U (\boldsymbol{A}^i)'$$, and $$\frac{\partial Y_t}{U_{t-i}} = \boldsymbol{A}^i \rightarrow 0$$ as $i \rightarrow \infty$.
Intuitively, this means that the impulse response of $$Y_t$$ to innovations converges to zero over time.
Furthermore, a stable VAR($$p$$) process is stationary -- its first and second moments are time invariant. 

## Keep in mind 

# Implementations 

## Julia

## R
