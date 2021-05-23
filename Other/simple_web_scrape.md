# Introduction

  The “rvest” package is a webscraping package in R that provides a
tremendous amount of versatility, as well as being easy to use. For this
specific task, of web scrapping pages on a website, we will be using
read\_html(), html\_node(), html\_table(), html\_elements(), and
html\_text(). I will also make use of the selector gadget tool,(link for
the download:[Selector Gaget](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb),
as well as F12, to find the html paths.

## Keep in Mind

  Remember that webscraping is an art as much a science so play around
with a problem and figure out creative ways to solve issues, it might
not pop out at you immediately.

## Also Consider

 Another good tool is html\_element. Also here is the rvest website for
more information. [rvest](https://rvest.tidyverse.org/)

# Implementation

## R

### html\_node and html\_text

    library(rvest)

    black_opals = read_html("https://blackopaldirect.com/product/black-opals/2-86-ct-black-opal-11-6x9-7x3-9mm/") # Website of interest

    price = black_opals %>% 
      html_node("#product-103505 > div.summary.entry-summary > p.price > span > bdi") %>% # Find the exact element's node for the price
      html_text() # Convert it to text 

    price # print the price

    ## [1] "US$2,500.00"

### html\_table

    world_cup = read_html("https://simple.wikipedia.org/wiki/FIFA_World_Cup") # Past_World_Cup_results

    cup_table = world_cup %>% html_elements(xpath = "/html/body/div[3]/div[3]/div[5]/div[1]/table[2]") %>%
      html_table() # Extract html elements

    cup_table = cup_table[[1]] # Assign the table from the lists

    cup_table %>% head(5) # First 5 obs

    ## # A tibble: 5 x 8
    ##   Year    Host    Winner  Score  `Runners-up` `Third Place` Score `Fourth Place`
    ##   <chr>   <chr>   <chr>   <chr>  <chr>        <chr>         <chr> <chr>         
    ## 1 1930 D~ Uruguay Uruguay 4 - 2  Argentina    United States [not~ Yugoslavia    
    ## 2 1934 D~ Italy   Italy   2 - 1~ Czechoslova~ Germany       3 - 2 Austria       
    ## 3 1938 D~ France  Italy   4 - 2  Hungary      Brazil        4 - 2 Sweden        
    ## 4 1950 D~ Brazil  Uruguay [note~ Brazil       Sweden        [not~ Spain         
    ## 5 1954 D~ Switze~ West G~ 3 - 2  Hungary      Austria       3 - 1 Uruguay
