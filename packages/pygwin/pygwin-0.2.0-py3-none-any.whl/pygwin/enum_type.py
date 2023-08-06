#!/usr/bin/env python3

"""Definition of class EnumType."""

from typing import Iterator


class EnumType(type):
    """EnumType is a metaclass for enum type definitions.

    >>> class Color(metaclass=EnumType):
    ...    RED = 'red'
    ...    GREEN = 'green'
    ...    BLUE = 'blue'
    >>> for c in Color:
    ...    print(c)
    red
    green
    blue
    >>> 'blue' in Color
    True
    >>> 'yellow' in Color
    False
    >>> import random
    >>> c = random.choice(Color)
    >>> c in ['red', 'green', 'blue']
    True

    """

    def __iter__(cls) -> Iterator[str]:
        for key in cls.__dict__:
            val = cls.__dict__[key]
            if not key.startswith('__') and isinstance(val, str):
                yield val

    def __len__(cls) -> int:
        return sum(1 for _ in enumerate(cls))

    def __getitem__(cls, i: int) -> str:
        for j, item in enumerate(cls):
            if j == i:
                return item
        raise IndexError
