---
title: Summary Statistics Tables
parent: Tables
grand_parent: Presentation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Summary Statistics Tables

Before looking at relationships between variables, it is generally a good idea to show a reader what the distributions of individual variables look like. A common way to do this, which allows you to show information about many variables at once, is a "Summary statistics table" or "descriptive statistics table" in which each row is one variable in your data, and the columns include things like number of observations, mean, median, standard deviation, and range.

## Keep in Mind

- Make sure that you are using the appropriate summary measures for the variables that you have. For example, if you have a variable indicating the country someone is from coded as that country's international calling code, don't include it in a table that reports the mean - you'd get an answer but that answer wouldn't make any sense.
- If you have categorical variables, you can generally still incorporate them into a summary statistics table by [turning them into binary "dummy" variables]({{ "/Data_Manipulation/Creating_Dummy_Variables/creating_dummy_variables.html" | relative_url }}).

## Also Consider

- Graphs can be more informative ways of showing the distribution of a variable, and you may want to show a graph of your variable's distribution in addition to its inclusion on a summary statistics table. There are many ways to do this, but two common ones are [density plots]({{ "/Presentation/Figures/density_plots.html" | relative_url }}) or [histograms]({{ "/Presentation/Figures/histograms.html" | relative_url }}) for continuous variables, or [bar plots]({{ "/Presentation/Figures/bar_graphs.html" | relative_url }}) for categorical variables.

# Implementations

## R

Probably the most straightforward and simplest way to do a summary statistics table in R is with the `sumtable` function in the **vtable** package, which also has many options for customization. There are also other options like `stargazer` in **stargazer**, `dfsummary()` in **summarytools**, `summary_table()` in **qwraps2** or `table1()` in **table1**. See [this page](https://thatdatatho.com/2018/08/20/easily-create-descriptive-summary-statistic-tables-r-studio/) for a comparison of different packages.

```r
# If necessary
# install.packages('vtable')
library(vtable)
data(mtcars)

# Feed sumtable a data.frame with the variables you want summarized
mt_tosum <- mtcars[,c('mpg','cyl','disp')]
# By default, the table shows up in the Viewer pane (in RStudio) or your browser (otherwise)
# (or if being run inside of RMarkdown, in the RMarkdown document format)
sumtable(mt_tosum)
# st() as a shortcut also works
st(mt_tosum)

# There are *many* options and customizations. For all of them, see
# help(sumtable)
# Some useful ones include out, which designates a file to send the table to
# (note that HTML tables can be copied straight into Word from an output file)
sumtable(mt_tosum, out = 'html', file = 'my_summary.html')

# sumtable will handle factor variables as expected,
# and you can replace variable names with "labels"
mt_tosum$trans <- factor(mtcars$am, labels = c('Manual','Automatic'))
st(mt_tosum, labels = c('Miles per Gallon','Cylinders','Displacement','Transmission'))

# Use group to get summary statistics by group
st(mt_tosum, labels = c('Miles per Gallon','Cylinders','Displacement'), group = 'trans')
```

Another good option is the package **skimr**, which is an excellent alternative to `base::summary()`. `skimr::skim()` takes different data types and outputs a summary statistic data frame. Numeric data gets miniature histograms and all types of data get information about the number of missing entries.

```r
# If necessary
# install.packages('dplyr')
# install.packages('skimr')
library(dplyr)
library(skimr)

skim(starwars)

#If you're wondering which columns have missing values, you can use skim() in a pipeline.
starwars %>%
  skim() %>%
  dplyr::filter(n_missing > 0) %>%
  dplyr::select(skim_variable, n_missing, complete_rate)
  
#You can analyze grouped data with skimr. You can also easily customize the output table using skim_with().
my_skim <- skim_with(base = sfl(
    n = length
))
starwars %>%
    group_by(species) %>%
    my_skim() %>%
    dplyr::filter(skim_variable == "height" & n > 1)

```

## Stata

The built-in Stata command `summarize` (which can be referred to in short as `su` or `summ`) easily creates summary statistics tables. However, while `summarize` is well-suited for viewing descriptive statistics on your own, it is not well-suited for making tables to publish in a paper, since it is difficult to limit the number of significant digits, and does not offer an easy way to export the table other than selecting the Stata output, selecting "Copy Table", and pasting into a spreadsheet.

For more flexible tables that can be easily exported, we will be using the highly flexible **estout** package. For more information on the many different options and specifications for **estout** summary tables, see [this page](http://repec.org/bocode/e/estout/estpost.html). We will also see how to use `outreg2` in the **outreg2** package, which is less flexible but is slightly less work to use for standard tables that are basically `summarize` but nicer-looking and output to a file.

```stata
* If necessary
* ssc install estout
* ssc install outreg2

sysuse auto.dta, clear

* summarize will give us a table that is great for our own purposes, not so much for exporting
summarize price mpg rep78 i.foreign

* Instead using estpost summarize will give us an esttab-compatible table
* Note that factor variables no longer work - we must make dummies by hand
xi i.foreign, pre(f_) noomit
estpost summarize price mpg rep78 f_*

* We can then use esttab and cells() to pick columns
* Now it's nicely formatted
* The quotes around the statistics put all the statistics in one row 
esttab, cells("count mean sd min max")

* If we want to limit the number of significant digits we must do this stat by stat
* Using a standard format option (see help format)
esttab, cells("count mean(fmt(%9.2f)) sd(fmt(%9.2f)) min max")

* And write out to file with "using"
esttab using mytable.rtf, cells("count mean(fmt(%9.2f)) sd(fmt(%9.2f)) min max") replace


* Or we can work with outreg2
* First, limit the data to the variables we want to summarize
preserve
keep price mpg rep78 f_*

* Then outreg2 with the sum(log) option to get summary statistics
outreg2 using myoutreg2table.doc, word sum(log) replace

* Defaults are very similar to what you'd get with summarize, but you can do things like change
* number of significant digits with dec(), or which stats are in there with eqkeep()
outreg2 using mysmalltable.doc, word sum(log) eqkeep(N mean) dec(3) replace

restore
```
