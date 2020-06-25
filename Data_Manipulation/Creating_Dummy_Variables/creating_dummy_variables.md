---
title: Creating Dummy Variables
parent: Data Manipulation
has_children: false
nav_order: 1
---

# Introduction

Creating a dummy variable can be just like creating any other variable but dummy variables can only take the value of 0 or 1 (or false or true). This gives us even more options in how we decide to add dummies. Dummy variables are often used as a way of including categorical variables in a model.

## Keep in Mind

Factor class vectors are automatically treated as dummies in regression models in R (Stata and SW languages have similar capabilities). In order to transform a categorical vector to a factor class you can simply use `factor()` on the variable in regression in R, or `i.` in Stata. This means you don't have to create a different dummy vector for every value. If you are interested in looking behind the scenes you can use `model.matrix()` to see how R is creating dummies from these factor class variables.

Note: `model.matrix()` creates a separate dummy column for all values in the vector. This is called one-hot encoding and, if you aren't careful, can lead to the dummy variable trap if an intercept is also included in the regression. The dummy variable trap arises because of perfect multicollinearity between the intercept term and the dummy variables (which row-wise all add up to 1). So one of the columns needs to be dropped from the regression in order for it to run. Typically, the first variable is the one which is dropped and effectively absorbed into the intercept term. If this happens then all the dummy estimates will be in reference to the dropped dummy. 

# Implementations

## Python

Several python libraries have functions to turn categorical variables into dummies, including **pandas**, **scikit-learn** (where it is called `OneHotEncoder`), and **statsmodels** (where it is called `categorical`). This example uses **pandas** `get_dummies` function.

```python
import pandas as pd

# Create a dataframe
df = pd.DataFrame({'colors': ['red', 'green', 'blue', 'red', 'blue'], 
                   'numbers': [5, 13, 1, 7, 5]})

# Replace the colors column with a dummy column for each color
df = pd.get_dummies(df, columns=['colors'])
```

## R

Turning a categorical variable into a set of dummies

```r
data(iris)

# To retain the column of dummies for the first 
# categorical value we remove the intercept
model.matrix(~-1+Species, data=iris)

# Then we can add the dummies to the original data
iris <- cbind(iris, model.matrix(~-1+Species, data=iris))

# Of course, in a regression we can skip this process
summary(lm(Sepal.Length ~ Petal.Length + Species, data = iris))
```

If you are only creating one dummy at a time rather than a set from a factor variable, creating a dummy variable doesn't have to be any different than creating any other variable. Below are several ways to create a new variable in R.

### dplyr::mutate

Let's say that we want our dummy to indicate if variable_1 > variable_2. To do this we can use `mutate`:

```r
# If necessary, install dplyr
# install.packages('dplyr')
library(dplyr)

data(iris)

# The below takes existing data (iris) and adds
# a new variable (Long.Petal) based on existing variables
# (Petal.Length and Petal.Width) and saves the result as
# mutated_data.
# Note: new variables do not have to be based on old
# variables
mutated_data = iris %>%
  mutate(Long.Petal = Petal.Length > Petal.Width)
```

This will create a new column of logical (`TRUE`/`FALSE`) variables. This works just fine for most uses of dummy variables. However if you need the variables to be 1s and 0s you can now take

```r
mutated_data <- mutated_data %>%
    mutate(Long.Petal = Long.Petal*1)
```

You could also nest that operation inside the original creation of new_dummy like so:

```r
mutated_data = iris %>%
  mutate(Long.Petal = (Petal.Length > Petal.Width)*1)
```

### Base R

```r
#the following creates a 5 x 2 data frame
letters = c("a","b","c", "d", "e")
numbers = c(1,2,3,4,5)
df = data.frame(letters,numbers)
```

Now I'll show several different ways to create a dummy indicating if the numbers variable is odd.

```r
df$dummy = df$numbers%%2

df$dummy = ifelse(df$numbers%%2==1,1,0)

df$dummy = df$numbers%%2==1

# the last one created a logical outcome to convert to numerical we can either

df$dummy = df$dummy * 1

# or

df$dummy = (df$numbers%%2==1) *1

```

## MATLAB

### Categorical to Dummy

The equivalent of `model.matrix()` in MATLAB is `dummyvar` which creates columns of one-hot encoded dummies from categorical variables. The following example is taken from MathWorks documentation.

```MATLAB
Colors = {'Red';'Blue';'Green';'Red';'Green';'Blue'};
Colors = categorical(Colors);

D = dummyvar(Colors)
```

### Other Dummies

In MATLAB you can store variables as columns in arrays. If you know you are going to add columns multiple times to the same array it is best practice to pre-allocate the final size of the array for computational efficiency. If you do this you can simply select the column you are designating for your dummy variable and story the dummys in that column.

```MATLAB
arr = [1,2,3;5,2,6;1,8,3];
dum = sum(data(:,:),2) <10;
data = horzcat(arr,dum);
```
In the above script I make a 3 by 3 array, then create a 3 x 1 array of dummy variables indicating if the sum of the rows are less than 10. Then I horizontally concatenate the arrays together. I should note that in MATLAB logicals are automatically stored as 1s and 0s instead of T/F like in R.

## Stata

In Stata, if we have a categorical variable stored as a number, we can use `i.` to turn it into a set of dummies, or include it directly in a regression.

```stata
sysuse auto.dta, clear

* Let's get the brand of the car
g brand = word(make,1)

* Turn it into a numerically coded categorical
encode brand, g(brand_n)

* include in a regression
regress mpg weight i.brand_n

* Or create a set of dummies
* specifying the prefix so it's easy to refer to
* Note this actually does not require 
* numeric encoding
xi i.brand, pre(b_)

regress mpg weight b_*


* Create a logical variable
gen highmpg = mpg > 30
```
