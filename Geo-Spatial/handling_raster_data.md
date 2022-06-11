---
title: Handling Raster Data
parent: Geo-Spatial
has_children: false
nav_order: 1
mathjax: false ## Switch to false if this page has no equations or other math rendering.
---

# Handling Raster Data

**Raster Data** is a form of storing data in a matrix organized by column and rows that contain values of information for an object. This matrix is formed of either cells or pixels. Information in this matrix can be discrete/thematic data like geospatial data, continuous data like temperature, and scanned data such as drawings. 

Since raster data is simple in design, the application of raster data is far reaching. Digital photographs and some LCD monitors have their data stored in raster format. In the context of geo-spatial, raster data is one pillar of geo-spatial analysis.  Continuous data such as landscapes and population densities can be presented as a surface map. Discrete data from sources like satellites can be analyzed so that maps can be made categorizing pixels to determine land use.  

## Keep in Mind

- Raster data files can become very large very quickly. Each cell contains information and the more accurate a graph or picture gets, the more information and number of cells needed grow rapidly. 
-	Zooming in and out of a raster image can lead to unappealing graphs or even loss of information. Inaccuracies can also occur depending on the dataset’s dimensions. 


## Also Consider

-	Another way to store and analyze data is using a vector approach. [**Data Carpentry**](https://datacarpentry.org/r-raster-vector-geospatial/06-vector-open-shapefile-in-r/index.html) has a very useful online lecture about Raster and vector data. 

# Implementations

## R

```r
# if necessary
# install.packages(c('sf', 'raster', 'stars', 'ggplot2', 'dplyr'))

library(sf)
library(raster)
library(ggplot2)
library(dplyr)
library(stars)

#The package **stars** contains data that can be used as a good starting point on how to work with raster data. 
ob_tif = system.file("tif/L7_ETMs.tif", package = "stars")
ob = read_stars(ob_tif)
ob
```

As you can see above, ther is alot of information packed into raster objects. Near the bottom of the table you will see X and Y values. We can use a function from **sf** to quickly find the dimensions of the file.

```r
st_bbox(ob)

#Now lets plot this information with the plot command with the raster package. 

plot(ob)
```

The next example will be using information from [**Harvard Forest and Quabbin Watershed NEON**](https://www.neonscience.org/field-sites/harv). This information is open to the public, but can be overwhelming. A single file can be found under the Data folder, then the Handling_Raster_Data folder. 

```r
harv = raster("https://github.com/LOST-STATS/lost-stats.github.io/blob/master/Geo-Spatial/Data/Handling_Raster_Data/HARV_dsmCrop.tif")

harv
```

There is a lot of meta data tied to every raster file. Note the line starting with **CRS**. This contains the bulk to the infromation you may be interested in. Notice at the end of the **CRS** line you can see "+units=m". This means this data is measured in meters.

```r
summary(harv)

#Here is another way to summarize the data. If you are more interested in learning about min, max, and NAs, then using the summary command is better. Notice the error statement. There is way too much data, so R is picking a random sample of the data. The summary with all the data can be pulled with the commented-out command below.
# summary(harv, maxsamp = ncell(harv))

# In order to use this information in ggplot, we will need to turn this data into a dataframe. 
harv_m = as.data.frame(sanj, xy = TRUE)
str(harv_m)

#str command gives you a quick third way to summarize the data. The raster data was turned into a dataframe with the X, Y, and fill(HARV_dsmCrop) as their own variables. 
ggplot() + 
  geom_raster(data = sanj_m, aes(x=x, y=y, fill=HARV_dsmCrop)) + 
  scale_fill_viridis_c()

#Look at this beautiful graph! 
#scale_fill_viridis_c() is a command in ggplot2 that is color blind friendly. 
```
