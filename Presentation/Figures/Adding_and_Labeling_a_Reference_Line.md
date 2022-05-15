---
title: Adding and Labeling a Reference Line
parent: Figures
grand_parent: Presentation
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Adding and Labeling a Reference Line 

With a lot of graph types, you may want to add a reference line so that the data can be compared to it. For example, perhaps you have a graph that shows growth over time, and want to have a reference line for "no growth" so you can easily see how far things have come. Or perhaps an event happens at a particular time and you want to mark when the event is. Or maybe you just want it to be easy to compare different categories to a mean.

## Keep in Mind

- Make sure that it's clear what your reference line is. A reader might not guess that it represents a mean, or a particular event, or something else. In some cases, the line extending to a particular value on the x- or y-axis does the job. Other times you might want a direct label.

## Also Consider

- This page will show how to place a line but not how to style it. You may want your line to be dashed, or bold, or a different color. In most cases the stylistic controls for your reference line will be the exact same as those for a regular [line graph]({{ "/Presentation/Figures/line_graphs.html" | relative_url }}). See [styling line graphs]({{ "/Presentation/Figures/styling_line_graphs.html" | relative_url }})

# Implementations

These implementations will add a line indicating the mean area to the bar graphs found in [line graph]({{ "/Presentation/Figures/bar_graphs.html" | relative_url }}). They will also show how to place a vertical line, this time at a particular value between the bars, showing how reference lines can be placed on discrete axes as well.

## Python

```python
# Load packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/DAAG/Manitoba.lakes.csv", index_col=0)

# Calculate the value where we want the reference line to be, the mean
# Note we could pick any other value here that we wanted
mean_area = np.mean(df['area'])

# This uses pandas' built-in bar plot function, but this uses
# matplotlib under the hood; any other matplotlib bar graph works the same
plt.style.use('seaborn')
ax = df.plot.bar(y='area', legend=False, ylabel='Area', rot=15)
ax.set_title('Area of lakes in Manitoba', loc='left')

# Place the line
plt.axhline(mean_area)

# Look at our result and figure out the appropriate x/y location
# We can figure out visually that it should be a bit above 5000, where
# the line is. But how about x? We can set x by trial and error, or 
# note that there are 9 bars and get the x-coordinate of the last one
# using ax.patches.get_x(), and adjust from there
plt.annotate('Mean Area', xy = (ax.patches[8].get_x() - .5, 5500))

# Similarly if we want to position a vertical line, we can  use plt.axvline.
# How to position it on a discrete non-numeric x axis?
# place it after the third bar using get_x to find the third bar
# and get_width to move over to the right side of the bar, then a bit more to adjust
plt.axvline(ax.patches[2].get_x() + ax.patches[2].get_width() + .25)
```

![Python Bar Graph of Canadian Areas, with Labeled Reference Lines](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Adding_and_Labeling_a_Reference_Line/python_labeled_reference_lines.png)

## R

In this example, we will place the line's label using the **ggplot2** function `annotate()`, which will require us to figure out the annotation's coordinates ourselves. However, if you prefer, you can use the point-and-click annotation tool [ggannotate](https://github.com/MattCowgill/ggannotate).

```{r}
library(tidyverse)

df = read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/DAAG/Manitoba.lakes.csv") %>%
  rename(Location = ...1)

# Get the reference value we want to mark
mean_area = df %>% pull(area) %>% mean()

# Make the bar plot, and order the bars by height, why not
p <- ggplot(df, aes(x = reorder(Location, -area), y = area)) + 
  geom_col() + 
  labs(x = 'Location', y = 'Area') +
  # add a horizontal line using geom_hline, specifying its y intercept
  geom_hline(yintercept = mean_area)

# Look at our result so far and figure out the appropriate x/y location 
# for our annotation. 
p

# We can figure out visually that it should be a bit above 5000, where
# the line is. But how about x? We want it over the 9th bar, so we start with 9
# and can adjust from there by changing x or the horizontal justification (hjust)
p <- p + annotate(geom = 'text', label = 'Mean Area', x = 9, y = 5500) + 
  # Now we can add a vertical reference line with geom_vline
  # If we want it between bars 3 and 4, that puts the line at x = 3.5
  geom_vline(xintercept = 3.5)

p
```

![R Bar Graph of Canadian Areas, with Labeled Reference Lines](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Adding_and_Labeling_a_Reference_Line/r_barplot_reference_lines.png)

## Stata

```stata
import delimited "https://vincentarelbundock.github.io/Rdatasets/csv/DAAG/Manitoba.lakes.csv", clear

rename v1 Location

* Get the reference value we want to mark
summ area
local mean_area = r(mean)

* Make the bar plot, and order the bars by height, why not
* And add a horizontal reference line with yline
graph bar area, over(Location, sort(1)) yti(Area) ///
	yline(`mean_area')
	
* From here, you need to use the Graph Editor
* Right-click the graph, do "Start Graph Editor", and add the annotation
* And you can also add a line object to place a vertical reference line

* If we want to do things ourselves, we need to switch to twoway
* (which we should do here anyway for a method that works with non-bar graphs)
* Unfortunately, twoway bar doesn't like categorical x axes so we need to do some work there

* Put the bars in order and create a labeled numeric variable
* that's in the order we want the bars
gsort -area
g Location_n = _n
* Make sure labutil is installed with ssc install labutil
labmask Location_n, values(Location)

* Get the reference value we want to mark
summ area
local mean_area = r(mean)

* NOW A DILEMMA:
* we can easily add vertical and horizontal lines in twoway with yline and xline (or tline for time series graphs)
* BUT these go BEHIND the graph, not in the foreground
* that's okay for our vertical line between bars 3 and 4 (at 3.5) so let's do that
* but for our horizontal line we'll need to draw it ourselves with function
* which is annoying since we'll have to specify its range by hand

* Start with our basic graph that mimics the graph bar we started with
twoway (bar area Location_n, xti("Location") yti("Area") xlab(1/9, valuelabel) legend(off) ///
	xline(3.5)) /// Our vertical line goes between bars 3 and 4, i.e. at 3.5
	(function y = `mean_area', range(.5 9.5) /// Now our horizontal line at the mean
	)

* Now we can look at our result and see where we think the annotation
* should go. For our x-axis value we have 9 bars so should aim somewhere around 9
twoway (bar area Location_n, xti("Location") yti("Area") xlab(1/9, valuelabel) legend(off) ///
	xline(3.5) text(5500 9 "Mean Area")) /// Our vertical line goes between bars 3 and 4, i.e. at 3.5
	(function y = `mean_area', range(.5 9.5))

```

![Stata Bar Graph of Canadian Areas, with Labeled Reference Lines](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Adding_and_Labeling_a_Reference_Line/stata_labeled_reference_lines.png)

## Tableau

To add a reference line in Tableau is easy when it's a continuous variable. Start by making your graph.

![Tableau Bar graph of Canadian areas](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Adding_and_Labeling_a_Reference_Line/tableau_reflines_1.png)

Then, go to the analytics pane and drag a reference line to your graph.

![Tableau adding a reference line](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Adding_and_Labeling_a_Reference_Line/tableau_reflines_2.png)


Select the calculation (or value) you want

![Tableau adjusting the reference line](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Adding_and_Labeling_a_Reference_Line/tableau_reflines_3.png)


And the result will be automatically labeled.

![Tableau bar graph with labeled reference line](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Adding_and_Labeling_a_Reference_Line/tableau_reflines_4.png)


For a reference line on a discrete variable, the process is much more involved. See [this guide](https://kb.tableau.com/articles/issue/add-reference-line-to-discrete-field).
