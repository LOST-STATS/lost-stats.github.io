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
