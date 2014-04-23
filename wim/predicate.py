from gi.repository import Wnck


class XidPredicate(object):
    def __init__(self, predicate_expr):
        self.predicate_expr = predicate_expr

    def windows(self):
        window = Wnck.Window.get(self.predicate)

        if window is not None:
            return [window]
        else:
            return []

    @property
    def predicate(self):
        return int(self.predicate_expr[-1])


class ClassPredicate(object):
    def __init__(self, predicate_expr):
        self.predicate_expr = predicate_expr

    def windows(self):
        group = Wnck.ClassGroup.get(self.predicate)

        if group is not None:
            return self._group_windows(group)
        else:
            return []

    def _group_windows(self, group):
        windows = Wnck.ClassGroup.get_windows(group)

        if windows is not None:
            return windows
        else:
            return []

    @property
    def predicate(self):
        return self.predicate_expr[-1]
