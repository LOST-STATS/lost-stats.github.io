---
title: Handling Missing Data
parent: Data Manipulation
has_children: false
nav_order: 1
mathjax: true
---

# Handling Missing Data

Missing data is common in applied econometrics and in most forms of statistical work. Some observations may be blank, unavailable, or recorded using a software-specific missing-value code. This page shows how to identify missing values, count them, remove incomplete observations, and fill in missing values using common statistical software.

## Keep in Mind

- Missing data can reduce your sample size and change your results.
- Different software packages represent missing values differently. Common markers include `NA`, `.`, and blank cells.
- Dropping observations with missing values is simple, but it can remove a large amount of information.
- Filling in missing values can be useful for some tasks, but the choice of method should be justified.
- Before making changes, it is a good idea to check how much missing data there is and which variables are affected.
- Missingness is not always random. If certain types of observations are more likely to be missing, this can affect inference.

## Also Consider

- [Combining Datasets]({{ "/Data_Manipulation/combining_datasets.html" | relative_url }}) because missing values often appear after merges.
- [Creating Dummy Variables]({{ "/Data_Manipulation/creating_dummy_variables.html" | relative_url }}) if you want to create an indicator for whether a value is missing.
- [Determine the Observation Level of a Data Set]({{ "/Data_Manipulation/determine_the_observation_level_of_a_data_set.html" | relative_url }}) to make sure the data structure is correct before cleaning.
- [Rowwise Calculations]({{ "/Data_Manipulation/rowwise_calculations.html" | relative_url }}) if you need to work across variables while checking for incomplete observations.

## Implementations

### Python

```python
# If needed, install pandas first:
# pip install pandas

import pandas as pd
import numpy as np

# Create a small example dataset
df = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "income": [50000, np.nan, 42000, 61000],
    "age": [25, 31, np.nan, 45]
})

# View the data
print(df)

# Check which entries are missing
print(df.isna())

# Count missing values in each column
print(df.isna().sum())

# Drop rows with any missing values
df_dropped = df.dropna()
print(df_dropped)

# Fill missing values with the column mean
df_filled = df.copy()
df_filled["income"] = df_filled["income"].fillna(df_filled["income"].mean())
df_filled["age"] = df_filled["age"].fillna(df_filled["age"].mean())

print(df_filled)
