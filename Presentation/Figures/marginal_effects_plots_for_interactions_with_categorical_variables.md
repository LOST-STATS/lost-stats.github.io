---
title: Marginal effects plots for interactions with categorical variables
parent: Figures
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Marginal effects plots for interactions with categorical variables

In many contexts, the effect of one variable on another might be allowed to vary. For example, the relationship between income and mortality might be different between someone with no degree, a high school degree, or a college degree.

A marginal effects plot for a categorical interaction displays the effect of $X$ on $Y$ on the y-axis for different values of a categorical variable $Z$ on the x-axis. The plot will often include confidence intervals as well. In some cases the categorical variable may be ordered, so you'd want the $Z$ values to show up in that order.

## Keep in Mind

- Some versions of these graphs normalize the effect of one of the categories to 0, and shows the effect for other values relative to that one.

## Also Consider

- Consider performing a [power analysis of interaction terms]({{ "/Other/power_analysis_for_interactions.html" | relative_url }}) before running your analysis to see whether you have the statistical power for your interactions
- [Marginal effects plots for interactions with continuous variables]({{ "/Figures/marginal_effects_plots_for_interactions_with_continuous_variables.html" | relative_url }})

# Implementations

In each of these examples, we will be using data on organ donation rates by state from [Kessler & Roth 2014](https://www.nber.org/papers/w20378). The example is of a [2x2 difference-in-difference model]({{ "/Research_Design/two_by_two_difference_in_difference.html" | relative_url }}) extended to estimate dynamic treatment effects, where treatment is interacted with the number of time periods until/since treatment goes into effect.

All of these examples directly retrieve effect and confidence interval information from the regression by hand rather than relying on a package; packages for graphing interactions often focus on continuous interactions. The original code snippets for the Python, R, and Stata examples comes from the textbook [The Effect](http://nickchk.com/causalitybook.html).

## Python

```python
# PYTHON CODE
import pandas as pd
import matplotlib.pyplot as plt
import linearmodels as lm

# Read in data
od = pd.read_csv(
    "https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Presentation/Figures/Data/Marginal_Effects_Plots_For_Interactions_With_Categorical_Variables/organ_donation.csv"
)

# Create Treatment Variable
od["California"] = od["State"] == "California"

# PanelOLS requires a numeric time variable
od["Qtr"] = 1
od.loc[od["Quarter"] == "Q12011", "Qtr"] = 2
od.loc[od["Quarter"] == "Q22011", "Qtr"] = 3
od.loc[od["Quarter"] == "Q32011", "Qtr"] = 4
od.loc[od["Quarter"] == "Q42011", "Qtr"] = 5
od.loc[od["Quarter"] == "Q12012", "Qtr"] = 6

# Create our interactions by hand,
# skipping quarter 3, the last one before treatment
for i in range(1, 7):
    name = f"INX{i}"
    od[name] = 1 * od["California"]
    od.loc[od["Qtr"] != i, name] = 0

# Set our individual and time (index) for our data
od = od.set_index(["State", "Qtr"])

mod = lm.PanelOLS.from_formula(
    """Rate ~
INX1 + INX2 + INX4 + INX5 + INX6 +
EntityEffects + TimeEffects""",
    od,
)

# Specify clustering when we fit the model
clfe = mod.fit(cov_type="clustered", cluster_entity=True)

# Get coefficients and CIs
res = pd.concat([clfe.params, clfe.std_errors], axis=1)
# Scale standard error to CI
res["ci"] = res["std_error"] * 1.96

# Add our quarter values
res["Qtr"] = [1, 2, 4, 5, 6]
# And add our reference period back in
reference = pd.DataFrame([[0, 0, 0, 3]], columns=["parameter", "lower", "upper", "Qtr"])
res = pd.concat([res, reference])

# For plotting, sort and add labels
res = res.sort_values("Qtr")
res["Quarter"] = ["Q42010", "Q12011", "Q22011", "Q32011", "Q42011", "Q12012"]

# Plot the estimates as connected lines with error bars

plt.errorbar(x="Quarter", y="parameter", yerr="ci", data=res)
# Add a horizontal line at 0
plt.axhline(0, linestyle="dashed")
```

![Categorical marginal effect plot in Python](https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Presentation/Figures/Images/Marginal_Effects_Plots_For_Interactions_With_Categorical_Variables/Python_Categorical_Interaction_Effect.png)

## R

If you happen to be using the **fixest** package to run your model, there is actually a single convenient command `coefplot` that will make the graph for you. However, this requires your analysis to use some other tools from **fixest** too. So below I'll show both the **fixest** approach as well as a more general approach (which also uses a **fixest** model but doesn't need to).

First, prepare the data:

```r?example=categorical
library(tidyverse)
library(fixest)
library(broom)

od <- read_csv("https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Presentation/Figures/Data/Marginal_Effects_Plots_For_Interactions_With_Categorical_Variables/organ_donation.csv")

# Treatment variable
od <- od %>%
  mutate(Treated = State == "California" &
    Quarter %in% c("Q32011", "Q42011", "Q12012")) %>%
  # Create an ordered version of Quarter so we can graph it
  # and make sure we drop the last pre-treatment interaction,
  # which is quarter 2 of 2011
  mutate(Quarter = relevel(factor(Quarter), ref = "Q22011")) %>%
  # The treated group is the state of California
  # The 1* is only necessary for the first fixest method below; optional for the second, more general method
  mutate(California = 1 * (State == "California"))
```

Next, our steps to do the **fixest**-specific method:

```r?example=categorical
# in the *specific example* of fixest, there is a simple and easy method:
od <- od %>% mutate(fQuarter = factor(Quarter,
  levels = c(
    "Q42010", "Q12011", "Q22011",
    "Q32011", "Q42011", "Q12012"
  )
))
femethod <- feols(Rate ~ i(California, fQuarter, drop = "Q22011") |
  State + Quarter, data = od)

coefplot(femethod, ref = c("Q22011" = 3), pt.join = TRUE)
```

However, for other packages this may not work, so I will also do it by hand in a way that will work with models more generally (even though we'll still run the model in fixest):

```rr?example=categorical
# Interact quarter with being in the treated group
clfe <- feols(Rate ~ California * Quarter | State,
  data = od
)

coefplot(clfe, ref = "Q22011")

# Use broom::tidy to get the coefficients and SEs
res <- tidy(clfe) %>%
  # Keep only the interactions
  filter(str_detect(term, ":")) %>%
  # Pull the quarter out of the term
  mutate(Quarter = str_sub(term, -6)) %>%
  # Add in the term we dropped as 0
  add_row(
    estimate = 0, std.error = 0,
    Quarter = "Q22011"
  ) %>%
  # and add 95% confidence intervals
  mutate(
    ci_bottom = estimate - 1.96 * std.error,
    ci_top = estimate + 1.96 * std.error
  ) %>%
  # And put the quarters in order
  mutate(Quarter = factor(Quarter,
    levels = c(
      "Q42010", "Q12011", "Q22011",
      "Q32011", "Q42011", "Q12012"
    )
  ))


# And graph
# "group = 1" is necessary to get ggplot to add the line graph
# when the x-axis is a factor
ggplot(res, aes(x = Quarter, y = estimate, group = 1)) +
  # Add points for each estimate and connect them
  geom_point() +
  geom_line() +
  # Add confidence intervals
  geom_linerange(aes(ymin = ci_bottom, ymax = ci_top)) +
  # Add a line so we know where 0 is
  geom_hline(aes(yintercept = 0), linetype = "dashed") +
  # Always label!
  labs(caption = "95% Confidence Intervals Shown")
```

![Categorical marginal effect plot in R/ggplot2](https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Presentation/Figures/Images/Marginal_Effects_Plots_For_Interactions_With_Categorical_Variables/R_Categorical_Interaction_Effect.png)

## Stata

```stata
* For running the model:
* ssc install reghdfe

import delimited using https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Presentation/Figures/Data/Marginal_Effects_Plots_For_Interactions_With_Categorical_Variables/organ_donation.csv, clear

* Create value-labeled version of quarter
* So we can easily graph it
g Qtr = 1
replace Qtr = 2 if quarter == "Q12011"
replace Qtr = 3 if quarter == "Q22011"
replace Qtr = 4 if quarter == "Q32011"
replace Qtr = 5 if quarter == "Q42011"
replace Qtr = 6 if quarter == "Q12012"

label def quarters 1 "Q42010" 2 "Q12011" 3 "Q22011" 4 "Q32011" 5 "Q42011" 6 "Q12012"
label values Qtr quarters

* Interact being in the treated group
* with Qtr, using ib3 to drop the third
* quarter (the last one before treatment)
g California = state == "California"

reghdfe rate California##ib3.Qtr, a(state Qtr) vce(cluster state)

* Pull out the coefficients and SEs
g coef = .
g se = .
forvalues i = 1(1)6 {
	replace coef = _b[1.California#`i'.Qtr] if Qtr == `i'
	replace se = _se[1.California#`i'.Qtr] if Qtr == `i'
}

* Make confidence intervals
g ci_top = coef+1.96*se
g ci_bottom = coef - 1.96*se

* Limit ourselves to one observation per quarter
keep Qtr coef se ci_*
duplicates drop

* Create connected scatterplot of coefficients
* with CIs included with rcap
* and a line at 0 from function
twoway (sc coef Qtr, connect(line)) (rcap ci_top ci_bottom Qtr) (function y = 0, range(1 6)), xtitle("Quarter") caption("95% Confidence Intervals Shown")
```

![Categorical marginal effect plot in Stata](https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Presentation/Figures/Images/Marginal_Effects_Plots_For_Interactions_With_Categorical_Variables/Stata_Categorical_Interaction_Effect.png)

