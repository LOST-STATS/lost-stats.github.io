---
title: Import a Foreign Data File
parent: Other
has_children: false
nav_order: 1
---


# Import a Foreign Data File

Commonly, data will be distributed in a format that is not native to the software that you are using, such as Excel. How can you import it?

This page is specifically about importing data files from formats specific to particular foreign software. For importing standard shared formats, see [Import a Delimited Data File (CSV, TSV)]({{ "/Other/import_a_delimited_data_file.html" | relative_url }}) or [Import a Fixed-Width Data File]({{ "/Other/import_a_fixed_width_data_file.html" | relative_url }}).

## Keep in Mind

- Check your data after it's imported to make sure it worked properly. Sometimes special characters will have trouble converting, or variable name formats are inconsistent, and so on. It never hurts to check!

## Also Consider

- [Import a Delimited Data File (CSV, TSV)]({{ "/Other/import_a_delimited_data_file.html" | relative_url }})
- [Import a Fixed-Width Data File]({{ "/Other/import_a_fixed_width_data_file.html" | relative_url }})
- [Export Data to a Foreign Format]({{ "/Other/export_data_to_a_foreign_format.html" | relative_url }})

# Implementations

Because there are so many potential foreign formats, these implementations will be more about listing the appropriate commands with example syntax than providing full working examples. Make sure that you fill in the proper filename. The filename should include a filepath, or you should [Set a Working Directory]({{ "/Other/set_a_working_directory.html" | relative_url }}).

## R

```r
# Load Excel files with the readxl package
# install.packages('readxl')
library(readxl)
data <- read_excel('filename.xlsx')

# Read Stata, SAS, and SPSS files with the haven package
# install.packages('haven')
library(haven)
data <- read_stata('filename.dta')
data <- read_spss('filename.sav')
# read_sas also supports .sas7bcat, or read_xpt supports transport files
data <- read_sas('filename.sas7bdat')

# Read lots of other types with the foreign package
# install.packages('foreign')
library(foreign)
data <- read.arff('filename.arff')
data <- read.dbf('filename.dbf')
data <- read.epiinfo('filename.epiinfo')
data <- read.mtb('filename.mtb')
data <- read.octave('filename.octave')
data <- read.S('filename.S')
data <- read.systat('filename.systat')
```

## Stata

Stata can import foreign files using the File -> Import menu. Alternately, you can use the import command:

```stata
import type using filename
```

where `type` can be `excel`, `spss`, `sas`, `haver`, or `dbase` (`import` can also be used to download data directly from sources like FRED).
