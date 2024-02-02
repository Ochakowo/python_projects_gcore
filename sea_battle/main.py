from player import Player
from field import Field

if __name__ == "__main__":

    # Выбор режима игры: "бот с ботом" или "игрок с ботом"
    print("Выберите режим игры: \n 1. Игрок с ботом \n 2. Бот с ботом")
    game_mode = int(input("Введите номер режима (1 или 2): "))

    if game_mode == 1:
        player_name = input("Введите имя игрока: ")
        player_board = Field(player_name)
        bot_board = Field("Бот")
        bot_board.set_bot_ships()
        player_board.set_player_ships()
        player = Player(player_name, bot_board)
        bot = Player("Бот", player_board)
        while True:
            if player.game_player():
                print("Player win")
                break
            if bot.game_bot():
                print("Bot win")
                break
    elif game_mode == 2:
        bot_board = Field("Бот1")
        bot_board1 = Field("Бот2")
        bot_board.set_bot_ships()
        bot_board1.set_bot_ships()
        bot = Player('Бот1', bot_board1)
        bot1 = Player("Бот2", bot_board)
        while True:
            if bot.game_bot():
                print("Bot1 win")
                break
            if bot1.game_bot():
                print("Bot2 win")
                break
    else:
        print("Неверный выбор. Выберите 1 или 2.")

