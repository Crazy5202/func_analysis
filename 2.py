import sympy
import numpy as np
from matplotlib import pyplot as plt, gridspec

# Точность поиска
precision = 0.5


# Задаём границы отрезка
left_edge = 0
right_edge = 0.8 + 12/10


# Задаём функции
t = sympy.symbols('t')
f = (2*10/5-t)**2
y = sympy.sin(3*t)
x = []

def scalar(wrapper_func) -> float:
    return sympy.integrate(wrapper_func, (t, left_edge, right_edge))

def norm(wrapper_func) -> float:
    return scalar(wrapper_func**2)**0.5

# Разбиение отрезка на точки для вычислений
split = 1000
coord_axis = np.linspace(left_edge, right_edge, split)

#

n = 1

fourier_sum = 0

plt.ion()
fig = plt.figure()  # Начинаем с одного графика
fig.suptitle(f'Графики для ε = {precision}', fontsize=16)

ax = fig.add_subplot(1, 1, 1)
ax.set_title(f'Приближаемая функция')
ax.plot(coord_axis, sympy.lambdify(t, y, 'numpy')(coord_axis))

while (1):
    new_elem = t**(n-1)
    
    for old_elem in x:
        new_elem -= old_elem * scalar(new_elem*old_elem)/scalar(old_elem*old_elem)
    #new_elem /= scalar(new_elem, new_elem)**0.5
    x.append(new_elem)
    
    fourier_sum += new_elem * scalar(y*new_elem)/scalar(new_elem*new_elem)
    
    # Отрисовываем

    data = sympy.lambdify(t, fourier_sum, 'numpy')(coord_axis)
    if type(data) == float:
        data = [data]*len(coord_axis)

    """
    ax = fig.add_subplot(1, n, n)
    ax.set_title(f'Итерация {n}')
    
    ax.plot(coord_axis, data, label=f"Шаг {n}")
    """


    
    gs = gridspec.GridSpec(1, n+1)

    # Reposition existing subplots
    for i, ax in enumerate(fig.axes):
        ax.set_position(gs[i].get_position(fig))
        ax.set_subplotspec(gs[i])

    # Add new subplot
    new_ax = fig.add_subplot(gs[n])
    new_ax.set_title(f'Итерация {n}')
    new_ax.plot(data)

    
    plt.draw()  # Обновляем график
    plt.pause(0.5)  # Небольшая задержка для визуализации

    if (norm(fourier_sum - y) < precision):
        break
        
    n += 1

print("DONE!")

plt.ioff()
plt.show()  # Показываем финальный результат