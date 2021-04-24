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

## Python

In this example, we'll use [**seaborn**](https://seaborn.pydata.org/index.html), a *declarative* plotting library that provides a quick and easy way to produce density plots. It builds on [**matplotlib**](https://matplotlib.org/).

```python
# You may need to install seaborn on the command line using 'pip install seaborn' or 'conda install seaborn'
import seaborn as sns

# Set a theme for seaborn
sns.set_theme(style="darkgrid")

# Load the example diamonds dataset
diamonds = sns.load_dataset("diamonds")

# Take a look at the data
print(diamonds.head())
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>carat</th>
      <th>cut</th>
      <th>color</th>
      <th>clarity</th>
      <th>depth</th>
      <th>table</th>
      <th>price</th>
      <th>x</th>
      <th>y</th>
      <th>z</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.23</td>
      <td>Ideal</td>
      <td>E</td>
      <td>SI2</td>
      <td>61.5</td>
      <td>55.0</td>
      <td>326</td>
      <td>3.95</td>
      <td>3.98</td>
      <td>2.43</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.21</td>
      <td>Premium</td>
      <td>E</td>
      <td>SI1</td>
      <td>59.8</td>
      <td>61.0</td>
      <td>326</td>
      <td>3.89</td>
      <td>3.84</td>
      <td>2.31</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.23</td>
      <td>Good</td>
      <td>E</td>
      <td>VS1</td>
      <td>56.9</td>
      <td>65.0</td>
      <td>327</td>
      <td>4.05</td>
      <td>4.07</td>
      <td>2.31</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.29</td>
      <td>Premium</td>
      <td>I</td>
      <td>VS2</td>
      <td>62.4</td>
      <td>58.0</td>
      <td>334</td>
      <td>4.20</td>
      <td>4.23</td>
      <td>2.63</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.31</td>
      <td>Good</td>
      <td>J</td>
      <td>SI2</td>
      <td>63.3</td>
      <td>58.0</td>
      <td>335</td>
      <td>4.34</td>
      <td>4.35</td>
      <td>2.75</td>
    </tr>
  </tbody>
</table>
</div>

```python
sns.kdeplot(data=diamonds, x="price", cut=0);
```

![png](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/density_plot/py_density_plot_1.png)

This is basic, but there are lots of ways to adjust it through keyword arguments (you can see these by running `help(sns.kdeplot)`) or via calling functions on the **matplotlib** `ax` object that running `sns.kdeplot` returns when not followed by `;`. In this simple example, the `cut` keyword argument forces the density estimate to end at the end-points of the data--which makes sense for a variable like price, which has a hard cut-off at 0.

Let's use further keyword arguments to enrich the plot, including different colours ('hues') for each cut of diamond. One keyword argument that may not be obvious is `hue_order`. The default function call would have arranged the `cut` types so that the 'Fair' cut obscured the other types, so the argument passed to the `hue_order` keyword below *reverses* the order of the unique list of diamond cuts via `[::-1]`.

```python
sns.kdeplot(data=diamonds,
            x="price",
            hue="cut",
            hue_order=diamonds['cut'].unique()[::-1],
            fill=True,
            alpha=.4,
            linewidth=0.5,
            cut=0.);
```

![png](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/density_plot/py_density_plot_2.png)


## R

For this R demonstration, we are going to use **ggplot2** package to create a density plot. Additionally, we will use the dataset `diamonds` that is natively available in R. 

To begin with this R demonstration, make sure that we install and load all the useful packages that we need it. We use the function `p_load()` in `pacman` package to help us to install and load the packages at one time. 

```{r}
#install and load necessary packages
if (!require("pacman")) install.packages("pacman")
pacman::p_load(ggplot2,viridis,RColorBrewer,tidyverse,ggthemes,ggpubr,datasets)
```

Next, in order to make a density plot, we are going to use the `ggplot()` and `geom_density()` functions. We will specify `price` as our x-axis. 

```{r,warning=FALSE}

ggplot(diamonds, aes(x=price))+
  geom_density()
```
![Basic density plot](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/density_plot/1.png)

We can always change the color of the density plot using the `col` argument and fill the color inside the density plot using `fill` argument. Furthermore, we can specify the degree of transparency density fill area using the argument `alpha` where `alpha` ranges from 0 to 1. 

```{r,warning=FALSE}
ggplot(diamonds, aes(x=price))+
  geom_density(fill="lightblue",
               col='black',
               alpha=0.6)
```

![Colored density plot](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/density_plot/2.png)
We can also change the type of line of the density plot as well by adding `linetype=` inside `geom_density()`.

```{r}
ggplot(diamonds, aes(x=price))+
  geom_density(fill="lightblue",
               col='black',
               linetype="dashed")
```

![Density plot with linetype](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/density_plot/3.png)
Furthermore, you can also combine both histogram and density plots together.

```{r,warning=FALSE,message=FALSE}
ggplot(diamonds, aes(x=price)) + 
 geom_histogram(aes(y=..density..), colour="black", fill="grey45")+
 geom_density(col="red",size=1,linetype='dashed') 
```
![Density Plot Overlaid on Histogram](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/density_plot/4.png)

What happen if we want to make multiple densities? 

For example, we want to make multiple densities plots for price based on the type of cut, all we need to do is adding `fill=cut` inside `aes()`.

```{r}
ggplot(data=diamonds, aes(x=price,fill=cut)) +
    geom_density(adjust=1.5, 
                 alpha=.3)
```
![multiple](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/density_plot/5.png)
:

## Stata 

For this demonstration, we will use the plottig scheme, a community-contributed color scheme for plots that greatly improves over Stata's default plot color schemes. For more on using schemes in Stata, see [here](https://blog.stata.com/2018/10/02/scheming-your-way-to-your-favorite-graph-style/).

```stata
clear all 
set more off 

ssc install blindschemes // Install the blindschemes set of color schemes, which includes plottig 
graph query, schemes // Show the available schemes you have installed, to confirm plottig was installed

*Pull in Stata's NHANES dataset 
use http://www.stata-press.com/data/r16/nhanes2.dta, clear

*Plot the kernel density 
kdensity height, scheme(plottig) 


