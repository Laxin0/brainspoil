from definitions import Token, TokenType, types_str, BinOpKind, binop_precs
from irnodes import *

# TODO: REWRITE THIS SHIT FROM SCRATCH

class Parser():
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.i = 0
        self.tok = None
        self.dec_vars: list[str] = []


    def nextt(self):
        self.i += 1
        self.tok = self.tokens[self.i]
    
    def error(self, msg: str):
        print(f"[Error]: {msg}")
        exit(1)
    def parse_token(self,  ttype:TokenType, i) -> tuple[ErrorExpect|Token, int]:
        if self.tokens[i].ttype == ttype:
            return self.tokens[i], i+1
        else:
            return ErrorExpect(ttype, self.tokens[i].ttype, self.tokens[i].loc), 0

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
            return NIdent(ident.val), i
    
    def parse_expr(self, i,  min_prec) -> tuple[Expr|ErrorExpect, int]:
        # TODO: rewrite this shit
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
            if ident.name in self.dec_vars:
                return ident, ni
            else:
                self.error(f"Undeclared variable `{ident.name}` at {self.tokens[i-1].loc}")
        
        par_op_t, i = self.parse_token(TokenType.PAR_OP, i)
        if isinstance(par_op_t, ErrorExpect):
            return par_op_t, 0

        expr, i = self.parse_expr(i, 1)

        if isinstance(expr, ErrorExpect):
            return expr, 0

        par_cl_t, i = self.parse_token(TokenType.PAR_CL, i)
        if isinstance(par_cl_t, ErrorExpect):
            return par_cl_t, 0

        return expr, i

    def parse_declare(self, i) -> tuple[NDecl|ErrorExpect, int]:
        print(self.dec_vars)
        kw_let, i = self.parse_token(TokenType.KW_LET, i)
        if isinstance(kw_let, ErrorExpect):
            return kw_let, 0

        ident, i = self.parse_ident(i)
        if isinstance(ident, ErrorExpect): return ident, 0

        if ident.name in self.dec_vars:
            print(self.dec_vars)
            self.error(f"Variable name `{ident.name}` already used. at {self.tokens[i].loc}")


        self.dec_vars.append(ident.name)
        val = NIntlit(0)
        assi, i = self.parse_token(TokenType.ASSIGN, i)
        if isinstance(assi, Token):
            val, i = self.parse_expr(i, 1)
            if isinstance(val, ErrorExpect):
                return val, 0

        semi, i = self.parse_token(TokenType.SEMI, i)
        return NDecl(ident, val), i
    
    def parse_assign(self, i) -> tuple[NAssign|ErrorExpect, int]:
        ident, i = self.parse_ident(i)
        if isinstance(ident, ErrorExpect): return ident
        if not(ident.name in self.dec_vars): self.error(f"Undeclared variable `{ident.name}` at {self.tokens[i].loc}")
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
        
        if not(ident.name in self.dec_vars):
            self.error(f"Undeclared variable `{ident.name}` at {self.tokens[i-1].loc}")
        
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
