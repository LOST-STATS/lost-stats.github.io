---
title: Propensity Score Matching
parent: Matching
grand_parent: Model Estimation
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Propensity Score Matching

Propensity Score Matching (PSM) is a non-parametric method of estimating a treatment effect in situations where randomization is not possible. This method comes from [Rosenbaum & Rubin, 1983](https://www.jstor.org/stable/2335942?seq=1) and works by estimating a propensity score which is the predicted probability that someone received treatment based on the explanatory variables of interest. As long as all confounders are included in the propensity score estimation, this reduces bias in observational studies by controlling for variation in treatment that is driven by confounding, essentially attempting to replicate a randomized control trial.

## Inverse Probability Weighting 

The recommendation of the current literature, by [King and Nielsen 2019](https://ideas.repec.org/a/cup/polals/v27y2019i04p435-454_00.html), is that propensity scores should be used with inverse probability weighting (IPW) rather than matching. With this in mind, there will be examples of how to implement IPWs first followed by the process for implementing a matching method. 

## Workflow for Inverse Probability Weighting

1. Run a logistic regression where the outcome variable is a binary indicator for whether or not someone received the treatment, and gather the predicted value of the propensity score. The explanatory variables in this case are the covariates that we might reasonably believe influence treatment
2. Filter out observations in our data that are not inside the range of our propensity scores, or that have extremely high or low values.
3. Create the inverse probability weights
4. Run a regression using the IPWs

## Workflow for Matching

1. The same as step one from the IPW section. 
2. Match those that received treatment with those that did not based on propensity score. There are a number of different ways to perform this matching including, but not limited to :

* Nearest neighbor matching
* Exact matching
* Stratification matching

In this example we will focus on nearest neighor matching.

## Checking Balance

Unlike methods like [Entropy Balancing]({{ "/Model_Estimation/Matching/entropy_balancing.html" | relative_url }}) and [Coarsened Exact Matching]({{ "/Model_Estimation/Matching/coarsened_exact_matching.html" | relative_url }}), propensity score approaches do not ensure that the covariates are balanced between the treated and control groups. It is a good idea to check whether decent balance has been achieved, and if it hasn't, go back and modify the model, perhaps adding more matching variables or allowing polynomial terms in the logistic regression, until there is acceptable balance.

1. Check the balance of the matched sample. That is, see whether the averages (and perhaps variances and other summary statistics) of the covariates are similar in the matched/weighted treated and control groups.
2. In the case of inverse probability weighting, also check whether the post-weighting propensity score distributions are similar in the treated and control groups.

Once the workflow is finished, the treatment effect can be estimated using the treated and matched sample with matching, or using the weighted sample with inverse probability weighting. 

## Keep in Mind

- Propensity Score Matching is based on selection on observable characteristics. This assume that the potential outcome is independent of the treatment D conditional on the covariates, or the Conditional Independence Assumption:

$$Y_i(1),Y_i(0)\bot|X_i$$

- Propensity Score Matching also requires us to make the Common Support or Overlap Assumption: 

$$0<Pr(D_i = 1 | Xi = x)<1$$

The overlap assumption says that the probability that the treatment is equal to 1 for each level of x is between zero and one, or in other words there are both treated and untreated units for each level of x. 

- Treatment effect estimation will produce incorrcect standard errors unless they are specifically tailored for matching results, since they will not account for noise in the matching process. Use software designed for treatment effect estimates with matching. Or, for inverse probability weighting, you can bootstrap the entire procedure (from matching to estimation) and produce standard errors that way.

# Implementations

## R

The matching implementation will use the **MatchIt** package. A great place to find more information about the MatchIt package is on the package's [github site](https://github.com/kosukeimai/MatchIt) or [CRAN Page](https://cran.r-project.org/web/packages/MatchIt/vignettes/MatchIt.html).

The inverse probability implementation uses the **causalweight** package. Here is a handy link to get more information about the  [causalweight package](https://cran.r-project.org/web/packages/causalweight/vignettes/bodory-huber.pdf) which is an alternative way of creating inverse probability weights, courtesy of Hugo Bodory and Martin Huber.

### Inverse Probability Weights in R

Data comes from [OpenIntro.org](https://www.openintro.org/data/index.php?data=smoking)

```r
# First follow basic workflow without causalweights package
library(pacman)
p_load(tidyverse, causalweight)

#Load data on smoking in the United Kingdom.
smoking = read_csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Model_Estimation/Matching/Data/smoking.csv")

#Turn smoking and married into numeric variables
smoking = smoking %>% mutate(smoke = 1*(smoke == "Yes"),
                              married = 1*(marital_status == "Married"))

# Pull out the variables
# Outcome
Y = smoking %>% pull(married)
# Treatment
D <- smoking %>% pull(smoke)
# Matching variables
X <- model.matrix(~-1+gender+age+marital_status+ethnicity+region, data = smoking)

# Note this estimats the propensity score for us, trims propensity 
# scores based on extreme values,
# and then produces appropriate bootstrapped standard errors
IPW <- treatweight(Y, D, X, trim = .001, logit = TRUE)

# Estimate and SE
IPW$effect
IPW$se
```

### Matching in R

```r
##load the packages and data we need.
library(pacman)
p_load(tidyverse, MatchIt)

smoking = read_csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Model_Estimation/Matching/Data/smoking.csv")

smoking = smoking %>% mutate(smoke = 1*(smoke == "Yes"))

##Step One: Run the logistic regression.

ps_model = glm(smoke ~ gender+age+marital_status+ethnicity+region, data=smoking)

##Step Two: Match on propensity score.
#Does not apply in this situation, but need to make sure there are no missing values in the covariates we are choosing. 
#In order to match use the matchit command, passing the function a formula, the data to use and the method, in this case, nearest neighor estimation.
Match = matchit(smoke ~ gender+age+marital_status+ethnicity+region, method = "nearest", data =smoking)

##Step Three: Check for Balance.
summary(match)

##Create a data frame from matches using the match.data function.
match_data = match.data(match)

#Check the dimensions.
dim(match_data)

##Step Four: Conduct Analysis using the new sample.
##Turn marital status into a factor variable so that we can use it in our regression 
match_data = match_data %>% mutate(marital_status = as.factor(marital_status))

##We can now get the treatment effect of smoking on gross income with and without controls
# Note these standard errors will be incorrect, see Caliendo and Kopeinig (2008) for fixes
# https://onlinelibrary.wiley.com/doi/full/10.1111/j.1467-6419.2007.00527.x
lm_nocontrols = lm(marital_status ~ smoke, data= match_data)

#With controls, standard errors also wrong here
lm_controls =lm(marital_status ~ smoke+age+gender+ethnicity+marital_status, data=match_data)
```
