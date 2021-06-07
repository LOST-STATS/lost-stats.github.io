---
title: Regular Expressions
parent: Data Manipulation
has_children: false
nav_order: 1
mathjax: false ## Switch to false if this page has no equations or other math rendering.
---

# Introduction

Regular expressions (AKA "Regex") can be thought of as a pattern of characters that describes a specific set of strings with a common structure. They can also be thought of as [state machines](https://www.youtube.com/watch?v=528Jc3q86F8). String functions can take a character variable and a regular expression, and show you whether and how they match. Regex is useful for extracting information from text such as documents, spreadsheets, log files, and code. Regex utilizes metacharacters that have specific meaning: `$ * + . ? [ ] ^ { } | ( ) \` to find what we are looking for within the string. They can be used for string matching / replacing, and are supported across several programming languages such as Python, R, Stata, SQL, and more, although syntax does sometimes differ slightly between languages. The metacharacters can be broken up into a few different groups based on their meaning. 

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
  - `\`: suppress the special meaning of metacharacters in regular expression. 
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

- Subexpressions can refer back to previously found strings
    - `()` can be wrapped around a part of the regular expression, and that part will be remembered.
    - `\1`, later in that regular expression, will refer to the contents of the first `()` being matched again (and `\2` would get the second, and so on). For example, `(.)\1` would match any string with a repeated character. This can also be used in substitution.  For example, regex `.*(pp).*` being substituted with `a\1ly` would replace `apple` with `apply`.

## Keep in Mind

- When using regular expressions everything is essentially a character, and we are writing patterns to match a specific sequence of characters.
- Most patterns use normal ASCII, which includes letters, digits, punctuation and other symbols like %#$@!, but unicode characters can be used to match any type of international text.

# Implementations

## Python

In Python, regular expressions are implemented in the [`re`](https://docs.python.org/3/library/re.html) module or, alternatively, through the `.str` interface in `pandas`. Let's go through a few examples:

If we want to search for all words that started with the characters "ab" we would use the character `^` to specify we want words that start with "ab".

```python
import re

strings = ["abcd", "cdab", "cabd", "c abd"]
filtered_strings = [s for s in strings if re.search(r"^ab", s)]

print(filtered_strings)
# ['abcd']
```

Some notes about this example:
* We've used the `re.search` function. Sometimes people instead use [`re.match`](https://docs.python.org/3/library/re.html#search-vs-match). `re.match` only looks for matches at the _beginning_ of strings, so the functions `re.search(r"^ab", s)` and `re.match(r"ab", s)` are equivalent.
* You'll notice that instead of using plain double quotes around our regular expression we used the pattern `r"^ab"`. The `r` means "raw string", and it turns off (almost) all escaping. Thus, `r"\d"` and `"\\d"` are equivalent. Because of the how common `\` is in regular expressions, it's usually wise to use raw strings for regular expressions to avoid confusing errors.

Alternatively, we could use also implement the above example with pandas:

```python
import pandas as pd

df = pd.DataFrame({"strings": ["abcd", "cdab", "cabd", "c abd"]})
df[df["strings"].str.contains(r"^ab", regex=True)]
```

If we instead want to *replace* the text that matches a regular expression, we can use the `re.sub` or pandas `.str.replace`:

```python
import re
import pandas as pd

strings = ["what", "why", "you", "blazers", "fire", "hello"]

# Replace all the vowels in strings containing a vowel with "!"
changed_strings = [
    re.sub(r"[aeiou]", "!", s)
    for s in strings
    if re.search(r"[aeiou]", s)
]
print(changed_strings)
# ['wh!t', 'y!!', 'bl!z!rs', 'f!r!', 'h!ll!']

# Do the same thing in pandas
df = pd.DataFrame({"strings": strings})
changed_series = df.loc[
    df["strings"].str.contains(r"[aeiou]", regex=True),
    "strings"
].str.replace(r"[aeiou]", "!", regex=True)
print(changed_series)
# 0       wh!t
# 2        y!!
# 3    bl!z!rs
# 4       f!r!
# 5      h!ll!
# Name: strings, dtype: object
```

## R

In R, we can write our Regular expressions using the base R functions or with the **stringr** package functions. [RegExplain](https://www.garrickadenbuie.com/project/regexplain/) is an RStudio addin for regular expressions. Regular expressions can be tricky at times, and RegExplain can help make it easier. RegExplain will allow you to build your regular expressions interactively.

First, we can write a regular expression using the base R functions. Additional [resources](https://github.com/STAT545-UBC/STAT545-UBC-original-website/blob/master/block022_regular-expression.md) on Regex, string functions, and syntax. We can use the grep() function to identify filenames, for example. If we set the argument `value = TRUE`, `grep()` returns the matches, while `value = FALSE` returns their indices. `grepl()` is a similar function but returns a logical vector. Including `ignore.case = TRUE` ignores case sensitivity. Some special characters in R cannot be directly coded in a string (i.e `'`), so we have to "escape" the single quote in the pattern, by preceding it with `\`.

One important note about working with regular expressions in R is that, because `\` itself needs to be escaped, we must escape this metacharacter with a double backslash like `\\$`.   

For example, if we want to search for all words that started with the characters "ab" we would use the character `^` to specify we want words that start with "ab".   

```r
#create a string 
(string <- c("abcd", "cdab", "cabd", "c abd")) 

# regex to search for strings that start with ab
grep("^ab", string, value = TRUE)
```

`grepl()` will tell us if there is a match to the pattern. Functions like `sub()` and `gsub()` replace the matches with new text. There are plenty of subexpressions so I will show a few.

```r
string <- c("what", "why", "you", "blazers", "fire", "hello") # create string

# here we get TRUE/FALSE depending on if the text has any of the vowels "[aeiou]"    
grepl("[aeiou]", string)

#we can use sub() and gsub() to replace text
sub("[aeiou]", "!", string)
```

Second, We can write the regular expression using the stringr package, which is said to be easier to use and remember. We can write a regular expression and use the stringr::str_match() function to extract all the phone numbers from the string. There are a number of other useful string functions in the [stringr](https://github.com/hadley/stringr) package. Additional resources on Regex, string functions, and syntax can be found [here](https://github.com/STAT545-UBC/STAT545-UBC-original-website/blob/master/block022_regular-expression.md).

Similar to using the base R function, we still want to use `^` to specify we want a work that starts with "ab". Now we have to specify that we want the entire word, not just the "ab" portion by including the `.*` syntax, which means "look for any character (`.`) any number of times (`*`)", in other words it picks up anything.

```r
# load package
library(stringr)

# create a string
(string <- c("abcd", "cdab", "cabd", "c abd")) 

# regex to search for strings that start with ab
str_match(string, "^ab.*")

# Similar to the grepl function there is str_detect, and similar to the gsub function there is str_replace
str_detect(string, "[aeiou]") # tells us T/F if the word contains any of the vowels in the given range.
str_replace(x, "[aeiou]", "!") # we can replace any vowels in the specified range with a ```!``` in their respective words
```
