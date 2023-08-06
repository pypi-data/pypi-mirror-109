#!/usr/bin/env python3

"""Definition of class StaticDict."""

from typing import get_origin, get_args, Dict, Any, Optional, Literal, Union


class StaticDict(dict[Any, Any]):
    """Static dictionaries are dictionaries with predefined keys.

    Keys of a StaticDict can only belong to a DEFAULT dictionary.  If
    a key of a StaticDict d is accessed and if key is not in d, then
    d[key] == DEFAULT[key].

    A TYPE dictionary can be defined in the class to defined types
    associated to keys of DEFAULT.  ValueError is raised if the value
    assigned to a key does not match its type defined in TYPE.  If the
    key is not in TYPE, then no type checking is made.

    >>> from typing import Literal, Union
    >>> class MyStaticDict(StaticDict):
    ...    DEFAULT = {'w': 4, 'x': 0, 'y': 0, 'z': 'test'}
    ...    TYPE = {'x': int, 'y': Literal[0, 1, 2], 'z': Union[str, int]}
    >>> d = MyStaticDict()
    >>> d['x'] = 26
    >>> print(d['y'])
    0
    >>> d['a'] = 1
    Traceback (most recent call last):
    KeyError: ...
    >>> d['x'] = 'test'  #  type error: int expected
    Traceback (most recent call last):
    ValueError: ...
    >>> d['y'] = 4  #  type error: 4 is not in [0, 1, 2]
    Traceback (most recent call last):
    ValueError: ...
    >>> d['w'] = list()  #  ok ('w' is not in TYPE)

    """

    DEFAULT: Dict[Any, Any] = {}
    TYPE: Dict[Any, Any] = {}

    def __init__(self, d: Optional[Dict[Any, Any]] = None):
        """Initialise a StaticDict initialised with dictionary d."""
        dict[Any, Any].__init__(self)
        if d is not None:
            for key in d:
                self[key] = d[key]

    @classmethod
    def get_default(cls, key: Any) -> Any:
        """Get default value associated with key.

        Raise KeyError if key is not in the class DEFAULT dictionary.

        """
        default = cls.DEFAULT
        if key not in default:
            cls.__raise_key_error(key)
        return default[key]

    @classmethod
    def set_default(cls, key: Any, value: Any) -> None:
        """Change the value associated with key in the DEFAULT dictionary.

        Raises KeyError if key is not in the DEFAULT dictionary.

        """
        default = cls.DEFAULT
        if key not in default:
            cls.__raise_key_error(key)
        default[key] = value

    def __setitem__(self, key: Any, value: Any) -> None:
        """Update the value associated with key.

        Raise IndexError if key is not in the DEFAULT dictionary.

        Raise ValueError if value is not a valid value for this key,
        according to the TYPE dictionary.

        """
        if key not in type(self).DEFAULT:
            type(self).__raise_key_error(key)
        type(self).__check(key, value)
        dict.__setitem__(self, key, value)

    @classmethod
    def __check(cls, key: Any, value: Any) -> None:
        def c(cond: bool) -> None:
            if not cond:
                cls.__raise_value_error(key, value)

        def rec(val: Any, typedef: Any) -> None:
            def check_items(values: Any, typedef: Any) -> None:
                if typedef is not None:
                    for item in values:
                        rec(item, typedef)
            if isinstance(typedef, type):
                c(isinstance(val, typedef))
            elif get_origin(typedef) == Literal:  # pylint: disable=W0143
                c(val in get_args(typedef))
            elif get_origin(typedef) == Union:  # pylint: disable=W0143
                ok = False
                for t in get_args(typedef):
                    try:
                        rec(val, t)
                        ok = True
                    except ValueError:
                        pass
                c(ok)
            elif get_origin(typedef) == tuple:
                try:
                    args = get_args(typedef)
                    c(len(args) == len(val))
                    for arg, tuple_val in zip(args, val):
                        rec(tuple_val, arg)
                except TypeError:
                    c(False)
            elif get_origin(typedef) in [list, set]:
                typ = get_origin(typedef)
                assert isinstance(typ, type)
                c(isinstance(val, typ))
                check_items(value, get_args(typedef)[0])
        typedef = cls.TYPE.get(key)
        if typedef is None or value is None:
            return
        rec(value, typedef)

    def __getitem__(self, key: Any) -> Any:
        """Get the value associated with key.

        Raise IndexError if key is not in the DEFAULT dictionary.  If
        key is not in self, return DEFAULT[key].

        """
        if not type(self).DEFAULT:
            type(self).__raise_key_error(key)
        if key not in self:
            result = type(self).DEFAULT[key]
        else:
            result = dict.__getitem__(self, key)
        return result

    @classmethod
    def __raise_value_error(cls, key: Any, value: Any) -> None:
        raise ValueError(
            '{} is not a valid value for key {} of a {} dictionary'.format(
                value, key, cls
            )
        )

    @classmethod
    def __raise_key_error(cls, key: Any) -> None:
        raise KeyError(
            '{} is not a valid key of a {} dictionary'.format(
                key, cls
            )
        )
