import sympy
import numpy as np
from matplotlib import pyplot as plt

# Точность поиска
precision = 1e-4


# Задаём границы отрезка
left_edge = 0
right_edge = 0.8 + 12/10


# Задаём функции
t = sympy.symbols('t')
f = (2*10/5-t)**2
y = sympy.sin(3*t)
x = []

def scalar(x,y) -> float:
    wrapper_func = x*y
    return sympy.integrate(wrapper_func, (t, left_edge, right_edge))


# Разбиение отрезка на точки для вычислений
split = 1000
coord_axis = np.linspace(left_edge, right_edge, split)

#plt.plot(coord_axis, sympy.lambdify(t, y, 'numpy')(coord_axis))
#plt.show()

n = 1

fourier_sum = 0

while (1):
    new_elem = t**(n-1)
    
    for old_elem in x:
        new_elem -= old_elem * scalar(new_elem, old_elem)/scalar(old_elem, old_elem)
    #new_elem /= scalar(new_elem, new_elem)**0.5
    x.append(new_elem)
    n += 1
    fourier_sum += new_elem * scalar(y, new_elem)/scalar(new_elem, new_elem)
    