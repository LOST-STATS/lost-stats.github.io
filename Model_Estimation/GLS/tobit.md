---
title: Tobit Regression
parent: Generalised Least Squares
grand_parent: Model Estimation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Tobit Regression


If you have ever encountered data that is censored in some way, then the Tobit method is worth a detailed look. Perhaps the measurement tools only detect at a minimum threashold or up until some maximum threshold, or there's a physical limitation or natural constraint that cuts off the range of outcomes. If the dependent variable has a limited range in any way, then an OLS regression will capture the relationship between variables with a cluster of zeros or maximums distorting the relationship. James Tobin's big idea was essentially to modify the likelihood function to represent the unequal sampling probability of observations depending if a latent dependent variable is smaller than or larger than that range. The Tobit model is also called a **Censored Regression Model** for this reason, as it allows flexility to account of either left or right side censorship. There is flexibility in the mathematics depending on how the censoring occurs. To learn more to match the mathematics/functional form to your practical application, wikipedia has a great page [here](https://en.wikipedia.org/wiki/Tobit_model) along with links to outside practical applications. 

**Para Español,** dale click en el siguiente enlance [aqui](https://sct.uab.cat/estadistica/sites/sct.uab.cat.estadistica/files/presentaciontobias.pdf). Estas notas tienen las lecciones importantes de esta pagina en Ingles. 

## Keep in Mind

- Tobit is used with **Censored Data**, which **IS NOT** the same as **Truncated Data** (see next section)
- Tobit can produce a kinked relationship after a zero cluster 
- Tobit can find the correct relationship underneath a maximum cluster
- For non-parametric tobit, you will need a CLAD operator (see link in next section)

## Also Consider

- If you are new to the concept of [limited dependent variables](https://en.wikipedia.org/wiki/Limited_dependent_variable) or [OLS Regression](https://en.wikipedia.org/wiki/Ordinary_least_squares), click these links.  
- Deciphering whether data is censored or truncated is important. If all observations are observed in "X" but the true value of "Y" isn't known outside some range, then it is **Censored**. At the Chernobyl disaster the radioactive isotope meter only read up until a maximum threshold, all areas ("X") are observed but the true value of the radioactive level ("Y") is right censored at a maximum. When there is not a full set of "X" observed, then data is **truncated**, or in other words, a censored Y value does not get it's input x observed thus the set {Y,X} is not complete. For more info try these [UH slides](https://www.bauer.uh.edu/rsusmel/phd/ec1-23.pdf) from Bauer School of Business (they also have relatively easily digestable theory). 
- The Tobit model type I (the main one people are talking about without specification) is really a morphed [maximum likelihood estimation](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation) of a [probit](https://en.wikipedia.org/wiki/Probit_model), more background from those links.  
- If you find yourself needing non-parametric form, you will need to use a CLAD operator as well as new variance estimation techniques, I recommend Bruce Hansen's from University of Wisconsin, notes [here](https://www.ssc.wisc.edu/~bhansen/718/NonParametrics9.pdf).

# Implementations

## R

We can use the **AER** package ([link](https://cran.r-project.org/web/packages/AER/index.html)) to run a tobit model in R.

```r
# install.packages("AER") # Install first if you don't have it yet
library(AER)

data("Affairs") # Use the "Affairs" dataset provided with AER

# Aside: this example replicates Table 22.4 in Greene (2003)

tob_mod1 = tobit(affairs ~ age + yearsmarried + religiousness + occupation + rating,
                 data = Affairs)
summary(tob_mod1)

# The default left- and right-hand side limts for the censored dependent variable
# are 0 and Inf, respectively. You might want to change these after inspecting your 
# data.
hist(Affairs$affairs
tob_mod2 = tobit(affairs ~ age + yearsmarried + religiousness + occupation + rating,
                 data = Affairs,
                 right = 4)        # RHS censored now at 4
summary(tob_mod2)
```

For another example check out M Clark's [Models by Example Page](https://m-clark.github.io/models-by-example/tobit.html).
