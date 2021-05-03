---
title: Generalized Method of Moments
parent: Generalised Least Squares
grand_parent: Model Estimation
has_children: false
nav_order: 1
mathjax: true 
---

# Generalized Method of Moments  

GMM is an estimation technique that does not require strong assumptions about the distributions of the underlying parameters. The key intuition is that if we know the expected value of population moments (such as mean or variance), then the sample equivalents will converge to that expected value using the law of large numbers. If the moments are functions of the parameters that we wish to estimate, then we can use these moment restrictions to estimate our parameters.

Suppose we have a vector of $$K$$ parameters we want to estimate, where the true values of those parameters are $$\theta_0$$ and a set of $$L \geq K$$ moment conditions provided by theory, $$E\left[g(Y_i,\theta_0)\right] = 0$$, where $$Y_i$$ is a vector of variables corresponding to one observation in our data. 

The sample version of the population moments are $$\hat{g}(\theta) \equiv \frac{1}{n}\sum_{i=1}^ng(Y_i,\theta)$$. Thus, we are trying find $$\theta$$ that makes $$\hat{g}(\theta)$$ as close to $$0$$ as possible. The GMM estimator is 

$$
\hat{\theta}_{GMM} = \underset{\theta}{\operatorname{argmin}}\hat{g}(\theta)^\prime \hat{W}\hat{g}(\theta)
$$

Where $$\hat{W}$$ is some positive semi-definite matrix, which gives us a consistent estimate of true parameters $$\theta$$ under relatively benign assumptions.

