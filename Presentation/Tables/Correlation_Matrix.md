---
title: Correlation Matrix
parent: Tables
grand_parent: Presentation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Correlation Matrixes 

A correlation matrix is a table used to present the results of correlation tests between multiple variables at a time. A correlation test is a statistical method used to define the correlation between two (and sometimes more) variables. The correlation coefficients from these tests are what a correlation matrix is composed of.

## Keep in Mind

When creating a correlation matrix it is important to consider the which type of method for correlation analysis will best meet your needs. While the most common is the Pearson Correlation Coefficient, the Spearman and the Kendall methods are also viable possibilities. The Pearson measures the linear dependence between two variables while Spearman and the Kendall methods use a rank-based, non-parametric correlation test. 

## Also Consider

As with most kinds of statistical analysis it is important to choose how to deal with missing values in your dataset when creating a correlation matrix. The most common method is to only include complete observations in the correlation test. This is a form of pairwise missing values. Pairwise missing values has an underlying assumption that all missing values are random, which is not necessarily the case. Multiple imputation is a often a better choice for dealing with missing values. It is just not as straightforward to do. 

# Implementation

## R 

```r
# If necessary
install.packages('corrr')
library(corrr)
data(mtcars)

#computing the correlation test using the pearson method
#changing the method to "spearman" or "kendall" will change the type of correlation test used
#"complete.obs" is a casewise deletion method for datasets with missing values

cor_test <- cor(mtcars, method = "pearson", use = "complete.obs")

#Creating the correlation matrix for the previous correlation test
round(cor_test)
```

The *cor()* function only creates correlation matrices with correlation coefficients. If you want to also include the p-values you will need to use the *rcorr()* function from the *Hmisc package.* This will only work for correlation tests using the Pearson or Spearman Methods.

```r
install.packages('Hmisc')
library(Hmisc)
data(mtcars)

#computing the correlation matrix using the pearson method (which is the default for rcorr())
cor_test2 <- rcorr(as.matrix(mtcars))

cor_test2
```

While the previous commands create correlation matrices *corrplot()* can be used to create a correlogram, which is a graphical display of a correlation matrix. The main difference between this and the matrices created above is that this plot will provide a visual representation of the correlation coefficients using a gradient of colors instead of displaying the coefficients themselves.

```r
install.packages("corrplot")
library(corrplot)
data(mtcars)

#replicating the first correlation matrix created above
cor_test <- cor(mtcars, method = "pearson", use = "complete.obs")

#creating the correlogram for cor_test
corrplot(cor_test, order = "hclust", 
         tl.col = "black", tl.srt = 45)
         
#it is also possible to create the plot and only include the upper portion 
corrplot(cor_test, type = "upper", order = "hclust", 
         tl.col = "black", tl.srt = 45)
```
