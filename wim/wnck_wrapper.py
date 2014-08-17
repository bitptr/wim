import itertools
import datetime
import calendar

from gi.repository import Wnck

from .wnck_state import WnckState


class WnckWrapper(object):
    def __init__(self, avoid):
        self.state = WnckState(avoid=avoid)

    def startup(self):
        self.state.connect_signals()
        return self

    @property
    def screen(self):
        return self.state.screen

    @property
    def workspaces(self):
        return self.state.workspaces

    @property
    def active_window(self):
        return self.state.active_window

    @property
    def prior_window(self):
        return self.state.prior_window

    @property
    def active_workspace(self):
        return self.state.active_workspace

    @property
    def windows(self):
        return self.state.windows

    def active_workspace_windows(self):
        return self.workspaces[self.active_workspace]

    def geometry_for(self, window):
        if window in self.windows and 'geometry' in self.windows[window]:
            return self.windows[window]['geometry']
        else:
            return Wnck.Window.get_geometry(window)

    def move_window_to_coordinates(self, window, x, y, w, h):
        Wnck.Window.set_geometry(
            window,
            Wnck.WindowGravity.STATIC,
            Wnck.WindowMoveResizeMask.X | Wnck.WindowMoveResizeMask.Y,
            x, y, w, h)

    def move_window_to_workspace(self, window, workspace):
        Wnck.Window.move_to_workspace(window, workspace)

    def activate_window(self, window):
        Wnck.Window.activate(window, self._now())

    def activate_workspace(self, workspace):
        Wnck.Workspace.activate(workspace, self._now())

    def workspace_number(self, number):
        return Wnck.Screen.get_workspace(self.screen, number)

    def by_xid(self, xid):
        return Wnck.Window.get(xid)

    def windows_for_group(self, group):
        return (Wnck.ClassGroup.get_windows(group) or [])

    def by_group(self, group):
        return Wnck.ClassGroup.get(group)

    def all_windows(self):
        return list(itertools.chain(*self.workspaces.values()))

    def window_name(self, window):
        return Wnck.Window.get_name(window)

    def window_pid(self, window):
        return Wnck.Window.get_pid(window)

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

    def _now(self):
        return calendar.timegm(datetime.datetime.utcnow().timetuple())
