from selector import Selector


class Direction(object):
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
            return Selector(direction_expr, expression, model)


class BaseDirection(object):
    def __init__(self, model, count):
        self.model = model
        self.count = count

    def move(self, window):
        (x, y, w, h) = self.model.geometry_for(window)
        self.model.move_window(window, *self._coordinates(x, y, w, h))

    def _coordinates(self, x, y, w, h):
        return (x, y, w, h)


class RightDirection(BaseDirection):

    def _coordinates(self, x, y, w, h):
        return (x + self.count, y, w, h)


class LeftDirection(BaseDirection):

    def _coordinates(self, x, y, w, h):
        return (x - self.count, y, w, h)
