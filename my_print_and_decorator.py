
def name_and_args_of_func(func):
    def wrapper(*args, **kwargs):
        """
        Декоратор принимает функцию в качестве аргумента и возвращает функцию, выводит необходимый принт, передаёт
        оригинальной функции аргументы
        :param args: Позиционные аргументы
        :param kwargs: Именованные аргументы
        """
        print(f"Запущена функция {func.__name__} с аргументами: {args} и {kwargs}.")
        return_value = func(*args, **kwargs)
        return return_value
    return wrapper


@name_and_args_of_func
def my_print(*args: any, sep=' ', end='\n') -> str:
    """
    Функция, которая полностью повторяет системный print
    :param args: Символы для вывода
    :param sep: Разделитель
    :param end: Знак конца строки
    :return: Строка с результатом принта
    """
    display = sep.join(args) + end
    return display


print(my_print('hello', 'world', sep='.', end='!!!!!'))
