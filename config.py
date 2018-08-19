from enum import Enum


class CellState(Enum):
    CELL_FOG = 0
    CELL_EMPTY = 1  # Пустая клетка. Видна хозяину поля
    CELL_MISS = -1  # Пустая клетка, в которую попал противник. Видна обоим игрокам
    CELL_DECK = 2  # Палуба корабля. Видна хозяину поля
    CELL_DECK_DEAD = -2  # Палуба корабля, в которую попал противник. Видна обоим игрокам
    CELL_CANT_PLACE_SHIP = -10


class Locale(Enum):
    RU = "АБВГДЕЖЗИК"
    EN = "ABCDEFGHIJ"

class Response(Enum):
    MISS = 'Мимо!'
    HIT = 'Попадение!'
    KILL = 'Убит!'
    LOST = 'Все!'
    REPEAT = 'В эту клетку уже стреляли!'


SHIP_CONFIG = {
    1: 4,
    2: 3,
    3: 2,
    4: 1
}

FIELD_DIMENSIONS = (10, 10)


class Theme(Enum):
    MAIN = {
        CellState.CELL_DECK.value: '███',
        CellState.CELL_DECK_DEAD.value: '▒▒▒',
        CellState.CELL_EMPTY.value: '   ',
        CellState.CELL_FOG.value: '   ',
        CellState.CELL_MISS.value: ' ● ',
        CellState.CELL_CANT_PLACE_SHIP.value: '░░░'
    }
    TESTING = {
        CellState.CELL_DECK.value: '[#]',
        CellState.CELL_DECK_DEAD.value: '[x]',
        CellState.CELL_EMPTY.value: '[ ]',
        CellState.CELL_FOG.value: '[?]',
        CellState.CELL_MISS.value: '[.]',
        CellState.CELL_CANT_PLACE_SHIP.value: '[.]'
    }
