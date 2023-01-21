from random import randint


class ExceptionGame(Exception):
    pass


class BoardOutException(ExceptionGame):
    def __str__(self):
        return "Введенных координат на доске нет"


class RepeatShotArea(ExceptionGame):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"


class DotBusy(ExceptionGame):
    def __str__(self):
        return "Точка занята"


class InvalidCoords(ExceptionGame):
    def __str__(self):
        return "Введено неверное количество координат"


class NotDigit(ExceptionGame):
    def __str__(self):
        return "Координаты должны быть цифрами"


class InvalidValue(ExceptionGame):
    def __str__(self):
        return "Неверное значение"


class Ship:
    def __init__(self, len_ship, x, y, direction):
        self.len_ship = len_ship
        self.x = x
        self.y = y
        self.direction = direction

    def dots(self):
        if self.direction == 0:
            ship_dots = [[self.x - 1, self.y - 1 + u] for u in range(self.len_ship)]
            return ship_dots
        else:
            ship_dots = [[self.x - 1 + u, self.y - 1] for u in range(self.len_ship)]
            return ship_dots


class Board:
    def __init__(self):
        self.field = []
        self.ships = []
        self.busy = []

    def add_ship(self, ship):
        ship_dots = ship.dots()
        for el in ship_dots:
            if el in self.busy or el[0] > 5 or el[1] > 5:
                return False
        self.ships.append(ship_dots)
        self.busy.extend(ship_dots)
        self.contour(ship_dots)
        for el in ship_dots:
            self.field[el[0]][el[1]] = chr(9617)
        return True

    def contour(self, ship):
        contour = [[-1, 1], [0, 1], [1, 1],
                   [-1, 0], [1, 0],
                   [-1, -1], [0, -1], [1, -1]]
        for el in contour:
            for dot in ship:
                if (x := [dot[0] + el[0], dot[1] + el[1]]) not in self.busy and 0 <= x[0] < 6 and 0 <= x[1] < 6:
                    self.busy.append(x)

    def random_board(self):
        while True:
            self.field = [['-'] * 6 for _ in range(6)]
            self.ships = []
            self.busy = []
            len_ships = [3, 2, 2, 1, 1, 1, 1]
            attempts = 0
            for i in range(len(len_ships)):
                while attempts < 20:
                    attempts += 1
                    ship = Ship(len_ships[i], randint(1, 6), randint(1, 6), randint(0, 1))
                    self.add_ship(ship)
                    if len(self.ships) == i + 1:
                        break
                else:
                    break
            self.busy = []
            return self.field

    def board_manual(self):
        while True:
            print('\nКоординаты первой палубы указываются через пробел в формате "х у",\n'
                  'корабль строится от этой точки вправо (для горизонтального направления необходимо указать 0)\n'
                  'или вниз (для вертикального направления необходимо указать 1)\n')
            self.field = [['-'] * 6 for _ in range(6)]
            self.ships = []
            self.busy = []
            len_ships = [3, 2, 2, 1, 1, 1, 1]
            for i in range(len(len_ships)):
                Draw(self.field, Player().board_to_print).print()
                print(f'Корабль, который предстоит расположить состоит из {len_ships[i]} палуб(ы)')
                while True:
                    try:
                        coords = input('Введите координаты первой палубы: ').split()
                        if not coords[0].isdigit() or not coords[1].isdigit():
                            raise NotDigit()
                        if len(coords) != 2:
                            raise InvalidCoords()
                        coords = list(map(int, coords))
                        if coords[0] not in list(range(1, 7)) or coords[1] not in list(range(1, 7)):
                            raise BoardOutException()
                    except ExceptionGame as e:
                        print(e)
                        continue
                    while True:
                        try:
                            direct = input('Задайте направление корабля: ')
                            if not direct.isdigit() or int(direct) not in [0, 1]:
                                raise InvalidValue()
                            direct = int(direct)
                            break
                        except ExceptionGame as e:
                            print(e)
                    ship = Ship(len_ships[i], coords[0], coords[1], direct)
                    if self.add_ship(ship):
                        break
                    else:
                        print('Корабли не должны соприкасаться или выходить за пределы доски')
                reset = input('Если необходимо сбросить расстановку введите любую букву,'
                              'если нет, то оставьте пустым или введите "0": ')
                if reset:
                    break
            else:
                self.busy = []
                return self.field


