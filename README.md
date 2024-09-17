# DO NOT TOUCH! THIS SHIT IS UNDER DEVELOPMENT!

But if you want to try..

# About
Brainspoil is the high level programming language that compiles to brainfuck and does life much easier.
This project is under development so it misses most of the features.
It may contain some pretty shitty code, not for the faint of heart...

# Quick start

### Download
```
git clone https://laxin0/brainspoil.git
```

### Run
```
<python> brainspoil/src/brainspoil.py
```

### Usage
```
Usage: <your python> brainspoil/src/brainspoil.py <command>
    commands: 
        com <code.bs> [-o <out_filename>]               Compile brainspoil code to brainfuck

        runbf <your_code.bf> [-tl <tape length>]        Run brainfuck code. You can specify tape length
                                                        (by defautl it is 1024)
```

**Example:**
```
python brainspoil/src/brainspoil.py com test.bs -o compiled_test.bf
```
```
python brainspoil/src/brainspoil.py runbf compiled_test.bf
```

# Brainspoil lang

### Variables declaring
```
let a;
let b = 2;
let c = a + (b - 3);
```
**Note:**
Only supports *subtraction* and *addition* in expressions (yet).
By default variable value is 0.
Only integers below 256 (this is how brainfuck works)
 
### Variables reassigning
```
let a;
a = 3;
a = 5 - 4;
```

### IO
```
let char = 104;
print char;
read char;
print char;
```

**Note:**
`print` statement prints a character with the corresponding askii code
`read` statement read a charcter from terminal and store it like askii code
