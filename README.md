# GSQL

[![CI](https://github.com/TheSYNcoder/gsql/actions/workflows/ci.yml/badge.svg)](https://github.com/TheSYNcoder/gsql/actions/workflows/ci.yml)
[![lint](https://github.com/TheSYNcoder/gsql/actions/workflows/lint.yml/badge.svg)](https://github.com/TheSYNcoder/gsql/actions/workflows/lint.yml)
[![codecov](https://codecov.io/gh/TheSYNcoder/gsql/branch/master/graph/badge.svg?token=9WOA87MKT0)](https://codecov.io/gh/TheSYNcoder/gsql)

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

Any change in the version is done through git

```
    $ git tag 1.0.1
```
