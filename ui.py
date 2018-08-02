import pydash as _
from configs.locale import Locale
from configs.theme import Theme
from configs.rules import FIELD_DIMENSIONS
from field import Field
import re

CELL_WIDTH = 3


def draw_field(field: Field, locale: Locale, theme: Theme, numbers_right: bool = False, opponent: bool = False):
    header = _.chain(locale.value).map_(lambda x: "{: ^{}}".format(x, CELL_WIDTH)).join().value()
    if numbers_right:
        header = ' '.join([header, ' ' * CELL_WIDTH])
    else:
        header = ' '.join([' ' * CELL_WIDTH, header])

    view = field.get_view(opponent)
    raw_rows = _.map_(view, lambda row: _.chain(row).map_(theme.value.get).join().value())
    line_numbers_fmt = '{{: {}{}}}'.format('<' if numbers_right else '>', CELL_WIDTH)
    line_numbers = _.map_(
        list(range(1, FIELD_DIMENSIONS[0] + 1)),
        line_numbers_fmt.format
    )
    if numbers_right:
        columns = _.zip_(raw_rows, line_numbers)
    else:
        columns = _.zip_(line_numbers, raw_rows)
    lines = [header] + _.map_(columns, ' '.join)

    return _.join(lines, '\n')


def to_cell_coordinates(item, locale: Locale):
    if not item:
        return None
    if item in locale.value:
        return locale.value.index(item)
    try:
        return int(item) - 1
    except ValueError:
        return None


def make_ship_from_str(string: str, locale: Locale):
    alpha = locale.value
    pattern = r'^([{}])(\d)(?:([{}])(\d))?$'.format(alpha, alpha)
    findings = re.findall(pattern, string)
    if not findings:
        raise Exception('Incorrect input')

    ship = _.map_(findings[0], lambda item: to_cell_coordinates(item, locale))
    if not ship[2]:
        # single deck ship
        return [(ship[1], ship[0])]

    else:
        start = [ship[1], ship[0]]
        finish = [ship[3], ship[2]]
        diff = _.chain(_.zip_(start, finish)).map_(lambda x: x[1] - x[0]).value()
        if diff[0] and diff[1]:
            raise Exception('Ship should be a straight line')

        if diff[0] == 0:  # vertical
            increment = [0, 1]
        else:  # horizontal
            increment = [1, 0]

        ship = []
        current = start
        while current != finish:
            ship.append((*current,))
            current[0] += increment[0]
            current[1] += increment[1]

        ship.append(tuple(finish))
        return ship


def input_field(player, locale: Locale):
    f = Field()
    while f.fleet_incomplete():
        print(draw_field(f, locale, Theme.MAIN))
        ship = input("Add ship >")
        try:
            f.add_fleet(make_ship_from_str(ship))
        except Exception as x:
            print(x)

    return f


if __name__ == '__main__':
    input_field('PLAYER A', Locale.RU)
