---
title: Regular Expressions
parent: Data Manipulation
has_children: false
nav_order: 1
mathjax: false ## Switch to false if this page has no equations or other math rendering.
---

# Introduction

Regular expressions (AKA "Regex") can be thought of as a pattern of characters that describes a specific set of strings with a common structure. String functions can take a character variable and a regular expression, and show you how they match. Regex is useful for extracting information from text such as documents, spreadsheets, log files, and code. Regex utilizes metacharacters that have specific meaning: `$ * + . ? [ ] ^ { } | ( ) \` to find what we are looking for within the string. They can be used for string matching / replacing, and are supported across several programming languages such as Python, R, Stata, SQL, and more.

## Keep in Mind

- When using regular expressions everything is essentially a character, and we are writing patterns to match a specific sequence of characters.
- Some special characters in R cannot be directly coded in a string (i.e `'`), so we have to "escape" the single quote in the pattern, by preceding it with `\`
- Most patterns use normal ASCII, which includes letters, digits, punctuation and other symbols like %#$@!, but unicode characters can be used to match any type of international text.

## Also Consider

- [RegExplain](https://www.garrickadenbuie.com/project/regexplain/) is an RStudio addin for regular expressions. Regular expressions can be tricky at times, and RegExplain can help make it easier. RegExplain will allow you to build your regular expressions interactively.

# Implementations

## R

There are two ways to perform this technique in R.

First, we can write the regular expression using base R functions. Additional [Resources](https://github.com/STAT545-UBC/STAT545-UBC-original-website/blob/master/block022_regular-expression.md) on Regex, string functions, and syntax. We can use the grep() function to identify filenames, for example. If we set the argument ``` value = TRUE ```, ``` grep() ``` returns the matches, while ``` value = FALSE ``` returns their indices. ``` grepl() ``` is a similar function but returns a logical vector. Including ``` ignore.case = TRUE ``` ignores case sensitivity.  

```r
#load packages

library(tidyverse)

files <- list.files()
head(files)

grep("Star", files, value = TRUE)

grep("Star", files, value = TRUE, ignore.case = TRUE)

grepl("Star", files)
```

Second, We can write the regular expression using the stringr package, which is said to be easier to use and remember. We can write a regular expression and use the stringr::str_match() function to extract all the phone numbers from the string. Some useful functions from the [stringr](https://github.com/hadley/stringr) package. Additional [Resources](https://github.com/STAT545-UBC/STAT545-UBC-original-website/blob/master/block022_regular-expression.md) on Regex, string functions, and syntax.

```r
#load packages

library(tidyverse)
library(stringr)

#create a string

phone_numbers <- c(
  "(541) 471 3918",
  "(603)281-0308",
  "Home: 425-707-7220",
  "(814)-462-8074",
  "9704443106",
  "I don't have a phone."
  )
  
#write regex

pattern <- '.*(\\d{3}).*(\\d{3}).*(\\d{4})'

#use stringr::str_match()

str_match(phone_numbers, pattern)

```

Similarly, we can search for all the numbers in a string using the stringr::str_match_all() function. 

```r
favorites <- c(
  "My favorite is 44 or 42",
  "I like 13 and 17",
  "Umm, 23 and 21"
)

str_match_all(favorites, "\\d+")

```