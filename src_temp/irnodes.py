from definitions import TokenType, types_str, BinOpKind, Token

class Statement(): pass
class Expr(): pass
class Term(Expr): pass

class NIntlit(Term):
    def __init__(self, val: int):
        self.val = val

class NIdent(Term):
    def __init__(self, tok: Token):
        self.tok = tok

class NDecl(Statement):
    def __init__(self, vid: NIdent, val: Expr):
        self.varid = vid
        self.val = val

class NPrint(Statement):
    def __init__(self, expr: Expr):
        self.expr = expr
    
class NRead(Statement):
    def __init__(self, ident: NIdent):
        self.ident = ident

class NAssign(Statement):
    def __init__(self, vid: NIdent, val: Expr):
        self.varid = vid
        self.val = val

class NBinExpr(Expr):
    def __init__(self, op: BinOpKind, lhs: Expr, rhs: Expr):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
class NScope(Statement):
    def __init__(self, statements: list[Statement]):
        self.stmts = statements

class ErrorExpect():
    def __init__(self, exp_type: TokenType, got_typ: TokenType, loc: tuple[int, int]):
        if isinstance(exp_type, list):
            self.msg = f"[Error] at {loc} : Expected {' or '.join(types_str[i] for i in exp_type)} but found {types_str[got_typ]}"
        else:
            self.msg = f"[Error] at {loc} : Expected {types_str[exp_type]} but found {types_str[got_typ]}"

    def report(self):
        print(self.msg)
        exit(1)





