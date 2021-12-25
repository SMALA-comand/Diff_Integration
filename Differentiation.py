import math
import random
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from scipy.misc import derivative

# Константы
inf = 10 ** 12


def ready_func_derivative(f, A, B, step):
    # тут можно использовать scipy.misc.derivative()
    def fun(x):
        try:
            ans = eval(f)
        except (ZeroDivisionError, ValueError):
            return 0.0  # этот ноль в ответ не пойдет, если что
        return ans

    deriv = []
    i = A

    while i <= B:
        dif = derivative(func=fun, x0=i, dx=step)
        i += step
        deriv.append(dif)

    return deriv

def diff(f, A = 0, B = 0, step = 0.1, accuracy = 3):
    '''
    Функция интегрирования
    Parameters
    ----------
    f : string, required
    Функция, записанная без y =  зависящая от x
    A : float, optional
    Начало промежутка дифференцирования
    B : float, optional
    Конец промежутка дифференцирования
    step : float, optional
    Шаг дифференцирования
    accuracy : int, float
    Точность дифференцирования

    Returns
    -------
    x_coord : array of float
    Координаты по оси x
    derivatives : array of float
    Значения производной
    f_x : array of float
    Значения исходной функции
    '''
    import check_function as ch_f
    f = ch_f.convertion(f)
    if 'x' not in f:
        print('Функция задана неверно. Попробуйте снова!')
        return(None, None, None)
    x_coord = []  # сюда записываем в каких точках считаем производные (при [-1, 1] и step=0.1 это будет -1,-0.9 и т.д.)
    derivatives = []  # сюда записываем ответы
    f_x = []
    i = A
    while i <= B:
        # наша функция записана как строка. Есть волшебная встроенная в питон штука как eval()
        # она считает нашу строку и выполнит так, будто бы это обычная команда в питоне.
        # например. У нас есть функция f = "x**2 + 2". Мы до вызова eval() определяем x=3. Потом вызываем eval(f)
        # и получаем значение этой функции при x=3, то есть (3**2 + 2) = 11
        # поэтому сначала пишем, что x = i и только потом считаем функции с помощью eval()
        x_coord.append(round(i, accuracy))
        x = i
        try:
            f0 = eval(f)
            f_x.append(f0)
        except (ZeroDivisionError, ValueError):
            f_x.append(None)

        x = i - step
        try:
            f1 = eval(f)
        # затем рассчитываем f(i-h)
        except (ZeroDivisionError, ValueError):
            # print(eval(f))
            derivatives.append(None)
            i += step
            continue

        # затем рассчитываем f(i+h)
        x = i + step
        try:
            f2 = eval(f)
        except (ZeroDivisionError, ValueError):
            # print(eval(f), '!')
            derivatives.append(None)
            i += step
            continue

        # теперь алгоритм расчета производной ...
        d_f = (f2 - f1) / (2 * step)
        d_f = round(d_f, accuracy)

        if abs(d_f) >= inf:
            derivatives.append(None)
        else:
            derivatives.append(d_f)
        i += step

    return x_coord, derivatives, f_x

def table_and_graph_for_different(title, x_coord, der, scpy, dlt, step, accuracy, f_x):
    """
            Строим график производной и сравниваем эффективность функции
            Parameters
            ----------
            title : string, required
                Функция, записанная в виде строки
            x_coord : array of float, required
                Координаты по оси x
            integrals: array of float, required
                Значения производной функции от x, посчитанные нашим алгоритмом
            scpy : array of float, required
                Значения производной функции от x, посчитанные методами scipy
            step : float, optional
                Шаг дифференцирования
            accuracy : int, required
                Задаёт точность подсчёта значений после запятой
            f_x : array of float, required
                Значения функции, по которой считаем производную

            Returns
            -------
            Строит график сравнения значений производных функций
            Выходные параметры отсутствуют

            """
    for i in range(len(scpy)):
        if scpy[i] is None or dlt[i] == '---':
            continue
        scpy[i] = round(scpy[i], accuracy)
        dlt[i] = round(dlt[i], accuracy)

    mytable = PrettyTable()

    mytable.title = title
    mytable.add_column("N", [i for i in range(1, len(x_coord) + 1)])
    mytable.add_column("x", x_coord)
    mytable.add_column("f'(x)", der)

    # Нужно добавить f'(x)сущ и del(f)

    mytable.add_column("f'(x)сущ", scpy)
    mytable.add_column("delta(f)", dlt)
    print(mytable)

    # Строим график
    fig, ax = plt.subplots(nrows=1, ncols=2)
    ax[0].plot(x_coord, der, 'bo-', label='Наша производная')
    ax[0].plot(x_coord, scpy, 'r--', label='Чужая производная')
    ax[0].set(xlabel='Ось абцисс x', ylabel="Значения производной f'(x)")
    ax[0].legend(loc='upper left')

    ax[1].plot(x_coord, f_x, 'b', label='Функция')
    ax[1].set(xlabel='Ось абцисс x', ylabel="Значения функции f(x)")
    ax[1].legend(loc='upper left')

    plt.title(f'График производной от ({title})', loc='center', pad=10)
    # ax.grid(axis = 'both')
    # plt.subplots_adjust(wspace=4, hspace=0)
    fig.set_figwidth(12)
    fig.set_figheight(6)
    plt.show()




