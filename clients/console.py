from .client import Client
from ui import make_ship_from_str, micro_draw
from field import Field
from my_types.coord import Coord
from ui import input_field


class ConsoleClient(Client):

    def request_name(self) -> str:
        return input('{} > Ваше имя > '.format(self.client_id))

    def request_move(self, my_field: Field, opponent_field: Field) -> Coord:
        print(micro_draw(opponent_field, my_field, locale=self.locale, theme=self.theme, border=self.border))
        print('{}, ваш ход!'.format(my_field.player_name))
        while True:
            try:
                move = make_ship_from_str(input('>'), self.locale)
                assert len(move) == 1
                return move[0]
            except AssertionError:
                pass

    def message(self, message: str) -> None:
        print('{} > {}'.format(self.client_id, message))

    def request_field(self) -> Field:
        return input_field(self.client_id, self.locale, self.theme)
