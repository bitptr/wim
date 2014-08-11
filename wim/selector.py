from __future__ import print_function

import sys

from .predicate import (XidWindowsPredicate,
                        ClassWindowsPredicate,
                        NameWindowsPredicate,
                        PidWindowsPredicate,
                        TypeWindowsPredicate,
                        OffsetWindowsPredicate,
                        AllWindowsPredicate,
                        CurrentWorkspacePredicate,
                        NumberWorkspaceSelector,
                        UnknownPredicate)


class SelectorFactory(object):
    def __new__(klass, selector_expr, expression, model):
        if selector_expr == '%':
            return CurrentWindowSelector(selector_expr, expression, model)
        elif selector_expr == '#':
            return PriorWindowSelector(selector_expr, expression, model)
        elif selector_expr == '<':
            return WindowPredicateSelector(selector_expr, expression, model)
        elif selector_expr == '[':
            return WorkspacePredicateSelector(selector_expr, expression, model)
        elif selector_expr is None:
            return NullSelector(selector_expr, expression, model)
        else:
            return UnknownSelector(selector_expr, expression, model)


class NullSelector(object):
    def __init__(self, selector_expr, expr, model):
        pass

    def runWindow(self, modification):
        pass


class UnknownSelector(object):
    def __init__(self, selector_expr, expr, model):
        self.selector_expr = selector_expr

    def runWindow(self, modification):
        self._print_error()

    def moveTo(self, direction):
        self._print_error()

    def move(self, window):
        self._print_error()

    def _print_error(self):
        print("Unknown selector: %s" % self.selector_expr, file=sys.stderr)


class CurrentWindowSelector(object):
    def __init__(self, selector_expr, expr, model):
        self.selector_expr = selector_expr
        self.model = model

    def runWindow(self, modification):
        modification(self._window())

    def moveTo(self, obj):
        obj.move(self._window())

    def move(self, window):
        print("Cannot move onto the current window")

    def _window(self):
        return self.model.active_window


class PriorWindowSelector(object):
    def __init__(self, selector_expr, expr, model):
        self.selector_expr = selector_expr
        self.model = model

    def runWindow(self, modification):
        modification(self._window())

    def moveTo(self, obj):
        obj.move(self._window())

    def move(self, window):
        print("Cannot move onto the prior window")

    def _window(self):
        return self.model.prior_window


class WindowPredicateSelector(object):
    def __init__(self, selector_expr, expression, model):
        self.selector_expr = selector_expr
        self.expression = expression
        self.model = model

    def runWindow(self, modification):
        for window in self._windows():
            modification(window)

    def move(self, window):
        print("Cannot move onto a window predicate")

    def _windows(self):
        windows = self._predicate().windows()

        if len(windows) == 0:
            print("No match", file=sys.stderr)
            return []
        else:
            return windows

    def _predicate(self):
        if len(self.predicate_expr) == 0:
            return AllWindowsPredicate(self.predicate_expr, self.model)
        elif self.predicate_expr[0] == '#':
            return XidWindowsPredicate(self.predicate_expr, self.model)
        elif self.predicate_expr[0] == '.':
            return ClassWindowsPredicate(self.predicate_expr, self.model)
        elif self.predicate_expr[0] == '@':
            return NameWindowsPredicate(self.predicate_expr, self.model)
        elif self.predicate_expr[0] == '&':
            return PidWindowsPredicate(self.predicate_expr, self.model)
        elif self.predicate_expr[0] == '?':
            return TypeWindowsPredicate(self.predicate_expr, self.model)
        elif self.predicate_expr[0].isdigit():
            return OffsetWindowsPredicate(self.predicate_expr, self.model)
        else:
            return UnknownPredicate(self.predicate_expr, self.model)

    @property
    def predicate_expr(self):
        return self.expression['window'][1:-1]


class WorkspacePredicateSelector(object):

    def __init__(self, selector_expr, expression, model):
        self.selector_expr = selector_expr
        self.expression = expression
        self.model = model

    def _workspace(self):
        return self._predicate().workspace()

    def _predicate(self):
        if len(self.predicate_expr) == 0:
            return CurrentWorkspacePredicate(self.predicate_expr, self.model)
        elif self.predicate_expr[0].isdigit():
            return NumberWorkspaceSelector(self.predicate_expr, self.model)
        else:
            return UnknownPredicate(self.predicate_expr, self.model)

    def move(self, window):
        self.model.move_window_to_workspace(window, self._workspace())

    def runWindow(self, modification):
        print("Window commands cannot be run on workspaces")

    @property
    def predicate_expr(self):
        return self.expression['workspace'][1:-1]
