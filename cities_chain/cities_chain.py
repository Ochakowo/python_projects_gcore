import time
import sys


sys.setrecursionlimit(3000)
start_time = time.time()


def read_file(file):
    with open(file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]
    cities = list(lines)
    return cities


def max_city_chain(cities: list) -> list:
    """
    Эта функция делает словарь городов, где каждый город связан с другим первой буквой его имени с последней
    буквой имени другого города
    Пример: {'ясногорск': ['краснослободск', 'карасук', 'кубинка', 'комсомольск', 'колпашево'], и т.д.}
    :param cities: наши города
    :return самая длинная цепочка городов из всех возможных
    """
    dict_city = {}
    for city in cities:
        # cоздаем пустой список для текущего города
        dict_city[city] = []
    for city in cities:
        # заполняем список с городами на последнюю букву текущего город
        for other_city in cities:
            if city != other_city and city[-1] == other_city[0]:
                # Если текущий город не равен другому городу и последняя буква текущего города совпадает с
                # первой буквой города
                dict_city[city].append(other_city)
                # добавляем город в список текущего города
    visited = {
        city: False for city in cities
    }  # город из списка cities отмечаю как непосещенный
    # {'макушино': False, 'краснослободск': False, и т.д.}
    max_chain = []
    for city in cities:
        chain = find_max_city_chain(dict_city, city, visited)
        if len(chain) > len(max_chain):
            max_chain = chain
    return max_chain


def find_max_city_chain(dict_city: dict, city: str, visited: dict, chain=None) -> list:
    """
    Функция рекурсивно проходит по всем городам, которые в листе текущего города
    :param dict_city: словарь, где ключи - города, а значения - список городов
    :param city: текущий город
    :param visited: словарь, отслеживающий, был ли город уже посещен
    :param chain: наша цепочка городов
    :return цепочка городов, начиная с данного города
    """
    if chain is None:
        chain = []
    visited[city] = True  # добавляем отметку, что текущий город посещенный
    chain.append(city)  # добавляем текущий город в текущую цепочку
    max_chain = (
        chain.copy()
    )  # создаем копию текущей цепочки и сохраняем ее как самую длинную цепочку
    for next_city in dict_city[city]:
        if not visited[next_city]:
            # вызываем рекурсивно функцию find_longest_city_chain для поиска цепочки с соседнего города
            new_chain = find_max_city_chain(dict_city, next_city, visited, chain)
            if len(new_chain) > len(max_chain):
                max_chain = new_chain

    visited[city] = False  # снимаем отметку о посещении с текущего города
    chain.pop()  # убираем его из текущей цепочки перед возвратом
    return max_chain


file = "cities60.txt"
cities = read_file(file)
result = max_city_chain(cities)
end_time = time.time()
timer = end_time - start_time

print(f"Максимально возможная цепочка: {result}")
print(f"Длина цепочки: {len(result)}")
print(f"Время выполнения кода: {timer / 60} минут")
