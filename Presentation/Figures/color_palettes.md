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
-   There are other ways to customize your graphs, such as adding [themes]({{ "/Presentation/Figures/graph_themes.html" | relative_url}}), which conforms your graph to a pre-determined aesthetic based on the function used.

# Implementations

## R

There are a huge array of color palette options and user-defined themes available in R. In the examples that follow, we'll limit ourselves to demonstrating with **ggplot2** ([link](https://ggplot2.tidyverse.org/)), although the same principles apply to base R plots, and only one or two additional palette themes.

First, let's load in some data that we can use to demonstrate color palette options. For these examples, we will use the palmer penguins data from the **palmerpenguins** package.

```r
# load in palmerpenguins package
library(palmerpenguins)

# Load the penguins data into memory
data("penguins")
```

### Discrete Data

The first two examples will deal with discrete color palettes for modeling discrete data. Let's first demonstrate a color palette option that comes with the `ggplot2` package, which will be used throughout this post to construct graphs. Let's see what **ggplot2** offers in terms of color customization by graphing penguin bill length and bill depth coloring by species.

```r
# load ggplot2
library(ggplot2)

# graph bill length vs depth coloring by species
ggplot(data = penguins, aes(x=bill_length_mm, y=bill_depth_mm, color=species)) +
   geom_point()
```

![Graph of bill depth vs. length with default color for species](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/r_palettes_1.png)

**ggplot2** provides default color options for quick graph making. However, we can change the colors for the species by using the `scale_color_brewer()` function from the `ggplot2` package

```r
# recreate previous graph, now using the scale_color_brewer() to change color palette

last_plot() +
  scale_color_brewer(palette = "RdYlGn")
```

![Graph of bill depth vs. length with new color palette for species](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/r_palettes_2.png)

