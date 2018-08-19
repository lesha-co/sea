from random import choices, randint, choice
from string import ascii_lowercase, digits
from typing import List

import pydash as py_

from check_field import find_adjacent_cells, find_ships, inc
from config import Locale, Theme, FIELD_DIMENSIONS, CellState
from field import Field
from helpers import from_move
from my_types.coord import Coord
from .client import Client


def diff(one: Coord, other: Coord) -> Coord:
    return other[0] - one[0], other[1] - one[1]


def calculate_ship_extension(ship: List[Coord], candidates: List[Coord]) -> List[Coord]:
    if len(ship) == 1:
        return find_adjacent_cells(ship[0], candidates)
    incr = diff(ship[0], ship[1])
    first, last = ship[0], ship[-1]
    if incr[1] == 0:  # vert
        ext = [inc(first, (-1, 0)), inc(last, (1, 0))]
    else:  # horiz
        ext = [inc(first, (0, -1)), inc(last, (0, 1))]

    return py_.intersection(ext, candidates)


class BotClient(Client):
    def __init__(self, client_id, locale=Locale.EN) -> None:
        super().__init__(locale, Theme.TESTING, False, client_id)

    def request_name(self) -> str:
        return 'bot-{}'.format(''.join(choices(ascii_lowercase + digits, k=3)))

    def request_move(self, my_field: Field, opponent_field: Field) -> Coord:
        v = opponent_field.get_view(opponent=True)

        exposed = [(i, j)
                   for i, row in enumerate(v)
                   for j, cell in enumerate(row)
                   if cell == CellState.CELL_DECK_DEAD.value]

        empty = [(i, j)
                 for i, row in enumerate(v)
                 for j, cell in enumerate(row)
                 if cell == CellState.CELL_FOG.value]
        ships = find_ships(v)

        dumb_candidates = py_.flat_map(exposed, lambda cell: find_adjacent_cells(cell, empty, only_orthogonal=True))

        dumb_candidates = py_.filter_(dumb_candidates,
                                      lambda candidate: v[candidate[0]][candidate[1]] != CellState.CELL_MISS.value)

        candidates = py_.flat_map(ships, lambda ship: calculate_ship_extension(ship, dumb_candidates))
        # print('---')
        # print('ships', ships)
        # print('Exposed decks', py_.map_(exposed, lambda exp: from_move(exp, self.locale)))
        # print('Dumb Candidates', py_.map_(dumb_candidates, lambda exp: from_move(exp, self.locale)))
        # print('Candidates', py_.map_(candidates, lambda exp: from_move(exp, self.locale)))

        if candidates:
            shoot = choice(candidates)
            # print('Using first candidate:', from_move(shoot, self.locale))
        else:
            shoot = choice(empty)
            # print('Blindly shoot at:', from_move(shoot, self.locale))
        # print('---')
        return shoot
