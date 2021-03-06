
---
title: "State Space Models"
parent: Time Series
has_children: false
nav_order: 1
mathjax: true
---

# Linear Gaussian State Space Models

The state space model can be used to represent a variety of dynamic processes, including standard ARIMA processes. 
It has two main components: (1) a hidden/latent $$x_t$$ process referred to as the state process, and (2) an observed process $$y_t$$ that is independent conditional on $$x_t$$.
Let us consider the most basic state space model -- the linear Gaussian model -- in which $$x_t$$ follows a linear autoregressive process and $$y_t$$ is a linear mapping of $x_t$ with added noise.
The linear Gaussian state space model is characterized by the following state equation:

$$ x_{t} + F \, x_{t-1} + u_t \, ,$$

where $$x_t$$ and $$u_t$$ are both $$p \times 1$$ vectors, such that $$u_t \sim i.i.d. N(0,Q)$$. 
It is assumed that the initial state vector $$x_0$$ is drawn from a normal distribution. 
The observation equation is expressed as 

$$y_t = A_t \, x_t + v_t \, ,$$ 

where $$y_t$$ is a $q \times 1$ observed vector, $$A_t$$ is a $$q \times p$$ observation matrix, and $$v_t \sim i.i.d. N(0,R)$$ is a $$q \times 1$$ noise vector.

## Keep in Mind

- Text.

## Also Consider

- Text.
- Text.

# Implementations

## R

Text.