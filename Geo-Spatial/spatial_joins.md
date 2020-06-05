---
title: Spatial Joins
parent: Geo-Spatial
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Spatial Joins

Spatial joins are crucial for merging different types of data in geospatial analysis.  For example, if you want to know how many libraries (points) are in a city, county, or state (polygon).  This skill allows you to take data from different types of spatial data (vector data like points, lines, and polygons, and raster data (with a little more work)) sets and merge them together using unique identifiers.

Joins are typically interesections of objects, but can be expressed in different ways.  These include: equals, covers, covered by, within, touches, near, crosses, and more.  These are all functions within the sf function in R.

## Keep in Mind

- When it comes to the package we are using in R for the US boundaries, it is much easier to install via the devtools.  This will save you the trouble of getting errors when installing the data packages for the boundaries.

```r
devtools::install_github("ropensci/USAboundaries")
devtools::install_github("ropensci/USAboundariesData")

```
- Even with installation, you may be prompted to install the "USAboundariesData" package and need to restart your session.

## Also Consider

- LIST OF OTHER TECHNIQUES THAT WILL COMMONLY BE USED ALONGSIDE THIS PAGE'S TECHNIQUE
- (E.G. LINEAR REGRESSION LINKS TO ROBUST STANDARD ERRORS),
- OR INSTEAD OF THIS TECHNIQUE
- (E.G. PIE CHART LINKS TO A BAR PLOT AS AN ALTERNATIVE)
- WITH EXPLANATION
- INCLUDE LINKS TO OTHER LOST PAGES WITH THE FORMAT [Description](https://lost-stats.github.io/Category/page_name.html). Categories include Data_Manipulation, Geo-Spatial, Machine_Learning, Model_Estimation, Presentation, Summary_Statistics, Time_Series, and Other

# Implementations

## R

We will need a few packages to do our analysis.  If you need to install any packages, do so with install.packages('name_of_package'), then load it if necessary.

```r
library(here)
library(sf)
library(dplyr)
library(viridis)
library(ggplot2)
library(USAboundaries)
library(rnaturalearth)
library(GSODR)
library(ggrepel)
library(cowplot)
```

We will work with polygon data from the USA boundaries initially, then move on to climate data point data and join them together.

We start with the boundaries of the United States to get desirable polygons to work with for our analysis.  To pay homage to the states of my alma maters, we will do some analysis with Oregon, Ohio, and Michigan.

```r
#Selecting the United States Boundaries, but omitting Alaska, Hawaii, and Puerto Rico for it to be scaled better

usa <- us_boundaries(type="state", resolution = "low") %>% 
  filter(!state_abbr %in% c("PR", "AK", "HI"))
  
#Ohio with high resolution
oh <- USAboundaries::us_states(resolution = "high", states = "OH")

#Oregon with high resolution
or <- USAboundaries::us_states(resolution = "high", states = "OR")

#Michigan with high resolution
mi <- USAboundaries::us_states(resolution = "high", states = "MI")

#Insets for the identified states

#Oregon
or_box <- st_make_grid(or, n = 1)

#Ohio
oh_box <- st_make_grid(oh, n = 1)

#Michigan
mi_box <- st_make_grid(mi, n = 1)

#We can also include the counties boundaries within the state too!

#Oregon
or_co <- USAboundaries::us_counties(resolution = "high", states = "OR")

#Ohio
oh_co <- USAboundaries::us_counties(resolution = "high", states = "OH")

#Michigan

mi_co <- USAboundaries::us_counties(resolution = "high", states = "MI")
```
Now we can plot it out

```r
plot(usa$geometry)
plot(or$geometry, add=T, col="gray50", border="black")
plot(or_co$geometry, add=T, border="green", col=NA)
plot(or_box, add=T, border="yellow", col=NA, lwd=2)
```
```r
plot(usa$geometry)
plot(oh$geometry, add=T, col="gray50", border="black")
plot(oh_co$geometry, add=T, border="yellow", col=NA)
plot(oh_box, add=T, border="blue", col=NA, lwd=2)
```
```r
plot(usa$geometry)
plot(mi$geometry, add=T, col="gray50", border="black")
plot(mi_co$geometry, add=T, border="gray", col=NA)
plot(mi_box, add=T, border="green", col=NA, lwd=2)
```
