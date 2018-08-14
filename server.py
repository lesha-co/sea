from enum import Enum
import pydash as _

import ui
from configs.locale import Locale
from configs.response import Response
from configs.theme import Theme
from field import Field, load_field


class GameState(Enum):
    LOBBY = "LOBBY"  # Игра еще не началась, игроки могут отправить свои поля
    PLAYER_A_MOVE = "A"
    PLAYER_B_MOVE = "B"
    GAMEOVER = "GAMEOVER"


class Server:

    def __init__(self):
        """Создает два пустых поля
        """
        field_a = load_field([
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
        ])
        field_b = load_field([
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
        ])
        current_player = 0
        locale = Locale.RU
        theme = Theme.MAIN
        border = True

        while True:

            drawings = ui.micro_draw(field_a, field_b, current_player, locale=locale, theme=theme, border=border)

            print(drawings)
            print('Игрок {}, ваш ход!'.format(current_player))
            target_field = field_a if current_player == 1 else field_b
            move = ui.make_ship_from_str(input('>'), locale)
            assert len(move) == 1
            move = move[0]
            response = target_field.hit(move)
            print('Ответ: ', response.name)
            if response == Response.MISS:
                current_player = 1 - current_player
            if response == Response.LOST:
                print('Игрок {} выиграл бой!'.format(current_player))
                break

        #field_a = ui.input_field("A", Locale.EN, Theme.MAIN)


if __name__ == '__main__':
    Server()
