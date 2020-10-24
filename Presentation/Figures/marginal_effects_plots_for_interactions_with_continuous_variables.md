---
title: Marginal Effects Plots for Interactions with Continuous Variables
parent: Figures
grand_parent: Presentation ## Optional for indexing
has_children: false
mathjax: true
nav_order: 1
---

# Marginal Effects Plots for Interactions with Continuous Variables

In many contexts, the effect of one variable on another might be allowed to vary. For example, the relationship between income and mortality is nonlinear, so the effect of an additional dollar of income on mortality is different for someone earning $20,000/year than for someone earning $100,000/year. Or maybe the relationship between income and mortality differs depending on how many years of education you have.

A marginal effects plot displays the effect of $$X$$ on $$Y$$ for different values of $$Z$$ (or $$X$$). The plot will often include confidence intervals as well. The same code will often work if there's not an explicit interaction, but you are, for example, estimating a logit model where the effect of one variable changes with the values of the others.

## Keep in Mind

- Interactions often have poor statistical power, and you will generally need a lot of observations to tell if the effect of $X$ on $$Y$$ is different for two given different values of $$Z$$.
- Make sure your graph has clearly labeled axes, so readers can tell whether your y-axis is the predicted value of $Y$ or the marginal effect of $$X$$ on $$Y$$.

## Also Consider

- Consider performing a [power analysis of interaction terms]({{ "/Other/power_analysis_for_interactions" | relative_url }}) before running your analysis to see whether you have the statistical power for your interactions
- [Average marginal effects]({{ "/Model_Estimation/average_marginal_effects.html" | relative_url }}) or [marginal effects at the mean]({{ "/Model_Estimation/marginal_effects_at_the_mean.html" | relative_url }}) can be used to get a single marginal effect averaged over your sample, rather than showing how it varies across the sample.
- [Marginal effects plots for interactions with categorical variables]({{ "/Presentation/Figures/marginal_effects_plots_for_interactions_with_categorical_variables.html" | relative_url }})

# Implementations

## R

The **interplot** package can plot the marginal effect of a variable $$X$$ (y-axis) against different values of some variable. If instead you want the predicted values of $$Y$$ on the y-axis, look at the **ggeffects** package.

```r
# Install relevant packages, if necessary:
# install.packages(c('ggplot2', 'interplot'))

# Load in ggplot2 and interplot
library(ggplot2)
library(interplot)

# Load in the txhousing data
data(txhousing)

# Estimate a regression with a nonlinear term
cubic_model <- lm(sales ~ listings + I(listings^2) + 
                    I(listings^3), 
                  data = txhousing)

# Get the marginal effect of var1 (listings)
# at different values of var2 (listings), with confidence ribbon.
# This will return a ggplot object, so you can 
# customize using ggplot elements like labs().
interplot(cubic_model, 
          var1 = "listings",
          var2 = "listings")+
  labs(x = "Number of Listings",
       y = "Marginal Effect of Listings")
# Try setting adding listings*date to the regression model
# and then in interplot set var2 = "date" to get the effect of listings at different values of date
```
This results in:

![Marginal effect of listings varying over listings, produced with R.](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Marginal-Effects-Plots-for-Interactions-with-Continuous-Variables/r_marginal_effect_continuous_interaction.png)

## Stata

We will use the `marginsplot` command, which requires Stata 12 or higher.

```stata
* Load in the National Longitudinal Survey of Youth - Women sample
sysuse nlsw88.dta

* Perform a regression with a nonlinear term
regress wage c.tenure##c.tenure

* Use margins to calculate the marginal effects
* Put the variable we're interested in getting the effect of in dydx()
* And the values we want to evaluate it at in at()
margins, dydx(tenure) at(tenure = (0(1)26))
* (If we had interacted with another variable, say age, we would specify similarly, 
* with at(age = (start(count-by)end)))

* Then, marginsplot
* The recast() and recastci() options make the effect/CI show up as a line/area
* Remove to get points/lines instead.
marginsplot, xtitle("Tenure") ytitle("Marginal Effect of Tenure") recast(line) recastci(rarea)
```
This results in:

![Marginal effect of tenure varying over tenure, produced with Stata.](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Marginal-Effects-Plots-for-Interactions-with-Continuous-Variables/stata_marginal_effects_continuous_interaction.png)
