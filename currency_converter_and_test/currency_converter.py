import requests

API_URL = 'https://www.cbr-xml-daily.ru/latest.js'
currencies: dict = {}


def get_currencies_from_api() -> dict:
    """ Функция получает курсы валют через api.
        Возвращает список словарь с курсами валют, где ключ это код валюты,
        значение — курс обмена 1 рубля на эту валюту
    """
    currs: dict = {}
    res = requests.get(API_URL)

    if res.status_code == 200:
        json = res.json()
        for rate in json['rates']:
            currs[rate] = float(json['rates'][rate])
    if len(currs) > 0:
        write_currencies_to_file(currs)

    return currs


def write_currencies_to_file(rates: dict):
    """ Сохраняет словарь с курсами валют в файл в формате ключ значение через пробел
        каждая пара с новой строки
    """
    try:
        with open("currencies.txt", "w") as curs_w:
            for code in rates:
                curs_w.write(f"{code} {rates[code]}\n")
    except PermissionError:
        print("Access denied. Can't write to file")


def to_rub(value: float, code: str, currencies: dict) -> float:
    """ Конвертирует валюту в рубли
        value - количество исходной валюты
        code - код исходной валюты
        currencies - словарь с курсами валют
    """
    if code in currencies.keys():
        return value / currencies[code]
    else:
        return 0


def from_rub(value: float, code: str, currencies: dict) -> float:
    """ Конвертирует валюту и рублей
            value - количество рублей
            code - код целевой валюты
            currencies - словарь с курсами валют
        """
    if code in currencies.keys():
        return value * currencies[code]
    else:
        return 0


def calc_result(query: str, currencies: dict) -> str:
    """ Парсит строку и вычисляет результат, возвращает вычисленное значение в заданном формате"""
    value, codes = query.split(" ", maxsplit=1)
    value = float(value)
    from_code, to_code = codes.split(">", maxsplit=1)
    from_code = from_code.strip().upper()
    to_code = to_code.strip().upper()

    if from_code != "RUB":
        rub_value = to_rub(value, from_code, currencies)
    else:
        rub_value = value

    if to_code != "RUB":
        res_value = from_rub(rub_value, to_code, currencies)
    else:
        res_value = rub_value

    return f"Result: {value:_.2f} {from_code} = {res_value:_.2f} {to_code}".replace("_", " ")


if __name__ == '__main__':

    try:
        with open("currencies.txt") as curs:
            for line in curs:
                code, value = line.split(" ", maxsplit=1)
                currencies[code] = float(value)
    except FileNotFoundError:
        currencies = get_currencies_from_api()

    if len(currencies) > 0:
        i = 0
        for code in currencies:
            print(f"{code}: {currencies[code]:9.4f}", end="  |  ")
            i += 1
            if i == 4:
                i = 0
                print("")
        print("\n")

        while True:
            print("Query format: 100 USD>RUB")
            query = input("Input your query: ")
            if query.strip() == "" or query.strip() == "0":
                break
            print(calc_result(query, currencies), "\n")
