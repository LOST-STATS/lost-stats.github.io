---
title: Random Forest
parent: Machine Learning
has_children: false
nav_order: 1
mathjax: false ## Switch to false if this page has no equations or other math rendering.
---

# Random Forest

INTRODUCTION SECTION

Random forest is one of the most popular and powerful machine learning algorithm. It consists of a number of decision trees, and every node in the decision trees is a condition on a single feature. Each individual tree gives a classification, and more trees in the forest are associated with higher accuracy. The forest chooses the classification having the most votes. Random forest classifier can be used for both classification and regression tasks. In terms of regression, it takes the average of the outputs by different trees. Random forest can work with large datasets with multiple dimensions. However, it may overfit data, especially for regression problems.

## Keep in Mind

Individual trees need to have low correlations with each other, and sometimes we may remove features that are largely correlated with other features.
There is no need for cross-validation or a separate test set in random forest.
Random forest can deal with missing values.

## Also Consider

If you are not familiar with decision tree, please go to the decision tree page first as decision trees are building blocks of random forests.

# Implementations

## R

```identifier for language type, see this page: https://github.com/jmm/gfm-lang-ids/wiki/GitHub-Flavored-Markdown-%28GFM%29-language-IDs
Commented code demonstrating the technique
```

## Python

Use iris features (sepal length and width, petal length and width) to predict iris species

#Import required libraries

```
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
sns.set()
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,confusion_matrix

'imports ready for use'
```

#Read data

```
file='Iris.csv'
iris = pd.read_csv(file)
iris.head(5)
```

#Check whether there are missing values to deal with

```
iris.info()
```

#Prepare data for training 

```
X=iris[['SepalLengthCm','SepalWidthCm','PetalLengthCm','PetalWidthCm']]
y=iris[['Species']]
```

#Split data into training and test set

```
X_train,X_test,y_train,y_test=train_test_split (X,y,test_size=0.3,random_state=1996)
X_train.shape,X_test.shape,y_train.shape,y_test.shape
```

#Creating model using random forest

```
Model=RandomForestClassifier(max_depth=2)
Model.fit(X_train,y_train)
```

#Predict values for test data

```
y_pred=Model.predict(X_test)
```

#Evaluate model prediction

```
print("Accuracy is:”,accuracy_score(y_pred, y_test)*100,”%")
```

#Predict what type of iris it is 

```
Model.predict([[3,4,5,2]])
```
