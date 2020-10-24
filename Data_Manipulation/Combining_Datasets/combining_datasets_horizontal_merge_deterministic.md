---
title: Horizontal Combination (Deterministic)
grand_parent: Data Manipulation ## Optional for indexing
parent: Combining Datasets
has_children:  false
nav_order: 2
---

# Combining Datasets: Horizontal Combination (Deterministic)

A deterministic merge is when there is some variable(s) that uniquely and dependably identifies individual units (be it people, firms, teams, etc.) across datasets. For example, we might have two datasets containing information about the same set of people, one with their financial information, the other with their educational information. To analyze the relationship between the education and financial measures, we need them in the same dataset and so would want to combine them. If both datasets had a unique identification field for each person, such as a social security number or other national id, we could use this to match the records, so that all information from the same person appeared on the same line.

Because we expect such identifiers to be unique to an individual (unlike many names, such as John Smith) and appear exactly the same in each dataset, we can use just this field to do the match, and don’t anticipate in ambiguity in determining which records match to each other. Thus, it is a deterministic merge. 

# Keep in mind
- For any number of reasons, one or both of the datasets may have more than one observation per unit or individual. That may be for a good reason -- such as havinng multiple test scores for the same student because they took exams at different points in time -- or it may be redundant information. Understanding the structure of your data is key before embarking on a deterministic merge. 
- It is a good idea to have a clear sense of how much overlap you anticipate across your datasets. It is important to examine the results of your merge and see if it matches the amount the overlap you expected. Subtle differences in a matching variable (e.g. if leading zeroes are present in an ID variable for one variable but not another) can be a source of major headaches for your analysis if not caught early. If something looks weird in your results later in the project, trouble with a merge is a common cause. So check your merge results early and often. 

# Also Consider

- [Determine the observation level of a data set]({{ "/Data_Manipulation/determine_the_observation_level_of_a_data_set.html" | relative_url }}).

# Implementations

## Python

