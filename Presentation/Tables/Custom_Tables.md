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

## R

There are multiple ways to create custom tables, here I am focusing on RStudio's **[gt](https://gt.rstudio.com/)** because it is easy to use. It has many more options than I am demonstrating here so be sure to look at their documentation.

```r
# Install gt if necessary
# install.packages('gt')
library(gt)

# I'm also loading magrittr so I can use the %>% pipe
library(magrittr)

# first create a tibble or data.frame object that contains all the information you want in your rows and columns.

# for this example I'll use a generic dataset
# which I'm truncating to make the final table easier to see
input_df = head(mtcars, 6)
input_df = input_df[, 1:5]


# create the table using the data.fram rownames in the table
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

<div id="inbiquicou" style="overflow-x:auto;overflow-y:auto;width:auto;height:auto;">
<style>html {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', 'Fira Sans', 'Droid Sans', Arial, sans-serif;
}

#inbiquicou .gt_table {
  display: table;
  border-collapse: collapse;
  margin-left: auto;
  margin-right: auto;
  color: #333333;
  font-size: 16px;
  font-weight: normal;
  font-style: normal;
  background-color: #FFFFFF;
  width: auto;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #A8A8A8;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #A8A8A8;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
}

#inbiquicou .gt_heading {
  background-color: #FFFFFF;
  text-align: center;
  border-bottom-color: #FFFFFF;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
}

#inbiquicou .gt_title {
  color: #333333;
  font-size: 125%;
  font-weight: initial;
  padding-top: 4px;
  padding-bottom: 4px;
  padding-left: 5px;
  padding-right: 5px;
  border-bottom-color: #FFFFFF;
  border-bottom-width: 0;
}

#inbiquicou .gt_subtitle {
  color: #333333;
  font-size: 85%;
  font-weight: initial;
  padding-top: 0;
  padding-bottom: 6px;
  padding-left: 5px;
  padding-right: 5px;
  border-top-color: #FFFFFF;
  border-top-width: 0;
}

#inbiquicou .gt_bottom_border {
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}

#inbiquicou .gt_col_headings {
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
}

#inbiquicou .gt_col_heading {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: normal;
  text-transform: inherit;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 6px;
  padding-left: 5px;
  padding-right: 5px;
  overflow-x: hidden;
}

#inbiquicou .gt_column_spanner_outer {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: normal;
  text-transform: inherit;
  padding-top: 0;
  padding-bottom: 0;
  padding-left: 4px;
  padding-right: 4px;
}

#inbiquicou .gt_column_spanner_outer:first-child {
  padding-left: 0;
}

#inbiquicou .gt_column_spanner_outer:last-child {
  padding-right: 0;
}

#inbiquicou .gt_column_spanner {
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 5px;
  overflow-x: hidden;
  display: inline-block;
  width: 100%;
}

#inbiquicou .gt_group_heading {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: middle;
}

#inbiquicou .gt_empty_group_heading {
  padding: 0.5px;
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  vertical-align: middle;
}

#inbiquicou .gt_from_md > :first-child {
  margin-top: 0;
}

#inbiquicou .gt_from_md > :last-child {
  margin-bottom: 0;
}

#inbiquicou .gt_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  margin: 10px;
  border-top-style: solid;
  border-top-width: 1px;
  border-top-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 1px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 1px;
  border-right-color: #D3D3D3;
  vertical-align: middle;
  overflow-x: hidden;
}

#inbiquicou .gt_stub {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-right-style: solid;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  padding-left: 5px;
  padding-right: 5px;
}

#inbiquicou .gt_stub_row_group {
  color: #333333;
  background-color: #FFFFFF;
  font-size: 100%;
  font-weight: initial;
  text-transform: inherit;
  border-right-style: solid;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
  padding-left: 5px;
  padding-right: 5px;
  vertical-align: top;
}

#inbiquicou .gt_row_group_first td {
  border-top-width: 2px;
}

#inbiquicou .gt_summary_row {
  color: #333333;
  background-color: #FFFFFF;
  text-transform: inherit;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
}

#inbiquicou .gt_first_summary_row {
  border-top-style: solid;
  border-top-color: #D3D3D3;
}

#inbiquicou .gt_first_summary_row.thick {
  border-top-width: 2px;
}

#inbiquicou .gt_last_summary_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}

#inbiquicou .gt_grand_summary_row {
  color: #333333;
  background-color: #FFFFFF;
  text-transform: inherit;
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
}

#inbiquicou .gt_first_grand_summary_row {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 5px;
  padding-right: 5px;
  border-top-style: double;
  border-top-width: 6px;
  border-top-color: #D3D3D3;
}

#inbiquicou .gt_striped {
  background-color: rgba(128, 128, 128, 0.05);
}

#inbiquicou .gt_table_body {
  border-top-style: solid;
  border-top-width: 2px;
  border-top-color: #D3D3D3;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
}

#inbiquicou .gt_footnotes {
  color: #333333;
  background-color: #FFFFFF;
  border-bottom-style: none;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
}

#inbiquicou .gt_footnote {
  margin: 0px;
  font-size: 90%;
  padding-left: 4px;
  padding-right: 4px;
  padding-left: 5px;
  padding-right: 5px;
}

#inbiquicou .gt_sourcenotes {
  color: #333333;
  background-color: #FFFFFF;
  border-bottom-style: none;
  border-bottom-width: 2px;
  border-bottom-color: #D3D3D3;
  border-left-style: none;
  border-left-width: 2px;
  border-left-color: #D3D3D3;
  border-right-style: none;
  border-right-width: 2px;
  border-right-color: #D3D3D3;
}

#inbiquicou .gt_sourcenote {
  font-size: 90%;
  padding-top: 4px;
  padding-bottom: 4px;
  padding-left: 5px;
  padding-right: 5px;
}

#inbiquicou .gt_left {
  text-align: left;
}

#inbiquicou .gt_center {
  text-align: center;
}

#inbiquicou .gt_right {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

#inbiquicou .gt_font_normal {
  font-weight: normal;
}

#inbiquicou .gt_font_bold {
  font-weight: bold;
}

#inbiquicou .gt_font_italic {
  font-style: italic;
}

#inbiquicou .gt_super {
  font-size: 65%;
}

#inbiquicou .gt_two_val_uncert {
  display: inline-block;
  line-height: 1em;
  text-align: right;
  font-size: 60%;
  vertical-align: -0.25em;
  margin-left: 0.1em;
}

#inbiquicou .gt_footnote_marks {
  font-style: italic;
  font-weight: normal;
  font-size: 75%;
  vertical-align: 0.4em;
}

#inbiquicou .gt_asterisk {
  font-size: 100%;
  vertical-align: 0;
}

#inbiquicou .gt_slash_mark {
  font-size: 0.7em;
  line-height: 0.7em;
  vertical-align: 0.15em;
}

#inbiquicou .gt_fraction_numerator {
  font-size: 0.6em;
  line-height: 0.6em;
  vertical-align: 0.45em;
}

#inbiquicou .gt_fraction_denominator {
  font-size: 0.6em;
  line-height: 0.6em;
  vertical-align: -0.05em;
}
</style>
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
</div>
