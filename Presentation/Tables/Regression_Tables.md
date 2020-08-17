---
title: Regression Tables
parent: Tables
grand_parent: Presentation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Regression Tables

Statistical packages often report regression results in a way that is not how you would want to display them in a paper or on a website. Additionally, they rarely provide an option to display multiple regression results in the same table. 

Two (bad) options for including regression results in your paper include copying over each desied number by hand, or taking a screenshot of your regression output. Much better is using a command that outputs regression results in a nice format, in a way you can include in your presentation.

## Keep in Mind

- Any good regression table exporting command should include an option to limit the number of significant digits in your result. You should almost always make use of this option. It is very rare that the seventh or eighth decimal place (commonly reported in statistics packages) is actually meaningful, and it makes it difficult to read your table.
- Variable names serve different purposes in statistical coding and in papers. Variable names in papers should be changed to be readable in the language of the paper. So for example, while employment may be recorded as `EMP_STAT` in your statistics package, you should rename it Employment for your paper. Most table exporting commands include options to perform this renaming. But if it doesn't, you can always change it by hand after exporting.
- If you use asterisks to indicate significance, be sure to check the significance levels that different numbers of asterisks indicate in the command you're using, as standards for what significance levels the asterisks mean vary across fields (and so vary across commands as well). Most commands include an option to change the significance levels used. On that note, *always include a table note saying what the different asterisk indicators mean!* These commands should all include one by default - don't take it out!

## Also Consider

