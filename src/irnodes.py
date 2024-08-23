class Statement(): pass

class NDecl(Statement):

    def __init__(self, name, val):
        self.varname = name
        self.val = val

class NAssign(Statement):
    def __init__(self, name, val):
        self.varname = name
        self.val = val
