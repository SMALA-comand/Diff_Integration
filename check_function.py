import math
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
