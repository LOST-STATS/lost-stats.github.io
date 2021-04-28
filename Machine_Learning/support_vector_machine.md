---
title: Support Vector Machine
parent: Machine Learning
has_children: false
mathjax: true
nav_order: 1
---

# Support Vector Machine

A support vector machine (hereinafter, SVM) is a supervised machine learning algorithm in that it is trained by a set of data and then classifies any new input data depending on what it learned during the training phase. SVM can be used both for classification and regression problems but here we focus on its use for classification. 

The idea is to separate two distinct groups by maximizing the distance between those points that are most hard to classify. To put it more formally, it maximizes the distance or margin between support vectors around the separating hyperplane. Support vectors here imply the data points that lie closest to the hyperplane. Hyperplanes are decision boundaries that are represented by a line (in two dimensional space) or a plane (in three dimensional space) that separate the two groups. 

Suppose a hypothetical problem of classifying apples from lemons. Support vectors in this case are apples that look closest to lemons and lemons that look closest to apples. They are the most difficult ones to classify. SVM draws a separating line or hyperplane that maximizes the distance or margin between support vectors, in this case the apples that look closest to the lemons and lemons that look closest to apples. Therefore support vectors are critical in determining the position as well as the slope of the hyperplane.  

For additional information about the support vector regression or support vector machine, refer to [Wikipedia: Support-vector machine](https://en.wikipedia.org/wiki/Support-vector_machine).

# Keep in Mind
- Note that optimization problem to solve for a linear separator is maximizing the margin which could be calculated as $$\frac{2}{\lVert w \rVert}$$. This could then be rewritten as minimizing $$\lVert w \rVert$$, or minimizing a monotonic transformation version of it expressed as $$\frac{1}{2}\lVert w \rVert^2$$. Additional constraint of $$y_i(w^T x_i + b) \geq 1$$ needs to be imposed to ensure that the data points are still correctly classified. As such, the constrained optimization problem for SVM looks as the following:  

$$
\text{min} \frac{\lVert w \rVert ^2}{2}
$$

s.t. $$y_i(w^T x_i + b) \geq 1$$, 

where $$w$$ is a weight vector, $$x_i$$ is each data point, $$b$$ is bias, and $$y_i$$ is each data point's corresponding label that takes the value of either $$\{-1, 1\}$$. 
For detailed information about derivation of the optimization problem, refer to [MIT presentation slides](http://web.mit.edu/6.034/wwwbob/svm-notes-long-08.pdf), [The Math Behind Support Vector Machines](https://www.byteofmath.com/the-math-behind-support-vector-machines/), and [Demystifying Maths of SVM - Part1](https://towardsdatascience.com/demystifying-maths-of-svm-13ccfe00091e).

- If data points are not linearly separable, non-linear SVM introduces higher dimensional space that projects data points from original finite-dimensional space to gain linearly separation. Such process of mapping data points into a higher dimensional space is known as the Kernel Trick. There are numerous types of Kernels that can be used to create higher dimensional space including linear, polynomial, Sigmoid, and Radial Basis Function. 

- Setting the right form of Kernel is important as it determines the structure of the separator or hyperplane.

# Also Consider 

- See the alternative classification method described on the [K-Nearest Neighbor Matching]({{ "/Machine_Learning/Nearest_Neighbor.html" | relative_url }}). 


# Implementations

## R

Following codes describe how to implement SVM in R. SVM relies on ``e1071`` package. To learn more about the package, check out its [CRAN page](https://cran.r-project.org/web/packages/e1071/index.html), as well as [this vignette](https://cran.r-project.org/web/packages/e1071/vignettes/svmdoc.pdf). Several other packages are also loaded to help us manipulate data (**dplyr**, **tidyverse**) and plot the results (**ggplot2**). 

Two examples are shown below that use linear SVM and non-linear SVM respectively. The first example shows how to implement linear SVM. We start by constructing data, separating them into training and test set. Using the training set, we fit the data using the `svm()` function. Notice that kernel argument for ``svm()`` function is specified as *linear* for our first example. Next, we predict the test data based on the model estimates using the `predict()` function. The first example result suggests that only one out of 59 data points is incorrectly classified. 

The second example shows how to implement non-linear SVM. The data in example two is generated in a way to have data points of one class centered around the middle whereas data points of the other class spread on two sides. Notice that kernel argument for the `svm()` function is specified as **radial** for our second example, based on the shape of the data. The second example result suggests that only two out of 58 data points are incorrectly classified. 

```r
# Install and load the packages
if (!require("tidyverse")) install.packages("tidyverse")
if (!require("e1071")) install.packages("e1071")
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("dplyr")) install.packages("dplyr")
library(tidyverse) # package for data manipulation
library(e1071)     # package for SVM 
library(ggplot2)   # package for plotting

###########################
# Example 1: Linear SVM ###
###########################

# Construct a completely separable data set
## Set seed for replication
set.seed(0715) 
## Make variable x 
x = matrix(rnorm(200, mean = 0, sd = 1), nrow = 100, ncol = 2) 
## Make variable y that labels x by either -1 or 1
y = rep(c(-1, 1), c(50, 50)) 
## Make x to have unilaterally higher value when y equals 1 
x[y == 1,] = x[y == 1,] + 3.5 
## Construct data set
d1 = data.frame(x1 = x[,1], x2 = x[,2], y = as.factor(y))
## Split it into training and test data
flag = sample(c(0,1), size = nrow(d1), prob=c(0.5,0.5), replace = TRUE) 
d1 = setNames(split(d1, flag), c("train", "test"))

# Plot
ggplot(data = d1$train, aes(x = x1, y = x2, color = y, shape = y)) +
  geom_point(size = 2) + 
  scale_color_manual(values = c("darkred", "steelblue"))

# SVM classification 
svmfit1 = svm(y ~ ., data = d1$train, kernel = "linear", cost = 10, scale = FALSE)
print(svmfit1)
plot(svmfit1, d1$train)

# Predictability
pred.d1 = predict(svmfit1, newdata = d1$test) 
table(pred.d1, d1$test$y)

###############################
# Example 2: Non Linear SVM ###
###############################

# Construct less separable data set
## Make variable x 
x = matrix(rnorm(200, mean = 0, sd = 1), nrow = 100, ncol = 2) 
## Make variable y that labels x by either -1 or 1
y <- rep(c(-1, 1) , c(50, 50)) 
## Make x to have extreme values when y equals 1 
x[y == 1, ][1:25,] = x[y==1,][1:25,] + 3.5
x[y == 1, ][26:50,] = x[y==1,][26:50,] - 3.5
## Construct data set
d2 = data.frame(x1 = x[,1], x2 = x[,2], y = as.factor(y)) 
## Split it into training and test data
d2 = setNames(split(d2, flag), c("train", "test"))

# Plot data
ggplot(data = d2$train, aes(x = x1, y = x2, color = y, shape = y)) +
  geom_point(size = 2) + 
  scale_color_manual(values = c("darkred", "steelblue"))

# SVM classification
svmfit2 = svm(y ~ ., data = d2$train, kernel = "radial", cost = 10, scale = FALSE)
print(svmfit2)
plot(svmfit2, d2$train)

# Predictability
pred.d2 = predict(svmfit2, newdata = d2$test) 
table(pred.d2, d2$test$y)

```

## Stata 

The below code shows how to implement support vector machines in Stata using the svmachines command. To learn more about this community contriuted command, you can read [this Stata Journal article.](http://schonlau.net/publication/16svm_stata.pdf)

```stata
clear all
set more off 

*Install svmachines
ssc install svmachines

*Import Data with a binary outcome for classification
use http://www.stata-press.com/data/r16/fvex.dta, clear

*First try logistic regression to benchmark the prediction quality of SVM against 
logit outcome group sex arm age distance y // Run the regression
predict outcome_predicted // Generate predictions from the regression

*Calculate the log loss - see https://ml-cheatsheet.readthedocs.io/en/latest/loss_functions.html for more info
gen log_loss = outcome*log(outcome_predicted)+(1-outcome)*log(1-outcome_predicted)

*Run SVM 
svmachines outcome group sex arm age distance y, prob // Specifiying the 
predict sv_outcome_predicted, probability
```

Next we will Calculate the [log loss (or cross-entropy loss)](https://ml-cheatsheet.readthedocs.io/en/latest/loss_functions.html) for SVM.
  
Note: Predictions following svmachines generate three variables from the stub you provide in the predict command (in this case sv_outcome_predicted). The first is just the same as the stub and stores the best-guess classification (the group with the highest probability out of the possible options). The next n variables store the probability that the given observation will fall into each of the possible classes (in the binary case, this is just n=2 possible classes). These new variables are the stub + the value of each class. In the case below, the suffixes are `_0` and `_1`. We use `sv_outcome_predicted_1` because it produces probabilities that are equivalent in their intepretation (probability of having a class of 1) to the probabilities produced by the logit model and that can be used in calculating the log loss. Calculating loss functions for multi-class classifiers is more complicated, and you can read more about that at the link above. 

```stata
gen log_loss_svm = outcome*log(sv_outcome_predicted_1)+(1-outcome)*log(1-sv_outcome_predicted_1)

*Show log loss for both logit and SVM, remember lower is better
sum log_loss log_loss_svm
```
