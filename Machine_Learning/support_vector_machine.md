---
title: Support Vector Machine
parent: Machine Learning
has_children: false
mathjax: true
nav_order: 1
---

# Support Vector Regression

A support vector machine (hereinafter, SVM) is one of the classification techniques. The idea is to separate two distinct groups by maximizing the distance between those points that are most hard to classify. To put it more formally, it maximizes the distance or margin between support vectors around the separating hyperplane. Support vectors here imply the data points that lie closest to the hyperplane. Hyperplanes are decision boundaries that are represented by a line (in two dimensional space) or a plane (in three dimensional space) that separate the two groups. 

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

- Setting the right form of kernel is important as it determines the structure of the separator or hyperplane.

# Also Consider 

- See the alternative classification method described on the [K-Nearest Neighbor Matching]({{ "/Machine_Learning/Nearest_Neighbor.html" | relative_url }}). 


# Implementations

TEXT.

## R

TEXT.

```r
# Load the necessary packages
## 
## 

# Data Generating Process 


```
