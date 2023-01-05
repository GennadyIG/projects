from random import randint


def print_xo():  # Печать поля
    print(' ', *list(range(size)), 'y')
    for i, row in enumerate(xo):
        print(i, *row)
    print('x\n')


def player_move(f):  # Ход игрока
    while True:
        coordinates = input(f"Ход игрока {users_move}: ").split()
        if not ''.join(coordinates).isdigit():
            print('Введенные значения не являются цифрами, попробуйте еще раз.')
            continue
        coordinates_list = list(map(int, coordinates))
        if len(coordinates_list) != 2:
            print(f'Введено не 2 координаты, повторите ввод.')
            continue
        if not 0 <= coordinates_list[0] < size or not 0 <= coordinates_list[1] < size:
            print('Нет ячейки с такими координатами, попробуйте еще раз.')
            continue
        if f[coordinates_list[0]][coordinates_list[1]] != '-':
            print('Ячейка занята, попробуйте еще раз.')
            continue
        else:
            return coordinates_list[0], coordinates_list[1]


def step_of_computer(f):  # Выбор координат компьютером
    for i in win:  # Поиск выигрышных комбинаций
        n = 0
        for j, k in i:
            if f[j][k] == token[users[1]]:
                n += 1
        if n == (size - 1):
            for j, k in i:
                if f[j][k] == '-':
                    return j, k
    for i in win:  # Поиск проигрышных комбинаций
        m = 0
        for j, k in i:
            if f[j][k] == token[users[0]]:
                m += 1
        if m == (size - 1):
            for j, k in i:
                if f[j][k] == '-':
                    return j, k
    while True:
        j = randint(0, size - 1)
        k = randint(0, size - 1)
        if f[j][k] == '-':
            return j, k


def result(value, f):  # Проверка на выигрыш
    for i in win:
        n = 0
        for j, k in i:
            if f[j][k] == value:
                n += 1
        if n == size:
            for j, k in i:
                f[j][k] = f'\033[32m{value}\033[0m'
            if value == token[users[0]]:
                print(f'Выиграл игрок {users[0]}!', users[0])
                return False
            else:
                print(f'Выиграл игрок {users[1]}!', users[1])
                return False
    return True


# Выбор количества игроков и контроль введенного значения
def numbers_of_players():
    while True:
        number_of_players = input('Сколько человек будут играть? (1 или 2): ')
        if number_of_players.isdigit() and 1 <= int(number_of_players) <= 2:
            if int(number_of_players) == 2:
                return [input('Введите имя первого игрока: '), input('Введите имя второго игрока: ')],\
                       int(number_of_players)
            else:
                return [input('Введите имя игрока: '), 'computer'], int(number_of_players)
        else:
            print('Введено некорректное значение, попробуем снова.')


# Размер игрового поля
def size_xo():
    while True:
        size_input = input('Введите размер стороны игрового поля (минимальный размер 3): ')
        if size_input.isdigit() and int(size_input) >= 3:
            return int(size_input)
        else:
            print('Введено некорректное значение, попробуем снова.')


size = size_xo()
users, players = numbers_of_players()
token = {users[0]: 'x', users[1]: 'o'}
users_move = None  # Переменная хранящая игрока, который сейчас ходит
score_user = [0, 0]
while True:
    count = 0  # Счетчик ходов
    # Игровое поле
    xo = [['-' for _ in range(size)] for i in range(size)]
    # Выигрышные комбинации
    win = [*list([[i, j] for i in range(size)] for j in range(size)),
           *list([[j, i] for i in range(size)] for j in range(size)),
           *list([[[i, i] for i in range(size)]]),
           *list([[[i, size - i - 1] for i in range(size)]])
           ]
    condition = True  # Условие основного цикла
    print_xo()
    print('Вводите координаты через пробел (x y)')
    while condition:
        # Выбор игрока
        if count % 2 == 0:
            users_move = users[0]
        else:
            users_move = users[1]
        # Ход компьютера / игрока
        if users_move == 'computer' and players == 1:
            x, y = step_of_computer(xo)
            xo[x][y] = token[users_move]
            print(f'Ход игрока computer: {x} {y}')
        else:
            x, y = player_move(xo)
            xo[x][y] = token[users_move]
        # Условия срабатывания проверки выигрыша и заполнения поля
        count += 1
        if count > (size - 1) * 2:
            condition = result(token[users_move], xo)
            if not condition and users_move == users[0]:
                score_user[0] += 1
            elif not condition and users_move == users[1]:
                score_user[1] += 1
        print_xo()
        if count == size ** 2 and condition:
            print('Ничья')
            break
    print(f'Счет этой сессии игр: {users[0]} {score_user[0]} : {score_user[1]} {users[1]}')
    while True:
        new_game = input(f'Хотите сыграть еще раз? (y/n): ')
        if new_game in ['n', 'y']:
            break
        else:
            print('Ошибка ввода, попробуйте еще раз.')
    if new_game == 'n':
        break
