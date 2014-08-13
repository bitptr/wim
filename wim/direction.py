from gi.repository import Wnck
import itertools

class Direction(object):
    def __init__(self, model, count):
        self.model = model
        self.count = count

    def move(self, window):
        (x, y, w, h) = self.model.geometry_for(window)
        self.model.move_window_to_coordinates(
            window, *self._coordinates(x, y, w, h))

    def jump(self, workspace):
        for _ in itertools.repeat(None, self.count):
            if workspace:
                workspace = Wnck.Workspace.get_neighbor(
                    workspace, self._motion())

        if workspace is not None:
            self.model.activate_workspace(workspace)

    def _coordinates(self, x, y, w, h):
        return (x, y, w, h)


class RightDirection(Direction):
    def _coordinates(self, x, y, w, h):
        return (x + self.count, y, w, h)

    def _motion(self):
        return Wnck.MotionDirection.RIGHT


class LeftDirection(Direction):
    def _coordinates(self, x, y, w, h):
        return (x - self.count, y, w, h)

    def _motion(self):
        return Wnck.MotionDirection.LEFT


class UpDirection(Direction):
    def _coordinates(self, x, y, w, h):
        return (x, y - self.count, w, h)

    def _motion(self):
        return Wnck.MotionDirection.UP


class DownDirection(Direction):
    def _coordinates(self, x, y, w, h):
        return (x, y + self.count, w, h)

    def _motion(self):
        return Wnck.MotionDirection.DOWN
