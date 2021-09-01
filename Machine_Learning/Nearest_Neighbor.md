---
title: K-Nearest Neighbor Matching
parent: Machine Learning
has_children: false
nav_order: 1
mathjax: true 
---

## Introduction

K-Nearest Neighbor Matching is to classify a new input vector x, examine the k-closest training data points to x and assign the object to the most frequently occurring class. Optionally, we give closer points larger weights and more distant points smaller weights. Common value for k is 3 or 5. At k=1, the error rate is always zero for the training sample because the closest point to any training data point is itself. Therefore, it will always overfit.


## Keep in Mind

When to Consider | Advantages | Disadvantages 
---------------- | ---------- | -------------
Instances map to points in $R^{n}$ | **Traning is very fast** | **Slow at query time**
Less than 20 attributes per instance | Learn complex target functions | Easily fooled by irrelevant attributes 
Lots of training data | Do not lose information 


## Also Consider

1. Distance measure 
   * Most common: Euclidean distance
   * Euclidean distance makes sense when different measurements are commensurate; each is variable measured in the same units.
   * If the measurements are different, say length and weight, it is not clear.
  
$$d_{E}(x^{i}, x^{j}) = (\sum_{k=1}^{p}(x^{i}_k - x^{j}_k)^2)^\frac{1}{2}$$

2. Standardization
   * When variables are not commensurate, we want to standardize them by dividing by the sample standard deviation. This makes them all equally important. 
   * The estimate for the standard deviation of $x_k$:
$$\hat{\sigma}_k = \biggl(\frac{1}{n}\sum_{i=1}^{n}(x^{i}_k - \bar{x}_k)^2\biggr)^\frac{1}{2}$$

      where $\bar{x}_k$ is the sample mean: 
$$\bar{x}_k = \frac{1}{n}\sum_{i=1}^{n}x^i_k $$

3. Weighted Euclidean Distance
   * Finally, if we have some idea of the relative importance of each variable, we can weight them:
  
$$d_{WE}(i,j) = \biggl(\sum_{k=1}^{p}w_k(x^i_k - x^j_k)^2\biggr)^\frac{1}{2} $$

4. Choosing k 
   * Increasing k reduces variance and increases bias.
  
5. For high-dimensional space, problem that the nearest neighbor may not be very close at all.

6. Memory-based technique. Must make a pass through the data for each classification. This can be prohibitive for large data sets. 


# Implementations

## Python

For KNN, it is not required to import packages other than **numpy**. You can basically do KNN with one package because it is mostly about computing distance and normalization. You would need TensorFlow and Keras as you try more advanced algorithms such as convolutional neural network. 

```c
import argparse
import numpy as np
from collections import Counter

# Process arguments for k-NN classification
def handle_args():
    parser = argparse.ArgumentParser(description=
                 'Make predictions using the k-NN algorithms.')

    parser.add_argument('-k', type=int, default=1, help='Number of nearest neighbors to consider')
    parser.add_argument('--varnorm', action='store_true', help='Normalize features to zero mean and unit variance')
    parser.add_argument('--rangenorm', action='store_true', help='Normalize features to the range [-1,+1]')
    parser.add_argument('--exnorm', action='store_true', help='Normalize examples to unit length')
    parser.add_argument('train',  help='Training data file')
    parser.add_argument('test',   help='Test data file')

    return parser.parse_args()


# Load data from a file
def read_data(filename):
  data = np.genfromtxt(filename, delimiter=',', skip_header=1)
  x = data[:, 0:-1]
  y = data[:, -1]
  return (x,y)


# Distance between instances x1 and x2
def dist(x1, x2):
    euclidean_distance = np.linalg.norm(x1 - x2)
    return euclidean_distance


# Predict label for instance x, using k nearest neighbors in training data
def classify(train_x, train_y, k, x):
    dists = np.sqrt(np.sum((x - train_x) ** 2, axis=1))
    idx = np.argsort(dists, 0)[:k]
    k_labels = [train_y[index] for index in idx]
    prediction = list()
    prediction.append(max(k_labels, key=k_labels.count))
    prediction = np.array(prediction)
    return prediction


# Process the data to normalize features and/or examples.
# NOTE: You need to normalize both train and test data the same way.
def normalize_data(train_x, test_x, rangenorm, varnorm, exnorm):
  if rangenorm:
    train_x = 2 * (train_x - np.min(train_x, axis=0)) / np.nan_to_num(np.ptp(train_x, axis=0)) - 1
    test_x = 2 * (test_x - np.min(test_x, axis=0)) / np.nan_to_num(np.ptp(train_x, axis=0)) - 1

    pass

  if varnorm:
    train_x = (train_x - np.mean(train_x, axis=0)) / np.nan_to_num(np.std(train_x, axis=0))
    test_x = (test_x - np.mean(test_x, axis=0)) / np.nan_to_num(np.std(test_x, axis=0))

    pass

  if exnorm:
    for i in train_x:
      train_x = i / np.linalg.norm(i)
    for k in test_x:
      test_x = k / np.linalg.norm(k)

    pass

  return train_x, test_x


# Run classifier and compute accuracy
def runTest(test_x, test_y, train_x, train_y, k):
  correct = 0
  for (x,y) in zip(test_x, test_y):
    if classify(train_x, train_y, k, x) == y:
      correct += 1
  acc = float(correct)/len(test_x)
  return acc


# Load train and test data.  Learn model.  Report accuracy.
def main():

  args = handle_args()

  # Read in lists of examples.  Each example is a list of attribute values,
  # where the last element in the list is the class value.
  (train_x, train_y) = read_data(args.train)
  (test_x, test_y)   = read_data(args.test)

  # Normalize the training data
  (train_x, test_x) = normalize_data(train_x, test_x, 
                          args.rangenorm, args.varnorm, args.exnorm)
    
  acc = runTest(test_x, test_y,train_x, train_y,args.k)
  print("Accuracy: ",acc)

if __name__ == "__main__":
  main()
```

