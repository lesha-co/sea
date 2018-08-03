from enum import Enum


class CellState(Enum):
    CELL_FOG = 0
    CELL_EMPTY = 1  # Пустая клетка. Видна хозяину поля
    CELL_MISS = -1  # Пустая клетка, в которую попал противник. Видна обоим игрокам
    CELL_DECK = 2  # Палуба корабля. Видна хозяину поля
    CELL_DECK_DEAD = -2  # Палуба корабля, в которую попал противник. Видна обоим игрокам
    CELL_CANT_PLACE_SHIP = -10
