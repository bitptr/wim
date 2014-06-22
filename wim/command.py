from __future__ import print_function

import datetime
import calendar
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


class ToggleShadeCommand(WindowCommand):
    def _modification(self, selection):
        if Wnck.Window.is_shaded(selection):
            Wnck.Window.unshade(selection)
        else:
            Wnck.Window.shade(selection)


class CloseCommand(WindowCommand):
    def _modification(self, selection):
        now = calendar.timegm(datetime.datetime.utcnow().timetuple())
        Wnck.Window.close(selection, now)


class PinCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.pin(selection)


class UnpinCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.unpin(selection)


class StickCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.stick(selection)


class UnstickCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.unstick(selection)


class SkipPagerCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.set_skip_pager(selection, True)


class SkipTasklistCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.set_skip_tasklist(selection, True)


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
