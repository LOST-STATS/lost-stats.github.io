---
title: Moving Average Models
parent: Time Series
output: 
  html_document:
    keep_md: yes
mathjax: TRUE
---



### Introduction

Moving Average Models are a common method for modeling linear processes that exhibit serial correlation. This can take many forms, but an easy example is weather patterns. Imagine we modelled Ski Lift Purchases over a 5 consecutive weekday period and did not have access to weather data. A weather shock would cause serial correlation in our estimation: A snow storm Monday would imply that there's a higher likelihood of a snow storm Tuesday. This means when we think of the simple process:

$$
SkiTicketPurchases_t = \mu + \theta_1*Weather_t
$$

We should add another variable for the previous days weather in our model:

$$
SkiTicketPurchases_t = \mu + \theta_1*Weather_t + \theta_2*Weather_{t-1}
$$

---

#### Definition

Let $\epsilon_t \overset{i.i.d.} \sim N(0, \sigma^2_{\epsilon})$. A moving average process, which is denoted MA(q), take the form as:

\[
y_t = \mu + \epsilon_t + \theta_1 \epsilon_{t-1} + ... + \theta_q \epsilon_{t-q}
\]

Note that a MA(q) process has *q lagged $\epsilon$ terms*. Thus a MA(1) process would take the form:

\[
y_t = \mu + \epsilon_t + \theta_1 \epsilon_{t-1}
\]

---

#### Properties of a MA(1) process:

(1) The mean is constant.
$$
\begin{aligned}
E(y_t) &= E(\mu + \epsilon_t + \theta_1 \epsilon_{t-1}) \\
&= \mu
\end{aligned}
$$

(2) The variance is constant.
$$
\begin{aligned}
Var(y_t) &= Var(\mu + \epsilon_t + \theta_1 \epsilon_{t-1}) \\
&= (1 + \theta_1^2) * \sigma^2_{\epsilon}
\end{aligned}
$$

(3) The covariance between $y_t$ and $y_{t-q}$ is decreasing as $q \to \infty$.
$$
\begin{aligned}
Cov(y_t, y_{t-1}) &= E(y_t*y_{t-1}) - E(y_t)E(y_{t-1}) \\
&= E([\mu + \epsilon_t + \theta_1 \epsilon_{t-1}] [\mu + \epsilon_{t-1} + \theta_1 \epsilon_{t-2}]) - \mu^2 \\
&= \mu^2 + \theta_1 \sigma_{\epsilon}^2 -\mu^2 \\
&= \theta_1 \sigma_{\epsilon}^2
\end{aligned}
$$

$$
\begin{aligned}
Cov(y_t, y_{t-2}) &= E(y_t*y_{t-2}) - E(y_t)E(y_{t-2}) \\
&= E([\mu + \epsilon_t + \theta_1 \epsilon_{t-1}] [\mu + \epsilon_{t-2} + \theta_1 \epsilon_{t-3}]) - \mu^2 \\
&= \mu^2 -\mu^2 \\
&= 0
\end{aligned}
$$


