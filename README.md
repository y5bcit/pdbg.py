# pdbg.py

## Table of Contents

- [pdbg.py](#pdbgpy)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Example](#example)
  - [Options](#options)

## Introduction

**pdbg** is a debugging tool for python. It is designed to be a simple and lightweight tool for troubleshooting errors in Python code.

When run, this tool will run the specified script, while outputting all the variable definitions during the run. This is useful for when you want to watch the changes made to variables during the execution of your code and you don't have an IDE with a debugger. This is also useful even when you *do* have a debugger, as many debuggers don't allow you to go back to previous steps in your code, making it easy to forget what the previous values were. This tool will show you all the changes at once in the command line output or in a file, meaning that forgetting what happened will never be an issue.

All of the functionality of this module is provided through a single function. The options for this function are detailed in the [Options](#options) section of this document

## Installation

You can install `pdbg` with `pip`

``` cmd
pip install pdbg-bcit
```

## Usage

Using this tool is very simple. In Windows, open CMD in the folder that you would normally run your python script. Then, enter the below command, with `$filepath` as the absolute path of the python script you want to debug.

```cmd
python -c "import pdbg; pdbg.pdbg(r'$filepath')"
```

This method will run the script and output all the variable definitions and changes in the targeted file. More options for this method are detailed in [options](#options).

## Example

Lets say we have a file with the following code.

```Python
def foo():
    bar = 0
    for i in range(3):
        bar += 1
    print(bar)

foo()
```

If we wanted to watch the variables changed in `foo()`, all we would have to do is open command line and run this command, with `$filepath` as the absolute path of the python file.

```cmd
python -c "import pdbg; pdbg.pdbg(r'$filepath', ['foo'])"
```

And this would be our output:

```text
[DebugLog] Entering function foo
[Debug]     bar = 0                                                  bar { None => 0 }
[Debug]     for i in range(3):                                       i { None => 0 }
[Debug]         bar += 1                                             bar { 0 => 1 }
[Debug]     for i in range(3):                                       i { 0 => 1 }
[Debug]         bar += 1                                             bar { 1 => 2 }
[Debug]     for i in range(3):                                       i { 1 => 2 }
[Debug]         bar += 1                                             bar { 2 => 3 }
3
```

## Options

`pdbg`.**pdbg**(file, *func_filter=[]*,  *var_filter=[]*, *output_file=None*, *seperator=", "*,*output_format="\{var_name} {{ \{pre_value} => \{new_value} }}"*)
* [Required] `file`
  * Absolute path to your Python script.
* `func_filter`
  * Filter the output by function name.
* `var_filter`
  * Filter the output by variables name.
* `output_file`
  * Defaults to None. Redirect the output of pdbg to a file if specified. Will output by printing in console otherwise
* `seperator`
  * Seperator used when multiple variables are changed in one line.
* `output_format`
  * A string that formats the output
  * `{var_name}` will be the name of the variable,
  * `{pre-value}` will be the initial variable
  * `{new_value}` will be the variable after changes.
* Read [the Python doc](https://docs.python.org/3.7/library/string.html#format-string-syntax) for more about formatting.
