from tokenization import Tokenizer
from parsing import Parser
from generation import Generator

def main():
    code: str
    with open('src\code.txt') as f:
        code = f.read()
    tokenizer = Tokenizer(code)
    tokens = tokenizer.get_tokens()
    print(list(map(str, tokens)))
    parser = Parser(tokens)
    ir = parser.parse_tokens()
    gen = Generator(ir)
    bfcode = gen.generate_bf()
    print(bfcode)

main()