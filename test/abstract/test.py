# coding: utf-8

import abc


class Shape(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def area(self):
        return 0


class Rectangle(Shape):
    def __init__(self, x, y):
        self.l = x
        self.b = y

    def area(self):
        return self.l * self.b


class NoShape(Shape):
    def __init__(self):
        pass


def test_shape():
    r = Rectangle(10, 20)
    print(f'area: {r.area()}')
    # that is bad
    # n = NoShape()
    # print(f'area: {n.area()}')


if __name__ == "__main__":
    test_shape()
