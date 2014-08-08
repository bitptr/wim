from .selector import SelectorFactory
from .command import CommandFactory
from .object_factory import ObjectFactory


def Runner(expression, model):
    selector = SelectorFactory(expression.get('selector'), expression, model)
    command = CommandFactory(expression.get('command'))
    obj = ObjectFactory(expression.get('direction'), expression, model)
    return command(expression, selector, obj)
