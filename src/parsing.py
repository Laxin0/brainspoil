from definitions import Token, TokenType
from irnodes import *

class Parser():
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.i = 0
        self.tok = None
        self.varsid: list[str] = []


    def nextt(self):
        self.i += 1
        self.tok = self.tokens[self.i]
    
    def error(self, msg: str):
        print(f"[Error]: {msg}")
        exit(1)

    def parse_declare(self) -> NDecl:
        if self.tok.ttype != TokenType.KW_LET: raise AssertionError("something wrong")
        self.nextt()
        if self.tok.ttype != TokenType.IDENT: self.error(f"Expected variable identifire but found {self.tok}")
        name = self.tok.val
        if name in self.varsid: self.error(f"Variable name `{name}` already used")
        self.varsid.append(name)
        self.nextt()
        val = 0
        if self.tok.ttype == TokenType.ASSIGN:
            self.nextt()
            if self.tok.ttype != TokenType.INTLIT: self.error(f"Expected int literal in variable declaration but found {self.tok}")
            val = self.tok.val
            self.nextt()
        if self.tok.ttype != TokenType.SEMI: self.error(f"Expected `;` but found {self.tok}")
        self.nextt()
        return NDecl(name, val)
    
    def parse_assign(self) -> NAssign:
        if self.tok.ttype != TokenType.IDENT: raise AssertionError("something wrong")
        name = self.tok.val
        if not(name in self.varsid): self.error(f"Undeclared variable `{name}`")
        self.nextt()
        if self.tok.ttype != TokenType.ASSIGN: self.error(f"Expected `=` after variable identifier but found {self.tok}")
        self.nextt()
        if self.tok.ttype != TokenType.INTLIT: self.error(f"Expected int literal in variable assignment but found {self.tok}")
        newval = self.tok.val
        self.nextt()
        if self.tok.ttype != TokenType.SEMI: self.error(f"Expected `;` but found {self.tok}")
        self.nextt()
        return NAssign(name, newval)

    def parse_tokens(self):
        self.i = 0
        self.tok = self.tokens[0]

        statements = []
        
        while self.tok.ttype != TokenType.EOF:
            if self.tok.ttype == TokenType.SEMI:
                self.error("Statement can't starts with `;`")
            elif self.tok.ttype == TokenType.IDENT:
                stmt = self.parse_assign()
                statements.append(stmt)
            elif self.tok.ttype == TokenType.KW_LET:
                stmt = self.parse_declare()
                statements.append(stmt)
            else:
                raise AssertionError(f"Unknown token type {self.tok.ttype.name}")
        return statements
    