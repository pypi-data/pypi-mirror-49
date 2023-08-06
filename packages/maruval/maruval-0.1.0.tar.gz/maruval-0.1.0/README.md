# maruval

Command line utilities for [marugoto](https://github.com/uzh/marugoto) content

> Version 0.1.0

[![Build Status](https://travis-ci.org/uzh/maruval.svg?branch=master)](https://travis-ci.org/uzh/maruval)
[![codecov.io](https://codecov.io/gh/uzh/maruval/branch/master/graph/badge.svg)](https://codecov.io/gh/uzh/maruval)
[![PyPI version](https://badge.fury.io/py/maruval.svg)](https://badge.fury.io/py/maruval)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

## Installing dependencies

*maruval* is predominantly written Python, so your machine needs Python and the Python package manager *pip* for installation. You should already have Python.

To check if you have *pip*, type `which pip3` and/or `which pip` into your command line. If either command returns a path to `pip`, you can proceed to `Installing maruval`.

To install *pip*, run the following command:

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py && rm get-pip.py
```

Now `which pip` should show a path to a *pip* executable.

If you want to use `marupretty`, the JSON pretty printer, you'll need to have the `jq` utility installed. Get it [here](https://stedolan.github.io/jq/) and save it as `jq` in `/usr/bin`


## Installing *maruval*

Once you have *Python*, *pip3*/*pip*, and maybe `jq`, run the following:

```bash
pip3 install maruval
# or, from the git repo:
git clone https://github.com/uzh/maruval && cd maruval && python.setup.py install
```

## Commands

* `maruval`: validate marugoto data
* `marufind` a utility to find folders with particular contents
* `marupretty`: pretty-print a JSON file or all files in a directory


### `maruval`: validate content

The main tool, *maruval*, checks for syntax and content errors in your JSON data. Use it on the command line like this:

```bash
maruval -f -nw <path-to-content>
```

Optional arguments:

* `-f`/`--fail-first` will stop *maruval* after first error
* `-nw`/`--no-warnings` will suppress warning messages

## Show help

```bash
maruval --help
```

### `marufind`: find particular content directories

```bash
# show directories containing both a videoComponent and textExercise file
marufind videoComponent,textExercise <path-to-content>
# show the opposite
marufind -not videoComponent,textExercise <path-to-content>
# show directories containing any of these files
marufind -any videoComponent,textExercise <path-to-content>
# show directories not containing any of these files
marufind -not -any videoComponent,textExercise <path-to-content>
# show directories containing only page, mail and dialog files
marufind -only page,mail,dialog <path-to-content>
# invert this --- directories containing more than these files
marufind -not -only page,mail,dialog <path-to-content>
```

```bash
marufind --help
```

### `marupretty`: tidy up a file or content directory

```bash
marupretty <path-to-content>
```
