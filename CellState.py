from enum import Enum
class CellState(Enum):
    FOG_OF_WAR = 0
    EMPTY_CELL = 1  #Пустая клетка. Видна хозяину поля
    HIT_EMPTY_CELL = -1  #Пустая клетка, в которую попал противник. Видна обоим игрокам
    DECK_CELL = 2  #Палуба корабля. Видна хозяину поля
    HIT_DECK_CELL = -2  #Палуба корабля, в которую попал противник. Видна обоим игрокам

