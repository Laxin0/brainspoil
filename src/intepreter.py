class Intepr():
    
    head: int
    code: str
    mem: bytearray
    memcap: int

    def __init__(self, code, memcap=1024):
        self.code = code
        self.memcap = memcap

    def run(self):
        pc = 0
        self.mem = bytearray(self.memcap)
        self.head = 0
        while pc < len(self.code):
            if self.code[pc] == '+':
                self.mem[self.head] = (self.mem[self.head] + 1) % 256
            elif self.code[pc] == '-':
                self.mem[self.head] = (self.mem[self.head] - 1) % 256
            elif self.code[pc] == ',':
                self.mem[self.head] = ord(input())
            elif self.code[pc] == '.':
                print(chr(self.mem[self.head]), end='')
            elif self.code[pc] == '>':
                self.head += 1
            elif self.code[pc] == '<':
                self.head -= 1
            elif self.code[pc] == '[':
                if self.mem[self.head] == 0:
                    stack = 1
                    while stack > 0:
                        pc += 1
                        if self.code[pc] == '[':
                            stack += 1
                        if self.code[pc] == ']':
                            stack -= 1
                    
            elif self.code[pc] == ']':
                if self.mem[self.head] != 0:
                    stack = 1
                    while stack > 0:
                        pc -= 1
                        if self.code[pc] == '[':
                            stack -= 1
                        if self.code[pc] == ']':
                            stack += 1
            else:
                print(f"inpalid character at {pc}")
                return
            pc += 1

    def dumpmem(self):
        print([n for n in self.mem])