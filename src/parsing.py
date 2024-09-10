from definitions import Token, TokenType, types_str, BinOpKind, binop_precs
from irnodes import *

# TODO: REWRITE THIS SHIT FROM SCRATCH

class Parser():
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.i = 0
        self.tok = None

    def nextt(self):
        self.i += 1
        self.tok = self.tokens[self.i]
    
    def error(self, msg: str):
        print(f"[Error]: {msg}")
        exit(1)

    def parse_intlit(self, i) -> tuple[NIntlit|ErrorExpect, int]:
        if self.tokens[i].ttype != TokenType.INTLIT: return ErrorExpect(TokenType.INTLIT, self.tokens[i].ttype, self.tokens[i].loc), 0
        lit = NIntlit(self.tokens[i].val)
        return lit, i+1

    
    def parse_ident(self, i) -> tuple[NIdent|ErrorExpect, int]:
        if self.tokens[i].ttype != TokenType.IDENT: return ErrorExpect(TokenType.IDENT, self.tokens[i].ttype, self.tokens[i].loc), 0
        ident = NIdent(self.tokens[i])
        return ident, i+1
    
    def parse_expr(self, i,  min_prec) -> tuple[Expr|ErrorExpect, int]:
        lhs, i = self.parse_term(i)
        
        if isinstance(lhs, ErrorExpect):
            return lhs, 0

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
                return rhs, 0

            lhs = NBinExpr(op, lhs, rhs)

        return lhs, i

    def parse_term(self, i) -> tuple[NIntlit|NIdent|Expr|ErrorExpect, int]:

        intlit, ni = self.parse_intlit(i)
        if isinstance(intlit, NIntlit):
            return intlit, ni
        
        ident, ni = self.parse_ident(i)
        if isinstance(ident, NIdent):
            return ident, ni
        
        if self.tokens[i].ttype != TokenType.PAR_OP:
            return ErrorExpect(TokenType.PAR_OP, self.tokens[i].ttype, self.tokens[i].loc), 0
        
        i += 1
        expr, i = self.parse_expr(i, 1)

        if isinstance(expr, ErrorExpect):
            return expr, 0
        
        if self.tokens[i].ttype != TokenType.PAR_CL:
            return ErrorExpect(TokenType.PAR_CL, self.tokens[i].ttype, self.tokens[i].loc), 0
        
        i += 1
        return expr, i

    def parse_declare(self, i) -> tuple[NDecl|ErrorExpect, int]:
        if self.tokens[i].ttype != TokenType.KW_LET: return ErrorExpect(TokenType.KW_LET, self.tokens[i].ttype, self.tokens[i].loc), 0
        i += 1
        ident, i = self.parse_ident(i)
        if isinstance(ident, ErrorExpect): return ident
        val = NIntlit(0)
        if self.tokens[i].ttype == TokenType.ASSIGN:
            i += 1
            val, i = self.parse_expr(i, 1)
            if isinstance(val, ErrorExpect): return val, 0

        if self.tokens[i].ttype != TokenType.SEMI: return ErrorExpect(TokenType.SEMI, self.tokens[i].ttype, self.tokens[i].loc), 0
        i += 1
        return NDecl(ident, val), i
    
    def parse_assign(self, i) -> tuple[NAssign|ErrorExpect, int]:
        ident, i = self.parse_ident(i)
        if isinstance(ident, ErrorExpect): return ident
        if self.tokens[i].ttype != TokenType.ASSIGN: return ErrorExpect(TokenType.ASSIGN, self.tokens[i].ttype, self.tokens[i].loc), 0
        i += 1
        
        newval, i = self.parse_expr(i, 1)

        if isinstance(newval, ErrorExpect):
            return newval, 0
        
        if self.tokens[i].ttype != TokenType.SEMI: self.error_exp(TokenType.SEMI, self.tokens[i].ttype, self.tokens[i].loc)
        i+=1
        return NAssign(ident, newval), i

    def parse_print(self, i) -> tuple[NPrint|ErrorExpect, int]:
        if self.tokens[i].ttype != TokenType.KW_PRINT: return ErrorExpect(TokenType.KW_PRINT, self.tokens[i].ttype, self.tokens[i].loc), 0
        i += 1

        expr, i = self.parse_expr(i, 1)
        if isinstance(expr, ErrorExpect):
            return expr, 0
        
        if self.tokens[i].ttype != TokenType.SEMI: return ErrorExpect(TokenType.SEMI, self.tokens[i].ttype, self.tokens[i].loc), 0
        i += 1
        return NPrint(expr), i

    def parse_read(self, i) -> tuple[NRead|ErrorExpect, int]:
        if self.tokens[i].ttype != TokenType.KW_READ: return ErrorExpect(TokenType.KW_READ, self.tokens[i].ttype, self.tokens[i].loc), 0
        i += 1
    
        ident, i = self.parse_ident(i)
        if isinstance(ident, ErrorExpect):
            return ident, 0
        
        if self.tokens[i].ttype != TokenType.SEMI: return ErrorExpect(TokenType.SEMI, self.tokens[i].ttype, self.tokens[i].loc), 0
        i += 1
        return NRead(ident), i
        
    def parse_tokens(self):
        i = 0
        statements = []
        
        while self.tokens[i].ttype != TokenType.EOF:
            if self.tokens[i].ttype == TokenType.SEMI:
                self.error(f"Statement can't starts with {types_str[TokenType.SEMI]} at {self.tokens[i].loc}")
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