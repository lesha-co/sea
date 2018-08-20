from config import Locale, Theme
from field import Field
from my_types.coord import Coord
from my_types.matrix_int import FieldView


class Client:
    def __init__(self, locale: Locale, theme: Theme, border: bool, client_id) -> None:

        self.locale = locale
        self.theme = theme
        self.border = border
        self.client_id = client_id
        self.client_id = self.request_name()
        self.field = self.request_field()

    def request_name(self) -> str:
        """
        Сервер запрашивает имя у игрока
        :return: str
        """
        raise Exception('Can\'t use base class')

    def request_field(self) -> Field:
        """
        Сервер запрашивает поле
        :return: int[][]
        """
        return Field.generate_random_field(self.client_id)

    def request_move(self, opponent_view: FieldView) -> Coord:
        """
        Сервер запрашивает ход
        :param opponent_view: представление поля противника
        :return: tuple(int, int)
        """
        raise Exception('Can\'t use base class')

    def message(self, message: str) -> None:
        """
        Сообщение от сервера
        :return:
        """
        pass

    def conclude(self, message: str, opponent_view: FieldView):
        return self.message(message)
