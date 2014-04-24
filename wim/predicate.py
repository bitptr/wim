from gi.repository import Wnck

from .util import maybe, singleton


class XidPredicate(object):
    def __init__(self, predicate_expr):
        self.predicate_expr = predicate_expr

    def windows(self):
        return maybe([], singleton, Wnck.Window.get(self.predicate))

    @property
    def predicate(self):
        return int(self.predicate_expr[-1])


class ClassPredicate(object):
    def __init__(self, predicate_expr):
        self.predicate_expr = predicate_expr

    def windows(self):
        def group_windows(group):
            return (Wnck.ClassGroup.get_windows(group) or [])

        return maybe([], group_windows, Wnck.ClassGroup.get(self.predicate))

    @property
    def predicate(self):
        return self.predicate_expr[-1]


class AllWindowsFilter(object):
    def __init__(self, predicate_expr):
        self.predicate_expr = predicate_expr

    def windows(self):
        return filter(self._matcher, self.screen_windows)

    @property
    def screen_windows(self):
        return Wnck.Screen.get_windows(self.screen)

    @property
    def screen(self):
        return Wnck.Screen.get_default()

    @property
    def predicate(self):
        return self.predicate_expr[-1]

    @property
    def workspace(self):
        return Wnck.Screen.get_active_workspace(self.screen)


class NamePredicate(AllWindowsFilter):
    def _matcher(self, window):
        is_on_workspace = Wnck.Window.is_on_workspace(
            window, self.workspace)
        name = Wnck.Window.get_name(window)
        return is_on_workspace and (name == self.predicate)


class PidPredicate(AllWindowsFilter):
    def _matcher(self, window):
        is_on_workspace = Wnck.Window.is_on_workspace(
            window, self.workspace)
        pid = Wnck.Window.get_pid(window)
        return is_on_workspace and (pid == int(self.predicate))


class TypePredicate(AllWindowsFilter):
    def _matcher(self, window):
        is_on_workspace = Wnck.Window.is_on_workspace(
            window, self.workspace)
        win_type = Wnck.Window.get_window_type(window)
        return is_on_workspace and (win_type == self._win_type(self.predicate))

    def _win_type(self, human):
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
        return types[human]
