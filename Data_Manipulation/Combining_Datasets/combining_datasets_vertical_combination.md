---
title: Vertical Combination
grand_parent: Data Manipulation ## Optional for indexing
parent: Combining Datasets
has_children:  false
nav_order: 1
---

# Combining Datasets: Vertical Combination

When combining two datasets that collect the same information about different people, they get combined vertically because they have variables in common but different observations. The result of this combination will more rows than the original dataset because it contains all of the people that are present in each of the original datasets. Here we combine the files based on the name or position of the columns in the dataset. It is a "vertical" combination in the sense that one set of observations gets added to the bottom of the other set of observations. 

# Keep in Mind 
- Vertical combinations require datasets to have variables in common to be of much use. That said, it may not be necessary for the two datasets to have exactly the same variables. Be aware of how your statistical package handles observations for a variable that is in one dataset but not another (e.g. are such observations set to missing?). 
- It may be the case that the datasets you are combining have the same variables but those variables are stored differently (numeric vs. string storage types). Be aware of how the variables are stored across datasets and how your statistical package handles attempts to combine the same variable with different storage types (e.g. Stata throws an error and will now allow the combination, unless the ", force" option is specified.) 

# Implementations

## Python

`pandas` is by far the most widely-used library for data manipulation in python. The `concat` function concatenates datasets vertically and combines datasets even if they don't contain the exact same set of variables. It's also possible to concatenate dataframes horizontally by passing the function the keyword argument `axis=1`.

```python
import pandas as pd

# Load California Population data from the internet
df_ca = pd.read_stata('http://www.stata-press.com/data/r14/capop.dta')
df_il = pd.read_stata('http://www.stata-press.com/data/r14/ilpop.dta')

# Concatenate a list of the dataframes (works on any number of dataframes)
df = pd.concat([df_ca, df_il])

```

## R

There are several ways to vertically combine data sets in R, including `rbind`. We will use the **dplyr** package function `bind_rows`, which allows the two data sets to combine even if they don't contain the exact same set of variables.

```r
# If necessary, install dplyr
# install.packages('dplyr')
library(dplyr)

# Load in mtcars data
data(mtcars)

# Split it in two, so we can combine them back together
mtcars1 <- mtcars[1:10,]
mtcars2 <- mtcars[11:32,]

# Use bind_rows to vertically combine the data sets
mtcarswhole <- bind_rows(mtcars1, mtcars2)
```

## Stata

```stata
* Load California Population data
webuse http://www.stata-press.com/data/r14/capop.dta // Import data from the web 

append using http://www.stata-press.com/data/r14/ilpop.dta // Merge on Illinois population data from the web 
```
You can also append multiple datasets at once, by simply listing both datasets separated by a space: 

```stata
* Load California Population data
* Import data from the web 
webuse http://www.stata-press.com/data/r14/capop.dta 

* Merge on Illinois and Texas population data from the web 
append using http://www.stata-press.com/data/r14/ilpop.dta http://www.stata-press.com/data/r14/txpop.dta 
```
Note that, if there are columns in one but not the other of the datasets, Stata will still append the two datasets, but observations from the dataset that did not contain those columns will have their values for that variable set to missing. 

```stata
* Load Even Number Data 
webuse odd.dta, clear 

append using http://www.stata-press.com/data/r14/even.dta 

```
