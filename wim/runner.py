from .selector import SelectorFactory
from .command import CommandFactory
from .object_factory import ObjectFactory


def Runner(expression, model):
    selector = SelectorFactory(expression['selector'], expression, model)
    command = CommandFactory(expression['action'])
    obj = ObjectFactory(expression['direction'], expression, model)
    return command(expression, selector, obj)
