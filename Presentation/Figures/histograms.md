---
title: Histograms
parent: Figures
grand_parent: Presentation ## Optional for indexing
has_children: false
mathjax: true
nav_order: 1
---
  
# Histograms
  
*Histograms* are an indespensible tool of research across disciplines. They offer a helpful way to represent the distribution of a variable of interest. Specifically, their function is to record how frequently data values fall within pre-specified ranges called "bins." Such visual representations can help researchers easily detect whether their data are distributed in a skewed or symmetric way, and can help detect outliers. 

Despite being such a popular tool for scientific research, choosing the bin width (alternatively, number of bins) is ultimately a choice by the researcher. Histograms are intended to convey information about the variable, and choosing the "right" bin size to convey the information helpfully can be something of an art.

The relationship between bin width $$h$$ and the number of bins $$k$$ is given by:

$$
k = \frac{ \max x - \min x}{h}
$$

For this reason, statistical softwares such as R and Stata will often accept either custom bin width specifications, or a number of bins.

## Histogram vs. bar graph

Because histograms represent data frequency using rectangular bars, they might be mistaken for [bar graphs]({{ "/Presentation/Figures/bar_graphs.html" | relative_url }}) at first glance. Whereas bar graphs (sometimes called bar charts) plot values for *categorical* data, histograms represent the distribution of continuous variables such as income, height, weight, etc.

# Implementations

When feeding data to visualise using a histogram, one will notice that both R and Stata will attempt to "guess" what the "best" bin width/number of bins are. These may be overridden by user commands, as we will see.

## Python

There are many plotting libraries in Python, including *declarative* (say what you want) and *imperative* (build what you want) options. In the example below, we'll explore several different options for plotting histogram data.

By far the quickest way to plot a histogram is to use data analysis package [**pandas**](https://pandas.pydata.org/)' built-in bar chart option (which uses plotting library [**matplotlib**](https://matplotlib.org/3.1.1/index.html)).

```python
import pandas as pd

df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/Ecdat/PSID.csv",
                 index_col=0)

df['earnings'].plot.hist();
```

![png](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/histogram_graphs/py_hist_1.png)

Note that, by default, the `hist` function shows counts on the y-axis.

We can make this plot a bit more appealing by calling on the customisation features from **matplotlib**. Calling `df['column-name'].plot.hist()` returns a **matplotlib** `ax` object that accepts further customisation. We will use this and a style to make the plot more appealing, while also switching to show a density rather than counts, setting the number of bins explicitly, and using a logarithmic scale.

```python
import matplotlib.pyplot as plt

plt.style.use('seaborn')

ax = df['earnings'].plot.hist(density=True, log=True, bins=80)
ax.set_title('Earnings in the PSID', loc='left')
ax.set_ylabel('Density')
ax.set_xlabel('Earnings');

```

![png](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/histogram_graphs/py_hist_2.png)


An alternative to the matplotlib-pandas combination is [**seaborn**](), a declarative plotting library. Using **seaborn**, we can quickly compared histograms of different cuts of the data. In the example below, a binary variable that sorts individuals into two groups based on age is added and used as the 'hue' of the keyword argument.

```python
import seaborn as sns

age_cut_off = 45
df[f'Older than {age_cut_off}'] = df['age']>age_cut_off

ax = sns.histplot(df, x="earnings", hue=f"Older than {age_cut_off}", element="step", stat="density")
ax.set_yscale('log')
```

![png](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/histogram_graphs/py_hist_3.png)

Finally, let's look at a different declarative library, [**plotnine**](https://plotnine.readthedocs.io/en/stable/), which is inspired by (and has very similar syntax to) R's plotting library **ggplot**.

```python
from plotnine import ggplot, aes, geom_histogram

(
    ggplot(df, aes(x='earnings', y='stat(density)')
          )
    + geom_histogram(bins=80)
)
```

![png](https://github.com/LOST-STATS/LOST-STATS.github.io/raw/master/Presentation/Figures/Images/histogram_graphs/py_hist_4.png)


## R

Histograms can be represented using base `R`, or more elegantly with `ggplot`. `R` comes with a built-in `states.x77` dataset containing per-capita income in the US states for the year 1974, which we will be using.

```r

# loading the data

incomes = data.frame( income = state.x77[,'Income'])

# first using base R

hist(incomes$income)

# now using ggplot

if(!require(ggplot2)) install.packages('ggplot2')
library(ggplot2)

ggplot( data = incomes ) + 
geom_histogram( aes( x = income ) )

# showing how we can adjust number of bins...

ggplot( data = incomes ) + 
geom_histogram( aes( x = income ) ,
                bins = 15 )

# ...or the width of each bin

ggplot( data = incomes ) + 
geom_histogram( aes( x = income ) ,
                binwidth = 500 )
```

## Stata

To illustrate the basic histogram function in Stata we will use the "auto" dataset.

```stata

** loading the data

webuse auto

* histogram with default bin width
* The frequency option puts a count of observations on the y-axis
* rather than a proportion

histogram mpg, frequency

* we can adjust the number of bins...

histogram mpg, bin(15) frequency

* ...or the bin width

hist mpg, width(2) frequency

```
