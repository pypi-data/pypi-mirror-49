# astspy
astspy (Abstract Syntax Tree SPY) is an open source command line tool to
extract information from Python source code files.

astspy can be used with Python 3 and 2 code, but make sure to
analyze files from each version in their respective environments.

# Features
- Print the names of classes and functions found in the file
- Calculate an aproximation of the number of lines of code of each class
  or function definition (sizes)
- See what functions or classes have docstrings
- Print the locations of the definitions in the file (line numbers)
- Get stats from the sizes of the definitions

## Installation

You can install, upgrade, and uninstall ``astspy.py`` with these commands:

```sh
  $ pip install astspy
  $ pip install --upgrade astspy
  $ pip uninstall astspy
```

## Help

To get help use:

```sh
  $ astspy -h
```
