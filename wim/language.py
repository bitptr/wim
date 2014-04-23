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
                      UnmaximizeCommand)
from .selector import (UnknownSelector,
                       CurrentWindowSelector,
                       WindowPredicateSelector)


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
    (Literal('<') + Optional(predicates) + Literal('>'))('window'),
    Literal('[') + Optional(predicates) + Literal(']'),
    Literal('{') + Optional(predicates) + Literal('}'),
    Literal('%'),
    Literal('#')
])

parser = Or([
    selector('selector') + action('action') + obj('object'),
    other
]) + StringEnd()
parser.ignore(comment)


class Selector(object):
    def __new__(klass, selector_expr, expression):
        if selector_expr == '%':
            return CurrentWindowSelector(selector_expr, expression)
        elif selector_expr == '<':
            return WindowPredicateSelector(selector_expr, expression)
        else:
            return UnknownSelector(selector_expr, expression)


def Runner(expression):
    mappings = {
        's': ShadeCommand,
        'vM': MaximizeVerticalCommand,
        'uV': UnmaximizeVerticalCommand,
        'hM': MaximizeHorizontalCommand,
        'uH': UnmaximizeHorizontalCommand,
        'm': UnknownCommand,
        'tS': UnknownCommand,
        'j': UnknownCommand,
        'M': MaximizeCommand,
        'uM': UnmaximizeCommand,
        'x': UnknownCommand,
        'p': UnknownCommand,
        'uP': UnknownCommand,
        'S': UnknownCommand,
        'uS': UnknownCommand,
        'kP': UnknownCommand,
        'kT': UnknownCommand,
        'f': UnknownCommand,
        'n': UnknownCommand,
        'uN': UnknownCommand,
        'a': UnknownCommand,
        'uA': UnknownCommand,
        'b': UnknownCommand,
        'uB': UnknownCommand,
        'yM': UnknownCommand,
        'yS': UnknownCommand,
        'r': UnknownCommand,
        'wC': UnknownCommand,
        'wL': UnknownCommand,
    }
    selector = Selector(expression['selector'], expression)
    command = mappings.get(expression['action'], UnknownCommand)
    return command(expression, selector)
