---
title: ANOVA
parent: Ordinary Least Squares
grand_parent: Model Estimation
has_children: false
nav_order: 1
mathjax: true
---

# ANOVA

ANOVA, meaning *Analysis of Variance*, is a statistical test that tells us about the differences between the means of two or more independent groups. ANOVA tests are most often used when looking at interaction effects between categorical independent variables and continuous dependent variables.


The null and alternative hypothesis of an ANOVA test are:  

   $$H_0:  \mu_1 = \mu_2 = \ldots = \mu_n$$  

   $$H_1:  \exists i, j : \mu_i \neq \mu_j$$

The null hypothesis ($H_0$) states that the means of the different levels are all equal, while the alternative hypothesis ($$H_1$$) states that at least one mean is different than that of the other variables.

### Common Variations of ANOVA

-   **One-way ANOVA**
    -   Used to determine relationship between a single variable and the response variable
    -   *Example:* Looking at student scores on  standardized test for all students in a school grouped by grade
-   **Two-way ANOVA**
    -   Used when examining two categorical independent variables and their relationship with the dependent variable
    -   Categorized as a type of factorial ANOVA
-   **Factorial (N-way) ANOVA**
    -   Test two or more categorical independent variables and their relationships to the dependent variable
    -   Terms *N-way* and *Factorial* are often used synonymous to describe testing that involves multiple independent variables and a single dependent variable
    -   *Example:* Measuring growth rate of plants based on the manipulation of watering frequency and exposure to sunlight

For more information, see [Wikipedia: Analysis of Variance](https://en.wikipedia.org/wiki/Analysis_of_variance#Assumptions) and [Statology: One-Way vs. Two-Way ANOVA](https://www.statology.org/one-way-vs-two-way-anova/)

## Keep in Mind

### Assumptions

There are strict assumptions made about data and variables with ANOVA testing methods:

1.  ***Normal distribution***
    -   Observations that are taken have been randomly selected from the population are independent from each other
    -   More likely to be a potential concern with data sets and sample sizes
2.  ***Independence of variables***
    -   Observations that are taken have been randomly selected from the population are are independent of each other
3.  ***Homoscedasticity***
    -   Variation around mean is similar for variables being tested
    -   Uses F-statistic to test homogeneity of variance in means
4.  **Equal Sample Sizes**
    -   If multiple groups are being tested, the number of observations included in the sample must be equal for each group

For more information and examples, see [BeST: Checking Assumptions of One-Way ANOVA](https://yieldingresults.org/wp-content/uploads/2015/03/Checking_ANOVA_assumptions.html)

### Advantages

-   Can be superior to other tests (such as z-test) since ANOVA allows us to make comparisons of multiple variables
-   Reduces Type I error rate
    -   Very important to consider depending on the context
-   Provides robust statistical inference if assumptions of data are met

### Disadvantages

-   Adding additional variables will increase test complexity and difficulty interpreting results
-   ANOVA test results only provide limited insight into potential interactions, [post hoc tests](https://stats.libretexts.org/Bookshelves/Applied_Statistics/Book%3A_An_Introduction_to_Psychological_Statistics_(Foster_et_al.)/11%3A_Analysis_of_Variance/11.08%3A_Post_Hoc_Tests#:~:text=A%20post%20hoc%20test%20is,will%20give%20us%20similar%20answers.) are often required to gain more robust insight into statistically significant ANOVA results
-   If the test tells us to reject the null hypothesis of equal means, it may not be clear which variable is having the explanatory effect if comparing multiple groups
-   Must check assumptions prior to using ANOVA to test data
    -   Data might not have all characteristics meeting the strict assumptions of ANOVA

## Also Consider

Different variations of ANOVA testing that can be used to better suit the context of the analysis. A few examples include:

-   **ANCOVA**
    -   Stands for [Analysis of Covariance](https://www.lehigh.edu/~wh02/ancova.html)
    -   Used to test interaction effects between independent categorical variables in addition to relationship with continuous dependent variable
    -   *Example:* Looking at relationship between hours spent studying and grade level (the independent variables) and standardizes test score (dependent variable), where it is suspected that there may be an interaction between independent variables; time spent studying would be a *covariate*
-   **MANOVA**
    -   Stands for [Multivariate Analysis of Variance](https://www.statisticssolutions.com/free-resources/directory-of-statistical-analyses/manova/)
    -   Looks at effects of multiple independent categorical variables and multiple continuous dependent variables and potential interacting effects
    -   Can be further classified into one-way and two-way tests
    -   *Example:* Testing the relationship between level of education (the independent variable) with standardized test scores and annual income (the dependent variables)
-   **Within-Subjects ANOVA**
    -   Also referred to as *Repeated Measures ANOVA*
    -   Can be used to examine differences between two or more time periods
    -   Frequently used when looking at test results for pre-treatment and post-treatment variable interaction
    -   *Example:* Looking at dependent variable of median income based on independent variable of level of education, measured in multiple different time periods over several years; the *Panel Study of Income Dynamics (PSID)*, more on that found [here](https://psidonline.isr.umich.edu/)

For more examples, see [Statistic Solutions: The Various Forms of ANOVA](https://www.statisticssolutions.com/the-various-forms-of-anova/)

# Implementations

## R

We will be using the `mtcars` data set included in the base program

Prior to running test, check underlying assumptions for the data

```r
# Selecting variables of interest
cars = mtcars[, c("mpg", # Dependent/response variable
                  "wt")] # Independent variable


# 1. Creating histograms to check for uniform distribution
hist(cars$mpg)
hist(cars$wt)

# 2. Using Chi Square test to check for variable independence
chisq.test(cars$mpg, cars$wt)

# 3. Creating model to check for variation around mean
mod = lm(formula = mpg~wt, data = cars)
plot(mod)
```

If we can verify these assumptions, then we can be confident that the information obtained from the ANOVA test will be an accurate measurement of the true relationship between the variables.

```r
# ANOVA test and summary
anova(mod)

#> Analysis of Variance Table
#> 
#> Response: mpg
#>           Df Sum Sq Mean Sq F value    Pr(>F)    
#> wt         1 847.73  847.73  91.375 1.294e-10 ***
#> Residuals 30 278.32    9.28                      
#> ---
#> Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
```

In this example, we can see that `wt` is significant on all levels. Therefore, we can reject our null hypothesis that both means being tested are equal and accept our alternative hypothesis.


