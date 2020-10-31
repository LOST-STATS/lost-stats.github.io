---
title: Random Forest
parent: Machine Learning
has_children: false
nav_order: 1
mathjax: false ## Switch to false if this page has no equations or other math rendering.
---

# Random Forest

Random forest is one of the most popular and powerful machine learning algorithms. A random forest works by building up a number of decision trees, each built using a bootstrapped sample and a subset of the variables/features. Each node in each decision tree is a condition on a single feature, selecting a way to split the data so as to maximize predictive accuracy. Each individual tree gives a classification. The average, or vote-counting of that classification across trees provides an overall prediction. More trees in the forest are associated with higher accuracy. A random forest classifier can be used for both classification and regression tasks. In terms of regression, it takes the average of the outputs by different trees. Random forest can work with large datasets with multiple dimensions. However, it may overfit data, especially for regression problems.

## Keep in Mind

- Individual features need to have low correlations with each other, and sometimes we may remove features that are strongly correlated with other features.
- Random forest can deal with missing values, and may simply treat "missing" as another value that the variable can take.

## Also Consider

- If you are not familiar with decision tree, please go to the [decision tree page]({{ "/Machine_Learning/decision_trees.html" | relative_url }}) first as decision trees are building blocks of random forests.

# Implementations

## Python

Random forests can be used to perform both regression and classification tasks. In the example below, we'll use the `RandomForestClassifier` from the popular [**sklearn**](https://scikit-learn.org/stable/index.html) machine learning library. `RandomForestClassifier` is an ensemble function that fits a number of decision tree classifiers on various sub-samples of the dataset and uses averaging to improve the predictive accuracy and control over-fitting. We'll use this classifier to predict the species of iris based on its properties, using data from the iris dataset.

You may need to install packages on the command line, using `pip install package-name` or `conda install package-name`, to run these examples (if you don't already have them installed).

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# Read data
df = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/datasets/iris.csv")

# Prepare data
X = df[["Sepal.Length", "Sepal.Width", "Petal.Length", "Petal.Width"]]
y = df[["Species"]]

# Split data into training and test set
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1996
)

# Creating model using random forest
model = RandomForestClassifier(max_depth=2)
model.fit(X_train, y_train)

# Predict values for test data
y_pred = model.predict(X_test)

# Evaluate model prediction
print(f"Accuracy is {accuracy_score(y_pred, y_test)*100:.2f} %")

```

## R

There are a number of packages in R capable of training a random forest, including **randomForest** and **ranger**. Here we will use **randomForest**.

We'll be using a built-in dataset in R, called "Iris". There are five variables in this dataset, including species, petal width and length as well as sepal length and width. 

```r
#Load packages
library(pacman)
pacman::p_load(tidyverse, rvest, dplyr, caret, randomForest, Metrics,
               readr)

#Read data in R
data(iris)
iris

#Create features and target
X <- iris %>%
  select(Sepal.Length, Sepal.Width, Petal.Length, Petal.Width)
y <- iris$Species

#Split data into training and test sets
index <- createDataPartition(y, p=0.75, list=FALSE)
X_train <- X[ index, ]
X_test <- X[-index, ]
y_train <- y[index]
y_test<-y[-index]

#Train the model
iris_rf <- randomForest(x = X_train, y = y_train , maxnodes = 10, ntree = 10)
print(iris_rf)

#Make predictions
predictions <- predict(iris_rf, X_test)

result <- X_test
result['Species'] <- y_test
result['Prediction']<-  predictions

head(result)

#Check the classification accuracy (number of correct predictions out of total datapoints used to test the prediction)
print(sum(predictions==y_test))
print(length(y_test))
print(sum(predictions==y_test)/length(y_test))
```
