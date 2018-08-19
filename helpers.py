from typing import Dict, List, Optional, TypeVar, Iterable

from pydash import py_

from config import Locale
from my_types.coord import Coord

T = TypeVar('T')


def group_by_keys(dicts: Iterable[Dict[str, T]], default_value: Optional[T] = None) -> Dict[str, List[T]]:
    all_keys = py_.chain(dicts).flat_map(lambda d: list(d.keys())).uniq().value()
    # ^ это эквивалентно вот этому:
    # all_keys = py_.flat_map(dicts, lambda d: list(d.keys()))
    # all_keys = py_.uniq(all_keys)

    values = py_.map_(all_keys, lambda key: py_.invoke_map(dicts, 'get', key, default_value))
    return py_.zip_object(all_keys, values)


def from_move(move: Coord, locale: Locale) -> str:
    return '{}{}'.format(locale.value[move[1]], move[0] + 1)
