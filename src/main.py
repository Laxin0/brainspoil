from tokenization import Tokenizer
from parsing import Parser
from generation import Generator
from intepreter import Intepr

def main():
    code: str
    with open('src/code.txt') as f:
        code = f.read()
    print('len =', len(code))
    print(code.replace('\n', '\\n'))
    tokenizer = Tokenizer(code)
    tokens = tokenizer.get_tokens()
    # print(list(map(str, tokens)))
    parser = Parser(tokens)
    ir = parser.parse_tokens()
    gen = Generator(ir)
    bfcode = gen.generate_bf()
    print(bfcode)
    inter = Intepr(bfcode, 32)
    print()
    print()
    inter.run()
    print()
    print()
    inter.dumpmem()
    print("sp =", gen.vsp)
    print("vars =", [tuple(i) for i in gen.variables.items()])

main()