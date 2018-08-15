from enum import Enum
import pydash as _

import ui
from configs.locale import Locale
from configs.response import Response
from configs.theme import Theme
from field import load_field


class Server:

    def __init__(self):
        """Создает два пустых поля
        """
        player_a_name = input('Игрок А, ваше имя >')
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
        ], player_a_name)
        player_b_name = input('Игрок Б, ваше имя >')
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
        ], player_b_name)
        locale = Locale.RU
        theme = Theme.MAIN
        border = True

        current_field = field_a
        target_field = field_b

        while True:
            print(ui.micro_draw(target_field, current_field, locale=locale, theme=theme, border=border))
            print('{}, ваш ход!'.format(current_field.player_name))
            try:
                move = ui.make_ship_from_str(input('>'), locale)
                assert len(move) == 1
                move = move[0]
                response = target_field.hit(move)
                print('{}!'.format(response.value))
                if response == Response.MISS:
                    current_field, target_field = target_field, current_field
                if response == Response.LOST:
                    print('Игрок {} выиграл бой!'.format(current_field.player_name))
                    break
            except Exception:
                print('Некорректный ввод!')



        #field_a = ui.input_field("A", Locale.EN, Theme.MAIN)


if __name__ == '__main__':
    Server()
