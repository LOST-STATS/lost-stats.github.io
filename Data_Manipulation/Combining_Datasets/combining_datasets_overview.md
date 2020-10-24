---
title: Combining Datasets
parent: Data Manipulation
has_children: true
nav_order: 1
---

# Combining Datasets Overview

There are two main ways to combine data: [vertically]({{ "/Data_Manipulation/Combining_Datasets/combining_datasets_vertical_combination.html" | relative_url }}) and [horizontally]({{ "/Data_Manipulation/Combining_Datasets/combining_datasets_horizontal_merge_deterministic.html" | relative_url }}). That is, you can want to combine observations (adding new variables) or combine variables (adding new observations). This is perhaps easiest to show visually:

Individual Name Info
|Name| ID |
|--|--|
|John Smith|A63240|
|Desiree Thomas|B78242|


Individual Age Info
|ID | Age |
|--|--|
|B78242|22|
|A63240|27|

In the case above, we would like to combine two datasets, the Individual Name Info and the Individual Date Info, that have different information about the same people, who are identified by the ID variable. The result from the merge would be to have a new dataset with more columns than the original datasets because it contains all of the information for each individual from both of the original datasets. Here we have to combine the files according to the ID variable, placing the information from observations with the same ID on the same row in the combined dataset.

Alternatively, the below example has two datasets that collect the same information about different people. We would like to combine these datasets vertically, with the result containing more rows than the original dataset, because it contains all of the people that are present in each of the original datasets. Here we combine the files based on the name or position of the columns in the dataset.

|Name|ID|Age|
|--|--|--|
|John Smith|A63240|22|
|Desiree Thomas|B78242|27|

|Name|ID|Age|
|--|--|--|
|Teresa Suarez|Y34208|19|
|Donald Akliberti|B72197|34|

These ways of combining data are referred to by different names across different programming languages, but will largely be referred to by one common set of terms (used by Stata and Python’s Pandas): merge for horizontal combination and append for for vertical combination.
