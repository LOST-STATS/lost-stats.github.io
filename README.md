# LOST

This is the official repo for **Library of Statistical Techniques** (LOST) website: https://lost-stats.github.io/

LOST is a publicly-editable website with the goal of making it easy to execute statistical techniques in statistical software.

## Building locally

If you are interested in local development, we use ruby 2.6.4. From there, you can run

```bash
bundle install
bundle exec jekyll serve
```

If you'd like to check for broken links, you can run

```bash
bundle exec jekyll build
bundle exec htmlproofer --assume-extension --allow-hash-href ./_site
```

## Linting code samples

In order to keep our formatting consistent, we try to format all of our code using [`black`](https://github.com/psf/black) for Python code and [`styler`](https://github.com/r-lib/styler) for R code. In order to run our automated linters, you will need R, Python 3.8+, and [Poetry](https://python-poetry.org/docs/#installation). Then you will need to run:

```bash
R -e 'install.packages("styler")'
poetry install
```

Once this is completed, then you should be able to run

```bash
poetry run lostutils style .
```

or you can specify specific directories or files a la

```bash
poetry run lostutils style Other Presentation/Figures/bar_graphs.md --skip Other/create_a_conda_package.md
```

## Testing code samples

We have some facilities for testing to make sure that all the code samples in this repository work, at least fo the open source languages. You will need a few extra requirements for this section.

*CAVEAT EMPTOR* The following commands run arbitrary code samples on your machine from this repository. They _are_ run inside isolated docker containers, but currently those containers have no ulimits. Thus, it is possible that they could, e.g., download giant files and cause your machine to come to a crawl.

### Requirements

You will first need to install [Docker](https://docs.docker.com/desktop/). You will also need Python 3.8 or above as well as [Poetry](https://python-poetry.org/docs/#installation). After this, you will need to run the following commands:

```bash
poetry install

docker pull ghcr.io/khwilson/lost-docker-images/tester-r
docker pull ghcr.io/khwilson/lost-docker-images/tester-python
```

At this point, the docker images will _not_ be updated unless you explicitly repull them.

### Running tests

After completing the setup, you can simply run

```
poetry run py.test tests
```

Note that this will take a _long_ time to run. You can reduce the set of tests run using the `--mdpath` option. For instance, to find and run all the code samples in the `Time_Series` and `Presentation` folders, you can run

```
py.test tests --mdpath Time_Series --mdpath Presentation
```

Furthermore, you can run tests in parallel by adding the `-n` parameter:

```
py.test tests -n 3 --mdpath Time_Series
```

### Adding dependencies

The docker images in which these tests are run are managed in the [lost-docker-images](https://github.com/khwilson/lost-docker-images) repo. See instructions there for adding dependencies. After which, you will need to refresh your docker images with:

```
docker pull ghcr.io/khwilson/lost-docker-images/tester-r
docker pull ghcr.io/khwilson/lost-docker-images/tester-python
```

### Connecting code samples

Note that a lot of code samples in this repository are broken up by raw markdown text. If you would like to connect these in a single runtime, you should specify the language as `language?example=some_id` for each code sample in the chain. For instance, a Python example might be specified as `python?example=seaborn` as you can see in the [Line Graphs Example](https://github.com/LOST-STATS/lost-stats.github.io/blob/source/Presentation/Figures/line_graphs.md).
