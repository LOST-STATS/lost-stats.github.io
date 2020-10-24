---
title: Get a List of Files
parent: Other
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Get a List of Files

When cleaning and compiling data, it is common to need to get a list of files in a directory so that you can loop over them. Often, the goal is to open the files one at a time so you can combine them together in some way.

For example, perhaps you have one data file per month, and want to compile them all together into a single data set.

## Keep in Mind

- Giving your files a consistent naming scheme will often make it easier to get this to work, as many approaches require you to give a template for the file names you want.
- Before doing this you will probably find it useful to [Set a Working Directory]({{ "/Other/set_a_working_directory.html" | relative_url }})

# Implementations

Note that, because these code examples necessarily refer to files on disk, they might not run properly if copied and pasted. But they can be used as templates.

## Python
The `glob` module finds all pathnames matching a specified pattern and stores them in a list. 

```python

import glob

# Retrieve all csvs in the working directory
list_of_files = glob.glob('*.csv')

# Retrieve all csvs in the working directory and all sub-directories
list_of_files = glob.glob('**/*.csv', recursive=True)
```

## R

The `list.files()` function can produce a list of files that can be looped over.

```r
# Get a list of all .csv files in the Data folder
# (which sits inside our working directory)
filelist <- list.files('Data','*.csv')

# filelist just contains file names now. If we want it to
# open them up from the Data folder we must say so
filelist <- paste0('Data/',filelist)

# Read them all in and then row-bind them together
# (assuming they're all the same format and can be rbind-ed)
datasets <- lapply(filelist,read.csv)
data <- do.call(rbind,datasets)

# Or, use the tidyverse with purrr
# (assuming they're all the same format and can be rbind-ed)
library(tidyverse)
data <- filelist %>%
  map(read_csv) %>%
  bind_rows()
```

## Stata

The `dir` function in Stata can be used to produce a list of files, which can be stored in a `local` (or `global`), and then looped over.

```stata
* Get a list of all .xlsx files in the Data folder
* (which sits inside our working directory)
local filelist: dir "Data/" files "*.xlsx"

* Append them all together
* (assuming this is what you want to do)
* filelist only contains file names - if we want it to look in
* the Data folder, we must say so explicitly
local firsttime = 1
foreach f in `filelist' {
	* import the data
	import excel using "Data/`f'", clear firstrow
	
	* Append it to the data we've already imported
	* Unless this is the first one we opened, in which
	* case just start a new file
	if `firsttime' == 0 {
		append using compiled_data.dta
	}
	save compiled_data.dta, replace
	local firsttime = 0
}
```
