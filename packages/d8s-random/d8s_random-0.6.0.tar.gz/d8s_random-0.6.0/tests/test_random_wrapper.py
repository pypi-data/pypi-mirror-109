from d8s_random import random_dilbert_integer, random_shuffle, random_xkcd_integer


def test_random_xkcd_integer_docs_1():
    assert random_xkcd_integer() == 4


def test_random_dilbert_integer_docs_1():
    assert random_dilbert_integer() == 9


def test_random_shuffle_docs_1():
    r = random_shuffle([1, 2, 3])
    print(r)
    assert len(r) == 3
    assert 1 in r
    assert 2 in r
    assert 3 in r
