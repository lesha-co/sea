from typing import Tuple


class Coord:
    def __init__(self, tup: Tuple[int, int]):
        self.i, self.j = tup

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord((self.i + other.i, self.j + other.j))

    def __sub__(self, other: 'Coord') -> 'Coord':
        return Coord((self.i - other.i, self.j - other.j))

    def __eq__(self, other: 'Coord'):
        return (self.i, self.j) == (other.i, other.j)

    def __le__(self, other: 'Coord') -> bool:
        return (self.i, self.j) <= (other.i, other.j)

    def __ge__(self, other: 'Coord') -> bool:
        return (self.i, self.j) >= (other.i, other.j)

    def __lt__(self, other: 'Coord') -> bool:
        return (self.i, self.j) < (other.i, other.j)

    def __gt__(self, other: 'Coord') -> bool:
        return (self.i, self.j) > (other.i, other.j)

    def __ne__(self, other: 'Coord') -> bool:
        return (self.i, self.j) != (other.i, other.j)

    def __str__(self) -> str:
        return '({},{})'.format(self.i, self.j)

    def __hash__(self) -> int:
        return (self.i, self.j).__hash__()

    def __repr__(self) -> str:
        return 'Coord.Coord(({},{}))'.format(self.i, self.j)
