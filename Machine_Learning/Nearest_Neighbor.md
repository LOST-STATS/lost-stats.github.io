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

For KNN, it is not required to import packages other than **numpy**. You can do KNN basically with one package because it is mostly about computing distance and normalization. You would need TensorFlow and Keras as you try more advanced algorithms such as convolutional neural network. 

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

