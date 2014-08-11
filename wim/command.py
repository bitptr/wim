from __future__ import print_function

import datetime
import calendar
from gi.repository import Wnck
import sys


class UnknownCommand:
    def __init__(self, expression, selector, obj):
        self.expression = expression

    def run(self):
        command = self.expression.get('command')
        print("Unknown command: %s" % command, file=sys.stderr)


class NullCommand:
    def __init__(self, expression, selector, obj):
        pass

    def run(self):
        pass


class WindowCommand:
    def __init__(self, expression, selector, obj):
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


class FullscreenCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.set_fullscreen(selection, True)


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


class MinimizeCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.minimize(selection)


class UnminimizeCommand(WindowCommand):
    def _modification(self, selection):
        now = calendar.timegm(datetime.datetime.utcnow().timetuple())
        Wnck.Window.unminimize(selection, now)


class AboveCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.make_above(selection)


class UnaboveCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.unmake_above(selection)


class BelowCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.make_below(selection)


class UnbelowCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.unmake_below(selection)


class KeyboardMoveCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.keyboard_move(selection)


class KeyboardSizeCommand(WindowCommand):
    def _modification(self, selection):
        Wnck.Window.keyboard_size(selection)


class ActivateCommand(object):
    def __init__(self, expression, selector, obj):
        self.selector = selector

    def run(self):
        self.selector.activate()


class MoveCommand(object):
    def __init__(self, expression, selector, obj):
        self.selector = selector
        self.obj = obj

    def run(self):
        self.selector.moveTo(self.obj)


class CommandFactory(object):

    def __new__(klass, command_expression):
        mappings = {
            's': ShadeCommand,
            'vM': MaximizeVerticalCommand,
            'uV': UnmaximizeVerticalCommand,
            'hM': MaximizeHorizontalCommand,
            'uH': UnmaximizeHorizontalCommand,
            'm': MoveCommand,
            'tS': ToggleShadeCommand,
            'j': ActivateCommand,
            'M': MaximizeCommand,
            'uM': UnmaximizeCommand,
            'x': CloseCommand,
            'p': PinCommand,
            'uP': UnpinCommand,
            'S': StickCommand,
            'uS': UnstickCommand,
            'kP': SkipPagerCommand,
            'kT': SkipTasklistCommand,
            'f': FullscreenCommand,
            'n': MinimizeCommand,
            'uN': UnminimizeCommand,
            'a': AboveCommand,
            'uA': UnaboveCommand,
            'b': BelowCommand,
            'uB': UnbelowCommand,
            'yM': KeyboardMoveCommand,
            'yS': KeyboardSizeCommand,
            'r': UnknownCommand,
            'wC': UnknownCommand,
            'wL': UnknownCommand,
            '[]': ActivateCommand,
            'None': NullCommand,
        }
        return mappings.get(str(command_expression), UnknownCommand)
