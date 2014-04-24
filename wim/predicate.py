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
        return filter(self._match, self.screen_windows)

    def _match(self, window):
        is_on_workspace = Wnck.Window.is_on_workspace(
            window, self.workspace)
        return is_on_workspace and self._matcher(window)

    @property
    def screen_windows(self):
        return Wnck.Screen.get_windows_stacked(self.screen)

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
        name = Wnck.Window.get_name(window)
        return (name == self.predicate)


class PidPredicate(AllWindowsFilter):
    def _matcher(self, window):
        pid = Wnck.Window.get_pid(window)
        return (pid == int(self.predicate))


class TypePredicate(AllWindowsFilter):
    def _matcher(self, window):
        win_type = Wnck.Window.get_window_type(window)
        return (win_type == self._win_type(self.predicate))

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


class OffsetPredicate(AllWindowsFilter):
    def __init__(self, predicate_expr):
        super(OffsetPredicate, self).__init__(predicate_expr)
        self.count = -1

    def _matcher(self, window):
        self.count += 1
        return (self.count == int(self.predicate))


class AllWindowsPredicate(AllWindowsFilter):
    def _matcher(self, window):
        return True
