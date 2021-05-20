# Introduction

  The “rvest” package is a web scraping package in R that provides a
tremendous amount of versatility, as well as being easy to use. For this
specific task, of web scrapping though pages on a website, we will be
using read\_html(), html\_node(), and html\_text(). I will also make use
of the selector gadget tool,(link for the download:[Selector Gaget](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb),
as well as F12, to find the html paths.

## Keep in Mind

  Also remember that web scraping is an art as much a science so play
around with a problem and figure out creative ways to solve the issue,
it might not pop out at you immediately.

## Also Consider

  Another useful function is html\_table(), if your data is able to be
coerced into this type of object I would suggest trying this over the
method bellow. Another good set of tools is html\_element and
html\_elements. Lastly here is the rvest website for more information. [rvest](https://rvest.tidyverse.org/)

# Implementation

## R

    ## Load and install the packages that we'll be using today
    if (!require("pacman")) install.packages("pacman")

    ## Loading required package: pacman

    pacman::p_load(dplyr, rvest, data.table, hrbrthemes, stringi, XML)

    black_opals = read_html("https://blackopaldirect.com/product/black-opals/2-86-ct-black-opal-11-6x9-7x3-9mm/") # Website of interest

    price = black_opals %>% 
      html_node("#product-103505 > div.summary.entry-summary > p.price > span > bdi") %>% # Find the exact element's node for the price
      html_text() # Convert it to text 

    price # print the price

    ## [1] "US$2,500.00"
