from random import choices, randint
from string import ascii_lowercase, digits
from config import Locale, Theme, FIELD_DIMENSIONS
from field import Field
from my_types.coord import Coord
from .client import Client


class BotClient(Client):
    def __init__(self, client_id) -> None:
        super().__init__(Locale.EN, Theme.TESTING, False, client_id)

    def request_name(self) -> str:
        return 'bot-{}'.format(''.join(choices(ascii_lowercase + digits, k=3)))

    def request_move(self, my_field: Field, opponent_field: Field) -> Coord:
        return randint(0, FIELD_DIMENSIONS[0]-1), randint(0, FIELD_DIMENSIONS[1]-1)
