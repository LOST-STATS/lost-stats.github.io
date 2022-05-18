---
title: Building Custom Tables
parent: Tables
grand_parent: Presentation ## Optional for indexing
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Building Custom Tables


Sometimes you need to create a table that doesn't fit neatly into any of the other categories of table shown the [Tables]({{ "/Presentation/Tables/Tables.html" | relative_url }}) page.


## Keep in Mind

- Graphs are sometimes a more effective way to convey information.

## Also Consider

- Check the [Tables]({{ "/Presentation/Tables/Tables.html" | relative_url }}) page to see if any of those approaches will work for your application.


# Implementations

## R

There are lots of ways to create custom tables, I am using RStudio's **[gt](https://gt.rstudio.com/)** because it is easy to use and gives me a lot of control over the table elements. It has many more options than I am demonstrating  so be sure to look at their documentation.

```r
# Install gt if necessary
# install.packages('gt')
library(gt)

# I'm also loading magrittr so I can use the %>% pipe
library(magrittr)

# you data will need to be in a data.frame or tibble object
# for this example I'll use the generic dataset mtcars
# which I'm truncating to make the final table easier to see
input_df = head(mtcars, 6)
input_df = input_df[, 1:5]


# create the table including the data.frame rownames
Ex_table = gt(input_df, rownames_to_stub = TRUE)


# add title, subtitle, and source note
Ex_table = Ex_table %>%
  tab_header(
    title = md("**Title in Bold Text**"),
    subtitle = "subtitle"
  ) %>%
  tab_source_note("Data from mtcars")


# add groupings to rows
Ex_table = Ex_table %>%
  tab_row_group(
    label = "4 Cylinder",
    rows = cyl == 4
  ) %>%
  tab_row_group(
    label = "6 Cylinder",
    rows = cyl == 6
  ) %>%
  tab_row_group(
    label = "8 Cylinder",
    rows = cyl == 8
  ) 
  
```

This produces:


<table class="gt_table">
  <thead class="gt_header">
    <tr>
      <th colspan="6" class="gt_heading gt_title gt_font_normal" style><strong>Title in Bold Text</strong></th>
    </tr>
    <tr>
      <th colspan="6" class="gt_heading gt_subtitle gt_font_normal gt_bottom_border" style>subtitle</th>
    </tr>
  </thead>
  <thead class="gt_col_headings">
    <tr>
      <th class="gt_col_heading gt_columns_bottom_border gt_left" rowspan="1" colspan="1"></th>
      <th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1">mpg</th>
      <th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1">cyl</th>
      <th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1">disp</th>
      <th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1">hp</th>
      <th class="gt_col_heading gt_columns_bottom_border gt_right" rowspan="1" colspan="1">drat</th>
    </tr>
  </thead>
  <tbody class="gt_table_body">
    <tr class="gt_group_heading_row">
      <td colspan="6" class="gt_group_heading">8 Cylinder</td>
    </tr>
    <tr class="gt_row_group_first"><td class="gt_row gt_right gt_stub">Hornet Sportabout</td>
<td class="gt_row gt_right">18.7</td>
<td class="gt_row gt_right">8</td>
<td class="gt_row gt_right">360</td>
<td class="gt_row gt_right">175</td>
<td class="gt_row gt_right">3.15</td></tr>
    <tr class="gt_group_heading_row">
      <td colspan="6" class="gt_group_heading">6 Cylinder</td>
    </tr>
    <tr class="gt_row_group_first"><td class="gt_row gt_right gt_stub">Mazda RX4</td>
<td class="gt_row gt_right">21.0</td>
<td class="gt_row gt_right">6</td>
<td class="gt_row gt_right">160</td>
<td class="gt_row gt_right">110</td>
<td class="gt_row gt_right">3.90</td></tr>
    <tr><td class="gt_row gt_right gt_stub">Mazda RX4 Wag</td>
<td class="gt_row gt_right">21.0</td>
<td class="gt_row gt_right">6</td>
<td class="gt_row gt_right">160</td>
<td class="gt_row gt_right">110</td>
<td class="gt_row gt_right">3.90</td></tr>
    <tr><td class="gt_row gt_right gt_stub">Hornet 4 Drive</td>
<td class="gt_row gt_right">21.4</td>
<td class="gt_row gt_right">6</td>
<td class="gt_row gt_right">258</td>
<td class="gt_row gt_right">110</td>
<td class="gt_row gt_right">3.08</td></tr>
    <tr><td class="gt_row gt_right gt_stub">Valiant</td>
<td class="gt_row gt_right">18.1</td>
<td class="gt_row gt_right">6</td>
<td class="gt_row gt_right">225</td>
<td class="gt_row gt_right">105</td>
<td class="gt_row gt_right">2.76</td></tr>
    <tr class="gt_group_heading_row">
      <td colspan="6" class="gt_group_heading">4 Cylinder</td>
    </tr>
    <tr class="gt_row_group_first"><td class="gt_row gt_right gt_stub">Datsun 710</td>
<td class="gt_row gt_right">22.8</td>
<td class="gt_row gt_right">4</td>
<td class="gt_row gt_right">108</td>
<td class="gt_row gt_right">93</td>
<td class="gt_row gt_right">3.85</td></tr>
  </tbody>
  <tfoot class="gt_sourcenotes">
    <tr>
      <td class="gt_sourcenote" colspan="6">Data from mtcars</td>
    </tr>
  </tfoot>
  
</table>


Citation for gt:  
Iannone R, Cheng J, Schloerke B (2022). gt: Easily Create Presentation-Ready Display Tables. https://gt.rstudio.com/, https://github.com/rstudio/gt.
