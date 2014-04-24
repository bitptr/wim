def maybe(base, f, potential):
    if potential is None:
        return base
    else:
        return f(potential)


def singleton(x):
    return [x]
