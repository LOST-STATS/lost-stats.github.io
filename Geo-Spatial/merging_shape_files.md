---
title: Merging Shape Files
mathjax: yes
nav_order: 1
parent: Geo-Spatial
has_children: no
---

# Merging Shape Files

When we work with spatial anaylsis, it is quite often we need to deal with data in different format and at different scales. For example, I have nc data with global pm2.5 estimation with $$0.01\times 0.01$$ resolution. But I want to see the pm2.5 estimation in municipal level. I need to integrate my nc file into my municipality shp file so that I can group by the data into municipal level and calculate the mean. Then, I can make a map of it.

In this page, I will use Brazil's pm2.5 estimation and its shp file in municipal level.


## Keep in Mind
- It doesn't have to be nc file to map into the shp file, any format that can read in and convert to a sf object works. But the data has to have geometry coordinates(longitude and latitude).


# Implementations

## R

Unusually for LOST, the example data files cannot be accessed from the code directly. Please visit [this page](https://github.com/LOST-STATS/lost-stats.github.io/tree/source/Geo-Spatial/Data/Merging_Shape_Files) and download both files to your working directory before running this code.

It is also **strongly recommended** that you find a high-powered computer or cloud service before attempting to run this code, as it requires a lot of memory.

```r
# If necesary
# install.packages(c('ncdf4','sp','raster','dplyr','sf','ggplot2','reprex','ggsn'))
# Load packages
library(ncdf4)
library(sp)
library(raster)
library(dplyr)
library(sf)
library(ggplot2)
library(reprex)

### Step 1: Read in nc file as a dataframe*
pm2010 = nc_open("GlobalGWRwUni_PM25_GL_201001_201012-RH35_Median_NoDust_NoSalt.nc")
nc.brick = brick("GlobalGWRwUni_PM25_GL_201001_201012-RH35_Median_NoDust_NoSalt.nc")
# Check the dimensions
dim(nc.brick)

# Turn into a data frame for use
nc.df = as.data.frame(nc.brick[[1]], xy = T)

head(nc.df)

### Step 2: Filter out a specific country.
# Global data is very big. I am going to focus only on Brazil.
nc.brazil = nc.df %>% filter(x >= -73.59 & x <= 34.47 & y >= -33.45 & y <= 5.16)
rm(nc.df)
head(nc.brazil)

### Step 3: Change the dataframe to a sf object using the st_as_sf function
pm25_sf = st_as_sf(nc.brazil, coords = c("x", "y"), crs = 4326, agr = "constant")
rm(nc.brazil)
head(pm25_sf)

### Step 4: Read in the Brazil shp file. we plan to merge to
Brazil_map_2010 = st_read("geo2_br2010.shp")
head(Brazil_map_2010)

### Step 5: Intersect pm25 sf object with the shp file.*
# Now let's use a sample from pm25 data and intersect it with the shp file. Since the sf object is huge, I recommend running the analysis on a cloud server
pm25_sample = sample_n(pm25_sf, 1000, replace = FALSE)

# Now look for the intersection between the pollution data and the Brazil map to merge them
pm25_municipal_2010 = st_intersection(pm25_sample, Brazil_map_2010)
head(pm25_municipal_2010)

### Step 6: Make a map using ggplot
pm25_municipal_2010 = pm25_municipal_2010 %>%
  select(1,6)
pm25_municipal_2010 = st_drop_geometry(pm25_municipal_2010)
Brazil_pm25_2010 = left_join(Brazil_map_2010, pm25_municipal_2010)
ggplot(Brazil_pm25_2010) +
  # geom_sf creates the map we need
  geom_sf(aes(fill = -layer), alpha=0.8, lwd = 0, col="white") +
  # and we fill with the pollution concentration data
  scale_fill_viridis_c(option = "viridis", name = "PM25") +
  ggtitle("PM25 in municipals of Brazil")+
  ggsn::blank()
```
