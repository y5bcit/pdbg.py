# pdbg.py
A Python debugger for learner which print out all changes.


### Usage

```python
import pdbg

pdbg.pdbg("/absolute/path/to/your/script")
```

### Options
`pdbg`.**pdbg**(file, *output_format="\{var_name} {{ \{pre_value} => \{new_value} }}"*, *seperator=", "*, *var_filter=[]*, *func_filter=[]*, *output_file=""*)
* [Required] `file`
  * Path to your script.
* `output_format`
  * The format of each changed variables. 
  * Use `{var_name}` `{pre_value}` `{new_value}` for variables.
  * Read [the Python doc](https://docs.python.org/3.7/library/string.html#format-string-syntax) for more about formatting.
* `seperator`
  * Seperator used when multiple variables changed in one line.
* `var_filter`
  * Filter the output by variables name.
* `func_filter`
  * Filter the output by function name.
* `output_file`
  * Redirect the output of pdbg to a file.