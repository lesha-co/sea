import pydash as _
from configs.locale import Locale
from configs.theme import Theme
from configs.rules import FIELD_DIMENSIONS
from field import Field

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
        list(range(1, FIELD_DIMENSIONS[0]+1)),
        line_numbers_fmt.format
    )
    if numbers_right:
        columns = _.zip_(raw_rows, line_numbers)
    else:
        columns = _.zip_(line_numbers, raw_rows)
    lines = [header] + _.map_(columns, ' '.join)

    return _.join(lines, '\n')


def make_ship_from_str(string:str):
    pass


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