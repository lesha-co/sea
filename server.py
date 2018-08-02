from enum import Enum

import ui
from configs.locale import Locale


class GameState(Enum):
    LOBBY = "LOBBY"  # Игра еще не началась, игроки могут отправить свои поля
    PLAYER_A_MOVE = "A"
    PLAYER_B_MOVE = "B"
    GAMEOVER = "GAMEOVER"


class Server:

    def __init__(self):
        """Создает два пустых поля
        """
        field_a = ui.input_field("A", Locale.RU)
