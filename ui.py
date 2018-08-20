from re import findall

from pydash import py_

from Coord import Coord
from check_field import check_fleet_config
from config import CellState, Locale, Theme, FIELD_DIMENSIONS
from field import Field
from my_types.matrix_int import FieldView
from my_types.weak_ship import WeakShip
from ship import Ship

CELL_WIDTH = 3


def micro_draw(target_view: FieldView, current_view: FieldView, **kwargs) -> str:

    draw_left = draw_field(target_view, numbers_right=False, **kwargs).split('\n')
    draw_right = draw_field(current_view, numbers_right=True, **kwargs).split('\n')

    lines = py_.zip_(draw_left, draw_right)
    combo_lines = py_.map_(lines, lambda pair: ' : '.join(pair))
    return '\n'.join(combo_lines)


def draw_field(v: FieldView, locale: Locale, theme: Theme,
               numbers_right: bool = False,
               border: bool = False):

    name_label, view = v
    header = py_.chain(locale.value).map_(lambda x: "{: ^{}}".format(x, CELL_WIDTH)).join().value()
    name_header = '{:<{}}'.format(name_label, CELL_WIDTH*len(locale.value))
    if numbers_right:
        name_header = ' '.join([name_header, ' ' * CELL_WIDTH])
        header = ' '.join([header, ' ' * CELL_WIDTH])
    else:
        header = ' '.join([' ' * CELL_WIDTH, header])
        name_header = ' '.join([' ' * CELL_WIDTH, name_header])

    sub_header = None
    if border:
        sub_header = "─" * CELL_WIDTH * len(locale.value)
        if numbers_right:
            sub_header += '─┐ ' + ' '*CELL_WIDTH
            header += '  '
            name_header += '  '

        else:
            sub_header = ' '*CELL_WIDTH + ' ┌─' + sub_header
            header = '  ' + header
            name_header = '  ' + name_header

    raw_rows = py_.map_(view, lambda row: py_.chain(row).map_(theme.value.get).join().value())
    line_numbers_fmt = '{{: {}{}}}'.format('<' if numbers_right else '>', CELL_WIDTH)
    line_numbers = py_.map_(
        list(range(1, FIELD_DIMENSIONS.i + 1)),
        line_numbers_fmt.format
    )
    if numbers_right:
        columns = py_.zip_(raw_rows, line_numbers)
    else:
        columns = py_.zip_(line_numbers, raw_rows)

    column_separator = ' '
    if border:
            column_separator = ' │ '
    lines = [name_header, header]
    if border:
        lines.append(sub_header)
    lines += py_.map_(columns, column_separator.join)

    return py_.join(lines, '\n')


def to_cell_coordinates(item, locale: Locale):
    if not item:
        return None
    if item in locale.value:
        return locale.value.index(item)
    try:
        return int(item) - 1
    except ValueError:
        return None


def make_ship_from_str(string: str, locale: Locale) -> WeakShip:
    
    alpha = locale.value
    pattern = r'^([{}])(\d+)(?:([{}])(\d+))?$'.format(alpha, alpha)
    findings = findall(pattern, string)
    assert findings, 'Incorrect input'

    ship = py_.map_(findings[0], lambda item: to_cell_coordinates(item, locale))
    if ship[2] is None:
        # single deck ship
        assert 0 <= ship[1] < FIELD_DIMENSIONS.i, 'Incorrect input'
        assert 0 <= ship[0] < FIELD_DIMENSIONS.j, 'Incorrect input'
        coord = Coord((ship[1], ship[0]))
        return Ship([coord])

    else:
        assert 0 <= ship[1] < FIELD_DIMENSIONS.i, 'Incorrect input'
        assert 0 <= ship[0] < FIELD_DIMENSIONS.j, 'Incorrect input'
        assert 0 <= ship[3] < FIELD_DIMENSIONS.i, 'Incorrect input'
        assert 0 <= ship[2] < FIELD_DIMENSIONS.j, 'Incorrect input'

        start = Coord((ship[1], ship[0]))
        finish = Coord((ship[3], ship[2]))
        diff = finish - start
        if diff.i and diff.j:
            raise Exception('Ship should be a straight line')

        if diff.i == 0:  # vertical
            increment = Coord((0, 1))
        else:  # horizontal
            increment = Coord((1, 0))

        ship = []
        current = start
        while current != finish:
            ship.append(current)
            current += increment

        ship.append(finish)
        return Ship(ship)


def draw_slots(diff, theme: Theme):
    keys = sorted(diff.keys())
    tile = theme.value[CellState.CELL_DECK.value]
    strings = py_.map_(keys, lambda key: '{} ×{}'.format(tile*key, diff[key]))
    return ' '.join(strings)


def input_field(player_name, locale: Locale, theme: Theme):
    f = Field(None, player_name=player_name)
    fleet_correct, diff = check_fleet_config(f.fleet, is_setup_stage=True)
    while diff:
        print('\n'.join([
            'Игрок {player_name}, выставьте свои корабли: \n'.format(player_name=player_name),
            ' ' + draw_slots(diff, theme) + '\n',
            draw_field(f.get_view(draw_contours=True), locale, theme, border=True)
        ]))

        ship = input("Добавить корабль (⏎ для рандомного поля) >").strip()
        if not ship:
            return Field.generate_random_field(player_name, base=f)

        try:
            f.add_fleet(make_ship_from_str(ship, locale))
            fleet_correct, diff = check_fleet_config(f.fleet, is_setup_stage=True)
        except BaseException as x:
            print(x)
    return f
