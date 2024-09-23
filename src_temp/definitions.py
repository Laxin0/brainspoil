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

    KW_LET = auto(),
    KW_PRINT = auto(),
    KW_READ = auto(),
    KW_IF = auto(),
    KW_ELSE = auto(),

    CUR_OP = auto(),
    CUR_CL = auto()

types_str = {TokenType.IDENT: 'variable name',
             TokenType.SEMI: '`;`',
             TokenType.EOF: 'end of file',
             TokenType.ASSIGN: '=',
             TokenType.INTLIT: 'int literal',
             TokenType.PAR_OP: '`(`',
             TokenType.PAR_CL: '`)`',
             TokenType.CUR_OP: '`{`',
             TokenType.CUR_CL: '`}`',
             TokenType.BINOP: '`+`, `-`, `*` or `/`',
             TokenType.KW_LET: '`let` keyword',
             TokenType.KW_PRINT: '`print` keyword',
             TokenType.KW_READ: '`read` keyword',
             TokenType.KW_IF: '`if` keyword',
             TokenType.KW_ELSE: '`else` keyword'}

keywords = {'let': TokenType.KW_LET,
            'print': TokenType.KW_PRINT,
            'read': TokenType.KW_READ,
            'if': TokenType.KW_IF,
            'else': TokenType.KW_ELSE}
from definitions import Token, TokenType, types_str, BinOpKind, binop_precs
from irnodes import *
import pprint
# TODO: REWRITE THIS SHIT FROM SCRATCH

