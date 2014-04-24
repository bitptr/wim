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
