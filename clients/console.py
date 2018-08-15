from ui import make_ship_from_str
from clients import Client
from configs import Locale
from field import Field, load_field
from my_types.coord import Coord


class ConsoleClient(Client):

    def __init__(self, locale: Locale) -> None:
        super().__init__()
        self.locale = locale

    def request_name(self) -> str:
        return input('Ваше имя:>')

    def request_field(self) -> Field:
        super().request_field()
        return load_field([
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 2],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 2, 2, 2, 1, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 2, 1, 2, 2, 1, 1, 1, 1],
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 2, 2, 1, 1],
            [1, 2, 1, 1, 2, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 2, 1, 1, 1, 2, 2],
            [1, 2, 1, 1, 1, 1, 1, 1, 1, 1],
        ], self.request_name())

    def request_move(self, my_field: Field, opponent_field: Field) -> Coord:
        print('{}, ваш ход!'.format(my_field.player_name))
        while True:
            try:
                move = make_ship_from_str(input('>'), self.locale)
                assert len(move) == 1
                return move[0]
            except AssertionError:
                pass

    def message(self, message: str) -> None:
        print(message)
