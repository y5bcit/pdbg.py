import os
import sys
import bdb

class pdbg(bdb.Bdb):
    def __init__(self, file, key='variable',value='value',seperator="-",variable=[]):
        bdb.Bdb.__init__(self, skip = None)
        import __main__
        __main__.__dict__.clear()
        import builtins
        __main__.__dict__.update({"__name__" : "__main__", "__file__" : file, "__builtins__": builtins })
        with open(file, "rb") as fp:
            statement = "exec(compile(%r, %r, 'exec'))" % (fp.read(), file) #compile(source, filename, mode) #mode can be eval, exec, single
        import sys
        import os
        sys.path[0] = os.path.dirname(file)
        self.prevlocals = {}
        self.prevline = ""
        self.initlocals = False
        self.seperator = seperator
        self.key = key
        self.value = value
        self.variable=variable
        self.run(statement) #run

    def user_line(self, frame):
        filename = self.canonic(frame.f_code.co_filename)
        changedvars = {}
        tempvars = {}
        if not self.initlocals:
            self.initlocals = True # By default, variables like __main__ should be hide
        else:
            for i in [*frame.f_locals]: # same as frame.f_locals.keys()
                if not (i + "_")[0:2] == "__":
                    if not i in self.prevlocals:
                        changedvars[i] = frame.f_locals[i]
                    elif self.prevlocals[i] != frame.f_locals[i]:
                        changedvars[i] = frame.f_locals[i]
        if "self" in changedvars and "cmd" in changedvars and "globals" in changedvars and "locals" in changedvars:
            changedvars = {}
        if len(self.prevline) > 0:
            hasVar = True
            for key in changedvars.keys():
                if(key in self.variable) or len(self.variable) == 0:
                    print("[Debug]", self.prevline, " " * (40 - len(self.prevline)), (self.key +" "+  key +" " + self.seperator +" " + self.value+" "+str(changedvars[key])))
                    hasVar = False
                elif(hasVar):
                    print("[Debug]", self.prevline)
        for key in tempvars.keys():
            print("[Debug]", self.prevline, " " * (40 - len(self.prevline)), (self.key +" "+  key +" " + self.seperator +" " + self.value+" "+tempvars[key]))
        self.prevlocals = frame.f_locals.copy() # copy a dict
        if filename[0] != "<":
            self.prevline = open(filename).readlines()[frame.f_lineno - 1].rstrip()
