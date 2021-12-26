import math
import random
import matplotlib.pyplot as plt
from prettytable import PrettyTable
from scipy.misc import derivative
import scipy.integrate as integrate

# Константы
inf = 10 ** 12

#Преобразование функции
def convertion(fun):
    '''
    Преобразует функцию к нужному нам виду
    Parameters
    ----------
    fun : str, required
        Функция без у=, записанная в виде строки

    Returns
    -------
    func : str
    Строка, для которой работает функция eval
    '''
    func = None
    while func is None:
        if '^' in fun:
            fun = fun.replace('^', '**')
        fun = fun.lower()

        for_title = fun
        plan = ['e', 'pi', 'sin', 'cos', 'tan', 'log']
        dict_replace = {i: 'math.' + i for i in plan}
        dict_replace['tg'] = 'math.tan'
        dict_replace['ln'] = 'math.log'
        dict_replace['ctan'] = '1/math.tan'
        dict_replace['ctg'] = '1/math.tan'

        for item in dict_replace:
            if item in fun:
                fun = fun.replace(item, dict_replace[item])

        # проверяем есть ли лишние буквы
        alphabet0 = ['b', 'd', 'f', 'j', 'k', 'q', 'r', 'u', 'v', 'w', 'y', 'z']
        alphabet1 = ['t', 'a', 'p', 'i', 's', 'n', 'c', 'o', 'l', 'g', 'h', 'm']
        alphabet2 = {
            't': ['math', 'tan'], 'a': ['math', 'tan'], 'p': ['pi'], 'i': ['sin', 'pi'],
            's': ['sin', 'cos'], 'n': ['tan', 'sin'], 'c': ['cos'], 'o': ['cos', 'log'],
            'l': ['log'], 'g': ['log'], 'h': ['math'], 'm': ['math']
        }
        for letter in range(12):
            if alphabet0[letter] in fun:
                print('У вас есть лишние переменные/символы букв')
                break
            let = alphabet1[letter]
            if fun.count(let) > sum(list(map(lambda x: fun.count(x), alphabet2[let]))):
                print('У вас есть лишние переменные/символы букв')
                break
        else:  # сюда заходим, если for закончился без break
            x = 1  # проверяем деление на ноль, синтаксис, ошибку вызову мат функций, ошибку значений мат функций
            flag = False
            try:
                eval(fun)
            except (SyntaxError, NameError):
                print('Синтаксическая ошибка!')
                flag = True
            except ValueError:
                if ValueEr(fun):
                    print('Скорее всего в вашей формуле статическая ошибка в логарифме, исправьте её')
                    flag = True
            except ZeroDivisionError:
                if ZeroDiv(fun):
                    print('Скорее всего в вашей формуле статическое деление на ноль')
                    flag = True
            except TypeError:
                print('Неправильное использование мат. функций (проверьте ваши логарифмы и тригонометрические ф-ции)')
                flag = True

            if flag:
                func = None
            if not flag:
                func = fun
    return func

#Дифференцирование

def diff(f, A = 0, B = 0, step = 0.1, accuracy = 3, graphics = 0):
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
    graphics : bool, optional
    Отмечает, нужен ли вывод графика функции
    Returns
    -------
    x_coord : array of float
    Координаты по оси x
    derivatives : array of float
    Значения производной
    f_x : array of float
    Значения исходной функции
    '''
    f = convertion(f)
    if 'x' not in f:
        print('Функция задана неверно. Попробуйте снова!')
        return(None, None, None)
    title = 'Производная от ' + f
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
    if graphics == 1:
        table_and_graph(title, x_coord, derivatives, accuracy, f_x)
    return x_coord, derivatives, f_x

#Интегрирование

def integr(f, A = 0, B = 0, step = 0.1, accuracy = 3, graphics = 0):
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
    graphics : bool, optional
    Отмечает, нужен ли вывод графика функции
    Returns
    -------
    x_coord : array of float
    Координаты по оси x
    integrals : array of float
    Значения интеграла
    f_x : array of float
    Значения исходной функции
    '''
    f = convertion(f)
    if 'x' not in f:
        print('Функция задана неверно. Попробуйте снова!')
        return (None, None, None)
    title = 'Интеграл от ' + f
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
    if graphics == 1:
        table_and_graph(title, x_coord, integrals, accuracy, f_x)
    return x_coord, integrals, f_x


def table_and_graph(title, x_coord, f_changed, accuracy, f_x):
    """
            Строим график вычисленной функции
            Parameters
            ----------
            title : string, required
                Функция, записанная в виде строки
            x_coord : array of float, required
                Координаты по оси x
            f_changed: array of float, required
                Значения вычисленной функции от x, посчитанные нашим алгоритмом
            accuracy : int, required
                Задаёт точность подсчёта значений после запятой
            f_x : array of float, required
                Значения исходной функции

            Returns
            -------
            Строит график сравнения значений производных функций
            Выходные параметры отсутствуют

            """
    for i in range(len(f_changed)):
        f_changed[i] = round(f_changed[i], accuracy)

    mytable = PrettyTable()

    mytable.title = title
    mytable.add_column("N", [i for i in range(1, len(x_coord) + 1)])
    mytable.add_column("x", x_coord)
    mytable.add_column("f_counted(x)", f_changed)

    # Нужно добавить f'(x)сущ и del(f)

    print(mytable)

    # Строим график
    fig, ax = plt.subplots(nrows=1, ncols=2)
    plt.title(f'Графики функции ({title})', loc='left')
    ax[0].plot(x_coord, f_changed, 'bo-', label='Вычисленная функция')
    ax[0].set(xlabel='Ось абцисс x', ylabel="Значения f_counted(x)")
    ax[0].legend(loc='upper left')

    ax[1].plot(x_coord, f_x, 'b', label='Функция')
    ax[1].set(xlabel='Ось абцисс x', ylabel="Значения функции f(x)")
    ax[1].legend(loc='upper left')


    # ax.grid(axis = 'both')
    # plt.subplots_adjust(wspace=4, hspace=0)
    fig.set_figwidth(12)
    fig.set_figheight(6)
    plt.show()


#Отлов ошибок

def ZeroDiv(fun):
    count = 0
    for j in range(20):
        x = random.randint(-100001, 100001)
        try:
            eval(fun)
        except ZeroDivisionError:
            count += 1
        except ValueError:
            continue
    if count == 20:
        return True
    return False


def ValueEr(fun):
    count = 0
    for j in range(20):
        x = random.randint(-100001, 100001)
        try:
            eval(fun)
        except ValueError:
            count += 1
        except ZeroDivisionError:
            continue
    if count == 20:
        return True
    return False