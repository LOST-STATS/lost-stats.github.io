---
title: Spatial Joins
parent: Geo-Spatial
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Spatial Joins

Spatial joins are crucial for merging different types of data in geospatial analysis.  For example, if you want to know how many libraries (points) are in a city, county, or state (polygon).  This skill allows you to take data from different types of spatial data (vector data like points, lines, and polygons, and raster data (with a little more work)) sets and merge them together using unique identifiers.

Joins are typically interesections of objects, but can be expressed in different ways.  These include: equals, covers, covered by, within, touches, near, crosses, and more.  These are all functions within the [sf](https://cran.r-project.org/web/packages/sf/sf.pdf) function in R.  

**Acknowledgments to [Ryan A. Peek](https://ryanpeek.org/) for his guide that I am reimagining for LOST.**

## Keep in Mind

- When it comes to the package we are using in R for the US boundaries, it is much easier to install via the [devtools](https://cran.r-project.org/web/packages/devtools/index.html).  This will save you the trouble of getting errors when installing the data packages for the boundaries.  Otherwise, your mileage may vary. When I installed USAboundariesData via USAboundaries, I received errors.

```r
devtools::install_github("ropensci/USAboundaries")
devtools::install_github("ropensci/USAboundariesData")

```
- Note: Even with installation, you may be prompted to install the "USAboundariesData" package and need to restart your session.   


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

We will work with polygon data from the USA boundaries initially, then move on to climate data point data via the Global Surface Summary of the Day (gsodr) package and join them together.

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
Now we can plot it out.


Oregon highlighted
```r
plot(usa$geometry)
plot(or$geometry, add=T, col="gray50", border="black")
plot(or_co$geometry, add=T, border="green", col=NA)
plot(or_box, add=T, border="yellow", col=NA, lwd=2)
```
![](https://raw.githubusercontent.com/lvought/lost-stats.github.io/source/Geo-Spatial/Images/join_image_1.png)

Ohio highlighted
```r
plot(usa$geometry)
plot(oh$geometry, add=T, col="gray50", border="black")
plot(oh_co$geometry, add=T, border="yellow", col=NA)
plot(oh_box, add=T, border="blue", col=NA, lwd=2)
```
![](https://github.com/lvought/lost-stats.github.io/blob/source/Geo-Spatial/Images/join_image_2.png?raw=true)

Michigan highlighted
```r
plot(usa$geometry)
plot(mi$geometry, add=T, col="gray50", border="black")
plot(mi_co$geometry, add=T, border="gray", col=NA)
plot(mi_box, add=T, border="green", col=NA, lwd=2)
```
![](https://github.com/lvought/lost-stats.github.io/blob/source/Geo-Spatial/Images/join_image_3.png?raw=true)

All three highlighted at once.

```r
plot(usa$geometry)
plot(mi$geometry, add=T, col="gray50", border="black")
plot(mi_co$geometry, add=T, border="gray", col=NA)
plot(mi_box, add=T, border="green", col=NA, lwd=2)
plot(oh$geometry, add=T, col="gray50", border="black")
plot(oh_co$geometry, add=T, border="yellow", col=NA)
plot(oh_box, add=T, border="blue", col=NA, lwd=2)
plot(or$geometry, add=T, col="gray50", border="black")
plot(or_co$geometry, add=T, border="green", col=NA)
plot(or_box, add=T, border="yellow", col=NA, lwd=2)
```

Now that there are polygons established and identified, we can add in some point data to join to our currently existing polygon data and do some analysis with it.  To do this we will use the Global Surface Summary of the Day (gsodr) package for climate data.

We will take the metadata from the GSODR package via 'isd_history', make it spatial data, then filter out only those observations in our candidate states of Oregon, Ohio, and Michigan.

```r
load(system.file("extdata", "isd_history.rda", package = "GSODR"))

#We want this to be spatial data
isd_history <- as.data.frame(isd_history) %>% 
  st_as_sf(coords=c("LON","LAT"), crs=4326, remove=FALSE)  

#There are many observations, so we want to narrow it to our three candidate states
isd_history_or <- dplyr::filter(isd_history, CTRY=="US", STATE=="OR")
isd_history_oh <- dplyr::filter(isd_history, CTRY=="US", STATE=="OH")
isd_history_mi <- dplyr::filter(isd_history, CTRY=="US", STATE=="MI")
```
This filtering should take you from around 26,700 observation sites around the world to approximately 200 in Michigan, 85 in Ohio, and 100 in Oregon.  These numbers may vary based on when you independently do your analysis.

Let's see these stations plotted in each state individually:

Note: the codes in the 'border' and 'bg' identifiers are from the [viridis](https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html) package.  You can get some awesome color scales using that package.  You can also use standard names.

Oregon
```r
plot(isd_history_or$geometry, cex=0.5)
plot(or$geometry, col=alpha("gray", 0.5), border="#1F968BFF", lwd=1.5, add=TRUE)
plot(isd_history_or$geometry, add=T, pch=21, bg="#FDE725FF", cex=0.7, col="black")
title("Oregon GSOD Climate Stations")
```

![](https://github.com/lvought/lost-stats.github.io/blob/source/Geo-Spatial/Images/join_image_5.png?raw=true)


Ohio
```r
plot(isd_history_oh$geometry, cex=0.5)
plot(oh$geometry, col=alpha("red", 0.5), border="gray", lwd=1.5, add=TRUE)
plot(isd_history_oh$geometry, add=T, pch=21, bg="black", cex=0.7, col="black")
title("Ohio GSOD Climate Stations")
```

![](https://github.com/lvought/lost-stats.github.io/blob/source/Geo-Spatial/Images/join_image_6.png?raw=true)

Michigan
```r
plot(isd_history_mi$geometry, cex=0.5)
plot(mi$geometry, col=alpha("green", 0.5), border="blue", lwd=1.5, add=TRUE)
plot(isd_history_mi$geometry, add=T, pch=21, bg="white", cex=0.7, col="black")
title("Michigan GSOD Climate Stations")
```
![](https://github.com/lvought/lost-stats.github.io/blob/source/Geo-Spatial/Images/join_image_7.png?raw=true)