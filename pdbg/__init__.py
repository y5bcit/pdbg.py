import os
import sys
import bdb


class pdbg(bdb.Bdb):
    def __init__(self, file: str, func_filter=[], var_filter=[], output_file=None, separator=", ", output_format="{var_name} {{ {pre_value} => {new_value} }}"):
        """Constructor for pdbg class. Parameters are used for choosing file and controlling output

        Args:
            file (str): Absolute path to a Python script.
            output_format (str, optional): Defaults to "{var_name} {{ {pre_value} => {new_value} }}". A string that formats the output.
                - {var_name} will be the name of the variable,
                - {pre-value} will be the initial variable
                - {new_value} will be the variable after changes.
            separator (str, optional): Defaults to ", ". Separator used when multiple variables are changed in one line.
            var_filter (list, optional): Defaults to []. Filter the output by variables name.
            func_filter (list, optional): Defaults to []. Filter the output by function name.
            output_file (str, optional): Defaults to None. Redirect the output of pdbg to a file if specified. Will output by printing in console otherwise.
        """

        bdb.Bdb.__init__(self, skip=None)
        import __main__
        __main__.__dict__.clear()
        import builtins
        __main__.__dict__.update(
            {"__name__": "__main__", "__file__": file, "__builtins__": builtins})
        with open(file, "rb") as fp:
            # compile(source, filename, mode) #mode can be eval, exec, single
            statement = "exec(compile(%r, %r, \"exec\"))" % (fp.read(), file)
        import sys
        import os
        file = os.path.abspath(file)
        self.scriptcwd = os.getcwd()
        sys.path[0] = os.path.dirname(file)
        os.chdir(sys.path[0])
        self.filepath = file.lower()
        self.code_source = open(file).readlines()
        self.prevlocals = {}
        self.prevline = ""
        self.initlocals = False
        self.last_frame = None
        self.func_filter = [func_filter] if isinstance(func_filter, str) else func_filter
        self.var_filter = [var_filter] if isinstance(var_filter, str) else var_filter
        self.output_file = output_file
        self.separator = separator
        self.output_format = output_format
        self.run(statement)

    def user_line(self, frame):
        filename = os.path.normcase(os.path.normpath(os.path.join(self.scriptcwd, frame.f_code.co_filename))).lower()
        if not filename == self.filepath:
            return
        curframe = self.get_stack(frame, None)[1]
        if self.last_frame is None:
            self.last_frame = curframe
        if not self.last_frame == curframe:
            self.last_frame = curframe
            if frame.f_code.co_name in self.func_filter or len(self.func_filter) == 0:
                if self.output_file:
                    with open(self.output_file, "a") as o:
                        o.write("[Function] Entering function " + frame.f_code.co_name)
                        o.write("\n")
                else:
                    print("[Function] Entering function", frame.f_code.co_name)
        if frame.f_code.co_name not in self.func_filter and len(self.func_filter) > 0:
            return
        changedvars = {}
        tempvars = {}
        if not self.initlocals:
            self.initlocals = True  # By default, variables like __main__ should be hide
        else:
            for i in [*frame.f_locals]:
                if not (i + "_")[0:2] == "__":
                    if i not in self.prevlocals:
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
                    formattedResult.append(self.output_format.format(var_name=i,
                                                                     pre_value=self.prevlocals[
                                                                         i] if i in self.prevlocals else None,
                                                                     new_value=str(tempvars[i])))
                # tobeprint = ["[Debug]", self.prevline, " " * (40 - len(self.prevline)), self.separator.join(formattedResult)]
                tobeprint = ["[Debug]", '{:60}'.format(
                    self.prevline), self.separator.join(formattedResult)]
            # else:
            #     tobeprint = ["[Debug]", self.prevline]
            if self.output_file:
                with open(self.output_file, "a") as o:

                    o.write(" ".join(tobeprint))
                    o.write("\n")
            else:
                if (tobeprint):
                    print(*tobeprint)
        self.prevlocals = frame.f_locals.copy()  # copy a dict
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
