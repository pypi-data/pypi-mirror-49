# built-in
import json
from collections import defaultdict
from functools import reduce
from typing import Optional


def _each(value):
    if isinstance(value, list):
        new_value = defaultdict(list)
        for line in value:
            for name, field in line.items():
                new_value[name].append(field)
        return dict(new_value)

    new_value = []
    for line in zip(*value.values()):
        new_value.append(dict(zip(value.keys(), line)))
    return new_value


def _flatten(value) -> list:
    if not isinstance(value, (list, tuple)):
        return [value]
    new_value = []
    for element in value:
        new_value.extend(_flatten(element))
    return new_value


FILTERS = {
    'each()': _each,
    'first()': lambda v: v[0],
    'flatten()': _flatten,
    'last()': lambda v: v[-1],
    'len()': len,
    'max()': max,
    'min()': min,
    'reverse()': lambda v: v[::-1],
    'sort()': sorted,
    'sum()': sum,
    'type()': lambda v: type(v).__name__,
    'zip()': lambda v: list(map(list, zip(*v))),

    # aliases
    '#': _each,
    'count()': len,
    'flat()': _flatten,
    'latest()': lambda v: v[-1],
    'length()': len,
    'reversed()': lambda v: v[::-1],
    'size()': len,
    'sorted()': sorted,
}


def getitem(value, key):
    # function
    filter = FILTERS.get(key)
    if filter is not None:
        return filter(value)

    # sum of fields
    if '+' in key:
        keys = key.split('+')
        return {key: value[key] for key in keys}

    # index
    if key.isdigit():
        key = int(key)
        return value[key]

    # slice
    if ':' in key:
        left, _sep, right = key.partition(':')
        if (not left or left.isdigit()) and (not right or right.isdigit()):
            left = int(left) if left else 0
            right = int(right) if right else None
            return value[left:right]

    # field
    return value[key]


def make_json(data, key: str = None, sep: Optional[str] = '-') -> str:
    json_params = dict(indent=2, sort_keys=True, ensure_ascii=False)
    # print all config
    if not key:
        return json.dumps(data, **json_params)  # type: ignore

    if sep is None:
        return json.dumps(data[key], **json_params)  # type: ignore

    keys = key.replace('.', sep).split(sep)
    value = reduce(getitem, keys, data)
    # print config section
    if isinstance(value, (dict, list)):
        return json.dumps(value, **json_params)  # type: ignore

    # print one value
    return str(value)
