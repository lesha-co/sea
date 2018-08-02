from configs.cell_state import CellState
from check_field import validate_field
from configs.rules import FIELD_DIMENSIONS


def make_field(opponent=False):
    field = []
    initial = CellState.CELL_FOG if opponent else CellState.CELL_EMPTY
    for i in range(FIELD_DIMENSIONS[0]):
        field.append([initial.value]*FIELD_DIMENSIONS[1])
    return field


class Ship:
    def __init__(self, cells):
        self.cells = cells
        self.state = [CellState.CELL_DECK] * len(cells)

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
            (0,  -1),          (0,  1),
            (1,  -1), (1,  0), (1,  1),
        ]
        all_adjacent_cells = []
        for cell in self.cells:
            for adj in adjacent_square:
                new_adj = (cell[0] + adj[0], cell[1] + adj[1])
                if new_adj not in all_adjacent_cells and new_adj not in self.cells:
                    all_adjacent_cells.append(new_adj)

        return all_adjacent_cells


class Field:
    def __init__(self, fleet=None):
        if fleet is None:
            fleet = []
        self.fleet = list(map(Ship, fleet))
        self.exposedCells = set()

    def add_fleet(self, ship):
        new_fleet = self.fleet + [ship]
        f = Field(fleet=new_fleet)
        try:
            validate_field(f.get_view(), is_setup_stage=True)
            self.fleet = new_fleet
        except AssertionError:
            raise BaseException('field is incorrect', ship)

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

    def hit(self, cell):
        self.exposedCells.add(cell)
        ship = self.lookup_ship(cell)
        if ship:
            ship.hit(cell)
            if ship.is_dead():
                # splash damage
                splash_damage = ship.all_adjacent_cells()
                self.exposedCells.update(splash_damage)


        return self

    def get_view(self, opponent:bool=False):
        """
        Построить вид поля
        :param opponent: строить с учетом exposedCells
        :return: 2д список (0)
        """
        view = make_field(opponent)

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
                    else:
                        view[i][j] = CellState.CELL_EMPTY.value

        return view