from __future__ import print_function

from gi.repository import Wnck
import sys

from .util import maybe, singleton


class XidWindowsPredicate(object):
    def __init__(self, predicate_expr, model, is_global):
        self.predicate_expr = predicate_expr
        self.model = model

    def windows(self):
        return maybe([], singleton, self.model.by_xid(self.predicate))

    @property
    def predicate(self):
        xid = self.predicate_expr[-1]
        if xid[1] == 'x':
            return int(xid, 16)
        else:
            return int(xid)


class ClassWindowsPredicate(object):
    def __init__(self, predicate_expr, model, is_global):
        self.predicate_expr = predicate_expr
        self.model = model

    def windows(self):
        def group_windows(group):
            return self.model.windows_for_group(group)

        return maybe([], group_windows, self.model.by_group(self.predicate))

    @property
    def predicate(self):
        return self.predicate_expr[-1]


class AllWindowsFilter(object):
    def __init__(self, predicate_expr, model, is_global=False):
        self.predicate_expr = predicate_expr
        self.model = model
        self.is_global = is_global

    @property
    def predicate(self):
        return self.predicate_expr[-1]

    def windows(self):
        return filter(self._match, self._workspace())

    def _workspace(self):
        if self.is_global:
            return self.model.all_windows()
        else:
            return self.model.active_workspace_windows()

    def _match(self, window):
        return self._matcher(window)


class NameWindowsPredicate(AllWindowsFilter):
    def _matcher(self, window):
        name = self.model.window_name(window)
        return (name == self.predicate)


class PidWindowsPredicate(AllWindowsFilter):
    def _matcher(self, window):
        pid = self.model.window_pid(window)
        return (pid == int(self.predicate))


class TypeWindowsPredicate(AllWindowsFilter):
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


class OffsetWindowsPredicate(AllWindowsFilter):
    def __init__(self, predicate_expr, model):
        super(OffsetWindowsPredicate, self).__init__(predicate_expr, model)
        self.count = -1

    def _matcher(self, window):
        self.count += 1
        return (self.count == int(self.predicate))


class AllWindowsPredicate(AllWindowsFilter):
    def _matcher(self, window):
        return True


class UnknownPredicate(object):
    def __init__(self, predicate_expr, model, is_global):
        self.predicate_expr = predicate_expr

    def windows(self):
        self._print_error()
        return []

    def workspace(self):
        self._print_error()
        return None

    def _print_error(self):
        print("Unknown predicate: %s" % self.predicate_expr, file=sys.stderr)


class CurrentWorkspacePredicate(object):
    def __init__(self, predicate_expr, model, is_global):
        self.predicate_expr = predicate_expr
        self.model = model

    def workspace(self):
        return self.model.active_workspace


class NumberWorkspacePredicate(object):
    def __init__(self, predicate_expr, model, *args):
        self.predicate_expr = predicate_expr
        self.model = model

    def workspace(self):
        return self.model.workspace_number(int(self.predicate_expr[0]))
