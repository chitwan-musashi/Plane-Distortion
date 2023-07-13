# Projection Operation
from math import sqrt, acos, atan, cos
from sympy.solvers import solve
import sympy as sym
from numpy import real, imag, arange
import matplotlib.pyplot as plt
import cmath

p1 =  -1.28391472e-01
p2 = -1.22196105e-01

xDistorted = 700
yDistorted = -700

x = sym.Symbol('x')
y = sym.Symbol('y')
eq1 = sym.Eq(y + p1*(x**2 + 3*(y**2)) + 2*p2*x*y, yDistorted) 
eq2 = sym.Eq(x + p2*(y**2 + 3*(x**2)) + 2*p1*x*y, xDistorted) 

eq = solve([eq1, eq2], (x, y))
print(eq)
theta = atan(sqrt(xDistorted**2 + yDistorted**2)/(sqrt((abs(eq[0][0]))**2 + (abs(eq[0][1]))**2 )))
theta = atan((xDistorted-800)/abs(eq[1][0]))
print(theta)


'''x = arange(-100,100, 0.1)
y = []
h = []

for i in x:
    solutiony = (-(2*p1*i) + cmath.sqrt((2*p1*i)**2 - 4*p2*(i + 3*p2*(i**2) - xDistorted)))/2*(p2**2)
    #solutiony_ = (-(2*p1*i) - cmath.sqrt((2*p1*i)**2 - 4*p2*(i + 3*p2*(i**2) - xDistorted)))/2*(p2**2)
    solutionz = (-(2*p2*i - 1) + cmath.sqrt((2*p2*i - 1)**2 - 4*3*p1*(p1*(i**2) - yDistorted)))/2*(p2**2)
    #solutionz_ = (-(2*p2*i - 1) - cmath.sqrt((2*p2*i - 1)**2 - 4*3*p1*(p1*(i**2) - yDistorted)))/2*(p2**2)
    y.append(solutiony)
    #y.append(solutiony_)
    h.append(solutionz)
    #h.append(solutionz_)
    if real(solutiony) == real(solutionz):
        print(i)

plt.plot(x,y)
plt.plot(x,h)
plt.show()'''