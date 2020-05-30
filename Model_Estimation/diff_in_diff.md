---
title: Difference in Difference 
parent: Category
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---


## INTRODUCTION

Overarching goal: think about how information on the time dimension helps us address selection problem in causal inference.

The causal inference with cross-sectional data is fundamentally tricky.

1. People, firms, etcare different from one another in lots of ways.
2. Can only get a clean comparison when you have a (quasi-)experimental setup, such as an experiment or an Regression discontinuity.

## KEEP IN MIND

Key insight of data with time dimension: Rather than comparing "i" to "j", compare i in t to i in (t−1).

1. "i"serves as a control for itself.
2. "i" am much more similar to myself yesterday than "i" am to "j".

## ALSO CONSIDER 
We want to estimate
Suppose in t = 0 (“Pre-period”),  t = 1 (“Post-period”), we can estimate 𝜏=Post-Pre
which is Y(post)-Y(pre)= Y(t=1)-Y(t=0)=𝜏 (D(t=1)-D(t=0)  ).



## IMPLEMENTSTIONS

In this case, we need to discover whether legalize marijuana could change the murder rate. After the year of 2014, we measure the difference of murder rate between legalize marijuana murder states and fully illegal to use of marijuana states. 

## Step 1:
* First of all, we need to load Data and Package, we call this data set "DiD".
```{r}
library(readr)
library(tidyverse)
library(broom)
library(here)
DiD<- read_csv(here("Data/DiD_crime.csv"))
```
## Step 2:
*Secondly, we create the indicator variable called "after" to indicate whether it is after the year of 2014, or between 2010-2013,"1" represents after 2014, "0" represents 2010-2013. If the year is after 2014 and the states decided to legalize marijuana, the indicator variable "treataafter" is "1" .

```{r}
DiD<-mutate(DiD,after=ifelse(DiD$year>=2014,1,0))
DiD<-mutate(DiD,treater=DiD$year>=2010&DiD$year<=2013)
DiD<-mutate(DiD,treatafter=after*treat)
```

## Step 3:
*Then we need to plot the graph to visualize the impact of legalize marijuana on murder rate by using ggplot.

```{r}
treated<-subset(DiD,DiD$treat==1)
mt<-ggplot(DiD,aes(x=year,y=murder))+geom_point(aes(colour=treat),size=3)+geom_vline(xintercept=2014,lty=4)
mt<-mt+labs(title="Murder and Time", x="year", y="murder")
mt<-mt+geom_line(aes(colour=treat,group=treat))
mt
```
![Diff-in-Diff](https://github.com/zuzhangjin/lost-stats.github.io/blob/source/Model_Estimation/Images/dif%20in%20dif.jpg)

## Step 4:
* We need to measure the impact of impact of legalize marijuana which is 𝜏=Post-Pre Y(t=1)-Y(t=0)=𝜏 (D(t=1)-D(t=0))  .
```{r}
DiD%>% filter(treat==1&year>=2010)%>%group_by(after)%>%summarize(tr_mean=mean(murder))
DiD%>% filter(treat==0&year>=2010)%>%group_by(after)%>%summarize(control_mean=mean(murder))


reg<-lm(murder~treater+treatafter+after,data=DiD)
```
## Step 5:
Finally, we use treatment mean minus the control mean to measure the impact of legalize marijuana on murder rate. It shows after legalization, the murder rate dropped by 0.3%.
```{r}
(4.52-4.15)-(4.85-4.18)
```