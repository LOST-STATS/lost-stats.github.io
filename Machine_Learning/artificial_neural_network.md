---
title: Artificial Neural Network
parent: Machine Learning
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Artificial Neural Network

Artificial neural networks are universal function approximators that consist of nodes, each of which does a computation on an input, and layers, which are collections of nodes that have access to the same inputs. There are many variations of neural networks but the most common is the multi-layer perceptron. They can be applied to supervised learning (e.g. regression and classification), unsupervised learning, and reinforcement learning.

As an example, a simple single-layer perceptron for regression with $$M$$ neurons in the hidden layer is defined as

$$ Z_m = \sigma(\alpha_{0m} + \alpha_{m}^TX), \quad m = 1, ..., M $$

$$ f(X) = \beta_0 + \beta^TZ $$

for feature matrix $$X$$ and activation function $\sigma$. A popular choice of activation function is the rectified linear unit, $$\sigma(v) = \max(0, v)$$.

## Keep in Mind

- There are many different choices of [activation function](https://en.wikipedia.org/wiki/Activation_function).
- There are many different choices of [network architecture](https://towardsdatascience.com/the-mostly-complete-chart-of-neural-networks-explained-3fb6f2367464), appropriate for different tasks.
- Neural networks are prone to overfitting, and are sensitive to both the scale of the inputs and the choice of starting weights in the hidden layer. There are many techniques available to reduce overfitting and other issues with neural networks.

# Implementations

## Python

There are many libraries for artificial neural networks in Python, including the widely-used, production-oriented **tensorflow** (from Google) and **PyTorch** (from Facebook). **scitkit-learn** has a simple neural network regressor that's just a single line:

```python
from sklearn.neural_network import MLPRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

# Generate synthetic data
X, y = make_regression(n_samples=1000, n_features=10)

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

# Create and fit model
regr = MLPRegressor(hidden_layer_sizes=(100,),
                    activation='relu').fit(X_train, y_train)

# Compute R^2 score
regr.score(X_test, y_test)
```
