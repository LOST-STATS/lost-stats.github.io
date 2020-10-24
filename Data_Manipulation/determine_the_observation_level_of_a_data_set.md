---
title: Determine the Observation Level of a Data Set
parent: Data Manipulation
has_children: false
mathjax: true
nav_order: 1
---

# Determine the Observation Level of a Data Set

The *observation level* of a data set is the set of case-identifying variables which, in combination, uniquely identify every row of the data set. For example, in the data set

| I | J | X |
| - | - | - |
| 1 | 1 | 3 |
| 1 | 2 | 3.5 |
| 2 | 1 | 2 |
| 2 | 2 | 4.5 |

the variables $$I$$ and $$J$$ uniquely identify rows. The first row has $$I = 1$$ and $$J = 1$$, and there is no other row with that combination. We could also say that $$X$$ uniquely identifies rows, but in this example $$X$$ is not a case-identifying variable, it's actual data.

When working with data that has case-identifier variables, like panel data, it's generally a good idea to know what set of them makes up the observation level of a data set. Otherwise you might perform [merges]({{ "/Data_Manipulation/Combining_Datasets/combining_datasets_horizontal_merge_deterministic.html" | relative_url }}) or case-level calculations incorrectly.

## Keep in Mind

- As in the above example, it's easy to uniquely identify rows using continuous data. But the goal is to figure out which *case-identifying* variables, like an individual's ID code, or a country code, or a time code, uniquely identify rows. Make sure you only try these variables.
- Even if you think you know what the observation level is, it's good to check. Lots of data is poorly behaved!

## Also Consider

- You can [collapse a data set]({{ "/Data_Manipulation/collapse_a_data_set.html" | relative_url }}) to switch from one observation level to another, coarser one.

# Implementations

## Python

To check for duplicate rows when using [**pandas**](https://pandas.pydata.org/) dataframes, you can call `duplicated` or, to omit the duplicates, `drop_duplicates`.

```python
# Use conda or pip to install pandas if you don't already have it installed

import pandas as pd

storms = pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/dplyr/storms.csv')

# Find the duplicates by name, year, month, day, and hour
level_variables = ['name', 'year', 'month', 'day', 'hour']
storms[storms.duplicated(subset=level_variables)]

# Drop these duplicates, but retain the first occurrence of each
storms = storms.drop_duplicates(subset=level_variables, keep='first')

```

## R

```r
# If necessary, install dplyr
# install.packages('dplyr')
# We do not need dplyr to detect the observation level
# But we will use it to get data, and for our alternate approach
library(dplyr)

# Get data on storms from dplyr
data("storms")

# Each storm should be identified by
# name, year, month, day, and hour
# anyDuplicated will return 0 if there are no duplicate combinations of these
# so if we get 0, the variables in c() are our observation level.
anyDuplicated(storms[,c('name','year','month','day','hour')])

# We get 2292, telling us that row 2292 is a duplicate (and possibly others!)
# We can pick just the rows that are duplicates of other rows for inspection
# (note this won't get the first time that duplicate shows up, just the subsequent times)
duplicated_rows <- storms[duplicated(storms[,c('name','year','month','day','hour')]),]


# Alternately, we can use dplyr
storms %>%
  group_by(name, year, month, day, hour) %>%
  # Add a variable with the number of times that particular combination shows up
  mutate(number_duplicates = n()) %>%
  # Then take that variable out
  pull(number_duplicates) %>%
  # And get the maximum of it
  max()
# If the result is 1, then we have found the observation level. If not, we have duplicates.

# We can pick out the rows that are duplicated for inspection
# by filtering on n(). This approach will give you every time the duplicate appears.
duplicated_rows <- storms %>%
  group_by(name, year, month, day, hour) %>%
  # Add a variable with the number of times that particular combination shows up
  filter(n() > 1)
```

## Stata

```stata
* Load surface.dta, which contains temperature recordings in different locations
sysuse surface.dta, clear

* duplicates report followed by a variable list will show how many times
* each combination shows up.
* I think there is one observation level for each location, so I'll check that
duplicates report latitude longitude
* If I am correct, then the only number in the "Copies" column will be 1.
* But it looks like I was not correct.

* duplicates tag will create a binary variable with 1 for all duplicates
* so I can examine the problem more closely
* (duplicates examples is another option)
duplicates tag latitude longitude, g(duplicated_data)

* If I want to know not just whether there are duplicates but how many
* of each there are for when I look more closely, I can instead do
by latitude longitude, sort: g number_of_duplicates_in_this_group = _N
```

For especially large datasets the [**Gtools**](https://gtools.readthedocs.io/en/latest/index.html) version of the various duplicates commands, [gduplicates](https://gtools.readthedocs.io/en/latest/usage/gduplicates/index.html), is a great option
```stata
* Install gtools if necessary
* ssc install gtools
* Recreate the two duplicates tasks from above
gduplicates report latitude longitude
gduplicates tag latitude longitude, g(g_duplicated_data)
```