Additional helpful information can be found at [Wikipedia: Moving Average Models](https://en.wikipedia.org/wiki/Moving-average_model)

---

### Keep in Mind

- Time series needs to be properly formatted (e.g. date columns should be formatted into a time)

- Model Selection uses the Akaike Information Criterion (AIC), Bayesian Information Criterion (BIC), or the Schwarz Information Criterion (SIC) to determine the appropriate number of terms to include. Refer to [Wikipedia:Model Selection](https://en.wikipedia.org/wiki/Model_selection#Criteria) for further information.

---

### Implementation

#### R


```r
#in the stats package we can simulate an ARIMA Model. ARIMA stands for Auto-Regressive Integrated Moving Average model. Since we haven't covered Auto-Regressive models or Integrated models, we will be setting those to 0 and only simulating a MA(q) model.
set.seed(123)
DT = arima.sim(n = 1000, model = list(ma = c(0.1, 0.3, 0.5)))
```


```r
plot(DT)
```

![](MA-Model_files/figure-html/unnamed-chunk-2-1.png)<!-- -->

```r
#ACF stands for Autocorrelation Function
#Here we can see that there may be potential for 3 lags in our MA process. (Note: This is due to property (3): the covariance of y_t and y_{t-3} is nonzero while the covariance of y_t and y_{t-4} is 0)
acf(DT, type = "covariance")
```

![](MA-Model_files/figure-html/unnamed-chunk-2-2.png)<!-- -->



```r
#Here I'm estimating an ARIMA(0,0,3) model which is a MA(3) model. Changing c(0,0,q) allows us to estimate a MA(q) process.
arima(x = DT, order = c(0,0,3))
```

```
## 
## Call:
## arima(x = DT, order = c(0, 0, 3))
## 
## Coefficients:
##          ma1     ma2     ma3  intercept
##       0.0722  0.2807  0.4781     0.0265
## s.e.  0.0278  0.0255  0.0294     0.0573
## 
## sigma^2 estimated as 0.9825:  log likelihood = -1410.63,  aic = 2831.25
```

```r
#We can also estimate a MA(7) model and see that the ma4, ma5, ma6, and ma7 are close to 0 and insignificant.
arima(x = DT, order = c(0,0,7))
```

```
## 
## Call:
## arima(x = DT, order = c(0, 0, 7))
## 
## Coefficients:
##          ma1     ma2     ma3      ma4      ma5      ma6      ma7  intercept
##       0.0714  0.2694  0.4607  -0.0119  -0.0380  -0.0256  -0.0219     0.0267
## s.e.  0.0316  0.0321  0.0324   0.0363   0.0339   0.0332   0.0328     0.0533
## 
## sigma^2 estimated as 0.9806:  log likelihood = -1409.65,  aic = 2837.3
```


```r
#forecast is a package designed to estimate ARIMA models. We can use it to estimate our MA(3) model.
library(forecast)
```


```r
# max.p allows us to set the # of AR lags to 0. To estimate an MA model, we set max.p = 0. This translates to estimating an ARIMA(0,0,q) = MA(q).
auto.arima(DT, max.p = 0)
```

```
## Series: DT 
## ARIMA(0,0,3) with zero mean 
## 
## Coefficients:
##          ma1     ma2     ma3
##       0.0723  0.2808  0.4782
## s.e.  0.0278  0.0255  0.0294
## 
## sigma^2 estimated as 0.9857:  log likelihood=-1410.73
## AIC=2829.47   AICc=2829.51   BIC=2849.1
```

```r
# we can also specify a start.q and a max.q to speed up our estimation.
auto.arima(DT, max.p = 0, start.q = 2, max.q = 4)
```

```
## Series: DT 
## ARIMA(0,0,3) with zero mean 
## 
## Coefficients:
##          ma1     ma2     ma3
##       0.0723  0.2808  0.4782
## s.e.  0.0278  0.0255  0.0294
## 
## sigma^2 estimated as 0.9857:  log likelihood=-1410.73
## AIC=2829.47   AICc=2829.51   BIC=2849.1
```

```r
# not using any restrictions will give the equation free range to use as many lags and terms to minimize the information criterion. This may result in terms that should not be there (such as AR terms). Additionally, using different information criterion (AIC, SIC or BIC) can give different predictions for our model.
auto.arima(DT, ic = "aic")
```

```
## Series: DT 
## ARIMA(3,0,3) with zero mean 
## 
## Coefficients:
##          ar1      ar2      ar3     ma1    ma2     ma3
##       0.0111  -0.0120  -0.0792  0.0620  0.280  0.5353
## s.e.  0.0931   0.0854   0.0861  0.0856  0.073  0.0880
## 
## sigma^2 estimated as 0.987:  log likelihood=-1409.9
## AIC=2833.79   AICc=2833.91   BIC=2868.15
```







