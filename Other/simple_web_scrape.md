---
title: Simple Web Scraping
parent: Other
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Introduction

Webscraping is the processs of programmatically extracting information from the internet that was intended to be displayed in a browser. But it should only be used as a last resort; generally an API (appplication programming interface) is a much better way to obtain information, if one is available.

If you do find yourself in a scraping situation, be really sure to check it's legally allowed and that you are not violating the website's `robots.txt` rules. `robots.txt` is a special file on almost every website that sets out what's fair play to crawl (conditional on legality) and what your webscraper should not go poking around in.

## Keep in Mind

  Remember that webscraping is an art as much a science so play around
with a problem and figure out creative ways to solve issues, it might
not pop out at you immediately.

# Implementation

## Python

Five of the most well-known and powerful libraries for webscraping in Python, which between them cover a huge range of needs, are [**requests**](https://docs.python-requests.org/en/master/), [**lxml**](https://lxml.de/), [**beautifulsoup**](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), [**selenium**](https://selenium-python.readthedocs.io/getting-started.html), and [**scrapy**](https://scrapy.org/). Broadly, requests is for downloading webpages via code, beautifulsoup and lxml are for parsing webpages and extracting info, and scrapy and selenium are full web-crawling solutions. For the special case of scraping table from websites, [**pandas**](https://pandas.pydata.org/) is the best option. 

For quick and simple webscraping of individual HTML tags, a good combo is **requests**, which does little more than go and grab the HTML of a webpage, and **beautifulsoup**, which then helps you to navigate the structure of the page and pull out what you're actually interested in. For dynamic webpages that use javascript rather than just HTML, you'll need **selenium**. To scale up and hit thousands of webpages in an efficient way, you might try **scrapy**, which can work with the other tools and handle multiple sessions, and all other kinds of bells and whistles... it's actually a "web scraping framework".

Let's see a simple example using **requests** and **beautifulsoup**, followed by an example of extracting a table using **pandas**. First we need to import the packages; remember you may need to install these first by running `pip install packagename` on your computer's command line.


```python?example=scrape
import requests
from bs4 import BeautifulSoup
import pandas as pd
```

Now we'll specify a URL to scrape, download it as a page, and show some of the HTML as downloaded (here, the first 500 characters)


```python?example=scrape
url = "https://blackopaldirect.com/product/black-opals/2-86-ct-black-opal-11-6x9-7x3-9mm/"
page = requests.get(url)
print(page.text[:500])
```

    <!DOCTYPE html>
    <html lang="en-US">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no">
    <link rel="profile" href="http://gmpg.org/xfn/11">
    <link rel="pingback" href="https://blackopaldirect.com/xmlrpc.php">
    <!-- Facebook Pixel Code -->
    <script>
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=


That's a bit tricky to read, let alone get any useful data out of. So let's now use **beautifulsoup**, which parses extracted HTML. To pretty print the page use `.text`. In the example below, we'll just show the first 100 characters and we'll also use `rstrip` and `lstrip` to trim leading and trailing whitespace:


```python?example=scrape
soup = BeautifulSoup(page.text, 'html.parser')
print(soup.text[:100].lstrip().rstrip())
```

    2.86 ct black opal 11.6x9.7x3.9mm - Black Opal Direct


There are lots of different elements, with tags, that make up a page of HTML. For example, a title might have a tag 'h1' and a class 'product_title'. Let's see how we can retrieve anything with a class that is 'price' and a tag that is 'p' as these are the characteristics of prices displayed on the URL we are scraping.


```python?example=scrape
price_html = soup.find("p", {"class": "price"})
print(price_html)
```

    <p class="price"><span class="woocommerce-Price-amount amount"><bdi><span class="woocommerce-Price-currencySymbol">US$</span>2,500.00</bdi></span></p>


This returns the first tag found that satisfies the conditions (to get all tags matching the criteria use `soup.find_all`). To extract the value, just use `.text`:


```python?example=scrape
price_html.text
```




    'US$2,500.00'



Now let's see an example of reading in a whole table of data. For this, we'll use **pandas**, the ubiquitous Python library for working with data. We will read data from the first table on 'https://simple.wikipedia.org/wiki/FIFA_World_Cup' using **pandas**. The function we'll use is `read_html`, which returns a list of dataframes of all the tables it finds when you pass it a URL. If you want to filter the list of tables, use the `match=` keyword argument with text that only appears in the table(s) you're interested in.

The example below shows how this works; looking at the website, we can see that the table we're interested in (of past world cup results), has a 'fourth place' column while other tables on the page do not. Therefore we run:


```python?example=scrape
df_list = pd.read_html('https://simple.wikipedia.org/wiki/FIFA_World_Cup', match='Fourth Place')
# Retrieve first and only entry from list of dataframes
df = df_list[0]
df.head()
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Year</th>
      <th>Host</th>
      <th>Winner</th>
      <th>Score</th>
      <th>Runners-up</th>
      <th>Third Place</th>
      <th>Score.1</th>
      <th>Fourth Place</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1930 Details</td>
      <td>Uruguay</td>
      <td>Uruguay</td>
      <td>4 - 2</td>
      <td>Argentina</td>
      <td>United States</td>
      <td>[note 1]</td>
      <td>Yugoslavia</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1934 Details</td>
      <td>Italy</td>
      <td>Italy</td>
      <td>2 - 1(a.e.t.)</td>
      <td>Czechoslovakia</td>
      <td>Germany</td>
      <td>3 - 2</td>
      <td>Austria</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1938 Details</td>
      <td>France</td>
      <td>Italy</td>
      <td>4 - 2</td>
      <td>Hungary</td>
      <td>Brazil</td>
      <td>4 - 2</td>
      <td>Sweden</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1950 Details</td>
      <td>Brazil</td>
      <td>Uruguay</td>
      <td>[note 2]</td>
      <td>Brazil</td>
      <td>Sweden</td>
      <td>[note 2]</td>
      <td>Spain</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1954 Details</td>
      <td>Switzerland</td>
      <td>West Germany</td>
      <td>3 - 2</td>
      <td>Hungary</td>
      <td>Austria</td>
      <td>3 - 1</td>
      <td>Uruguay</td>
    </tr>
  </tbody>
</table>
</div>

This delivers the table neatly loaded into a **pandas** dataframe ready for further use.

## R

The “rvest” package is a webscraping package in R that provides a
tremendous amount of versatility, as well as being easy to use. For this
specific task, of web scrapping pages on a website, we will be using
read\_html(), html\_node(), html\_table(), html\_elements(), and
html\_text(). I will also make use of the selector gadget tool,(link for
the download:[Selector Gaget](https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb),
as well as F12, to find the html paths.

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

Another good tool is html\_element. Also here is the rvest website for
more information. [rvest](https://rvest.tidyverse.org/)
