from __future__ import print_function

from pyparsing import oneOf, StringEnd, Literal, Forward
from pyparsing import alphas, empty, nums, ZeroOrMore, Keyword, Regex
from pyparsing import Optional, Or, White, Word, OneOrMore

from .command import (UnknownCommand,
                      ShadeCommand,
                      MaximizeVerticalCommand,
                      UnmaximizeVerticalCommand,
                      MaximizeHorizontalCommand,
                      UnmaximizeHorizontalCommand,
                      MaximizeCommand,
                      UnmaximizeCommand,
                      ToggleShadeCommand,
                      CloseCommand,
                      PinCommand,
                      UnpinCommand,
                      StickCommand,
                      UnstickCommand,
                      SkipPagerCommand,
                      SkipTasklistCommand,
                      FullscreenCommand,
                      MinimizeCommand,
                      UnminimizeCommand,
                      AboveCommand,
                      UnaboveCommand,
                      BelowCommand,
                      UnbelowCommand,
                      KeyboardMoveCommand,
                      KeyboardSizeCommand,
                      MoveCommand)
from .selector import Selector
from .direction import Direction


number = OneOrMore(Word(nums))
string = OneOrMore(Word(alphas + '~-/'))
regexp = Literal('/') + string + Literal('/')
x = Or([string, number, regexp])('identifier')

predicate = Or([
    Literal('#') + x,
    Literal('.') + x,
    Literal('@') + x,
    Literal('&') + x,
    Literal('?') + x,
    x
])

and_predicate = Forward()
and_predicate << Or([
    predicate + White() + and_predicate,
    predicate('predicate')
])

predicates = Forward()
predicates << Or([
    and_predicate + Literal(',') + predicates,
    and_predicate
])

comment = Regex('".*')

other = Or([Keyword('windows'), Keyword('desktop')])

selector = Forward()

direction = ZeroOrMore(oneOf(list(nums)))('count') + Optional(Or([
    oneOf(['r', 'l', 'u', 'd', 'n', 's', 'e', 'w', 'p'])('logical'),
    selector
]))

action = Or([
    Literal('s'),
    Literal('vM'),
    Literal('uV'),
    Literal('hM'),
    Literal('uH'),
    Literal('m'),
    Literal('tS'),
    Literal('j'),
    Literal('M'),
    Literal('uM'),
    Literal('x'),
    Literal('p'),
    Literal('uP'),
    Literal('S'),
    Literal('uS'),
    Literal('kP'),
    Literal('kT'),
    Literal('f'),
    Literal('n'),
    Literal('uN'),
    Literal('a'),
    Literal('uA'),
    Literal('b'),
    Literal('uB'),
    Literal('yM'),
    Literal('yS'),
    Literal('r'),
    Literal('wC'),
    Literal('wL'),
    empty
])

selector << Or([
    (Literal('g') + selector)('global'),
    (Literal('<') + Optional(predicates) + Literal('>'))('window'),
    (Literal('[') + Optional(predicates) + Literal(']'))('workspace'),
    (Literal('{') + Optional(predicates) + Literal('}'))('application'),
    Literal('%')('current'),
    Literal('#')('prior')
])

parser = Or([
    selector('selector') + action('action') + direction('direction'),
    other
]) + StringEnd()
parser.ignore(comment)


def Runner(expression, model):
    mappings = {
        's': ShadeCommand,
        'vM': MaximizeVerticalCommand,
        'uV': UnmaximizeVerticalCommand,
        'hM': MaximizeHorizontalCommand,
        'uH': UnmaximizeHorizontalCommand,
        'm': MoveCommand,
        'tS': ToggleShadeCommand,
        'j': UnknownCommand,
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
    }
    selector = Selector(expression['selector'], expression, model)
    command = mappings.get(expression['action'], UnknownCommand)
    direction = Direction(expression['direction'], expression, model)
    return command(expression, selector, direction)
