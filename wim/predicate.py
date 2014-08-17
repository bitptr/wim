from .util import maybe, singleton
from .exception import WimException


class XidWindowsPredicate(object):
    def __init__(self, predicate_expr, wnck_wrapper, is_global):
        self.predicate_expr = predicate_expr
        self.wnck_wrapper = wnck_wrapper

    def windows(self):
        return maybe([], singleton, self.wnck_wrapper.by_xid(self.predicate))

    @property
    def predicate(self):
        xid = self.predicate_expr[-1]
        if xid[1] == 'x':
            return int(xid, 16)
        else:
            return int(xid)


class ClassWindowsPredicate(object):
    def __init__(self, predicate_expr, wnck_wrapper, is_global):
        self.predicate_expr = predicate_expr
        self.wnck_wrapper = wnck_wrapper

    def windows(self):
        def group_windows(group):
            return self.wnck_wrapper.windows_for_group(group)

        return maybe([], group_windows,
                     self.wnck_wrapper.by_group(self.predicate))

    @property
    def predicate(self):
        return self.predicate_expr[-1]


class AllWindowsFilter(object):
    def __init__(self, predicate_expr, wnck_wrapper, is_global=False):
        self.predicate_expr = predicate_expr
        self.wnck_wrapper = wnck_wrapper
        self.is_global = is_global

    @property
    def predicate(self):
        return self.predicate_expr[-1]

    def windows(self):
        return filter(self._match, self._workspace())

    def _workspace(self):
        if self.is_global:
            return self.wnck_wrapper.all_windows()
        else:
            return self.wnck_wrapper.active_workspace_windows()

    def _match(self, window):
        return self._matcher(window)


class NameWindowsPredicate(AllWindowsFilter):
    def _matcher(self, window):
        name = self.wnck_wrapper.window_name(window)
        return (name == self.predicate)


class PidWindowsPredicate(AllWindowsFilter):
    def _matcher(self, window):
        pid = self.wnck_wrapper.window_pid(window)
        return (pid == int(self.predicate))


class TypeWindowsPredicate(AllWindowsFilter):
    def _matcher(self, window):
        return self.wnck_wrapper.is_window_of_type(window, self.predicate)


class OffsetWindowsPredicate(AllWindowsFilter):
    def __init__(self, predicate_expr, wnck_wrapper):
        super(OffsetWindowsPredicate, self).__init__(
            predicate_expr, wnck_wrapper)
        self.count = -1

    def _matcher(self, window):
        self.count += 1
        return (self.count == int(self.predicate))


class AllWindowsPredicate(AllWindowsFilter):
    def _matcher(self, window):
        return True


class UnknownPredicate(object):
    def __init__(self, predicate_expr, wnck_wrapper, is_global):
        self.predicate_expr = predicate_expr

    def windows(self):
        self._raise_error()
        return []

    def workspace(self):
        self._raise_error()
        return None

    def _raise_error(self):
        raise WimException("Unknown predicate: %s" % self.predicate_expr)


class CurrentWorkspacePredicate(object):
    def __init__(self, predicate_expr, wnck_wrapper, is_global):
        self.predicate_expr = predicate_expr
        self.wnck_wrapper = wnck_wrapper

    def workspace(self):
        return self.wnck_wrapper.active_workspace


class NumberWorkspacePredicate(object):
    def __init__(self, predicate_expr, wnck_wrapper, *args):
        self.predicate_expr = predicate_expr
        self.wnck_wrapper = wnck_wrapper

    def workspace(self):
        return self.wnck_wrapper.workspace_number(int(self.predicate_expr[0]))
