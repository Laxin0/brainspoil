from tokenization import Tokenizer
from parsing import Parser
from generation import Generator
from intepreter import Intepr
from sys import argv

def usage():
    print('Usage: <your python> brainspoil/src/brainspoil.py <command>'                                                       )
    print(                                                                                                         )
    print('    commands:'                                                                                          )
    print('        com <code.bs> [-o <out_filename>]               Compile brainspoil code to brainfuck'           )
    print(                                                                                                         )
    print('        runbf <your_code.bf> [-tl <tape length>]        Run brainfuck code. You can specify tape length')
    print('                                                        (by defautl it is 1024)'                        )

def com(path: str, outpath: str=''):
    code: str
    try:
        with open(path, 'r') as infile:
            code = infile.read()
    except FileNotFoundError:
        print(f'[Error]: File `{path}` does not exist')
        exit(1)

    print(f'Compiling {path}...')
    #TODO: maybe add debug mode
    #print('len =', len(code))
    #print('code =', code.replace('\n', '\\n'))
    #TODO: store this shit all time is disgusting...
    tokenizer = Tokenizer(code)
    tokens = tokenizer.get_tokens()
    #print(list(map(str, tokens)))
    parser = Parser(tokens)
    ir = parser.parse_tokens()
    gen = Generator(ir)
    bfcode = gen.generate_bf()

    if outpath == '':
        outpath = path[:path.rfind('.')]+'.bf'

    print(f'Writing bf code to {outpath}...')
    try:
        with open(outpath, 'w') as out:
            out.write(bfcode)
    except:
        print(f'[Error] Can\'t write to file `{outpath}` for some reason.')
        exit(1)
    print(f'Successful compilation from `{path}` to `{outpath}`.')
    #print('bfcode =', bfcode)
    #print("sp =", gen.vsp)
    #print("vars =", [tuple(i) for i in gen.variables.items()])

def runbf(path: str, tlength: int=1024, dump: bool=False):
    code: str
    try:
        with open(path, 'r') as infile:
            code = infile.read()
    except FileNotFoundError:
        print(f'[Error]: File `{path}` does not exist')
        exit(1)
    print(f'Running `{path}`...\n')
    intepr = Intepr(code, tlength)
    intepr.run()
    print(f'\n\nProgram executed.')
    if dump:
        intepr.dumpmem()

def main():
    #print(argv)
    args = argv[1:] # remove path to this python file
    if len(args) == 0:
        usage()
        exit(0)

    match args:
        case 'com', path:
            com(path)
        case 'com', path, '-o', outpath:
            com(path, outpath)
        case 'runbf', path:
            runbf(path)
        case 'runbf', path, '-tl', length:
            l: int
            try:
                l = int(length)
                assert l > 0
            except:
                print('[Error]: Tape length must be positive integer')
                exit(1)
            runbf(path, l)
        case _:
            print("Maybe you did something wrong?")
            print()
            usage()
            exit(0)

main()