There are three main ways to join datasets horizontally in python using the `merge` function in **pandas**: one-to-one joins (e.g. two DataFrames joined on unique indexes), many-to-one joins (e.g. joining a unique index to one or more columns in a different DataFrame), and many-to-many joins (joining columns on columns). The column(s) to use as keys for the merge are specified with the `on=` keyword argument. The merges are different depending on if the merge is `inner` (use only those keys in both DataFrames), `outer` (use the cartesian product of all keys), `left` (use only keys in the left DataFrame), or `right` (use only keys in the right DataFrame). Outer joins will include entries for all possible combinations of columns. Further details can be found in the [**pandas** documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html#brief-primer-on-merge-methods-relational-algebra).

```python
import pandas as pd

gdp_2018 = pd.DataFrame({'country': ['UK', 'USA', 'France'],
                         'currency': ['GBP', 'USD', 'EUR'],
                         'gdp_trillions': [2.1, 20.58, 2.78]})

dollar_value_2018 = pd.DataFrame({'currency': ['EUR', 'GBP', 'YEN', 'USD'],
                                  'in_dollars': [1.104, 1.256, .00926, 1]})

# Perform a left merge, which discards 'YEN'
GDPandExchange = pd.merge(gdp_2018, dollar_value_2018, how='left', on='currency')
```

## R

There are several ways to combine data sets horizontally in R, including base-R `merge` and several different approaches in the **data.table** package. We will be using the `join` functions in the **dplyr** package.

```r
# If necessary, install dplyr
# install.packages('dplyr')
library(dplyr)

# This data set contains information on GDP in local currency
GDP2018 <- data.frame(Country = c("UK", "USA", "France"),
                  Currency = c("Pound", "Dollar", "Euro"),
                  GDPTrillions = c(2.1, 20.58, 2.78))
# This data set contains dollar exchange rates
DollarValue2018 <- data.frame(Currency = c("Euro", "Pound", "Yen", "Dollar"),
                              InDollars = c(1.104, 1.256, .00926, 1))
```

Next we want to join together `GDP2018` and `DollarValue2018` so we can convert all the GDPs to dollars and compare them. There are three kinds of observations we could get - observations in `GDP2018` but not `DollarValue2018`, observations in `DollarValue2018` but not `GDP2018`, and observations in both. Use `help(join)` to pick the variant of `join` that keeps the observations we want. The "Yen" observation won't have a match, and we don't need to keep it. So let's do a `left_join` and list `GDP2018` first, so it keeps matched observations, plus any observations only in `GDP2018`.

```r
GDPandExchange <- left_join(GDP2018, DollarValue2018)
```

The `join` function will automatically detect that the `Currency` variable is shared in both data sets and use it to join them. Generally, you will want to be sure that the set of variables you are joining by uniquely identifies observations in at least one of the data sets you are joining. If you're not sure whether that's true, see [Determine the observation level of a data set]({{ "/Data_Manipulation/determine_the_observation_level_of_a_data_set.html" | relative_url }}), or run `join` through the `safe_join` from the **pmdplyr** package.

## Stata 

**A Quick Prelude About “Master” And “Using” Datasets**

When merging two datasets together, there are two relevant datasets to consider. The first is the one currently in Stata’s memory, the other is whatever dataset (not currently loaded into Stata) that you would like to merge onto the dataset in memory. For ease of reference, Stata calls the dataset in memory the “master” dataset and the other file the “using” dataset. When you see the syntax of the merge command, the reason for calling it the “using” dataset will become clear. 



### In Stata, there are 3 types of deterministic merges: 

#### 1-to-1 

A one-to-one merge expects there to be no more than one row in each dataset to have a	matched pair in the other dataset. If there is more than one observation with the same identifying variable(s) in either the master or using datasets when attempting to do a one-to-one merge, Stata will throw an error. (Note: you can check to see if there is more than one observation per identifying variable by using the “duplicates report” command, or the Gtools variant for especially large datasets, called “gduplicates report.”) 

```stata
*Import Data with Car Sizes and Merge it to Data on Car Prices using the ID variable “Make”
webuse autosize.dta, clear 
	
merge 1:1 make using http://www.stata-press.com/data/r14/autoexpense.dta 
```

Note that the syntax specifies “make” as the identifying variable after the merge type (1:1) and before the using statement (thus why we call the data not in memory the “using” data. The result of this merge shows 5 successful matches and one observation from the master dataset that did not have a match. 

   | Result          |                # of obs. | _merge value            |
   |-----------------|--------------------------|-------------|
   | not matched from master|                        1 |(_merge==1)  |
   | not matched from using|                        0 |(_merge==2)  |
   |                 |                          |             |
   | matched         |                        5 |(_merge==3)  |

Note that Stata creates a new variable (_merge) during the merge that stores the merge status of each observation, where a value of 1 means that the observation was only found in the master dataset, 2 means it was found only in the using dataset, and 3 means it was found in both and successfully merged. 

#### Many-to-1

A many-to-one merge occurs when the master dataset contains multiple observations of the same unit or individual (say, multiple test scores for the same student), while the using dataset has only one observation per unit or individual (say, the age of each student). Here is the syntax for a many-to-1 merge. 

```stata
*Import Data with Car Sizes and Merge it to Data on Car Prices using the ID variable “Make”
webuse sforce.dta, clear 
	
merge m:1 region using http://www.stata-press.com/data/r14/dollars.dta
```
Note that in this case that the syntax changes from merge 1:1 to merge m:1 where m stands for many. In this case, the identifying variable is "region." 

#### 1-to-Many 

A one-to-many merge is the opposite of a many to one merge, with multiple observations for the same unit or individual in the using rather than the master data. The only different in the syntax is that it becomes merge 1:m rather than merge m:1. 

#### Many-to-Many

A many-to-many merge is intended for use when there are multiple observations for each combination of the set of merging variables in both master and using data. However, `merge m:m` has strange behavior that is effectively never what you want, and it is not recommended.
