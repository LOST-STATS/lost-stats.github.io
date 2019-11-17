---
title: Collapse a Data Set
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

It is common to want to *collapse* a data set from one level to another, coarser level. For example, perhaps instead of one row per combination of $$I$$ and $$J$$, we simply want one row per $$I$$, perhaps with the average $$X$$ across all $$I$$ observations. This would result in:

| I |  X |
| - | - |
| 1 | 3.25 |
| 2 | 3.25 |

This can be one useful way to produce [summary statistics](https://lost-stats.github.io/Summary_Statistics/summary_statistics.html), but can also be used to rid the data of unnecessary or unusable detail, or to change one data set to match the observation level of another.

## Keep in Mind

- Collapsing a data set almost by definition requires losing some information. Make sure that you actually want to lose this information, rather than, for example, doing a [horizontal merge](https://lost-stats.github.io/Data_Manipulation/Combining_Datasets/combining_datasets_horizontal_merge_deterministic.html), which can match data sets with different observation levels without losing information.
- Make sure that, for each variable you plan to retain in your new, collapsed data, you know the correct procedure that should be used to figure out the new, summarized value. Should the collapsed data for variable $$X$$ use the mean of all the observations you started with? The median? The mode? The first value found in the data? Think through these decisions.

## Also Consider

- For more information about observation levels and how to determine what the current observation level is, see [determine the observation level of a data set](https://lost-stats.github.io/Data_Manipulation/determine_the_observation_level_of_a_data_set).

# Implementations

## R

```r
# If necessary, install dplyr
# install.packages('dplyr')
library(dplyr)

# Get data on storms from dplyr
data("storms")

# We would like each storm to be identified by
# name, year, month, and day
# However, currently, they are also identified by hour,
# And even then there are sometimes multiple observations per hour

# To construct the collapsed data, we start with the original
storms_collapsed <- storms %>%
  # group by the variables that make the new observation level
  group_by(name, year, month, day) %>% 
  # And use summarize() to pick the variables to keep, as well as
  # the functions we want to use to collapse each variable.
  # Let's get the mean wind and pressure, and the first category value
  summarize(wind = mean(wind),
            pressure = mean(pressure),
            category = first(category))
# Note that if we wanted to collapse every variable in the data with the 
# same function, we could instead use summarize_all()
```

## Stata

```stata
** Load surface.dta, which contains temperature recordings in different locations
sysuse surface.dta, clear

* Currently, there is one observation per latitude per longitude per date
* I would like this to just be one observation per latitude/longitude

* So I construct a collapse command.
* I take my new target observation level and put it in by()
* and then take each variable I'd like to keep around and tell
* Stata what function to use to create the new collapsed value, here (mean)
collapse (mean) temperature, by(latitude longitude)
```
