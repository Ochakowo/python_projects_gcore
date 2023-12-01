def factorial_generator() -> int:
    """
    Генератор для вычисления факториала
    """
    result = 1
    number = 0
    while True:
        yield result
        number += 1
        result *= number


def increase_exponentiation() -> int:
    """
    Замыкание для возведения в степень
    """
    exp = 0

    def increase(start):
        nonlocal exp
        result = start ** exp
        exp += 1
        return result

    return increase


increase_exp = increase_exponentiation()
factorial_gen = factorial_generator()

taylor_series = lambda x, n: sum(increase_exp(x) / next(factorial_gen) for i in range(n))

x = 1  # Степень
n = 4  # Количество членов ряда

print(taylor_series(x, n))
