---
title: Boosted Regression Trees
parent: Machine Learning
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---


## Introduction

  Boosting is a numerical optimization technique for minimizing the loss function by adding, at each step, a new tree that best reduces (steps down the gradient of) the loss function. For Boosted Regression Trees (BRT), the first regression tree is the one that, for the selected tree size, maximally reduces the loss function.


## Keep in Mind

The Boosted Trees Model is a type of additive model that makes predictions by combining decisions from a sequence of base models. More formally we can write this class of models as:

$$ g(x) = f_0(x)+f_1(x)+f_2(x)+... $$

where the final classifier $$g$$ is the sum of simple base classifiers $$f_i$$. For the boosted trees model, each base classifier is a simple decision tree. This broad technique of using multiple models to obtain better predictive performance is called model ensembling.

Random forests improve upon bagged trees by decorrelating the trees. In order to decorrelate its trees, a random forest only considers a random subset of predictors when making each split (for each tree). This is compared to boosted trees, which can pass information from one to the other. We add each new tree to our model (and update our residuals). Trees are typically small—slowly improving where it struggles.

- Check [here](https://turi.com/learn/userguide/supervised-learning/boosted_trees_regression.html) for more help.

## Also Consider

- There are non-boosted approaches to decision trees, which can be found at [Decision Trees]({{ "/Machine_Learning/decision_trees.html" | relative_url }}) and [Random Forest]({{ "/Machine_Learning/random_forest.html" | relative_url }}).

# Implementations

## Python

There are several packages that can be used to estimate boosted regression trees but [**sklearn**](https://scikit-learn.org/stable/index.html) provides a function `GradientBoostingRegressor` that is perhaps the most user-friendly.

```python
# Install scikit-learn using conda or pip if you don't already have it installed
from sklearn.datasets import make_regression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

# Generate some synthetic data
X, y = make_regression()

# Split the synthetic data into train and test arrays
X_train, X_test, y_train, y_test = train_test_split(X, y)

# The number of trees is set by n_estimators; there are many other options that
# you should experiment with. Typically the defaults will be sensible but are
# unlikely to be perfect for your use case. Let's create the empty model:
reg = GradientBoostingRegressor(n_estimators=100,
                                max_depth=3,
                                learning_rate=0.1,
                                min_samples_split=3)
# Fit the model
reg.fit(X_train, y_train)

# Predict the value of the first test case
reg.predict(X_test[:1])

# R^2 score for the model (on the test data)
reg.score(X_test, y_test)
```

## R

Boosted trees can be produced using the **gbm** package

Boosting has three tuning parameters.

1. The number of trees `B` (important to prevent overfitting)
2. The shrinkage parameter `lambda` (controls boosting's learning rate
 - often 0.01 or 0.001)
3. The number of splits in each tree (the tree's complexity)

data from:https://www.kaggle.com/kondla/carinsurance

```r
# Load necessary packages and set the seed
library(pacman)
p_load(tidyverse,janitor, caret, glmnet, magrittr, 
       dummies, janitor, rpart.plot, e1071, dplyr, caTools, naniar,
       forcats, ggplot2, MASS,creshape, pROC,ROCR,readr, gbm)
set.seed(101) 

# Load in data
carInsurance_train <- read_csv("https://raw.githubusercontent.com/LOST-STATS/LOST-STATS.github.io/master/Machine_Learning/Data/boosted_regression_trees/carInsurance_train.csv")
summary(carInsurance_train)

# Produce a training and a testing subset of the data
sample = sample.split(carInsurance_train$Id, SplitRatio = .8)
train = subset(carInsurance_train, sample == TRUE)
test  = subset(carInsurance_train, sample == FALSE)
total <- rbind(train ,test)
gg_miss_upset(total)
```

Step 1: Produce dummies as appropriate

```r
total$CallStart<-as.character(total$CallStart)

total$CallStart<-strptime(total$CallStart,format=" %H:%M:%S")

total$CallEnd<-as.character(total$CallEnd)

total$CallEnd<-strptime(total$CallEnd,format=" %H:%M:%S")

total$averagetimecall<-as.numeric(as.POSIXct(total$CallEnd)-as.POSIXct(total$CallStart),units="secs")

time<-mean(total$averagetimecall,na.rm = TRUE)
```

Produce dummy variables as appropriate

```r
total_df <- dummy.data.frame(total %>% 
                                dplyr::select(-CallStart, -CallEnd, -Id, -Outcome))
summary(total_df)
```

Fill in missing values

```r
total_df$Job[is.na(total_df$Job)] <- "management"
total_df$Education [is.na(total_df$Education)] <- "secondary"
total_df$Marital[is.na(total_df$Marital)] <-"married"
total_df$Communication[is.na(total_df$Communication)] <- "cellular"
total_df$LastContactMonth[is.na(total_df$LastContactMonth)] <- "may"
```

Step 2: Preprocess data with median imputation and a central scaling

```r
clean_new <- preProcess(
  x = total_df %>% dplyr::select(-CarInsurance) %>% as.matrix(),
  method = c('medianImpute')
) %>% predict(total_df)
```

Step 3: Divide the data into testing and training data

```r
trainclean <- head(clean_new, 3200) %>% as.data.frame()
testclean <- tail(clean_new, 800) %>% as.data.frame()
summary(trainclean)
```
Step 4: Parameters

**gbm** needs the three standard parameters of boosted trees—plus one more:
- `n.trees`, the number of trees
- `interaction.depth`, trees' depth (max. splits from top)
- `shrinkage`, the learning rate
- `n.minobsinnode`, minimum observations in a terminal node

Step 5: Train the boosted regression tree

Notice that `trControl` is being set to select parameters using five-fold cross-validation (`"cv"`).

```r
carinsurance_boost = train(
  factor(CarInsurance)~.,
  data = trainclean,
  method = "gbm",
  trControl = trainControl(
    method = "cv",
    number = 5
  ),
  tuneGrid = expand.grid(
    "n.trees" = seq(25, 200, by = 25),
    "interaction.depth" = 1:3,
    "shrinkage" = c(0.1, 0.01, 0.001),
    "n.minobsinnode" = 5)
)
```
