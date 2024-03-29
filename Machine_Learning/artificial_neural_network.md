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

## Julia

Julia community puts a lot of effort into development of Neural Networks ecosystem.
These efforts are largely fueled and greatly helped by two major features of Julia.
First, pure Julia code (with a little help from the developer) gets translated into
efficient and optimized machine code in many cases rivaling C/C++. This largely
alleviates "two languages problem". Second, Julia features advanced metaprogramming
facilities making possible sophisticated source code transformations, Automatic Differentiation
in particular.

The main production-quality Machine Learning framework is [Flux](https://fluxml.ai/)
and [Lux](https://lux.csail.mit.edu/dev/) presents an alternative better suited for
and motivated by Scientific Machine Learning tasks. In the following example we'll
stick with the former.

```julia
using Flux, MLUtils

n_samples = 1000
n_features = 10
hidden_layer_size = 100

# our underlying equation will be
# y = x1 + 10*x2 - 7*x3 + 2*x4 + 3*x5 - 14*x6 + x7 + 3*x8 - x9 + 11*x10 - 40
# the coefficients are arbitrary, they don't represent anything
# we'll collect them in a single (column) vector
coeffs = [1, 10, -7, 2, 3, -14, 1, 3, -1, 11]
b = -40

# a n_samples*n_features matrix of "observations"
X = randn(Float32, n_samples, n_features)
# calculating "responses" corresponding to "observations" X
# according to the above equation (using matrix-vector product)
# adding a little random noise
y = X*coeffs .+ b .+ 0.02f0 .* randn(Float32, n_samples)

# We leave out 15 % of the data for testing
train_data, test_data = splitobs((X', y); at=0.85)

# our model consists of two fully connected layers, first one using `relu` activation
model = Chain(Dense(n_features => hidden_layer_size, relu), Dense(hidden_layer_size => 1))

# we're collecting all of the model's parameters (weights and biases of all the layers)
parameters = Flux.params(model)

# using Mean Sqared Error as a measure of the loss
# we can use our Neural Network as if it was just a function, applying it
# to a single observation or the whole set of observations at once
loss(x, y) = Flux.Losses.mse(model(x), y)

# currently our model is an extremely poor fit to both train and test data
loss(train_data[1], train_data[2]')
# 2123.2031f0
loss(test_data[1], test_data[2]')
# 1939.8761f0

# we'll use ADAM optimization strategy with default parameters
opt = Adam()

# now let's train our model wrt. our data!
Flux.train!(loss, parameters, eachobs(train_data), opt)

# the fitness of the model improved a lot on both train and test data!
loss(train_data[1], train_data[2]')
# 96.052666f0
loss(test_data[1], test_data[2]')
# 100.78666f0
```

Another prominent feature of the Julia ecosystem, especially with relation to
Neural Networks, is highly-developed support for NVidia GPUs (AMD and Intel GPUs
support is under development as well). **CUDA.jl** library provides Julia bindings
and high-level functions as well as underlying CUDA and CuNN C++ libraries,
thus simple `import Pkg; Pkg.add("CUDA")` makes you ready to offload your computations
to a graphics card.

For the most part **Flux** is oblivious to the location of data &mdash; RAM or GPU
&mdash; therefore after copying all our data to a GPU we can feed it to exactly
the same functions for training, loss and so on. For copying we'll employ `Flux.gpu`
function which does nothing if there's no CUDA installed. This way our code can be
GPU-oblivious too: it will use GPU if one is present, otherwise it will work
just as fine on a CPU (albeit slower).

```julia
import CUDA
# we don't actually need to directly call functions from the CUDA library
# but we want to be sure it got loaded.
# also we can call `CUDA.functional()` to check if a GPU is present and accessible.

# copying the data to a GPU with the `Flux.gpu` function
gpu_train_data = (gpu(collect(train_data[1])), gpu(collect(train_data[2])))
gpu_test_data = (gpu(collect(test_data[1])), gpu(collect(test_data[2])))

# building a new untrained model and moving it to a GPU
gpu_model = gpu(Chain(Dense(n_features => hidden_layer_size, relu), Dense(hidden_layer_size => 1)))
gpu_ps = Flux.params(gpu_model)

# the same loss function but now using `gpu_model`
gpu_loss(x, y) = Flux.Losses.mse(gpu_model(x), y)

# the loss of an untrained model is again very high
# but now all the calculations happen on a GPU
gpu_loss(gpu_train_data[1], gpu_train_data[2]')
# 2134.6206f0
gpu_loss(gpu_test_data[1], gpu_test_data[2]')
# 2145.352f0

# here we use `Flux.DataLoader` to feed our training data into the `Flux.train!` function
# 50 (batchsize) instances at a time. Using batches is preferable on a GPU to improve
# the throughput and a GPU can handle many more than 50 at once in our case.
gpu_train_loader = Flux.DataLoader((gpu_train_data[1], gpu_train_data[2]'), batchsize = 50)

# on the flip side considering a batch at a time reduces gradient information available
# for training compared to instance-by-instance approach thus hampering learning rate
# we compensate by running the same training loop over the same data several times (epochs)
# there's no reason for the number of epochs to be the same as a batch size, I just like
# the number 50 :)
for i=1:50
  Flux.train!(gpu_loss, gpu_ps, gpu_train_loader, opt)
end

# now the loss is significantly better :)
gpu_loss(gpu_train_data[1], gpu_train_data[2]')
# 38.33216f0
gpu_loss(gpu_test_data[1], gpu_test_data[2]')
# 31.173874f0
```


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