##  R 
The simplest way to perform KNN in R is with the package **class**. It has a KNN function that is rather user friendly and does not require you to do distance computing as it runs everything with euclidean distance. For more advanced types nearest neighbors testing it would be best to use the _matchit function_ from the [**matchit** package.](https://kosukeimai.github.io/MatchIt/reference/matchit.html) To verify results this example also used the _confusionMatrix function_ from the package **caret**.  
    Due to how this package is designed the easiest room for error would be during normalization by normalizing variables such as character or other ones that do not require normalization. Another good source of error is not including drop = TRUE for your target, or y, vector which will prevent the model from running. Finally, the way this example verifies results it is vital to convert the target into a factor as the data has to be in similar kind in order for R to give you an output.

```

library(tidyverse)
library(readr)

#For KNN
library(class)
library(caret)


#Import the Dataset
df <- read_csv("wdbc.csv")
view(df)

#the first column is an identifier so remove that, anything that does not aid in classifying can be removed
df <- df[-1]


#See the count of the target, either B, benign, or M, malignant
table(df[1])

#Normalize the Dataset

normal<- function(x) { return ((x - min(x)) / (max(x) - min(x))) }

#Apply to what needs to be normalized, in this case not the target
df_norm <- as.data.frame(lapply(df[2:31], normal))

#Verify that normalization has occurred
summary(df_norm[1])
summary(df_norm[3])
summary(df_norm[11])
summary(df_norm[23])


#Split the dataframe into test and train datasets - note there are two dataframes
#First test and train from the features, here is an example of about a 70/30 split for testing and training

x_train <- df_norm[1:397,]

x_test <- df_norm[398:568,]


#Now test and train for the target - here is import that you do ", 1" to indicate only one column
#It will not work unless you use drop = TRUE
y_train <- df[1:397, 1, drop = TRUE]

y_test <- df[398:568, 1, drop = TRUE]


#The purpose of installing those packages were to use these next functions, first KNN
#Like the python example states, best practice for K unless assigned is the square root of the number of observations
pred <- knn(train = x_train, test = x_test, cl = y_train, k = 23)

#Confusion Matrix from Caret

#KNN converts to a factor with two levels so we need to make sure the test dataset is similar
y_test <- y_test %>% factor(levels = c("B", "M"))

#See how well the model did
confusionMatrix(y_test, pred)

```

### References for R walkthrough
The dataset used is from the UCI Machine Learning Repository under _Breast Cancer Wisconsin (Diagnostic) Data Set_. [Rdocumentation for KNN](https://www.rdocumentation.org/packages/class/versions/7.3-19/topics/knn) was used in order to work on this example. Also, [statology's "how to create a confusion matrix"](https://www.statology.org/confusion-matrix-in-r/)
[wdbc.csv](https://github.com/LOST-STATS/lost-stats.github.io/files/7088929/wdbc.csv)
