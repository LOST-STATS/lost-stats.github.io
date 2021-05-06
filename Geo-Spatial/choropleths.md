---
title: Choropleths
parent: Geo-Spatial
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Choropleths

Choropleths are maps in which areas are shaded or patterned in proportion to a statistical variable that represents an aggregate summary of a geographic characteristic within each area. For instance, population might be represented by dark green where it is (relatively) high and light green where it is (relatively) low. Choropleths are useful when you want to show differences in variables across areas.

## Keep in Mind

- Geospatial packages in R and Python tend to have a large number of complex dependencies, which can make installing them painful. Best practice is to install geospatial packages in a new virtual environment.
- Think carefully about the units you're using and whether plotting your data on a map is really informative. Choropleths can all too easily end up simply being plots of population density - and no-one will be surprised to see that areas like Manhattan have a high population!

# Implementations

## Python

The [**geopandas**](https://geopandas.org/) package is the easiest way to start making choropleths in Python. For plotting more sophisticated maps, there's [**geoplot**](https://residentmario.github.io/geoplot/index.html). In the example below, we'll see three ways of plotting data on GDP per capita by geography. The first uses **geopandas** built-in `.plot` method. The second combines this with the **matplotlib** package to create a more attractive looking chart. The third example uses **geoplot** to create a cartogram in which the area of each country on the map gets shrunk according to how small its GDP per capita is.

```python
# Geospatial packages tend to have many elaborate dependencies. The quickest
# way to get going is to use a clean virtual environment and then
# 'conda install geopandas' followed by
# 'conda install -c conda-forge descartes'

import matplotlib.pyplot as plt
import geopandas as gpd

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

world = world[(world.pop_est > 0) & (world.name != "Antarctica")]

world['gdp_per_cap'] = 1.0e6 * world.gdp_md_est / world.pop_est

# Simple choropleth
world.plot(column='gdp_per_cap')

# Much better looking choropleth
plt.style.use('seaborn-paper')
fig, ax = plt.subplots(1, 1)
world.plot(column='gdp_per_cap',
           ax=ax,
           cmap='plasma',
           legend=True,
           vmin=0.,
           legend_kwds={'label': "GDP per capita (USD)",
                        'orientation': "horizontal"})
plt.axis('off')

# Now let's try a cartogram
# If you don't have it already, geoplot can be installed by runnning
# 'conda install geoplot -c conda-forge' on the command line.
import geoplot as gplt

ax = gplt.cartogram(
    world,
    scale='gdp_per_cap',
    hue='gdp_per_cap',
    cmap='plasma',
    linewidth=0.5,
    figsize=(8, 12)
)
gplt.polyplot(world, facecolor='lightgray', edgecolor='None', ax=ax)
plt.title("GDP per capita (USD)")
plt.show()
```

## R

The [**sf**](https://github.com/r-spatial/sf/) is a fantastic package to make choropleths and more in R. In the following code, we will walk through an identical example of the python implementation above, with the same data from [rnaturalearth](https://cran.r-project.org/web/packages/rnaturalearth/README.html), but using R and and creating our plots with the wonderful [ggplot2](https://ggplot2.tidyverse.org/) package. In order to produce the cartogram plots, we use the [cartogram](https://cran.r-project.org/web/packages/cartogram/index.html) package.

```r
## Load and install the packages that we'll be using today
library(sf)
library(tidyverse)
library(ggplot2)
library(rnaturalearth)
library(viridis)
library(cartogram)
library(scales)

# N.B. rnaturalearth is currently broken: https://github.com/ropensci/rnaturalearth/issues/29
world <- ne_download() %>% st_as_sf()

world = world %>%
  filter(POP_EST > 0,
         NAME != "Antarctica") %>%
  mutate(gdp_per_capita = 1.0e6*(GDP_MD_EST / as.numeric(POP_EST)))

## Simple choropleth plot
ggplot(data = world) +
    geom_sf(aes(fill = gdp_per_capita))


## Much better looking choropleth with ggplot2
world %>%
  st_transform(crs = "+proj=eqearth +wktext") %>%
  ggplot() +
    geom_sf(aes(fill = gdp_per_capita)) +
    theme_void() +
    labs(title = "",
         caption = "Data downloaded from www.naturalearthdata.com",
         fill = "GDP per capita (USD)") +
    scale_fill_viridis(labels = comma) +
  theme(legend.position = "bottom",
        legend.key.width = unit(1.5, "cm"))


## Now let's try a cartogram using the cartogram package that was loaded above
world_cartogram = world %>%
  st_transform(crs = "+proj=eqearth +wktext") %>%
  cartogram_ncont("gdp_per_capita", k = 100, inplace = TRUE)

ggplot() +
  geom_sf(data = world, alpha = 1, color = "grey70", fill = "grey70") +
  geom_sf(data = world_cartogram, aes(fill = gdp_per_capita),
          alpha = 1, color = "black", size = 0.1) +
  scale_fill_viridis(labels = comma) +
  labs(title = "Cartogram - GDP per capita",
       caption = "Data downloaded from www.naturalearthdata.com",
       fill = "GDP per capita") +
  theme_void()
```
