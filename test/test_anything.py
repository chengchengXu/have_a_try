# coding: utf-8

import sys
import asyncio
import random
import inspect


def test_dict_ref():
    def in_func(x: 'dict'):
        x['add'] = {'vale': 12}

    config = {'r1': 13, 'alpha': ['test', 'reall']}
    in_func(config)
    print(config)


async def func_with_callback():
    print('bbb')
    await asyncio.sleep(random.randint(1, 3))
    print(inspect.stack()[1][3])


async def func_without_callback():
    print('aaa')
    await asyncio.sleep(random.randint(1, 3))
    print(inspect.stack()[1][3])


def test_asyncio_callback():
    # f2 = asyncio.create_task(func_without_callback())
    # f1 = asyncio.create_task(func_with_callback()).add_done_callback(lambda x: print('just print it'))
    # asyncio.get_event_loop().run_until_complete(
    #     asyncio.wait([
    #         f1, f2
    #     ])
    # )
    asyncio.get_event_loop().run_until_complete(
        asyncio.wait([
            func_without_callback(), func_with_callback()
        ])
    )


def test_replace_kwargs():
    # that's a wrong case for multiple values for one keyword
    # x_wapper = {'x': 'warpper_x', 'y': 'warpper_y'}
    # test_replace_kwargs_inner(x=111, **x_wapper)

    x_wrapper = {'x': 'warpper_x'}
    test_replace_kwargs_inner(**x_wrapper, y=111)


def test_replace_kwargs_inner(**kwargs):
    print(kwargs)


class Father():
    @classmethod
    def __init__(self, a):
        self.a = 1 if not a else a
    @classmethod
    def w_1(cls):
        print(cls.a, ' in the first place')
    @classmethod
    def w_2(cls):
        print(cls.a, ' in the second place')
    @classmethod
    def w_3(cls):
        print(cls.a, ' in the third place')
    @classmethod
    def workflow(cls):
        cls.w_1()
        cls.w_2()
        cls.w_3()

class Son():
    @classmethod
    def __init__(self, s):
        super(Son, Son).__init__(3)
        self.b = s
    @classmethod
    def w_2(cls):
        print('Second place with ', cls.a, cls.b)

def test_drive():
    n = Son(11)
    # that's error for Son don't have attribute workflow
    n.workflow()


class TransClassFather:
    def __init__(self, the_class):
        self._the_class = the_class

    def showTheClass(self):
        print(self._the_class._dynamic_data)


class TransClassSon(TransClassFather):
    _dynamic_data = 'abc'
    def __init__(self):
        super().__init__(TransClassSon)

    @staticmethod
    def showTheClass():
        if not hasattr(TransClassSon, '_cmd'):
            TransClassSon._cmd = TransClassSon()
        import random
        TransClassSon._dynamic_data = f'abc.{random.randint(1, 100)}'
        super(TransClassSon, TransClassSon._cmd).showTheClass()


def test_transmit_class_as_parameter():
    TransClassSon.showTheClass()


class TestInheritFather:
    def __init__(self, s):
        self._s = s
    def f1(self):
        print('father f1')
    def f2(self):
        print('father f2')
    def f3(self):
        print('father f3')
    def workflow(self):
        self.f1()
        self.f2()
        self.f3()
    def get_s(self):
        print(self._s)

class TestInheritSon(TestInheritFather):
    def __init__(self):
        super().__init__('aa{bb}cc')
    def f2(self):
        print('son f2')
    def get_s(self):
        print(self._s.replace('{bb}', 'fff'))

def test_inherit():
    a = TestInheritSon()
    a.workflow()
    a.get_s()


if __name__ == "__main__":
    # [print(x) for x in sys.argv]
    # test_dict_ref()
    # test_asyncio_callback()
    # test_replace_kwargs()
    # test_drive()
    # test_transmit_class_as_parameter()
    test_inherit()
