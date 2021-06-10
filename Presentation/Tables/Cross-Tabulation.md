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

A cross-tabulation is one of the more rudimentary forms of analysis there is. When presenting data for initial qualitative and quantitative analysis it is important to show how distribution of responses and distribution of groups work in the dataset. This can allow you to immediately see where deeper analysis can be used and the patterns within the data. They are specifically useful in both market research and population surveys.

## Keep in Mind

- For percentages, tabyl will default to a large number of significant figures. It is important to remember format it to the desired number of decimals.


## Also Consider

- Cross-tabulations are relatively simple but the possibilities are endless. It is less about knowing how to make the table and more about knowing what variables to include in order to spot trends in the data.


# Implementations


## R

There are  many packages for creating cross tabulations in R. Here we will focus on one: tabyl, which is part of the janitor package, and is dplyr's version of the table() function. This command can be used to quickly create pretty cross-tabulations which are report ready. 



```r
#Load in the packages
library(pacman)
p_load(tidyverse,janitor,kableExtra, lubridate)
```
First we can see how tabyl can create a quick summary table. To create the input just put the desired x and y variables into the tabyl() command. 

```r
# Get lakers data
data("lakers")

#Filter for only lakers players

lakersd = lakers %>% filter(team == "LAL")

#Create a crosstab for each basketball action for each player
lakersd %>%
  tabyl(player,etype)
  
              player ejection foul free throw rebound shot  sub timeout turnover violation
                            0    1          0     679    0 1431     346       27        11
       Adam Morrison        0    4          2       8   12    0       0        3         0
        Andrew Bynum        0  164        207     366  466    0       0       80         4
          Chris Mihm        0   23          7      34   40    0       0       10         0
         D.J. Mbenga        0   33          8      31   57    0       0       13         5
        Derek Fisher        0  179        122     180  646    0       0       68         3
             Jackson        0    2          0       0    0    0       0        0         0
       Jordan Farmar        0   99         75     110  389    0       0       87         4
         Josh Powell        0   99         48     170  228    0       0       50         4
         Kobe Bryant        0  180        529     410 1619    0       0      200         7
          Lamar Odom        0  233        240     599  665    0       0      133         3
         Luke Walton        0   98         52     172  289    0       0       63         0
           Pau Gasol        0  159        423     752  993    0       0      148         6
       Sasha Vujacic        0  153         70     128  375    0       0       32         4
       Shannon Brown        0    9          9      20   42    0       0        9         0
             Sun Yue        0    5          0       0    6    0       0        1         0
        Trevor Ariza        1  159        159     334  578    0       0       83         7
 Vladimir Radmanovic        0   48         25     112  203    0       0       44         2
             Yue Sun        0    4          0       0    3    0       0        2         0  

```



You can even create tables analyzing three variables. Here is the same table as above for home and away games.


