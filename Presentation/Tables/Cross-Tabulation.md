---
title: Cross-Tabulation
parent: Tables
grand_parent: Presentation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: false ## Switch to false if this page has no equations or other math rendering.
---

# Cross Tabulations

A cross-tabulation is a table that shows the relationship between two or more variables. While more complex models are incredibly important, it is just as useful to quickly understand and present a basic picture of your data. This is where cross-tabulations come in handy, they simplify the data by creating subgroups which can be interpreted at a smaller and more granular scale.

A cross-tabulation is rudimentary form of analysis, and a great starting point for working with relationships between discrete variables. When presenting data for initial qualitative and quantitative analysis it is important to show how distribution of responses and distribution of groups works in the dataset. This can allow you to immediately see where deeper analysis can be used and the patterns within the data. They are specifically useful in both market research and population surveys.

## Keep in Mind

- Cross-tabulations are generally not appropriate if either of the variables you're looking at is continuous. You may want to consider a [scatterplot]({{ "/Presentation/Figures/Scatterplots.html" | relative_url }}) in this case, or a number of other options.
- By default, cross-tabulations count (tabulate) the number of observations in each cell. But it is usually straightforward to have it provide the percentage in each cell instead. Which one you want depends on what question you're trying to answer. 


## Also Consider

- Cross-tabulations are relatively simple but the possibilities are endless. It is less about knowing how to make the table and more about knowing what variables to include in order to spot trends in the data.


# Implementations

## Python

In Python we can use the `.crosstab()` method in **pandas**.

```python?example=pytab
import pandas as pd

# Get Lakers data
lakers = pd.read_csv('https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Presentation/Tables/Data/lakers.csv')

# Filter for only a couple Lakers players for space
lakersd = lakers.loc[lakers['team'] == "LAL"]
lakersd = lakersd.loc[lakers['player'].isin(['Jordan Farmar','Pau Gasol','Kobe Bryant'])]

# Create a crosstab for each basketball action for each player
pd.crosstab(lakersd['player'],lakersd['etype'])

# etype          foul  free throw  rebound  shot  turnover  violation
# player                                                             
# Jordan Farmar    99          75      110   389        87          4
# Kobe Bryant     180         529      410  1619       200          7
# Pau Gasol       159         423      752   993       148          6
```

You can even create tables analyzing three variables. Here is the same table as above for home and away games.


```python?example=pytab
# add game_type to the crosstab
# Use brackets[] to distinguish which two-way crosstab is "inside" a broader one.
pd.crosstab([lakersd['player'],lakersd['etype']],lakersd['game_type'])

# game_type                 away  home
# player        etype                 
# Jordan Farmar foul          51    48
#               free throw    21    54
#               rebound       48    62
#               shot         189   200
#               turnover      45    42
#               violation      2     2
# Kobe Bryant   foul          93    87
#               free throw   315   214
#               rebound      213   197
#               shot         882   737
#               turnover      93   107
#               violation      3     4
# Pau Gasol     foul          78    81
#               free throw   221   202
#               rebound      389   363
#               shot         513   480
#               turnover      78    70
#               violation      5     1
```

You can use the `normalize` argument to get percentages instead of counts. `normalize = 'index'` gets proportions relative to the row totals, `normalize = 'column'` goes relative to the column, and `normalize = 'all'` does relative to the whole table.

```python?example=pytab
pd.crosstab(lakersd['player'],lakersd['etype'], normalize = 'all')

# etype              foul  free throw   rebound      shot  turnover  violation
# player                                                                      
# Jordan Farmar  0.015994    0.012116  0.017771  0.062843  0.014055   0.000646
# Kobe Bryant    0.029079    0.085460  0.066236  0.261551  0.032310   0.001131
# Pau Gasol      0.025687    0.068336  0.121486  0.160420  0.023910   0.000969
```

Tests of independence between the two variables can be obtained by passing `.crosstab()` output to `scipy.stats.contingency_table`.

## R

There are  many functions for creating cross tabulations in R, including the base-R `table()` function. Here we will focus on one: `tabyl`, which is part of the **janitor** package, and is the **tidyverse** version of the table() function. This command can be used to quickly create pretty cross-tabulations which are report ready. 

```r?example=rtab
#Load in the packages
library(pacman)
p_load(tidyverse,janitor,kableExtra, lubridate)
```

First we can see how `tabyl` can create a quick summary table. To create the input just put the desired x and y variables into the tabyl() command. 

