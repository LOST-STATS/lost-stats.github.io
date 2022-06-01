---
title: "Animated graphs"
parent: Figures
grand_parent: Presentation
has_children: no
nav_order: 1
mathjax: no
output:
  html_document:
    keep_md: true
---

# Animated graphs

This is a brief explanation of how to make animated graphs. Animated graphs help present information that changes over the years or states. Therefore, it is a useful tool to use for some scenarios.

## Keep in Mind

- Animated graphs can be in any shape line, plot,  bar, etc.
- For animated graphs, it is easier to graph fewer groups to show the changes, however with some data manipulation and using an adequate color plate we can present, a nicely animated graph shows many categories.
- The animated dimensions are important to present the animated details. 
- Each animation required is the right duration and the number of frames depends on the given inputs.

## Also Consider

- You may need to do some data manipulation to create the right animated graph.
- Check- Check the presentation [Figures]({{ "/Presentation/Figures/Figures.html" | relative_url }}), there are many charts we can animate. 

# Implementations

Notes on implementations: 

## R

There are many great packages to do animated graphs such as gganimate and plotly.
here we used gganimate, and ggplot2 to do animated bar graphs. and gifski to save the results.

In R, one of the best tools for creating graphs is the function ggplot(), found in the ggplot2 package.

For this R demonstration, we will introduce how to use ggplot2 package to create Animated graphs. First, we load all the packages we need.

```r
# Load in necessary packages
library(ggplot2)
library(gganimate)
library(gifski)
library(dplyr)
```

```
## 
## Attaching package: 'dplyr'
```

```
## The following objects are masked from 'package:stats':
## 
##     filter, lag
```

```
## The following objects are masked from 'package:base':
## 
##     intersect, setdiff, setequal, union
```

```r
# Load in desired data (gapminder)
library(gapminder)
```

## Animated bar charts

### example for animated bar charts shows comparisinf over time for two countries.

```r
graph_data1 <- gapminder  %>% filter(continent=="Oceania")

# first use ggplot for the graph 
ggplot(graph_data1, aes(x=country, y=gdpPercap, fill=country)) + 
  geom_bar(stat='identity') +
  theme_bw() + # then set the gganimate,
  transition_states( # to specify the transition, here we specify 
    year,
    transition_length = 2,
    state_length = 1) +
  ease_aes('sine-in-out') + # to control easing of aesthetics 
  labs(title = 'Gdp per Capita in year: {closest_state}', # title with the timestamp period
  subtitle = 'Oceania countries (1992 - 2007)') 
```

<img src="Animated-graphs_files/figure-html/unnamed-chunk-2-1.gif" style="display: block; margin: auto;" />

```r
anim_save("graph1.gif") # to save the graph as gif
```

### example for animated bars for 25 countries over time.


```r
graph_data <- gapminder %>% filter(continent=="Americas")

# Plot bar graphs by country, we have 25 countries in the Americas, that hard to interpretation using one graph.
# this example shows how gganimate can create a nice animated graph even with that high number of countries 
graph_2 <- ggplot(graph_data, aes(x=country, y=gdpPercap, fill=country)) + 
  geom_bar(stat='identity') +
  theme_bw() + # gganimate specific bits:
  transition_states(
    year,
    transition_length = 2,
    state_length = 1) +
  ease_aes('sine-in-out')+ 
  theme(axis.text=element_blank(),
        axis.title.x=element_blank(),
        legend.position="center",
        panel.border=element_blank(),
        axis.title.y=element_text(size=20),
        axis.text.y = element_text(hjust=1, size=16),
        axis.text.x = element_text(angle = 45, hjust=1, size=16),
        plot.title=element_text(size=25, hjust=0.5, face="bold", colour="black", vjust=1),
        plot.subtitle=element_text(size=24, hjust=0.5, face="italic", color="grey"),
        plot.margin = margin(2, 2, 4, 4, "cm"))+ 
  labs(title = 'Gdp per Capita for year: {closest_state}', # title with the timestamp period
  subtitle = 'Americas countries (1992 - 2007)') 
```

### Save it as gif file formate using animated function


```r
# The animated sitting, create an image per frame, in this example, we used year so it creates an image for each year
animate(graph_2, 100, fps = 20, end_pause=30,  width = 1400, height = 1000, 
        renderer = gifski_renderer("gganim1.gif"))
```

![](Animated-graphs_files/figure-html/unnamed-chunk-4-1.gif)<!-- -->

## Animatrd Line Chart 


```r
# Plot North America, here we try line graph by only graph North America countries 
graph_data3 <- graph_data %>% filter(country %in% c("United States", "Canada", "Mexico"))

# Plot line graph
graph_3 <- ggplot(data = graph_data3) +
  geom_line(mapping = aes(x=year, y=lifeExp, color=country)) +
  theme_bw() +
  theme(legend.position = "right") +
  labs(title = 'Life Expectancy in North America (1992 - 2007)')+
    transition_reveal(year) + #Reveal data along a given dimension 
  ease_aes('linear') # The values change linearly during tweening
  
graph_3
```

<img src="Animated-graphs_files/figure-html/unnamed-chunk-5-1.gif" style="display: block; margin: auto;" />

```r
anim_save("graph_3.gif") # to save the graph as gif
```
