---
title: Title of page
parent: Category
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Name of Page (don't put INTRODUCTION here; put the name of the page)

If this is your first time writing a new LOST page, please consider giving the [Contributing](https://lost-stats.github.io/Contributing/Contributing.html) page a look.

INTRODUCTION SECTION

Remember that you can use inline math, e.g. $$x + y$$. In general, you should render variables in math mode ($$X$$, $$Y$$, etc.)

You can also render math in display mode:

$$
\int_a^b f(x)dx
$$

The Introduction, Keep in Mind, and Also Consider sections should be LANGUAGE-AGNOSTIC, i.e. they should not be specific to a given language. Language-specific stuff goes in Implementations.

## Keep in Mind

- LIST OF IMPORTANT THINGS TO REMEMBER ABOUT USING THE TECHNIQUE

## Also Consider

- LIST OF OTHER TECHNIQUES THAT WILL COMMONLY BE USED ALONGSIDE THIS PAGE'S TECHNIQUE
- (E.G. LINEAR REGRESSION LINKS TO ROBUST STANDARD ERRORS),
- OR INSTEAD OF THIS TECHNIQUE
- (E.G. PIE CHART LINKS TO A BAR PLOT AS AN ALTERNATIVE)
- WITH EXPLANATION
- INCLUDE LINKS TO OTHER LOST PAGES WITH THE FORMAT [Description]({{ "/Category/page.html" | relative_url }}). Categories include Data_Manipulation, Geo-Spatial, Machine_Learning, Model_Estimation, Presentation, Summary_Statistics, Time_Series, and Other, with subcategories at some points. Check the URL of the page you want to link to on [the published site](https://lost-stats.github.io/).

# Implementations

Notes on implementations: 

- Keep in mind this will NOT PRODUCE CODE OUTPUT FOR YOU, so if you want output to be visible you'll need to include it directly (and on that note, submit this as an .md file, not .rmd).
- Keep implementations fairly short - you're not writing a book chapter here! A single straightforward demonstration is often all you need. Extra demonstrations can be handy if there's an important alternate task you want to show. You don't need to show off every option.
- Ideally we will use the same data for all the examples across all the languages. So it's a good idea to convert your data into something universal (like CSV).

## NAME OF LANGUAGE/SOFTWARE 1

```identifier for language type, see this page: https://github.com/jmm/gfm-lang-ids/wiki/GitHub-Flavored-Markdown-%28GFM%29-language-IDs
Commented code demonstrating the technique
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
