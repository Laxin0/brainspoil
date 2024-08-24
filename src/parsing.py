from definitions import Token, TokenType, types_str
from irnodes import *

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

    def parse_declare(self) -> NDecl:
        self.nextt()
        if self.tok.ttype != TokenType.IDENT: self.error(f"Expected {types_str[TokenType.IDENT]} but found {types_str[self.tok.ttype]} at {self.tok.loc}")
        name = self.tok.val
        if name in self.dec_vars: self.error(f"Variable name `{name}` already used. at {self.tok.loc}")
        self.dec_vars.append(name)
        self.nextt()
        val = 0
        if self.tok.ttype == TokenType.ASSIGN:
            self.nextt()
            if self.tok.ttype != TokenType.INTLIT: self.error(f"Expected {types_str[TokenType.INTLIT]} in variable declaration but found {types_str[self.tok.ttype]} at {self.tok.loc}")
            val = self.tok.val
            self.nextt()
        if self.tok.ttype != TokenType.SEMI: self.error(f"Expected {types_str[TokenType.SEMI]} but found {types_str[self.tok.ttype]} at {self.tok.loc}")
        self.nextt()
        return NDecl(name, val)
    
    def parse_assign(self) -> NAssign:
        name = self.tok.val
        if not(name in self.dec_vars): self.error(f"Undeclared variable `{name}` at {self.tok.loc}")
        self.nextt()
        if self.tok.ttype != TokenType.ASSIGN: self.error(f"Expected {types_str[TokenType.ASSIGN]} after variable identifier but found {types_str[self.tok.ttype]} at {self.tok.loc}")
        self.nextt()
        if self.tok.ttype != TokenType.INTLIT: self.error(f"Expected {types_str[TokenType.INTLIT]} in variable assignment but found {types_str[self.tok.ttype]} at {self.tok.loc}")
        newval = self.tok.val
        self.nextt()
        if self.tok.ttype != TokenType.SEMI: self.error(f"Expected {types_str[TokenType.SEMI]} but found {types_str[self.tok.ttype]} at {self.tok.loc}")
        self.nextt()
        return NAssign(name, newval)

    def parse_tokens(self):
        self.i = 0
        self.tok = self.tokens[0]

        statements = []
        
        while self.tok.ttype != TokenType.EOF:
            if self.tok.ttype == TokenType.SEMI:
                self.error(f"Statement can't starts with {types_str[TokenType.SEMI]} at {self.tok.loc}")
            elif self.tok.ttype == TokenType.IDENT:
                stmt = self.parse_assign()
                statements.append(stmt)
            elif self.tok.ttype == TokenType.KW_LET:
                stmt = self.parse_declare()
                statements.append(stmt)
            else:
                raise AssertionError(f"Unknown token type {self.tok.ttype.name} at {self.tok.loc}")
        return statements
    