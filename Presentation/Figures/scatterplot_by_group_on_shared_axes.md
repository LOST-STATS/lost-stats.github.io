---
title: Scatterplot by Group on Shared Axes
parent: Figures
grand_parent: Presentation ## Optional for indexing
has_children: false
mathjax: true
nav_order: 1
---

# Scatterplot by Group on Shared Axes

[Scatterplot]({{ "/Presentation/Figures/scatterplot.html" | relative_url }})s are a standard data visualization tool that allows you to look at the relationship between two variables $$X$$ and $$Y$$. If you want to see how the relationship between $$X$$ and $$Y$$ might be different for Group A as opposed to Group B, then you might want to plot the scatterplot for both groups on the same set of axes, so you can compare them.

## Keep in Mind

- Scatterplots may not work well if the data is discrete, or if there are a large number of data points. 

## Also Consider

- Sometimes, instead of putting both Group A and Group B on the same set of axes, it makes more sense to plot them separately, and put the plots next to each other. See [Faceted Graphs]({{ "/Presentation/Figures/faceted_graphs.html" | relative_url }}).
- There are many ways to make the scatterplots of the two groups distinct. See [Styling Scatterplots]({{ "/Presentation/Figures/styling_scatterplots.html" | relative_url }}).

# Implementations

## R

```r
library(ggplot2)

# Load auto data
data(mtcars)

# Make sure that our grouping variable is a factor
# and labeled properly
mtcars$Transmission <- factor(mtcars$am, 
                              labels = c("Automatic", "Manual"))

# Put wt on the x-axis, mpg on the y-axis, 
ggplot(mtcars, aes(x = wt, y = mpg, 
                   # distinguish the Transmission values by color,
                   color = Transmission)) + 
  # make it a scatterplot with geom_point()
  geom_point()+
  # And label properly
  labs(x = "Car Weight", y = "MPG")
```
This results in:

![Scatterplot of car weight against MPG, differentiated by transmission type, in R](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Scatterplot-by-Groups-on-Shared-Axes/r_scatterplot_by_transmission.png)

## Stata

```stata
* Load auto data
sysuse auto.dta

* Start a twoway command
* Then, for each group, put its scatter command in ()
* Using if to plot each group separately
* And specifying mcolor or msymbol (etc.) to differentiate them
twoway (scatter weight mpg if foreign == 0, mcolor(black)) (scatter weight mpg if foreign == 1, mcolor(blue))

* Add a legend option so you know what the colors mean
twoway (scatter weight mpg if foreign == 0, mcolor(black)) (scatter weight mpg if foreign == 1, mcolor(blue)), legend(lab(1 Domestic) lab(2 Foreign)) xtitle("Weight") ytitle("MPG")
```
This results in:

![Scatterplot of car weight against MPG, differentiated by foreign, in Stata](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Scatterplot-by-Groups-on-Shared-Axes/stata_scatterplot_by_group.png)
