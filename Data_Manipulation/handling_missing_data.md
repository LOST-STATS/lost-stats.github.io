---
title: Handling Missing Data
parent: Data Manipulation
has_children: false
nav_order: 1
mathjax: true
---

Introduction

# Handling Missing Data
Missing data occurs when some observations in a dataset do not have recorded values for certain variables. This is common in surveys, experiments, and administrative datasets.
Handling missing data is an important step in data cleaning. If missing values are ignored, they can lead to biased results or reduce the reliability of statistical models.
This page introduces several common techniques for identifying and handling missing data.

## Keep in Mind
- Missing data may occur because of survey non-response, data entry errors, or equipment failures.
- Some statistical software automatically removes rows with missing values.
- Removing missing data can reduce the sample size.
- Imputation methods estimate missing values but may introduce bias if used incorrectly.

## Also Consider
- Mean Imputation – replacing missing values with the mean of the variable.
- Multiple Imputation – generating several possible values for missing data to reflect uncertainty.
- Data Cleaning – identifying incorrect or inconsistent data.

Implementation

Python Example

```python
import pandas as pd

# Load dataset
data = pd.read_csv("data.csv")

# Check missing values
print(data.isnull().sum())

# Drop rows with missing values
data_clean = data.dropna()

# Replace missing values with mean
data['income'] = data['income'].fillna(data['income'].mean())
```

R Example

```r
data <- read.csv("data.csv")

# Check missing values
colSums(is.na(data))

# Remove rows with missing values
data_clean <- na.omit(data)

# Replace missing values with mean
data$income[is.na(data$income)] <- mean(data$income, na.rm = TRUE)
```

Excel Instructions

## Excel

1. Open your dataset in Excel.
2. Select the column with missing values.
3. Use the Filter tool to locate blank cells.
4. Replace blank cells with a value such as the mean.
5. Alternatively, remove rows containing missing values.



