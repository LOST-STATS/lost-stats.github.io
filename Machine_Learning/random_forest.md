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

## R

There are a number of packages in R capable of training a random forest, including **randomForest** and **ranger**. Here we will use **randomForest**.

We'll be using a built-in dataset in R, called "Iris". There are five variables in this dataset, including species, petal width and length as well as sepal length and width.

```r
#Load packages
library(tidyverse)
library(rvest)
library(dplyr)
library(caret)
library(randomForest)
library(Metrics)
library(readr)

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


## Python

Use iris features (sepal length and width, petal length and width) to predict iris species


```python
# Import libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,confusion_matrix

#Read data
filename = 'https://vincentarelbundock.github.io/Rdatasets/csv/datasets/iris.csv'
iris = pd.read_csv(filename)
iris.head(5)

#Check whether there are missing values to deal with
iris.info()

#Prepare data for training
X=iris[['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm']]
y=iris[['Species']]

#Split data into training and test set
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=1996)
X_train.shape,X_test.shape,y_train.shape,y_test.shape

#Creating model using random forest
Model=RandomForestClassifier(max_depth=2)
Model.fit(X_train,y_train)

#Predict values for test data
y_pred=Model.predict(X_test)

#Evaluate model prediction
print("Accuracy is:”,accuracy_score(y_pred, y_test)*100,”%")

#Predict what type of iris it is
Model.predict([[3,4,5,2]])
```
