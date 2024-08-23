from irnodes import *

class Generator():
    def __init__(self, statements: list[Statement]):
        self.statements = statements
        self.bfcode = ''
        self.headp = 0
    
    def gen_moveto(self, toaddr: int):
        steps = toaddr-self.headp
        if steps > 0:
            self.bfcode += '>'*steps
        else:
            self.bfcode += '<'*(-steps)
        self.headp += steps
        

    def generate_bf(self) -> str:
        bfvars = {}
        vsp = 0
        for stmt in self.statements:
            if isinstance(stmt, NDecl):
                '''DECLARE'''
                bfvars.update({stmt.varname: vsp})
                self.gen_moveto(vsp)
                self.bfcode += '[-]' + '+'*stmt.val
                vsp += 1

            elif isinstance(stmt, NAssign):
                '''ASSIGN'''
                self.gen_moveto(bfvars[stmt.varname])
                self.bfcode += '[-]' + '+'*stmt.val

        return self.bfcode