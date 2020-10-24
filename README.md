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