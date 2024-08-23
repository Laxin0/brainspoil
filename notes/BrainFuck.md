0t0a00b0s000000
   ^

let a
a
{
	let b
	ab
	let c
	abc
	a = b + c
	abc
}
a
let q
aq
a += q
aq


\[ stack ] 


`@(k)`

zero()  ->  `[-]`
set current cell to zero

add(k)  ->  `[ - @(k) + @(-k) ]`
add curent cell to $+k (unsafe)

add(b, s, t)  ->  
```
copy(s, t)
@(b)
[ - @(t-b) + @(s-t) + @(b-s)]
@(t-b)
move(b-t)
@(-t)
```

move(k)  ->  `@k zero() @(-k) [ - @(k) + @(-k) ]`

copy(k, t)  -> 
```
@(t) zero() @(k-t) zero() @(-k)
[ - @(t) + @(k-t) + @(-k) ]
@(t) move(-t) @(-t)
```

ifelse(t)  ->
```
@(t)[-]+@(-t) устанавливаем флаг 1 для случая else
[
    здесь действия ветки true
    @(t)[-]@(-t) устанавливаем флаг 0 для случая else
    [-] выход из цикла
]
@(t)
[
	@(-t)
    здесь действия ветки false
    @(t)[-] выход из цикла
]
@(-t)
```

*stmt = parse_stmt()
is stmt is None: error(self.tok.pos)*
# Lang
let a
let b
let c = a + b

if cond:
	pass
		pass
else:
	pass

`if cond:`
`\t pass`
`else:`
`\t pass`

`while cond:`
`\t if cond:` 
`\t \t pass`

while cond:
	if cond:
		pass

exec(>>++<<-.)

layout v = {3, 2}
def x = 0+6
const y = 1

v.5

macro f:
	pass

## ideas

struct d = {x = 1 , y = 2}
d.x
d.y



*math* -> + - * / 


$$
\begin{align}
[\text{Prog}] &\to [\text{Stmt}]^* \\
[\text{Stmt}] &\to
\begin{cases}
\text{exit}([\text{Expr}]); \\
\text{let}\space\text{ident} = [\text{Expr}]; \\
\text{ident} = \text{[Expr]}; \\
\text{if} ([\text{Expr}])[\text{Scope}]\text{[IfPred]}\\
[\text{Scope}]
\end{cases} \\
\text{[Scope]} &\to {[\text{Stmt}]^*} \\
\text{[IfPred]} &\to
\begin{cases}
\text{elif}(\text{[Expr]})\text{[Scope]}\text{[IfPred]} \\
\text{else}\text{[Scope]} \\
\epsilon
\end{cases} \\
[\text{Expr}] &\to
\begin{cases}
[\text{Term}] \\
[\text{BinExpr}]
\end{cases} \\
[\text{BinExpr}] &\to
\begin{cases}
[\text{Expr}] * [\text{Expr}] & \text{prec} = 1 \\
[\text{Expr}] / [\text{Expr}] & \text{prec} = 1 \\
[\text{Expr}] + [\text{Expr}] & \text{prec} = 0 \\
[\text{Expr}] - [\text{Expr}] & \text{prec} = 0 \\
\end{cases} \\
[\text{Term}] &\to
\begin{cases}
\text{intlit} \\
\text{ident} \\
([\text{Expr}])
\end{cases}
\end{align}
$$