import os
import sys
import bdb

class pdbg(bdb.Bdb):
    def __init__(self, file):
        bdb.Bdb.__init__(self, skip = None)
        import __main__
        __main__.__dict__.clear()
        import builtins
        __main__.__dict__.update({"__name__" : "__main__", "__file__" : file, "__builtins__": builtins })
        with open(file, "rb") as fp:
            statement = "exec(compile(%r, %r, 'exec'))" % (fp.read(), file)
        import sys
        import os
        sys.path[0] = os.path.dirname(file)
        self.prevlocals = {}
        self.prevline = ""
        self.initlocals = False
        self.run(statement)

    def user_line(self, frame):
        filename = self.canonic(frame.f_code.co_filename)
        changedvars = {}
        if not self.initlocals:
            self.initlocals = True
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
            print("[Debug]", self.prevline, " " * (40 - len(self.prevline)), ("# " + str(changedvars)) if len(changedvars) > 0 else "")
        self.prevlocals = frame.f_locals.copy() # copy a dict
        if filename[0] != "<":
            self.prevline = open(filename).readlines()[frame.f_lineno - 1].rstrip()