class Parser():
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.i = 0
        self.tok = None
    def get_token(self, i):
        return self.tokens[i], i

    def peek_token(self, i):
        return self.tokens[i]

    def parse_token(self,  ttype:TokenType, i) -> tuple[ErrorExpect|Token, int]:
        if self.tokens[i].ttype == ttype:
            return self.tokens[i], i+1
        else:
            return ErrorExpect(ttype, self.tokens[i].ttype, self.tokens[i].loc), i

    def parse_intlit(self, i) -> tuple[NIntlit|ErrorExpect, int]:
        intlit, i = self.parse_token(TokenType.INTLIT, i)
        if isinstance(intlit, ErrorExpect):
            return intlit, i
        else:
            return NIntlit(intlit.val), i
    
    def parse_ident(self, i) -> tuple[NIdent|ErrorExpect, int]:
        ident, i = self.parse_token(TokenType.IDENT, i)
        if isinstance(ident, ErrorExpect):
            return ident, i
        else:
            return NIdent(ident), i

    def parse_expr(self, i,  min_prec) -> tuple[Expr|ErrorExpect, int]:
        # TODO: did't touch yet
        lhs, i = self.parse_term(i)
        
        if isinstance(lhs, ErrorExpect):
            return lhs, i

        while True:
            token = self.tokens[i]
            if (token.ttype == TokenType.EOF or token.ttype != TokenType.BINOP or binop_precs[token.val] < min_prec):
                break

            assert token.ttype == TokenType.BINOP

            op = token.val
            prec = binop_precs[op]
            next_min_prec = prec + 1

            i += 1

            rhs, i = self.parse_expr(i, next_min_prec)
            
            if isinstance(rhs, ErrorExpect):
                return rhs, i

            lhs = NBinExpr(op, lhs, rhs)

        return lhs, i

    def parse_term(self, i) -> tuple[NIntlit|NIdent|Expr|ErrorExpect, int]:

        intlit, i = self.parse_intlit(i)
        if isinstance(intlit, NIntlit):
            return intlit, i
        
        ident, i = self.parse_ident(i)
        if isinstance(ident, NIdent):
            return ident, i
        
        par_op_t, i = self.parse_token(TokenType.PAR_OP, i)
        if isinstance(par_op_t, ErrorExpect):
            return par_op_t, i

        expr, i = self.parse_expr(i, 1)

        if isinstance(expr, ErrorExpect):
            return expr, i

        par_cl_t, i = self.parse_token(TokenType.PAR_CL, i)
        if isinstance(par_cl_t, ErrorExpect):
            return par_cl_t, i

        return expr, i

    def parse_declare(self, i) -> tuple[NDecl|ErrorExpect, int]:
        kw_let, i = self.parse_token(TokenType.KW_LET, i)
        if isinstance(kw_let, ErrorExpect):
            return kw_let, i
        # let ...
        ident, i = self.parse_ident(i)

        if isinstance(ident, ErrorExpect):
            return ident, i
        # let id ...

        assi, i = self.parse_token(TokenType.ASSIGN, i)
        if isinstance(assi, ErrorExpect):
            semi, i = self.parse_token(TokenType.SEMI, i)
            if isinstance(semi, ErrorExpect):
                return semi, i
            # let id ;
            return NDecl(ident, NIntlit(0)), i
        else:
            # let id = ...
            i = ni
            val, i = self.parse_expr(i, 1)
            if isinstance(val, ErrorExpect):
                return val, i
            
            # let id = (epr) ...
            semi, i = self.parse_token(TokenType.SEMI, i)
            if isinstance(semi, ErrorExpect):
                return semi, i
            
            # let id = (epr) ;
            return NDecl(ident, val), i
        
    
    def parse_assign(self, i) -> tuple[NAssign|ErrorExpect, int]:
        ident, i = self.parse_ident(i)
        if isinstance(ident, ErrorExpect):
            return ident, i
        
        assi, i = self.parse_token(TokenType.ASSIGN, i)
        if isinstance(assi, ErrorExpect):
            return assi, i
        
        newval, i = self.parse_expr(i, 1)

        if isinstance(newval, ErrorExpect):
            return newval, i
        
        semi, i = self.parse_token(TokenType.SEMI, i)
        if isinstance(semi, ErrorExpect):
            return semi, i
        
        return NAssign(ident, newval), i

    def parse_print(self, i) -> tuple[NPrint|ErrorExpect, int]:
        print_kw, i = self.parse_token(TokenType.KW_PRINT, i)
        if isinstance(print_kw, ErrorExpect):
            return print_kw, i

        expr, i = self.parse_expr(i, 1)
        if isinstance(expr, ErrorExpect):
            return expr, i
        
        semi, i = self.parse_token(TokenType.SEMI, i)
        if isinstance(semi, ErrorExpect):
            return semi, i

        return NPrint(expr), i

    def parse_read(self, i) -> tuple[NRead|ErrorExpect, int]:
        read_kw, i = self.parse_token(TokenType.KW_READ, i)
        if isinstance(read_kw, ErrorExpect):
            return read_kw, i
    
        ident, i = self.parse_ident(i)
        if isinstance(ident, ErrorExpect):
            return ident, i
        
        semi, i = self.parse_token(TokenType.SEMI, i)
        if isinstance(semi, ErrorExpect):
            return semi, i
        
        return NRead(ident), i
    
    def parse_statement(self, i):
        dec, i = self.parse_declare(i)
        if isinstance(dec, NDecl):
            return dec, i
        
        assi, i = self.parse_assign(i)
        if isinstance(assi, NAssign):
            return assi, i

        prin, i = self.parse_print(i)
        if isinstance(prin, NPrint):
            return prin, i

        read, i = self.parse_print(i)
        if isinstance(read, NRead):
            return read, i

        scope, i = self.parse_scope(i)
        if isinstance(scope, NScope):
            return scope, i

        tok, i = self.get_token(i)
        return ErrorExpect([TokenType.KW_LET, TokenType.KW_PRINT, TokenType.KW_READ, TokenType.IDENT], tok.ttype, tok.loc), i

    def parse_scope(self, i):
        op_cur, i = self.parse_token(TokenType.CUR_OP, i)
        if isinstance(op_cur, ErrorExpect):
            return op_cur, i

        statements = []
        while True:
            stmt, i = self.parse_statement(i)
            if isinstance(stmt, ErrorExpect):
                break
            else:
                statements.append(stmt)

        if len(statements) == 0:
            return stmt, i

        cl_cur, i = self.parse_token(TokenType.CUR_CL, i)
        if isinstance(cl_cur, ErrorExpect):
            return cl_cur, i

        return NScope(statements), i

    def parse_ifelse(self, i):
        if_, i = self.parse_token(TokenType.KW_IF, i)
        if isinstance(if_, ErrorExpect):
            return if_, i

        expr, i = self.parse_expr(i)
        if isinstance(expr, ErrorExpect):
            return expr, i

        true_scope, i = self.parse_scope(i)
        if isinstance(true_scope, ErrorExpect):
            return true_scope, i

        else_, i = self.parse_token(TokenType.KW_ELSE, i)
        if isinstance(else_, ErrorExpect):
            return NIfElse(expr, true_scope, None), i
        else:
            false_scope, i = self.parse_scope(i)
            if isinstance(false_scope, ErrorExpect):
                return false_scope, i

            return NIfElse(expr, true_scope, false_scope), i
    def parse_tokens(self):
        i = 0

        statements = []
        while self.peek_token(ni).ttype != TokenType.EOF:
            stmt, i = self.parse_statement(i)
            if isinstance(stmt, ErrorExpect):
                stmt.report()
            else:
                statements.append(stmt)
        return statements

        while self.tokens[i].ttype != TokenType.EOF:
            if self.tokens[i].ttype == TokenType.SEMI:
                print(f"Statement can't starts with {types_str[TokenType.SEMI]} at {self.tokens[i].loc}")
                exit(1)
            elif self.tokens[i].ttype == TokenType.IDENT:
                stmt, i = self.parse_assign(i)
                if isinstance(stmt, ErrorExpect):
                    stmt.report()

                statements.append(stmt)
            elif self.tokens[i].ttype == TokenType.KW_LET:
                stmt, i = self.parse_declare(i)
                if isinstance(stmt, ErrorExpect):
                    stmt.report()
                statements.append(stmt)
            elif self.tokens[i].ttype == TokenType.KW_PRINT:
                stmt, i = self.parse_print(i)
                if isinstance(stmt, ErrorExpect):
                    stmt.report()
                statements.append(stmt)
            elif self.tokens[i].ttype == TokenType.KW_READ:
                stmt, i= self.parse_read(i)
                if isinstance(stmt, ErrorExpect):
                    stmt.report()
                statements.append(stmt)
            else:
                raise AssertionError(f"Unknown token type {self.tokens[i].ttype.name} at {self.tokens[i].loc}")
        return statements

class Token():
    def __init__(self, ttype: TokenType, val: int|None|BinOpKind, loc: tuple[int, int]):
        self.ttype = ttype
        self.val = val
        self.loc = loc

    def __str__(self):
        return f"Token({self.ttype.name}, {self.val})"
