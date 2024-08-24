from enum import Enum

enumc = 0
def auto(start_with_zero = False):
    global enumc
    if start_with_zero:
        enumc = 0
    t = enumc
    enumc += 1
    return t

class TokenType(Enum):
    IDENT = auto(),
    SEMI = auto(),
    EOF = auto(),
    ASSIGN = auto(),
    INTLIT = auto(),

    KW_LET = auto()

types_str = {TokenType.IDENT: 'variable name',
             TokenType.SEMI: '`;`',
             TokenType.EOF: 'end of file',
             TokenType.ASSIGN: '=',
             TokenType.INTLIT: 'int literal',
             
             TokenType.KW_LET: '`let` keyword'}

keywords = {'let': TokenType.KW_LET}

class Token():
    def __init__(self, ttype: TokenType, val: int|None, loc: tuple[int, int]):
        self.ttype = ttype
        self.val = val
        self.loc = loc

    def __str__(self):
        return f"Token({self.ttype.name}, {self.val})"