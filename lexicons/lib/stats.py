

def mean(xs):
    return float(sum(xs)) / float(len(xs))


def variance(xs, xbar=None):
    if xbar is None:
        xbar = mean(xs)

    squared_error = [(x - xbar)**2 for x in xs]
    return mean(squared_error)


def sd(xs, xbar=None):
    return variance(xs, xbar)**0.5
