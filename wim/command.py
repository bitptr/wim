from __future__ import print_function

from gi.repository import Wnck
import sys


class UnknownCommand:
    def __init__(self, expression, selector):
        self.expression = expression

    def run(self):
        command = self.expression['action']
        print("Unknown command: %s" % command, file=sys.stderr)


class WindowCommand:
    def __init__(self, expression, selector):
        self.expression = expression
        self.selector = selector

    def run(self):
        self.selector.runWindow(self._modification)


class ShadeCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.shade(selection)


class MaximizeVerticalCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.maximize_vertically(selection)


class UnmaximizeVerticalCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.unmaximize_vertically(selection)


class MaximizeHorizontalCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.maximize_horizontally(selection)


class UnmaximizeHorizontalCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.unmaximize_horizontally(selection)


class MaximizeCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.maximize(selection)


class UnmaximizeCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.unmaximize(selection)