```r

#add game_type to the crosstab

lakersd %>%
  tabyl(player,etype, game_type)

$away
              player ejection foul free throw rebound shot sub timeout turnover violation
                            0    0          0     341    0 725     174       21         4
       Adam Morrison        0    0          0       1    3   0       0        1         0
        Andrew Bynum        0   67         70     129  191   0       0       33         0
          Chris Mihm        0   10          3      14   17   0       0        5         0
         D.J. Mbenga        0   13          6      19   26   0       0        4         0
        Derek Fisher        0   88         64      83  309   0       0       24         0
             Jackson        0    2          0       0    0   0       0        0         0
       Jordan Farmar        0   51         21      48  189   0       0       45         2
         Josh Powell        0   51         22      85  117   0       0       25         2
         Kobe Bryant        0   93        315     213  882   0       0       93         3
          Lamar Odom        0  124        131     287  351   0       0       67         2
         Luke Walton        0   53         30      90  151   0       0       31         0
           Pau Gasol        0   78        221     389  513   0       0       78         5
       Sasha Vujacic        0   72         27      62  151   0       0       14         2
       Shannon Brown        0    3          0       6   17   0       0        4         0
             Sun Yue        0    1          0       0    1   0       0        1         0
        Trevor Ariza        1   84         57     161  279   0       0       45         4
 Vladimir Radmanovic        0   26          9      52   89   0       0       23         0
             Yue Sun        0    0          0       0    0   0       0        0         0

$home
              player ejection foul free throw rebound shot sub timeout turnover violation
                            0    1          0     338    0 706     172        6         7
       Adam Morrison        0    4          2       7    9   0       0        2         0
        Andrew Bynum        0   97        137     237  275   0       0       47         4
          Chris Mihm        0   13          4      20   23   0       0        5         0
         D.J. Mbenga        0   20          2      12   31   0       0        9         5
        Derek Fisher        0   91         58      97  337   0       0       44         3
             Jackson        0    0          0       0    0   0       0        0         0
       Jordan Farmar        0   48         54      62  200   0       0       42         2
         Josh Powell        0   48         26      85  111   0       0       25         2
         Kobe Bryant        0   87        214     197  737   0       0      107         4
          Lamar Odom        0  109        109     312  314   0       0       66         1
         Luke Walton        0   45         22      82  138   0       0       32         0
           Pau Gasol        0   81        202     363  480   0       0       70         1
       Sasha Vujacic        0   81         43      66  224   0       0       18         2
       Shannon Brown        0    6          9      14   25   0       0        5         0
             Sun Yue        0    4          0       0    5   0       0        0         0
        Trevor Ariza        0   75        102     173  299   0       0       38         3
 Vladimir Radmanovic        0   22         16      60  114   0       0       21         2
             Yue Sun        0    4          0       0    3   0       0        2         0
  
```

With tabyl you can also use the adorn commands to add percentages. For basketball this would help see what players you would be analyzing when looking at team shot data.

```r
lakers_shot = lakersd %>% filter(etype == "shot")

lakers_shot %>%
#Create tabyl
  tabyl(player,result) %>%
#Add a totals row
  adorn_totals(where = c("row","col")) %>% 
#Add percentages of total shots taken by players  
  adorn_percentages(denominator = "col") %>%
#Format to 1 decimal place  
  adorn_pct_formatting(digits = 1)%>%
#Include amount of observations  
  adorn_ns()
  
player          made        missed         Total
       Adam Morrison   0.1%    (4)   0.2%    (8)   0.2%   (12)
        Andrew Bynum   8.2%  (259)   6.0%  (207)   7.0%  (466)
          Chris Mihm   0.5%   (15)   0.7%   (25)   0.6%   (40)
         D.J. Mbenga   0.9%   (27)   0.9%   (30)   0.9%   (57)
        Derek Fisher   8.5%  (267)  10.9%  (379)   9.8%  (646)
       Jordan Farmar   4.9%  (153)   6.8%  (236)   5.9%  (389)
         Josh Powell   3.2%  (102)   3.6%  (126)   3.4%  (228)
         Kobe Bryant  24.1%  (757)  24.8%  (862)  24.5% (1619)
          Lamar Odom  10.6%  (332)   9.6%  (333)  10.1%  (665)
         Luke Walton   4.1%  (128)   4.6%  (161)   4.4%  (289)
           Pau Gasol  18.2%  (570)  12.2%  (423)  15.0%  (993)
       Sasha Vujacic   4.6%  (144)   6.7%  (231)   5.7%  (375)
       Shannon Brown   0.7%   (22)   0.6%   (20)   0.6%   (42)
             Sun Yue   0.0%    (0)   0.2%    (6)   0.1%    (6)
        Trevor Ariza   8.5%  (266)   9.0%  (312)   8.7%  (578)
 Vladimir Radmanovic   2.9%   (92)   3.2%  (111)   3.1%  (203)
             Yue Sun   0.1%    (2)   0.0%    (1)   0.0%    (3)
               Total 100.0% (3140) 100.0% (3471) 100.0% (6611)  
```

This already shows how useful cross tabs can be spotting trends in data, if you were to just do analysis on the Lakers you may miss that Kobe Bryant was greatly skewing the data without them.


