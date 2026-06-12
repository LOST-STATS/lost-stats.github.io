---
title: A/B Testing
parent: Machine Learning
has_children: false
nav_order: 1
mathjax: true
---

# A/B Testing

A/B testing is a controlled experiment used to compare two variants of a product, webpage, or feature. One version is usually the current experience (A, or "control") and the other is a modified version (B, or "treatment"). The goal is to determine whether the new version produces a meaningful change in a pre-defined outcome, such as conversion rate, click-through rate, or revenue.

A/B testing is primarily an experimental design process rather than a single statistical test. The most important parts are choosing the metric, randomizing assignment, calculating the sample size for adequate power, and pre-specifying how and when the experiment will stop. The actual comparison of the two variants can be implemented with different inferential tests depending on the outcome type and software environment.

A/B tests are widely used in product development and online experimentation because they provide a direct way to measure causal effects from a randomized comparison.

## Assumptions and Considerations

A successful A/B test depends on several assumptions and practical decisions:

- Random assignment: users or units should be assigned to A or B at random so that the groups are comparable.
- Stable unit treatment value assumption (SUTVA): one user's assignment should not affect another user's outcome.
- Identical measurement: the outcome should be measured consistently for both groups over the same period.
- Sufficient sample size: a test must be large enough to detect the expected effect size with acceptable statistical power.
- Clear primary metric: choose the most important metric before the test begins and avoid changing it partway through.
- Duration and timing: run the experiment long enough to capture typical user behavior, while avoiding seasonality or external events that could bias results.
- Sample ratio: maintain the intended allocation ratio (for example, 50/50) and watch for traffic or instrumentation issues that shift the ratio.
- Power and stopping rules: calculate sample size before the test starts, choose a minimum detectable effect, and decide whether the test will use a fixed horizon or a pre-registered sequential stopping rule.

## Design Considerations: power, stopping rules, and test choice

A/B testing is not just the final hypothesis test. It is the combination of experiment setup, metric selection, randomization, and analysis plan. Two important elements are statistical power (making sure the test can detect a practically meaningful effect) and stopping rules (avoiding bias from peeking or stopping early).

The examples in this page show one common analysis path for binary conversion data. In practice, A/B testing can use different software and equivalent inference approaches:

- a two-proportion z-test or an equivalent chi-squared test for binary conversion metrics,
- a t-test or regression for continuous outcomes,
- regression adjustments when covariates are needed to improve precision.

Both the Python and R examples below use the same A/B setup: two variants, conversion counts, visitor totals, and the same two-proportion z-test for comparison. The important point is that the underlying experimental design is what makes this A/B test, not the specific language used for the final comparison.

## Python Implementation Example

### Two-Proportion Z-Test

When comparing conversion rates between two groups, a two-proportion z-test is the standard statistical approach. This test evaluates whether the difference in success rates between two groups is statistically significant.

The test statistic is calculated as:

$$
Z = \frac{p_1 - p_2}{\sqrt{p (1 - p) \left(\frac{1}{n_1} + \frac{1}{n_2} \right)}}
$$

where $p_1$ and $p_2$ are the conversion rates for variants A and B, $n_1$ and $n_2$ are the sample sizes, and $p$ is the pooled proportion across both groups. A large absolute value of $Z$ (typically $|Z| > 1.96$ for a 0.05 significance level) suggests the variants differ significantly.

The example below calculates the two-proportion z-test manually, which makes the computation transparent and matches the R implementation:

```python
import pandas as pd
from scipy import stats
import numpy as np

# Example results for two variants
results = pd.DataFrame(
    {
        "variant": ["A", "B"],
        "conversions": [120, 150],
        "visitors": [2000, 2100],
    }
)

results["rate"] = results["conversions"] / results["visitors"]
print(results)

# Extract values
n1 = 2000
n2 = 2100
p1 = 120 / n1
p2 = 150 / n2

# Calculate pooled proportion
p_pooled = (120 + 150) / (n1 + n2)

# Calculate the two-proportion z-test statistic
z_stat = (p2 - p1) / np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))

# Calculate p-value (two-sided)
p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

# Calculate 95% confidence interval for the difference
se_diff = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
ci_lower = (p2 - p1) - 1.96 * se_diff
ci_upper = (p2 - p1) + 1.96 * se_diff

# Calculate lift
lift = (p2 - p1) / p1

# Print results
print(f"Variant A rate: {p1:.4f}")
print(f"Variant B rate: {p2:.4f}")
print(f"z-statistic: {z_stat:.3f}")
print(f"p-value: {p_value:.4f}")
print(f"Lift: {lift * 100:.2f} %")
print(f"95% CI for difference: {ci_lower:.4f} to {ci_upper:.4f}")
```

A few notes on the example:

