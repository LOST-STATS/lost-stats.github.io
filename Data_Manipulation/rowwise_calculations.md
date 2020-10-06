---
title: Rowwise Calculations
parent: Data Manipulation
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Rowwise Calculations

When working with a table of data, it's not uncommon to want to perform a calculations across many columns. For example, taking the mean of a bunch of columns for each row.

This is generally not difficult to do by hand if the number of variables being handled is small. For example, in most software packages, you could take the mean of columns `A` and `B` for each row by just asking for `(A+B)/2`.

This becomes more difficult, though, when the list of variables gets too long to type out by hand, or when the calculation doesn't play nicely with being given columns. In these cases, approaches explicitly designed for rowwise calculations are necessary.

## Keep in Mind

- When incorporating lots of variables, rowwise calculations often allow you to select those variables by group, such as "all variables starting with r_". When doing this, check ahead of time to make sure you aren't accidentally incorporating unintended variables.

# Implementations

## Python

The [**pandas**](https://pandas.pydata.org/) data analysis package provides several methods for performing row-wise (or column-wise) operations in Python. Many common operations, such as sum and mean, can be called directly (eg summing over multiple columns to create a new column). It's useful to know the axis convention in pandas: operations that combine columns often require the user to pass `axis=1` to the function, while operations that combine rows require `axis=0`. This convention follows the usual one for matrices of denoting individual elements first by the *i*th row and then by the *j*th column.
Although not demonstrated in the example below, [lambda](https://www.analyticsvidhya.com/blog/2020/03/what-are-lambda-functions-in-python/) functions can be used for more complex operations that aren't built-in and apply to multiple rows or columns.

```python
# If necessary, install pandas using pip or conda
import pandas as pd

# Grab the data
df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/ggplot2/midwest.csv",
                 index_col=0)

# Let's assume that we want to sum, row-wise, every column
# that contains 'perc' in its column name and check that
# the total is 300. Use a list comprehension to get only
# relevant columns, sum across them (axis=1), and create a
# new column to store them:
df['perc_sum'] = df[[x for x in df.columns if 'perc' in x]].sum(axis=1)

# We can now check whether, on aggregate, each row entry of this new column
# is 300 (it's not!)
df['perc_sum'].describe()

```

## R

There are a few ways to perform rowwise operations in R. If you are summing the columns or taking their mean, `rowSums` and `rowMeans` in base R are great. 

For something more complex, `apply` in base R can perform any necessary rowwise calculation, but `pmap` in the `purrr` package is likely to be faster.

In all cases, the **tidyselect** helpers in the **dplyr** package can help you to select many variables by name.

```r
# If necessary
# install.packages(c('purrr','ggplot2','dplyr'))
# ggplot2 is only for the data
data(midwest, package = 'ggplot2')
# dplyr is for the tidyselect functions, the pipe %>%, and select() to pick columns
library(dplyr)

# There are three sets of variables starting with "perc" - let's make sure they
# add up to 300 as they maybe should
# Use starts_with to select the variables

# First, do it with rowSums, 
# either by picking column indices or using tidyselect
midwest$rowsum_rowSums1 <- rowSums(midwest[,c(12:16,18:20,22:26)])
midwest$rowsum_rowSums2 <- midwest %>%
  select(starts_with('perc')) %>%
  rowSums()

# Next, with apply - we're doing sum() here for the function
# but it could be anything
midwest$rowsum_apply <- apply(
  midwest %>% select(starts_with('perc')), 
  MARGIN = 1, 
  sum)

# Next, two ways with purrr:
library(purrr)
# First, using purrr::reduce, which is good for some functions like summing
# Note that . is the data set being sent by %>%
midwest <- midwest %>%
  mutate(rowsum_purrrReduce = reduce(select(., starts_with('perc')), `+`))

# More flexible, purrr::pmap, which works for any function
# using pmap_dbl here to get a numeric variable rather than a list
midwest <- midwest %>%
  mutate(rowsum_purrrpmap = pmap_dbl(
    select(.,starts_with('perc')),
    sum))

# So do we get 300?
summary(midwest$rowsum_rowSums2)
# Uh-oh... looks like we didn't understand the data after all.
```

## Stata

Stata has a series of built-in row operations that use the `egen` command. See `help egen` for the full list, and look for functions beginning with `row` like `rowmean`. 

The full list includes: `rowfirst` and `rowlast` (first or last non-missing observation), `rowmean`, `rowmedian`, `rowmax`, `rowmin`, `rowpctile`, and `rowtotal` (the mean, median, max, min, given percentile, or sum of all the variables), and `rowmiss` and `rownonmiss` (the count of the number of missing or nonmissing observations across the variables).

The **egenmore** package, which can be installed with `ssc install egenmore`, adds `rall`, `rany`, and `rcount` (checks a condition for each variable and returns whether all are true, any are true, or the number that are true), `rownvals` and `rowsvals` (number of unique values for numeric and string variables, respectively), and `rsum2` (`rowtotal` with some additional options).

```stata
* Get data on midwestern states
import delimited using "https://vincentarelbundock.github.io/Rdatasets/csv/ggplot2/midwest.csv"

* There are three sets of variables starting with "perc" - let's make sure they
* add up to 300 as they should
* Use * as a wildcard for variable names
egen total_perc = rowtotal(perc*)

summ total_perc
* They don't! Uh oh.

* Let's just check the education variables - should add up to 100
* Use - to include all variables from one to the other
* based on their current order in the data
egen total_ed = rowtotal(perchsd-percprof)

* Oh that explains it...
* These aren't exclusive categories (HSD, college overlap)
* and also leaves out non-HS graduates.
summ total_ed
```
