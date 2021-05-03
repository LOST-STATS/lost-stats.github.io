---
title: Collapse a Data Set
parent: Data Manipulation
has_children: false
mathjax: true
nav_order: 1
---

# Collapse a Data Set

The *observation level* of a data set is the set of case-identifying variables which, in combination, uniquely identify every row of the data set. For example, in the data set

| I | J | X |
| - | - | - |
| 1 | 1 | 3 |
| 1 | 2 | 3.5 |
| 2 | 1 | 2 |
| 2 | 2 | 4.5 |

the variables $$I$$ and $$J$$ uniquely identify rows. The first row has $$I = 1$$ and $$J = 1$$, and there is no other row with that combination. We could also say that $$X$$ uniquely identifies rows, but in this example $$X$$ is not a case-identifying variable, it's actual data. 

It is common to want to *collapse* a data set from one level to another, coarser level. For example, perhaps instead of one row per combination of $$I$$ and $$J$$, we simply want one row per $$I$$, perhaps with the average $$X$$ across all $$I$$ observations. This would result in:

| I |  X |
| - | - |
| 1 | 3.25 |
| 2 | 3.25 |

This can be one useful way to produce [summary statistics]({{ "/Presentation/Tables/Summary_Statistics_Tables.html" | relative_url }}), but can also be used to rid the data of unnecessary or unusable detail, or to change one data set to match the observation level of another.

## Keep in Mind

- Collapsing a data set almost by definition requires losing some information. Make sure that you actually want to lose this information, rather than, for example, doing a [horizontal merge]({{ "/Data_Manipulation/Combining_Datasets/combining_datasets_horizontal_merge_deterministic.html" | relative_url }}), which can match data sets with different observation levels without losing information.
- Make sure that, for each variable you plan to retain in your new, collapsed data, you know the correct procedure that should be used to figure out the new, summarized value. Should the collapsed data for variable $$X$$ use the mean of all the observations you started with? The median? The mode? The first value found in the data? Think through these decisions.

## Also Consider

- For more information about observation levels and how to determine what the current observation level is, see [determine the observation level of a data set]({{ "/Data_Manipulation/determine_the_observation_level_of_a_data_set" | relative_url }}).

# Implementations

For our implementation examples, we'll use the "storms" dataset that comes bundled with the **dplyr** R package and is also available as a downloadable CSV [here](https://vincentarelbundock.github.io/Rdatasets/csv/dplyr/storms.csv). This dataset contains hourly track data for 198 tropical storms from 1993 to 2006. Our task in each of the implementation examples will be the same: We want to collapse this hourly dataset to the daily level, and obtain the mean wind speed and pressure reading for each storm. Moreover, we'll also get the first category listing of each storm, thereby demonstrating how we can combine multiple aggregation functions (*mean* and *first*) in a single operation.

## Julia

Julia adopts a highly modular approach to package functionality. The main data wrangling operations are all bundled in the [**DataFrames.jl**](https://dataframes.juliadata.org/stable/) package. But for this example, we'll also need to load the [**Statistics.jl**](https://github.com/JuliaLang/Statistics.jl) library (that comes bundled with the base Julia installation) for the `mean` and `first` aggregating functions. The [**RDatasets**](https://github.com/JuliaStats/RDatasets.jl) package simply provides a conveniet way to import R datasets, although we could also import the "storms" CSV manually from the web if desired.

```julia
#] add DataFrames, RDatasets
using DataFrames, Statistics, RDatasets

storms = dataset("dplyr", "storms")

combine(groupby(storms, [:name, :year, :month, :day]), 
        [:wind, :pressure] .=> mean, [:category] .=> first)
```

## Python

For our Python implementation we'll use the very popular [**pandas**](https://pandas.pydata.org/docs/) library. Note that, after specifying the grouping variables, we'll use dictionary of functions (of the form `'original column': 'function'`) to aggregate the other variables by.

```python
import pandas as pd

# Pull in data on storms
storms = pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/dplyr/storms.csv')

# We'll save the collapsed data as a new object called `storms_collapsed` (this is optional)
storms_collapsed = (storms
                    .groupby(['name', 'year', 'month', 'day'])
                    .agg({'wind': 'mean',
                          'pressure': 'mean',
                          'category': 'first'}))
```

## R

R provides several package ecoystems for data wrangling and collapsing. We'll show you three (in increasing order of speed for this particular task, although they'll all complete quickly).

First, [**dplyr**](https://dplyr.tidyverse.org/):

```r
# If necessary, install dplyr
# install.packages('dplyr')
library(dplyr)

# The storms dataset comes bundled with dplyr, so we can load it directly
data("storms")

# We'll save the collapsed data as a new object called `storms_collapsed` (this is optional)
storms_collapsed = storms %>%
  group_by(name, year, month, day) %>% 
  summarize(across(c(wind, pressure), mean), category = first(category))
```

Second, [**data.table**](https://rdatatable.gitlab.io/data.table/index.html):

```r
# install.packages('data.table')
library(data.table)

# Set the already-loaded storms dataset as a data.table
setDT(storms)

storms[, 
       .(wind=mean(wind), pressure=mean(pressure), category=first(category)), 
       by = .(name, year, month, day)]
```
Third: [**collapse**](https://sebkrantz.github.io/collapse/):

```r
# install.packages('collapse')
library(collapse)

collap(storms, 
       by = ~name+year+month+day, 
       custom = list(fmean=c('wind', 'pressure'), ffirst='category'))
```

## Stata

For Stata, we'll use the generic `collapse` command.

```stata
** Read in the data
import delimited https://vincentarelbundock.github.io/Rdatasets/csv/dplyr/storms.csv

collapse (mean) wind (mean) pressure (first) category, by(name year month day)
```
With big datasets, Stata can be slow compared to other languages, though they do seem to be trying to [change that](https://www.stata.com/new-in-stata/faster-stata-speed-improvements/) a bit. The community-contributed [**gtools**](https://gtools.readthedocs.io/en/latest/usage/gtools/index.html) suite can help a lot with speedups and, fortunately, has a faster version of collapse, called `gcollapse`. Note that we won't necessarily see a benefit for small(ish) datasets like the one that we are using here. But note that the syntax is otherwise identical. 

```stata
* ssc install gtools
* gtools, upgrade

gcollapse (mean) wind (mean) pressure (first) category, by(name year month day)
```