class Player:
    def __init__(self, name=None):
        self.board = Board()
        self.name = name
        self.shot = []
        self.board_to_print = [['-'] * 6 for _ in range(6)]

    def move(self, other):
        for ship in range(len(other.board.ships)):
            if self.shot in other.board.ships[ship]:
                other.board.busy.append(self.shot)
                other.board.ships[ship].remove(self.shot)
                if not other.board.ships[ship]:
                    other.board.ships.remove([])
                other.board_pl[self.shot[0]][self.shot[1]] = chr(9609)
                other.board_to_print[self.shot[0]][self.shot[1]] = chr(9609)
                if not len(other.board.ships):
                    exit(print(f'Игрок {self.name} выиграл!'))
                return True
        else:
            other.board.busy.append(self.shot)
            other.board_to_print[self.shot[0]][self.shot[1]] = chr(9642)
            other.board_pl[self.shot[0]][self.shot[1]] = chr(9642)
            return False


class AI(Player):
    def __init__(self, name):
        super().__init__(name)
        self.board_pl = self.board.random_board()

    def ask(self, other):
        while True:
            try:
                self.shot = [randint(0, 5), randint(0, 5)]
                if self.shot in other.board.busy:
                    raise RepeatShotArea
                break
            except ExceptionGame:
                continue
        return self.shot


class User(Player):
    def __init__(self, name, manual_filling: bool):
        super().__init__(name)
        if manual_filling:
            self.board_pl = self.board.board_manual()
        else:
            self.board_pl = self.board.random_board()

    def ask(self, other):
        while True:
            try:
                dot = input('Введите координаты выстрела: ').split()
                if not dot[0].isdigit() or not dot[1].isdigit():
                    raise NotDigit()
                self.shot = list(map(lambda x: int(x) - 1, dot))
                if len(self.shot) != 2:
                    raise InvalidCoords()
                if self.shot[0] not in list(range(0, 6)) or self.shot[1] not in list(range(0, 6)):
                    raise BoardOutException()
                if self.shot in other.board.busy:
                    raise RepeatShotArea()
                break
            except ExceptionGame as e:
                print(e)
                continue
        return self.shot


class Draw:
    def __init__(self, player, computer):
        self.player = player
        self.computer = computer

    def print(self):
        print('  ', *list(range(1, 7)), ' \t\t  ', *list(range(1, 7)), ' ', sep=' | ')
        for number, row in enumerate(list(zip(self.player, self.computer)), start=1):
            for i in row:
                print(number, ' | ', end='')
                print(*i, sep=' | ', end=' |\t\t')
            print()


class Game:
    @staticmethod
    def start():
        print(f'Игра "МОРСКОЙ БОЙ"\n\nОбозначения в игре:\n'
              f'"-" - неиспользованная ячейка\n"{chr(9617)}" - целая палуба корабля\n'
              f'"{chr(9609)}" - подбитая палуба корабля\n"{chr(9642)}" - промах\n\n'
              f'Координаты выстрела вводятся через пробел в формате "х у"\nУдачи в игре!\n')
        computer = AI('Computer')
        manual = bool(input('Как будем расставлять корабли?\n'
                            '(для автозаполнения ничего вводить не нужно, иначе любую букву): '))
        player = User(input('Назовите свое имя: '), manual)
        game_board = Draw(player.board_pl, computer.board_to_print)
        game_board.print()
        count = 0
        while True:
            if count % 2 == 0:
                current_user = player
                other_user = computer
            else:
                current_user = computer
                other_user = player
            print(f'Ход игрока {current_user.name}')
            print(f'Выстрел по координатам {list(map(lambda x: int(x) + 1, current_user.ask(other_user)))}')
            if current_user.move(other_user):
                print(f'Попадание! Игрок {current_user.name} стреляет еще раз.')
            else:
                count += 1
                print(f'Мимо! Ход переходит к игроку {other_user.name}.')
            game_board.print()


Game.start()
