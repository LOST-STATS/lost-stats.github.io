---
title: Building Custom Tables
parent: Tables
grand_parent: Presentation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Building Custom Tables


Sometimes you need to create a table that doesn't fit neatly into any of the other categories of table shown the [Tables]({{ "/Presentation/Tables.html" | relative_url }}) page.


## Keep in Mind

- Graphs are sometimes a more effective way to convay information.

## Also Consider

- Check the [Tables]({{ "/Presentation/Tables.html" | relative_url }}) page to see if any of those approaches will work for your application.


# Implementations

Notes on implementations: 

- Keep in mind this will NOT PRODUCE CODE OUTPUT FOR YOU, so if you want output to be visible you'll need to include it directly (and on that note, submit this as an .md file, not .rmd).
- Keep implementations fairly short - you're not writing a book chapter here! A single straightforward demonstration is often all you need. Extra demonstrations can be handy if there's an important alternate task you want to show. You don't need to show off every option.
- Ideally we will use the same data for all the examples across all the languages. So it's a good idea to convert your data into something universal (like CSV).

## R

There are multiple ways to create custom tables, here I am focusing on RStudio's **[gt](https://gt.rstudio.com/)** because it is easy to use. 

```r
# Install gt if necessary
# install.packages('gt')
library(gt)

# Get mtcars data
data(mtcars)
```

LOST does have a code checker for some languages. If you have code split over multiple code chunks, and earlier code chunks are necessary to run later ones, give the chunk an ID like so:

```language?example=examplename
x = 1
```

```language?example=examplename
x = x + 1
```

Or if the code checker should skip it, say so!

```language?skip=true&skipReason=file_does_not_exist
read.csv('file-that-does-not-exist.csv')
```

## NAME OF LANGUAGE/SOFTWARE 2 WHICH HAS MULTIPLE APPROACHES

There are two ways to perform this technique in language/software 2.

First, explanation of what is different about the first way:

```identifier for language type, see this page: https://github.com/jmm/gfm-lang-ids/wiki/GitHub-Flavored-Markdown-%28GFM%29-language-IDs
Commented code demonstrating the technique
```

Second, explanation of what is different about the second way:

```identifier for language type, see this page: https://github.com/jmm/gfm-lang-ids/wiki/GitHub-Flavored-Markdown-%28GFM%29-language-IDs
Commented code demonstrating the technique
```
