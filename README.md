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

## Testing code samples

We have some facilities for testing to make sure that all the code samples in this repository work, at least fo the open source languages. You will need a few extra requirements for this section.

*CAVEAT EMPTOR* The following commands run arbitrary code samples on your machine from this repository. They _are_ run inside isolated docker containers, but currently those containers have no ulimits. Thus, it is possible that they could, e.g., download giant files and cause your machine to come to a crawl.

### Requirements

You will first need to install [Docker](https://docs.docker.com/desktop/). You will also need Python 3.8 or above. After this, you will need to run the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip install 'mistune==2.0.0rc1' 'py.test==6.1.1' 'pytest-xdist==2.1.0'

docker pull ghcr.io/lost-stats/lost-docker-images/tester-r
docker pull ghcr.io/lost-stats/lost-docker-images/tester-python
```

At this point, the docker images will _not_ be updated unless you explicitly repull them.

### Running tests

After completing the setup, you can simply run

```
source venv/bin/activate
py.test test_samples.py
```

Note that this will take a _long_ time to run. You can reduce the set of tests run using the `--mdpath` option. For instance, to find and run all the code samples in the `Time_Series` and `Presentation` folders, you can run

```
py.test test_samples.py --mdpath Time_Series --mdpath Presentation
```

Furthermore, you can run tests in parallel by adding the `-n` parameter:

```
py.test test_samples.py -n 3 --mdpath Time_Series
```

### Adding dependencies

The docker images in which these tests are run are managed in the [lost-docker-images](https://github.com/lost-stats/lost-docker-images) repo. See instructions there for adding dependencies. After which, you will need to refresh your docker images with:

```
docker pull ghcr.io/lost-stats/lost-docker-images/tester-r
docker pull ghcr.io/lost-stats/lost-docker-images/tester-python
```

### Connecting code samples

Note that a lot of code samples in this repository are broken up by raw markdown text. If you would like to connect these in a single runtime, you should specify the language as `language?example=some_id` for each code sample in the chain. For instance, a Python example might be specified as `python?example=seaborn` as you can see in the [Line Graphs Example](https://github.com/LOST-STATS/lost-stats.github.io/blob/source/Presentation/Figures/line_graphs.md).