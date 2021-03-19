---
title: Propensity Score Matching
parent: Model Estimation / Research Design
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

## Conceptual Basis

Drawing causal inferences from non-random, observational data faces a critical methodological challenge. Treatment and non-treatment groups are not equal in expectation so the observed differences in outcomes cannot be attributed to the treatment condition. Propensity score matching (PSM) method is intended to overcome this challenge. The big idea is: if we can find a set of covariates ($X_i$) that is determinant of whether a participant gets treated or not, we can estimate a treatment effect by using only the observations with identical value of $X_i$. In other words, the PSM approach is based on the conditional independence assumption (CIA), i.e., treatment is considered as good as random conditional on $X_i$.  

## The Matching Workflow

Thanks to Dr. David D. Liebowitz's causal inference in educational research [class](https://www.daviddliebowitz.com/teaching){target = "blank"} at the University of Oregon, College of Education, I learned the following steps to conduct PSM in practice: 

1. Investigate the selection process explicitly by fitting a "selection model". Specifically, fit a logistic regression model below with treatment group membership as the outcome variable and predictors you believe describe the process of selection. 

$$ D_i = \frac{1}{1 + e^{-X_i \theta_i}} $$

2. Use the fitted selection model to estimate the fitted probability of selection into treatment ($\hat{p}$) for each participant, store these propensity scores (estimated probabilities) into a new variable in your dataset. 

3. Stratify the sample using the propensity scores. A rule of thumb here is at least five strata (removing up to 90% of the observed bias). 

4. Within each stratum, check whether the balancing condition has been satisfied. If not, re-stratify (combining or splitting strata) or go back to re-specify your $X_i$ until balance is achieved.

5. Estimate the treatment effect within each stratum.

6. Average the estimated effects up.

## Keep in Mind


## Also Consider

- LIST OF OTHER TECHNIQUES THAT WILL COMMONLY BE USED ALONGSIDE THIS PAGE'S TECHNIQUE
- (E.G. LINEAR REGRESSION LINKS TO ROBUST STANDARD ERRORS),
- OR INSTEAD OF THIS TECHNIQUE
- (E.G. PIE CHART LINKS TO A BAR PLOT AS AN ALTERNATIVE)
- WITH EXPLANATION
- INCLUDE LINKS TO OTHER LOST PAGES WITH THE FORMAT [Description]({{ "/Category/page.html" | relative_url }}). Categories include Data_Manipulation, Geo-Spatial, Machine_Learning, Model_Estimation, Presentation, Summary_Statistics, Time_Series, and Other, with subcategories at some points. Check the URL of the page you want to link to on [the published site](https://lost-stats.github.io/).

# Implementations

## NAME OF LANGUAGE/SOFTWARE 1

```identifier for language type, see this page: https://github.com/jmm/gfm-lang-ids/wiki/GitHub-Flavored-Markdown-%28GFM%29-language-IDs
Commented code demonstrating the technique
```

## NAME OF LANGUAGE/SOFTWARE 2 WHICH HAS MULTIPLE APPROACHES

There are two ways to perform this technique in language/software 2.

First, explanation of what is different about the first way:

```identifier for language type, see this page: https://github.com/jmm/gfm-lang-ids/wiki/GitHub-Flavored-Markdown-%28GFM%29-language-IDs
Commented code demonstrating the technique
```

Second, explanation of what is different about the second way:

```identifier for language type, see this page: https://github.com/jmm/gfm-lang-ids/wiki/GitHub-Flavored-Markdown-%28GFM%29-language-IDs
Commented code demonstrating the technique
```
