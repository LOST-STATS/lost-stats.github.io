---
title: Creating a Variable with Group Calculations
parent: Data Manipulation
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Creating a Variable with Group Calculations

Many data sets have hierarchical structures, where individual observations belong within certain groups. For example, data with students inside classrooms inside schools. Or companies inside countries. See the below table for one example

| I | J | X |
| - | - | - |
| 1 | 1 | 3 |
| 1 | 2 | 3.5 |
| 2 | 1 | 2 |
| 2 | 2 | 5 |

Here, we have data where each group $$I$$ has multiple rows, one for each $$J$$. 

We often might want to create a new variable that performs a calculation *within* each group, and assigns the result to each value in that group. For example, perhaps we want to calculate the mean of $$X$$ within each group $$I$$, so we can know how far above or below the group average each observation is. Our goal is:


| I | J | X | AvgX |
| - | - | - | -    |
| 1 | 1 | 3 | 3.25 |
| 1 | 2 | 3.5 | 3.25 |
| 2 | 1 | 2 | 3.5 | 
| 2 | 2 | 5 | 3.5 |


## Also Consider

- If the goal is to produce a data set with *one row per group* rather than *a new variable assigning the calculation to each observation in the group*, then instead look at [Collapse a Data Set]({{ "/Data_Manipulation/collapse_a_data_set.html" | relative_url }}).

# Implementations

## Julia 

The **DataFrames.jl** package makes data aggregation and manipulaion relatively straigthforward. 

```julia
# Load required packages
using CSV             # Import .csv files 
using DataFrames      # Working with data frames 
using Statistics      # Required to calculate a mean 

# Import .csv file from GitHub and store as a DataFrame 
storms = CSV.read(download("https://vincentarelbundock.github.io/Rdatasets/csv/dplyr/storms.csv"), DataFrame)

# Use 'groupby' to aggregate data by groups (namely: name, year, month and day columns) and use 'transform' to add a new column called 'mean_wind' containing the mean of the existing 'wind' column
storms_group = transform(groupby(storms, [:name, :year, :month, :day]), :wind=> mean => :mean_wind)
```

## Python

**pandas** doesn't have a straightforward and flexible built-in method for doing this, with aggregation methods heavily preferring to work as described on [Collapse a Data Set]({{ "/Data_Manipulation/collapse_a_data_set.html" | relative_url }}). However, we can just follow those methods and then `merge` the result back in.

```python
import pandas as pd

# Pull in data on storms
storms = pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/dplyr/storms.csv')

# Use groupby and agg to perform a group calculation
# Here it's a mean, but it could be anything
meanwind = (storms.groupby(['name', 'year', 'month', 'day'])
            .agg({'wind': 'mean'})
            # Rename so that when we merge it in it has a 
            # different name
           .rename({'wind': 'mean_wind'}))
            # make sure it's a data frame so we can join it  
    
# Use merge to bring the result back into the data
storms = pd.merge(storms,meanwind,
                    on = ['name', 'year', 'month', 'day'])
```

## R

The **dplyr** package makes this process easy.

```r
library(dplyr)

data("storms")

# Use group_by to designate the groups
storms <- storms %>%
  group_by(name, year, month, day) %>%
  # To add a new column, rather than collapse,
  # just use mutate instead of summarize
  # note that "mean" could be anything here
  mutate(mean_wind = mean(wind))
```

## Stata

This process is made easy in Stata using the `egen` command. `egen` is not entirely flexible and is limited to a set of predetermined group calculations (see `help egen`), although this can be expanded using the **egenmore** package (`ssc install egenmore` then `help egenmore`). However, the list of predetermined functions is long enough that you'll rarely be caught out!

```stata
import delimited "https://vincentarelbundock.github.io/Rdatasets/csv/dplyr/storms.csv", clear

* Use bysort to determine the grouping, and egen to do the calculation
bysort name year month day: egen mean_wind = mean(wind)
```
