---
title: Binned Scatterplots
parent: Figures
grand_parent: Presentation ## Optional for indexing
mathjax: yes
nav_order: 1
# output:
#   html_document:
#     df_print: paged
has_children: no
---


# Introduction

Binned scatterplots are a variation on scatterplots that can be useful when there are too many data points that are being plotted. Binned scatterplots take all data observations from the original scatterplot and place each one into exactly one group called a bin. Once every observation is in a bin, each bin will get one point on a scatterplot, reducing the amount of clutter on your plot, and potentially making trends easier to see visually. 

## Keep in Mind

- Bins are determined based on the conditioning variable (usually the x variable). Bin width can be determined in multiple ways. For example, you can set bin width with the goal of getting the same amount of observations into each bin. In this scenario, bins will likely all differ in width unless your data observations are equally spaced. You could also set bin width so that every bin is of equal width (and has unequal amount of observations falling into each bin).
- Once observations are placed into bins using the conditioning variable, an outcome variable (usually the y variable) is produced by aggregating all observations in the bin and using a summary statistic to obtain one single point. Possible summary statistics that can be used include mean, median, max/min, or count.
- The number of bins you will separate your data into is the most important decision you will likely make. There is no one way to determine this (the binsreg package in R has a default optimal number of bins that it calculates), but you will face the bias-variance trade off when selecting this parameter.


## Also Consider

- [Scatterplots]({{ "/Presentation/Figures/Scatterplots.html" | relative_url}})
- [Styling Scatterplots]({{ "/Presentation/Figures/Styling_Scatterplots.html" | relative_url }})
- Binned scatterplots are used frequently used in [Regression Discontinuity]({{ "/Model_Estimation/Research_Design/regression_discontinuity_design.html" | relative_url }}) 


# Implementations

## R

For the examples below I will be using this created data:
```r
x = rnorm(mean=50, sd=50, n=10000)
y =  x + rnorm(mean=0, sd=100, n=10000)
df = data.frame(x=x, y=y)
```

```r
library(ggplot2)
ggplot(df, aes(x=x, y=y)) + 
  geom_point()
```

![Our Data Plotted](Images/binscatter/data.png)

After plotting, we can see that there may be a trend, but the graph is over cluttered and not easy to interpret right away. This is when binned scatterplots are most useful.

There are multiple ways to code observations into bins, but we will do it simply creating a new 'bin' column in dplyr for this example. However, you can look [here](https://towardsdatascience.com/goodbye-scatterplot-welcome-binned-scatterplot-a928f67413e4) for an example using the binsreg package.

```r
library(dplyr)

# this will create 25 quantiles using y and assign the observations in each quantile to a separate bin
df = df %>% mutate(bin = ntile(y, n=25))

new_df = df %>% group_by(bin) %>% summarise(xmean = mean(x), ymean = mean(y)) #find the x and y mean of each bin

ggplot(new_df, aes(x=xmean, y=ymean)) + 
  geom_point()

```

![Binned Data Plotted](Images/binscatter/binscatter.png)

After binning and summarizing the data, we can identify the trend much easier! (but lose a sense of the very high variance)
