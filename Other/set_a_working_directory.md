---
title: Set a Working Directory
parent: Other
has_children: false
nav_order: 1
mathjax: true ## Switch to false if this page has no equations or other math rendering.
---

# Set a Working Directory

When you want to refer to files on your computer in your code, for example to load a data file, you can usually refer to them in one of two ways:

- Using an *absolute path*, which starts from the root of the computer. On Windows it would look something like `C:/Users/Name/Documents/MyFile.csv` 
- Using a *relative path* which starts in the *working directory* and works from there. For example, if your workind directory were `C:/Users/Name/` then you could refer to that same `MyFile.csv` file using `Documents/MyFile.csv` as a relative path.

Using absolute paths is generally frowned upon because it makes it very difficult for anyone to run your code on their computer, since they won't have the same folder structure.

So, you want to use relative paths in your code. This means you need to know how to set the working directory so you know where your file searching starts from.

## Keep in Mind

- If you set a working directory *in your code*, that's basically the same as using an absolute path. Your code won't work on anyone else's computer! Setting a working directory is generally something you'll do interactively (by hand, either using a menu or some code you type directly in the console) when you start your software package.
- Once you are in a working directory, you can explore your folder structure using your filepath. As above, if your working directory is `C:/Users/Name/`, you can get to the file `MyFile.csv` in the `C:/Users/Name/Documents/` folder with `Documents/MyFile.csv`. You can also go *up* folders with `..`. You can get at `image.png` in the `Users` folder with `../image.png` Or if you want the file `C:/Users/Admin/passwords.txt` you could do `../Admin/passwords.txt`. This means you can set your working directory *once*, and reach for files anywhere you like without having to change it again. Or if you got the working directory wrong, you can get at a new one with a relative filepath! If `cd()` is your language's working-directory-setting command, you can go from `C:/Users/Name/Documents/` to `C:/Users/Name/` with `cd('..')` to go up one folder.
- Because setting the working directory is often done by hand anyway, it's common for it to be a point-and-click or menu feature in your software, even in software designed for use with text code. Some examples of this will be in the Implementations section.
- Many editors and IDEs come with *project managers*. Most project managers have you designate a folder as being that project's home. Then, when you open that project, most managers will automatically set the working directory to that home folder.
- In Windows, if you copy a filepath in, it will often use \ instead of / between folders. Many programming languages don't like this. You may have to change them manually.

## Also Consider

- [Get a list of files from a directory]({{ "/Other/get_a_list_of_files.html" | relative_url }}).

# Implementations

## Python

In Python, the `os.chdir()` function will let you change working directories.

```python?skip=true&skipReason=folder_does_not_exist
import os
os.chdir('C:/My/New/Working/Directory/')

# Or if you want to change the directory to your "Home" directory, you can use os.path.expanduser("~")
os.chdir(os.path.expanduser("~"))
```

In the Spyder IDE, the working directory is listed by default in the top-right, and you can edit it directly.

![Spyder working directory line](https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Other/Images/spyder_wd.PNG)

## R

In R, the `setwd()` function can change the working directory.

```r?skip=true&skipReason=folder_does_not_exist
setwd('C:/My/New/Working/Directory/')
```

If you are working in an R project, there is also the **here** package.

```r?skip=true&skipReason=folder_does_not_exist
library(here)
here()
```

`here()` will start in whatever your current working directory and look upwards into parent folders until it finds something that indicates that it's found a folder containing a project: an `.Rproj` (R Project) file, a `.git` or `.svn` folder, or any of the files `.here`, `.projectile`, `remake.yml`, or `DESCRIPTION`, and will set the working directory to that folder. This won't work if you haven't set up a proper project folder structure.

If you are using RStudio, there are several other ways to set the working directory. In the Session menu, you can choose to set the working directory to the Source File location (whatever folder the active code tab file is saved in), to the File Pane location (whatever folder the Files pane, in the bottom-right by default, has navigated to), or you can choose it using your standard operating system folder-picker.

![Rstudio working directory selection from Session menu](https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Other/Images/rstudio_session_wd.png)

You can also navigate to the folder you want in the Files pane (which is in the bottom-right by default) and select More $$\rightarrow$$ Set as Working Directory.

![Rstudio working directory selection from Files pane](https://github.com/LOST-STATS/lost-stats.github.io/raw/source/Other/Images/rstudio_pane_wd.PNG)

## Stata

In Stata, you can use the `cd` command to change working directories.

```stata?skip=true&skipReason=folder_does_not_exist
cd "C:/My/New/Working/Directory/"
```

You can also change the working directory in the File $$\rightarrow$$ Change Working Directory menu, which will pull up your standard operating system folder-picker.

Additionally, if you open Stata by clicking on a `.do` file saved on your computer, the working directory will automatically be set to whatever folder that `.do` file is saved in.

## Julia

In Julia, you can use the `cd()` function to change the working directory.

```julia 
cd("C:/My/New/Working/Directory/")
```

You may use the `pwd()` function to check the current working directory.

```julia
pwd()
```
