---
title: Balance Tables
parent: Tables
grand_parent: Presentation ## Optional for indexing
has_children: false
nav_order: 1
---

# Balance Tables

Balance Tables are a method by which you can statistically compare differences in characteristics between a treatment and control group. Common in experimental work and when using matching estimators, balance tables show if the treatment and control group are 'balanced' and can be seen as similarly 'identical' for comparison of a causal effect. 

## Keep in Mind

- When a characteristic is statistically different between control and treatment, your study is unbalanced in respect to that attribute.
- When a characteristic is unbalanced in your study, you may want to consider controlling for that attribute as a variable in your model specification.
- Balance tables can only report numeric differences and are not suitable for string value comparisions


# Implementations

## R

```r
# Import Dependency
library("cobalt")

# Load Data
data(mtcars)

# Create Balance Table
bal.tab(am ~ mpg + hp, data = mtcars)
```

## Stata

```stata
* Import Dependency: 'ssc install table1' 
* Load Data
sysuse auto, clear

* Create Balance Table
* You need to declare the kind of variable for each, as well as the variable by which you define treatment and control. 
* Adding test gives the statistical difference between the two groups. The ending saves your output as an .xls file

table1, by(foreign) vars(price conts \ mpg conts \ weight contn \ length conts) test saving(bal_tab.xls, replace)
```
#### Also Consider
The World Bank's very useful [ietoolkit](https://blogs.worldbank.org/impactevaluations/ie-analytics-introducing-ietoolkit) for Stata has a very flexible command for creating balance tables, iebaltab. You can learn more about how to use it on their [Wiki page on the command](https://dimewiki.worldbank.org/wiki/Iebaltab).
