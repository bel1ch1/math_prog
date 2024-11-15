import random

def create_board(size):
    return [['~' for _ in range(size)] for _ in range(size)]

def print_board(board):
    print("  " + " ".join(str(i) for i in range(len(board))))
    for i, row in enumerate(board):
        print(i, " ".join(row))

def place_ships(board, num_ships):
    ships_placed = 0
    while ships_placed < num_ships:
        x = random.randint(0, len(board) - 1)
        y = random.randint(0, len(board) - 1)
        if board[x][y] != 'S':  # Проверяем, что корабль не установлен на это место
            board[x][y] = 'S'
            ships_placed += 1

def make_guess(board, guess):
    x, y = guess
    if board[x][y] == 'S':
        board[x][y] = 'X'  # Попадание
        return True
    elif board[x][y] == '~':
        board[x][y] = 'O'  # Промах
        return False
    return None  # Повторный выстрел

def main():
    size = 6
    num_ships = 3
    board = create_board(size)
    place_ships(board, num_ships)

    print("Добро пожаловать в игру 'Морской бой'!")
    turns = 0
    hits = 0

    while hits < num_ships:
        print_board(board)
        guess = input("Введите координаты для выстрела (формат: x y): ")
        try:
            x, y = map(int, guess.split())
            if x < 0 or x >= size or y < 0 or y >= size:
                print("Координаты вне поля. Попробуйте снова.")
                continue
            result = make_guess(board, (x, y))
            if result is True:
                print("Попадание!")
                hits += 1
            elif result is False:
                print("Промах!")
            else:
                print("Вы уже стреляли в эту клетку. Попробуйте снова.")
            turns += 1
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите координаты в формате 'x y'.")

    print("Поздравляем! Вы потопили все корабли за", turns, "выстрелов.")

if __name__ == "__main__":
    main()
