---
title: Causal Diagrams
parent: Model_Estimation
has_children: false
nav_order: 1
mathjax: false
---


Causal Diagrams are crucial models that can help outline the data-generating process when creating a regression model, as they help identify which variables are confounders. If a variable in the data-generating process affects both the treatment and outcome variables but is not included in the model, the model will no longer capture the treatment variable's sole impact on the outcome. This creates omitted variable bias and endogeneity as the treatment variable will be correlated with another variable in the error term. To avoid this, adding these confounding variables as controls to the model can help, but identifying what to control for can be difficult without a causal diagram.

The first step in creating the diagram is to identify the treatment and outcome variables, as well as any other variables related to them that are present in the real world and affect the data's source. The goal of the model is to draw arrows between variables that cause each other, and to list all paths of arrows and variables that start from the treatment and reach the outcome variable. If a variable is associated with both the treatment and the outcome, it creates a confounding backdoor path that should generally be blocked through adjustment. Once we identify these backdoor path variables, we can efficiently control for them, ensuring that the treatment variable is no longer correlated with the error term and obtaining a relatively unbiased estimate.

## Keep in Mind

- This guide covers the most common functions and syntax forms for creating and analyzing causal diagrams in dagitty. For additional graph specifications, advanced graph types, variable attributes, and further examples, users can consult the dagitty help documentation by running `help("dagitty")`.
- All outputs regarding adjustments and paths will be correct based on the information provided by the user. If the user inputs an incorrect data-generating process, the paths and adjustments will be correct for the given diagram, but not for the overall data-generating process.

## Also Consider

- [Simple Linear Regression]({{ "/Model_Estimation/OLS/simple_linear_regression.html" | relative_url }}) — once confounders are identified via a causal diagram, they should be added as controls in a regression model to isolate the treatment variable's causal effect on the outcome.
- [Fixed Effects in Linear Regression]({{ "/Model_Estimation/OLS/fixed_effects_in_linear_regression.html" | relative_url }}) — another common approach to controlling for unobserved confounding variables in a regression model.

# Implementations

## R

To create the causal diagram in R, we will use the dagitty package to draw and analyze it to determine what to control for in a regression.

```r
library(dagitty)
```

```r
# dagitty(x, layout = FALSE)
```

The code above highlights the structure of creating a causal diagram with dagitty, where there are two main arguments that the function dagitty (which will create the causal diagram) will take. X takes the user's input as a string specifying which variables and information should be present in the causal diagram and transforms it into the diagram itself.

The layout portion of the argument, with false as the default, allows the user to specify whether they want R to organize and space out all variables in the causal diagram so they are readable and well-spaced, if the setting is set to true. When setting the layout to equal false, R will not automatically adjust the positions of all variables, which may cause overlap that will need to be adjusted later to make the diagram readable.

```r
#Code Structure of the First Argument (X)
  # "[graph type]{[statements]}"

#The user can input the graph type they want, along with the variables to include in the model using the syntax above

#Example Code
x=dagitty("dag{ x -> y }", layout=TRUE)
plot(x)
```

The plot above displays a simple diagram with an arrow from x to y, showing that x causes y.

In the code above, the first argument is enclosed in quotation marks because it is a string. It then contains "dag", which tells R what type of causal diagram to make. For most general causal diagram creation and analysis, using the dag model will be sufficient, as it allows arrows to connect the given variables with -> or two-way arrows (<->). This model type is used in most causal inference applications because it clearly represents causal relationships between variables, but please note that it does not allow for feedback loops. Inside the braces, variables can be listed individually or connected with arrows. The arrow operator indicates a causal relationship, where the variable on the left is assumed to cause the variable on the right.

**Advanced model types:**

