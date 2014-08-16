from pyparsing import (oneOf, StringEnd, Literal, Forward, Suppress, hexnums,
                       alphas, empty, nums, ZeroOrMore, Keyword, Regex,
                       Combine, Optional, Or, White, Word, OneOrMore)


number = OneOrMore(Word(nums))
string = OneOrMore(Word(alphas + '~-/'))
hexnumber = Combine(Literal('0x') + OneOrMore(Word(hexnums)))
x = (hexnumber | number | string)('identifier')

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

comment = Regex('".*')('comment')

other = Or([Keyword('windows'), Keyword('desktop')])

selector = Forward()

direction = ZeroOrMore(oneOf(list(nums)))('count') + Optional(Or([
    oneOf(['r', 'l', 'u', 'd', 'n', 's', 'e', 'w', 'p'])('logical'),
    selector
]))

command = (Literal('s')
           | Literal('vM')
           | Literal('uV')
           | Literal('hM')
           | Literal('uH')
           | Literal('m')
           | Literal('tS')
           | Literal('j')
           | Literal('M')
           | Literal('uM')
           | Literal('x')
           | Literal('p')
           | Literal('uP')
           | Literal('S')
           | Literal('uS')
           | Literal('kP')
           | Literal('kT')
           | Literal('f')
           | Literal('n')
           | Literal('uN')
           | Literal('a')
           | Literal('uA')
           | Literal('b')
           | Literal('uB')
           | Literal('yM')
           | Literal('yS')
           | Literal('r')
           | Literal('wC')
           | Literal('wL')
           | empty)

selector << Or([
    (Literal('g') + selector)('global'),
    (Literal('<') + Optional(predicates) + Literal('>'))('window'),
    (Literal('[') + Optional(predicates) + Literal(']'))('workspace'),
    (Literal('{') + Optional(predicates) + Literal('}'))('application'),
    Literal('%')('current'),
    Literal('#')('prior')
])

parser = Or([
    Suppress(ZeroOrMore(White())),
    selector('selector') + command('command') + direction('direction'),
    other,
]) + ZeroOrMore(comment) + StringEnd()
