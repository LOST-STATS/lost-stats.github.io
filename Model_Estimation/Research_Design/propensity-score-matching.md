---
title: Propensity Score Matching
parent: Research Design
grand_parent: Model Estimation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Propensity Score Matching

## Conceptual Basis

Drawing causal inferences from non-random, observational data faces a critical methodological challenge. Treatment and non-treatment groups are not equal in expectation so the observed differences in outcomes cannot be attributed to the treatment condition. Propensity score matching (PSM) method is intended to overcome this challenge. The big idea is: if we can find a set of covariates ($X_i$) that is determinant of whether a participant gets treated or not, we can estimate a treatment effect by using only the observations with identical value of $X_i$. In other words, the PSM approach is based on the conditional independence assumption, i.e., treatment is considered as good as random conditional on a known set of $X_i$.  

## The Matching Workflow

Thanks to Dr. David D. Liebowitz's causal inference in educational research  [class](https://www.daviddliebowitz.com/teaching) at the University of Oregon, College of Education, I learned the following steps to conduct PSM in practice: 

1. Investigate the selection process explicitly by fitting a "selection model". Specifically, fit a logistic regression model below with treatment group membership as the outcome variable and predictors you believe describe the process of selection. 

$$ D_i = \frac{1}{1 + e^{-X_i \theta_i}} $$

2. Use the fitted selection model to estimate the fitted probability of selection into treatment ($\hat{p}$) for each participant, store these propensity scores (estimated probabilities) into a new variable in your dataset. 

3. Stratify the sample using the propensity scores. A rule of thumb here is at least five strata (removing up to 90% of the observed bias). 

4. Within each stratum, check whether the balancing condition has been satisfied. If not, re-stratify (combining or splitting strata) or go back to re-specify your $X_i$ until balance is achieved.

5. Estimate the treatment effect within each stratum.

6. Average the estimated effects up.

## Keep in Mind

PSM is not a magic way to create treatment and control conditions out of non-random, observational data. You have to present evidence that the conditional independence assumption is met before you go ahead and use the approach. 

## Also Consider

There are many approaches to implement PSM: 

 - Nearest neighbor (Euclidian or Mahalanobisdistance)  
 - Kernel matching  
 - Machine learning  
 - Calipers  
 - With or without replacement  

## Implementation  

An awesome tutorial of how to implement PSM in R by [Simon Ejdemyr](https://github.com/sejdemyr) is [here](https://sejdemyr.github.io/r-tutorials/statistics/tutorial8.html).
