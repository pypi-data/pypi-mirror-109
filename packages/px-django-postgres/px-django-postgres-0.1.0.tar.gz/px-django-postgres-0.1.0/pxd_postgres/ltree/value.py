from collections.abc import Iterable
from collections import UserList
from typing import Union


__all__ ='LtreeValueParserables', 'LtreeValue', 'LtreeIntValue',


LtreeValueParserables = (str, int, float, Iterable)


class LtreeValue(UserList):
    _base_type: type = str

    def __init__(self, value: Union[Iterable, str, int]) -> None:
        base = self._base_type

        if isinstance(value, str):
            value = value.strip().split('.') if value else []
        elif isinstance(value, (int, float)):
            value = [int(value)]
        elif isinstance(value, Iterable):
            value = [v for v in value]
        else:
            raise ValueError('Invalid value: {!r} for ltree'.format(value))

        super(LtreeValue, self).__init__(initlist=[base(x) for x in value])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '.'.join(map(str, self))


class LtreeIntValue(LtreeValue):
    _base_type: type = int
