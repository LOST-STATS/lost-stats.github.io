---
title: Graph Themes
parent: Figures
grand_parent: Presentation
has_children: no
nav_order: 1
mathjax: no
---

## Introduction

Graph themes help enhance an already informative line, scatter, bar, or boxplots. With the implementation of beautiful data visualization, graphs become aesthetically pleasing; with improper implementation of data visualization, graphs become muddled and confusing

## Keep in Mind

- When adding themes to a graph, ensure that the theme being used is appropriate for the data that is represented. For example, a scatterplot works best with graph themes that include gridlines while geometric data graphs look better without any lines.

- While there are a whole host of existing themes that can improve the appearance of graphs, modifying or creating your own themes can be the most effective way to visualize data. Though seemingly complicated, customizing your own graph theme is surprisingly easy and there is a helpful guide attached to the bottom of this page that walks through theme modification.

## Also Consider

- Not everyone can see the entire color spectrum. When using certain themes or arguments within themes, bear in mind that it can be hard to distinguish between similar colors or other color combinations for those with color-vision deficiency.

## Implementations

## R

In this R example, we will be using the **ggplot2** package and the *theme()* function to add themes to graphs. The dataset we are using comes built into **ggplot2** and is known as `msleep`. The `msleep` dataset includes the sleep patterns of 83 different animals, as well as characteristics like the genus, brain weight, and whether the animal is a carnivore, herbivore, or other -vore.

```r
#Load in necessary packages (ggplot2)

library(ggplot2)
library(ggthemes)

#Load in desired data (msleep)

data(msleep)
```

After viewing the data, we can create a scatterplot with the y-axis representing the total amount of hours the animal is asleep, the x axis representing the weight of the animal's brain, and the dots of the scatterplot colored by the -vore type of the animal.

```r

sleep_plot <- ggplot(data=msleep, aes(x = sleep_total, y = brainwt, color = vore)) +
  geom_point()

sleep_plot

```

Now that we have this basic plot, we can use the *theme()* function to customize it. The **ggplot2** package comes with some built-in theme options which are listed below:

- theme_bw() 
- theme_classic() 
- theme_dark() 
- theme_gray()
- theme_grey() 
- theme_light()
- theme_linedraw() 
- theme_minimal() 
- theme_test()
- theme_void() 

To see examples of these, visit the [Complete themes](https://ggplot2.tidyverse.org/reference/ggtheme.html) page of the **ggplot2** documentation provided by tidyverse or run the code below:

```r

#Here is the animal sleep plot we made earlier with all the ggplot2 themes added to it

bw = sleep_plot + theme_bw()

classic = sleep_plot + theme_classic()

dark = sleep_plot + theme_dark()

gray = sleep_plot + theme_gray()

light = sleep_plot + theme_light()

line = sleep_plot + theme_linedraw()

minimal = sleep_plot + theme_minimal()

test = sleep_plot + theme_test()

void = sleep_plot + theme_void()

```

These are very basic themes to use, but can clean up a graph in a pinch. However, by downloading the **ggthemes** package, graphs can be taken up a notch. Here is a list of these themes:

- theme_base() 
- theme_calc() 
- theme_clean()
- theme_economist() & theme_economist_white()
- theme_excel() & theme_excel_new() 
- theme_few() 
- theme_fivethirtyeight()
- theme_gdocs()
- theme_hc() 
- theme_igray() 
- theme_par()
- theme_pander()
- theme_solarized() & theme_solarized_2()
- theme_solid() 
- theme_stata() 
- theme_tufte()
- theme_wsj()

To check out multiple examples of each of themes as well as others, visit the [ggthemes](https://yutannihilation.github.io/allYourFigureAreBelongToUs/ggthemes/) page of the website ALL YOUR FIGURE ARE BELONG TO US.

For more helpful insight into **ggthemes** and its arguments, visit the [Introduction to ggthemes](https://mran.microsoft.com/snapshot/2016-12-03/web/packages/ggthemes/vignettes/ggthemes.html) site by Jeffrey B. Arnold.

For a simple example of each of these themes, run the code below:

```r

#Here is the animal sleep plot we made earlier with all the ggthemes added to it

base = sleep_plot + theme_base()

calc = sleep_plot + theme_calc()

clean = sleep_plot + theme_clean()

economist = sleep_plot + theme_economist()

excel_new = sleep_plot + theme_excel_new()

few = sleep_plot + theme_few()

fivethirtyeight = sleep_plot + theme_fivethirtyeight()

gdocs = sleep_plot + theme_gdocs()

hc = sleep_plot + theme_hc()

igray = sleep_plot + theme_igray()

par = sleep_plot + theme_par()

pander = sleep_plot + theme_pander()

solarized = sleep_plot + theme_solarized()

solarized_2 = sleep_plot + theme_solarized_2()

solid = sleep_plot + theme_solid()

stata = sleep_plot + theme_stata()

tufte = sleep_plot + theme_tufte()

wsj = sleep_plot + theme_wsj()
```

If none of these existing themes are your cup of tea, maybe try to create your own theme. Customizing your own theme allows you to change axis labels, legend text and shape, and even background color. To do this, you will use the *theme()* function and include an *element_xx()* object. Element objects that can be used are listed below:

- element_line() - can add color, linetype, and size arguments
- element_text() - can add color, face, angle, and size arguments
- element_rect() - can add color, fill, and size arguments

For ways to customize your own *theme()* in ggplot2, check out the R Graphics Cookbook by Winston Chang. Chang offers an excellent section on modifying graph themes in [Chapter 9.4](https://r-graphics.org/recipe-appearance-theme-modify); at the bottom of the page is a helpful table that outlines each argument that can be used by *theme()*, a description of what each does, and the *element_xx()* to specify when using an argument. 

For a simple example of modifying a theme, run the following code:

```r

#This code modifies the legend of the graph

modified = sleep_plot +
  theme(
    legend.background = element_rect(fill = "white", color = "dodgerblue", size = 1),
    legend.title = element_text(color = "brown", face = "bold", size = 18),
    legend.text = element_text(color = "brown", face = "bold", size = 10),
    legend.key = element_rect(color = "dodgerblue", size = 0.5)
  )

#We use blue and brown here, as most color-blind people can distinguish these two colors

#element_rect changes the box around the legend and the boxes around the colors for -vore

#element_text changes the text color, size, and face within the legend

```