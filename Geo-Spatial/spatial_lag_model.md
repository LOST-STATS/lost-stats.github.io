---
title: Spatial Lag Model
parent: Geo-Spatial
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Spatial Lag Model

Data that is to some extent geographical in nature often displays *spatial autocorrelation*. Outcome variables and explanatory variables both tend to be clustered geographically, which can drive spurious correlations, or upward-biased treatment effect estimates [(Ploton et al. 2020)](https://www.nature.com/articles/s41467-020-18321-y).

One way to account for this spatial dependence is to model the autocorrelation directly, as would be done with autocorrated time-series data. One such model is the spatial lag model, in which a dependent variable is predicted using the value of the dependent variable of an observation's "neighbors."

$$ Y_i = \rho W Y_j + \beta X_i + \varepsilon_i $$

Where $Y_j$ is the set of $Y$ values from observations other than $i$, and $W$ is a matrix of spatial weights, which are higher for $j$s that are spatially closer to $i$.

This process requires estimation of which observations constitute neighbors, and generally the estimation of $\rho$ is performed using a separate process from how $\beta$ is estimated. More estimation details are in [Darmofal (2015)](https://books.google.com/books?hl=en&lr=&id=ULrbCgAAQBAJ&oi=fnd&pg=PR15&dq=darmofal+2015&ots=Au-lgbU6CX&sig=lInE51tvCv3aq09ht6pIUQGOsmw#v=onepage&q=darmofal%202015&f=false).

## Keep in Mind

- There is more than one way to create the weighting matrix, and also more than one way to estimate the spatial lag model. Be sure to read the documentation to see what model and method your command is estimating, and that it's the one you want.
- Some approaches select a list of "neighbor" observations, such that each observation $j$ either is or is not a neighbor of $i$ (note that non-neighbors can still affect $i$ if they are neighbors-of-neighbors, and so on)
- The effect of a given predictor in a spatial lag model is not just given by its coefficient, but should also include its spillover effects via $\rho$.

## Also Consider

- There are other ways of modeling spatial dependence, such as the [Spatial Moving-Average Model]({{ "/Geo-Spatial/spatial_moving_average_model.html" | relative_url }})
- A common test to determine whether there is spatial dependence that needs to be modeled is the [Moran Test]({{ "/Geo-Spatial/moran_test.html" | relative_url }})

# Implementations

These examples will use some data on US colleges from [IPEDS](https://nces.ed.gov/ipeds/), including their latitude, longitude, and the extent of distance learning they offered in 2018. It will then see if this distance learning predicts (and perhaps reduces?) the prevalence of COVID in the college's county by July 2020.

## Python

```python
import pandas as pd
# can install all below with:
# !pip install pysal
from libpysal.cg import KDTree, RADIUS_EARTH_MILES
from libpysal.weights import KNN
from spreg import ML_Lag

url = ('https://github.com/LOST-STATS/lost-stats.github.io/raw/source'
        '/Geo-Spatial/Data/Merging_Shape_Files/colleges_covid.csv')

# specify index cols we need only for identification -- not modeling
df = pd.read_csv(url, index_col=['unitid', 'instnm'])

# we'll `pop` renaming columns so they're no longer in our dataframe
x = df.copy().dropna(how='any')

# tree object is the main input to nearest neighbors
tree = KDTree(
    data=zip(x.pop('longitude'), x.pop('latitude')), 
    # default is euclidean, but we want to use arc or haversine distance
    distance_metric='arc',
    radius=RADIUS_EARTH_MILES
)
nn = KNN(tree, k=5)

y = x.pop('covid_cases_per_cap_jul312020')

# spreg only accepts numpy arrays or lists as arguments
mod = ML_Lag(
    y=y.to_numpy(),
    x=x.to_numpy(), 
    w=nn,
    name_y=y.name,
    name_x=x.columns.tolist()
)

# results
print(mod.summary)


```

## R

```r
# if necessary
# install.packages(c('spatialreg', 'spdep'))

# Library for calculating neighbors
library(spdep)
# And for the spatial lag model
library(spatialreg)

# Load data
df <- read.csv('https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Geo-Spatial/Data/Merging_Shape_Files/colleges_covid.csv')

# Use latitude and longitude to determine the list of neighbors
# Here we're using K-nearest-neighbors to find 5 neighbors for each college
# But there are othe rmethods available

# Get latitude and longitude into a matrix
# Make sure longitude comes first
loc_matrix <- as.matrix(df[, c('longitude','latitude')])

# Get 5 nearest neighbors
kn <- knearneigh(loc_matrix, 5)

# Turn the k-nearest-neighbors object into a neighbors object
nb <- knn2nb(kn)

# Turn the nb object into a listw object
# Which is a list of spatial weights for the neighbors
listw <- nb2listw(nb)

# Use a spatial regression
# This uses the method from Bivand & Piras (2015) https://www.jstatsoft.org/v63/i18/.
m <- lagsarlm(covid_cases_per_cap_jul312020 ~ pctdesom + pctdenon, 
              data = df, 
              listw = listw)

# Note that, whlie summary(m) will show rho below the regression results,
# most regression-table functions like modelsummary::msummary() or jtools::export_summs()
# will include it as a coefficient along with the others and report its standard error
summary(m)
```

## Stata

Stata has a suite of built-in spatial analysis commands, which we will be using here. A more thorough description of using Stata for spatial autocorrelation models (and perhaps using shapefiles to start with) can be found [here](https://www.stata.com/features/overview/spatial-autoregressive-models/).

```stata
* Import data
import delimited using "https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Geo-Spatial/Data/Merging_Shape_Files/colleges_covid.csv", clear

* This process requires full data
drop if missing(pctdesom) | missing(pctdenon)

* Get Stata to recognize this is a spatial dataset
* with longitude and latitude
spset unitid, coord(longitude latitude)

* Create matrix of inverse distance weights
spmatrix create idistance M
* Note that Stata doesn't have an automatic process for selecting a set of neighbors
* Unless you are working with a shapefile

* Run spatial regression model
* This uses a maximum likelihood estimator, but GS2SLS is also available
spregress covid_cases_per_cap_jul312020 pctdesom pctdenon, ml dvarlag(M)

* Get impact of each predictor, including spillovers, with estat impact
estat impact
```
