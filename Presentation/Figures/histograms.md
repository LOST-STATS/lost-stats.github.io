---
title: Histograms
parent: Figures
grand_parent: Presentation ## Optional for indexing
has_children: false
mathjax: true
nav_order: 1
---
  
# Histograms
  
*Histograms* are an indespensible tool of research across disciplines. They offer a helpful way to represent the distribution of a variable of interest. Specifically, their function is to record how frequently data values fall within pre-specified ranges called "bins." Such visual representations can help researchers easily detect whether their data are distributed in a skewed or symmetric way, and can help detect outliers. 

Despite being such a popular tool for scientific research, choosing the bin width (alternatively, number of bins) is ultimately a choice by the researcher. Histograms are intended to convey information about the variable, and choosing the "right" bin size to convey the information helpfully can be something of an art.

The relationship between bin width $$h$$ and the number of bins $$k$$ is given by:

$$
k = \frac{ \max x - \min x}{h}
$$

For this reason, statistical softwares such as R and Stata will often accept either custom bin width specifications, or a number of bins.

## Histogram vs. bar graph

Because histograms represent data frequency using rectangular bars, they might be mistaken for [bar graphs](https://lost-stats.github.io/Presentation/Figures/bar_graphs.html) at first glance. Whereas bar graphs (sometimes called bar charts) plot values for *categorical* data, histograms represent the distribution of continuous variables such as income, height, weight, etc.

# Implementations

When feeding data to visualise using a histogram, one will notice that both R and Stata will attempt to "guess" what the "best" bin width/number of bins are. These may be overridden by user commands, as we will see.

## R

Histograms can be represented using base `R`, or more elegantly with `ggplot`. `R` comes with a built-in `states.x77` dataset containing per-capita income in the US states for the year 1974, which we will be using.

```r

# loading the data

incomes = data.frame( income = state.x77[,'Income'])

# first using base R

hist(incomes$income)

# now using ggplot

if(!require(ggplot2)) install.packages('ggplot2')
library(ggplot2)

ggplot( data = incomes ) + 
geom_histogram( aes( x = income ) )

# showing how we can adjust number of bins...

ggplot( data = incomes ) + 
geom_histogram( aes( x = income ) ,
                bins = 15 )

# ...or the width of each bin

ggplot( data = incomes ) + 
geom_histogram( aes( x = income ) ,
                binwidth = 500 )
```

## Stata

To illustrate the basic histogram function in Stata we will use the "auto" dataset.

```stata

** loading the data

webuse auto

* histogram with default bin width
* The frequency option puts a count of observations on the y-axis
* rather than a proportion

histogram mpg, frequency

* we can adjust the number of bins...

histogram mpg, bin(15) frequency

* ...or the bin width

hist mpg, width(2) frequency

```
