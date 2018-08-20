from field import Field
from Coord import Coord
from my_types.matrix_int import FieldView
from ui import input_field
from ui import make_ship_from_str, micro_draw
from .client import Client


class ConsoleClient(Client):

    def request_name(self) -> str:
        return input('{} > Ваше имя > '.format(self.client_id)) or 'Human'

    def request_move(self, opponent_view: FieldView) -> Coord:
        print(micro_draw(
            opponent_view,
            self.field.get_view(opponent=False),
            locale=self.locale,
            theme=self.theme, border=self.border))
        print('{}, ваш ход!'.format(self.field.player_name))
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

    def conclude(self, message: str, opponent_view: FieldView):
        self.message(message)
        print(micro_draw(
            opponent_view,
            self.field.get_view(),
            locale=self.locale, theme=self.theme, border=self.border))