By using the `scale_color_brewer()` function (which again comes bundled with **ggplot2**), we are able to change the color palette used to color the data points. This is particularly helpful when we need to color many different groups, as we can specify a palette with lots of colors available to assign to each group. There are many different palette options we can specify, check out the [**ggplot2**](https://ggplot2.tidyverse.org/reference/scale_brewer.html#ref-usage) website for more available options.

In addition to changing the color of data points, we can use color palettes to change the fill color of a graph object, which is particularly useful when creating bar charts, line graphs, boxPlots, or filling in confidence intervals. Let's create a new example where we make a bar chart of the number of penguins from each species in the data set:

```r
# create bar chart of number of penguins from each species, coloring the fill of the bars by species

ggplot(data = penguins, aes(x=species)) +
   geom_bar(aes(fill = species))
```

![Graph of number of penguins from each species using default fill colors](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/r_palettes_3.png)

Again, **ggplot2** uses default colors to fill in the bars. However, we can change these colors using a dedicated color palette package. Let's try the **ggsci** package ([link](https://nanx.me/ggsci/)) this time, which comes with many different fill options inspired by those used in science journals and popular tv shows. For the example below, we'll use the `scale_fill_simpsons()` function to change the bar colors to a set inspired by the long-running comedy show.

```r
# load in ggsci package

library(ggsci)

# add the scale_fill_simpsons() function to change bar colors

last_plot() +
  scale_fill_simpsons()
 ```

![Graph of number of penguins from each species using specified color palette for bar fill](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/r_palettes_4.png)

Now the bars are a different set of colors from the default set! If you want to learn more about all the options available from the `ggsci` package, visit its [cran page.](https://cran.r-project.org/web/packages/ggsci/vignettes/ggsci.html)

### Continuous Data

The previous examples use a discrete variable to color the data by. We can also apply color palettes to continuous variables for a color gradient scale. Let's return to the first example, but change the variable we are coloring by from "species" to `body_mass_g` and see what we get.

```r
# Recreate first example, but switch color to body_mass_g variable

ggplot(data = penguins, aes(x=bill_length_mm, y=bill_depth_mm, color=body_mass_g)) +
   geom_point()
```

![Graph of bill depth vs. length using default color gradient for body mass](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/r_palettes_5.png)

Now, instead of having a set number of colors modeling our data, we see a gradient scale in the legend on the left-hand side of the chart. **ggplot2** defaults to a blue color gradient, with lighter shades of blue representing heavier penguins. It is a bit difficult to discern the different shades, however, making this graph hard to read. A popular alterative these days is the `viridis` palette, which **ggplot2** includes as an option..

```r
# recall previous plot, but this time using scale_color_viridis_c()
# note that the "_c" suffix indicates "continuous" data

last_plot() +
  scale_color_viridis_c()
 ```

![Graph of bill depth vs. length using specified color palette for updated gradient for body mass](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/r_palettes_6.png)

Now we have a better idea about how penguin body mass relates to bill length and depth. The `scale_color_viridis_C()` function is well known for having a wide range of color shades as well as being visible to color blind people.

These simple examples are certainly not the end-all be-all, but they should hopefully demonstrate that there are lots of customization options available for your graphs. Ultimately, it comes down to personal preference and what type of data you are modeling. Make sure to keep in mind too how you should call attention to specific parts of your charts to best convey the information within the data. With that being said, the options are seemingly endless when it comes to color palettes in R, so play around with your favorite color palette packages to find the best option for you!

Some other fun, pre-defined color palette packages in R include:

- **colorspace** ([link](https://colorspace.r-forge.r-project.org/index.html))
- **wesanderson** ([link](https://github.com/karthik/wesanderson))

## Stata

Stata has more limited native options to use colors and color palettes to graphs. However, thanks to Ben Jann package **colrspace** and **palettes**, it is relatively easy to extract and translate color palettes to be used in Stata. In addition, it is also possible to combine this packages with **grstyle** (also by Ben Jann), to modify the colors of the scheme in memory, to easily change the colors of most of your graphs.

To facilitate further the use of colors in your graphs, I put together a wrapper that will combine the use of Ben Jann's packages, to easily combine palettes and schemes, for most of your color needs.

### Setup

First, we need to install a few packages from ssc.

```stata
* To modify schemes
ssc install grstyle
* To add color palettes and palettes translators in Stata
net install palettes , replace from("https://raw.githubusercontent.com/benjann/palettes/master/")
net install colrspace, replace from("https://raw.githubusercontent.com/benjann/colrspace/master/")
* A wrapper for the commands above, plus adding other predefined palettes
ssc install color_style
```

Second, lets load some data that we can use to demonstrate color palette options. For these examples, I will use iris.dta dataset. This has similar characteristics as the penguins dataset used in the R example above. The examples that follow will try to replicate the figures described in R. I will also use the scheme `white`, which is clear than the Stata default scheme.

```stata
webuse iris, clear
```

### Discrete Data

The first two examples will deal color palettes for discrete data, emphasizing on the use of color_style. We start by creating a simple scatter of sepal length and with by iris type, using default color options in Stata.
Note that there is a new comand (mscatter in ssc) that can create scatterplots by groups more directly. However, I will stay with the simpler scatter for this example.

```stata
two (scatter seplen sepwid if iris==1) ///
    (scatter seplen sepwid if iris==2) ///
    (scatter seplen sepwid if iris==3), ///
    legend(order(1 "Sectosa" 2 "Versicolor" 3 "Virginica"))
```

![Sepal Length vs Sepal Width](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/stata_palettes_1.png)

This, however, generates dots with colors that are hard to differentiate. We could, instead use "tableau" colors:

```stata
color_style tableau
two (scatter seplen sepwid if iris==1) ///
    (scatter seplen sepwid if iris==2) ///
    (scatter seplen sepwid if iris==3), ///
    legend(order(1 "Sectosa" 2 "Versicolor" 3 "Virginica"))
```
![Sepal Length vs Sepal Width](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/stata_palettes_2.png)

Alternatively, we could use a more colorful palette option, such as **RdYlGn**. However, because this palette is made for continous data, you would do better if instead use color_style option `n(#)`.

```stata
color_style RdYlGn, n(3)
two (scatter seplen sepwid if iris==1) ///
    (scatter seplen sepwid if iris==2) ///
    (scatter seplen sepwid if iris==3), ///
    legend(order(1 "Sectosa" 2 "Versicolor" 3 "Virginica"))
```
![Sepal Length vs Sepal Width](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/stata_palettes_3.png)

By using `color_style` function, we can change the colors used for the data points. However, using this method has the hard constrain of defining up to 15 different colors. Check the helpfile of `colorpalette` to see all predefined colorpalette options, and type `color_style, list` for additional palettes that come with this command.

In addition to changing the color of data points, we can use color palettes to change the fill color of a graph object, which is particularly useful when creating bar charts, line graphs, boxPlots, or filling in confidence intervals. Let's create a new example where we plot the means of sepal and petal length and width.

```stata
color_style s2
graph bar (mean) seplen sepwid petlen petwid, title("S2color-Stata Default") name(m1)
color_style RdYlGn
graph bar (mean) seplen sepwid petlen petwid, title("RdYlGn-up to 15") name(m2)
color_style RdYlGn, n(4)
graph bar (mean) seplen sepwid petlen petwid, title("RdYlGn-for 4 groups") name(m3)
color_style google
graph bar (mean) seplen sepwid petlen petwid, title("Google-Palette") name(m4)
graph combine m1 m2 m3 m4, nocopies
```

![Sepal Petal Means](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/stata_palettes_4.png)

There could be, however, that a particular palette is not yet available in `color_style`, or `colorpalette`. If you have the HEX colors, you can still use them!. Here I use "Simpsons" and "Tron" hex colors for the bar graphs.

```stata
** Like Simpsons (ggsci)
color_style #FED439 #709AE1 #8A9197 #D2AF81
graph bar (mean) seplen sepwid petlen petwid, title("S2color-Stata Default") name(m5)
** Like Tron (ggsci)
color_style #FF410D #6EE2FF #F7C530 #95CC5E
graph bar (mean) seplen sepwid petlen petwid, title("RdYlGn-up to 15") name(m6)
graph combine m5 m6, nocopies
```

![Sepal Petal Means2](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/stata_palettes_5.png)


### Continuous Data

The previous examples use a discrete variable to color the data by. While colorpalette allows you to set colors for continuous data as well, using interpolation of colors when appropriate, schemes can only manage up to 15 different groups. There are other user written commands, however that work with colorpalette on the background, and may allow you to do this kind of graphs

```stata
** Like Scatter but for multiple groups.
ssc install mscatter
mscatter seplen sepwid, over(petlen) colorpalette(viridis) alegend msize(2) title(viridis) name(m7, replace) legend(col(2))
mscatter seplen sepwid, over(petlen) colorpalette(egypt) alegend msize(2) title(egypt) name(m8, replace)  legend(col(2))
mscatter seplen sepwid, over(petlen) colorpalette(magma) alegend msize(2) title(magma) name(m9, replace)  legend(col(2))
mscatter seplen sepwid, over(petlen) colorpalette(google) alegend msize(2) title(google) name(m10, replace)   legend(col(2))
graph combine m7 m8 m9 m10, nocopies altshrink
```
![Scatter-MultiGoup](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Color_Palettes/stata_palettes_6.png)

While this approach provides an option for multiple levels of colors, some work is needed to have better formatted labels.

These simple examples should  demonstrate that there are lots of customization options available for your graphs. Ultimately, it comes down to personal preference and what type of data you are modeling. Make sure to keep in mind too how you should call attention to specific parts of your charts to best convey the information within the data.

### What is happening in the background

To understand what is happening in the background. `color_style` calls on `colorpalette` to identify colors for a particular palette. `colorpalette` comes loaded with many predefined palettes, which are constantly being updated. Once the colors are obtained, `color_style` calls on `grstyle` to modify all color attributes in the current scheme. `color_style` also comes with a good selection of palettes, that one may want to explore.

By default, `color_style` uses all colors in a particular palette, recycling them if more colors are needed. However, one can request use fewer colors (say 3), for better color contrast. This may depend on the type of palette one is using. Using this method only allows you to change colors for up to 15 groups. Other programs exist, however, when one wants to use more than 15 groups of colors.
