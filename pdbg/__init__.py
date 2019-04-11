import os
import sys
import bdb

class pdbg(bdb.Bdb):
    def __init__(self, file, output_format="{var_name} {{ {pre_value} => {new_value} }}", seperator=", ", var_filter=[], func_filter=[], output_file=""):
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
        self.code_source = open(file).readlines()
        self.prevlocals = {}
        self.prevline = ""
        self.output_file = output_file
        self.initlocals = False
        self.output_format = output_format
        self.seperator = seperator
        self.var_filter = var_filter
        self.func_filter = func_filter
        self.run(statement)

    def user_line(self, frame):
        filename = self.canonic(frame.f_code.co_filename)
        if not filename == self.filepath:
            return
        if not frame.f_code.co_name in self.func_filter and len(self.func_filter) > 0:
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
                    formattedResult.append(self.output_format.format(var_name = i,
                                                                     pre_value = self.prevlocals[i] if i in self.prevlocals else None,
                                                                     new_value = str(tempvars[i])))
                #tobeprint = ["[Debug]", self.prevline, " " * (40 - len(self.prevline)), self.seperator.join(formattedResult)]
                tobeprint = ["[Debug]", '{:40}'.format( self.prevline),self.seperator.join(formattedResult)]
            else:
                tobeprint = ["[Debug]", self.prevline]
            if len(self.output_file) > 0:
                with open(self.output_file, "a") as o:
                    o.write(" ".join(tobeprint))
                    o.write("\n")
            else:
                print(*tobeprint)
        self.prevlocals = frame.f_locals.copy() # copy a dict
        if filename[0] != "<":
            self.prevline = self.code_source[frame.f_lineno - 1].rstrip()
            

    def _filter(self, variables):
        if len(self.var_filter) == 0:
            return variables
        ret = {}
        for key in [*variables]:
            if key in self.var_filter:
                ret[key] = variables[key]
        return ret