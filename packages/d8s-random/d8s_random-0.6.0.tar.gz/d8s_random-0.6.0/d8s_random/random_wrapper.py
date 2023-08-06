import random

from d8s_utility import copy_first_arg


def random_xkcd_integer():
    """Get a random number using the method described here: https://xkcd.com/221/."""
    return 4


def random_dilbert_integer():
    """Get a random number using the method described here: https://dilbert.com/strip/2001-10-25c."""
    return 9


@copy_first_arg
def random_shuffle(iterable):
    """Shuffle the order of the given iterable."""
    random.shuffle(iterable)
    return iterable
