---
title: Regression Discontinuity Design
parent: Research Design
grand_parent: Model Estimation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Regression Discontinuity Design

Regression discontinuity (RDD) is a research design for the purposes of causal inference. It can be used in cases where treatment is assigned based on a cutoff value of a "running variable". For example, perhaps students in a school take a test in 8th grade. Students who score 30 or below are assigned to remedial classes, while students scoring above 30 stay in regular classes. Regression discontinuity could be applied to this setting with test score as a running variable and 30 as the cutoff to look at the effects of remedial classes.

Regression discontinuity works by focusing on the cutoff. It makes an estimate of what the outcome is within a narrow bandwidth to the left of the cutoff, and also makes an estimate of what the outcome is to the right of the cutoff. Then it compares them to generate a treatment effect estimate.

See [Wikpedia: Regression Discontinuity Design](https://en.wikipedia.org/wiki/Regression_discontinuity_design) for more information.

Regression discontinuity receives a lot of attention because it relies on what some consider to be plausible assumptions. If the running variable is finely measured and is not being manipulated, then one can argue that being just to the left or the right of a cutoff is effectively random (someone getting a 30 or 31 on the test can basically be down to bad luck on the day) and so this approach by itself can remove confounding from lots of factors.

## Keep in Mind

- There are many, many options to choose when performing an RDD. Bandwidth selection procedure, polynomial terms, bias correction, etc. etc.. Please check the help file for your command of choice closely, and ensure you know what kind of analysis you're about to run. Don't assume the defaults are correct.
- Regression discontinuity relies on the absence of *manipulation* of the running variable. In the test score example, if the teachers scoring the exam nudge a few students from 30 to 31 so they can avoid remedial classes, RDD doesn't work any more.
- Because the method relies on isolating a narrow bandwidth around the cutoff, RDD doesn't work quite the same if the running variable is discrete and split into a small number of groups. You want a running variable with a lot of different values! See [Kolesár and Rothe (2018)](https://www.aeaweb.org/articles?id=10.1257/aer.20160945) for more information.
- In order to improve statistical performance, regression discontinuity designs often incorporate information from data points far away from the cutoff to improve the estimate of what the outcome is near the cutoff. This can be done nonparametrically, but is most often done by fitting a separate polynomial function for the running variable on either side of the cutoff. A temptation is to use a very high-order polynomial (say, $$x, x^2, x^3, x^4$$ and $$x^5$$) to improve fit. However, in general a low-order polynomial is probably a better idea. See [Gelman and Imbens 2019](https://amstat.tandfonline.com/doi/abs/10.1080/07350015.2017.1366909) for more information.
- Regression discontinuity designs are very well-suited to graphical demonstrations of the method. Software packages designed for RDD specifically will almost always provide an easy method for creating these graphs, and it is rare that you will not want to do this. However, do keep in mind that graphs can sometimes obscure meaningfully large effects. See [Kirabo Jackson](https://twitter.com/KiraboJackson/status/1074110061025419268) for an explanation.
- Regression discontinuities can be *sharp*, where everyone to one side of the cutoff is treated and nobody on the other side is, or *fuzzy*, where the probability of treatment changes across the cutoff but assignment isn't perfect. Most RDD packages can handle both. The intuition for both is similar, but the statistical properties of sharp designs are generally stronger. Fuzzy RDD can be thought of as similar to using an instrumental variables estimator in a case of imperfect random assignment in an experiment. Covariates are generally not necessary in a sharp RDD but may be advisable in a fuzzy one.

## Also Consider

- The [Regression Kink Design]({{ "/Model_Estimation/regression_kink_design.html" | relative_url }}) is an extension of RDD that looks for a change in *a relationship between the running variable and the outcome*, i.e. the slope, at the cutoff, rather than a change in the predicted outcome.
- Regression discontinuity designs are often accompanied by placebo tests, where the same RDD is run again, but with a covariate or some other non-outcome measure used as the outcome. If the RDD shows a significant effect for the covariates, this suggests that balancing did not occur properly and there may be an issue with the RDD assumptions.
- Part of performing an RDD is selecting a bandwidth around the cutoff to focus on. This can be done by context, but more commonly there are data-based methods for selecting a bandwidth Check your RDD command of choice to see what methods are available for selecting a bandwidth.

# Implementations

## Stata

A standard package for performing regression discontinuity in Stata is **rdrobust**, installable from `scc`.

```stata
* If necessary
* ssc install rdrobust

* Load RDD of house elections from the R package rddtools,
* and originally from Lee (2008) https://www.sciencedirect.com/science/article/abs/pii/S0304407607001121
import delimited "https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Estimation/Data/Regression_Discontinuity_Design/house.csv", clear

* x is "vote margin in the previous election" and y is "vote margin in this election"

* If we want to specify options for bandwidth selection, we can run rdbwselect directly.
* Otherwise, rdrobust will run it with default options by itself
* c(0) indicates that treatment is assigned at 0 (i.e. someone gets more votes than the opponent)
rdbwselect y x, c(0)

* Run a sharp RDD with a second-order polynomial term
rdrobust y x, c(0) p(2)

* Run a fuzzy RDD 
* We don't have a fuzzy RDD in this data, but let's create one, where
* probability of treatment jumps from 20% to 60% at the cutoff
g treatment = (runiform() < .2)*(x < 0) + (runiform() < .6)*(x >= 0)
rdrobust y x, c(0) fuzzy(treatment)

* Generate a standard RDD plot with a polynomial of 2 (default is 4)
rdplot y x, c(0) p(2)
```

## R

There are several packages in R designed for the estimation of RDD. Three prominent options are **rdd**, **rddtools**, and **rdrobust**. See [this article](https://files.eric.ed.gov/fulltext/EJ1141190.pdf) for comparisons between them in terms of their strengths and weaknesses. The article, considering the verisons of the packages available in 2017, recommends **rddtools** for assumption and sensitivity checks, and **rdrobust** for bandwidth selection and treatment effect estimation. We will consider **rdrobust** here. See [the rddtools walkthrough](https://github.com/bquast/rddtools-article) for a detailed example of the use of **rddtools**.

```r
# If necessary
# install.packages('rdrobust')
library(rdrobust)

# Load RDD of house elections from the R package rddtools,
# and originally from Lee (2008) https://www.sciencedirect.com/science/article/abs/pii/S0304407607001121
df <- read.csv("https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Estimation/Data/Regression_Discontinuity_Design/house.csv")

# x is "vote margin in the previous election" and y is "vote margin in this election"

# If we want to specify options for bandwidth selection, we can run rdbwselect directly.
# Otherwise, rdrobust will run it with default options by itself
# c(0) indicates that treatment is assigned at 0 (i.e. someone gets more votes than the opponent)
bandwidth <- rdbwselect(df$y, df$x, c=0)

# Run a sharp RDD with a second-order polynomial term
rdd <- rdrobust(df$y, df$x,
                c=0, p=2)
summary(rdd)

# Run a fuzzy RDD 
# We don't have a fuzzy RDD in this data, but let's create one, where
# probability of treatment jumps from 20% to 60% at the cutoff
N <- nrow(df)
df$treatment <- (runif(N) < .2)*(df$x < 0) + (runif(N) < .6)*(df$x >= 0)
rddfuzzy <- rdrobust(df$y, df$x,
                     c=0, p=2, fuzzy = df$treatment)
summary(rddfuzzy)

# Generate a standard RDD plot with a polynomial of 2 (default is 4)
rdplot(df$y, df$x,
       c = 0, p = 2)
```
