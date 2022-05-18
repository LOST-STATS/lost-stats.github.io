---
title: "Color Palettes"
parent: Figures
grand_parent: Presentation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Color Palettes

Color palettes are a simple way to customize graphs and improve data visualization through increased color ranges and options. There are a multitude of packages that add color palette options for all types of data, including continuous and discrete color palettes.

## Keep in Mind

-   Not all color palettes can be used in every situation. Some are better suited for continuous data and others for discrete data.
-   There are different functions for scale colors and fill colors, pick the right function for your specific case.
-   Check the help file or manual for any color palette package for information on arguments and color options available.

## Also Consider

-   Remember, not all color palette packages can be used in every scenario. Some are better suited for discrete variables while others are better for continuous variables.
-   There are other ways to customize your graphs, such as adding [themes]({{ "/Presentation/Figures/graph_themes.html" \| relative_url}}), which conforms your graph to a pre-determined aesthetic based on the function used.

# Implementations

## R

First, let's load in some data that we can use to demonstrate color palette options. For these examples, I will use the palmer penguins data from the `palmerpenguins` package.

```r
# load in palmer penguins package
library(palmerpenguins)

# assign penguins data to an object
data = penguins
```

### Discrete Data

The first two examples will deal with discrete color palettes for modeling discrete data. Let's first demonstrate a color palette option that comes with the `ggplot2` package, which will be used throughout this post to construct graphs. Let's see what `ggplot2` offers in terms of color customization by graphing penguin bill length and bill depth coloring by species.

```r
# load ggplot2
library(ggplot2)

# graph bill length vs depth coloring by species
ggplot(data = penguins, aes(x=bill_length_mm, y=bill_depth_mm, color=species)) + geom_point()
```

![Graph of bill depth vs. length with default color for species](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/r_palettes_1.png)

`ggplot2` provides default color options for quick graph making. However, we can change the colors for the species by using the `scale_color_brewer()` function from the `ggplot2` package

```r
# recreate previous graph, now using the scale_color_brewer() to change color palette

ggplot(data = penguins, aes(x=bill_length_mm, y=bill_depth_mm, color=species)) + geom_point() +
  scale_color_brewer(palette = "RdYlGn")
  ```

![Graph of bill depth vs. length with new color palette for species](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/r_palettes_2.png)

By using the `scale_color_brewer()` function (which again comes loaded with ggplot), we are able to change the color palette used to color the data points. This is particularly helpful when we need to color many different groups, as we can specify a palette with lots of colors available to assign to each group. There are many different palette options we can specify, check out the [ggplot2](https://ggplot2.tidyverse.org/reference/scale_brewer.html#ref-usage) website for more available options.

In addition to changing the color of data points, we can use color palettes to change the fill color of a graph object, which is particularly useful when creating bar charts, line graphs, boxPlots, or filling in confidence intervals. Let's create a new example where we make a bar chart of the number of penguins from each species in the data set:

```r
# create bar chart of number of penguins from each species, coloring the fill of the bars by species

ggplot(data = penguins, aes(x=species)) + geom_bar(aes(fill = species)) 
```

![Graph of number of penguins from each species using default fill colors](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/r_palettes_3.png)

Again, `ggplot2` uses default colors to fill in the bars. However, we can change these colors using a color palette package. Let's try the `ggsci` package this time, which comes with many different fill options inspired by those used in science journals and popular tv shows. For the example below, we'll use the `scale_fill_simpsons()` function to change the bar colors to a set inspired by the long-running comedy show.

```r
# load in ggsci package

library(ggsci)

# add the scale_fill_simpsons() function to change bar colors

ggplot(data = penguins, aes(x=species)) + geom_bar(aes(fill = species)) + 
  scale_fill_simpsons()
 ```

![Graph of number of penguins from each species using specified color palette for bar fill](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/r_palettes_4.png)

Now the bars are a different set of colors from the default set! If you want to learn more about all the options available from the `ggsci` package, visit its [cran page.](https://cran.r-project.org/web/packages/ggsci/vignettes/ggsci.html)

### Continuous Data

The previous examples use a discrete variable to color the data by. We can also apply color palettes to continuous variables for a color gradient scale. Let's return to the first example, but change the variable we are coloring by from "species" to `body_mass_g` and see what we get.

```r
# Recreate first example, but switch color to body_mass_g variable

ggplot(data = penguins, aes(x=bill_length_mm, y=bill_depth_mm, color=body_mass_g)) + geom_point()
```

![Graph of bill depth vs. length using default color gradient for body mass](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/r_palettes_5.png)

Now, instead of having a set number of colors modeling our data, we see a gradient scale in the legend on the left-hand side of the chart. `ggplot2` defaults to a blue color gradient, with lighter shades of blue representing heavier penguins. It is a bit difficult to discern the different shades, however, making this graph hard to read. We can edit this using the `viridis` package, which offers a greater variation of shades in its color gradient.

```r
# load in viridis package

library(viridis)

# copy plot code from previous chunk, but add scale_color_viridis() function

ggplot(data = penguins, aes(x=bill_length_mm, y=bill_depth_mm, color=body_mass_g)) + geom_point() + 
  scale_color_viridis() 
 ```

![Graph of bill depth vs. length using specified color palette for updated gradient for body mass](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/r_palettes_6.png)

Now we have a better idea about how penguin body mass relates to bill length and depth. The `scale_color_viridis()` function is well known for having a wide range of color shades as well as being visible to color blind people.

These simple examples are certainly not the end-all be-all, but they should hopefully demonstrate that there are lots of customization options available for your graphs. Ultimately, it comes down to personal preference and what type of data you are modeling. Make sure to keep in mind too how you should call attention to specific parts of your charts to best convey the information within the data. With that being said, the options are seemingly endless when it comes to color palettes in R, so play around with your favorite color palette packages to find the best option for you!
