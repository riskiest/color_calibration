import numpy as np

class Singleton(type):
    _instances = {}
    great = {3,2,1}

    def __call__(cls, *args, **kwargs):
        if (cls, *args) not in cls._instances:
            cls._instances[(cls, *args)] = super(Singleton, cls).__call__(*args, **kwargs)
            print(cls)
            print(cls._instances)
        return cls._instances[(cls, *args)]

# class A(metaclass = Singleton):
#     # print(A._instances)
#     def __init__(self, a = 3):
#         self.a = a

# class B(A):
#     def __init__(self):
#         super().__init__()
#         self.b = 0

# class C:
#     m = 0




# class IdentityMatrix:
#     def __matmul__(self, other):
#         return other

#     def __rmatmul__(self, other):
#         return other

#     __array_priority__ = 1

# class _sRGB():
#     # io = D65_2
#     a = 0.055
#     gamma = 2.4
#     # _linear()

#     def _linear(self):
#         '''
#         linearization parameters
#         see ColorSpace.pdf for details;        
#         '''
#         self.alpha = self.a+1
#         self.K0 = self.a/(self.gamma-1)
#         self.phi = (self.alpha**self.gamma*(self.gamma-1)**(self.gamma-1))/(self.a**(self.gamma-1)*self.gamma**self.gamma)
#         self.beta = self.K0/self.phi

class A:
    i = [10]

class B(A):
    pass
# class A:
#     def __init__(self):
#         self.__name__ = type(self).__name__

# class B(A):
#     def __init__(self):
#         super().__init__()
#         self.c=0

if __name__ == "__main__":
    a = A()
    b = B()
    print(a.i, b.i)
    b.i.append(5)
    print(a.i, b.i)