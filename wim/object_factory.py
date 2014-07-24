from .direction import RightDirection, LeftDirection
from .selector import SelectorFactory


class ObjectFactory(object):
    def __new__(klass, direction_expr, expression, model):
        count = 1
        if 'count' in expression:
            count = int(''.join(expression['count']))

        logical = {
            'r': RightDirection,
            'l': LeftDirection
        }

        if 'logical' in expression:
            return logical[expression['logical']](model, count)
        else:
            return SelectorFactory(direction_expr, expression, model)
