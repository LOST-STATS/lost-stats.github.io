---
title: Boosted Regression tree
parent: Machine Learning
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---


#INTRODUCTION SECTION

Boosting is a numerical optimization technique for minimizing the loss function by adding, at each step, a new tree that best reduces (steps down the gradient of) the loss function. For BRT, the first regression tree is the one that, for the selected tree size, maximally reduces the loss function.


## Keep in Mind
-The Boosted Trees Model is a type of additive model that makes predictions by combining decisions from a sequence of base models. More formally we can write this class of models as:

g(x)=f0(x)+f1(x)+f2(x)+...
where the final classifier g is the sum of simple base classifiers fi. For boosted trees model, each base classifier is a simple decision tree. This broad technique of using multiple models to obtain better predictive performance is called model ensembling.
- Check [here]source from: https://turi.com/learn/userguide/supervised-learning/boosted_trees_regression.html) for more help.

## Also Consider

Random forest in R , decesion tree in R
-You have many options for training random forests in R.
E.g., party , Rborist , ranger , randomForest .
-caret offers access to each of these packages via train .
E.g., method = "rf" or method = "ranger"
-Random forests improve upon bagged trees by decorrelating the trees.
In order to decorrelate its trees, a random forest only considers a random
subset of predictors when making each split (for each tree)

# Implementations

## R

For R user , boosted trees via "gbm" package
-Boosting allows trees to pass on information to each other.
We add each new tree to our model (and update our residuals).
Trees are typically small—slowly improving where it struggles.

## How to boosted

Boosting has three tuning parameters.
1.The number of trees B.(important to prevent overfitting)
2.The shrinkage parameter lambda.(controls boosting's learning rate
(often 0.01 or 0.001).)
3.The number of splits in each tree.(trees' complexity).
data from:https://www.kaggle.com/kondla/carinsurance

```

library(pacman)
p_load(tidyverse,janitor, caret, glmnet, magrittr, 
       dummies,janitor,rpart.plot,e1071,dplyr,caTools,naniar,
       forcats,ggplot2,MASS,reshape, pROC,ROCR,readr)

set.seed(101) 

carInsurance_train <- read_csv("carInsurance_train.csv")
summary(carInsurance_train)

sample = sample.split(carInsurance_train$Id, SplitRatio = .8)
train = subset(carInsurance_train, sample == TRUE)
test  = subset(carInsurance_train, sample == FALSE)
total <- rbind(train ,test)
gg_miss_upset(total)
```

## STEP1: choose the variable string and  the non-integer variable ,change it to character

```
variable=total%>%mutate(Job=as.character(total$Job),
                        Marital=as.character(total$Marital),
                        Education=as.character(total$Education),
                        Communication=as.character(total$Communication),
                        LastContactMonth=as.character(total$LastContactMonth),
                        Outcome=as.character(total$Outcome))
```

### dummy the date variable
```
total$CallStart<-as.character(total$CallStart)

total$CallStart<-strptime(total$CallStart,format=" %H:%M:%S")

total$CallEnd<-as.character(total$CallEnd)

total$CallEnd<-strptime(total$CallEnd,format=" %H:%M:%S")

total$averagetimecall<-as.numeric(as.POSIXct(total$CallEnd)-as.POSIXct(total$CallStart),units="secs")

time<-mean(total$averagetimecall,na.rm = TRUE)
```

### dummy the data
```
total_df <- dummy.data.frame(total%>% select(-CallStart)%>%select(-CallEnd)%>%select(-Id)%>%select(-Outcome))
summary(total_df)
```

### solve the NA in the character variable
### remove the NA in character variable

```
total_df$Job[is.na(total_df$Job)] <- "management"
total_df$Education [is.na(total_df$Education)] <- "secondary"
total_df$Marital[is.na(total_df$Marital)]<-"married"
total_df$Communication[is.na(total_df$Communication)]<-"cellular"
total_df$LastContactMonth[is.na(total_df$LastContactMonth)]<-"may"
```

### STEP2:Take care the missing the value use the scale center and medianimpute method

```
clean_new <- preProcess(
  x = total_df%>%select(-CarInsurance) %>% as.matrix(),
  method = c('medianImpute')
)%>% predict(total_df)
```

##step3:divdie the total data into two part , train and test data
```
trainclean<- head(clean_new, 3200) %>% as.data.frame()
testclean<- tail(clean_new, 800) %>% as.data.frame()
summary(trainclean)
```


## step 4 explain the name 
gbm needs the three standard parameters of boosted trees—plus one more:
. n.trees , the number of trees
. interaction.depth , trees' depth (max. splits from top)
. shrinkage , the learning rate
. n.minobsinnode , minimum observations in a terminal node

##step5 boosted

# Train the random forest
```
carinsurance_boost = train(
factor(CarInsurance)~.,
data = carInsurance_train,
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