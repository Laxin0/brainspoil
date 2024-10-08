from irnodes import *

class Generator():
    def __init__(self, statements: list[Statement]):
        self.statements = statements
        self.bfcode = ''
        self.headp = 0
        self.variables = {}
        self.vsp = 0
    
    def error(self, msg):
        print("[Error]:", msg)
        exit(1)

    def generate_bf(self) -> str:
        def to(toaddr: int):
            steps = toaddr-self.headp
            self.headp = toaddr
            if steps > 0:
                return '>'*steps
            else:
                return '<'*(-steps)
    
        def zero(a): return to(a) + '[-]'

        def move(d, s):
            return zero(d) + unsmove(d, s)
        
        def unsmove(d, s):
            return to(s) + '[-' + to(d) + '+' + to(s) + ']'
        
        def copy(d, s, t):
            return zero(d) + zero(t) + to(s) + '[-' + to(t) + '+' + to(d) + '+' + to(s) + ']' + unsmove(s, t)
        
        def addto(d, s, t):
            return zero(t) + to(s) + '[-' + to(t) + '+' + to(d) + '+' + to(s) + ']' + unsmove(s, t)
        
        def sub(r, a, b, t):
            return f'{copy(r, a, t)}{to(b)}[-{to(t)}+{to(r)}-{to(b)}]{unsmove(b, t)}'
        
        def add(s, a, b, t):
            return copy(s, a, t) + addto(s, b, t)
        
        def setc(a, val):
            return zero(a) + val*'+'

        def gen_id(node: NIdent):
            assert isinstance(node, NIdent)
            if node.tok.val in self.variables.keys():
                return self.variables[node.tok.val]
            else:
                self.error(f"Using undeclared variable `{node.tok.val}` at {node.tok.loc}")
        
        def gen_int(node: NIntlit):
            assert isinstance(node, NIntlit)
            self.bfcode += setc(self.vsp, node.val)
            self.vsp += 1
            return self.vsp-1
        
        def gen_term(node: Term):
            if isinstance(node, NIdent):
                return gen_id(node)
            elif isinstance(node, NIntlit):
                return gen_int(node)
            else:
                assert False

        def gen_binexpr(node: NBinExpr):
            assert isinstance(node, NBinExpr)
            res = self.vsp
            self.vsp += 1

            lhs = gen_expr(node.lhs)
            rhs = gen_expr(node.rhs)

            if node.op == BinOpKind.ADD:
                self.bfcode += add(res, lhs, rhs, self.vsp)
            elif node.op == BinOpKind.SUB:
                self.bfcode += sub(res, lhs, rhs, self.vsp)
            elif node.op == BinOpKind.MULT:
                raise NotImplementedError()
            elif node.op == BinOpKind.DIV:
                raise NotImplementedError()
            else:
                assert False
            
            self.vsp = res + 1
            return res

        def gen_expr(node: Expr):
            if isinstance(node, Term):
                return gen_term(node)
            elif isinstance(node, NBinExpr):
                return gen_binexpr(node)
            else:
                assert False

        def gen_decl(node: NDecl):
            assert isinstance(node, NDecl)
            val_a = gen_expr(node.val)
            var_tok = node.varid.tok
            if var_tok.val in self.variables.keys():
                self.error(f"Redeclaring variable `{var_tok.val}` at {var_tok.loc}")
            if val_a in self.variables.values():
                var_a = self.vsp
                self.vsp += 1
                self.bfcode += copy(var_a, val_a, self.vsp)
                self.variables.update({node.varid.tok.val: var_a})
            else:
                self.variables.update({node.varid.tok.val: val_a})


        def gen_assign(node: NAssign):
            assert isinstance(node, NAssign)

            var_a = gen_id(node.varid)
            val_a = gen_expr(node.val)
            if val_a in self.variables.values():
                self.bfcode += copy(var_a, val_a, self.vsp)
            else:
                self.bfcode += move(var_a, val_a)
                self.vsp = val_a

        def gen_print(node: NPrint):
            assert isinstance(node, NPrint)
            val_a = gen_expr(node.expr)
            self.bfcode += to(val_a) + '.'
            if not(val_a in self.variables.values()):
                self.vsp -= 1

        def gen_read(node: NRead):
            assert isinstance(node, NRead)
            addr = gen_id(node.ident)
            self.bfcode += to(addr) + ','
        
        def gen_ifelse(node: NIfElse):
            assert isinstance(node, NIfElse)
            if node.false_scope is None:
                cond = gen_expr(node.cond)
                self.bfcode += to(cond) + '['
                gen_scope(node.true_scope)
                self.bfcode += to(self.vsp) + '[-]]'
            else:
                t = self.v
                self.bfcode += f'{to(t)}[-]+{to(cond)}['
                gen_scope
        
        def gen_scope(node: NScope):
            assert isinstance(node, NScope)
            temp = self.vsp

            for stmt in node.stmts:
                if isinstance(stmt, NDecl):
                    '''DECLARE'''
                    gen_decl(stmt)

                elif isinstance(stmt, NAssign):
                    '''ASSIGN'''
                    gen_assign(stmt)
            
                elif isinstance(stmt, NPrint):
                    '''PRINT'''
                    gen_print(stmt)
            
                elif isinstance(stmt, NRead):
                    '''READ'''
                    gen_read(stmt)
                elif isinstance(stmt, NScope):
                    '''SCOPE'''
                    gen_scope(stmt)
                else:
                    assert False
            for i in range(self.vsp - temp):
                self.variables.popitem()
            # TODO: allow shadowing
            self.vsp = temp
        for stmt in self.statements:
                if isinstance(stmt, NDecl):
                    '''DECLARE'''
                    gen_decl(stmt)

                elif isinstance(stmt, NAssign):
                    '''ASSIGN'''
                    gen_assign(stmt)
            
                elif isinstance(stmt, NPrint):
                    '''PRINT'''
                    gen_print(stmt)
            
                elif isinstance(stmt, NRead):
                    '''READ'''
                    gen_read(stmt)
                elif isinstance(stmt, NScope):
                    '''SCOPE'''
                    gen_scope(stmt)
                else:
                    assert False

        return self.bfcode
