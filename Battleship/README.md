# Игра "Морской бой"
____
«Морской бой» — игра для двух участников, в которой игроки по очереди называют координаты на неизвестной им карте соперника. Если у соперника по этим координатам имеется корабль (координаты заняты), то корабль или его часть «топится», а попавший получает право сделать ещё один ход. Цель игрока — первым потопить все корабли противника. При размещении корабли не могут касаться друг друга сторонами и углами.
Поле игры имеет размер 6х6, второго игрока заменяет ИИ.
При запуске игра описывает обозначения использующиеся на поле и правила ввода значений. Также запрашиваются имя игрока и метод размещения кораблей (ручное или авторазмещение).

![image](https://user-images.githubusercontent.com/120253513/213887109-e1a4f611-221e-4a09-bc5a-e9465b3cd689.png)

Если выбрано ручное размещение кораблей, то описываются правила по которым это происходит, после этого поочередно запрашиваются корабли, начиная с наибольшего с возможность сброса к состоянию пустого поля.

![image](https://user-images.githubusercontent.com/120253513/213887345-ba324f8c-b8c7-476d-acb1-da1f797e5e36.png)

После завершения расстановки кораблей игрок и ИИ попеременно ходят указывая координаты выстрела, итог каждого хода отрисовывается. В конце игры выводится победитель.
![image](https://user-images.githubusercontent.com/120253513/213887623-a912aa92-5c64-43a3-950a-4687c38cba96.png)


В отдельные классы выведены:
+ Игрок, компьютер (с методами запроса координат выстрелов) и их родительский класс с методом обработки этих запросов
+ Игровое поле с методами позволяющими заполнить его перед началом игры
+ Получение данных о корабле с последующим получением всех его палуб
+ Исключения

Для удобства проверки программы в 246 строке можно computer.board_to_print заменить на computer.board_pl
