from typing import List, Iterator, Tuple

from helpers import adjacent_square
from config import CellState
from Coord import Coord


class Ship:
    def __init__(self, cells: List[Coord]):
        self.cells = cells
        self.state = [CellState.CELL_DECK] * len(cells)

    def __len__(self) -> int:
        return len(self.cells)

    def get_cell(self, cell: Coord) -> CellState:
        return self.state[self.cells.index(cell)]

    def hit(self, cell: Coord):
        self.state[self.cells.index(cell)] = CellState.CELL_DECK_DEAD

        return self

    def get_view(self) -> Iterator[Tuple[Coord, CellState]]:
        return zip(self.cells, self.state)

    def is_dead(self) -> bool:
        return all(map(lambda state: state == CellState.CELL_DECK_DEAD, self.state))

    def all_adjacent_cells(self) -> List[Coord]:
        all_adjacent_cells = []
        for cell in self.cells:
            for adj in adjacent_square:
                new_adj = cell + adj
                if new_adj not in all_adjacent_cells and new_adj not in self.cells:
                    all_adjacent_cells.append(new_adj)

        return all_adjacent_cells
