---
title: Regular Expressions
parent: Data Manipulation
has_children: false
nav_order: 1
mathjax: false ## Switch to false if this page has no equations or other math rendering.
---

# Introduction

Regular expressions (AKA "Regex") can be thought of as a pattern of characters that describes a specific set of strings with a common structure. String functions can take a character variable and a regular expression, and show you how they match. Regex is useful for extracting information from text such as documents, spreadsheets, log files, and code. Regex utilizes metacharacters that have specific meaning: `$ * + . ? [ ] ^ { } | ( ) \` to find what we are looking for within the string. They can be used for string matching / replacing, and are supported across several programming languages such as Python, R, Stata, SQL, and more. The metacharacters can be broken up into a few different groups based on their meaning. 

- Specify the amount of repetitions of the pattern
  - `*`: matches at least 0 times.   
  - `+`: matches at least 1 times.     
  - `?`: matches at most 1 times.    
  - `{n}`: matches exactly n times.    
  - `{n,}`: matches at least n times.    
  - `{n,m}`: matches between n and m times.

- Specify where the match will be located in the string or word 
  - `^`: matches the start of the string.   
  - `$`: matches the end of the string.   
  - `\b`: matches the empty string at either edge of a _word_. Don't confuse it with `^ $` which marks the edge of a _string_.
  - `\B`: matches the empty string provided it is not at an edge of a word.

- Operators 
  - `.`: matches any single character.
  - `[...]`: a character list, matches any one of the characters inside the square brackets. 
  - `[^...]`: an inverted character list. Matches any characters __except__ those inside the square brackets.  
  - `\`: suppress the special meaning of metacharacters in regular expression. Because `\` itself needs to be escaped in R, we must escape this metacharacter with a double backslash like `\\$`.   
  - `|`: an "or" operator. Matches patterns on either side of the `|`.  
  - `(...)`: grouping in regular expressions. 
  
- Specify entire classes of characters like numbers or letters

  - Two Types: One uses  `[:` and `:]` around a predefined name, and the other uses `\` and a special character
  
  - `[:digit:]` or `\d`: digits, equivalent to `[0-9]`.  
  - `\D`: non-digits, equivalent to `[^0-9]`.  
  - `[:lower:]`: lower-case letters, equivalent to `[a-z]`.  
  - `[:upper:]`: upper-case letters, equivalent to `[A-Z]`.
  - `[:punct:]`: punctuation characters.
  - `[:alnum:]`: alphanumeric characters.

## Keep in Mind

- When using regular expressions everything is essentially a character, and we are writing patterns to match a specific sequence of characters.
- Most patterns use normal ASCII, which includes letters, digits, punctuation and other symbols like %#$@!, but unicode characters can be used to match any type of international text.

# Implementations

## R

In R, we can write our Regular expressions using the base R functions or with the stringr package functions. [RegExplain](https://www.garrickadenbuie.com/project/regexplain/) is an RStudio addin for regular expressions. Regular expressions can be tricky at times, and RegExplain can help make it easier. RegExplain will allow you to build your regular expressions interactively.

First, we can write a regular expression using the base R functions. Additional [Resources](https://github.com/STAT545-UBC/STAT545-UBC-original-website/blob/master/block022_regular-expression.md) on Regex, string functions, and syntax. We can use the grep() function to identify filenames, for example. If we set the argument ``` value = TRUE ```, ``` grep() ``` returns the matches, while ``` value = FALSE ``` returns their indices. ``` grepl() ``` is a similar function but returns a logical vector. Including ``` ignore.case = TRUE ``` ignores case sensitivity. Some special characters in R cannot be directly coded in a string (i.e `'`), so we have to "escape" the single quote in the pattern, by preceding it with `\` .

For example, if we want to search for all words that started with the characters "ab" we would use the character ``` ^ ``` to specify we want words that start with "ab".   

```r
#load packages

library(tidyverse)

#create a string 

(string <- c("abcd", "cdab", "cabd", "c abd")) 

head(string)

#regex to search for strings that start with ab

grep("^ab", string, value = TRUE)


```

```grepl()``` will tell us if there is a match to the pattern. 

```r
string <- c("what", "why", "you", "blazers", "fire", "hello") # create string

# here we get TRUE/FALSE depending on if the text has any of the vowels in the range "[aeiou]"    
grepl("[aeiou]", string)
```

Second, We can write the regular expression using the stringr package, which is said to be easier to use and remember. We can write a regular expression and use the stringr::str_match() function to extract all the phone numbers from the string. Some useful functions from the [stringr](https://github.com/hadley/stringr) package. Additional [Resources](https://github.com/STAT545-UBC/STAT545-UBC-original-website/blob/master/block022_regular-expression.md) on Regex, string functions, and syntax.

Similar to using the base R function, we still want to use ``` ^ ``` to specify we want a work that starts with "ab". Now we have to specify that we want the entire word, not just the "ab" portion by including the ``` .* ``` syntax.

```r
#load packages

library(tidyverse)
library(stringr)

#create a string

(string <- c("abcd", "cdab", "cabd", "c abd")) 

head(string)
  
#regex to search for strings that start with ab

str_match(string, "^ab.*")

```

We can use the ```str_detect()``` function to tell us if there's a match to the pattern similar to the ```grepl()``` function

```r
string <- c("what", "why", "you", "blazers", "fire", "hello") # create string

str_detect(string, "[aeiou]")
```