There are three other model types that can be used if more advanced causal diagrams are needed to create the data-generating process. The first is a MAG model, which includes hidden or unobserved variables and other factors that cannot be directly measured. It can use - – edges to represent selection effects and <-> edges to represent unobserved confounding variables. Next is a PDAG model, which is similar to the DAG model but can be used when the directions of arrows between variables are unknown. It also uses – -between two variables to indicate that the direction of the relationship is not yet known. The most advanced model is the PAG model specification, which introduces even greater uncertainty among variables and uses special edge types to represent that uncertainty. This specification uses @-@, @->, and @-- to define the relationships between variables. PAGs are typically used when the exact causal structure cannot be fully determined from the available information.

Note: the two-way arrows x <-> y are another way to show unobserved factors that may not be known impacting both x and y (x ← U → y).

**Assigning Variables:**

```r
d=dagitty("dag{
x [exposure]
y [outcome]
x -> y}")
plot(d)
```

In the code chunk above, once the model type is specified, the user can add the variables they want to include in the model using curly braces. In the example, the variable X has an arrow to variable Y, meaning that X causes Y. It is also possible to list variables in the braces ({ x y z }), however, this just adds the variables to the diagram and does not connect any arrows to them. To have multiple variables with arrows between them, they can also be added within the curly braces with as many variables as the user desires ({x -> y -> z }). The user can also specify what variables are the treatment and outcome by implementing the following code:

Using the code above, X is specified as the treatment variable, and Y is the outcome variable. Additionally, the plot function is used to plot the causal diagram.

**Implementation:**

```r
#This code creates a simple causal diagram that maps the DGP of how tutoring impacts college test scores, where socioeconomic status effects both variables.

g <- dagitty("dag{
Tutoring [exposure]
CollegeTestScores [outcome]

Tutoring-> CollegeTestScores
SocioeconomicStatus -> Tutoring 
SocioeconomicStatus -> CollegeTestScores 
IntrinsicMotivation -> CollegeTestScores
}", layout = TRUE)
plot(g)
```

The plot above displays the causal diagram showing IntrinsicMotivation and SocioeconomicStatus both pointing to CollegeTestScores, and SocioeconomicStatus also pointing to Tutoring, which in turn points to CollegeTestScores.

To create a causal diagram that specifies the exposure and the outcome and includes other variables that affect other variables, the following code structure can be used, and the user can add as many variables with arrows between them as they want. To change the variable names, the user can simply type the variable names. Note: the name of the variable does not need to be wrapped in quotation marks.

In the causal diagram above, the code has created a diagram showing that socioeconomic status is a confounder for both tutoring and college test scores, meaning it must be controlled for to isolate the causal effect of tutoring on college test scores. Please note that it is not necessary to control for intrinsic motivation, as it only affects the outcome variable. Variables that create open backdoor paths between the treatment and outcome should generally be controlled for.

```r
paths(g)
```

```
$paths
[1] "Tutoring -> CollegeTestScores"
[2] "Tutoring <- SocioeconomicStatus -> CollegeTestScores"

$open
[1] TRUE TRUE
```

The output above lists the paths connecting the exposure and outcome variables. Below the listed paths, dagitty indicates whether each path is open (TRUE) or blocked (FALSE). Open backdoor paths can create omitted variable bias and should generally be blocked by controlling for an appropriate variable.

```r
adjustmentSets(g)
```

```
{ SocioeconomicStatus }
```

If the user wants to confirm which variables they must control for to reduce omitted variable bias, they can use the code above, which will output any confounding variables within the model. This is a crucial function within the dagitty package, as visually identifying which variables to control for can be difficult when the data-generating process involves many variables and many arrows in the model. Once the function identifies which variables need to be controlled for, the user is encouraged to add these variables as controls in their regression model to isolate the treatment variable's causal effect on the outcome.

```r
g <- dagitty("dag{
  x -> y ; x <- z -> y
  x [exposure]
  y [outcome]
  z [unobserved]
}")
```

The code above is another way to create the causal diagram, where the user can specify the causal relationships between variables on a single line, separated by semicolons. Then, the variables are labeled as an exposure, outcome, or unobserved. Using the code above may be beneficial for users who want to see all causal relationships on a single line and then specify the type of each variable.

