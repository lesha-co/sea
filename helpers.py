from typing import Dict, List, Optional, TypeVar, Iterable

from pydash import py_

T = TypeVar('T')


def group_by_keys(dicts: Iterable[Dict[str, T]], default_value: Optional[T]=None) -> Dict[str, List[T]]:
    all_keys = py_.chain(dicts).flat_map(lambda d: list(d.keys())).uniq().value()
    # ^ это эквивалентно вот этому:
    # all_keys = py_.flat_map(dicts, lambda d: list(d.keys()))
    # all_keys = py_.uniq(all_keys)

    values = py_.map_(all_keys, lambda key: py_.invoke_map(dicts, 'get', key, default_value))
    return py_.zip_object(all_keys, values)
