import math
import random
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from prettytable import PrettyTable


# Константы
inf = 10 ** 12


def ready_func_integrate(f, A, B, step):
    # тут можно использовать scipy.integrate()
    def fun(x):
        try:
            ans = eval(f)
        except (ZeroDivisionError, ValueError):
            return 0.0  # этот ноль в ответ не пойдет, если что
        return ans

    integra = []
    i = A

    while i <= B:
        integrate_r = integrate.quad(fun, A, i)
        i += step
        integra.append(integrate_r[0])

    return integra


def integr(f, A = 0, B = 0, step = 0.1, accuracy = 3):
    '''
    Функция интегрирования
    Parameters
    ----------
    f : string, required
    Функция, записанная без y =  зависящая от x
    A : float, optional
    Начало промежутка интегрирования
    B : float, optional
    Конец промежутка интегрирования
    step : float, optional
    Шаг интегрирования
    accuracy : int, float
    Точность интегрирования

    Returns
    -------
    x_coord : array of float
    Координаты по оси x
    integrals : array of float
    Значения интеграла
    f_x : array of float
    Значения исходной функции
    '''
    import check_function as ch_f
    f = ch_f.convertion(f)
    if 'x' not in f:
        print('Функция задана неверно. Попробуйте снова!')
        return (None, None, None)

    x_coord = [A]  # сюда записываем в каких точках считаем интеграл (при [-1, 1] и step=0.1 это будет -1, -0.9 и т.д.)
    integrals = [0]  # сюда записываем ответ
    x = A
    f_x = [eval(f)]
    i = A + step
    while i <= B:
        # здесь рассчитываем f(i)
        x = i
        x_coord.append(round(i, accuracy))
        try:
            f1 = eval(f)
            f_x.append(f1)
        except (ZeroDivisionError, ValueError):
            integrals.append(None)
            f_x.append(None)
            i += step
            continue

        x = i - step
        try:
            f2 = eval(f)
        except (ZeroDivisionError, ValueError):
            integrals.append(None)
            i += step
            continue

        # теперь алгоритм расчета интеграла ...
        D_F = step * (f1 + f2) / 2
        D_F = round(D_F, accuracy)

        if abs(D_F) >= inf:
            integrals.append(None)
        else:
            integrals.append(D_F)
        i += step

    return x_coord, integrals, f_x


def table_and_graph_for_integrate(title, x_coord, integrals, scpy, step, accuracy, f_x):
    """
        Строим график и сравниваем эффективность функции
        Parameters
        ----------
        title : string, required
            Функция, записанная в виде строки
        x_coord : array of float, required
            Координаты по оси x
        integrals: array of float, required
            Значения интеграла функции от x, посчитанные нашим алгоритмом
        scpy : array of float, required
            Значения интеграла функции от x, посчитанные методами scipy
        step : float, optional
            Шаг интегрирования
        accuracy : int, required
            Задаёт точность подсчёта значений после запятой
        f_x : array of float, required
            Значения функции, по которой считаем интеграл

        Returns
        -------
        Строит график сравнения значений Превообразных функций
        Выходные параметры отсутствуют

        """

    mytable = PrettyTable()
    mytable.title = title
    mytable.add_column("N", [i for i in range(1, len(x_coord) + 1)])
    mytable.add_column("x", x_coord)
    for i in range(1, len(integrals)):
        try:
            integrals[i] += integrals[i - 1]
        except TypeError:
            integrals[i] = integrals[i]
    mytable.add_column("F(x)", integrals)

    dlt = [0] * len(x_coord)
    # вычисляем дельту
    for l in range(len(x_coord)):
        if integrals[l] is None or scpy[l] is None:
            dlt[l] = '---'
        else:
            dlt[l] = abs(scpy[l] - integrals[l])

    for i in range(len(scpy)):
        if scpy[i] is None or dlt[i] == '---':
            continue
        scpy[i] = round(scpy[i], accuracy)
        dlt[i] = round(dlt[i], accuracy)
    print(sum(dlt))
    # Нужно добавить F(x)сущ и DELTA(F)

    mytable.add_column("F(x)сущ", scpy)
    mytable.add_column("DELTA(F)", dlt)
    print(mytable)

    # Строим график
    fig, ax = plt.subplots(nrows=1, ncols=2)
    ax[0].plot(x_coord, integrals, 'co-', label='Наш интеграл')
    ax[0].plot(x_coord, scpy, 'r--', label='Чужой интеграл')
    ax[0].set(xlabel='Ось абцисс x', ylabel="Значения интеграла F(x)")
    ax[0].legend(loc='upper left')

    ax[1].plot(x_coord, f_x, 'b', label='Функция')
    ax[1].set(xlabel='Ось абцисс x', ylabel="Значения функции f(x)")
    ax[1].legend(loc='upper left')

    plt.title(f'График интеграла от ({title})', loc='center', pad=10)
    # ax.grid(axis = 'both
    # plt.subplots_adjust(wspace=4, hspace=0)
    fig.set_figwidth(12)
    fig.set_figheight(6)
    plt.show()


