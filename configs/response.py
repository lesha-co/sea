from enum import Enum


class Response(Enum):
    MISS = 0
    HIT = 1
    KILL = 2
    LOST = 3