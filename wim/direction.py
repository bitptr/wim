import itertools

from .util import now


class Direction(object):
    def __init__(self, wnck_wrapper, count):
        self.wnck_wrapper = wnck_wrapper
        self.count = count

    def move(self, window):
        (x, y, w, h) = self.wnck_wrapper.geometry_for_window(window)
        self.wnck_wrapper.move_window_to_coordinates(
            window, *self._coordinates(x, y, w, h))

    def jump(self, workspace):
        for _ in itertools.repeat(None, self.count):
            if workspace:
                workspace = self.wnck_wrapper.call_workspace(
                    "get_neighbor", workspace,
                    self.wnck_wrapper.get_motion_direction(self._motion()))

        if workspace is not None:
            self.wnck_wrapper.call_workspace("activate", workspace, now())

    def _coordinates(self, x, y, w, h):
        return (x, y, w, h)


class RightDirection(Direction):
    def _coordinates(self, x, y, w, h):
        return (x + self.count, y, w, h)

    def _motion(self):
        return "RIGHT"


class LeftDirection(Direction):
    def _coordinates(self, x, y, w, h):
        return (x - self.count, y, w, h)

    def _motion(self):
        return "LEFT"


class UpDirection(Direction):
    def _coordinates(self, x, y, w, h):
        return (x, y - self.count, w, h)

    def _motion(self):
        return "UP"


class DownDirection(Direction):
    def _coordinates(self, x, y, w, h):
        return (x, y + self.count, w, h)

    def _motion(self):
        return "DOWN"
