# Multiple Imputation

Many data sets have missing values, where some observations are incomplete for certain variables. Surveys, administrative records, and labor datasets frequently contain observations where variables like education or income are not recorded. See the table below for one example.

| id | wage | educ | exper | female |
|----|------|------|-------|--------|
| 1 | 22 | 16 | 5 | 0 |
| 2 | 18 | 14 | 3 | 1 |
| 3 | 25 | NA | 7 | 0 |
| 4 | 20 | 13 | 4 | 1 |
| 5 | 27 | 17 | 8 | 0 |
| 6 | 19 | NA | 6 | 1 |
| 7 | 24 | 16 | 9 | 0 |
| 8 | 21 | 15 | 5 | 1 |
| 9 | 28 | 18 | 10 | 0 |
| 10 | 23 | NA | 7 | 1 |
| 11 | 17 | 12 | 2 | 1 |
| 12 | 26 | 17 | 8 | 0 |
| 13 | 22 | 15 | 4 | 0 |
| 14 | 20 | NA | 5 | 1 |
| 15 | 29 | 19 | 11 | 0 |
| 16 | 18 | 13 | 3 | 1 |
| 17 | 27 | 17 | 9 | 0 |
| 18 | 21 | 14 | 4 | 1 |
| 19 | 30 | 20 | 12 | 0 |
| 20 | 24 | NA | 6 | 1 |

Here, we have data where the variable *educ* is missing in five observations.

Multiple imputation is a principled method for handling missing data. Rather than filling in each missing value once, it generates several plausible versions of the complete dataset, estimates the model in each one, and then combines the results. This approach preserves both the information in incomplete observations and the uncertainty introduced by missing data.

Multiple imputation is typically justified under the **Missing at Random (MAR)** assumption. Under MAR, the probability that education is missing depends only on observed variables (such as experience and gender), not on the unobserved value of education itself once those variables are taken into account. When this assumption is plausible and the imputation model is well specified, multiple imputation can produce unbiased estimates with valid standard errors.

Our goal is to estimate the wage regression

$$
wage_i = \beta_0 + \beta_1 educ_i + \beta_2 exper_i + \beta_3 female_i + u_i
$$

using multiple imputation so that we retain all observations and obtain valid standard errors and confidence intervals.

## How Multiple Imputation Works

Multiple imputation proceeds in three steps:

1. **Imputation**: Create $m$ completed datasets by replacing missing values with draws from a model based on observed data  
2. **Analysis**: Estimate the regression model separately in each imputed dataset  
3. **Pooling**: Combine estimates using **Rubin's rules**

If $\hat{\beta}^{(j)}$ is the estimate from dataset $j = 1, \dots, m$, the pooled estimate is:

$$
\bar{\beta} = \frac{1}{m} \sum_{j=1}^{m} \hat{\beta}^{(j)}
$$

The variance combines:

- **within-imputation variance** (average of estimated variances)  
- **between-imputation variance** (variation across estimates)  

This step is essential. Using only a single imputed dataset ignores between-imputation uncertainty and leads to incorrect inference.

## Also Consider

- If the goal is to drop missing observations, see **Complete-Case Analysis**  
- If using only one filled-in dataset, see **Single Imputation**  

## Implementations

The `mice` package (R) and its Julia counterpart `Mice.jl` implement the full workflow, including proper pooling via Rubin's rules. Python and Stata provide similar functionality.

---

### Julia

