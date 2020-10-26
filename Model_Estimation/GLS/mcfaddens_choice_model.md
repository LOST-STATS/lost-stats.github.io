---
title: McFadden's Choice Model (Alternative-Specific Conditional Logit)
parent: Generalised Least Squares
grand_parent: Model Estimation ## Optional for indexing
has_children: false
mathjax: true
nav_order: 1
---

# McFadden's Choice Model (Alternative-Specific Conditional Logit)

Discrete choice models are a regression method used to predict a categorical dependent variable with more than two categories. For example, a discrete choice model might be used to predict whether someone is going to take a train, car, or bus to work. 

McFadden's Choice Model is a discrete choice model that uses [conditional logit]({{ "/Model_Estimation/GLS/conditional_logit.html" | relative_url }}), in which the variables that predict choice can vary either at the individual level (perhaps tall people are more likely to take the bus), or at the alternative level (perhaps the train is cheaper than the bus).

For more information, see [Wikipedia: Discrete Choice](https://en.wikipedia.org/wiki/Discrete_choice)

## Keep in Mind

- Just like other regression methods, the McFadden model does not guarantee that the estimates will be causal. Similarly, while the McFadden model is designed so that the results can be interpreted in terms of a "random utility" function, making inferences about utility functions does require additional assumptions.
- The standard McFadden model assumes that the choice follows the [Independence of Irrelevant Alternatives](https://en.wikipedia.org/wiki/Independence_of_irrelevant_alternatives#In_econometrics), which may be a strong assumption. There are variants of the McFadden model that relax this assumption.
- If you are working with an estimation command that only allows alternative-specific predictors and not case-specific predictors, you can add them yourself by interacting the case-specific predictors with binary variables for the different alternatives. If $$Income$$ is your case-specific variable and your alternatives are "train", "bus", and "car", you'd add $$Income \times (mode == "train")$$, $$Income \times (mode == "bus")$$, and $$Income \times (mode == "car")$$ to your model. These are your case-specific predictors.
- Choice model regressions often have specific demands on how your data is structured. These vary across estimation commands and software packages. However, a common one is this (others will be pointed out in specific Implementations below): The data must contain a variable indicating the choice cases (i.e. you choose a car, that's one case, then I choose a car, that's a different case), a variable with the alternatives being chosen between, a binary variable equal to 1 for the alternative actually chosen (this should be 1 or `TRUE` exactly once within each choice case), and then variables that are case-specific or alternative-specific.

In the below table, $$I$$ gives the choice case, $$Alts$$ gives the options, $$Chose$$ gives the choice, $$X$$ is a variable that varies at the alternative level, and $$Y$$ is a variable that varies at the case level.

|I|Alts|Chose|X|Y|
|-|----|-----|-|-|
|1|A   | 1   |10|3|
|1|B   | 0   |20|3|
|1|C   | 0   |10.5|3|
|2|A   | 0   |8 |5|
|2|B   | 1   |9 |5|
|3|C   | 0   |1 |5|

This might be referred to as "long" choice data. "Wide" choice data is also common, and looks like:

|I|Chose|Y|XA|XB|XC|
|-|-----|-|--|--|--|
|1|A    |3|10|20|10.5|
|2|B    |5|8|9|1|

## Also Consider

- In order to relax the independence of irrelevant alternatives assumption and/or more closely model individual preferences, consider the [mixed logit]({{ "/Model_Estimation/Multilevel_Models/mixed_logit.html" | relative_url }}), [nested logit]({{ "/Model_Estimation/GLS/nested_logit.html" | relative_url }}) or [hierarchical Bayes conditional logit]({{ "/Model_Estimation/Multilevel_Models/hierarchical_bayes_conditional_logit.html" | relative_url }}) models.

# Implementations

## R

We will implement McFadden's choice model in R using the **mlogit** package, which can accept "wide" or "long" data in the `mlogit.data` function.

```R
# If necessary, install mlogit package
# install.packages('mlogit')
library(mlogit)

# Get Car data, in "wide" choice format
data(Car)


# For this we need to specify the choice variable with choice
# whether it's currently in wide or long format with shape
# the column numbers of the alternative-specific variables with varying.
# We need alt.levels to tell us what our alternatives are (1-6, as seen in choice).
# We also need sep = "" since our wide-format variable names are type1, type2, etc.
# If the variable names were type_1, type_2, etc., we'd need sep = "_".
# If this were long data we'd also want:
# the case identifier with id.var (for individuals) and/or chid.var 
# (for multiple choices within individuals)
# And a variable indicating the alternatives with alt.var
# But could skip the alt.levels and sep arguments
mlogit.Car <- mlogit.data(Car,
                          choice = 'choice',
                          shape = 'wide',
                          varying = 5:70,
                          alt.levels = 1:6,
                          sep="")
# mlogit.Car is now in "long" format
# Note that if we did start with "long" format we could probably skip the mlogit.data() step.

# Now we can run the regression with mlogit().
# We "regress" the choice on the alternative-specific variables like type, fuel, and price
# Then put a pipe separator | 
# and add our case-specific variables like college
model <- mlogit(choice ~ type + fuel + price | college, 
                data = mlogit.Car)

# Look at the results
summary(model)
```

## Stata

Stata has the McFadden model built in. We will estimate the model using the older `asclogit` command as well as the `cmclogit` command that comes with Stata 16. These commands require "long" choice data, as described in the Keep in Mind section.

```stata
* Load in car choice data
webuse carchoice

* To use asclogit, we "regress" our choice variable (purchase)
* on any alternative-specific variables (dealers)
* then we put our case ID variable consumerid in case()
* and our variable specifying alternatives, car, in alternatives()
* then finally we put any case-specific variables like gender and income, in casevars()
asclogit purchase dealers, case(consumerid) alternatives(car) casevars(gender income)


* To use cmclogit, we first declare our data to be choice data with cmset
* specifying our case ID variable and then the set of alternatives
cmset consumerid car

* Now that Stata knows the structure, we can omit those parts from the asclogit
* specification, but the rest stays the same!
cmclogit purchase dealers, casevars(gender income)
```

Why bother with the `cmclogit` version? `cmset` gives you a lot more information about your data, and makes it easy to transition between different choice model types, including those incorporating panel data (each person makes multiple choices).
