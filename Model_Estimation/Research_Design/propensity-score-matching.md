---
title: Propensity Score Matching
parent: Research Design
grand_parent: Model Estimation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Propensity Score Matching

## Conceptual Basis

Drawing causal inferences from non-random, observational data faces a critical methodological challenge. Treatment and non-treatment groups are not equal in expectation so the observed differences in outcomes cannot be attributed to the treatment condition. Propensity score matching (PSM) method is intended to overcome this challenge. The big idea is: if we can find a set of covariates ($X_i$) that is determinant of whether a participant gets treated or not, we can estimate a treatment effect by using only the observations with identical value of $X_i$. In other words, the PSM approach is based on the conditional independence assumption, i.e., treatment is considered as good as random conditional on a known set of $X_i$.  

## The Matching Workflow

Thanks to Dr. David Liebowitz's causal inference in educational research [class](https://www.daviddliebowitz.com/teaching) at the University of Oregon, I learned the following steps to conduct PSM in practice: 

1. Investigate the selection process explicitly by fitting a "selection model". Specifically, fit a logistic regression model below with treatment group membership as the outcome variable and predictors you believe describe the process of selection. 

$$ D_i = \frac{1}{1 + e^{-X_i \theta_i}} $$

2. Use the fitted selection model to estimate the fitted probability of selection into treatment ($\hat{p}$) for each participant, store these propensity scores (estimated probabilities) into a new variable in your dataset. 

3. Stratify the sample using the propensity scores. A rule of thumb here is at least five strata (removing up to 90% of the observed bias). 

4. Within each stratum, check whether the balancing condition has been satisfied. If not, re-stratify (combining or splitting strata) or go back to re-specify your $X_i$ until balance is achieved.

5. Estimate the treatment effect within each stratum.

6. Average the estimated effects up.

## Keep in Mind

PSM is not a magic way to create treatment and control conditions out of non-random, observational data. You have to present evidence that the conditional independence assumption is met before you go ahead and use the approach. 

## Implementations

### R

An awesome tutorial of how to implement PSM in R by [Simon Ejdemyr](https://github.com/sejdemyr) can be found [here](https://sejdemyr.github.io/r-tutorials/statistics/tutorial8.html). Here is a simplified version of this implementation. It's worth noticing that, besides the simplification, a major change I've made is to use a different and arguably more intuitive plot to visualize the region of common support. Credit for this plot goes to Dr. Liebowitz.

Before everything, follow Simon Ejdemyr's instruction [here](https://github.com/sejdemyr/ecls) to obtain the data file, "ecls.csv". It takes approximately five minutes to store this data file in you local ready to be used during the following analysis.

To start with, let's call the below packages and read in the data (multiple ways to do this but I just put my code file "matching.R" and the data file "ecls.csv" in one folder and read in the data with the help of the **here** package).

```r 
if (!require("pacman")) install.packages("pacman")
pacman::p_load(dplyr, MatchIt, here)
here::i_am("matching.R")
ecls <- read.csv("ecls.csv")
```

The goal here is to estimate the effect of going to Catholic school ("treatment" condition) on student math achievement. The outcome variable is student standardized (mean = 0, sd = 1) math score, "c5r2mtsc_std", and the predictor variable is the Cathlic school indicator, "catholic". 

Remember from the above the big idea here is that if we can find an ideal set of covariates that is determinant of whether a student goes to Catholic school or not, we can estimate the causal effect by using only the observations that have identical value of these covariates. Keep in mind that in real world, selection of this set of covariates should be supported by methodological as well as practical evidence. For the simplicity of this short introduction, let's use only five covariates to predict the treatment group membership.

 - race_white: Is the student white (1) or not (0)?
 - p5hmage: Mother’s age
 - w3income: Family income
 - p5numpla: Number of places the student has lived for at least 4 months
 - w3momed_hsb: Is the mother’s education level high-school or below (1) or some college or more (0)?
 
Note that the treatment group membership, "catholic" is a binary variable, so we fit a logit model here using the glm() function.

```r 
ecls <- ecls %>% mutate(w3income_1k = w3income / 1000)
m_ps <- glm(catholic ~ race_white + w3income_1k + p5hmage + p5numpla + w3momed_hsb, family = binomial(), data = ecls)
summary(m_ps)
```

Next, we use the predict() function to generate the propensity score from the previous estimation and obtain a new dataframe that has two columns, propensity score, "pr_score", and treatment group membership, "catholic". 

```r
prs_df <- data.frame(pr_score = predict(m_ps, type = "response"),
                     catholic = m_ps$model$catholic)
head(prs_df)
```

It is helpful to plot the smoothed densities of the propensity score, the probability of going to Catholic school based on the selected five covariates, by whether the student in fact goes to Catholic school, then visually examine the region of common support. This information helps us to justify the matching approach being used later on as well as to make decisions on whether the selected set of covariates needs to change.  

```r
ggplot(prs_df, aes(pr_score, fill = as.factor(catholic))) + 
  geom_density(alpha=0.1) + 
  theme_pander(base_size = 12, 
               base_family = "Fira Sans Book") +
  xlab("Probability of Going to Catholic School") +
  scale_fill_discrete(name = "", labels = c("Non-Catholic School", "Catholic School")) 
```

An intuitive and simple method for estimating the treatment effect is to restrict the sample to have only observations within the region of common support, then to divide the restricted sample into five quintiles based on the propensity score, then within each quintile, estimate the mean difference in student math score by treatment status. 

The **MatchIt** package can help us to adopt a more complex method. This method is to find pairs of observations that have very similar propensity scores, but that differ in their treatment status. This **MatchIt** package estimates the propensity score in the background and then matches observations based on the method of choice (“nearest” in this case). Note that this package doesn't allow missing values so we delete observations with NAs first. 

```r
ecls_cov <- c('race_white', 'p5hmage', 'w3income', 'p5numpla', 'w3momed_hsb')
ecls_nomiss <- ecls %>%
  select(c5r2mtsc_std, catholic, one_of(ecls_cov)) %>%
  na.omit()
mod_match <- matchit(catholic ~ race_white + w3income + p5hmage + p5numpla + w3momed_hsb, method = "nearest", data = ecls_nomiss)
summary(mod_match)
```

Our last step for now is to create a data frame that has only the matched observations, then use OLS with/without covariates to estimate the effects of going to Catholic school on student math achievement.

```r
dta_m <- match.data(mod_match)

lm_treat1 <- lm(c5r2mtsc_std ~ catholic, data = dta_m)
summary(lm_treat1)

lm_treat2 <- lm(c5r2mtsc_std ~ catholic + race_white + p5hmage +
                  I(w3income / 10^3) + p5numpla + w3momed_hsb, data = dta_m)
summary(lm_treat2)
```
                    



