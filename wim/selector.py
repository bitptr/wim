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
from .exception import WimException


class SelectorFactory(object):
    def __new__(klass, selector_expr, expression, model,
                is_global=False):
        selectors = {'%': CurrentWindowSelector,
                     '#': PriorWindowSelector,
                     'g': GlobalSelector,
                     '<': WindowPredicateSelector,
                     '[': WorkspacePredicateSelector}
        klass = selectors.get(selector_expr, UnknownSelector)
        return klass(selector_expr, expression, model, is_global)


class GlobalSelector(object):
    def __new__(klass, _old_selector_expr, expression, model, is_global):
        selector_expr = drop_while(expression.get('global'),
                                   lambda e: e == 'g')[0]
        return SelectorFactory(selector_expr, expression, model,
                               is_global=True)


class UnknownSelector(object):
    def __init__(self, selector_expr, expr, model, is_global):
        self.selector_expr = selector_expr

    def runWindow(self, modification):
        self._raise_error()

    def moveTo(self, direction):
        self._raise_error()

    def move(self, window):
        self._raise_error()

    def _raise_error(self):
        raise WimException("Unknown selector: %s" % self.selector_expr)


class CurrentWindowSelector(object):
    def __init__(self, selector_expr, expr, model, is_global):
        self.selector_expr = selector_expr
        self.model = model

    def runWindow(self, modification):
        if self._window():
            modification(self._window())

    def moveTo(self, obj):
        obj.move(self._window())

    def move(self, window):
        raise WimException("Cannot move onto the current window")

    def activate(self):
        if self._window():
            self.model.activate_window(self._window())

    def _window(self):
        return self.model.active_window


class PriorWindowSelector(object):
    def __init__(self, selector_expr, expr, model, is_global):
        self.selector_expr = selector_expr
        self.model = model

    def runWindow(self, modification):
        if self._window():
            modification(self._window())

    def moveTo(self, obj):
        obj.move(self._window())

    def move(self, window):
        raise WimException("Cannot move onto the prior window")

    def activate(self):
        if self._window():
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
        self.runWindow(self.model.activate_window)

    def move(self, window):
        raise WimException("Cannot move onto a window predicate")

    def moveTo(self, obj):
        for window in self._windows():
            obj.move(window)

    def _windows(self):
        return self._predicate().windows()

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
        self.is_global = is_global

    def _workspace(self):
        return self._predicate().workspace()

    def _windows(self):
        return self.model.workspaces[self._workspace()]

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

    def moveTo(self, obj):
        obj.jump(self._workspace())

    def activate(self):
        workspace = self._workspace()
        if workspace:
            self.model.activate_workspace(workspace)

    def runWindow(self, modification):
        map(modification, self._windows())

    @property
    def predicate_expr(self):
        return self.expression['workspace'][1:-1]
