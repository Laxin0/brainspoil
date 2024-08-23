from definitions import TokenType, Token, keywords
    
class Tokenizer():
    def __init__(self, src: str):
        self.src = src

    def get_tokens(self):
        i = 0
        tokens = []
        while i < len(self.src):
            if self.src[i] == ';':
                tokens.append(Token(TokenType.SEMI, None))
                i += 1
            elif self.src[i].isalpha():
                buf = ''
                while i < len(self.src) and self.src[i].isalnum():
                    buf += self.src[i]
                    i += 1
                if buf in keywords.keys():
                    tokens.append(Token(keywords[buf], None))
                else:
                    tokens.append(Token(TokenType.IDENT, buf))
            elif self.src[i].isspace():
                i+=1
            elif self.src[i] == '=':
                tokens.append(Token(TokenType.ASSIGN, None))
                i+=1
            elif self.src[i].isnumeric():
                buf = ''
                while i < len(self.src) and self.src[i].isnumeric():
                    buf += self.src[i]
                    i += 1
                tokens.append(Token(TokenType.INTLIT, int(buf)%256))
            else:
                raise AssertionError("invalid token")
        tokens.append(Token(TokenType.EOF, None))
        return tokens
    
