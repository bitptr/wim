from __future__ import print_function

from gi.repository import Wnck
import sys


class UnknownCommand:
    def __init__(self, expression, selector):
        self.expression = expression

    def run(self):
        command = self.expression['action']
        print("Unknown command: %s" % command, file=sys.stderr)


class Command:
    def __init__(self, expression, selector):
        self.expression = expression
        self.selector = selector

    def run(self):
        for selection in self.selector:
            self._modification(selection)


class ShadeCommand(Command):
    def _modification(self, selection):
        Wnck.Window.shade(selection)


class MaximizeVerticalCommand(Command):
    def _modification(self, selection):
        Wnck.Window.maximize_vertically(selection)


class UnmaximizeVerticalCommand(Command):
    def _modification(self, selection):
        Wnck.Window.unmaximize_vertically(selection)


class MaximizeHorizontalCommand(Command):
    def _modification(self, selection):
        Wnck.Window.maximize_horizontally(selection)


class UnmaximizeHorizontalCommand(Command):
    def _modification(self, selection):
        Wnck.Window.unmaximize_horizontally(selection)


class MaximizeCommand(Command):
    def _modification(self, selection):
        Wnck.Window.maximize(selection)


class UnmaximizeCommand(Command):
    def _modification(self, selection):
        Wnck.Window.unmaximize(selection)
