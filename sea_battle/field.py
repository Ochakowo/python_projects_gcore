import random
from enums import ShootResult


class Field:
    size = 10
    ship_lengths = {40: 4, 30: 3, 31: 3, 20: 2, 21: 2, 22: 2, 10: 1, 11: 1, 12: 1, 13: 1}

    def __init__(self, player_name):
        """Создаем пустое поле 10x10, сюда же передаём имена игроков (бота)"""
        self.board = [['_'] * self.size for _ in range(self.size)]
        self.player_name = player_name

    def display_board(self, show_board=False):
        """Выводим текущее состояние поля, создаём копию доски для отображения"""
        copy_board = [row.copy() for row in self.board]
        for i, row in enumerate(copy_board):
            for j, cell in enumerate(row):
                for key in self.ship_lengths.keys():
                    if cell == str(key):
                        copy_board[i][j] = "S"

        print(f"\nИгровое поле {self.player_name}:")
        print("   A B C D E F G H I J")
        for i, row in enumerate(copy_board, start=1):
            print(f"{i:>2} {' '.join(row if show_board
                                     else [cell if cell in ('0', 'K', 'X')
                                           else '_' for cell in row])}")

    def set_player_ships(self):
        """Устанавливаем корабль на поле игрока, проверяем поле ввода на корректность ввода"""
        count = 0
        for length in self.ship_lengths.values():
            print(f"\n{self.player_name}, установите {length}-палубный корабль")
            while True:
                position = input("Введите координаты и направление (H - горизонтально, V - вертикально). "
                                 "Например, A1H: ").upper()
                if len(position) not in (3, 4) or " " in position:
                    print("Неверный ввод. Пожалуйста, попробуйте еще раз.")
                    continue
                col, *row, direction = " ".join(position).split()
                row = "".join(row)
                if (col not in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
                        or row.isnumeric() is False or int(row) not in range(1, 11)):
                    print("Неверный ввод координат. Пожалуйста, попробуйте еще раз.")
                    continue
                if direction not in ('H', 'V'):
                    print("Неверное значение направления. Пожалуйста, попробуйте еще раз.")
                    continue
                col, row = ord(col) - ord('A'), int(row) - 1
                if self.__check_set_ship(row, col, length, direction):
                    self.__place_ship(row, col, length, direction, count)
                    self.display_board(show_board=True)
                    count += 1
                    break
                else:
                    print("Невозможно установить корабль в данных координатах. Пожалуйста, попробуйте еще раз.")

    def set_bot_ships(self):
        """Автоматически расставляем корабли для бота в рандомные ячейки"""
        count = 0
        for length in self.ship_lengths.values():
            while True:
                col = random.randint(0, self.size - 1)
                row = random.randint(0, self.size - 1)
                direction = random.choice(['H', 'V'])
                if self.__check_set_ship(row, col, length, direction):
                    self.__place_ship(row, col, length, direction, count)
                    count += 1
                    break

    def __check_set_ship(self, row: int, col: int, length: int, direction: str):
        """Проверяем, можно ли установить корабль в данном направлении (с учетом границ поля) и нет ли
        соседних кораблей в радиусе одной ячейки"""
        if direction == 'H':
            if col + length > self.size:
                return False
            for i in range(length):
                if not self.check_cell(row, col + i):
                    return False
                for j in range(-1, 2):
                    for k in range(-1, 2):
                        new_row, new_col = row + j, col + i + k
                        if (0 <= new_row < self.size and 0 <= new_col < self.size
                                and self.board[new_row][new_col].isnumeric()):
                            return False
        elif direction == 'V':
            if row + length > self.size:
                return False
            for i in range(length):
                if not self.check_cell(row + i, col):
                    return False
                for j in range(-1, 2):
                    for k in range(-1, 2):
                        new_row, new_col = row + i + j, col + k
                        if (0 <= new_row < self.size and 0 <= new_col < self.size
                                and self.board[new_row][new_col].isnumeric()):
                            return False
        return True

    def __place_ship(self, row: int, col: int, length: int, direction: str, count):
        """Устанавливаем корабль на поле в каждой ячейке согласно длине корабля"""
        key = list(self.ship_lengths.keys())[count]
        for i in range(length):
            if direction == 'H':
                self.__set_cell(row, col + i, str(key))
            elif direction == 'V':
                self.__set_cell(row + i, col, str(key))

    def check_cell(self, row: int, col: int):
        """Проверяем границы поля и текущее состояние ячейки"""
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] not in ['0', 'K', 'X']

    def __set_cell(self, row: int, column: int, value):
        """Меняем значение "_" ячейки на ключ из ship_lengths"""
        self.board[row][column] = value

    def receive_shot(self, row: int, col: int):
        """Обработка выстрела и возвращение результата (попадание, промах и т. д.)"""
        if self.board[row][col] == '_':
            self.board[row][col] = '0'
            return ShootResult.MISS
        else:
            hit = str(self.board[row][col])
            self.board[row][col] = 'X'
            if hit not in sum(self.board, []):
                self.__obvodka_kill_ship(row, col)
                return ShootResult.KILL
            return ShootResult.HIT

    def __obvodka_kill_ship(self, row, col):
        """Рекурсивно вокруг уничтоженного корабля перезаписывает пустые ячейки на 0. Х перезаписывает на К"""
        self.board[row][col] = 'K'
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1)]
        for r, c in directions:
            new_row, new_col = row + r, col + c
            if (0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0])
                    and self.board[new_row][new_col] == '_'):
                self.board[new_row][new_col] = '0'
            if (0 <= new_row < len(self.board) and 0 <= new_col < len(self.board[0])
                    and self.board[new_row][new_col] == 'X'):
                self.board[new_row][new_col] = 'K'
                self.__obvodka_kill_ship(new_row, new_col)

    def is_game_over(self):
        """Если на поле K встречается 20 раз, значит все корабли на поле уничтожены"""
        if (sum(self.board, []).count('K')) == 20:
            print("Game over")
            return True
        return False
