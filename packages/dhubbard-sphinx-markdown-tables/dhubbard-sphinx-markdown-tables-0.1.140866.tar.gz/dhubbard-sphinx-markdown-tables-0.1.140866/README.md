[![Build Status](https://cd.screwdriver.cd/pipelines/3023/badge)](https://cd.screwdriver.cd/pipelines/3023)
[![Code Coverage](https://codecov.io/gh/dwighthubbard/sphinx-markdown-tables/branch/master/graph/badge.svg)](https://codecov.io/gh/dwighthubbard/sphinx-markdown-tables)


Note: 

This is a fork of `sphinx-markdown-tables` package that works with newer versions of the `markdown` package.

# sphinx-markdown-tables

A [Sphinx](http://www.sphinx-doc.org/en/master/) extension for rendering markdown tables.

Sphinx supports markdown via [Recommonmark,](https://github.com/rtfd/recommonmark) which does not support tables. This
extension provides them.

It renders markdown tables as HTML, as defined by [python-markdown](https://python-markdown.github.io/)

## Installation

    pip install dhubbard-sphinx-markdown-tables

## Usage

### Quick version
Add `sphinx_markdown_tables` to `extensions` in `conf.py`, like so:

    extensions = [
        'sphinx_markdown_tables',
    ]

### Longer version
Sphinx needs to be configured to use markdown. First, you need `recommonmark`:

    pip install recommonmark

In `conf.py`, configure `source_parsers` and `source_suffix`:

    source_parsers = {
        '.md': 'recommonmark.parser.CommonMarkParser',
    }

    source_suffix = ['.rst', '.md']

Once Sphinx is configured appropriately, add `sphinx_markdown_tables` to `extensions`, like so:

    extensions = [
        'sphinx_markdown_tables',
    ]

For more information on Sphinx and markdown, see the
[Sphinx documentation.](http://www.sphinx-doc.org/en/master/usage/markdown.html)

## License
This project is available under the GPLv3 license. For other licensing arrangements contact
[Ryan Fox.](https://foxrow.com)
