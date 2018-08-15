from field import Field
from my_types.coord import Coord


class Client:
    def request_name(self) -> str:
        """
        Сервер запрашивает имя у игрока
        :return: str
        """
        pass

    def request_field(self) -> Field:
        """
        Сервер запрашивает поле
        :return: int[][]
        """
        pass

    def request_move(self, my_field: Field, opponent_field: Field) -> Coord:
        """
        Сервер запрашивает ход
        :param my_field: поле игрока
        :param opponent_field: поле противника
        :return: tuple(int, int)
        """
        pass

    def message(self, message: str) -> None:
        """
        Сообщение от сервера
        :return:
        """
        pass
