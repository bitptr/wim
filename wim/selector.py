from __future__ import print_function

from gi.repository import Wnck
import sys


class CurrentWindowSelector(object):
    def __init__(self, selector_expr):
        self.selector_expr = selector_expr

    def runWindow(self, modification):
        modification(self._window())

    def _window(self):
        Wnck.Screen.force_update(self._screen())
        return Wnck.Screen.get_active_window(self._screen())

    def _screen(self):
        return Wnck.Screen.get_default()


class UnknownSelector(object):
    def __init__(self, selector_expr):
        self.selector_expr = selector_expr

    def runWindow(self, modification):
        print("Unknown selector: %s" % self.selector_expr, file=sys.stderr)
