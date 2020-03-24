---
title: Creating Dummy Variables
parent: Data Manipulation
has_children: false
nav_order: 1
---

#Introduction

Creating a dummy variable can be just like creating any other variable but dummy variables can only take the value of 0 or 1. This gives us even more options in how we decide to add dummys. Below I walk through a few methods you can use to add dummy variables to your data.

## Keep in Mind

Factor class vectors are automatically treated as dummies in regression models in R (Stata and SW languages have similar capabilities). In order to transform a categorical vector to a factor class you can simply use `as.factor()`. This means you don't have to create a different dummy vector for every value. If you are interested in looking behind the scenes you can use `model.matrix()` to see how R is creating dummies from these factor class variables.

Note: `model.matrix()` creates a seperate dummy column for all values in the vector. This is called one-hot encoding and, if you aren't careful, can lead to the dummy variable trap. The dummy variable trap arises because of perfect multicolinearity between the intercept term and the dummy variables (which row-wise all add up to 1). So one of the columns needs to be dropped from the regression in order for it to run. Typically the first variable is the one which is dropped and effectively absorbed into the intercept term. If this happens then all the dummy estimates will be in reference to the dropped dummy. If you wish you can automatically drop the intercept term instead of a dummy by adding a 0 to your regression call i.e. `lm(formula = Sepal.Length ~ 0 + Species, data = iris)`.

# Implementations

## R

As I mentioned, creating a dummy variable doesn't have to be any different than creating any other variable. Below are several ways to create a new variable in R.

### dplyr::mutate

```r
# If necessary, install dplyr
# install.packages('dplyr')
library(dplyr)

# The below takes existing data (old_data) and adds
# a new variable (new_variable) based on an existing
# variable (variable_1) and saves the result as
# mutated_data.
# Note: new variables do not have to be based on old
# variables
mutated_data = old_data %>%
  mutate(new_variable = variable_1*10)
```

This page is about making dummy variables so let's say that we want our dummy to indicate if variable_1 > variable_2. To do this we can use `mutate` just like we did above.

```r
mutated_data = old_data %>%
  mutate(new_dummy = variable_1 > variable_2)
```

This will create a new column of logical (true/false) variables. This works just fine for most uses of dummy variables. However if you need the variables to be 1s and 0s you can now take

```r
mutated_data$new_dummy = mutated_data$new_dummy * 1
```

You could also nest that operation inside the original creation of new_dummy like so:

```r
mutated_data = old_data %>%
  mutate(new_dummy = (variable_1 > variable_2)*1)
```

Otherwise you could use an `ifelse` function to accomplish the same outcome:

```r
mutated_data = old_data %>%
  mutate(new_dummy = ifelse(variable_1 > variable_2, 1, 0))
```

### Base R

I used some base R above to wrangle the dummys from logical to numeric values, but it is worth noting that you can accomplish everything we just did in the **dplyr** in base R.

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

df$dummy = df$numbers%%2==1 *1

```

### Also Consider

There are many other methods one can use to create a dummy variable to add to some data. One could even create a vector of dummy variables and then merge that with an existing data set. That method is described in the article about horizontally combining data sets using functions like `join` and `merge`.

## MATLAB

In MATLAB you can store variables as columns in arrays. If you know you are going to add columns multiple times to the same array it is best practice to pre-allocate the final size of the array for computational efficiency. If you do this you can simply select the column you are designating for your dummy variable and story the dummys in that column.

```MATLAB
arr = [1,2,3;5,2,6;1,8,3];
dum = sum(data(:,:),2) <10;
data = horzcat(arr,dum);
```
In the above script I make a 3 by 3 array, then create a 3 x 1 array of dummy variables indicating if the sum of the rows are less than 10. Then I horizontally concatenate the arrays together. I should note that in MATLAB logicals are automatically stored as 1s and 0s instead of T/F like in R.


