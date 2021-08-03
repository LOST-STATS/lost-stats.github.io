---
title: Ordered Probit/Logit
parent: Generalised Least Squares
grand_parent: Model Estimation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Ordered Probit / Ordered Logit

Ordered probit and ordered logit are regression methods intended for use when the dependent variable is *ordinal*. That is, there is a natural ordering to the different (discrete) values, but no cardinal value. So we might know $$A > B$$ but not *by how much* $$A$$ is greater than $$B$$.

Examples of ordinal data include responses on a Likert scale ("Very satisfied" is more satisfied than "Satisfied", and "Satisfied" is more satisfied than "Not Satisfied", but the difference between "Very satisfied" and "Satisfied" may not be the same as the difference between "Satisfied" and "Not Satisfied" but we may not know by how much) or education levels (a Master's degree is more education than a Bachelor's degree, but how much more?).

When the dependent variable is ordinal, typical linear regression may not work well because it relies on absolute differences in value. 

Ordered probit and ordered logit take a latent-variable approach to this problem. They assume that the discrete dependent variable simply represents a continuous latent variable. In the Likert scale example this might be "satisfied-ness". In ordered probit this latent variable is normally distributed, and in ordered logit it is distributed according to a logistic distribution. 

Then, the actual values just carve up the regions of that latent variable. So if satisfied-ness is distributed $$S\sim N(0,1)$$, then perhaps "very satisfied" is $$S > .892$$, "satisfied" is $.321 < S \leq .892$$, and so on. The .321 and .892 are "cutoff values" separating the categories. These cutoff values are estimated by ordered probit and ordered logit.

These models assume that predictors affect the latent variable the same no matter which level you're at. There isn't a predictor that, for example, makes you more likely to be "satified" and less likely to be either "very satisfied" *or* "not satisfied" (or a predictor that has a slight positive effect going from "not satisfied" to "satisfied" but a huge effect going from "satisfied" to "very sastisfied"). You can imagine taking your ordinal variable and collapsing it into a binary one: comparing, say, "very not satisfied" and "not satisfied" as one group vs. "satisfied" and "very satisfied" as the other in a typical probit or logit. Ordered logit/probit assumes that this will give the same results as if you'd split somewhere else, comparing "very not satisfied", "not satisfied", and "satisfied" vs. "very satisfied". This is the "parallel lines" or "parallel regression" assumption, or for ordered logit "proportional odds".

## Keep in Mind

- Coefficients on predictors are scaled in terms of the *latent variable* and in general are difficult to interpret. You can calculate marginal effects from ordered probit/logit results, which report how changes in a predictor are related to people moving from one category to another. For example, if the marginal effect of $$X$$ is +.03 for "very not satisfied", +.02 for "not satisfied", .+.02 for "satisfied", and -.07 for "very satisfied", that means that a one-unit increase in $$X$$ results in a drop in the proportion of the sample predicted to be "very satisfied" and that drop is reallocated across the other three levels, everyone shifting down a bit and some ending up in a new category.
- To identify the model, one of the cutoff parameters (the lowest one, separating the lowest category and the second-lowest) is usually fixed at 0. The cutoff values are in general only meaningful *relative to each other* for this reason and don't mean anything on their own. 
- It is a good idea to test the parallel lines assumption. This is commonly done using a [Brant (1990)](https://www.jstor.org/stable/2532457) test, which basically checks the different above/below splits possible with the dependent variable and sees how much the coefficients differ (hoping they don't differ a lot!). If the test fails, you may want to use a *generalized* ordered logit, which has less explanatory power but does not rely on the parallel trends assumption. Code for both these steps is below. Doing the test rather than just starting with generalized ordered logit is a good idea because you do lose power and interpretability with generalized ordered logit; see [Williams 2016](https://www3.nd.edu/~rwilliam/gologit2/UnderStandingGologit2016.pdf).

## Also Consider

- If the dependent variable is not ordered, consider a [multinomial model]({{ "/Model_Estimation/GLS/mcfaddens_choice_model.html" | relative_url }}) instead.


# Implementations

## R

The necessary tools to work with ordered probit and logit are unfortunately scattered across several packages in R. **MASS** contains the ordered probit/logit estimator, **brant** has the Brant test, and if that fails you're off to **VGAM** for generalized ordered logit.

```r
# For the ordered probit/logit model
library(MASS)
# For the brant test
library(brant)
# For the generalized ordered logit
library(VGAM)
# For marginal effects
library(erer)

# Data on marital happiness and affairs
# Documentation: https://vincentarelbundock.github.io/Rdatasets/doc/Ecdat/Fair.html
mar <- read.csv('https://vincentarelbundock.github.io/Rdatasets/csv/Ecdat/Fair.csv')

# See how various factors predict marital happiness
m <- polr(factor(rate) ~ age + child + religious + education + nbaffairs,
          data = mar, 
          method = 'logistic' # change to 'probit' for ordered probit
          )

summary(m)

# Brant test of proportional odds
brant(m)
# The "Omnibus" probability is .03, if we have alpha = .05 then we reject proportional odds
# Specifically the test tells us that education is the problem. Dang.

# We can use vglm for the generalized ordered logit
gologit <- vglm(factor(rate) ~ age + child + religious + education + nbaffairs,
                cumulative(link = 'logitlink', parallel = FALSE), # parallel = FALSE tells it not to assume parallel lines
                data = mar)
summary(gologit)                
# Notice how each predictor now has many coefficients - one for each level
# and we have other problems denoted in its warnings!

# If we want marginal effects for our original ordered logit...
ocME(m)
```

## Stata

Ordered logit / probit requires a few packages to be installed, including **gologit2** for the generalized ordered logit, and for the Brant test **spost13**, which is not on ssc.

```stata
* For the brant test we must install spost13 
* which is not on ssc, so do "findit spost13" and install "spost13_ado"
* for generalized ordered logit, do "ssc install gologit2"

* Data on marital happiness and affairs
* Documentation: https://vincentarelbundock.github.io/Rdatasets/doc/Ecdat/Fair.html
import delimited "https://vincentarelbundock.github.io/Rdatasets/csv/Ecdat/Fair.csv", clear

* strings can't be factors
encode child, g(child_n)

* Run ologit or oprobit
ologit rate age i.child_n religious education nbaffairs

* Use the brant test
brant
* The "All" probability is .03, if we have alpha = .05 then we reject proportional odds
* Specifically the test tells us that education is the problem. Dang.

* Running generalized ordered logit instead
gologit2 rate age i.child_n religious education nbaffairs
* Notice how each predictor now has many coefficients - one for each level
* and we have a negative predicted probability denoted in the warnings!

* We can get marginal effects for either model using margins
ologit rate age i.child_n religious education nbaffairs
margins, dydx(*)

gologit2 rate age i.child_n religious education nbaffairs
margins, dydx(*)
```
