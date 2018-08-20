from unittest import TestCase

from Coord import Coord
from clients.bot import get_move_candidates
from config import CellState

m = CellState.CELL_MISS.value
x = CellState.CELL_DECK_DEAD.value
o = CellState.CELL_FOG.value


class GetViewTestCase(TestCase):

    def test_extend_ship(self) -> None:
        candidates = get_move_candidates([
            [o, o, o, o, o, o, o],
            [o, o, m, x, x, o, o],
            [o, o, o, o, o, o, o]
        ])

        self.assertEqual([Coord((1, 5))], candidates)

    def test_extend_ship_at_border(self) -> None:
        candidates = get_move_candidates([
            [o, o, o, o, o, o, o],
            [o, o, m, o, o, x, x],
            [o, o, o, o, o, o, o]
        ])

        self.assertEqual([Coord((1, 4))], candidates)
