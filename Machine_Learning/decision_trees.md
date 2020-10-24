---
title: Decision Trees
parent: Machine Learning
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---
Decision trees are among the most common and useful machine learning methodologies. While they are a relatively simple method, they are incredibly easy to understand and implement for both classification and regression problems.

A decision tree "grows" by creating a cutoff point (often called a split) at a single point in the data that maximizes accuracy. The tree's prediction is then based on the mean of the region that results from the input data.

For both regression and classification trees, it is important to optimize the number of splits that we allow the tree to make. If there is no limit, the trees would be able to create as many splits as the data will allow. This would mean the tree could perfectly "predict" every value from the training dataset, but would perform terribly out of sample (i.e., overfit the data). As such, it is important to keep a reasonable limit on the number of splits. This is achieved by creating a penalty that the algorithm has to pay in order to perform another split. If the increase in accuracy is worth more than the penalty, it will make the split.

For regression trees, the decision to split along a continuum of values is often made by minimizing the residual sum of squares:

$$
minimize \sum(y-prediction)^2
$$

This should be highly reminiscent of ordinary least squares. Where this differs is in the number of splits created, the binary nature of the splits, and its nonlinear nature.

The methodology behind classificiation is very similar, except the splits are decided by minimizing purity, such as the Gini index:

$$
G= 1 - \sum_{i = 1}^{C} (p_{i})^2 
$$

The goal here is to create regions with as of classifications as possible, as such, a smaller Gini index implies a more pure region.

## Keep in Mind
* While decision trees are easy to interpret and understand, they often underpreform relative to other machine learning methodologies. 
* Even though they may not offer the best predictions, decision trees excel at identifying key variables in the data.


## Also Consider
* Decision trees are the basis for all tree-based methodologies. More robust methods, such as [Random Forests]({{ "/Machine_Learning/random_forest.html" | relative_url }}), are a collection of decision trees that aggregate their decisions into a single prediction. These forests are often more useful for predictive modeling.

# Implementations

## Python

The easiest way to get started with decision trees in Python is to use the [**scikit-learn**](https://scikit-learn.org/stable/index.html) package. In the example below, we'll use data on the passengers of the Titanic to build a classification tree that predicts whether passengers survived or not (binary outcome) based on
properties such as passenger age, gender as recorded in the data, and class of cabin. As ever with machine learning, it's essential that an out-of-sample set, also known as a test set, is retained and used to score the final model.

```python
# Install sklearn and pandas using pip or conda, if you don't have them already.
# Note that the 'f-strings' used in the print statements below are only available in Python>=3.6.
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_confusion_matrix
import pandas as pd

titanic = pd.read_csv("https://raw.githubusercontent.com/Evanmj7/Decision-Trees/master/titanic.csv",
                      index_col=0)

# Let's ensure the columns we want to treat as continuous are indeed continuous by using pd.to_numeric
# The errors = 'coerce' keyword argument will force any values that cannot be
# cast into continuous variables to become NaNs.
continuous_cols = ['age', 'fare']
for col in continuous_cols:
    titanic[col] = pd.to_numeric(titanic[col], errors='coerce')

# Set categorical cols & convert to dummies
cat_cols = ['sex', 'pclass']
for col in cat_cols:
    titanic[col] = titanic[col].astype('category').cat.codes

# Clean the dataframe. An alternative would be to retain some rows with missing values by giving
# a special value to nan for each column, eg by imputing some values, but one should be careful not to
# use information from the test set to impute values in the training set if doing this. Strictly speaking,
# we shouldn't be dropping the nans from the test set here (as we pretend we don't know what's in it) - but
# for the sake of simplicity, we will.
titanic = titanic.dropna()

# Create list of regressors
regressors = continuous_cols + cat_cols
# Predicted var
y_var = ['survived']

# Create a test (25% of data) and train set
train, test = train_test_split(titanic, test_size=0.25)

# Now let's create an empty decision tree to solve the classification problem:
clf = tree.DecisionTreeClassifier(max_depth=10, min_samples_split=5,
                                  ccp_alpha=0.01)
# The last option, ccp_alpha, prunes low-value complexity from the tree to help
# avoid overfitting.

# Fit the tree with the data
clf.fit(train[regressors], train[y_var])

# Let's take a look at the tree:
tree.plot_tree(clf)

# How does it perform on the train and test data?
train_accuracy = round(clf.score(train[regressors], train[y_var]), 4)
print(f'Accuracy on train set is {train_accuracy}')

test_accuracy = round(clf.score(test[regressors], test[y_var]), 4)
print(f'Accuracy on test set is {test_accuracy}')

# Show the confusion matrix
plot_confusion_matrix(clf, test[regressors], test[y_var])

# Although it won't be the same from run to run, this model scored around 80%
# out of sample, and has slightly more false positives than false negatives.
```

## R
```r
# Load packages
# install.packages("pacman") ## already installed
library(pacman)
p_load(rpart,rpart.plot,caret,rattle)
# We will utilize data regarding passengers on their survival. We have multiple pieces of information on every passenger, including passenger age, sex, cabin number, and class. 

# Our goal is to build a decision tree that can predict whether or not passengers survived the wreck, making it a classification tree. These same methodologies can be used and applied to a regression tree framework.

# Read in the data
titanic <- read.csv("https://raw.githubusercontent.com/Evanmj7/Decision-Trees/master/titanic.csv")

# Set a seed for reproducability
set.seed(1234)

# The data is clean for the most part, but some variables have been read in as factors instead of numeric variables, so we can fix that with the following code.
titanic$age <- as.numeric(titanic$age)
titanic$fare <- as.numeric(titanic$fare)

# As with all machine learning methodologies, we want to create a test and a training dataset

# Take a random sample of the data, here we have chosen to use 75% for training and 25% for validation
samp_size <- floor(0.75*nrow(titanic))
train_index <- sample(seq_len(nrow(titanic)),size=samp_size,replace=FALSE)

train <- titanic[train_index, ]
test <- titanic[-train_index, ]

# Now that we have our test and train datasets, we can build our trees. Here, we will use the package "rpart". Other packages, such as "ranger" are also viable options.

# Here we can pick some variables we think would be good, the tree will decide which ones are best. Some data we have isn't useful, such as an individual's name or the random ID we assigned passengers, so there is no need to include them.

basic_tree <- rpart(
  survived ~ pclass + sex + age + fare + embarked, # our formula
  data=train,
  method = "class", # tell the model we are doing classification
  minsplit=2, # set a minimum number of splits
  cp=.02 # set an optional penalty rate. It is often useful to try out many different ones, use the caret package to test many at once
)

basic_tree

# plot it using the packages we loaded above
fancyRpartPlot(basic_tree,caption="Basic Decision Tree")

# This plot gives a very intuitive visual representation on what is going on behind the scenes.

# Now we should predict using the test data we left out!
predictions <- predict(basic_tree,newdata=test,type="class")

# Make the numeric responses as well as the variables that we are testing on into factors
predictions <- as.factor(predictions)
test$survived <- as.factor(test$survived)

# Create a confusion matrix which tells us how well we did.
confusionMatrix(predictions,test$survived)

# This particular model got ~80% accuracy. This varies each time if you do not set a seed. Much better than a coin toss, but not great. With some additional tuning a decision tree can be much more accurate! Try it for yourself by changing the factors that go into the prediction and the penalty rates.

```
