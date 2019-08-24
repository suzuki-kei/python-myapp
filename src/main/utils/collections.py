from functools import reduce
from itertools import zip_longest


def flatten(*values):
    def generator(x):
        if isinstance(x, (list, tuple, set, range)):
            for value in x:
                yield from generator(value)
        else:
            yield x
    return list(generator(values))


def frequencies(values):
    def reducer(counts, value):
        counts[value] = counts.get(value, 0) + 1
        return counts
    return reduce(reducer, values, {})


def chunked(values, size, padding=None):
    if size < 1:
        raise ValueError("Invalid size", size)
    return zip_longest(*[iter(values)] * size, fillvalue=padding)

