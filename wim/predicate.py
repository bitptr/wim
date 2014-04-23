from gi.repository import Wnck


class XidPredicate(object):
    def __init__(self, predicate_expr):
        self.predicate_expr = predicate_expr

    def windows(self):
        window = Wnck.Window.get(self.predicate)

        if window is not None:
            return [window]
        else:
            return []

    @property
    def predicate(self):
        return int(self.predicate_expr[-1])
