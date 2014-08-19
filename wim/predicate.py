from .util import maybe, singleton, str_to_xid
from .exception import WimException


class XidWindowsPredicate(object):
    def __init__(self, predicate_expr, wnck_wrapper, is_global):
        self.predicate_expr = predicate_expr
        self.wnck_wrapper = wnck_wrapper
        self.is_global = is_global

    def windows(self):
        return maybe([], singleton, self._window())

    def _window(self):
        window = self.wnck_wrapper.call_window("get", self.predicate)
        if (self.is_global
                or window in self.wnck_wrapper.active_workspace_windows()):
            return window
        else:
            return None

    @property
    def predicate(self):
        return str_to_xid(self.predicate_expr[-1])


class ClassWindowsPredicate(object):
    def __init__(self, predicate_expr, wnck_wrapper, is_global):
        self.predicate_expr = predicate_expr
        self.wnck_wrapper = wnck_wrapper
        self.is_global = is_global

    def windows(self):
        def group_windows(group):
            return (self.wnck_wrapper.call_class_group("get_windows", group)
                    or [])

        all_windows = maybe([], group_windows,
                            self.wnck_wrapper.call_class_group(
                                "get", self.predicate))
        if self.is_global:
            return all_windows
        else:
            current_windows = self.wnck_wrapper.active_workspace_windows()
            return [window for window in all_windows
                    if window in current_windows]

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
        name = self.wnck_wrapper.call_window("get_name", window)
        return (name == self.predicate)


class PidWindowsPredicate(AllWindowsFilter):
    def _matcher(self, window):
        pid = self.wnck_wrapper.call_window("get_pid", window)
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


class InvalidPredicate(object):
    def __init__(self, predicate_expr, wnck_wrapper, is_global):
        self.predicate_expr = predicate_expr

    def windows(self):
        self._raise_error()
        return []

    def workspace(self):
        self._raise_error()
        return None

    def _raise_error(self):
        raise WimException("Invalid predicate: %s" % self.predicate_expr)


class CurrentWorkspacePredicate(object):
    def __init__(self, predicate_expr, wnck_wrapper, is_global):
        self.predicate_expr = predicate_expr
        self.wnck_wrapper = wnck_wrapper

    def workspace(self):
        return self.wnck_wrapper.active_workspace()


class NumberWorkspacePredicate(object):
    def __init__(self, predicate_expr, wnck_wrapper, *args):
        self.predicate_expr = predicate_expr
        self.wnck_wrapper = wnck_wrapper

    def workspace(self):
        return self.wnck_wrapper.call_screen("get_workspace",
                                             (int(self.predicate_expr[0])))


class ApplicationPredicate(object):
    def __init__(self, predicate_expr, wnck_wrapper, is_global):
        self.predicate_expr = predicate_expr
        self.wnck_wrapper = wnck_wrapper
        self.is_global = is_global

    def windows(self):
        return filter(self._match, self._workspace())

    def _workspace(self):
        if self.is_global:
            return self.wnck_wrapper.all_windows()
        else:
            return self.wnck_wrapper.active_workspace_windows()

    def _match(self, window):
        application = self.wnck_wrapper.call_window("get_application", window)
        if application:
            return self._property(application) == self.predicate
        else:
            return False

    def _property(self, application):
        return self.wnck_wrapper.call_application(
            self._application_property_get_method(), application)


class XidApplicationPredicate(ApplicationPredicate):
    def _application_property_get_method(self):
        return "get_xid"

    @property
    def predicate(self):
        return str_to_xid(self.predicate_expr[-1])


class NameApplicationPredicate(ApplicationPredicate):
    def _application_property_get_method(self):
        return "get_name"

    @property
    def predicate(self):
        return self.predicate_expr[-1]


class PidApplicationPredicate(ApplicationPredicate):
    def _application_property_get_method(self):
        return "get_pid"

    @property
    def predicate(self):
        return int(self.predicate_expr[-1])
