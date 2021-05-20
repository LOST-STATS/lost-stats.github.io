# Introduction

  The “rvest” package is a web scraping package in R that provides a
tremendous amount of versatility, as well as being easy to use. For this
specific task, of web scrapping though pages on a website, we will be
using read\_html(), html\_elements(), and html\_text(). I will also make
use of the selector gadget tool,(link for the download:
[Selector Gaget](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb)
to find the html elements.

## Keep in Mind

  I prefer to use html\_elements over html\_element, this is because
elements is more versatile. Also remember that web scraping is an art as
much a since so play around with a problem and figure out creative ways
to solve the issue, it might not pop out at you immediately.

## Also Consider

  Another useful function is html\_table(), if your data is able to be
coerced into this type of object I would suggest trying this over the
method bellow. Lastly here is the rvest website for more information.
[rvest](https://rvest.tidyverse.org/)

# Implementation

## R

    ## Load and install the packages that we'll be using today
    if (!require("pacman")) install.packages("pacman")

    ## Loading required package: pacman

    pacman::p_load(dplyr, rvest, data.table, hrbrthemes, stringi, xml2)

  So lets get started, the first step when trying to scrape through
multiple pages, is to look for common delineation between pages on the
same sight.

<img src="images/Base_url.PNG" width="390" />

  This is the normal http that will give you the first 120 results for
the Eugene Craigslist.

    # Base URL, Look for the consistent piece of the HTTP across tabs/sections
    base_url = c('https://eugene.craigslist.org/d/for-sale/search/sss?s=')

<img src="images/dif_url.PNG" width="432" />

Between these two web addresses we can see that they have a simple
number delineation, so we can implement a for loop across the pages we
want to look at.

read\_html(): This will read the http it is given. html\_elements():
This extracts the element you give it. A good tool for this is the
selector gadget, alternatively F12 will open up a window that allows you
to go through a websites elements.  
html\_text(): This creates a character variable of the element passed to
it.

    # Find common delineations. In this case it is simply a number
    url_num_change = seq(0,3000,120) # This is a sequence from 0-3000 by 120 and it is what we will use to change in our html
    all <- data.frame() # Placeholder dataframe

    for (x in 1:as.numeric(length(url_num_change))) {
      j = paste(base_url,url_num_change[x]) # Combine all character strings
      v = gsub(" ", "", j)  # Remove empty spaces from string
      date_col = read_html(v) %>% html_elements(".result-date") %>% html_text() # Grab the date 
      price = read_html(v) %>% html_elements(".result-price") %>% html_text() # Grab the price 
      descrip = read_html(v) %>% html_elements(".hdrlnk") %>% html_text() # Grab the description 
      k = cbind(date_col,price,descrip) # Coll bind 
      Sys.sleep(3) # Be nice!
      df = data.frame(k) # Assign to a place holder df
      all <- rbind(all,df) #Make a  total data from with the assignment operator
    }

    # This will of course change over time and your output will not be the same.
    head(all,5) # Print the first 5 obs

    ##   date_col price                                                    descrip
    ## 1   May 19   $50                                                  Kids desk
    ## 2   May 19   $50                             215/65R 15s on chry van wheels
    ## 3   May 19  $125                                                  Kids Desk
    ## 4   May 19  $125                                     40 ft extension ladder
    ## 5   May 19   $25 Antique Chinese White Porcelain Ginger Jar Lamp (Oriental)
