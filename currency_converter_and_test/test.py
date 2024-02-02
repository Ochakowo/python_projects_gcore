import os
import pytest
import time
from currency_converter import to_rub, write_currencies_to_file


@pytest.fixture
def currencies_fixture():
    """Фикстура возвращает словарь с курсами валют для теста test_to_rub"""
    return {'USD': 0.01, 'EUR': 0.009, 'UZS': 136.761}


@pytest.fixture
def fake_currencies_fixture():
    """Фикстура с фейковым словарём для теста test_write_currencies_to_read_only_file"""
    return {'USD': 0.02, 'EUR': 0.01, 'UZS': 139.96}


@pytest.fixture(scope="session", autouse=True)
def timer():
    """Фикстура которая посчитает время выполнения всех тестов. Вывод с опцией -s"""
    start_time = time.time()
    yield
    end_time = time.time() - start_time
    print(f"\nВремя выполнения всех тестов: {end_time:.2f} секунды")


@pytest.mark.parametrize("value, code, expected_result", [
    (1, 'USD', 100),
    (500, 'EUR', 20000),
    (10, 'BTC', 0),
    (2000, 'UZS', 15),
])
def test_to_rub(value, code, expected_result, currencies_fixture):
    """Тест для функции to_rub"""

    # Добавил слип для проверки работы фикстуры таймера
    # time.sleep(1)

    result = to_rub(value, code, currencies_fixture)
    assert result == expected_result, \
        f"Failed для {value} {code} в RUB. Ожидается: {expected_result}, Фактически: {result:.2f}"
    if 'BTC' in code:
        pytest.xfail("Такой валюты у нас нет")


def test_write_currencies_to_file(currencies_fixture):
    """Тест для функции write_currencies_to_file. Сохраняет словарь из фикстуры, проверяет его"""
    write_currencies_to_file(currencies_fixture)
    with open("currencies.txt", "r") as file:
        for line in file.readlines():
            code, value = line.split()
            assert code in currencies_fixture
            assert float(value) == currencies_fixture[code]


def test_write_currencies_to_read_only_file(currencies_fixture, fake_currencies_fixture):
    """Тест должен запускаться после test_write_currencies_to_file.
    Устанавливаем права на read-only, пробуем переписать на фейковый словарь, проверяем что файл не изменился."""
    os.chmod("currencies.txt", 0o444)

    # raises не ловит исключение из функции write_currencies_to_file, сделал через другой способ
    # with pytest.raises(PermissionError):
    #     write_currencies_to_file(fake_currencies_fixture)

    try:
        write_currencies_to_file(fake_currencies_fixture)
    except PermissionError:
        pass
    with open("currencies.txt", "r") as file:
        for line in file.readlines():
            code, value = line.split()
            assert code in currencies_fixture
            assert float(value) == currencies_fixture[code]