- The pooled proportion `p_pooled` combines both groups to estimate the common proportion under the null hypothesis.
- The z-statistic is calculated the same way as in the R example.
- The p-value is calculated from the standard normal distribution using `scipy.stats.norm.cdf()`.
- The confidence interval uses the standard normal approximation, matching the R implementation.
- Both Python and R perform the identical two-proportion z-test with the same output.

## R Implementation Example

### Two-Proportion Z-Test

In R, we can perform the same two-proportion z-test to compare conversion rates across groups. The test evaluates whether the difference in success rates between two groups is statistically significant.

Although R's `prop.test()` function is commonly used in practice and reports an equivalent chi-squared statistic, the example below computes the two-proportion z-test directly so that the calculations match the Python implementation exactly.

The example below demonstrates how to calculate and interpret the two-proportion z-test for variants:

```r
# Example results for two variants
variant_a_conversions <- 120
variant_a_visitors <- 2000

variant_b_conversions <- 150
variant_b_visitors <- 2100

# Combine data
successes <- c(variant_a_conversions, variant_b_conversions)
trials <- c(variant_a_visitors, variant_b_visitors)

# Calculate conversion rates
rate_a <- variant_a_conversions / variant_a_visitors
rate_b <- variant_b_conversions / variant_b_visitors

# Calculate pooled proportion
p_pooled <- sum(successes) / sum(trials)

# Calculate the two-proportion z-test statistic
z_stat <- (rate_b - rate_a) / sqrt(p_pooled * (1 - p_pooled) * (1/variant_a_visitors + 1/variant_b_visitors))

# Calculate p-value (two-sided)
p_value <- 2 * (1 - pnorm(abs(z_stat)))

# Calculate 95% confidence interval for the difference
se_diff <- sqrt(p_pooled * (1 - p_pooled) * (1/variant_a_visitors + 1/variant_b_visitors))
ci_lower <- (rate_b - rate_a) - 1.96 * se_diff
ci_upper <- (rate_b - rate_a) + 1.96 * se_diff

# Calculate lift
lift <- (rate_b - rate_a) / rate_a

# Print results
print(paste("Variant A rate:", round(rate_a, 4)))
print(paste("Variant B rate:", round(rate_b, 4)))
print(paste("z-statistic:", round(z_stat, 3)))
print(paste("p-value:", round(p_value, 4)))
print(paste("Lift:", round(lift * 100, 2), "%"))
print(paste("95% CI for difference:", round(ci_lower, 4), "to", round(ci_upper, 4)))
```

A few notes on the example:

- The pooled proportion `p_pooled` combines both groups to estimate the common proportion under the null hypothesis.
- The z-statistic is calculated the same way as in the Python example.
- The p-value is calculated from the standard normal distribution.
- The confidence interval uses the same formula as in Python.
- Both Python and R perform the identical two-proportion z-test.

## Interpretation of Results

When interpreting A/B test results, focus on both statistical and practical significance:

- A low p-value (commonly below 0.05) means the observed difference is unlikely to have occurred by chance, under the null hypothesis of no difference.
- The sign of the observed lift indicates whether variant B performed better or worse than variant A.
- Confidence intervals give a range of plausible values for the true effect and help judge how uncertain the estimate is.
- Even a statistically significant result may be too small to matter in business terms. Compare the effect size to a pre-defined minimum detectable effect.
- If the p-value is not significant, it does not prove that the variants are equal; it may mean the test was underpowered or the effect is smaller than expected.

## Common Pitfalls and Limitations

A/B testing is a powerful tool, but it has limitations and common failure modes:

- Multiple comparisons: testing many variants or metrics increases the chance of false positives unless you adjust for it.
- Peeking or stopping early: repeatedly checking results and ending the test once significance appears inflates the false positive rate.
- Underpowered tests: too few observations can make it impossible to detect a real effect.
- Non-random assignment: if the groups differ in meaningful ways, the experiment is not a valid causal comparison.
- External changes: product launches, marketing campaigns, or seasonality can distort the comparison.
- Mis-specified metrics: optimizing the wrong metric may produce outcomes that are easier to measure but less valuable.
- User behavior changes: novelty effects, learning effects, or long-term retention may not be visible in a short-term A/B test.
- Data quality issues: missing data, duplicate users, or instrumentation errors can lead to misleading conclusions.

## Keep in Mind

- A/B tests are most useful when the intervention is clearly defined and the target metric is well chosen.
- Always plan the experiment, the metric, and the required sample size before launching.
- Use the results as one input in a broader decision process, rather than treating a single test as definitive.

## Also Consider

- If you are interested in how A/B testing fits into broader predictive and experimental workflows, review the [Machine Learning]({{ "/Machine_Learning/Machine_Learning.html" | relative_url }}) overview.
