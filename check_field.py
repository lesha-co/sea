import pydash as _
from collections import Counter
from configs.cell_state import CellState
from configs.rules import SHIP_CONFIG, FIELD_DIMENSIONS
from helpers import zip_by_keys


def find_checked_cells(field):
    return [
        (i, j)
        for i, row in enumerate(field)
        for j, cell in enumerate(row)
        if cell == CellState.CELL_DECK.value
    ]


def find_adjacent_cells(origin, cells):
    adjacent_square = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1),
    ]
    diffs = _.map_(cells, lambda other: (other[0] - origin[0], other[1] - origin[1]))

    adjacent = _.filter_(
        _.zip_(cells, diffs),
        lambda pair: pair[1] in adjacent_square,

    )

    return _.map_(adjacent, 0)


def find_adjacent_cells_recursive(origin, cells):
    selected = [origin]
    while True:
        current_selected = []
        for cell in selected:
            current_selected += find_adjacent_cells(cell, cells)

        current_selected = filter(lambda sel: sel not in selected, current_selected)
        current_selected = list(set(current_selected))
        if not current_selected:
            break

        selected += current_selected

    return sorted(selected)


def find_ships(field):
    found_ships = []
    cells = find_checked_cells(field)
    while cells:
        adjacent_group = find_adjacent_cells_recursive(cells[0], cells)
        cells = [
            coord for coord in cells if coord not in adjacent_group
        ]
        found_ships.append(adjacent_group)
    return found_ships


def check_ship_shape(ship):
    """
    Проверяет форму корабля
    :param ship: Список клеток корабля
    :return: True/False
    """
    if len(ship) == 1:
        return True
    ship = sorted(ship)
    increments = map(
        lambda pair: (pair[1][0] - pair[0][0], pair[1][1] - pair[0][1]),
        zip(ship, ship[1:]))
    common_increment = list(set(increments))
    return len(common_increment) == 1 and common_increment[0] in [(0, 1), (1, 0)]


def check_fleet_config(fleet, is_setup_stage=False):
    """
    Проверяет конфигурацию флота (1 4палубный, 2 3палубных итд)
    :param fleet: список кораблей
    :param is_setup_stage: Если True, то отключает проверку на недостающие корабли (считается, что поле находится в
    процессе заполнения и игрок еще не выставил все корабли)
    :return: (bool, [dict])
    """
    lengths = map(len, fleet)
    config = Counter(lengths)
    if is_setup_stage:
        if config == SHIP_CONFIG:
            return True

        configs = zip_by_keys((config, SHIP_CONFIG), 0)
        diff = _.map_values(configs, lambda counts: counts[1] - counts[0])
        return False, diff

    return config == SHIP_CONFIG


def check_ship_bounds(ship):
    """
    Проверяет, что корабль внутри поля
    :param ship: Список клеток корабля
    :return: True/False
    """
    return all(
        0 <= cell[0] < FIELD_DIMENSIONS[0] and 0 <= cell[1] < FIELD_DIMENSIONS[1]
        for cell in ship
    )


def validate_field(field, is_setup_stage=False):
    """
    Проверяет поле на ошибки
    :param field: 2d список клеток
    :param is_setup_stage: Если True, то отключает проверку на недостающие корабли (считается, что поле находится в
    процессе заполнения и пользователь еще не выставил все корабли)
    :return:
    """
    ships = find_ships(field)
    assert check_fleet_config(ships, is_setup_stage), \
        "Fleet config is invalid (ships are touching or extra/missing ship)"
    for ship in ships:
        assert check_ship_shape(ship), "There is a deformed ship somewhere on the field ({})".format(ship)
        assert check_ship_bounds(ship), "Ship outside bounds ({})".format(ship)
    return True
