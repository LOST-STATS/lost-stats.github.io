---
title: "Density Plots"
parent: Figures
grand_parent: Presentation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

## Introduction

A density plot visualises the distribution of data over a continuous interval (or time period). Density Plots are not affected by the number of bins (each bar used in a typical histogram) used, thus, they are better at visualizing the shape of the distribution than a histogram unless the bins in the histogram have a theoretical meaning.

## Keep in Mind

- Notice that the variable on the x-axis should be continuous. Density plots are not designed for use with discrete variables.

## Also Consider

= You might also want to know how to make a histogram or a line graph, click [Histogram]({{ "/Presentation/Figures/histograms.html" | relative_url }}) or [Line graph]({{ "/Presentation/Figures/line_graphs.html" | relative_url }}) for more information.


# Implementations

## R

For this R demonstration, we are going to use **ggplot2** package to create a density plot. Additionally, we will use the dataset `diamonds` that is made available by the **ggplot2** package.

To begin with this R demonstration, make sure that we install and load all the useful packages that we need it.

```r?example=density
# load necessary packages
library(ggplot2)
library(viridis)
library(RColorBrewer)
library(tidyverse)
library(ggthemes)
library(ggpubr)
library(datasets)
```

Next, in order to make a density plot, we are going to use the `ggplot()` and `geom_density()` functions. We will specify `price` as our x-axis.

```r?example=density
ggplot(diamonds, aes(x = price)) +
  geom_density()
```
![Basic density plot]({{ "/Presentation/Figures/Images/density_plot/1.png" | relative_url }})

We can always change the color of the density plot using the `col` argument and fill the color inside the density plot using `fill` argument. Furthermore, we can specify the degree of transparency density fill area using the argument `alpha` where `alpha` ranges from 0 to 1.

```r?example=density
ggplot(diamonds, aes(x = price)) +
  geom_density(fill = "lightblue", col = "black", alpha = 0.6)
```

![Colored density plot]({{ "/Presentation/Figures/Images/density_plot/2.png" | relative_url }})
We can also change the type of line of the density plot as well by adding `linetype=` inside `geom_density()`.

```r?example=density
ggplot(diamonds, aes(x = price)) +
  geom_density(fill = "lightblue", col = "black", linetype = "dashed")
```

![Density plot with linetype]({{ "/Presentation/Figures/Images/density_plot/3.png" | relative_url }})
Furthermore, you can also combine both histogram and density plots together.

```r?example=density
ggplot(diamonds, aes(x = price)) +
  geom_histogram(aes(y = ..density..), colour = "black", fill = "grey45") +
  geom_density(col = "red", size = 1, linetype = "dashed")
```
![Density Plot Overlaid on Histogram]({{ "/Presentation/Figures/Images/density_plot/4.png" | relative_url }})

What happen if we want to make multiple densities?

For example, we want to make multiple densities plots for price based on the type of cut, all we need to do is adding `fill=cut` inside `aes()`.

```r?example=density
ggplot(data = diamonds, aes(x = price, fill = cut)) +
  geom_density(adjust = 1.5, alpha = .3)
```
![multiple]({{ "/Presentation/Figures/Images/density_plot/5.png" | relative_url }})
