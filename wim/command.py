from .exception import WimException
from .util import now


class UnknownCommand:
    def __init__(self, expression, selector, obj, wnck_wrapper):
        self.expression = expression

    def run(self):
        command = self.expression.get('command')
        raise WimException("Unknown command: %s" % command)


class WindowCommand:
    def __init__(self, expression, selector, obj, wnck_wrapper):
        self.expression = expression
        self.selector = selector
        self.wnck_wrapper = wnck_wrapper

    def run(self):
        self.selector.runWindow(self._modification)


class ShadeCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("shade", selection)


class ToggleShadeCommand(WindowCommand):
    def _modification(self, selection):
        if self.wnck_wrapper.call_window("is_shaded", selection):
            self.wnck_wrapper.call_window("unshade", selection)
        else:
            self.wnck_wrapper.call_window("shade", selection)


class CloseCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("close", selection, now())


class PinCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("pin", selection)


class UnpinCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("unpin", selection)


class StickCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("stick", selection)


class UnstickCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("unstick", selection)


class SkipPagerCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("set_skip_pager", selection, True)


class SkipTasklistCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("set_skip_tasklist", selection, True)


class FullscreenCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("set_fullscreen", selection, True)


class MaximizeVerticalCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("maximize_vertically", selection)


class UnmaximizeVerticalCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("unmaximize_vertically", selection)


class MaximizeHorizontalCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("maximize_horizontally", selection)


class UnmaximizeHorizontalCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("unmaximize_horizontally", selection)


class MaximizeCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("maximize", selection)


class UnmaximizeCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("unmaximize", selection)


class MinimizeCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("minimize", selection)


class UnminimizeCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("unminimize", selection, now())


class AboveCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("make_above", selection)


class UnaboveCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("unmake_above", selection)


class BelowCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("make_below", selection)


class UnbelowCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("unmake_below", selection)


class KeyboardMoveCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("keyboard_move", selection)


class KeyboardSizeCommand(WindowCommand):
    def _modification(self, selection):
        self.wnck_wrapper.call_window("keyboard_size", selection)


class ActivateCommand(object):
    def __init__(self, expression, selector, obj, wnck_wrapper):
        self.selector = selector

    def run(self):
        self.selector.activate()


class MoveCommand(object):
    def __init__(self, expression, selector, obj, wnck_wrapper):
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
        }
        return mappings.get(str(command_expression), UnknownCommand)
