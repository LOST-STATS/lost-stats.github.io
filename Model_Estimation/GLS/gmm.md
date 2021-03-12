---
title: Generalized Method of Moments
parent: Generalized Least Squares
grand_parent: Model Estimation
has_children: false
nav_order: 1
mathjax: true 
---

# Generalized Method of Moments  

GMM is an estimation technique that does not require strong assumptions about the distributions of the underlying parameters. The key intuition is that if we know the expected value of population moments (such as mean or variance), then the sample equivalents will converge to that expected value using the law of large numbers. If the moments are functions of the parameters that we wish to estimate, then we can use these moment restrictions to estimate our parameters.

Suppose we have a vector of $K$ parameters we want to estimate, where the true values of those parameters are $\theta_0$ and a set of $L \geq K$ moment conditions provided by theory, $E\left[g(Y_i,\theta_0)\right] = 0$, where $Y_i$ is a vector of variables corresponding to one observation in our data. 

The sample version of the population moments are $\hat{g}(\theta) \equiv \frac{1}{n}\sum_{i=1}^ng(Y_i,\theta)$. Thus, we are trying find $\theta$ that makes $\hat{g}(\theta)$ as close to $0$ as possible. The GMM estimator is 

$$\hat{\theta}_{GMM} = \underset{\theta}{\operatorname{argmin}}\hat{g}(\theta)^\prime \hat{W}\hat{g}(\theta)$$

Where $\hat{W}$ is some positive semi-definite matrix, which gives us a consistent estimate of true parameters $\theta$ under relatively benign assumptions.

For more details, visit the [Wikipedia Page](https://en.wikipedia.org/wiki/Generalized_method_of_moments). 


## Keep in Mind

- There are two important assumptions necessary for identification, meaning that $\hat{\theta}_{GMM}$ is uniquely minimized at the true value $\theta_0$  
  - **Order Condition**: There are at least as many moment conditions as parameters to be estimated, $L \geq K$.  
  - **Rank Condition**: The $K \times L$ matrix of derivatives $\bar{G}_n(\theta_0)$ will have full column rank, $L$.
- Any positive semi-definite weight matrix $\hat{W}$ will produce an asymptotically consistent estimator for $\theta$, but we want to choose the weight matrix that gives estimates the smallest asymptotic variance. There are various methods for choosing $\hat{W}$ outlined [here](https://en.wikipedia.org/wiki/Generalized_method_of_moments#Implementation), which are various iterative processes
- [Sargan-Hansen J-Test](https://en.wikipedia.org/wiki/Generalized_method_of_moments#Sargan%E2%80%93Hansen_J-test) can be used to test the specification of the model, by determining whether the sample moments are sufficiently close to zero
- The small sample properties of GMM are not great, consider (bootstrapping)[({{ "Model_Estimation/Statistical_Inference/Nonstandard_Errors/bootstrap_se.html" | relative_url }})] or set $\hat{W} = I$ (See Hayashi, Econometrica pg 215)

## Also Consider

- Under certain moment conditions, GMM is equivalent to many other estimators that are used more commonly. These include...
  - **[OLS]({{ "Model_Estimation/OLS/simple_linear_regression.html" | relative_url }})** if $E[x_i(y_i - x_i^\prime\beta)]=0$
  - **[Instrumental Variables]({{ "Model_Estimation/Research_Design/instrumental_variables.html" | relative_url }})** if $E[z_i(y_i - x_i^\prime\beta)]=0$ 
- Maximum likelihood estimation is also a specific case of GMM that makes assumptions about the distributions of the parameters. This gives maximum likelihood better small sample properties


# Implementations

## R

The `gmm` package ([link](https://cran.r-project.org/web/packages/gmm/index.html)) can be used to implement GMM in `R`, with the key function being `gmm()`. The first example recovers the parameters of a normal distribution, where the moment conditions are derived from the [normal distribution](https://en.wikipedia.org/wiki/Normal_distribution#Moments).

```r

# Loading the gmm package
if (!require("pacman")) install.packages("pacman")
pacman::p_load(gmm)

# Parameters we are going to estimate
mu = 3
sigma = 2

# Generating random numbers 
set.seed(0219)
n = 500
x = rnorm(n = n, mean = mu, sd = sigma)

# Moment restrictions 
g1 <- function(theta, x) {
  m1 = (theta[1]-x)
  m2 = (theta[2]^2 - (x - theta[1])^2)
  m3 = x^3-theta[1]*(theta[1]^2+3*theta[2]^2)
  f = cbind(m1,m2,m3)
 return(f)
}

# Running GMM 
gmm_mod = gmm(
  # Moment restriction equations 
  g = g1,
  # Matrix of data
  x = x,
  # Starting location
  t0 = c(0,0)
)

# Reporting results
summary(gmm_mod)
  
```

Another common application of GMM is with linear moment restrictions. These can be specified by writing the regression formula as the `g` argument of the `gmm()` function and the matrix of instruments as the `x` argument. 

```r

# library(gmm) # already loaded
library(gmm)
# Setting parameter values
alpha = 1
beta = 2

# Taking random draws
set.seed(0219)
z1 = rnorm(n = 500, 1,2)
z2 = rnorm(n = 500,-1,1)
e = rnorm(n = 500, 0, 1)

# Collecting instruments
H = cbind(h1, h2)

# Specifying model, where x is endogenous
x = z1 + z2 + e
y = alpha + beta * x + e

# Running GMM
lin_gmm_mod = gmm(
  g = y ~ x,
  x = H
)

# Reporting results
summary(lin_gmm_mod)

```

