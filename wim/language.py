from __future__ import print_function

from pyparsing import oneOf, StringEnd, Literal, Forward
from pyparsing import alphas, empty, nums, ZeroOrMore, Keyword, Regex
from pyparsing import Optional, Or, White, Word, OneOrMore
from gi.repository import Wnck

from .command import (UnknownCommand, ShadeCommand,
                      MaximizeVerticalCommand, UnmaximizeVerticalCommand)


number = OneOrMore(Word(nums))
string = OneOrMore(Word(alphas + '~-'))
regexp = Literal('/') + string + Literal('/')
x = Or([string, number, regexp])

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
    predicate
])

predicates = Forward()
predicates << Or([
    and_predicate + Literal(',') + predicates,
    and_predicate
])

comment = Regex('".*')

other = Or([Keyword('windows'), Keyword('desktop')])

selector = Forward()

obj = ZeroOrMore(oneOf(list(nums))) + Optional(Or([
    oneOf(['r', 'l', 'u', 'd', 'n', 's', 'e', 'w', 'p']),
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
    Literal('g') + selector,
    Literal('<') + Optional(predicates) + Literal('>'),
    Literal('[') + Optional(predicates) + Literal(']'),
    Literal('{') + Optional(predicates) + Literal('}'),
    Literal('%'),
    Literal('#')
])

parser = Or([
    selector.setResultsName('selector') +
    action.setResultsName('action') +
    obj.setResultsName('object'),
    other
]) + StringEnd()
parser.ignore(comment)


class Selector:
    def __init__(self, selector_expr):
        self.selector_expr = selector_expr

    def results(self):
        Wnck.Screen.force_update(self._screen())

        if self.selector_expr == '%':
            return [Wnck.Screen.get_active_window(self._screen())]
        else:
            return []

    def _screen(self):
        return Wnck.Screen.get_default()


def Runner(expression):
    mappings = {
        's': ShadeCommand,
        'vM': MaximizeVerticalCommand,
        'uV': UnmaximizeVerticalCommand,
    }
    selector = Selector(expression['selector']).results()
    command = mappings.get(expression['action'], UnknownCommand)
    return command(expression, selector)
