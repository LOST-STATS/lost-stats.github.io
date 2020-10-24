---
title: Line Graph with Labels at the Beginning or End of Lines
parent: Figures
grand_parent: Presentation ## Optional for indexing
has_children: false
nav_order: 1
---

# Line Graph with Labels at the Beginning or End of Lines

A [line graph]({{ "/Presentation/Figures/line_graphs.html" | relative_url }}) is a common way of showing how a value changes over time (or over any other x-axis where there's only one observation per x-axis value). It is also common to put several line graphs on the same set of axes so you can see how multiple values are changing together.

When putting multiple line graphs on the same set of axes, a good idea is to label the different lines *on the lines themselves*, rather than in a legend, which generally makes things easier to read.

## Keep in Mind

- Check the resulting graph to make sure that labels are legible, visible in the graph area, and don't overlap.

## Also Consider

- More generally, see [Line graph]({{ "/Presentation/Figures/line_graphs.html" | relative_url }}) and [Styling line graphs]({{ "/Presentation/Figures/styling_line_graphs.html" | relative_url }}). In particular, consider [Styling line graphs]({{ "/Presentation/Figures/styling_line_graphs.html" | relative_url }}) in order to distinguish the lines by color, pattern, etc. in addition to labels
- If there are too many lines to be able to clearly follow them, labels won't help too much. Instead, consider [Faceted graphs]({{ "/Presentation/Figures/faceted_graphs.html" | relative_url }}).

# Implementations

## R

```R
# If necessary, install ggplot2, lubridate, and directlabels
# install.packages(c('ggplot2','directlabels', 'lubridate'))
library(ggplot2)
library(directlabels)

# Load in Google Trends Nobel Search Data
# Which contains the Google Trends global search popularity index for the four
# research-based Nobel prizes over a month.
df <- read.csv('https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Presentation/Figures/Data/Line_Graph_with_Labels_at_the_Beginning_or_End_of_Lines/Research_Nobel_Google_Trends.csv')

# Properly treat our date variable as a date
# Not necessary in all applications of this technique.
df$date <- lubridate::ymd(df$date)

# Construct our standard ggplot line graph
# Drawing separate lines by name
# And using the log of hits for visibility
ggplot(df, aes(x = date, y = log(hits), color = name)) + 
  labs(x = "Date",
       y = "Log of Google Trends Index")+
  geom_line()+
  # Since we are about to add line labels, we don't need a legend
  theme(legend.position = "none") +
  # Add, from the directlabels package, 
  # geom_dl, using method = 'last.bumpup' to put the 
  # labels at the end, and make sure that if they intersect, 
  # one is bumped up
  geom_dl(aes(label = name), method = 'last.bumpup') + 
  # Extend the x axis so the labels are visible - 
  # Try the graph a few times until you find a range that works
  scale_x_date(limits = c(min(df$date), lubridate::ymd('2019-10-25')))
```
This results in:

![Line Graph of Search Popularity for Research Nobels in R.](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Line_Graph_with_Labels_at_the_Beginning_or_End_of_Lines/R_line_graph_with_labels.png)

## Stata

Unfortunately, performing this technique in Stata requires placing each `text()` label on the graph. However, this can be automated with the use of a for loop to build the code using locals.

```stata
* Load in Google Trends Nobel Search Data
* Which contains the Google Trends global search popularity index for the four
* research-based Nobel prizes over a month.
import delimited "https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Presentation/Figures/Data/Line_Graph_with_Labels_at_the_Beginning_or_End_of_Lines/Research_Nobel_Google_Trends.csv", clear

* Convert the date variable to an actual date
* (not necessary in all implementations)
g ymddate = date(date, "YMD")
* Format the new variable as a date so we see it properly on the x-axis
format ymddate %td

* Graph log(hits) for visibility
g loghits = log(hits)

* Get the different prize types to graph
levelsof name, l(names)

* Figure out the last time period in the data set
quietly summarize ymddate
local lastday = r(max)

* Start constructing a local that contains all the line graphs to graph
local lines
* Start constructing a local that contains the text labels to add
local textlabs
* Loop through each one
foreach n in `names' {
	* Add in the line graph code
	* by building on the local we already have (`lines') and adding a new twoway segment
	local lines `lines' (line loghits ymddate if name == "`n'")
	
	* Figure out the value this line hits on the last point on the graph
	quietly summ loghits if name == "`n'" & ymddate == `lastday'
	* The text command takes the y-value (from the mean we just took)
	* the x-value (the last day on the graph),
	* and the text label (the name we are working with)
	* Plus place(r) to put it to the RIGHT of that point
	local textlabs `textlabs' text(`r(mean)' `lastday' "`n'", place(r))
}

* Finally, graph our lines
* with the twoway lines we've specified, followed by the text labels
* We're sure to remove the legend with legend(off)
* and extend the x-axis so we can see the labels with xscale(range())
quietly summarize ymddate
local start = r(min)
local end = r(max) + 5
twoway `lines', `textlabs' legend(off) xscale(range(`start' `end')) xtitle("Date") ytitle("Log of Google Trends Index")
```

This results in:

![Line Graph of Search Popularity for Research Nobels in Stata](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/Line_Graph_with_Labels_at_the_Beginning_or_End_of_Lines/stata_line_graph_with_labels.png)
