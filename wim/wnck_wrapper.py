import itertools

from gi.repository import Wnck

from .wnck_state import WnckState


class WnckWrapper(object):
    def __init__(self, avoid):
        self._state = WnckState(avoid=avoid)

    def startup(self):
        self._state.connect_signals()
        return self

    def active_window(self):
        return self._state.active_window

    def prior_window(self):
        return self._state.prior_window

    def active_workspace(self):
        return self._state.active_workspace

    def active_workspace_windows(self):
        return self._state.workspaces[self.active_workspace()]

    def windows_in_workspace(self, workspace):
        return self._state.workspaces[workspace]

    def all_windows(self):
        return list(itertools.chain(*self._state.workspaces.values()))

    def geometry_for_window(self, window):
        if (window in self._state.windows
                and 'geometry' in self._state.windows[window]):
            return self._state.windows[window]['geometry']
        else:
            return Wnck.Window.get_geometry(window)

    def move_window_to_coordinates(self, window, x, y, w, h):
        Wnck.Window.set_geometry(
            window,
            Wnck.WindowGravity.STATIC,
            Wnck.WindowMoveResizeMask.X | Wnck.WindowMoveResizeMask.Y,
            x, y, w, h)

    def is_window_of_type(self, window, human):
        win_type = Wnck.Window.get_window_type(window)
        types = {
            'desktop': Wnck.WindowType.DESKTOP,
            'dialog': Wnck.WindowType.DIALOG,
            'dock': Wnck.WindowType.DOCK,
            'menu': Wnck.WindowType.MENU,
            'normal': Wnck.WindowType.NORMAL,
            'splashscreen': Wnck.WindowType.SPLASHSCREEN,
            'toolbar': Wnck.WindowType.TOOLBAR,
            'utility': Wnck.WindowType.UTILITY,
        }
        return (win_type == types[human])

    def get_motion_direction(self, attr):
        if hasattr(Wnck.MotionDirection, attr):
            return getattr(Wnck.MotionDirection, attr)

    def call_workspace(self, method, *args):
        return self._call(Wnck.Workspace, method, *args)

    def call_window(self, method, *args):
        return self._call(Wnck.Window, method, *args)

    def call_class_group(self, method, *args):
        return self._call(Wnck.ClassGroup, method, *args)

    def call_application(self, method, *args):
        return self._call(Wnck.Application, method, *args)

    def call_screen(self, method, *args):
        return self._call(Wnck.Screen, method, self._state.screen, *args)

    def _call(self, obj, method, *args):
        if hasattr(obj, method) and callable(getattr(obj, method)):
            return getattr(obj, method)(*args)
