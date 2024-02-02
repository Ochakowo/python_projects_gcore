import csv


def create_maze_field(csv_maze_file) -> list:
    """
    Чтение csv файла. Открываем файл с указанием разделителя. Преобразуем данные в двумерный массив, разбив каждое
    число файла на отдельные ячейки. Перезаписываем ячейку финиша: нижняя правая пустая ячейка == 'F'.
    :param csv_maze_file: Входящий файл с лабиринтом в формате csv
    :return: Двумерный массив
    """
    with open(csv_maze_file) as f:
        reader = csv.reader(f, delimiter=';')
        maze_field = [_ for _ in reader]
    maze_field[-2][-2] = 'F'
    return maze_field


def check_values_nearby(field: list, row: int = 1, col: int = 1) -> bool:
    """
    Проверка соседних значений
    :param field: Наш лабиринт из csv
    :param row: Положение ячейки начала
    :param col: Положение ячейки начала
    """
    if field[row][col] == '0':
        field[row][col] = '*'
        if field[row][col + 1] in ['0', 'F'] and check_values_nearby(field, row, col + 1):
            return True
        if field[row + 1][col] in ['0', 'F'] and check_values_nearby(field, row + 1, col):
            return True
        if field[row][col - 1] in ['0', 'F'] and check_values_nearby(field, row, col - 1):
            return True
        if field[row - 1][col] in ['0', 'F'] and check_values_nearby(field, row - 1, col):
            return True
        else:
            field[row][col] = '0'

    if field[row][col] == 'F':
        field[row][col] = '*'
        return True


maze_file = 'maze.csv'
maze_field = create_maze_field(maze_file)
check_values_nearby(maze_field)
for line in maze_field:
    print(*line)
