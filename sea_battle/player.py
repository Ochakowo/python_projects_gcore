import random
from enums import ShootResult


class Player:
    shoot_stack = []

    def __init__(self, player_name, opponent_board):
        self.current_player_name = player_name
        self.opponent_board = opponent_board

    def game_player(self):
        while True:
            target = input(f"\n{self.current_player_name}, введите координаты для выстрела (например, A1): ").upper()
            if len(target) not in (2, 3) or " " in target:
                print("Неверный ввод. Пожалуйста, попробуйте еще раз.")
                continue
            col, *row = " ".join(target).split()
            row = "".join(row)
            if (col not in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
                    or row.isnumeric() is False or int(row) not in range(1, 11)):
                print("Неверный ввод координат. Пожалуйста, попробуйте еще раз.")
                continue
            col, row = ord(col) - ord('A'), int(row) - 1

            if not self.opponent_board.check_cell(row, col):
                print("Эта клетка уже была атакована. Пожалуйста, выберите другую.")
                continue

            result = self.opponent_board.receive_shot(row, col)
            self.opponent_board.display_board()

            match result:
                case ShootResult.HIT:
                    print(f"\n{self.current_player_name}, попадание в клетке {target}!")
                    continue
                case ShootResult.KILL:
                    print(f"\n{self.current_player_name}, ты затопил корабль!")
                    if self.opponent_board.is_game_over():
                        return True
                    continue
                case ShootResult.MISS:
                    print(f"\n{self.current_player_name}, промах в клетке {target}!")
                    break
            return False

    def game_bot(self):
        while True:
            if len(self.shoot_stack) == 0:
                row = random.randint(0, self.opponent_board.size - 1)
                col = random.randint(0, self.opponent_board.size - 1)

            if len(self.shoot_stack) == 2:
                row, col = self.shoot_stack[-2:]
                directions = [[row, col + 1], [row, col - 1], [row + 1, col], [row - 1, col]]
                target = []
                for new_row, new_col in directions:
                    target.append((new_row, new_col))
                row, col = random.choice(target)

            if len(self.shoot_stack) > 2:
                rows, cols = self.shoot_stack[0::2], self.shoot_stack[1::2]
                if cols.count(cols[0]) == len(cols):
                    rows.sort(reverse=True)
                    if len(self.shoot_stack) == 6:
                        del rows[1]
                    new_row = [x + 1 if i % 2 == 0 else x - 1 for i, x in enumerate(rows)]
                    target = []
                    for i in range(len(new_row)):
                        target.append((new_row[i], cols[0]))
                    row, col = random.choice(target)
                if rows.count(rows[0]) == len(rows):
                    cols.sort(reverse=True)
                    if len(self.shoot_stack) == 6:
                        del cols[1]
                    new_col = [x + 1 if i % 2 == 0 else x - 1 for i, x in enumerate(cols)]
                    target = []
                    for i in range(len(new_col)):
                        target.append((rows[0], new_col[i]))
                    row, col = random.choice(target)

            if not self.opponent_board.check_cell(row, col):
                continue

            result = self.opponent_board.receive_shot(row, col)
            self.opponent_board.display_board(show_board=True)

            match result:
                case ShootResult.HIT:
                    self.shoot_stack.extend([row, col])
                    print(f"\n{self.current_player_name} попал в клетку ({chr(col + ord('A'))}{row + 1})!")
                    continue
                case ShootResult.KILL:
                    self.shoot_stack.clear()
                    print(f"\n{self.current_player_name} уничтожил корабль в клетке "
                          f"({chr(col + ord('A'))}{row + 1})!")
                    if self.opponent_board.is_game_over():
                        return True
                    continue
                case ShootResult.MISS:
                    print(f"\n{self.current_player_name} промахнулся в клетке "
                          f"({chr(col + ord('A'))}{row + 1})!")
                    break
            return False
