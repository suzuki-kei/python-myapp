
def flatten(*values):
    def generator(x):
        if isinstance(x, (list, tuple, set, range)):
            for value in x:
                yield from generator(value)
        else:
            yield x
    return list(generator(values))

