---
title: Reshape Panel Data from Wide to Long
grand_parent: Data Manipulation ## Optional for indexing
parent: Reshaping Data
has_children:  false
nav_order: 1
---

# Reshape Panel Data from Wide to Long

Panel data is data in which individuals are observed at multiple points in time. There are two standard ways of storing this data:

In wide format, there is one row per individual. Then, for each variable in the data set that varies over time, there is one column per time period. For example:

| Individual | FixedCharacteristic | TimeVarying1990 | TimeVarying1991 | TimeVarying1992 |
|------------|---------------------|-----------------|-----------------|-----------------|
| 1          | C                   | 16              | 20              | 22              |
| 2          | H                   | 23.4            | 10              | 14              |

This format makes it easy to perform calculations across multiple years.

In long format, there is one row per individual per time period:

| Individual | FixedCharacteristic | Year | TimeVarying |
|------------|---------------------|------|-------------|
| 1          | C                   | 1990 | 16          |
| 1          | C                   | 1991 | 20          |
| 1          | C                   | 1992 | 22          |
| 2          | H                   | 1990 | 23.4        |
| 2          | H                   | 1991 | 10          |
| 2          | H                   | 1992 | 14          |

This format makes it easy to run models like [fixed effects](https://lost-stats.github.io/Model_Estimation/fixed_effects.html). 

Reshaping is the method of converting wide-format data to long and [vice versa](https://lost-stats.github.io/Data_Manipulation/reshape_panel_data_from_long_to_wide.html)..

## Keep in Mind

- If your data has multiple observations per individual/time, then standard reshaping techniques generally won't work.
- It's a good idea to check your data by directly looking at it both before and after a reshape to check that it worked properly.

## Also Consider

- To go in the other direction, [reshape from long to wide](https://lost-stats.github.io/Data_Manipulation/Reshaping/reshape_panel_data_from_long_to_wide.html).
- [Determine the observation level of a data set](https://lost-stats.github.io/Data_Manipulation/determine_the_observation_level_of_a_data_set.html).

# Implementations

## R

There are many ways to reshape in R, including base-R `reshape` and the deprecated `reshape2::melt` and `cast` and `tidyr::gather` and `spread`. We will be using the **tidyr** package function `pivot_longer`, which requires **tidyr** version 1.0.0 or later.

```r
# install.packages('tidyr')
library(tidyr)

# Load in billboard, which has one row per song
# and one variable per week, for its chart position each week
data("billboard")

# If we look at the data, we'll see that we have:
# identifying information in "artist" and "track"
# A variable consistent within individuals "date.entered"
# and a bunch of variables containing position information
# all named wk and then a number
names(billboard)
```

Now we think:
1. Think about the set of variables that contain time-varying information. Here's it's `wk1-wk76`. So we can give a list of all the variables we want to widen using the `tidyselect` helper function `starts_with()`: `starts_with("wk")`. This list of variable names will be our `col` argument.
2. Think about what we want the new variables to be called. I'll call the week time variable "week" (this will be the `names_to` argument), and the data values currently stored in `wk1-wk76` is the "position" (`values_to`).
3. Think about the values you want to be in your new time variable. The column names are `wk1-wk76` but we want the variable to have 1-76 instead, so we'll take out the "wk" with `names_prefix = "wk"`.

```r
billboard_long <- pivot_longer(billboard,
                               col = starts_with("wk"),
                               names_to = "week",
                               names_prefix = "wk",
                               values_to = "position",
                               values_drop_na = TRUE)
# values_drop_na says to drop any rows containing missing values of position.
# If reshaping to create multiple variables, see the names_sep or names_pattern options.
```

## Stata

```stata
* Load blood pressure data in wide format, which contains
* bp_before and bp_after
sysuse bpwide.dta
```

The next steps involve thinking:
1. Think about the set of variables that identify individuals. Here it's `patient`. This will go in `i()`, so we have `i(patient)`.
2. Think about the set of variables that vary across time. Here's it's `bp_`. Note the inclusion of the `_`, so that "before" and "after" will be our time periods. This will be one of our "stub"s.
3. Think about what we want the new time variable to be called. I'll just call it "time", and this goes in `j()`, so we have `j(time)`.

```stata
* Syntax is:
* reshape long stub, i(individualvars) j(newtimevar)
* So we have
reshape long bp_ i(patient) j(time) s
* Where the s indicates that our time variable is a string ("before", "after")
* Note that simply typing 
reshape
* will show the syntax for the function
```

With especially large datasets, the [**Gtools**](https://gtools.readthedocs.io/en/latest/index.html) package provides a much faster version of reshape known as greshape. The syntax can function exactly the same, though they provide alternative syntax that you may find more intuitive. 

```stata
* If necessary, install gtools
* ssc install gtools

* First, we will create a toy dataset that is very large to demonstrate the speed gains 
* Clear memory
clear all 
* Turn on return message to see command run time
set rmsg on 
* Set data size to 15 million observations
set obs 15000000 
* Create an ID variable 
generate person_id = _n 

* Create 4 separate fake test scores per student 
generate test_score1 = round(rnormal(180, 30))
generate test_score2 = round(rnormal(180, 30))
generate test_score3 = round(rnormal(180, 30))
generate test_score4 = round(rnormal(180, 30))

* Demonstrate the comparative speed of these two Reshape approaches 
	
* The traditional reshape command
preserve 
reshape long test_score, i(person_id) j(test_number) 
restore 
	
*The Gtools reshape command  
preserve
greshape long test_score, i(person_id) j(test_number) 
restore 
	
*The Gtools reshape command, alternative syntax
preserve
greshape long test_score, by(person_id) keys(test_number)
restore 
```

Note: there is much more guidance to the usage of greshape on the [**Gtools** reshape page](https://gtools.readthedocs.io/en/latest/usage/greshape/index.html). 