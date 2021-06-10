---
title: Graph Themes
parent: Figures
grand_parent: Presentation
has_children: no
nav_order: 1
mathjax: no
---

## Introduction

Graph themes help enhance an already informative line, scatter, bar, or boxplot. With the implementation of useful themes, graphs become aesthetically pleasing; with improper implementation of themes, graphs become muddled and confusing.

## Keep in Mind

- When adding themes to a graph, ensure that the theme being used is appropriate for the data that is represented. For example, a scatterplot works best with graph themes that include gridlines while geometric data graphs look better without any lines.

- While there are a whole host of existing themes that can improve the appearance of graphs, modifying or creating your own themes can be the most effective way to visualize data. Though seemingly complicated, customizing your own graph theme is surprisingly easy and there is a helpful guide attached to the bottom of this page that walks through theme modification.

## Also Consider

- Not everyone can see the entire color spectrum. When using certain themes or arguments within themes, bear in mind that it can be hard to distinguish between similar colors or other color combinations for those with color-vision deficiency.

## Implementations

## R

In this R example, we will be using the **ggplot2** package and the *theme* function to add themes to graphs. The dataset we are using comes built into **ggplot2** and is known as `msleep`. The `msleep` dataset includes the sleep patterns of 83 different animals, as well as characteristics like the genus, brain weight, and whether the animal is a carnivore, herbivore, or other -vore.

```r
#Load in necessary packages (ggplot2)

library(ggplot2)
library(ggthemes)
library(hrbrthemes)

#Load in desired data (msleep)

data(msleep)
```

After viewing the data, we can create a scatterplot with the y-axis representing the total amount of hours the animal is asleep, the x axis representing the weight of the animal's brain, and the dots of the scatterplot colored by the -vore type of the animal.

```r

#basic scatterplot of sleep against brain weight

sleep_plot <- ggplot(data=msleep, aes(x = sleep_total, y = brainwt, color = vore)) +
  geom_point()

sleep_plot

```

