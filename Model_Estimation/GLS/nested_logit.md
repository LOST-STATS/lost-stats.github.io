---
title: "Nested Logit Model"
parent: Model Estimation
has_children: false
nav_order: 1
output: 
  html_document:
    keep_md: TRUE
mathjax: TRUE
---

A nested logistical regression (nested logit, for short) is a statistical method for finding a best-fit line when the the outcome variable $Y$ is a binary variable, taking values of 0 or 1. Logit regressions, in general, follow a [logistical distribution](https://en.wikipedia.org/wiki/Logistical_distribution) and restrict predicted probabilities between 0 and 1. 

Traditional logit models require that the [Independence of Irrelevant Alternatives(IIA)](https://en.wikipedia.org/wiki/Independence_of_irrelevant_alternatives) property holds for all possible outcomes of some process. Nested logit models differ by allowing 'nests' of outcomes that satisfy IIA within them, but not requiring that all outcomes jointly satisfy IIA.

For an example of violating the IIA property, see [Red Bus/Blue Bus Paradox.](https://en.wikipedia.org/wiki/Independence_of_irrelevant_alternatives#Criticisms_of_the_IIA_assumption)

For a more thorough theoretical treatment, see  [SAS Documentation: Nested Logit.](https://support.sas.com/documentation/cdl/en/etsug/66840/HTML/default/viewer.htm#etsug_mdc_sect032.htm)

<br>

## Keep in Mind

- Returned beta coefficients are not the marginal effects normally returned from an OLS regression. They are maximum likelihood estimations. A beta coefficient can not be interpreted as "a unit increase in $X$ leads to a $\beta$ unit change in the probability of $Y$."

- The marginal effect can be obtained by performing a transformation after you estimate. A rough estimation technique is to divide the beta coefficient by 4.

- Another transformation that may be helpful is the odds ratio. This value is found by raising $e$ to the power of the beta coefficient. $e^\beta$ can be interpreted as : the percentage change in likelihood of $Y$, given a unit change in $X$.

<br>

# Implementations

## R

R has multiple packages that can estimate a nested logit model. To show a simple example, we will use the `mlogit` package. 


```r
# Install mlogit and AER packages and load them.
# install.packages("mlogit","AER")
library("mlogit","AER")

# Load dataset TravelMode
data("TravelMode",package = "AER")



# Use the mlogit() function to run a nested logit estimation

# Here, we will predict what mode of travel individuals
# choose using cost and wait times

nestedlogit = mlogit(
  formula = choice~gcost+wait,
  data = TravelMode,
  ##The variable from which our nests are determined
  alt.var = 'mode',
  #The variable that dictates the binary choice
  choice = 'choice',
  #List of nests as named vectors
  nests = list(Fast = c('air','train'), Slow = c('car','bus')))


# The results

summary(nestedlogit)

# In this case, air travel is treated as the base level.
# others maximum likelihood estimators relative
# to air are reported as separate intercepts

# The elasticities for each cluster are displayed
# as iv:Fast and iv:Slow
```
Another set of more robust examples comes from [Kenneth Train and Yves Croissant](https://cran.r-project.org/web/packages/mlogit/vignettes/e2nlogit.html)

