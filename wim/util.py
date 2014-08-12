def maybe(base, f, potential):
    if potential is None:
        return base
    else:
        return f(potential)


def singleton(x):
    return [x]


def drop_while(l, p):
    if l == []:
        return []
    elif p(l[0]):
        return drop_while(l[1:], p)
    else:
        return l
