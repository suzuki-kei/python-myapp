from functools import reduce


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

