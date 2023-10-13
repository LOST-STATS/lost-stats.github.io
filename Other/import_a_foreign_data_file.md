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
- Before doing this you will probably find it useful to [Set a Working Directory]({{ "/Other/set_a_working_directory.html" | relative_url }})

## Also Consider

- [Import a Delimited Data File (CSV, TSV)]({{ "/Other/import_a_delimited_data_file.html" | relative_url }})
- [Import a Fixed-Width Data File]({{ "/Other/import_a_fixed_width_data_file.html" | relative_url }})
- [Export Data to a Foreign Format]({{ "/Other/export_data_to_a_foreign_format.html" | relative_url }})

# Implementations

Because there are so many potential foreign formats, these implementations will be more about listing the appropriate commands with example syntax than providing full working examples. Make sure that you fill in the proper filename. The filename should include a filepath, or you should [Set a Working Directory]({{ "/Other/set_a_working_directory.html" | relative_url }}).

## Julia

Julia ecosystem features many packages for working with various file formats.
Here we'll consider

- [Arrow.jl](https://arrow.apache.org/julia/dev/)
- [Avro.jl](https://juliadata.github.io/Avro.jl/stable/)
- [Parquet2.jl](https://expandingman.gitlab.io/Parquet2.jl/)
- [XLSX.jl](https://felipenoris.github.io/XLSX.jl/stable/)

```julia?skip=true&skipReason=files_dont_exist
# Uncomment if you want to install packages programmatically
# using Pkg

# We'll load all the data into DataFrames for uniform processing
using DataFrames

# Apache Arrow
# To install the package
# Pkg.add("Arrow")
using Arrow
df = DataFrame(Arrow.Table("filename.arrow")) # load (mmap) data and convert it to a DataFrame for analysis

# Apache Avro
# To install the package
# Pkg.add("Avro")
using Avro
df = DataFrame(Avro.readtable("filename.avro")) # load data and convert it to a DataFrame for analysis

# Apache Parquet
# To install the package
# Pkg.add("Parquet2")
using Parquet2
df = DataFrame(Parquet2.Dataset("filename.parq"); copycols=false) # load data and convert it to a DataFrame for analysis

# Apache Parquet
# To install the package
# Pkg.add("XLSX")
using XLSX
# load data from the specified sheet in the file and convert it to a DataFrame for analysis
df = DataFrame(XLSX.readtable("filename.xlsx", "mysheet"))
```

## R

```r?skip=true&skipReason=files_dont_exist
# Generally, you may use the rio package to import any tabular data type to be read in fluently without requiring a specification of the file type.
library(rio)
data <- import('filename.xlsx')
data <- import('filename.dta')
data <- import('filename.sav')

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
