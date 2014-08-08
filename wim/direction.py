class Direction(object):
    def __init__(self, model, count):
        self.model = model
        self.count = count

    def move(self, window):
        (x, y, w, h) = self.model.geometry_for(window)
        self.model.move_window(window, *self._coordinates(x, y, w, h))

    def _coordinates(self, x, y, w, h):
        return (x, y, w, h)


class RightDirection(Direction):

    def _coordinates(self, x, y, w, h):
        return (x + self.count, y, w, h)


class LeftDirection(Direction):

    def _coordinates(self, x, y, w, h):
        return (x - self.count, y, w, h)


class UpDirection(Direction):

    def _coordinates(self, x, y, w, h):
        return (x, y - self.count, w, h)


class DownDirection(Direction):

    def _coordinates(self, x, y, w, h):
        return (x, y + self.count, w, h)
