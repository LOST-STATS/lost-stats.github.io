Propensity Score Matching
=========================

Propensity Score Matching(PSM) is a non-parametric method of estimating
a treatment effect in situations where randomization is not possible.
This method comes from [Rosenbaum & Rubin,
1983](https://www.jstor.org/stable/2335942?seq=1) and works by
estimating a propensity score which is the predicted probability that
someone received treatment based on the explanatory variables of
interest. This reduces bias in observational studies by balancing the
covariates between a group that received the treatment and a group that
did not, essentially attempting to replicate a randomized control trial.

Basic Workflow
--------------

Step One:

run a logistic regression where the outcome variable is a binary
indicator for whether or not someone received the treatment and gather
the estimate of the propensity score. The explanatory variables in this
case are the covariates that we might reasonably believe influence
treatment

Step Two:

Match those that received treatment with those that did not based on
propensity score. There are a number of different ways to perform this
matching including, but not limited to :

\*Nearest neighbor matching

\*Exact matching

\*Stratification matching

In this example we will focus on nearest neighor matching, which we will
use through th MatchIt package

Step Three:

Check the balance of the matched sample using the summary command. This
is good practice to ensure that the matching worked well and that the
constructed control and treatment groups have similar observable
characteristics.

Step Four;

Run analysis using this new sample which will give us an average
treatment effect.

Keep in Mind
------------

Propensity Score Matching is based on selection on observable
characteristics. This assume that the potential outcome is independent
of the treatment D conditional on the covariates.
*Y*<sub>*i*</sub>(1), *Y*<sub>*i*</sub>(0)⊥|*X*<sub>*i*</sub>

This is known as the Conditional Independence Assumption

Propensity Score Matching also requires us to make the Common Support or
Overlap Assumption.

0 &lt; *P**r*(*D*<sub>*i*</sub> = 1|*X**i* = *x*) &lt; 1

This assumption says that the probability that the treatment is equal to
1 for each level of x is between zero and one, or in other words there
are both treated and untreated units for each level of x.

Because Propensity Score Matching relies so heavily on these
assumptions, [Regression
Discontinuity](https://lost-stats.github.io/Model_Estimation/Research_Design/regression_discontinuity_design.html),
[Differences in
Differences](https://lost-stats.github.io/Model_Estimation/Research_Design/two_by_two_difference_in_difference.html),
and other quasi-experimental designs may provide more accurate and
robust results.

Further Resouces
----------------

A great place to find more information about the MatchIt package is on
the package’s [github site](https://github.com/kosukeimai/MatchIt).

Noah Greifer’s [Cran
Page](https://cran.r-project.org/web/packages/MatchIt/vignettes/MatchIt.html)
is another good resource for getting started using Propensity Score
Matchign in R.

Implemenation in R
------------------

Implementation can be done using the MatchIt package

Data comes from
[OpenIntro.org](https://www.openintro.org/data/index.php?data=smoking)

    ##load the packages we need.

    library(pacman)
    p_load(tidyverse, MatchIt)

    ##load data on smoking in the United Kingdom.

    smoking = read_csv("smoking.csv")

    ##turn smoking into a binary variable.
    smoking = smoking %>%mutate(smoke = if_else(smoke == "Yes",1,0))

    ##Step One: Run the logistic regression.

    ps_model = glm( smoke ~ gender+age+marital_status+ethnicity+region, data=smoking)

    #get a summary of the model
    summary(ps_model)

    ## 
    ## Call:
    ## glm(formula = smoke ~ gender + age + marital_status + ethnicity + 
    ##     region, data = smoking)
    ## 
    ## Deviance Residuals: 
    ##      Min        1Q    Median        3Q       Max  
    ## -0.55418  -0.27303  -0.15987   0.02787   0.96529  
    ## 
    ## Coefficients:
    ##                               Estimate Std. Error t value Pr(>|t|)    
    ## (Intercept)                   0.546000   0.083401   6.547 7.80e-11 ***
    ## genderMale                    0.021092   0.020945   1.007   0.3141    
    ## age                          -0.005006   0.000705  -7.101 1.82e-12 ***
    ## marital_statusMarried        -0.180542   0.036295  -4.974 7.22e-07 ***
    ## marital_statusSeparated      -0.064618   0.060647  -1.065   0.2868    
    ## marital_statusSingle         -0.076666   0.040876  -1.876   0.0609 .  
    ## marital_statusWidowed        -0.064849   0.045950  -1.411   0.1583    
    ## ethnicityBlack                0.005511   0.098925   0.056   0.9556    
    ## ethnicityChinese             -0.014203   0.104098  -0.136   0.8915    
    ## ethnicityMixed                0.137113   0.129648   1.058   0.2904    
    ## ethnicityRefused              0.135407   0.133987   1.011   0.3124    
    ## ethnicityUnknown              0.327998   0.303946   1.079   0.2807    
    ## ethnicityWhite                0.074726   0.067133   1.113   0.2658    
    ## regionMidlands & East Anglia -0.040008   0.038145  -1.049   0.2944    
    ## regionScotland                0.069128   0.047879   1.444   0.1490    
    ## regionSouth East              0.001382   0.041966   0.033   0.9737    
    ## regionSouth West              0.013819   0.047010   0.294   0.7688    
    ## regionThe North              -0.026368   0.038668  -0.682   0.4954    
    ## regionWales                  -0.024207   0.056625  -0.428   0.6691    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## (Dispersion parameter for gaussian family taken to be 0.1741188)
    ## 
    ##     Null deviance: 316.19  on 1690  degrees of freedom
    ## Residual deviance: 291.13  on 1672  degrees of freedom
    ## AIC: 1863.8
    ## 
    ## Number of Fisher Scoring iterations: 2

    ## Step Two: Match on propensity score.

    #does not apply in this situation, but need to make sure there are no missing values in the covariates we are choosing. 

    #in order to match use the matchit command, passing the function a formula, the data to use and the method, in this case, nearest neighor estimation.

    match = matchit(smoke ~ gender+age+marital_status+ethnicity+region, method = "nearest", data =smoking)

    ##Step 3: Check for Balance.
    summary(match)

    ## 
    ## Call:
    ## matchit(formula = smoke ~ gender + age + marital_status + ethnicity + 
    ##     region, data = smoking, method = "nearest")
    ## 
    ## Summary of Balance for All Data:
    ##                              Means Treated Means Control Std. Mean Diff.
    ## distance                            0.3083        0.2293          0.6482
    ## genderFemale                        0.5558        0.5756         -0.0398
    ## genderMale                          0.4442        0.4244          0.0398
    ## age                                42.7150       52.1969         -0.5860
    ## marital_statusDivorced              0.1378        0.0811          0.1644
    ## marital_statusMarried               0.3397        0.5268         -0.3951
    ## marital_statusSeparated             0.0523        0.0362          0.0721
    ## marital_statusSingle                0.3753        0.2118          0.3376
    ## marital_statusWidowed               0.0950        0.1441         -0.1674
    ## ethnicityAsian                      0.0190        0.0260         -0.0511
    ## ethnicityBlack                      0.0190        0.0205         -0.0108
    ## ethnicityChinese                    0.0119        0.0173         -0.0503
    ## ethnicityMixed                      0.0119        0.0071          0.0442
    ## ethnicityRefused                    0.0095        0.0071          0.0249
    ## ethnicityUnknown                    0.0024        0.0008          0.0326
    ## ethnicityWhite                      0.9264        0.9213          0.0195
    ## regionLondon                        0.1188        0.1039          0.0458
    ## regionMidlands & East Anglia        0.2185        0.2764         -0.1400
    ## regionScotland                      0.1211        0.0764          0.1372
    ## regionSouth East                    0.1544        0.1472          0.0198
    ## regionSouth West                    0.0998        0.0906          0.0307
    ## regionThe North                     0.2399        0.2559         -0.0375
    ## regionWales                         0.0475        0.0496         -0.0099
    ##                              Var. Ratio eCDF Mean eCDF Max
    ## distance                         1.0780    0.1869   0.2890
    ## genderFemale                          .    0.0198   0.0198
    ## genderMale                            .    0.0198   0.0198
    ## age                              0.7302    0.1200   0.2379
    ## marital_statusDivorced                .    0.0567   0.0567
    ## marital_statusMarried                 .    0.1871   0.1871
    ## marital_statusSeparated               .    0.0160   0.0160
    ## marital_statusSingle                  .    0.1635   0.1635
    ## marital_statusWidowed                 .    0.0491   0.0491
    ## ethnicityAsian                        .    0.0070   0.0070
    ## ethnicityBlack                        .    0.0015   0.0015
    ## ethnicityChinese                      .    0.0054   0.0054
    ## ethnicityMixed                        .    0.0048   0.0048
    ## ethnicityRefused                      .    0.0024   0.0024
    ## ethnicityUnknown                      .    0.0016   0.0016
    ## ethnicityWhite                        .    0.0051   0.0051
    ## regionLondon                          .    0.0148   0.0148
    ## regionMidlands & East Anglia          .    0.0579   0.0579
    ## regionScotland                        .    0.0448   0.0448
    ## regionSouth East                      .    0.0072   0.0072
    ## regionSouth West                      .    0.0092   0.0092
    ## regionThe North                       .    0.0160   0.0160
    ## regionWales                           .    0.0021   0.0021
    ## 
    ## 
    ## Summary of Balance for Matched Data:
    ##                              Means Treated Means Control Std. Mean Diff.
    ## distance                            0.3083        0.3074          0.0079
    ## genderFemale                        0.5558        0.5511          0.0096
    ## genderMale                          0.4442        0.4489         -0.0096
    ## age                                42.7150       42.0641          0.0402
    ## marital_statusDivorced              0.1378        0.1306          0.0207
    ## marital_statusMarried               0.3397        0.3729         -0.0702
    ## marital_statusSeparated             0.0523        0.0546         -0.0107
    ## marital_statusSingle                0.3753        0.3682          0.0147
    ## marital_statusWidowed               0.0950        0.0736          0.0729
    ## ethnicityAsian                      0.0190        0.0190          0.0000
    ## ethnicityBlack                      0.0190        0.0166          0.0174
    ## ethnicityChinese                    0.0119        0.0048          0.0658
    ## ethnicityMixed                      0.0119        0.0119          0.0000
    ## ethnicityRefused                    0.0095        0.0071          0.0245
    ## ethnicityUnknown                    0.0024        0.0024          0.0000
    ## ethnicityWhite                      0.9264        0.9382         -0.0455
    ## regionLondon                        0.1188        0.1116          0.0220
    ## regionMidlands & East Anglia        0.2185        0.2185          0.0000
    ## regionScotland                      0.1211        0.1235         -0.0073
    ## regionSouth East                    0.1544        0.1496          0.0131
    ## regionSouth West                    0.0998        0.0855          0.0476
    ## regionThe North                     0.2399        0.2613         -0.0501
    ## regionWales                         0.0475        0.0499         -0.0112
    ##                              Var. Ratio eCDF Mean eCDF Max Std. Pair Dist.
    ## distance                         1.0142    0.0019   0.0261          0.0098
    ## genderFemale                          .    0.0048   0.0048          0.8509
    ## genderMale                            .    0.0048   0.0048          0.8509
    ## age                              0.9215    0.0127   0.0404          0.6383
    ## marital_statusDivorced                .    0.0071   0.0071          0.6272
    ## marital_statusMarried                 .    0.0333   0.0333          0.5417
    ## marital_statusSeparated               .    0.0024   0.0024          0.3949
    ## marital_statusSingle                  .    0.0071   0.0071          0.6623
    ## marital_statusWidowed                 .    0.0214   0.0214          0.4293
    ## ethnicityAsian                        .    0.0000   0.0000          0.0380
    ## ethnicityBlack                        .    0.0024   0.0024          0.2262
    ## ethnicityChinese                      .    0.0071   0.0071          0.1535
    ## ethnicityMixed                        .    0.0000   0.0000          0.0238
    ## ethnicityRefused                      .    0.0024   0.0024          0.1714
    ## ethnicityUnknown                      .    0.0000   0.0000          0.0048
    ## ethnicityWhite                        .    0.0119   0.0119          0.4820
    ## regionLondon                          .    0.0071   0.0071          0.5654
    ## regionMidlands & East Anglia          .    0.0000   0.0000          0.2185
    ## regionScotland                        .    0.0024   0.0024          0.4732
    ## regionSouth East                      .    0.0048   0.0048          0.6442
    ## regionSouth West                      .    0.0143   0.0143          0.4280
    ## regionThe North                       .    0.0214   0.0214          0.5507
    ## regionWales                           .    0.0024   0.0024          0.4132
    ## 
    ## Percent Balance Improvement:
    ##                              Std. Mean Diff. Var. Ratio eCDF Mean eCDF Max
    ## distance                                98.8       81.2      99.0     91.0
    ## genderFemale                            76.0          .      76.0     76.0
    ## genderMale                              76.0          .      76.0     76.0
    ## age                                     93.1       74.0      89.4     83.0
    ## marital_statusDivorced                  87.4          .      87.4     87.4
    ## marital_statusMarried                   82.2          .      82.2     82.2
    ## marital_statusSeparated                 85.2          .      85.2     85.2
    ## marital_statusSingle                    95.6          .      95.6     95.6
    ## marital_statusWidowed                   56.4          .      56.4     56.4
    ## ethnicityAsian                         100.0          .     100.0    100.0
    ## ethnicityBlack                         -61.6          .     -61.6    -61.6
    ## ethnicityChinese                       -30.8          .     -30.8    -30.8
    ## ethnicityMixed                         100.0          .     100.0    100.0
    ## ethnicityRefused                         1.6          .       1.6      1.6
    ## ethnicityUnknown                       100.0          .     100.0    100.0
    ## ethnicityWhite                        -132.6          .    -132.6   -132.6
    ## regionLondon                            51.9          .      51.9     51.9
    ## regionMidlands & East Anglia           100.0          .     100.0    100.0
    ## regionScotland                          94.7          .      94.7     94.7
    ## regionSouth East                        33.6          .      33.6     33.6
    ## regionSouth West                       -54.7          .     -54.7    -54.7
    ## regionThe North                        -33.6          .     -33.6    -33.6
    ## regionWales                            -13.1          .     -13.1    -13.1
    ## 
    ## Sample Sizes:
    ##           Control Treated
    ## All          1270     421
    ## Matched       421     421
    ## Unmatched     849       0
    ## Discarded       0       0

    ##create data frame from matches using the match.data function.

    match_data = match.data(match)


    #check the dimensions.
    dim(match_data)

    ## [1] 842  15

    ##Step Four: Conduct Analysis using the new sample.

    ##turn marital status into a factor variable so that we can use it in our regression 
    match_data = match_data %>% mutate(marital_status = as.factor(marital_status))


    ## we can now get the treatment effect of smoking on gross income with and without controls
    lm_nocontrols = lm(marital_status ~ smoke, data= match_data)

    lm_nocontrols

    ## 
    ## Call:
    ## lm(formula = marital_status ~ smoke, data = match_data)
    ## 
    ## Coefficients:
    ## (Intercept)        smoke  
    ##     2.88124      0.06888

    # with controls
    lm_controls =lm(marital_status ~ smoke+age+gender+ethnicity+marital_status, data=match_data)

    lm_controls

    ## 
    ## Call:
    ## lm(formula = marital_status ~ smoke + age + gender + ethnicity + 
    ##     marital_status, data = match_data)
    ## 
    ## Coefficients:
    ##      (Intercept)             smoke               age        genderMale  
    ##         3.051402          0.073764         -0.007937          0.034983  
    ##   ethnicityBlack  ethnicityChinese    ethnicityMixed  ethnicityRefused  
    ##         0.821333         -0.251707         -0.008274          0.829804  
    ## ethnicityUnknown    ethnicityWhite  
    ##        -1.157318          0.141197
