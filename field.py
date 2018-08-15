from typing import List, Optional

from check_field import validate_field, find_ships
from config import CellState, Response, FIELD_DIMENSIONS
from my_types.coord import Coord
from my_types.weak_ship import WeakShip
from ship import Ship


class Field:
    def __init__(self, fleet: Optional[List[WeakShip]]=None, player_name='') -> None:
        self.player_name = player_name
        if fleet is None:
            fleet = []
        if fleet and type(fleet[0]) is list:
            fleet = list(map(Ship, fleet))
        self.fleet = fleet
        self.exposedCells = set()

    def add_fleet(self, ship: WeakShip):
        new_fleet = self.fleet + [Ship(ship)]
        f = Field(fleet=new_fleet, player_name=self.player_name)
        try:
            validate_field(f.get_view(), is_setup_stage=True)
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

    def get_view(self, opponent: bool = False, draw_contours: bool = False):
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

        for i in range(FIELD_DIMENSIONS[0]):
            for j in range(FIELD_DIMENSIONS[1]):
                if opponent and not (i, j) in self.exposedCells:
                    view[i][j] = CellState.CELL_FOG.value
                else:
                    ship = self.lookup_ship((i, j))
                    if ship:
                        view[i][j] = ship.get_cell((i, j)).value
                    elif (i, j) in self.exposedCells:
                        view[i][j] = CellState.CELL_MISS.value
                    elif (i, j) in contours:
                        view[i][j] = CellState.CELL_CANT_PLACE_SHIP.value
                    else:
                        view[i][j] = CellState.CELL_EMPTY.value

        return view

    @staticmethod
    def make_field(opponent=False) -> List[List[int]]:
        field = []
        initial = CellState.CELL_FOG if opponent else CellState.CELL_EMPTY
        for i in range(FIELD_DIMENSIONS[0]):
            field.append([initial.value] * FIELD_DIMENSIONS[1])
        return field

    @staticmethod
    def load_field(field: List[List[int]], player_name: str) -> 'Field':
        return Field(find_ships(field), player_name)


