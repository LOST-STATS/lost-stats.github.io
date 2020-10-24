---
title: Faceted Graphs
parent: Figures
grand_parent: Presentation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: false
---

# Faceted Graphs

When plotting relationship among variables of interest, one of the useful ways to create visual impact is by way of using facet, which subsets data with faceted variable and creates plots for each of the subset seperately. The result is a panel of subplots, with each subplot depicting the plot for same set of variables. This approach can be especially useful for panel datasets, with the panel variable acting as facet variable and each subplot depicting time series trend of variable of interest.

## Keep in Mind

- It is important to use a categorical (discrete) variable as a facet variable for creating faceted graphs. 
- Plotting libraries generally fall into two broad camps: *imperative* (specify all of the steps to get the desired outcome) or *declarative* (specify the desired outcome without the steps). Imperative plotting gives more control and some people may find each step clearer to read, but it can also be fiddly and cumbersome, especially with simple plots. Declarative plotting trades away control in favour of tried and tested processes that can quickly produce standardised charts, but the specialised syntax can be a barrier for newcomers. Facets are available in both types, but the code to produce them will look quite different.


## Also Consider

- It is important to know the basic plotting techniques such as [Bar Graphs]({{ "/Presentation/Figures/bar_graphs.html" | relative_url }}), [Line Graphs]({{ "/Presentation/Figures/line_graph_with_labels_at_the_beginning_or_end.html" | relative_url }}) and [Scatterplot]({{ "/Presentation/Figures/Figures/scatterplot_by_group_on_shared_axes.html" | relative_url }}) before learning about faceted graphs as the facets are an addition to the underlying plot such as bar graph, line graph, scatterplot etc.


# Implementations

## Python

Python has both imperative and declarative plotting libraries, and many of them have support for faceted graphs. In the example below, we'll look at three libraries: two declarative, [**seaborn**](https://seaborn.pydata.org/index.html) and [**plotnine**](https://plotnine.readthedocs.io/en/stable/index.html), and one imperative, [**matplotlib**](https://matplotlib.org/). The imperative library **matplotlib** is by far the most popular plotting tool in Python, having been used as part of efforts to detect [gravitational waves](https://www.gw-openscience.org/s/events/GW150914/GW150914_tutorial.html) and produce the [first image of a black hole](https://numpy.org/case-studies/blackhole-image/). Often, other libraries build upon it as a foundation. For plots that will be shown on the web, the declarative library [**altair**](https://altair-viz.github.io/) has very good facet support.

Because **matplotlib** is imperative, it takes more effort by the user to produce a simple facet chart. So the first example below will use **seaborn**, a declarative library that builds on **matplotlib**. We'll use it to produce a plot from the Penguins dataset, with a facet for each island. As ever, you may need to conda or pip install the libraries used in the examples.

```python
import seaborn as sns

# Load the example Penguins dataset
df = sns.load_dataset("penguins")

# Plot a scatter of bill properties with
# columns (facets) given by island and colour
# given by the species of Penguin
sns.relplot(x="bill_depth_mm", y="bill_length_mm",
            hue="species", col="island",
            alpha=.5, palette="muted", data=df)
```

Results in:

![Faceted graph_seaborn](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Faceted_Graphs/seaborn_facet_example.png)

If you have used R for plotting, you might be familiar with the **ggplot** package. **plotnine** is another declarative plotting library in Python that is inspired by the API for **ggplot** in R.

```python
from plotnine import *
from plotnine.data import mtcars

(ggplot(mtcars, aes('wt', 'mpg', color='factor(gear)'))
 + geom_point()
 + stat_smooth(method='lm')
 + facet_wrap('~gear'))
```

Results in:

![Faceted graph_plotnine](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Faceted_Graphs/plotnine_facet_example.png)

For more complex charts, where you want full control over facet placement, the imperative library **matplotlib** has a wealth of options. The code for a simple facet plot using synthetic data is:

```python
import matplotlib.pyplot as plt
import numpy as np

# Some example data to display
x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x ** 2)

fig, (ax1, ax2) = plt.subplots(2, sharex=True)
fig.suptitle('Two sine waves')
ax1.plot(x, y)
ax2.scatter(x + 1, -y, color='red')
```

(NB: no figure shown in this case.) Note how everything is specified. While `plt.subplots(nrows, ncols, ...)` allows for a rectangular facet grid, even more complex facets can be constructed using the [mosaic option](https://matplotlib.org/3.3.0/tutorials/provisional/mosaic.html) in **matplotlib** version 3.3.0+. The arrangment of facets can be specified either through text, as in the example below, or with lists of lists:

```python

import matplotlib.pyplot as plt

axd = plt.figure(constrained_layout=True).subplot_mosaic(
    """
    TTE
    L.E
    """)
for k, ax in axd.items():
    ax.text(0.5, 0.5, k,
            ha='center', va='center', fontsize=36,
            color='darkgrey')
```

Results in:

![Faceted graph_advanced](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Faceted_Graphs/matplotlib_advanced_facet.png)



## R

Implementation of faceted graph in R explained below is taken from online book [R for Data Science](https://r4ds.had.co.nz/data-visualisation.html#facets) by Hadley Wickham and Garett Grolemund. The book is also an excellent source for various data visualization techniques in R and learning R in general.

We will use **tidyverse** package available in R for faceted graphs. **Tidyverse** is actually a meta-package which has various packages, and we will use **ggplot2** package for our purpose. This package has a data frame (it is like a table in R), called 'mpg' which contains observations collected by the US Environmental Protection Agency on 38 models of car.

To create faceted graph, use `facet_wrap()` option in ggplot. The argument inside the bracket is `~` sign follwed by the categorical variable to be used to create subsets of data. Its use is illustrated in the code given below.

```R
#Install package, if not already installed.
install.packages("tidyverse")

#Load the package
library(tidyverse)

# Now, we will create faceted graph, with variable 'displ' (a car's engine size) on  # x-axis and variable 'hwy (car's fuel efficiency on highway) on y-axis. We will use # `facet_wrap(~class)` option to created faceted graph. The variable 'class' denotes # type of car. We use 'geom_point()` to create a scatterplot.

ggplot(data = mpg)+
geom_point(mapping = aes(x = displ, y = hwy))+
facet_wrap(~class)
```
The above set of code results in the following panel of subplots:
![Faceted graph](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Faceted_Graphs/faceted_graph_class.png).

Additionally, one can create faceted graph using two variables with `facet_grid()`. Inside the bracket, use two variables seperated by `~`. The example of the same using 'mpg' dataframe and two variables 'drv' (whether it's front wheel, rear wheel or 4wd) and 'cyl' (number of cylinders) is given below.

```R
ggplot(data = mpg)+
geom_point(mapping = aes(x = displ, y = hwy))+
facet_grid(drv ~ cyl)
```
The code reults in the follwing panel of subplots:
![Faceted graph with two variables](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Faceted_Graphs/faceted_graph_two_variables.png)


## Stata

In stata, faceted graph can be created by using option `by()` and mentioning the faceted variable in the bracket. Let's see an example of the same . Let's access pre-installed dataset in Stata, called 'auto.dta' which has 1978 automobile data. The following code generates scatterplot with 'length of car' on x-axis, 'mileage of car' on y-axis and variable 'foreign' (whether the car is manufactured domestically or imported) used to create subsets of data. `sysuse auto` is used to load the table 'auto.dta'.

```
sysuse auto
twoway (scatter mpg length), by(foreign)
```

The code generates the following graph:
![Faceted Graph by Origin of Car](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Faceted_Graphs/stata_faceted_graph.png)
