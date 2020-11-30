"""
Python Singleton with parameters (so the same parameters get you the same object)
with support to default arguments and passing arguments as kwargs (but no support for pure kwargs).
And implementation for MongoClient class from pymongo package.
"""
# from pymongo import MongoClient
import inspect


# class Singleton(type):
#     """ Simple Singleton that keep only one value for all instances
#     """
#     def __init__(cls, name, bases, dic):
#         super(Singleton, cls).__init__(name, bases, dic)
#         cls.instance = None

#     def __call__(cls, *args, **kwargs):
#         if cls.instance is None:
#             cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls.instance


class SingletonArgs(type):
    """ Singleton that keep single instance for single set of arguments. E.g.:
    assert SingletonArgs('spam') is not SingletonArgs('eggs')
    assert SingletonArgs('spam') is SingletonArgs('spam')
    Only supports hashable arguments.
    """
    _instances = {}
    # _init = {}

    # def __init__(cls, name, bases, dct):
    #     pass
        # cls._init[cls] = cls.get('__init__', None)
        # cls._init[cls] = cls.__init__
        # parents = inspect.getmro(cls)
        # for parent in parents:
        #     if parent.__init__:
        #         cls._init[cls] = parent.__init__
        #         break
        # print('***:', cls._init)


    def __call__(cls, *args, **kwargs):
        # init = cls._init[cls]
        # if init is not None:
        #     # print('-----')
        #     # ig = inspect.getcallargs(object.__init__, None, *args, **kwargs)
        #     # print(ig)
        #     # print(ig.items())
        #     key = (cls, frozenset(inspect.getcallargs(object.__init__, None, *args, **kwargs).items()))
        # else:
        #     key = cls
        key = (cls, frozenset(inspect.getcallargs(cls.__init__, None, *args, **kwargs).items()))

        if key not in cls._instances:
            cls._instances[key] = super(SingletonArgs, cls).__call__(*args, **kwargs)
        return cls._instances[key]


# class SingletonMongoClient(object):
#     """ Class based on Singleton type to work with MongoDB connections
#     """
#     __metaclass__ = SingletonArgs

#     def __init__(self, url, db_name=None):
#         if db_name:
#             self.connection = MongoClient(url)[db_name]
#         else:
#             self.connection = MongoClient(url).get_default_database()

#     def connection(self):
#         return self.connection


# def db_init(db_name=None):
#     url = 'mongodb://localhost:27017/'
#     c = SingletonMongoClient(url, db_name).connection
#     return c


def tests():
    # class A(object, metaclass=SingletonArgs):
    #     FOO = 'bar'
    #     # pass

    # assert A() is A()

    class B(metaclass=SingletonArgs):
        def __init__(self, key):
            self.key = key
    assert B('key1') is B('key1')
    assert B('key1') is not B('key2')

    class C(metaclass=SingletonArgs):
        def __init__(self, key=None):
            self.key = key

    assert C() is C()
    assert C() is C(None)
    assert C(None) is C(key=None)
    assert C() is C(key=None)
    assert C() is not C('key')
    assert C('key') is C('key')
    assert C('key') is C(key='key')
    assert C('key1') is not C(key='key2')
    assert C(key='key1') is not C(key='key2')

    class D(metaclass=SingletonArgs):
        def __init__(self):
            pass

    class E(metaclass=SingletonArgs):
        def __init__(self):
            pass

    assert D() is not E()

    class F(metaclass=SingletonArgs):
        def __init__(self, k1, k2=None, **kwargs):
            self.k1 = k1
            self.k2 = k2
    
    assert F('k1') is F('k1', None)
    assert F('k1') is not F('k2', None)
    assert F('k1') is F('k1', k2 = None)
    assert F('k1') is F(k2 = None, k1='k1')
    assert F(k1='k1',k2 = None) is F(k2 = None, k1='k1')

    class H(metaclass=SingletonArgs):
        def __init__(self, k1=None, k2=None):
            self.k1 = k1
            self.k2 = k2
    
    assert H('k1') is H('k1', None)
    assert H('k1') is not H('k2', None)
    assert H('k1') is H('k1', k2 = None)
    assert H('k1') is H(k2 = None, k1='k1')
    assert H(k1='k1',k2 = None) is H(k2 = None, k1='k1')    


    class I(H):
        pass
        # def __init__(self, k1=None, k2=None):
        #     self.k1 = k1
        #     self.k2 = k2
    
    assert I('k1') is I('k1', None)
    assert I('k1') is not I('k2', None)
    assert I('k1') is I('k1', k2 = None)
    assert I('k1') is I(k2 = None, k1='k1')
    assert I(k1='k1',k2 = None) is I(k2 = None, k1='k1')    


if __name__ == "__main__":
    tests()