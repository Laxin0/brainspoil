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
            return NIdent(ident), i

    def parse_expr(self, i,  min_prec) -> tuple[Expr|ErrorExpect, int]:
        # TODO: did't touch yet
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
        
        par_op_t, ni = self.parse_token(TokenType.PAR_OP, i)
        if isinstance(par_op_t, ErrorExpect):
            return par_op_t, 0

        expr, ni = self.parse_expr(ni, 1)

        if isinstance(expr, ErrorExpect):
            return expr, 0

        par_cl_t, ni = self.parse_token(TokenType.PAR_CL, ni)
        if isinstance(par_cl_t, ErrorExpect):
            return par_cl_t, 0

        return expr, ni

    def parse_declare(self, i) -> tuple[NDecl|ErrorExpect, int]:
        kw_let, i = self.parse_token(TokenType.KW_LET, i)
        if isinstance(kw_let, ErrorExpect):
            return kw_let, 0
        # let ...
        ident, i = self.parse_ident(i)

        if isinstance(ident, ErrorExpect):
            return ident, 0
        # let id ...

        assi, ni = self.parse_token(TokenType.ASSIGN, i)
        if isinstance(assi, ErrorExpect):
            semi, i = self.parse_token(TokenType.SEMI, i)
            if isinstance(semi, ErrorExpect):
                return semi, 0
            # let id ;
            return NDecl(ident, NIntlit(0)), i
        else:
            # let id = ...
            i = ni
            val, i = self.parse_expr(i, 1)
            if isinstance(val, ErrorExpect):
                return val, 0
            
            # let id = (epr) ...
            semi, i = self.parse_token(TokenType.SEMI, i)
            if isinstance(semi, ErrorExpect):
                return semi, 0
            
            # let id = (epr) ;
            return NDecl(ident, val), i
        
    
    def parse_assign(self, i) -> tuple[NAssign|ErrorExpect, int]:
        ident, i = self.parse_ident(i)
        if isinstance(ident, ErrorExpect):
            return ident, 0
        
        assi, i = self.parse_token(TokenType.ASSIGN, i)
        if isinstance(assi, ErrorExpect):
            return assi, 0
        
        newval, i = self.parse_expr(i, 1)

        if isinstance(newval, ErrorExpect):
            return newval, 0
        
        semi, i = self.parse_token(TokenType.SEMI, i)
        if isinstance(semi, ErrorExpect):
            return semi, 0
        
        return NAssign(ident, newval), i

    def parse_print(self, i) -> tuple[NPrint|ErrorExpect, int]:
        print_kw, i = self.parse_token(TokenType.KW_PRINT, i)
        if isinstance(print_kw, ErrorExpect):
            return print_kw, 0

        expr, i = self.parse_expr(i, 1)
        if isinstance(expr, ErrorExpect):
            return expr, 0
        
        semi, i = self.parse_token(TokenType.SEMI, i)
        if isinstance(semi, ErrorExpect):
            return semi, 0

        return NPrint(expr), i

    def parse_read(self, i) -> tuple[NRead|ErrorExpect, int]:
        read_kw, i = self.parse_token(TokenType.KW_READ, i)
        if isinstance(read_kw, ErrorExpect):
            return read_kw, 0
    
        ident, i = self.parse_ident(i)
        if isinstance(ident, ErrorExpect):
            return ident, 0
        
        semi, i = self.parse_token(TokenType.SEMI, i)
        if isinstance(semi, ErrorExpect):
            return semi, 0
        
        return NRead(ident), i
    
    def parse_statement(self, i):
        dec, ni = self.parse_declare(i)
        if isinstance(dec, NDecl):
            return dec, ni
        
        assi, ni = self.parse_assign(i)
        if isinstance(assi, NAssign):
            return assi, ni

        prin, ni = self.parse_print(i)
        if isinstance(prin, NPrint):
            return prin, ni

        read, ni = self.parse_print(i)
        if isinstance(read, NRead):
            return read, ni

        scope, ni = self.parse_scope(i)
        if isinstance(scope, NScope):
            return scope, ni

        tok, i = self.get_token(i)
        return ErrorExpect([TokenType.KW_LET, TokenType.KW_PRINT, TokenType.KW_READ, TokenType.IDENT], tok.ttype, tok.loc), 0

    def parse_scope(self, i):
        op_cur, i = self.parse_token(TokenType.CUR_OP, i)
        if isinstance(op_cur, ErrorExpect):
            return op_cur, 0

        statements = []
        ni = i
        while True:
            stmt, ni = self.parse_statement(ni)
            if isinstance(stmt, ErrorExpect):
                break
            else:
                statements.append(stmt)
                i = ni


        if len(statements) == 0:
            return stmt, 0

        cl_cur, i = self.parse_token(TokenType.CUR_CL, i)
        if isinstance(cl_cur, ErrorExpect):
            return cl_cur, 0

        return NScope(statements), i


    def parse_tokens(self):
        i = 0

        statements = []
        ni = i
        while self.peek_token(ni).ttype != TokenType.EOF:
            stmt, ni = self.parse_statement(ni)
            if isinstance(stmt, ErrorExpect):
                stmt.report()
            else:
                statements.append(stmt)
                i = ni
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