Now that we have this basic plot, we can use the *theme* function to customize it. The **ggplot2** package comes with some built-in theme options which can be explored at the [Complete themes](https://ggplot2.tidyverse.org/reference/ggtheme.html) page of the **ggplot2** documentation provided by tidyverse.

Since we are using a scatterplot in this example, *theme_bw* is a simple and elegant way to display the data. Here is an example of what a *theme_bw* graph looks like:

```r

#Here is the animal sleep plot we made earlier with all the ggplot2 theme_bw() added to it

bw = sleep_plot + theme_bw()

bw

```

This is a nice, clean look, with gridlines, borders, and clearly defined axes. While *theme_bw* does an excellent job displaying the data, there are some themes that do not lend themselves easily to scatterplots. One such theme is *theme_void*, shown below:

```r
#Animal sleep plot with theme_void() from ggplot2

void = sleep_plot + theme_void()

void

```

This theme removes all gridlines, borders, and axes, leading to a very confusing image of floating colored points and a legend. When trying to display geometric data, this theme is useful, but for scatterplots it is less than ideal.

These are very basic themes to use, but can clean up a graph in a pinch. However, by downloading the **ggthemes** package, graphs can be taken up a notch. 

While most of the ***ggthemes** options are great, some really stand out. Three themes (*theme_economist*, *theme_fivethirtyeight*, and *theme_wsj*) all mimic the graph style of major media/news outlets. If you really want to sell your graph and look like mainstream media, here are some examples:

```r

#theme_economist mimics graphs from The Economist magazine

economist = sleep_plot + theme_economist()

economist

#theme_fivethirtyeight mimics graphs from FiveThirtyEight, a political/sports/statistics blogging site

fivethirtyeight = sleep_plot + theme_fivethirtyeight()

fivethirtyeight

#theme_wsj mimcs graphs from The Wall Street Journal newspaper

wsj = sleep_plot + theme_wsj()

wsj

```
The data we plotted is rather simple and plain; these themes would look better on a more refined graph, one with proper names, clear positioning, and distinguished data points or lines, but these graphs still look better than the original. 

To check out multiple examples of **ggthemes**, visit the [ggthemes](https://yutannihilation.github.io/allYourFigureAreBelongToUs/ggthemes/) page of the website ALL YOUR FIGURE ARE BELONG TO US.

For more helpful insight into **ggthemes** and its arguments, visit the [Introduction to ggthemes](https://mran.microsoft.com/snapshot/2016-12-03/web/packages/ggthemes/vignettes/ggthemes.html) site by Jeffrey B. Arnold.

Another great option for adding themes to **ggplot2** is **hrbrthemes**. Themes in **hrbrthemes** change the formatting up a bit, so don't be surprised if your axes titles move a bit. For this example, *theme_modern_rc* is used, as it makes the colored points of the graph pop off the screen. You can take your graph up another notch by adding one of the color options that **hrbrthemes** has to offer, in this case *scale_color_ft*:

```r

#hrbrthemes graph with scale_color_ft and theme_modern_rc 

hrbr = sleep_plot + scale_color_ft() + theme_modern_rc()

hrbr

```
There is much more that **hrbrthemes** has to offer beyond what is shown here; other scaling options, font choices, and utilities make **hrbrthemes** a more customizable theme package than **ggplot2** or **ggthemes**. For more theme options of **hrbrthemes**, check out this [hrbrthemes](https://hrbrmstr.github.io/hrbrthemes/) page.

If none of these existing themes are your cup of tea, maybe try to create your own theme or modify one of those listed above to suit your tastes. To do this, you will use the *theme* function and include an *element_xx* object. Element objects that can be used are listed below:

- element_line() - can add color, linetype, and size arguments
- element_text() - can add color, face, angle, and size arguments
- element_rect() - can add color, fill, and size arguments

Please take note that customizing themes in this way will not do everything. It will not allow you to change the placement of axis titles, line shapes, or other geometric properties. But it does allow you to make your graphs more aesthetically pleasing by changing font size or color, adding shapes around legends, and filling the backgrounds of graphs with colors and gridlines.

For ways to customize your own *theme* in **ggplot2**, check out the R Graphics Cookbook by Winston Chang. Chang offers an excellent section on modifying graph themes in [Chapter 9.4](https://r-graphics.org/recipe-appearance-theme-modify); at the bottom of the page is a helpful table that outlines each argument that can be used by *theme*, a description of what each does, and the *element_xx* to specify when using an argument. 

For a simple example of creating a theme, run the following code:

```r

#This code modifies the legend of the graph

legend = sleep_plot +
  theme(
    legend.background = element_rect(fill = "white", color = "dodgerblue", size = 1),
    legend.title = element_text(color = "brown", face = "bold", size = 18),
    legend.text = element_text(color = "brown", face = "bold", size = 10),
    legend.key = element_rect(color = "dodgerblue", size = 0.5)
  )
  
legend

#We use blue and brown here, as most color-blind people can distinguish these two colors

#element_rect changes the box around the legend and the boxes around the colors for -vore

#element_text changes the text color, size, and face within the legend

```

You can also modify an already existing theme using the same method as above. Here is what it looks like to modify the axis titles of the **hrbrthemes** graph we created earlier:

```r

modified = hrbr + theme(axis.title.x = element_text(colour = "yellow", size = 12, face = "bold"), 
  axis.title.y = element_text(colour = "yellow", size = 12, face = "bold"))
  
modified

```

This is just scratching the surface of graph themes in R. Even more theme packages exist, like **ggpubr** and **wesanderson**; these won't be explored on this page, but if you're interested check out this [ggpubr](https://rpkgs.datanovia.com/ggpubr/index.html) page and this [wesanderson](https://rforpoliticalscience.com/2020/07/26/make-wes-anderson-themed-graphs-with-wesanderson-package-in-r/) page.