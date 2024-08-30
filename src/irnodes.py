from definitions import TokenType, types_str, BinOpKind

class Statement(): pass
class Expr(): pass
class Term(Expr): pass

class NIntlit(Term):
    def __init__(self, val: int):
        self.val = val

class NIdent(Term):
    def __init__(self, name: str):
        self.name = name

class NDecl(Statement):
    def __init__(self, vid: NIdent, val: Expr):
        self.varid = vid
        self.val = val

class NAssign(Statement):
    def __init__(self, vid: NIdent, val: Expr):
        self.varid = vid
        self.val = val

class NBinExpr(Expr):
    def __init__(self,op: BinOpKind, lhs: Expr, rhs: Expr):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

class ErrorExpect():
    def __init__(self, exp_type: TokenType, got_typ: TokenType, loc: tuple[int, int]):
        self.msg = f"[Error]: Expected {types_str[exp_type]} but found {types_str[got_typ]} at {loc}"

    def report(self):
        print(self.msg)
        exit(1)




