---
title: Non-standard errors
parent: Ordinary least squares
grand_parent: Estimation
nav_order: 2
---

# Non-standard errors

## Robust standard errors

### R
```r
library(estimatr)

lm_robust(mpg ~ cyl + hp + wt, data = mtcars)
```
