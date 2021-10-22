# GSQL

[![CI](https://github.com/TheSYNcoder/gsql/actions/workflows/ci.yml/badge.svg)](https://github.com/TheSYNcoder/gsql/actions/workflows/ci.yml)
[![pre-commit](https://github.com/TheSYNcoder/gsql/actions/workflows/lint.yml/badge.svg)](https://github.com/TheSYNcoder/gsql/actions/workflows/lint.yml)

You should be ashamed of yourself as a developer by using google sheets through the browser.
Use the power of GSQL to use gsheets like never before!

## Under construction 🚧🚧

## Usage 

Coming soon ...

### Development

This project uses ``black`` to format code and ``flake8`` for linting. We also support ``pre-commit`` to ensure
these have been run. To configure your local environment please install these development dependencies and set up
the commit hooks.

```bash

   $ pip install black flake8 pre-commit
   $ pre-commit install

```

Install further dependencies using

```
    $ pip install requirements.txt    
```

Before making a pull request

```
$ pre-commit run --all-files
$ pytest

```
All tests should pass
