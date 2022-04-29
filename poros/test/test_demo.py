import pytest


def func(x):
    return x ** 2


def test_pass():
    assert func(3) == 9


class Test2:
    def test_d1(self):
        assert 1 == 1
        
    def test_d2(self):
        assert 2 == 2
    
