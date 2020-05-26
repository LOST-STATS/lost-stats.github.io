---
title: Formatting graph legends
parent: Presentation
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Formatting graph legends

Graphs and charts are an instrumental way to explain and visualize your data and results. However, graph legends are often overlooked but are one of the most important aspects when presenting your data. Without an effective legend, the information you want intended to convey can get misinterpreted by the reader.

## Keep in Mind

**What makes a good legend?**

1. Title
- You should include a brief title that encompasses the whole figure. The title should answer the question *"what is this figure about?"* clearly and concicely. 

2. Definitions and descriptions
- This is the section where you can explain all the different components contained within the figure. This inclues any key symbols, colors, scale changes, lines or other compenets that are needed to understand the information clearly. 

3. Methods *(optional)*
- This is a very short description of the statistical methods used. The best way to approach this is to try and simplify the methods section so the figure can stand alone from the rest of the paper. 

4. Results *(optional)*
- Include a sentence or two that summarizes the results that can be found in that particular graph.

**Avoid clutter**
- It is important to keep these legends simple, an effective legend is there to help the graph stand alone.

## Also Consider

Before finalizing your legend the graph itself should be completed. Deciding which type of graph is best suited for your data is a whole topic in itself. For information on choosing and creating different types of graphs, you can explore the [Presentation](https://lost-stats.github.io/Presentation/Presentation.html#presentation) tab located on the LOST website. 

Some of the graphical implementations this page contains include are;
[Bar Graphs](https://lost-stats.github.io/Presentation/bar_graphs.html), [Histograms](https://lost-stats.github.io/Presentation/histograms.html), and [Scatterplot by Group on Shared Axes](https://lost-stats.github.io/Presentation/scatterplot_by_group_on_shared_axes.html). 

Check out [this article](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4078179/) for a brief description of the relationships shown for different graph types . 


# Implementations

## R

For this first example we will be using the _**Iris**_ dataset that is preloaded within R to create a base graph so that we can work with the legend on its own. 

```R

#load necessary packages
if (!require("pacman")) install.packages("pacman")
pacman::p_load(dplyr,ggplot2, janitor)

#load in dataset
data(iris)
iris <- clean_names(iris)

#creating the base graph (box plot)
fig_1 <- ggplot(iris, aes(species, petal_length, fill=species)) + 
  geom_boxplot()+
  scale_y_continuous("Petal Length (cm)", breaks= seq(0,30, by=.5))+
  labs(title = "Iris Petal Length Box Plot", x = "Species")

fig_1

```
![Base Box Plot]()

# Some basics 
## *Changing the legend title and changing the fonts*
Making the graph visually appealing is as important as making sure the information is conveyed clearly and concisely. By  changing the legend title from the default could help explain your results better. 

```R

#Changing the name of the legend
fig_1 + labs(fill = "Iris Species")

#Font Options
  #this command will control the legend title
fig_1 + theme(legend.title = element_text(colour="dark green", size=10, 
                                      face="italic"))
                                      
  #While this command will affect the options within the legend
fig_1 + theme(legend.text = element_text(colour="dark green", size=10, 
                                      face="italic"))                                    

#side note: you can change the color, size and face for the other text option within the figure. (ie: title and axis)

```

## *Changing legend location*
The legend locations default is to be located to the right hand side of the graph. It can be moved around the graph or within the figure itself. 

```R

#Changing legend position
  ##For this option you can use either desctiptive values such as; “left”,“top”, “right”, “bottom”, “none” 
fig_1 + theme(legend.position="bottom")

  ##Or a numeric vector that gives x and y cordinates for the position
fig_1 + theme(legend.position = c(0.4, 0.9),
          legend.direction = "horizontal")  

```
# *Changing the order of the legend options*
While in this example the order of the variables has no hold, there could be times where the listed order of the objects could be important to the visual depiction. 

```R

#This moves the objects within the graph
fig_1 + scale_x_discrete(limits=c("virginica", "setosa", "versicolor"))

#This section is controling the order the objects appear in the legend
iris$species <- factor(iris$species, levels = c("virginica", "setosa", "versicolor"))
  #you will have to re-run the fig_1 code from earlier for this to work

```

# *Removing the legend*
There are few instances where you would remove the whole legend but there are sometimes where the legend title is repeating the information found in the title of the figure itself.

```R

#Removing the just the title
fig_1 + theme(legend.title = element_blank())

#
Removing the whole legend
fig_1 + scale_color_discrete(name="Iris Species",
        labels = c("Virginica", "Versicolor", "Setosa"))
        
```

For an in-depth description for achademic publications or scientific wrtitings I would check out [this blog post](https://www.biosciencewriters.com/Tips-for-Writing-Outstanding-Scientific-Figure-Legends.aspx) written by Michelle S., Ph.D. 

This example focused on using ggplot  but there are many other pachages that can be used within R for creating figures. Plotly is a free and open-source graphing library for R and [this article](https://plotly.com/r/legend/) gives an in depth analysis of the package. 