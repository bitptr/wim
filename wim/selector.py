from __future__ import print_function

from gi.repository import Wnck
import sys

from .predicate import (XidPredicate,
                        ClassPredicate,
                        NamePredicate)


class UnknownSelector(object):
    def __init__(self, selector_expr, expr):
        self.selector_expr = selector_expr

    def runWindow(self, modification):
        print("Unknown selector: %s" % self.selector_expr, file=sys.stderr)


class CurrentWindowSelector(object):
    def __init__(self, selector_expr, expr):
        self.selector_expr = selector_expr

    def runWindow(self, modification):
        modification(self._window())

    def _window(self):
        Wnck.Screen.force_update(self._screen())
        return Wnck.Screen.get_active_window(self._screen())

    def _screen(self):
        return Wnck.Screen.get_default()


class WindowPredicateSelector(object):
    def __init__(self, selector_expr, expression):
        self.selector_expr = selector_expr
        self.expression = expression

    def runWindow(self, modification):
        for window in self._windows():
            modification(window)

    def _windows(self):
        Wnck.Screen.force_update(self._screen())
        windows = self._predicate().windows()

        if len(windows) == 0:
            print("No match", file=sys.stderr)
            return []
        else:
            return windows

    def _predicate(self):
        if self.predicate_expr[0] == '#':
            return XidPredicate(self.predicate_expr)
        elif self.predicate_expr[0] == '.':
            return ClassPredicate(self.predicate_expr)
        elif self.predicate_expr[0] == '@':
            return NamePredicate(self.predicate_expr)
        elif self.predicate_expr[0] == '&':
            pass
        elif self.predicate_expr[0] == '?':
            pass
        elif self.predicate_expr[0].isdigit():
            pass
        else:
            pass

    @property
    def predicate_expr(self):
        return self.expression['window'][1:-1]

    def _screen(self):
        return Wnck.Screen.get_default()
