from __future__ import print_function

import sys

from .predicate import (XidPredicate,
                        ClassPredicate,
                        NamePredicate,
                        PidPredicate,
                        TypePredicate,
                        OffsetPredicate,
                        AllWindowsPredicate,
                        UnknownPredicate)


class SelectorFactory(object):
    def __new__(klass, selector_expr, expression, model):
        if selector_expr == '%':
            return CurrentWindowSelector(selector_expr, expression, model)
        elif selector_expr == '#':
            return PriorWindowSelector(selector_expr, expression, model)
        elif selector_expr == '<':
            return WindowPredicateSelector(selector_expr, expression, model)
        else:
            return UnknownSelector(selector_expr, expression, model)


class UnknownSelector(object):
    def __init__(self, selector_expr, expr, model):
        self.selector_expr = selector_expr

    def runWindow(self, modification):
        print("Unknown selector: %s" % self.selector_expr, file=sys.stderr)


class CurrentWindowSelector(object):
    def __init__(self, selector_expr, expr, model):
        self.selector_expr = selector_expr
        self.model = model

    def runWindow(self, modification):
        modification(self._window())

    def moveTo(self, direction):
        direction.move(self._window())

    def _window(self):
        return self.model.active_window


class PriorWindowSelector(object):
    def __init__(self, selector_expr, expr, model):
        self.selector_expr = selector_expr
        self.model = model

    def runWindow(self, modification):
        modification(self._window())

    def moveTo(self, direction):
        direction.move(self._window())

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
            return XidPredicate(self.predicate_expr, self.model)
        elif self.predicate_expr[0] == '.':
            return ClassPredicate(self.predicate_expr, self.model)
        elif self.predicate_expr[0] == '@':
            return NamePredicate(self.predicate_expr, self.model)
        elif self.predicate_expr[0] == '&':
            return PidPredicate(self.predicate_expr, self.model)
        elif self.predicate_expr[0] == '?':
            return TypePredicate(self.predicate_expr, self.model)
        elif self.predicate_expr[0].isdigit():
            return OffsetPredicate(self.predicate_expr, self.model)
        else:
            return UnknownPredicate(self.predicate_expr, self.model)

    @property
    def predicate_expr(self):
        return self.expression['window'][1:-1]
