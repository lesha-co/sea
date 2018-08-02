from enum import Enum
class GameState(Enum):
    LOBBY = "LOBBY" # Игра еще не началась, игроки могут отправить свои поля
    PLAYER_A_MOVE = "A"
    PLAYER_B_MOVE = "B"
    GAMEOVER = "GAMEOVER"



class Server:

    def __init__(self):
        """Создает два пустых поля
        """
        field_A = input_field("A")