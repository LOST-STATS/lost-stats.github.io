---
title: Propensity Score Matching
parent: Category
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

Propensity Score Matching(PSM) is a non-parametric method of estimating a treatment effect in situations where randomization is not possible. This method comes from [Rosenbaum & Rubin, 1983](https://www.jstor.org/stable/2335942?seq=1) and works by estimating a propensity score which is the predicted probability that someone received treatment based on the explanatory variables of interest. This reduces bias in observational studies by balancing the covariates between a group that received the treatment and a group that did not, essentially attempting to replicate a randomized control trial.


# Inverse Probability Weighting 

The recommendation of the current literature, by [King and Nielsen 2019](https://ideas.repec.org/a/cup/polals/v27y2019i04p435-454_00.html), is that propensity scores should be used for inverse probability weights (IPW) rather than matching. With this in mind, there will be examples of how to implement IPWs first followed by the process for implementing a matching method. 

# Workflow for Inverse Probability Weighting

Step One: 

Run a logistic regression where the outcome variable is a binary indicator for whether or not someone received the treatment and gather the predicted value of the propensity score. The explanatory variables in this case are the covariates that we might reasonably believe influence treatment

Step Two:

Filter out observations in our data which are not inside the range of our propensity scores.

Step Three:

Create the invere probability weights

Step Four:

Run a regression using the IPWs




# Workflow for Matching

Step One:

The same as step one from the IPW section. 

Step Two:

Match those that received treatment with those that did not based on propensity score. There are a number of different ways to perform this matching including, but not limited to :

*Nearest neighbor matching

*Exact matching

*Stratification matching

In this example we will focus on nearest neighor matching, which we will use through th MatchIt package


Step Three:

Check the balance of the matched sample using the summary command. This is good practice to ensure that the matching worked well and that the constructed control and treatment groups have similar observable characteristics.

Step Four;

Run analysis using this new sample which will give us an average treatment effect. 




## Keep in Mind

Propensity Score Matching is based on selection on observable characteristics. This assume that the potential outcome is independent of the treatment D conditional on the covariates. 
$Y_i(1),Y_i(0)\bot|X_i$

This is known as the Conditional Independence Assumption 

Propensity Score Matching also requires us to make the Common Support or Overlap Assumption.

$0<Pr(D_i = 1 | Xi = x)<1$

This assumption says that the probability that the treatment is equal to 1 for each level of x is between zero and one, or in other words there are both treated and untreated units for each level of x. 

Because Propensity Score Matching relies so heavily on these assumptions, [Regression Discontinuity](https://lost-stats.github.io/Model_Estimation/Research_Design/regression_discontinuity_design.html), [Differences in Differences](https://lost-stats.github.io/Model_Estimation/Research_Design/two_by_two_difference_in_difference.html), and other quasi-experimental designs may provide more accurate and robust results.




## Further Resouces

For more information about IPWs check out this [page](https://theeffectbook.net/ch-Matching.html?panelset3=r-code4#panelset3_r-code4) by Nick Huntinton-Klein.


A great place to find more information about the MatchIt package is on the package's [github site](https://github.com/kosukeimai/MatchIt). 

Noah Greifer's [Cran Page](https://cran.r-project.org/web/packages/MatchIt/vignettes/MatchIt.html) is another good resource for getting started using Propensity Score Matchign in R. 

Here is a handy link to get more information about the  [causalweight package](https://cran.r-project.org/web/packages/causalweight/vignettes/bodory-huber.pdf) which is an alternative way of creating the IPWs, courtesy of Hugo Bodory and Martin Huber.




## Implemenation of Inverse Probability Weights in R

Data comes from [OpenIntro.org](https://www.openintro.org/data/index.php?data=smoking)


```r
# R Code
# First follow basic workflow without causal weights package
library(pacman)
p_load(tidyverse)

#Load data on smoking in the United Kingdom.

smoking = read_csv("smoking.csv")

#Turn smoking into a numeric variable 
smoking = smoking %>%mutate(smoke = if_else(smoke == "Yes",1,0))

smoking

#Step One: Run the logistic regression.

ps_model = glm(smoke ~ gender+age+marital_status+ethnicity+region, data=smoking,
                family = binomial(link='logit'))

#Gather the predicted values for our propensity score.
smoking = smoking %>% 
  mutate(p_scores = predict(ps_model, type="response"))


#Step Two: Filter out observations in our data which are not inside the range of our propensity scores.


#Create min p_score value 
min_pscores = smoking%>%filter(smoke==1)%>%
  pull(p_scores)%>%
  min(na.rm = TRUE)


#Create max p_score value
max_pscores = smoking%>%filter(smoke==1)%>%
  pull(p_scores)%>%
  max(na.rm=TRUE)

#Create filtered dataset
smoking_filtered = smoking%>%filter(p_scores>=min_pscores, p_scores<=max_pscores)

#Create the IPWs.

smoking_filtered = smoking_filtered%>%
  mutate(ipw = case_when(
    smoke == 1 ~ 1/p_scores,
    smoke == 0 ~ 1/(1-p_scores)))


# IPWs to weight regression

#Create a new variable that is equal to 1 if person is married and 0 if not
smoking_filtered = smoking_filtered%>%mutate(married = if_else(marital_status=="Married",1,0))




##Regress treatment on outcome using weights
m1 = lm(married~ smoke, data=smoking_filtered, weights=ipw)




```

## Implementation of Matching in R

```r
# R Code
##load the packages we need.

p_load( MatchIt)

(smoke = if_else(smoke == "Yes",1,0))

##Step One: Run the logistic regression.

ps_model = glm( smoke ~ gender+age+marital_status+ethnicity+region, data=smoking)


##Step Two: Match on propensity score.

#Does not apply in this situation, but need to make sure there are no missing values in the covariates we are choosing. 

#In order to match use the matchit command, passing the function a formula, the data to use and the method, in this case, nearest neighor estimation.

Match = matchit(smoke ~ gender+age+marital_status+ethnicity+region, method = "nearest", data =smoking)

##Step Three: Check for Balance.
summary(match)

##Create data frame from matches using the match.data function.

match_data = match.data(match)


#Check the dimensions.
dim(match_data)


##Step Four: Conduct Analysis using the new sample.

##Turn marital status into a factor variable so that we can use it in our regression 
match_data = match_data %>% mutate(marital_status = as.factor(marital_status))


##We can now get the treatment effect of smoking on gross income with and without controls
lm_nocontrols = lm(marital_status ~ smoke, data= match_data)



#With controls
lm_controls =lm(marital_status ~ smoke+age+gender+ethnicity+marital_status, data=match_data)




```







