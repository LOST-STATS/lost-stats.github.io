---
title: Creating Categorical Variables
parent: Data Manipulation
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Creating Categorical Variables

Many variables are categorical in nature. Each observation takes one of a set list of values, which are mutually exclusive. We may want to create these variables from raw data, assigning the category based on the values of other variables.

For example, we may create a simplified four or five-category race variable based on a self-reported open-ended "race" question on a survey. Or we may want to create income bins based on splitting up a continuous variable.

This page will explore how to consider a set of conditions and assigning a category based on those conditions. For example, maybe everyone with a value of `birthplace == 'USA'` and `citizenship == 'USA'` is in the 'natural-born USA citizen' category.

## Keep in Mind

- Make sure that the categories you're going for are truly mutually exclusive, or you'll have to figure out what to do with overlaps later when you find them!

# Implementations

## Python

We can use the filtering operation in **pandas** to only assign the categorical value to the rows that satisfy the condition.

```python?example=catpy
import pandas as pd

# and purely for the dataset
import statsmodels.api as sm
mtcars = sm.datasets.get_rdataset('mtcars').data

# Now we go through each pair of conditions and group assignments,
# using loc to only send that group assignment to observations
# satisfying the given condition
mtcars.loc[(mtcars.mpg <= 19) & (mtcars.hp <= 123), 'classification'] = 'Efficient and Non-Powerful'
mtcars.loc[(mtcars.mpg > 19) & (mtcars.hp <= 123), 'classification'] = 'Inefficient and Non-Powerful'
mtcars.loc[(mtcars.mpg <= 19) & (mtcars.hp > 123), 'classification'] = 'Efficient and Powerful'
mtcars.loc[(mtcars.mpg > 19) & (mtcars.hp > 123), 'classification'] = 'Inefficient and Powerful'
```

There's another way to achieve the same outcome using *lambda functions*. In this case, we'll create a dictionary of pairs of classification names and conditions, for example `'Efficient': lambda x: x['mpg'] <= 19`. We'll then find the first case where the condition is true for each row and create a new column with the paired classification name.

```python?example=catpy
# Dictionary of classification names and conditions expressed as lambda functions
conds_dict = {
    'Efficient and Non-Powerful': lambda x: (x['mpg'] <= 19) & (x['hp'] <= 123),
    'Inefficient and Non-Powerful': lambda x: (x['mpg'] > 19) & (x['hp'] <= 123),
    'Efficient and Powerful': lambda x: (x['mpg'] <= 19) & (x['hp'] > 123),
    'Inefficient and Powerful': lambda x: (x['mpg'] > 19) & (x['hp'] > 123),
}

# Find name of first condition that evaluates to True
mtcars['classification'] = mtcars.apply(lambda x: next(key for
                                                       key, value in
                                                       conds_dict.items()
                                                       if value(x)),
                                        axis=1)
```
There's quite a bit to unpack here! `.apply(lambda x: ..., axis=1)` applies a lambda function rowwise to the entire dataframe, with individual columns accessed by, for example, `x['mpg']`. (You can apply functions on an index using `axis=0`.) The `next` keyword returns the next entry in a list that evaluates to true or exists (so in this case it will just return the first entry that exists). Finally, `key for key, value in conds_dict.items() if value(x)` iterates over the pairs in the dictionary and returns only the condition names (the 'keys' in the dictionary) for conditions (the 'values' in the dictionary) that evaluate to true.

## R

We will create a categorical variable in two ways, first using `case_when()` from the **dplyr** package, and then using the faster `fcase()` from the **data.table** package.

```r
library(dplyr)

data(mtcars)

mtcars <- mtcars %>%
  mutate(classification = case_when(
    mpg <= 19 & hp <= 123 ~ 'Efficient and Non-Powerful', # Here we list each pair of conditions and group assignments
    mpg > 19 & hp <= 123 ~ 'Inefficient and Non-Powerful',
    mpg <= 19 & hp > 123 ~ 'Efficient and Powerful',
    mpg > 19 & hp > 123 ~ 'Inefficient and Powerful'
  )) %>%
  mutate(classification = as.factor(classification)) # Storing categorical variables as factors often makes sense
```

Now, using `fcase()` in **data.table**, which has similar syntax to `case_when()` except it uses more commas instead of `~`.

```r
library(data.table)

data(mtcars)

mtcars <- as.data.table(mtcars)

mtcars[, classification := fcase(
  mpg <= 19 & hp <= 123, 'Efficient and Non-Powerful', # Here we list each pair of conditions and group assignments
  mpg > 19 & hp <= 123, 'Inefficient and Non-Powerful',
  mpg <= 19 & hp > 123, 'Efficient and Powerful',
  mpg > 19 & hp > 123, 'Inefficient and Powerful'
)]

# Storing categorical variables as factors often makes sense
mtcars[, classification := as.factor(classification)]
```

## Stata

There are several ways to turn conditionals into a categorical variable in Stata. However, the easiest way that requires learning the least lingo is just to use good ol' `replace` with `if`.

```stata
sysuse auto.dta, clear

* Use if on each step, including generate, so that
* observations that satisfy none of the conditions end up missing
g classification = "Efficient and Non-Powerful" if mpg <= 19 & gear_ratio <= 2.9
replace classification = "Inefficient and Non-Powerful" if mpg > 19 & gear_ratio <= 2.9
replace classification = "Efficient and Powerful" if mpg <= 19 & gear_ratio > 2.9
replace classification = "Inefficient and Powerful" if mpg > 19 & gear_ratio > 2.9
```
