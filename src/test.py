from sympy import Symbol,sin,limit

x = Symbol('x')
y = limit(sin(x)/x,x,0)
print(y)