---
title: A/B Testing
parent: Machine Learning
has_children: false
nav_order: 1
mathjax: true
---

# A/B Testing

A/B testing is a controlled experiment used to compare two variants of a product, webpage, or feature. One version is usually the current experience (A, or "control") and the other is a modified version (B, or "treatment"). The goal is to determine whether the new version produces a meaningful change in a pre-defined outcome, such as conversion rate, click-through rate, or revenue.

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

## Python Implementation Example

### Two-Proportion Z-Test

When comparing conversion rates between two groups, a two-proportion z-test is the standard statistical approach. This test evaluates whether the difference in success rates between two groups is statistically significant.

The test statistic is calculated as:

$$
Z = \frac{p_1 - p_2}{\sqrt{p (1 - p) \left(\frac{1}{n_1} + \frac{1}{n_2} \right)}}
$$

where $p_1$ and $p_2$ are the conversion rates for variants A and B, $n_1$ and $n_2$ are the sample sizes, and $p$ is the pooled proportion across both groups. A large absolute value of $Z$ (typically $|Z| > 1.96$ for a 0.05 significance level) suggests the variants differ significantly.

The example below uses the `statsmodels` library, which is a common choice for simple A/B test statistics:

```python
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest, proportion_confint

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

successes = results["conversions"].values
trials = results["visitors"].values

stat, pvalue = proportions_ztest(successes, trials, alternative="two-sided")
print(f"z-statistic: {stat:.3f}")
print(f"p-value: {pvalue:.4f}")

# Confidence interval for the difference in proportions

diff = results.loc[1, "rate"] - results.loc[0, "rate"]
ci_low, ci_high = proportion_confint(
    successes[1] - successes[0], trials[1] + trials[0], method="wilson"
)

print(f"Observed lift: {diff:.3%}")
print(f"Approximate confidence interval: {ci_low:.3%}, {ci_high:.3%}")
```

A few notes on the example:

- `results` holds the conversion counts for both variants.
- `proportions_ztest` tests whether the two conversion rates differ.
- `proportion_confint` can be used to obtain a rough confidence interval for the estimated difference.

## R Implementation Example

### Chi-Squared Test for Proportions

In R, the `prop.test()` function performs a chi-squared test to compare proportions across groups.

Internally, this test is equivalent to the two-proportion z-test used in the Python example for the two-group case, $\chi^2 = z^2$. The test evaluates whether observed success counts differ significantly from what we would expect under the null hypothesis of equal proportions.

The chi-squared test statistic is constructed by comparing observed cell counts in a contingency table to expected counts under independence:

$$
\chi^2 = \sum \frac{(O - E)^2}{E}
$$

where $O$ is the observed count and $E$ is the expected count for each cell. A larger $\chi^2$ value indicates a more significant difference between the groups.

The example below demonstrates how to use `prop.test()` to compare conversion rates between variants:

```r
# Example results for two variants
variant_a_conversions <- 120
variant_a_visitors <- 2000

variant_b_conversions <- 150
variant_b_visitors <- 2100

# Combine data
successes <- c(variant_a_conversions, variant_b_conversions)
trials <- c(variant_a_visitors, variant_b_visitors)

# Run two-proportion z-test
test_result <- prop.test(successes, trials, alternative = "two.sided")
print(test_result)

# Extract key statistics
p_value <- test_result$p.value
conf_int <- test_result$conf.int

# Calculate conversion rates and lift
rate_a <- variant_a_conversions / variant_a_visitors
rate_b <- variant_b_conversions / variant_b_visitors
lift <- (rate_b - rate_a) / rate_a

print(paste("Variant A rate:", round(rate_a, 4)))
print(paste("Variant B rate:", round(rate_b, 4)))
print(paste("Lift:", round(lift * 100, 2), "%"))
print(paste("p-value:", round(p_value, 4)))
print(paste("95% CI for difference:", round(conf_int[1], 4), "to", round(conf_int[2], 4)))
```

A few notes on the example:

- `prop.test()` conducts a chi-squared test comparing proportions across two or more groups.
- The function returns p-values, confidence intervals, and test statistics automatically.
- `rate_a` and `rate_b` are the conversion rates for each variant, and `lift` shows the percentage change from A to B.

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
