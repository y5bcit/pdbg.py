# pdbg.py

## Table of Contents

- [pdbg.py](#pdbgpy)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Options](#options)

**pdbg** is a debugging tool for python. It is designed to be a simple and lightweight tool for troubleshooting errors in Python code.

When run, this tool will run the specified script, while outputting all the variable definitions during the run.

All of the functionality of this module is provided through a single function. The options for this function are detailed in the [Options](#options) section of this document

## Installation

You can install `pdbg` with `pip`

``` cmd
pip install pdbg-bcit
```

## Usage

Using this tool is very simple. Just open python and import the library and you'll be ready to get started.

```python
import pdbg

pdbg.pdbg(file)
```

Running the `pdbg.pdbg()` method will run the script and output all the variable definitions and changes in the targeted file. More options for this method are detailed below.

## Options

`pdbg`.**pdbg**(file, *output_format="\{var_name} {{ \{pre_value} => \{new_value} }}"*, *seperator=", "*, *var_filter=[]*, *func_filter=[]*, *output_file=""*)
* [Required] `file`
  * Absolute path to your Python script.
* `output_format`
  * The format of the output
  * {var_name} will be the name of the variable,
  * {pre-value} will be the initial variable
  * {new_value} will be the variable after changes.
  * Read [the Python doc](https://docs.python.org/3.7/library/string.html#format-string-syntax) for more about formatting.
* `seperator`
  * Seperator used when multiple variables are changed in one line.
* `var_filter`
  * Filter the output by variables name.
* `func_filter`
  * Filter the output by function name.
* `output_file`
  * Defaults to None. Redirect the output of pdbg to a file if specified. Will output by printing in console otherwise
