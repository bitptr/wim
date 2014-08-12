from __future__ import print_function

import sys

from .util import drop_while
from .predicate import (XidWindowsPredicate,
                        ClassWindowsPredicate,
                        NameWindowsPredicate,
                        PidWindowsPredicate,
                        TypeWindowsPredicate,
                        OffsetWindowsPredicate,
                        AllWindowsPredicate,
                        CurrentWorkspacePredicate,
                        NumberWorkspacePredicate,
                        UnknownPredicate)


class SelectorFactory(object):
    def __new__(klass, selector_expr, expression, model,
                is_global=False):
        selectors = {'%': CurrentWindowSelector,
                     '#': PriorWindowSelector,
                     'g': GlobalSelector,
                     '<': WindowPredicateSelector,
                     '[': WorkspacePredicateSelector,
                     None: NullSelector}
        klass = selectors.get(selector_expr, UnknownSelector)
        return klass(selector_expr, expression, model, is_global)


class GlobalSelector(object):
    def __new__(klass, _old_selector_expr, expression, model, is_global):
        selector_expr = drop_while(expression.get('global'),
                                   lambda e: e == 'g')[0]
        return SelectorFactory(selector_expr, expression, model,
                               is_global=True)


class NullSelector(object):
    def __init__(self, selector_expr, expr, model, is_global):
        pass

    def runWindow(self, modification):
        pass


class UnknownSelector(object):
    def __init__(self, selector_expr, expr, model, is_global):
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
    def __init__(self, selector_expr, expr, model, is_global):
        self.selector_expr = selector_expr
        self.model = model

    def runWindow(self, modification):
        modification(self._window())

    def moveTo(self, obj):
        obj.move(self._window())

    def move(self, window):
        print("Cannot move onto the current window")

    def activate(self):
        self.model.activate_window(self._window())

    def _window(self):
        return self.model.active_window


class PriorWindowSelector(object):
    def __init__(self, selector_expr, expr, model, is_global):
        self.selector_expr = selector_expr
        self.model = model

    def runWindow(self, modification):
        modification(self._window())

    def moveTo(self, obj):
        obj.move(self._window())

    def move(self, window):
        print("Cannot move onto the prior window")

    def activate(self):
        self.model.activate_window(self._window())

    def _window(self):
        return self.model.prior_window


class WindowPredicateSelector(object):
    def __init__(self, selector_expr, expression, model,
                 is_global):
        self.selector_expr = selector_expr
        self.expression = expression
        self.model = model
        self.is_global = is_global

    def runWindow(self, modification):
        for window in self._windows():
            modification(window)

    def activate(self):
        windows = self._windows()
        if not windows:
            pass
        elif len(windows) != 1:
            print("Only window may be activated at a time")
        else:
            self.model.activate_window(windows[0])

    def move(self, window):
        print("Cannot move onto a window predicate")

    def _windows(self):
        windows = self._predicate().windows()
        if len(windows) == 0:
            print("No match", file=sys.stderr)
        return windows

    def _predicate(self):
        def predicate_klass():
            if len(self.predicate_expr) == 0:
                return AllWindowsPredicate
            elif self.predicate_expr[0].isdigit():
                return OffsetWindowsPredicate
            else:
                predicates = {'#': XidWindowsPredicate,
                              '.': ClassWindowsPredicate,
                              '@': NameWindowsPredicate,
                              '&': PidWindowsPredicate,
                              '?': TypeWindowsPredicate}
                return predicates.get(self.predicate_expr[0],
                                      UnknownPredicate)

        return predicate_klass()(self.predicate_expr,
                                 self.model,
                                 self.is_global)

    @property
    def predicate_expr(self):
        return self.expression['window'][1:-1]


class WorkspacePredicateSelector(object):

    def __init__(self, selector_expr, expression, model, is_global):
        self.selector_expr = selector_expr
        self.expression = expression
        self.model = model
        self.is_global

    def _workspace(self):
        return self._predicate().workspace()

    def _predicate(self):
        def predicate_klass():
            if len(self.predicate_expr) == 0:
                return CurrentWorkspacePredicate
            elif self.predicate_expr[0].isdigit():
                return NumberWorkspacePredicate
            else:
                return UnknownPredicate
        return predicate_klass()(self.predicate_expr,
                                 self.model,
                                 self.is_global)

    def move(self, window):
        self.model.move_window_to_workspace(window, self._workspace())

    def activate(self):
        workspace = self._workspace()
        if workspace:
            self.model.activate_workspace(workspace)
        else:
            print("No such workspace: %s" % self.predicate_expr[0])

    def runWindow(self, modification):
        print("Window commands cannot be run on workspaces")

    @property
    def predicate_expr(self):
        return self.expression['workspace'][1:-1]
