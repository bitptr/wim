from __future__ import print_function

from gi.repository import Wnck
import sys

from .util import maybe, singleton


class XidPredicate(object):
    def __init__(self, predicate_expr, model):
        self.predicate_expr = predicate_expr

    def windows(self):
        return maybe([], singleton, Wnck.Window.get(self.predicate))

    @property
    def predicate(self):
        return int(self.predicate_expr[-1])


class ClassPredicate(object):
    def __init__(self, predicate_expr, model):
        self.predicate_expr = predicate_expr

    def windows(self):
        def group_windows(group):
            return (Wnck.ClassGroup.get_windows(group) or [])

        return maybe([], group_windows, Wnck.ClassGroup.get(self.predicate))

    @property
    def predicate(self):
        return self.predicate_expr[-1]


class AllWindowsFilter(object):
    def __init__(self, predicate_expr, model):
        self.predicate_expr = predicate_expr
        self.model = model

    @property
    def predicate(self):
        return self.predicate_expr[-1]

    def windows(self):
        return filter(self._match, self.model.active_workspace_windows())

    def _match(self, window):
        return self._matcher(window)


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
    def __init__(self, predicate_expr, model):
        super(OffsetPredicate, self).__init__(predicate_expr, model)
        self.count = -1

    def _matcher(self, window):
        self.count += 1
        return (self.count == int(self.predicate))


class AllWindowsPredicate(AllWindowsFilter):
    def _matcher(self, window):
        return True


class UnknownPredicate(object):
    def __init__(self, predicate_expr, model):
        self.predicate_expr = predicate_expr

    def windows(self):
        print("Unknown predicate: %s" % self.predicate_expr, file=sys.stderr)
        return []
