from .direction import (RightDirection, LeftDirection,
                        DownDirection, UpDirection)
from .selector import SelectorFactory


class ObjectFactory(object):
    def __new__(klass, direction_expr, expression, model):
        count = 1
        if 'count' in expression:
            count = int(''.join(expression['count']))

        logical = {
            'r': RightDirection,
            'l': LeftDirection,
            'u': UpDirection,
            'd': DownDirection,
            'e': RightDirection,
            'w': LeftDirection,
            'n': UpDirection,
            's': DownDirection,
        }

        selector_expr = None if not direction_expr else direction_expr[0]

        if 'logical' in expression:
            return logical[expression['logical']](model, count)
        else:
            return SelectorFactory(selector_expr, expression, model)
