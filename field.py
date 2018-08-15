from configs.cell_state import CellState
from check_field import validate_field, check_fleet_config, find_ships
from configs.response import Response
from configs.rules import FIELD_DIMENSIONS


def make_field(opponent=False):
    field = []
    initial = CellState.CELL_FOG if opponent else CellState.CELL_EMPTY
    for i in range(FIELD_DIMENSIONS[0]):
        field.append([initial.value] * FIELD_DIMENSIONS[1])
    return field


def load_field(field, player_name):
    ships = find_ships(field)
    return Field(ships, player_name)


class Ship:
    def __init__(self, cells):
        self.cells = cells
        self.state = [CellState.CELL_DECK] * len(cells)

    def __len__(self):
        return len(self.cells)

    def get_cell(self, cell):
        return self.state[self.cells.index(cell)]

    def hit(self, cell):
        self.state[self.cells.index(cell)] = CellState.CELL_DECK_DEAD

        return self

    def get_view(self):
        return zip(self.cells, self.state)

    def is_dead(self):
        return all(map(lambda state: state == CellState.CELL_DECK_DEAD, self.state))

    def all_adjacent_cells(self):
        adjacent_square = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        all_adjacent_cells = []
        for cell in self.cells:
            for adj in adjacent_square:
                new_adj = (cell[0] + adj[0], cell[1] + adj[1])
                if new_adj not in all_adjacent_cells and new_adj not in self.cells:
                    all_adjacent_cells.append(new_adj)

        return all_adjacent_cells


class Field:
    def __init__(self, fleet=None, player_name=''):
        self.player_name = player_name
        if fleet is None:
            fleet = []

        if fleet and type(fleet[0]) is list:
            fleet = list(map(Ship, fleet))
        self.fleet = fleet
        self.exposedCells = set()

    def add_fleet(self, ship):
        new_fleet = self.fleet + [Ship(ship)]
        f = Field(fleet=new_fleet, player_name=self.player_name)
        try:
            validate_field(f.get_view(), is_setup_stage=True)
            self.fleet = new_fleet
        except AssertionError as x:
            raise BaseException('field is incorrect', x, ship)

    def lookup_ship(self, cell):
        """
        Ищет корабль по клетке
        :param cell: (i, j)
        :return: список клеток корабля, статус клетки
        """
        for ship in self.fleet:
            if cell in ship.cells:
                return ship
        return None

    def is_dead(self):
        return all(map(lambda ship: ship.is_dead(), self.fleet))

    def hit(self, cell):
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
        view = make_field(opponent)
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
