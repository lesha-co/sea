from enum import Enum


class Response(Enum):
    MISS = 'Мимо'
    HIT = 'Попадение'
    KILL = 'Убит'
    LOST = 'Все'
    REPEAT = 'В эту клетку уже стреляли'
