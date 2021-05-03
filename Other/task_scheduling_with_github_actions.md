---
title: Task Scheduling with Github Actions
parent: Other
has_children: false
nav_order: 1
---

Typically when performing statistical analyses, we write code to be run approximately once. But software more generally is frequently run multiple times. Web servers run constantly, executing the same code over and over in response to user commands. A video game is rerun on demand, each time you turn it on.

In statistical analyses, though, if code is to be run multiple times, it often needs to be run _on a schedule_. For instance, you may want to scrape weather data every hour to build an archive for later analysis. Or perhaps you want to perform the _same_ statistical analyses each week on new data as it comes in. In our experience, this is the worst kind of tasks for humans to do: They have to reliably remember to run a piece of code at a specified time, aggregate the results in a consistent format, and then walk away. One mistimed meeting or baby feeding and it's likely the reseaercher will forget to hit "go."

Thankfully, in addition to doing things over and over or on demand, computers are also reasonably good at keeping time. In this article, we'll describe the role of a _task scheduler_ and demonstrate how to use [Github Actions](https://github.com/features/actions) to run a simple data gathering task at regular intervals and commit that data to a repository.

## The Problem We'll Solve

The United States [Substance Abuse and Mental Health Services Administration (SAMHSA)](https://www.samhsa.gov/) is an agency inside the U.S. Department of Health and Human Services tasked with overseeing the country's substance abuse and mental health initiatives. A major one of these initiatives is maintaining the list of "waived providers" who can prescribe opioids, something that is typically prohibited under the federal Controlled Substances Act.

SAMHSA makes available a list of _currently_ waived providers, but does _not_ publish (at least easily) historical lists of providers. As such, we'll write a small web scraper that pulls all the data from their website and writes it out to a CSV.

This article, however, is not about web scrapers. Instead, our problem is that SAMHSA seems to update the list without fanfare at irregular intervals. So we would like to scrape their website _every day_. This article demonstrates how set up a Github repo to do just that.

## Requirements

You'll need:
  1. A [Github](https://www.github.com/) account and some familiarity with git
  2. A program that can be run on the command line that accomplishes your data gathering task
  3. The _requirements_ for that program enumerated in one of several standard ways

For the rest of this section, we'll focus a bit on requirements (2) and (3).

### Requirement (2): A command line program

What you'll be able to tell Github to do is run a series of commands. It is best to package these up into one command that will do everything for you.

For instance, if you're using `python`, you will probably want to have a file called `main.py` that looks something like this:

```python
import csv
import sys
from datetime import datetime
from typing import List, Union

import requests

URL = "https://whereveryourdatais.com/"

def process_page(html: str) -> List[List[Union[int, str]]]:
    """
    This is the meat of your web scraper:
    Pulling out the data you want from the HTML of the web page
    """


def pull_data(url: str) -> List[List[Union[int, str]]]:
    resp = requests.get(url)
    resp.raise_for_status()

    content = resp.content.decode('utf8')
    return process_page(content)


def main():
    # The program takes 1 optional argument: an output filename. If not present,
    # we will write the output a default filename, which is:
    filename = f"data/output-{datetime.utcnow().strftime('%Y-%m-%d').csv"
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    print(f"Will write data to {filename}")

    print(f"Pulling data from {URL}...")
    data = pull_data(URL)
    print(f"Done pulling data.")

    print("Writing data...")
    with open(filename, 'wt') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(data)
    print("Done writing data.")


if __name__ == "__main__":
    main()
```

Here the meat of your web scraper goes into the `pull_data` and the `process_page` functions. These are then wrapped into the `main` function which you can call on the command line as:

```bash
python3 main.py
```

Similarly, if you're using `R`, you'll want to create a `main.R` file to similar effect. For instance, it might look something like:

```R
library(readr)
library(httr)

URL <- "https://whereveryourdatais.com/"

#' This hte meat of your web scraper:
#' Pulling out the data you want from the HTML of the web page
process_page <- function(html) {
    # Process html
}

#' Pull data from a single URL and return a tibble with it nice and ordered
pull_data <- function(url) {
    resp <- GET(url)
    if (resp$status_code >= 400) {
        stop(paste0("Something bad occurred in trying to pull ", URL))
    }

    return(process_page(content(resp)))
}

main <- function() {
    # The program takes 1 optional argument: an output filename. If not present,
    # we will write the output a default filename, which is:
    date <- Sys.time()
    attr(date, "tzone") <- "UTC"
    filename <- paste0("data/output-", as.Date(date, format = "%Y-%m-%d"))

    args <- commandArgs(trailingOnly = TRUE)
    if (length(args) > 0) {
        filename <- args[1]
    }

    print(paste0("Will write data to ", filename))

    print(paste0("Pulling data from ", URL))
    data <- pull_data(URL)
    print("Done pulling data")

    print("Writing data...")
    write_csv(data, filename)
    print("Done writing data.")
}
```

Here the meat of your web scraper goes into the `pull_data` and the `process_page` functions. These are then wrapped into the `main` function which you can call on the command line as (note the `--vanilla`):

```
Rscript --vanilla main.R
```

### Requirement (3): Enumerated lists of requirements

In order for Github to run your command, it will need to know what _dependencies_ it needs to install. For experts, using a tool like [poetry](https://python-poetry.org/) in Python or [renv](https://rstudio.github.io/renv/articles/renv.html) in R is probably what you actually want to do. However, for the purposes of this article, we'll stick to a simple list.

As such, you should create a file entitled `requirements.txt` in your project's main folder. In this you should list, one requirement per line, the requirements of your script. For instance, in the python example above, your `requirements.txt` should look like

```
requests
```

The `R` example should have

```
httr
readr
```

If you're using `R`, you'll also need to add the following script in a file called `install.R` to your project:

```R
CRAN <- "https://mirror.las.iastate.edu/CRAN/"

process_file <- function(filepath) {
  con <- file(filepath, "r")
  while (TRUE) {
    line <- trimws(readLines(con, n = 1))
    if (length(line) == 0) {
      break
    }
    install.packages(line, repos = CRAN)
  }

  close(con)
}

process_file("requirements.txt")
```

## Setting up the Action

With all of the above accomplished, you should have a `main.py` or a `main.R` file and a `requirements.txt` file setup in your repository. If you're using `R`, you'll also have an `install.R` script present. With that, we move to setting up the Github Action!

In this section, we assume that your repository is already on Github. Throughout, we'll assume that the repository is hosted at `USERNAME/REPO`, e.g., `lost-stats/lost-stats.github.io`.

### Telling it to run

Now you just need to add a file called `.github/workflows/schedule.yml` to your repo. Its contents should look like this:

```yaml
name: Run scheduled action
on:
  schedule:
    # You need to set your schedule here
    - cron: CRON_SCHEDULE

jobs:
  pull_data:
    runs-on: ubuntu-20.04
    steps:
      - name: Checkout code
        uses: actions/checkout@v2
        with:
          persist-credentials: false
          fetch-depth: 0

      # If using Python:
      - name: Set up Python 3.8
        uses: actions/setup-python@v2
        with:
          python-version: "3.8"

      # If using R:
      - name: Set up R 4.0.3
        uses: r-lib/actions/setup-r@v1
        with:
          r-version: "4.0.3"

      # If using Python:
      - name: Install dependencies
        run: pip install -r requirements.txt

      # If using R:
      - name: Install dependencies
        run: Rscript --vanilla install.R

      # If using Python:
      - name: Pull data
        run: python3 main.py

      # If using R:
      - name: Pull data
        run: Rscript --vanilla main.R

      # NOTE: This commits everything in the `data` directory. Make sure this matches your needs
      - name: Git commit
        run: |
          git add data
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git commit -m "Commiting data"

      # NOTE: Check that your branch name is correct here
      - name: Git push
        run: |
          git push "https://${GITHUB_ACTOR}:${TOKEN}@github.com/${GITHUB_REPOSITORY}.git" HEAD:main
        env:
          TOKEN: {% raw %}${{ secrets.GITHUB_TOKEN }}{% endraw %}
```

You'll need to edit this file and retain only the stanzas that pertain to whether you're using Python or R. However, you'll need to make a few adjustments. Let's go through the file stanza by stanza to explain what it is doing:

### name: Run scheduled action

This is just a descriptive name. Everything after the `:` is decorative. Name it whatever you like!

### on:

This section describes when the action should run. Github actions supports several potential events, including `push`, `pull_request`, and `repository_dispatch`. However, since this is a scheduled action, we're going to use the `schedule` event.

The next line `- cron: CRON_SCHEDULE` tells Github how frequently to run the action. You need to replace `CRON_SCHEDULE` with your preferred frequency. You need to write this in "[cron](https://en.wikipedia.org/wiki/Cron) syntax," which is an arcane but pretty universally recognized format for specifying event schedules. I recommend using a helper like [this one](https://cron.help/) to write this expression.

For instance, let's say we want to run this job at noon UTC every day. Then this line should become `- cron: "0 12 * * *"`.

### jobs:

This tells us that we're about to begin specifying the list of jobs to be run on the schedule described above.

### pull_data:

This is also just a descriptive name. It is best that it follow `snake_casing`, in particular, it should have no spaces or strange characters.

### runs-on: ubuntu-20.04

This specifies which operating system to run your code on. Github supports a lot of choices, but generally, `ubuntu-20.04` or `ubuntu-latest` is what you'll want.

### steps:

In what follows, we list out the individual steps Github should take. Each step consists of several components:
  * `name:` A descriptive name. Can be anything you'd like. It's also optional, but I find it useful.
  * `uses:` Optionally reference an series of steps somebody else has already specified.
  * `with:` If using `uses:`, specificy any variables in calling that action.
  * `run:` Just simply run a (series of) commands in the shell, one per line.
  * `env:` Specify envrionment variables for use in the shell.

We'll see several examples of this below.

### Checkout code

This stanza tells the action to checkout this repository's code. This will begin basically every Github action you build. Note that it `uses:` a standard action that is maintained by Github itself.

### Setup Python or R

These are actions that tell Github to make a specific version of Python or R available in your envrionment. You probably only need one, but you can use both if you need. Specify the exact version you want in the `with:` section.

### Install dependencies

This runs a script that installs all the dependencies you enumerated earlier in `requirements.txt`. Python comes with a built in dependency manager called `pip`, so we just point it to our list of dependencies. On the other hand, we tell `R` to execute our dependency installation script `install.R`.

In either case, we're using `run:` as we're telling Github to execute a command in its own shell.

### Pull data

This is the task we're actually going to run! Note that we're calling either the `main.py` or `main.R` file we built before. After this is done, we assume there will be a new file in the `data/` directory.

### Git commit

This stanza commits the new data to this repository and sets up the required git variables. Note that here we're using `run: |`. In YAML, ending a line with `|` indicates that all the following lines that are at the same tab depth should be used as a single value. So here, we're telling Github to run the commands, `git add data`, `git config --local user.email "action@github.com"`, etc in order.

### Git push

This pushes the commit back up to the repository using `git push`.

Note that if the name of your main branch is not `main` (for instance, it may be `master`), you will need to change `HEAD:main` to whatever your main branch is called (e.g., `HEAD:master`).

Also note that we are setting an environment variable here. Specfically, in the `env:` section we're setting the `TOKEN` environment variable to `{% raw %}${{ secrets.GITHUB_TOKEN }}{% endraw %}`. This is a a special value that Github generates for each run of your action that allows your action to manipulate its own repository. In this case, it's allowing it to push a commit back to the central repository.

## And that's all!

And that's it! With that file commited, you Github action should run every day at noon UTC.

From here, there are a lot of simple extensions to be made and tried. Here are some challenges to make sure you know what's going on above:
  * Instead making the job run every day at noon UTC, make it run on Wednesdays at 4pm UTC.
  * Instead of returning at `tibble`, return a `data.frame` in R. Note that you'll need to expand the collection of requirements!
  * Instead of returning a list of lists in Python, return a pandas data frame. Note that you'll need to expand the collection of requirements!

## One final note: API keys

A very common need to pull data is some sort of API key. Your cron job will need access to your API key. Conveniently, Github has provided a nice functionality to do exactly this: [Secrets](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets).

To get your API key to your script, follow these steps:
  1. Setup your secret according to the above instructions. Let's give it the name `API_KEY` for convenience.
  2. Modify your `main.py` or `main.R` file to look for the `API_KEY` environemnt variable. For instance, in Python you might do:

```python
import os

api_key = os.environ.get("API_KEY", some_other_way)
```

or in R you might do

```R
api_key <- Sys.getenv("API_KEY", unset = some_other_way)
```

  3. Amend the `Pull data` step in your action to set the `API_KEY` environment variable. For instance, it might look like:

```yaml
- name: Pull data
  run: python3 main.py
  env:
    API_KEY: {% raw %}${{ secrets.API_KEY }}{% endraw %}
```