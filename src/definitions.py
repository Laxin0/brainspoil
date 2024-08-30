from enum import Enum

enumc = 0
def auto(start_with_zero = False):
    global enumc
    if start_with_zero:
        enumc = 0
    t = enumc
    enumc += 1
    return t

class BinOpKind(Enum):
    ADD = auto(),
    SUB = auto(),
    MULT = auto(),
    DIV = auto()

str_to_binopkind = {
    '+': BinOpKind.ADD,
    '-': BinOpKind.SUB,
    '*': BinOpKind.MULT,
    '/': BinOpKind.DIV
}

binop_precs = {
    BinOpKind.ADD: 1,
    BinOpKind.SUB: 1,
    BinOpKind.MULT: 2,
    BinOpKind.DIV: 2
}

class TokenType(Enum):
    IDENT = auto(),
    SEMI = auto(),
    EOF = auto(),

    ASSIGN = auto(),
    BINOP = auto(),

    PAR_CL = auto(),
    PAR_OP = auto(),

    INTLIT = auto(),

    KW_LET = auto()

types_str = {TokenType.IDENT: 'variable name',
             TokenType.SEMI: '`;`',
             TokenType.EOF: 'end of file',
             TokenType.ASSIGN: '=',
             TokenType.INTLIT: 'int literal',
             TokenType.PAR_OP: '`(`',
             TokenType.PAR_CL: '`)`',
             
             TokenType.BINOP: '`+`, `-`, `*` or `/`',
             TokenType.KW_LET: '`let` keyword'}

keywords = {'let': TokenType.KW_LET}

class Token():
    def __init__(self, ttype: TokenType, val: int|None|BinOpKind, loc: tuple[int, int]):
        self.ttype = ttype
        self.val = val
        self.loc = loc

    def __str__(self):
        return f"Token({self.ttype.name}, {self.val})"