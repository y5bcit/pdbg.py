import os
import sys
import bdb

class pdbg(bdb.Bdb):
    def __init__(self, file, format="{varname} {{ {prevvalue} => {newvalue} }}", seperator=", ", variable=[], outputfile=""):
        bdb.Bdb.__init__(self, skip = None)
        import __main__
        __main__.__dict__.clear()
        import builtins
        __main__.__dict__.update({"__name__" : "__main__", "__file__" : file, "__builtins__": builtins })
        with open(file, "rb") as fp:
            statement = "exec(compile(%r, %r, \"exec\"))" % (fp.read(), file) #compile(source, filename, mode) #mode can be eval, exec, single
        import sys
        import os
        sys.path[0] = os.path.dirname(file)
        self.filepath = file.lower()
        self.prevlocals = {}
        self.prevline = ""
        self.outputfile = outputfile
        self.initlocals = False
        self.format = format
        self.seperator = seperator
        self.varfilter = variable
        self.run(statement)

    def user_line(self, frame):
        filename = self.canonic(frame.f_code.co_filename)
        if not filename == self.filepath:
            return
        changedvars = {}
        tempvars = {}
        if not self.initlocals:
            self.initlocals = True # By default, variables like __main__ should be hide
        else:
            for i in [*frame.f_locals]:
                if not (i + "_")[0:2] == "__":
                    if not i in self.prevlocals:
                        changedvars[i] = frame.f_locals[i]
                    elif self.prevlocals[i] != frame.f_locals[i]:
                        changedvars[i] = frame.f_locals[i]
        if "self" in changedvars and "cmd" in changedvars and "globals" in changedvars and "locals" in changedvars:
            changedvars = {}
        if len(self.prevline) > 0:
            tempvars = self._filter(changedvars)
            tobeprint = []
            if len(tempvars) > 0:
                formattedResult = []
                for i in [*tempvars]:
                    formattedResult.append(self.format.format(varname = i,
                                                              prevvalue = self.prevlocals[i] if i in self.prevlocals else None,
                                                              newvalue = str(tempvars[i])))
                tobeprint = ["[Debug]", self.prevline, " " * (40 - len(self.prevline)), self.seperator.join(formattedResult)]
            else:
                tobeprint = ["[Debug]", self.prevline]
            if len(self.outputfile) > 0:
                with open(self.outputfile, "a") as o:
                    o.write(" ".join(tobeprint))
                    o.write("\n")
            else:
                print(*tobeprint)
        self.prevlocals = frame.f_locals.copy() # copy a dict
        if filename[0] != "<":
            self.prevline = open(filename).readlines()[frame.f_lineno - 1].rstrip()

    def _filter(self, variables):
        if len(self.varfilter) == 0:
            return variables
        ret = {}
        for key in [*variables]:
            if key in self.varfilter:
                ret[key] = variables[key]
        return ret