For more details, visit the [Wikipedia Page](https://en.wikipedia.org/wiki/Generalized_method_of_moments). 


## Keep in Mind

- There are two important assumptions necessary for identification, meaning that $$\hat{\theta}_{GMM}$$ is uniquely minimized at the true value $$\theta_0$$  
  - **Order Condition**: There are at least as many moment conditions as parameters to be estimated, $$L \geq K$$.  
  - **Rank Condition**: The $$K \times L$$ matrix of derivatives $$\bar{G}_n(\theta_0)$$ will have full column rank, $$L$$.
- Any positive semi-definite weight matrix $$\hat{W}$$ will produce an asymptotically consistent estimator for $$\theta$$, but we want to choose the weight matrix that gives estimates the smallest asymptotic variance. There are various methods for choosing $$\hat{W}$$ outlined [here](https://en.wikipedia.org/wiki/Generalized_method_of_moments#Implementation), which are various iterative processes
- [Sargan-Hansen J-Test](https://en.wikipedia.org/wiki/Generalized_method_of_moments#Sargan%E2%80%93Hansen_J-test) can be used to test the specification of the model, by determining whether the sample moments are sufficiently close to zero
- The small sample properties of GMM are not great, consider [bootstrapping]({{ "Model_Estimation/Statistical_Inference/Nonstandard_Errors/bootstrap_se.html" | relative_url }}) or set $$\hat{W} = I$$ (See Hayashi, Econometrics pg 215)

## Also Consider

- Under certain moment conditions, GMM is equivalent to many other estimators that are used more commonly. These include...
  - **[OLS]({{ "Model_Estimation/OLS/simple_linear_regression.html" | relative_url }})** if $$E[x_i(y_i - x_i^\prime\beta)]=0$$
  - **[Instrumental Variables]({{ "Model_Estimation/Research_Design/instrumental_variables.html" | relative_url }})** if $$E[z_i(y_i - x_i^\prime\beta)]=0$$ 
- Maximum likelihood estimation is also a specific case of GMM that makes assumptions about the distributions of the parameters. This gives maximum likelihood better small sample properties, at the cost of the stronger assumptions  


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
  # Starting location for minimization algorithm
  t0 = c(0,0) # Required when g argument is a function
)

# Reporting results
summary(gmm_mod)
  
```

Another common application of GMM is with linear moment restrictions. These can be specified by writing the regression formula as the `g` argument of the `gmm()` function and the matrix of instruments as the `x` argument. Suppose we have a model $$y_i = \alpha + \beta x_i + \epsilon_i$$, but $$E[x_i(y_i - x_i^\prime\beta)]\neq 0$$, so OLS would produce a biased estimate of $$\beta$$. If we have a vector of instruments $$z_i$$ that are correlated with $$x_i$$ and have moment conditions $$E[z_i(y_i - x_i^\prime\beta)]=0$$, then we can use GMM to estimate $$\beta$$. 

```r

# library(gmm) # already loaded

# Setting parameter values
alpha = 1
beta = 2

# Taking random draws
set.seed(0219)
z1 = rnorm(n = 500, 1,2)
z2 = rnorm(n = 500,-1,1)
e = rnorm(n = 500, 0, 1)

# Collecting instruments
Z = cbind(z1, z2)

# Specifying model, where x is endogenous
x = z1 + z2 + e
y = alpha + beta * x + e

# Running GMM
lin_gmm_mod = gmm(
  g = y ~ x,
  x = Z
)

# Reporting results
summary(lin_gmm_mod)

```


## Stata

Stata provides an official command `gmm`, which can be used for the estimation of models via this method if you provide moments of interest. 

The first example will be in recovering the coefficients that determine the distribution of a variable, assuming that variable follows a normal distribution.

First lets simulate some data, and set the parameters

```stata
**# Normal distribution

*** Parameters to estimate
local mu    = 3
local sigma = 2

*** Generate sample
set seed 219
clear
set obs 500
gen x = rnormal(`mu',`sigma')
```

In this code, I use `local` to identify the true parameters of interest. the mean `mu` and standard deviation `sigma`. Im also using `set seed`, to simulare data that can be replicated. The variable `x` is obtained based on a random draw from a normal distribution.

The next step is to declare all the moment conditions. Here Im declaring them with `local` but could be written just as well with `global` or written directly instead of the ``m1'` expressions in the `gmm` command.

Keep in mind that `locals` only stay in memory _locally_. Once you run the program, they dissapear. _Globals_ instead, can be used at any point after they are declared. For this reason, when using the code for this example, either copy it by hand into the console, or put it all in the *same* do file and run it together, so the locals are all in the same environment together.

In the `gmm` syntax below, the coefficients of interest to be estimated, are written within curly brakets "{}". I can also declare within the brakets initial values for the coefficients. Here `mu=1` and `sigma=1`.

Following the example above, we can declare 3 equations to define the moments for a normal distribution: the mean, the variance, and the kurtosis. However, because there are only 2 unknowns (mean and standard deviation), the model will be overidentified. This means that I can use either all 3 moments, or just any 2 of them.

In this case, because the true distribution is normal, you only need two parameters to describe the distribution. Thus, you should get the same results, (or quite close), regardless of which pair of moments you use.

```stata
*** Declare moments restrictions
local m1  {mu=1}-x
local m2  {sigma=1}^2 - (x-{mu=1})^2
local m3  x^3 - {mu=1}*({mu}^2+3*{sigma=1}^2)
gmm (`m1') (`m2') (`m3'), winitial(identity) 
est sto m1
gmm (`m1') (`m2') , winitial(identity) 
est sto m2
gmm (`m1') (`m3') , winitial(identity) 
est sto m3
gmm (`m2') (`m3') , winitial(identity) 
est sto m4
est tab m1 m2 m3 m4, se
```

A second example for the use of `gmm` is for the estimation of standard linear regression models. 
For this, lets create some data, where the variable of interest is $$X$$ 

```stata
**# LR estimation

*** Parameters to estimate 
local a0 1
local a1 2
clear
set obs 500
*** Exogenous variables
gen z1 = rnormal(1,2)
gen z2 = rnormal(-1,1)

*** unobserved error
gen e = rnormal()

*** Data Generating process
gen x = z1+z2+e     // X is endogenous to e
gen y=`a0'+`a1'*x+e
```

Next, we can use `gmm` to estimate the model, under different assumptions

```stata
*** gmm ignoring endogeneity
** this is your error
local m1 y-{a0}-{a1}*x  
** which implies First order condition E(m1)=0 
** and E(x*m1)=0 
gmm (`m1'), winitial(identity) instrument(x)

*** gmm with endogeneity
** here, it implies E(z*m1)=0 
local m1 y-{a0}-{a1}*x
gmm (`m1'), winitial(identity) instrument(z1)
est sto m1
gmm (`m1'), winitial(identity) instrument(z2)
est sto m2
gmm (`m1'), winitial(identity) instrument(z1 z2)
est sto m3
est tab m1 m2 m3, se

** I could also write the moment conditions more explicitly
local m1 y-{a0}-{a1}*x
gmm (`m1') (z1*(`m1')), winitial(identity)
est sto m1
gmm (`m1') (z2*(`m1')), winitial(identity) 
est sto m2
gmm (`m1') (z1*(`m1')) (z2*(`m1')), winitial(identity)  
est sto m3
est tab m1 m2 m3, se
** producing the same results as before
```

