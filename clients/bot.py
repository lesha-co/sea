from random import choices, choice
from string import ascii_lowercase, digits
from typing import List

import pydash as py_

from Coord import Coord
from check_field import find_adjacent_cells, find_ships
from config import Locale, Theme, CellState
from my_types.matrix_int import FieldView, MatrixInt
from ship import Ship
from .client import Client


def get_move_candidates(v: MatrixInt) -> List[Coord]:
    ships = find_ships(v)  # Находим все куски кораблей

    # Находим все пустые клетки
    empty = [Coord((i, j))
             for i, row in enumerate(v)
             for j, cell in enumerate(row)
             if cell == CellState.CELL_FOG.value]

    # Для каждого куска корабля выбираем клетки, где он может продолжаться
    candidates = py_.flat_map(ships, lambda ship: calculate_ship_extension(ship, empty))
    return candidates or empty


def calculate_ship_extension(ship: Ship, candidates: List[Coord]) -> List[Coord]:
    if len(ship) == 1:
        return find_adjacent_cells(ship.cells[0], candidates, only_orthogonal=True)
    increment = ship.cells[1] - ship.cells[0]
    first, last = ship.cells[0], ship.cells[-1]
    if increment.j == 0:  # vertical
        ext = [first + Coord((-1, 0)), last + Coord((1, 0))]
    else:  # horizontal
        ext = [first + Coord((0, -1)), last + Coord((0, 1))]

    return py_.intersection(ext, candidates)


class BotClient(Client):
    def __init__(self, client_id, locale=Locale.EN) -> None:
        super().__init__(locale, Theme.TESTING, False, client_id)

    def request_name(self) -> str:
        return 'bot-{}'.format(''.join(choices(ascii_lowercase + digits, k=3)))

    def request_move(self, opponent_view: FieldView) -> Coord:
        return choice(get_move_candidates(opponent_view[1]))
