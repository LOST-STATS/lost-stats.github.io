---
title: Non-standard errors
parent: OLS
grand_parent: Estimation
nav_order: 1
---

# Non-standard errors

## Robust standard errors

```r
library(estimatr)

lm_robust(mpg ~ cyl + hp + wt, data=mtcars)
```
