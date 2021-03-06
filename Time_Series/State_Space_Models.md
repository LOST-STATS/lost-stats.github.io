
---
title: "State Space Models""
parent: Time Series
has_children: false
nav_order: 1
mathjax: yes
---

# Linear Gaussian State Space Models

The state space model can be used to represent a variety of dynamic processes, including standard ARIMA processes. 
It has two main components: (1) a hidden/latent $$x_t$$ process referred to as the state process, and (2) an observed process $$y_t$$ that is independent conditional on $$x_t$$.
Let us consider the most basic state space model -- the linear Gaussian model.
The linear Gaussian state space model is characterized by the following state equation:
$$$ x_{t} + A \, x_{t-1} + u_t \, ,$$$
where $$x_t$$ and $$u_t$$ are both $$p \times 1$$ vectors, such that $$u_t \sim i.i.d. N(0,Q)$$. 
It is assumed that the initial state vector $$x_0$$ is drawn from a normal distribution. 

## Keep in Mind

- Text.

## Also Consider

- Text.
- Text.

# Implementations

## R

Text.