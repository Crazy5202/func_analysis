import sympy
import numpy as np
from matplotlib import pyplot as plt, gridspec

# Класс для отрисовки сеткой

class Drawer():

    def __init__(self, max_cols, plot_cords, initial_data) -> None:
        """Принимает параметры и рисует приближаемую функцию.
        """
        self.fig = plt.figure()
        self.row = 1
        self.col = 1
        self.max_cols = max_cols
        self.plot_cords = plot_cords
        
        # Отрисовка начального графика
        ax = self.fig.add_subplot(self.row, self.col, (self.row-1)*self.max_cols + self.col)
        ax.set_title('Приближаемая функция')
        ax.plot(plot_cords, initial_data)

    def plot_new(self, data: list) -> None:
        """Добавляет график новой итерации в сетку."""
        self.col += 1
        if (self.col % (self.max_cols+1) == 0):
            self.col = 1
            self.row += 1
        
        gs = gridspec.GridSpec(self.row, self.max_cols)

        # Перемещение предыдущих графиков
        for i, ax in enumerate(self.fig.axes):
            ax.set_position(gs[i].get_position(self.fig))
            ax.set_subplotspec(gs[i])

        # Отрисовка нового графика
        ind = (self.row-1)*self.max_cols + self.col-1
        new_ax = self.fig.add_subplot(gs[ind])
        new_ax.set_title(f'Итерация {ind}')
        new_ax.plot(self.plot_cords, data)


# Точность приближения

precision = 0.01



# Задание границ отрезка

left_edge = 0
right_edge = 0.8 + 12/10

# Задание функции

t = sympy.symbols('t') # переменная для интегрирования и вычислений
f = (2*10/5-t)**2
y = sympy.sin(3*t)
x = [] # содержит ортогональный базис вида t^(n-1)

def scalar(wrapper_func) -> float:
    return sympy.integrate(wrapper_func, (t, left_edge, right_edge))

def norm(wrapper_func) -> float:
    return scalar(wrapper_func**2)**0.5

# Разбиение отрезка на точки для вычислений

split = 1000
cords = np.linspace(left_edge, right_edge, split)

# Задание начального параметра и частичной суммы ряда Фурье

n = 1
fourier_sum = 0

# Начальная отрисовка

plt.ion() # включает интерактивный режим, чтобы отрисовывать в процессе выполнения
drawer = Drawer(3, cords, sympy.lambdify(t, y, 'numpy')(cords))

# Выполняем, пока не будет выполнено условие выхода

while (1):
    # Выбор нового элемента базиса

    new_elem = t**(n-1)
    
    # Ортогонализация элемента предыдущим

    for old_elem in x:
        new_elem -= old_elem * scalar(new_elem*old_elem)/scalar(old_elem*old_elem)
    
    # Добавление элемента в базис

    x.append(new_elem)
    
    # Изменение частичной суммы ряда Фурье

    fourier_sum += new_elem * scalar(y*new_elem)/scalar(new_elem*new_elem)
    
    # Рассчёт значений частичной суммы ряда Фурье

    data = sympy.lambdify(t, fourier_sum, 'numpy')(cords)
    if type(data) == float:
        data = [data]*len(cords)

    # Отрисовка новой итерации

    drawer.plot_new(data)
    plt.draw()  # обновляет график
    plt.pause(0.5)  # создаёт задержку для обновления графика

    # Проверка, что отклонение меньше чем заданная точность

    if (norm(fourier_sum - y) < precision): 
        break
        
    # Условие выхода не выполнилось => новая итерация

    n += 1

plt.ioff() # выключает интерактивный режим, чтобы оставить конечный результат
print("\n\nРАБОТА ПРОГРАММЫ ЗАКОНЧЕНА!\n\n")
plt.show()  # показывает финальный результат