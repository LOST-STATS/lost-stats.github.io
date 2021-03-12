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

For additional information about the support vector regression or support vector machine, refer to [Wikipedia: Support-Vector-Machine]().

# Keep in Mind
- Note that we could solve for the optimal hyperplane by solving the following equation:
$$
\text{min} \frac{1}{2} || \omega ||^2 \\
s.t. 
$$
- If data points are not linearly separable, non-linear SVM introduces higher dimensional space that projects data points from original finite-dimensional space to gain linearly separation. Such process of mapping data points into a higher dimensional space is known as the Kernel Trick. There are numerous types of Kernels that can be used to create higher dimensional space including linear, polynomial, Sigmoid, and Radial Basis Function. 
- Setting the right form of kernel is important as it determines the structure of the classifier.


# Also Consider 

- LIST OF OTHER TECHNIQUES THAT WILL COMMONLY BE USED ALONGSIDE THIS PAGE'S TECHNIQUE
- (E.G. LINEAR REGRESSION LINKS TO ROBUST STANDARD ERRORS),
- OR INSTEAD OF THIS TECHNIQUE
- (E.G. PIE CHART LINKS TO A BAR PLOT AS AN ALTERNATIVE)
- WITH EXPLANATION
- INCLUDE LINKS TO OTHER LOST PAGES WITH THE FORMAT [Description]({{ "/Category/page.html" | relative_url }}). Categories include Data_Manipulation, Geo-Spatial, Machine_Learning, Model_Estimation, Presentation, Summary_Statistics, Time_Series, and Other, with subcategories at some points. Check the URL of the page you want to link to on [the published site](https://lost-stats.github.io/).

# Implementations

TEXT.

## R

TEXT.

```r
## Load the necessary packages

## Data Generating Process 


```
