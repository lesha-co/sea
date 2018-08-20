from functools import reduce
from itertools import product
from random import choice
from typing import List, Optional

from pydash import py_

from Coord import Coord
from check_field import validate_field, find_ships, get_available_cells, find_straight_segments, check_fleet_config
from config import CellState, Response, FIELD_DIMENSIONS, SHIP_CONFIG
from my_types.matrix_int import FieldView, MatrixInt
from ship import Ship


class Field:
    def __init__(self, fleet: Optional[List[Ship]] = None, player_name='') -> None:
        self.player_name = player_name
        if fleet is None:
            fleet = []
        if fleet and type(fleet[0]) is list:
            fleet = list(map(Ship, fleet))
        self.fleet = fleet
        self.exposedCells = set()

    def add_fleet(self, ship: Ship):
        new_fleet = self.fleet + [ship]
        f = Field(fleet=new_fleet, player_name=self.player_name)
        try:
            validate_field(f.get_view()[1], is_setup_stage=True)
            self.fleet = new_fleet
        except AssertionError as x:
            raise BaseException('field is incorrect', x, ship)

    def lookup_ship(self, cell: Coord):
        """
        Ищет корабль по клетке
        :param cell: (i, j)
        :return: список клеток корабля, статус клетки
        """
        for ship in self.fleet:
            if cell in ship.cells:
                return ship
        return None

    def is_dead(self) -> bool:
        return all(map(lambda ship: ship.is_dead(), self.fleet))

    def hit(self, cell: Coord) -> Response:
        if cell in self.exposedCells:
            return Response.REPEAT
        self.exposedCells.add(cell)
        ship = self.lookup_ship(cell)
        if ship:
            ship.hit(cell)
            if ship.is_dead():
                # splash damage
                splash_damage = ship.all_adjacent_cells()
                self.exposedCells.update(splash_damage)
                if self.is_dead():
                    return Response.LOST
                return Response.KILL
            else:
                return Response.HIT
        else:
            return Response.MISS

    def get_view(self, opponent: bool = False, draw_contours: bool = False) -> FieldView:
        """
        Построить вид поля
        :param opponent: строить с учетом exposedCells
        :param draw_contours: показывать клетки, где запрещено ставить корабли (только если opponent=False)
        :return: 2д список (0)
        """
        view = Field.make_field(opponent)
        draw_contours = draw_contours and not opponent
        contours = set()
        if draw_contours:
            for ship in self.fleet:
                contours.update(ship.all_adjacent_cells())

        for i, j in product(range(FIELD_DIMENSIONS.i), range(FIELD_DIMENSIONS.j)):
            if opponent and not Coord((i, j)) in self.exposedCells:
                view[i][j] = CellState.CELL_FOG.value
            else:
                ship = self.lookup_ship(Coord((i, j)))
                if ship:
                    view[i][j] = ship.get_cell(Coord((i, j))).value
                elif Coord((i, j)) in self.exposedCells:
                    view[i][j] = CellState.CELL_MISS.value
                elif Coord((i, j)) in contours:
                    view[i][j] = CellState.CELL_CANT_PLACE_SHIP.value
                else:
                    view[i][j] = CellState.CELL_EMPTY.value

        return self.player_name, view

    @staticmethod
    def make_field(opponent=False) -> MatrixInt:
        field = []
        initial = CellState.CELL_FOG if opponent else CellState.CELL_EMPTY
        for i in range(FIELD_DIMENSIONS.i):
            field.append([initial.value] * FIELD_DIMENSIONS.j)
        return field

    @staticmethod
    def load_field(field: MatrixInt, player_name: str) -> 'Field':
        return Field(find_ships(field), player_name)

    @staticmethod
    def generate_random_field(player_name: str, base: Optional['Field'] = None) -> 'Field':
        missing_config = SHIP_CONFIG
        if base:
            initial = base.get_view()[1]
            _, missing_config = check_fleet_config(find_ships(initial), True)
        else:
            initial = Field.make_field()

        lengths = []
        for k, v in missing_config.items():
            for i in range(v):
                lengths.append(k)

        lengths = sorted(lengths, reverse=True)
        f = reduce(Field._try_place, lengths, initial)
        return Field(find_ships(f), player_name)

    @staticmethod
    def _try_place(acc: MatrixInt, desired_length: int) -> MatrixInt:
        available_cells = get_available_cells(acc, FIELD_DIMENSIONS)
        segments = find_straight_segments(available_cells, True) + \
            find_straight_segments(available_cells, False)

        available_segments = py_.filter_(segments, lambda segment: len(segment) >= desired_length)
        chosen_segment = choice(available_segments)

        len_diff = len(chosen_segment) - desired_length
        available_subsegments = py_.map_(list(range(len_diff + 1)), lambda x: chosen_segment[x:x + desired_length])
        chosen_subsegment = choice(available_subsegments)

        new_field = py_.clone_deep(acc)
        for c in chosen_subsegment:
            new_field[c.i][c.j] = CellState.CELL_DECK.value

        return new_field


if __name__ == '__main__':
    from ui import draw_field
    from config import Locale, Theme
    print(draw_field(
        Field.generate_random_field('== DEMO RUN ==').get_view(draw_contours=True),
        Locale.EN,
        Theme.MAIN,
        border=True,
    ))
