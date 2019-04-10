# pdbg.py
A Python debugger for learner which print out all changes.


### Usage

```python
import pdbg

pdbg.pdbg("/path/to/your/script")
```

### Options
`pdbg`.**pdbg**(file, *format="\{varname} {{ \{prevvalue} => \{newvalue} }}"*, *seperator=", "*, *variable=[]*, *outputfile=""*)
* [Required] `file`
  * Path to your script.
* `format`
  * The format of each changed variables. Read [the Python doc](https://docs.python.org/3.7/library/string.html#format-string-syntax) for more about formatting.
* `seperator`
  * Seperator used when multiple variables changed in one line.
* `variable`
  * Filter the output by variables name.
* `outputfile`
  * Redirect the output of pdbg to a file.