The `Mice.jl` package (inspired by R's `mice`) handles imputation and pooling.

```julia
using DataFrames
using Mice
using GLM
using Random

Random.seed!(123)

data = DataFrame(
    id = 1:20,
    wage = [22, 18, 25, 20, 27, 19, 24, 21, 28, 23, 17, 26, 22, 20, 29, 18, 27, 21, 30, 24],
    educ = [16, 14, missing, 13, 17, missing, 16, 15, 18, missing, 12, 17, 15, missing, 19, 13, 17, 14, 20, missing],
    exper = [5, 3, 7, 4, 8, 6, 9, 5, 10, 7, 2, 8, 4, 5, 11, 3, 9, 4, 12, 6],
    female = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1]
)

imputedData = mice(data, m = 5)

analyses = with(imputedData, d ->
    glm(@formula(wage ~ educ + exper + female), d, Normal(), IdentityLink())
)

pooled = pool(analyses)

println(pooled)
````

---

### Python

Using `miceforest` for chained equations and `statsmodels` for estimation.

```python

import pandas as pd
import miceforest as mf
import statsmodels.api as sm
import numpy as np

data = pd.DataFrame({
    'id': range(1, 21),
    'wage': [22, 18, 25, 20, 27, 19, 24, 21, 28, 23, 17, 26, 22, 20, 29, 18, 27, 21, 30, 24],
    'educ': [16, 14, np.nan, 13, 17, np.nan, 16, 15, 18, np.nan, 12, 17, 15, np.nan, 19, 13, 17, 14, 20, np.nan],
    'exper': [5, 3, 7, 4, 8, 6, 9, 5, 10, 7, 2, 8, 4, 5, 11, 3, 9, 4, 12, 6],
    'female': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1]
})

kernel = mf.ImputationKernel(data, num_datasets=5, random_state=123)
kernel.mice(5)

coefs = []
vars_ = []

for i in range(kernel.num_datasets):
    comp = kernel.complete_data(dataset=i)
    X = sm.add_constant(comp[['educ', 'exper', 'female']])
    y = comp['wage']
    model = sm.OLS(y, X).fit()
    coefs.append(model.params.values)
    vars_.append(model.cov_params().values)

coefs = np.array(coefs)      # shape: (m, k)
vars_ = np.array(vars_)      # shape: (m, k, k)

m = coefs.shape[0]

# Pooled coefficient vector
pooled_coefs = np.mean(coefs, axis=0)

# Within-imputation variance
within_var = np.mean(vars_, axis=0)

# Between-imputation variance
between_var = np.cov(coefs, rowvar=False, ddof=1)

# Rubin's Rules total variance
pooled_var = within_var + (1 + 1/m) * between_var

# Standard errors
pooled_se = np.sqrt(np.diag(pooled_var))

results = pd.DataFrame({
    'coef': pooled_coefs,
    'se': pooled_se,
    't': pooled_coefs / pooled_se
}, index=['const', 'educ', 'exper', 'female'])

print(results)
```

---

### R

The key step is to estimate the model across all imputations and pool results using Rubin's rules.

```r
install.packages("mice")
library(mice)

data <- data.frame(
  id = 1:20,
  wage = c(22,18,25,20,27,19,24,21,28,23,17,26,22,20,29,18,27,21,30,24),
  educ = c(16,14,NA,13,17,NA,16,15,18,NA,12,17,15,NA,19,13,17,14,20,NA),
  exper = c(5,3,7,4,8,6,9,5,10,7,2,8,4,5,11,3,9,4,12,6),
  female = c(0,1,0,1,0,1,0,1,0,1,1,0,0,1,0,1,0,1,0,1)
)

md.pattern(data)

imp <- mice(data, m = 5, method = "pmm", seed = 123)

fit <- with(imp, lm(wage ~ educ + exper + female))

pooled <- pool(fit)

summary(pooled)
```

---

### Stata

Stata provides built-in support for multiple imputation.

```stata
clear
input id wage educ exper female
1 22 16 5 0
2 18 14 3 1
3 25 . 7 0
4 20 13 4 1
5 27 17 8 0
6 19 . 6 1
7 24 16 9 0
8 21 15 5 1
9 28 18 10 0
10 23 . 7 1
11 17 12 2 1
12 26 17 8 0
13 22 15 4 0
14 20 . 5 1
15 29 19 11 0
16 18 13 3 1
17 27 17 9 0
18 21 14 4 1
19 30 20 12 0
20 24 . 6 1
end

mi set mlong
mi register imputed educ

mi impute pmm educ wage exper female, add(5) rseed(123)

mi estimate: regress wage educ exper female
```

## Interpretation

By imputing missing education values and correctly pooling across multiple datasets, we retain all 20 observations rather than discarding incomplete cases. This improves statistical efficiency and produces valid standard errors that reflect uncertainty from missing data. Compared to complete-case analysis or single imputation, multiple imputation provides more reliable inference when the MAR assumption is reasonable and the imputation model is appropriately specified.


