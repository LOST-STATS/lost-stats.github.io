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


## Also Consider

- It is important to know the basic plotting techniques such as [Bar Graphs](https://lost-stats.github.io/Presentation/bar_graphs.html), [Line Graphs](https://lost-stats.github.io/Presentation/line_graph_with_labels_at_the_beginning_or_end.html) and [Scatterplot](https://lost-stats.github.io/Presentation/scatterplot_by_group_on_shared_axes.html) before learning about faceted graphs as the facets are an addition to the underlying plot such as bar graph, line graph, scatterplot etc.


# Implementations

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
![Faceted graph](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Images/Faceted_Graphs/faceted_graph_class.png).

Additionally, one can create faceted graph using two variables with `facet_grid()`. Inside the bracket, use two variables seperated by `~`. The example of the same using 'mpg' dataframe and two variables 'drv' (whether it's front wheel, rear wheel or 4wd) and 'cyl' (number of cylinders) is given below.

```R
ggplot(data = mpg)+
geom_point(mapping = aes(x = displ, y = hwy))+
facet_grid(drv ~ cyl)
```
The code reults in the follwing panel of subplots:
![Faceted graph with two variables](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Images/Faceted_Graphs/faceted_graph_two_variables.png)


## Stata

In stata, faceted graph can be created by using option `by()` and mentioning the faceted variable in the bracket. Let's see an example of the same . Let's access pre-installed dataset in Stata, called 'auto.dta' which has 1978 automobile data. The following code generates scatterplot with 'length of car' on x-axis, 'mileage of car' on y-axis and variable 'foreign' (whether the car is manufactured domestically or imported) used to create subsets of data. `sysuse auto` is used to load the table 'auto.dta'.

```
sysuse auto
twoway (scatter mpg length), by(foreign)
```

The code generates the following graph:
![Faceted Graph by Origin of Car](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Images/Faceted_Graphs/stata_faceted_graph.png)