```r?example=rtab
# Get lakers data
data("lakers")

# Filter for only a couple Lakers players for space

lakersd = lakers %>% filter(team == "LAL") %>% filter(player %in% c('Jordan Farmar','Pau Gasol','Kobe Bryant'))

# Example using the base-R table() function
table(lakersd$player, lakersd$etype)

# Create a crosstab for each basketball action for each player
# Syntax is similar to table() but tabyl takes the data set as its first argument
lakersd %>%
  tabyl(player,etype)

# player foul free throw rebound shot turnover violation
# Jordan Farmar   99         75     110  389       87         4
# Kobe Bryant  180        529     410 1619      200         7
# Pau Gasol  159        423     752  993      148         6
```

You can even create tables analyzing three variables. Here is the same table as above for home and away games.


```r?example=rtab

# add game_type to the crosstab
lakersd %>%
  tabyl(player,etype, game_type)

# $away
# player foul free throw rebound shot turnover violation
# Jordan Farmar   51         21      48  189       45         2
# Kobe Bryant   93        315     213  882       93         3
# Pau Gasol   78        221     389  513       78         5
# 
# $home
# player foul free throw rebound shot turnover violation
# Jordan Farmar   48         54      62  200       42         2
# Kobe Bryant   87        214     197  737      107         4
# Pau Gasol   81        202     363  480       70         1
```

With `tabyl` you can also use the adorn commands to add percentages. For basketball this would help see what players you would be analyzing when looking at team shot data.

```r?example=rtab
lakers_shot = lakersd %>% filter(etype == "shot")

lakers_shot %>%
  # Create tabyl
  tabyl(player,result) %>%
  # Add a totals row
  adorn_totals(where = c("row","col")) %>% 
  # Add percentages of total shots taken by players  
  adorn_percentages(denominator = "col") %>%
  # Format to 1 decimal place  
  adorn_pct_formatting(digits = 1)%>%
  # Include amount of observations  
  adorn_ns()

# player          made        missed         Total
# Jordan Farmar  10.3%  (153)  15.5%  (236)  13.0%  (389)
# Kobe Bryant  51.1%  (757)  56.7%  (862)  53.9% (1619)
# Pau Gasol  38.5%  (570)  27.8%  (423)  33.1%  (993)
# Total 100.0% (1480) 100.0% (1521) 100.0% (3001) 
```

A chi square test of independence can use the `chisq.test()` function, which can accept `table()` output, or just your two variables directly. 

## Stata

In Stata we can use the base `tabulate` command, which can be shortened to `tab`.

```stata?example=statatab
* Load data
import delimited "https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Presentation/Tables/Data/lakers.csv"

* Filter for only a couple Lakers players for space
keep if team == "LAL" & inlist(player, "Jordan Farmar","Pau Gasol","Kobe Bryant")

* Create a crosstab for each basketball action for each player
tab player etype


*                      |                               etype
*               player |      foul  free th..    rebound       shot   turnover  violation |     Total
*----------------------+------------------------------------------------------------------+----------
*        Jordan Farmar |        99         75        110        389         87          4 |       764 
*          Kobe Bryant |       180        529        410      1,619        200          7 |     2,945 
*            Pau Gasol |       159        423        752        993        148          6 |     2,481 
*----------------------+------------------------------------------------------------------+----------
*                Total |       438      1,027      1,272      3,001        435         17 |     6,190 

```

To creat tables analyzing three variables, use `by` with `tab`. The following example produces a separate table for home and away games. You could alternately use the `table` command, using `table player etype game_type` to get a very similar result. Switching to `table` is a good idea for anything more complex than this, as it's a very flexible command.


```stata?example=statatab
bysort game_type: tab player etype

*----------------------------------------------------------------------------------------------------------------
*-> game_type = away
*
*                      |                               etype
*               player |      foul  free th..    rebound       shot   turnover  violation |     Total
*----------------------+------------------------------------------------------------------+----------
*        Jordan Farmar |        51         21         48        189         45          2 |       356 
*          Kobe Bryant |        93        315        213        882         93          3 |     1,599 
*            Pau Gasol |        78        221        389        513         78          5 |     1,284 
*----------------------+------------------------------------------------------------------+----------
*                Total |       222        557        650      1,584        216         10 |     3,239 
*
*----------------------------------------------------------------------------------------------------------------
*-> game_type = home
*
*                      |                               etype
*               player |      foul  free th..    rebound       shot   turnover  violation |     Total
*----------------------+------------------------------------------------------------------+----------
*        Jordan Farmar |        48         54         62        200         42          2 |       408 
*          Kobe Bryant |        87        214        197        737        107          4 |     1,346 
*            Pau Gasol |        81        202        363        480         70          1 |     1,197 
*----------------------+------------------------------------------------------------------+----------
*                Total |       216        470        622      1,417        219          7 |     2,951 
```


`tab` has a number of options that allow for different kinds of analysis. `row` calculates the percentage of the row that each cell constitutes. `col` does the same for columns, and `cell` works for the overall table. Tests of independence between the two variables can be performed with the `chi2` option (among some other available tests; see the help file).
