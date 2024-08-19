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

# Use 'groupby' to aggregate data by groups (namely: name, year, month and day
# columns) and use 'transform!' to add a new column called 'mean_wind'
# containing the mean of the existing 'wind' column. (The `!` means that this
# change will be made in-place.)
transform!(groupby(storms, [:name, :year, :month, :day]), :wind=> mean => :mean_wind)
```

## Python

**pandas** accomplishes this by using the groupby-transform approach. We can either call numpy's mean function or use a lambda and apply the .mean() method to each group

```python
import pandas as pd

# Pull in data on storms
storms = pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/dplyr/storms.csv')

# Use groupby and agg to perform a group calculation
# Here it's a mean, but it could be any function
storms['mean_wind'] = storms.groupby(['name','year','month','day'])['wind'].transform(lambda x: x.mean())

# this tends to be a bit faster because it uses an existing function instead of a lambda
import numpy as np
storms['mean_wind'] = storms.groupby(['name','year','month','day'])['wind'].transform(np.mean)

```

Though the above may be a great way to do it, it certainly seems complex. There is a much easier way to achieve similar results that is easier on the eyes (and brain!). This is using panda's aggregate() method with tuple assignments. This results in the most easy-to-understand way, by using the aggregate method after grouping since this would allow us to follow a very simple format of `new_column_name = ('old_column', 'agg_funct')`. So, for example:

```python
import pandas as pd

# Pull in data on storms
storms = pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/dplyr/storms.csv')

# Use groupby and group the columns and perform group calculations

# The below calculations aren't particularly indicative of a good analysis,
# but give a quick look at a few of the calculations you can do
df = (
    storms
    .groupby(by=['name', 'year', 'month', 'day']) #group
    .aggregate(
        avg_wind = ('wind', 'mean'), 
        max_wind = ('wind', 'max'),
        med_wind = ('wind', 'median'),
        std_pressure = ('pressure', 'std'),
        first_year = ('year', 'first')
    )
    .reset_index() # Somewhat similar to ungroup. Removes the grouping from the index
)

```


## R

In R, we can use either the **dplyr** or **data.table** package to do this.

Here's how to do it with **dplyr**...

```r
library(dplyr)

data("storms") # The dataset is bundled with dplyr, so we'll just open directly

# Use 'group_by' to designate the groups and 'mutate' to create new column(s).
# Note that dplyr doesn't modify in-place, so we need to reassign the result.
storms = storms %>%
  group_by(name, year, month, day) %>%
  mutate(mean_wind = mean(wind))
```

...and here's how to do it with **data.table**.

```r
library(data.table)

# storms = fread("https://vincentarelbundock.github.io/Rdatasets/csv/dplyr/storms.csv")
setDT(storms) # Set the already-loaded storms DF as a data.table

# Use ':=' for in-place modification
storms[, mean_wind := mean(wind), by = .(name, year, month, day)]
```


## Stata

This process is made easy in Stata using the `egen` command. `egen` is not entirely flexible and is limited to a set of predetermined group calculations (see `help egen`), although this can be expanded using the **egenmore** package (`ssc install egenmore` then `help egenmore`). However, the list of predetermined functions is long enough that you'll rarely be caught out!

```stata
import delimited "https://vincentarelbundock.github.io/Rdatasets/csv/dplyr/storms.csv", clear

* Use bysort to determine the grouping, and egen to do the calculation
bysort name year month day: egen mean_wind = mean(wind)
```
