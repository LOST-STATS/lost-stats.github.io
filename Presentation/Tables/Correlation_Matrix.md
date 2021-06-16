---
title: Correlation Matrix
parent: Tables
grand_parent: Presentation ## Optional for indexing
has_children: false
nav_order: 1
---

# Correlation Matrixes 

A correlation matrix is a table used to present the results of correlation tests between multiple variables at a time. A correlation test is a statistical method used to define the correlation between two (and sometimes more) variables. The correlation coefficients from these tests are what a correlation matrix is composed of. They are often used as a method to summarize large amounts of data with the intention of identifying patterns of highly correlated variables. They can be a key component to checking the viability of other analyses.

## Keep in Mind

- When creating a correlation matrix it is important to consider the which type of method for correlation analysis will best meet your needs. While the most common is the Pearson Correlation Coefficient, the Spearman and the Kendall methods are also viable possibilities. The Pearson measures the linear dependence between two variables while Spearman and the Kendall methods use a rank-based, non-parametric correlation test. 
- Correlation only measures a *linear* relationship between two variables. Correlation will not pick up on non-linearity, and sometimes the correlation may be zero even when the two variables are clearly related.
- - As with most kinds of statistical analysis it is important to choose how to deal with missing values in your dataset when creating a correlation matrix. The most common method is to only include complete observations in the correlation test. This is a form of pairwise missing values. Pairwise missing values has an underlying assumption that all missing values are random, which is not necessarily the case. Multiple imputation is in some cases a often a better choice for dealing with missing values. It is just not as straightforward to do. 
- Thinking more about missing values, there are two approaches to dropping missing values (if that's what you're doing). One approach, the **complete observations** approach, is to drop an observation from *all* calculations for the entire matrix if it contains any missing values. So in a correlation matrix for the variables $A$, $B$, and $C$, and row 1 of the data was missing its $C$ value, it would also be dropped from the calculation of $Corr(A,B)$. This first approach is preferred if you want to understand the correlation structure of an analysis that will drop observations in a similar way, like a covariance matrix or a linear regression. The second approach, the **pairwise complete observations** approach, is to only drop observations from correlation calculations involving missing data, so row 1 with a missing $C$ value would be dropped from $Corr(B,C)$ and $Corr(A,C)$, but not from $Corr(A,B)$. This sceond approach is preferred if you want to understand the overall relationships between the variables.

## Also Consider

- Correlations measure linear relationships, and so are effectively rescaled versions of results from [Ordinary Least Squares]({{ "/Model_Estimation/OLS/simple_linear_regression.html" | relative_url }}) regression
- Correlation matrices can be visualized as [Heatmap Correlation Matrices]({{ "/Presentation/Figures/heatmap_colored_correlation_matrix.html" | relative_url }})


# Implementation

## Python

```python
import pandas as pd
import numpy as np

d = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/datasets/mtcars.csv")

# Get the correlation matrix
d.corr()

# Default is Pearson but we can do Kendall or Spearman with method
d.corr(method = 'spearman')

# This approach uses pairwise-complete correlations by default, but we can
# drop non-complete rows first to do a complete-cases correlation matrix
d.dropna().corr()

# If we want significance we'll have to do it one at a time
# (although we could build a loop to get it for all pairs of columns)
# We could get a p-value by just running OLS, or we can use Pearson directly
from scipy import stats

pvalue = stats.pearsonr(d['mpg'],d['disp'])[1]
```

## R 

```r
data(mtcars)

# computing the correlation test using the pearson method
# changing the method to "spearman" or "kendall" will change the type of correlation test used
# "complete.obs" is a casewise deletion method for datasets with missing values

cor_test <- cor(mtcars, method = "pearson", use = "complete.obs")

# Creating the correlation matrix for the previous correlation test
round(cor_test)

# To do a pairwise-complete approach, where observations with missing data in some variables
# are still included in correlations for others, do use = "pairwise.complete.obs"
# (no difference in this case since there's no missing data)
cor(mtcars, method = "pearson", use = "pairwise.complete.obs")
```

The *cor()* function only creates correlation matrices with correlation coefficients. If you want to also include the p-values you will need to use the *rcorr()* function from the *Hmisc package.* This will only work for correlation tests using the Pearson or Spearman Methods.

```r
library(Hmisc)
data(mtcars)

#computing the correlation matrix using the pearson method (which is the default for rcorr())
cor_test2 <- rcorr(as.matrix(mtcars))

cor_test2
```

## Stata

```stata
sysuse auto.dta, clear

* For a basic correlation matrix using Pearson, use cor
* This uses a complete cases method
cor *

* To do a pairwise-complete method, use pwcorr
pwcorr *

* You can also perform significance tests on the 
* individual correlations using the sig option
pwcorr *, sig
* p-values are below each correlation
```