- If you are a Word user, and the command you are using does not export to Word or RTF, you can get the table into Word by exporting an HTML, CSV, or LaTeX, then opening up the result in your browser, Excel, or [TtH](http://hutchinson.belmont.ma.us/tth/), respectively. Excel and HTML tables can generally be copy/pasted directly into Word (and then formatted within Word). You may at that point want to use Word's "[Convert Text to Table](https://support.office.com/en-us/article/Convert-text-to-a-table-or-a-table-to-text-b5ce45db-52d5-4fe3-8e9c-e04b62f189e1)" command, especially if you've pasted in HTML.
- By necessity, regression-output commands often have about ten million options, and they can't all be covered on this page. If you want it to do something, it probably can. To reduce errors, it is probably a good idea to do as little formatting and copy/pasting by hand as possible. So if you want to do something it doesn't do by default, like adding additional calculations, check out the **help file** for your command to see how you can do it automatically.

# Implementations

## R

There are many, many packages for exporting regression results in R, including RStudio's **[gt](https://gt.rstudio.com/)**, **texreg**, and **xtable**. Here we will focus on two: **stargazer**, which is probably the easiest to use, and **huxtable**, which is slightly more up-to-date and offers advanced formatting options, outlined on its [website](https://hughjonesd.github.io/huxtable/).

```r
# Install stargazer if necessary
# install.packages('stargazer')
library(stargazer)

# Get mtcars data
data(mtcars)

# Let's give it two regressions to output
lm1 <- lm(mpg ~ cyl, data = mtcars)
lm2 <- lm(mpg ~ cyl + hp, data = mtcars)

# Let's output an HTML table, perhaps for pasting into Word
# We could instead set type = 'latex' for LaTeX or type = 'text' for a text-only table.
stargazer(lm1, lm2, type = 'html', out = 'my_reg_table.html')

# In line with good practices, we should use readable names for our variables
stargazer(lm1, lm2, type = 'html', out = 'my_reg_table.html',
          covariate.labels = c('Cylinders','Horsepower'),
          dep.var.labels = 'Miles per Gallon')
```

This produces:

<table class="huxtable" style="border-collapse: collapse; margin-bottom: 2em; margin-top: 2em; width: 50%; margin-left: auto; margin-right: auto;  ">
<col><col><col><tr>
<td style="vertical-align: top; text-align: center; white-space: nowrap; border-style: solid solid solid solid; border-width: 0.8pt 0pt 0pt 0pt; padding: 4pt 4pt 4pt 4pt;"></td>
<td style="vertical-align: top; text-align: center; white-space: nowrap; border-style: solid solid solid solid; border-width: 0.8pt 0pt 0.4pt 0pt; padding: 4pt 4pt 4pt 4pt;">(1)</td>
<td style="vertical-align: top; text-align: center; white-space: nowrap; border-style: solid solid solid solid; border-width: 0.8pt 0pt 0.4pt 0pt; padding: 4pt 4pt 4pt 4pt;">(2)</td>
</tr>
<tr>
<td style="vertical-align: top; text-align: left; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">Cylinders</td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">-2.876 ***</td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">-2.265 ***</td>
</tr>
<tr>
<td style="vertical-align: top; text-align: left; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;"></td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">(0.322)&nbsp;&nbsp;&nbsp;</td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">(0.576)&nbsp;&nbsp;&nbsp;</td>
</tr>
<tr>
<td style="vertical-align: top; text-align: left; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">Horsepower</td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">-0.019&nbsp;&nbsp;&nbsp;&nbsp;</td>
</tr>
<tr>
<td style="vertical-align: top; text-align: left; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;"></td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; border-style: solid solid solid solid; border-width: 0pt 0pt 0.4pt 0pt; padding: 4pt 4pt 4pt 4pt;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; border-style: solid solid solid solid; border-width: 0pt 0pt 0.4pt 0pt; padding: 4pt 4pt 4pt 4pt;">(0.015)&nbsp;&nbsp;&nbsp;</td>
</tr>
<tr>
<td style="vertical-align: top; text-align: left; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">N</td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
</tr>
<tr>
<td style="vertical-align: top; text-align: left; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">R2</td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">0.726&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">0.741&nbsp;&nbsp;&nbsp;&nbsp;</td>
</tr>
<tr>
<td style="vertical-align: top; text-align: left; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">logLik</td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">-81.653&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; padding: 4pt 4pt 4pt 4pt;">-80.781&nbsp;&nbsp;&nbsp;&nbsp;</td>
</tr>
<tr>
<td style="vertical-align: top; text-align: left; white-space: nowrap; border-style: solid solid solid solid; border-width: 0pt 0pt 0.8pt 0pt; padding: 4pt 4pt 4pt 4pt;">AIC</td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; border-style: solid solid solid solid; border-width: 0pt 0pt 0.8pt 0pt; padding: 4pt 4pt 4pt 4pt;">169.306&nbsp;&nbsp;&nbsp;&nbsp;</td>
<td style="vertical-align: top; text-align: right; white-space: nowrap; border-style: solid solid solid solid; border-width: 0pt 0pt 0.8pt 0pt; padding: 4pt 4pt 4pt 4pt;">169.562&nbsp;&nbsp;&nbsp;&nbsp;</td>
</tr>
<tr>
<td colspan="3" style="vertical-align: top; text-align: left; white-space: normal; padding: 4pt 4pt 4pt 4pt;"> *** p &lt; 0.001;  ** p &lt; 0.01;  * p &lt; 0.05.</td>
</tr>
</table>

Now we will do the same thing with `huxtable`, using mostly defaults.

```
# Install huxtable and magrittr if necessary
# install.packages('huxtable', 'magrittr')
# huxtable works more easily with the pipe %>%
# which can come from magrittr or dplyr or tidyverse, etc.
library(huxtable)
library(magrittr)

# First we build a huxreg object, using readable names
huxreg(lm1, lm2,
       coefs=c('Cylinders' = 'cyl',
               'Horsepower' = 'hp')) %>%
  # We can send it to the screen to view it instantly
  print_screen()

# Or we can send it to a file with the quick_ functions, which can 
# output to pdf, docx, html, xlsx, pptx, rtf, or latex.
huxreg(lm1, lm2,
       coefs=c('Cylinders' = 'cyl',
               'Horsepower' = 'hp')) %>%
  # Let's make an HTML file
  quick_html(file = 'my_reg_output.html')
```
Which produces (note the different asterisks behavior, which can be changed with `huxreg`'s `stars` option):

<table style="text-align:center"><tr><td colspan="3" style="border-bottom: 1px solid black"></td></tr>
<tr><td style="text-align:left"></td><td colspan="2"><em>Dependent variable:</em></td></tr>
<tr><td></td><td colspan="2" style="border-bottom: 1px solid black"></td></tr>
<tr><td style="text-align:left"></td><td colspan="2">Miles per Gallon</td></tr>
<tr><td style="text-align:left"></td><td>(1)</td><td>(2)</td></tr>
<tr><td colspan="3" style="border-bottom: 1px solid black"></td></tr><tr><td style="text-align:left">Cylinders</td><td>-2.876<sup>***</sup></td><td>-2.265<sup>***</sup></td></tr>
<tr><td style="text-align:left"></td><td>(0.322)</td><td>(0.576)</td></tr>
<tr><td style="text-align:left"></td><td></td><td></td></tr>
<tr><td style="text-align:left">Horsepower</td><td></td><td>-0.019</td></tr>
<tr><td style="text-align:left"></td><td></td><td>(0.015)</td></tr>
<tr><td style="text-align:left"></td><td></td><td></td></tr>
<tr><td style="text-align:left">Constant</td><td>37.885<sup>***</sup></td><td>36.908<sup>***</sup></td></tr>
<tr><td style="text-align:left"></td><td>(2.074)</td><td>(2.191)</td></tr>
<tr><td style="text-align:left"></td><td></td><td></td></tr>
<tr><td colspan="3" style="border-bottom: 1px solid black"></td></tr><tr><td style="text-align:left">Observations</td><td>32</td><td>32</td></tr>
<tr><td style="text-align:left">R<sup>2</sup></td><td>0.726</td><td>0.741</td></tr>
<tr><td style="text-align:left">Adjusted R<sup>2</sup></td><td>0.717</td><td>0.723</td></tr>
<tr><td style="text-align:left">Residual Std. Error</td><td>3.206 (df = 30)</td><td>3.173 (df = 29)</td></tr>
<tr><td style="text-align:left">F Statistic</td><td>79.561<sup>***</sup> (df = 1; 30)</td><td>41.422<sup>***</sup> (df = 2; 29)</td></tr>
<tr><td colspan="3" style="border-bottom: 1px solid black"></td></tr><tr><td style="text-align:left"><em>Note:</em></td><td colspan="2" style="text-align:right"><sup>*</sup>p<0.1; <sup>**</sup>p<0.05; <sup>***</sup>p<0.01</td></tr>
</table>


## Stata

There are two main ways of outputting regression results in Stata, both of which must be installed from `ssc install`: **outreg2** and **estout**. We will use **estout** here, as it is more flexible. More detail is available on the [**estout** website](http://repec.sowi.unibe.ch/stata/estout/).

Also note that, in a pinch, if you're using a strange command that does not play nicely with **estout**, you can often select *any* Stata regression output, select the output, right-click, do "Copy Table", and paste the result into Excel. This is only if all else fails.

```stata

* Install estout if necessary
* ssc install estout

* Load auto data
sysuse auto.dta, clear

* Let's provide it two regressions
* Making sure to store the results each time
reg mpg weight
estimates store weightonly
reg mpg weight foreign
estimates store weightandforeign

* Now let's export the table using estout
* while renaming the variables for readability using the variable labels already in Stata
* replacing any table we've already made
* and making an HTML table with style(html)
* style(tex) also works, and the default is tab-delimited data for use in Excel.
* Note also the default is to display t-statistics in parentheses. If we want 
* standard errors instead, we say so with se
esttab weightonly weightandforeign using my_reg_output.html, label replace style(html) se
```


Which produces:

<table border="0" width="*">
<tr><td colspan="3"><hr></td></tr>
<tr><td>                    </td><td>         (1)              </td><td>         (2)              </td></tr>
<tr><td>                    </td><td>Mileage (mpg)              </td><td>Mileage (mpg)              </td></tr>
<tr><td colspan="3"><hr></td></tr>
<tr><td>Weight (lbs.)       </td><td>    -0.00601<sup>***</sup></td><td>    -0.00659<sup>***</sup></td></tr>
<tr><td>                    </td><td>  (0.000518)              </td><td>  (0.000637)              </td></tr>
<tr><td colspan="3">&nbsp;</td></tr>
<tr><td>Car type            </td><td>                          </td><td>      -1.650              </td></tr>
<tr><td>                    </td><td>                          </td><td>     (1.076)              </td></tr>
<tr><td colspan="3">&nbsp;</td></tr>
<tr><td>Constant            </td><td>       39.44<sup>***</sup></td><td>       41.68<sup>***</sup></td></tr>
<tr><td>                    </td><td>     (1.614)              </td><td>     (2.166)              </td></tr>
<tr><td colspan="3"><hr></td></tr>
<tr><td>Observations        </td><td>          74              </td><td>          74              </td></tr>
<tr><td colspan="3"><hr></td></tr>
<tr><td colspan="3">Standard errors in parentheses<br /><sup>*</sup> <i>p</i> < 0.05, <sup>**</sup> <i>p</i> < 0.01, <sup>***</sup> <i>p</i> < 0.001</td></tr>
</table>

