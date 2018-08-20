from random import choices, choice
from string import ascii_lowercase, digits
from typing import List

import pydash as py_

from check_field import find_adjacent_cells, find_ships
from config import Locale, Theme, CellState
from Coord import Coord
from helpers import from_move
from my_types.matrix_int import MatrixInt
from .client import Client


def calculate_ship_extension(ship: List[Coord], candidates: List[Coord]) -> List[Coord]:
    if len(ship) == 1:
        return find_adjacent_cells(ship[0], candidates, only_orthogonal=True)
    increment = ship[1] - ship[0]
    first, last = ship[0], ship[-1]
    if increment.j == 0:  # vertical
        ext = [first + Coord((-1, 0)), last + Coord((1, 0))]
    else:  # horizontal
        ext = [first, Coord((0, -1)), last + Coord((0, 1))]

    return py_.intersection(ext, candidates)


class BotClient(Client):
    def __init__(self, client_id, locale=Locale.EN) -> None:
        super().__init__(locale, Theme.TESTING, False, client_id)

    def request_name(self) -> str:
        return 'bot-{}'.format(''.join(choices(ascii_lowercase + digits, k=3)))

    def request_move(self, opponent_view: MatrixInt) -> Coord:

        ships = find_ships(opponent_view)  # Находим все куски кораблей

        # Находим все пустые клетки
        empty = [Coord((i, j))
                 for i, row in enumerate(opponent_view)
                 for j, cell in enumerate(row)
                 if cell == CellState.CELL_FOG.value]

        # Для каждого куска корабля выбираем клетки, где он может продолжаться
        candidates = py_.flat_map(ships, lambda ship: calculate_ship_extension(ship, empty))
        print('---')
        print('ships', ships)
        print('Candidates', py_.map_(candidates, lambda exp: from_move(exp, self.locale)))

        # Если таковые есть, стреляем наугад в них
        if candidates:
            shoot = choice(candidates)
            print('Using first candidate:', from_move(shoot, self.locale))
        # Иначе стреляем вслепую
        else:
            shoot = choice(empty)
            print('Blindly shoot at:', from_move(shoot, self.locale))
        print('---')
        return shoot
