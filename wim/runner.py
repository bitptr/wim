from .selector import SelectorFactory
from .command import CommandFactory
from .object_factory import ObjectFactory


def Runner(expression, wnck_wrapper):
    selector = SelectorFactory(expression['selector'], expression,
                               wnck_wrapper)
    command = CommandFactory(expression['command'])
    obj = ObjectFactory(expression['direction'], expression, wnck_wrapper)
    return command(expression, selector, obj, wnck_wrapper)
